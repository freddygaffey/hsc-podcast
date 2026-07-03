/* paper-export.js — the paper generator's PDF export engine (canonical).
 *
 * Builds a print-ready practice paper from baked question-crop PDFs (pdf-lib merge,
 * fully client-side). generator.html is a thin UI over this; tools/generate_paper.py
 * is a dev smoke-tool only. Design: docs/past-paper-generator.md §5.2 + the
 * review-sheet exemplar (numbered whole questions flowing compactly, provenance line
 * per question, cover block with topics + exam-equivalent time, optional writing space).
 *
 * API:
 *   PaperExport.buildPaper(items, options) ->
 *     Promise<{paper: Uint8Array, answers: Uint8Array|null, skipped: [...], pageCount}>
 *   options.fetchAsset REQUIRED: (item, "question"|"answer") -> Promise<ArrayBuffer>
 *   Preset resolution: {...DEFAULTS, ...PRESETS[options.preset], ...options}
 *
 * Layout: flowing vertical cursor, multiple questions per page. Crops render at
 * near-native scale; a crop taller than a page is SLICED across pages via
 * embedPage(page, boundingBox) with a repeated overlap strip so no text line is lost.
 * All pdf-lib coordinates are bottom-left origin; embedPage boxes are in raw source
 * coords (offset by the crop's own box origin).
 */
(function () {
  "use strict";

  const DEFAULTS = {
    preset: "review-sheet",
    title: "HSC Practice Paper",
    subjectName: "",
    cover: "block",           // "page" | "block" | "none"
    numbering: "sequential",  // "sequential" | "source"
    provenance: true,
    writingSpace: false,      // false | {linesPerMark, minLines, maxLines, lineGap, skipTypes}
    answers: "none",          // "none" | "appended" | "separate"
    minutesPerMark: 1.5,
    pageNumbers: true,
    formatProvenance: null,   // (item) => string
    fetchAsset: null,         // REQUIRED
    onProgress: null,
    page: { w: 595.28, h: 841.89, margin: 42 },
    maxCropScale: 1.0,
    sliceOverlapPt: 12,
    minWidowPt: 90,
    gapAfterQuestion: 14,
  };

  const PRESETS = {
    "review-sheet": { cover: "block", writingSpace: false, answers: "appended" },
    "practice-exam": {
      cover: "page",
      writingSpace: { linesPerMark: 3, minLines: 3, maxLines: 24, lineGap: 26, skipTypes: ["mc"] },
      answers: "separate",
    },
  };

  const INK = { r: 0.10, g: 0.11, b: 0.14 };
  const GREY = { r: 0.42, g: 0.45, b: 0.50 };
  const ACCENT = { r: 0.18, g: 0.36, b: 0.92 };
  const RULE = { r: 0.80, g: 0.83, b: 0.88 };

  // Helvetica is WinAnsi-only — strip anything outside cp1252 so drawText never throws.
  function winAnsi(s) {
    return String(s || "").replace(/[^ -~ -ÿ–—‘’“”·]/g, "?");
  }

  function defaultProvenance(item) {
    const src = (item.paperSlug || "").replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
    const bits = [src];
    if (item.questionNumber) bits.push("Q" + item.questionNumber + (item.partLabel || ""));
    if (item.topic || item.module) bits.push(item.topic || item.module);
    if (item.marks) bits.push(item.marks + " mark" + (item.marks > 1 ? "s" : ""));
    return bits.filter(Boolean).join("  ·  ");
  }

  // ---------- asset prefetch (concurrency-limited, never throws per-item) ----------
  async function prefetch(items, o) {
    const jobs = [];
    for (const item of items) {
      jobs.push({ item, kind: "question" });
      if (o.answers !== "none" && item.answerKey) jobs.push({ item, kind: "answer" });
    }
    const results = new Map(); // item -> {question: bytes|Error, answer: bytes|Error}
    let done = 0, idx = 0;
    async function worker() {
      while (idx < jobs.length) {
        const j = jobs[idx++];
        let got;
        try { got = await o.fetchAsset(j.item, j.kind); if (!got) throw new Error("empty"); }
        catch (e) { got = e instanceof Error ? e : new Error(String(e)); }
        const slot = results.get(j.item) || {};
        slot[j.kind] = got;
        results.set(j.item, slot);
        done++;
        if (o.onProgress) o.onProgress({ stage: "fetch", done, total: jobs.length, item: j.item });
      }
    }
    await Promise.all(Array.from({ length: 4 }, worker));
    return results;
  }

  // ---------- renderer ----------
  function makeDocCtx(PDFLib, doc, fonts, o) {
    const { w: pageW, h: pageH, margin: m } = o.page;
    const ctx = {
      doc, fonts, o, page: null, y: 0,
      contentW: pageW - 2 * m, pageW, pageH, m,
      newPage() {
        this.page = doc.addPage([pageW, pageH]);
        this.y = pageH - m;
        return this.page;
      },
      avail() { return this.page ? this.y - m : 0; },
      text(str, x, y, size, font, color) {
        this.page.drawText(winAnsi(str), { x, y, size, font, color: PDFLib.rgb(color.r, color.g, color.b) });
      },
      line(x1, y1, x2, y2, width, color) {
        this.page.drawLine({ start: { x: x1, y: y1 }, end: { x: x2, y: y2 },
                             thickness: width, color: PDFLib.rgb(color.r, color.g, color.b) });
      },
    };
    return ctx;
  }

  function drawQuestionHeader(ctx, b, continued) {
    const { m } = ctx, o = ctx.o;
    const label = (b.isAnswer ? "Answer " : "Question ") + b.n + (continued ? " (continued)" : "");
    ctx.text(label, m, ctx.y - 11, 11, ctx.fonts.bold, continued ? GREY : ACCENT);
    if (!continued && o.provenance) {
      const prov = (o.formatProvenance || defaultProvenance)(b.item);
      ctx.text(prov, m, ctx.y - 22, 8, ctx.fonts.reg, GREY);
      ctx.line(m, ctx.y - 26, ctx.pageW - m, ctx.y - 26, 0.7, RULE);
      ctx.y -= 30;
    } else {
      ctx.y -= 16;
    }
  }

  async function drawQuestion(PDFLib, ctx, b) {
    const o = ctx.o, m = ctx.m;
    // placeholder for failed fetches — keeps its numbered slot, stays traceable
    if (b.error) {
      const h = 44;
      if (!ctx.page || h + 30 > ctx.avail()) ctx.newPage();
      drawQuestionHeader(ctx, b, false);
      ctx.page.drawRectangle({ x: m, y: ctx.y - h, width: ctx.contentW, height: h,
        borderColor: PDFLib.rgb(RULE.r, RULE.g, RULE.b), borderWidth: 1 });
      ctx.text("This question could not be loaded — " + (o.formatProvenance || defaultProvenance)(b.item),
               m + 10, ctx.y - 26, 9, ctx.fonts.reg, GREY);
      ctx.y -= h + o.gapAfterQuestion;
      return;
    }

    const srcDoc = await PDFLib.PDFDocument.load(b.asset);
    const p0 = srcDoc.getPage(0);
    const box = p0.getCropBox ? p0.getCropBox() : p0.getMediaBox();
    const scale = Math.min(ctx.contentW / box.width, o.maxCropScale);
    const scaledH = box.height * scale;

    // widow control: header + first chunk of crop must fit together
    const headerH = 30;
    if (!ctx.page || headerH + Math.min(scaledH, o.minWidowPt) > ctx.avail()) ctx.newPage();
    drawQuestionHeader(ctx, b, false);

    const ovlSrc = o.sliceOverlapPt / scale;
    let srcTop = box.y + box.height;
    while (srcTop > box.y + 1) {
      const availSrc = ctx.avail() / scale;
      let take = Math.min(availSrc, srcTop - box.y);
      if (take < 2 * ovlSrc && srcTop - box.y > take) {   // sliver — move to fresh page
        ctx.newPage(); drawQuestionHeader(ctx, b, true); continue;
      }
      const emb = await ctx.doc.embedPage(p0, {
        left: box.x, right: box.x + box.width,
        top: srcTop, bottom: srcTop - take,
      });
      ctx.page.drawPage(emb, { x: m, y: ctx.y - take * scale, xScale: scale, yScale: scale });
      ctx.y -= take * scale;
      const remaining = srcTop - take - box.y;
      if (remaining > 1) {
        srcTop -= (take - ovlSrc);       // repeat an overlap strip on the next page
        ctx.newPage();
        drawQuestionHeader(ctx, b, true);
      } else {
        srcTop = box.y;
      }
    }
    ctx.y -= o.gapAfterQuestion;
  }

  function drawWritingSpace(ctx, b) {
    const cfg = b.cfg, m = ctx.m;
    let owed = Math.min(Math.max((b.marks || 1) * cfg.linesPerMark, cfg.minLines), cfg.maxLines);
    // don't orphan a couple of lines at a page bottom
    if (ctx.avail() < cfg.minLines * cfg.lineGap) ctx.newPage();
    while (owed > 0) {
      if (ctx.avail() < cfg.lineGap) { ctx.newPage(); }
      ctx.y -= cfg.lineGap;
      ctx.line(m, ctx.y, ctx.pageW - m, ctx.y, 0.6, RULE);
      owed--;
    }
    ctx.y -= 8;
  }

  function drawCoverBlock(ctx, b) {
    const o = ctx.o, m = ctx.m;
    const topics = b.topics.slice(0, 12);
    const h = 96 + topics.length * 15;
    if (!ctx.page || h > ctx.avail()) ctx.newPage();
    ctx.text(o.title, m, ctx.y - 22, 20, ctx.fonts.bold, INK);
    if (o.subjectName) ctx.text(o.subjectName, m, ctx.y - 40, 11, ctx.fonts.reg, GREY);
    ctx.y -= 56;
    ctx.text(`${b.count} questions   ·   ${b.totalMarks} marks   ·   exam-equivalent time ${Math.round(b.totalMarks * o.minutesPerMark)} min (${o.minutesPerMark} min/mark)`,
             m, ctx.y - 10, 10.5, ctx.fonts.reg, INK);
    ctx.y -= 26;
    if (topics.length) {
      ctx.text("Covers:", m, ctx.y - 10, 10, ctx.fonts.bold, INK);
      ctx.y -= 16;
      for (const t of topics) { ctx.text("·  " + t, m + 10, ctx.y - 10, 10, ctx.fonts.reg, INK); ctx.y -= 15; }
    }
    ctx.line(m, ctx.y - 8, ctx.pageW - m, ctx.y - 8, 1, RULE);
    ctx.y -= 22;
  }

  function drawCoverPage(ctx, b) {
    const o = ctx.o, m = ctx.m;
    ctx.newPage();
    ctx.text(o.title, m, ctx.pageH - 150, 26, ctx.fonts.bold, INK);
    if (o.subjectName) ctx.text(o.subjectName, m, ctx.pageH - 178, 13, ctx.fonts.reg, GREY);
    ctx.text(`${b.count} questions`, m, ctx.pageH - 226, 11, ctx.fonts.reg, INK);
    ctx.text(`${b.totalMarks} marks`, m, ctx.pageH - 244, 11, ctx.fonts.reg, INK);
    ctx.text(`Exam-equivalent time: ${Math.round(b.totalMarks * o.minutesPerMark)} minutes`, m, ctx.pageH - 262, 11, ctx.fonts.reg, INK);
    if (b.topics.length) {
      ctx.text("Covers:", m, ctx.pageH - 300, 11, ctx.fonts.bold, INK);
      b.topics.slice(0, 16).forEach((t, i) =>
        ctx.text("·  " + t, m + 10, ctx.pageH - 320 - i * 16, 10.5, ctx.fonts.reg, INK));
    }
    ctx.text("Generated from real HSC past-paper questions — every question traceable to its source.",
             m, 56, 8, ctx.fonts.reg, GREY);
    ctx.page = null;  // next block starts a fresh page
  }

  function drawSectionHeader(ctx, b) {
    const m = ctx.m;
    ctx.newPage();
    ctx.text(b.text, m, ctx.y - 24, 22, ctx.fonts.bold, INK);
    ctx.line(m, ctx.y - 34, ctx.pageW - m, ctx.y - 34, 1, RULE);
    ctx.y -= 50;
  }

  async function renderDoc(PDFLib, blocks, o) {
    const doc = await PDFLib.PDFDocument.create();
    const fonts = {
      reg: await doc.embedFont(PDFLib.StandardFonts.Helvetica),
      bold: await doc.embedFont(PDFLib.StandardFonts.HelveticaBold),
    };
    const ctx = makeDocCtx(PDFLib, doc, fonts, o);
    let done = 0;
    for (const b of blocks) {
      if (b.type === "coverPage") drawCoverPage(ctx, b);
      else if (b.type === "coverBlock") drawCoverBlock(ctx, b);
      else if (b.type === "sectionHeader") drawSectionHeader(ctx, b);
      else if (b.type === "question") await drawQuestion(PDFLib, ctx, b);
      else if (b.type === "writingSpace") drawWritingSpace(ctx, b);
      done++;
      if (o.onProgress) o.onProgress({ stage: "layout", done, total: blocks.length, item: b.item || null });
    }
    if (o.pageNumbers) {
      const pages = doc.getPages();
      pages.forEach((p, i) => p.drawText(`Page ${i + 1} of ${pages.length}`, {
        x: o.page.w / 2 - 26, y: 24, size: 8, font: fonts.reg,
        color: PDFLib.rgb(GREY.r, GREY.g, GREY.b) }));
    }
    return doc;
  }

  // ---------- plan phase (pure) ----------
  function planBlocks(items, assets, o, forAnswers) {
    const blocks = [];
    const loaded = items.filter(it => !(assets.get(it)?.question instanceof Error));
    if (!forAnswers && o.cover !== "none") {
      const totalMarks = loaded.reduce((s, q) => s + (q.marks || 0), 0);
      // multi-part questions carry slash-joined topic strings — split so the cover
      // lists each syllabus area once
      const topics = [...new Set(loaded.flatMap(q =>
        String(q.topic || q.module || "").split(/\s*\/\s*/)).filter(Boolean))];
      blocks.push({ type: o.cover === "page" ? "coverPage" : "coverBlock",
                    count: loaded.length, totalMarks, topics });
    }
    items.forEach((item, i) => {
      const n = o.numbering === "source" && item.questionNumber ? item.questionNumber : i + 1;
      const slot = assets.get(item) || {};
      if (forAnswers) {
        if (slot.question instanceof Error) return;             // question itself failed
        if (!item.answerKey || !slot.answer || slot.answer instanceof Error) return;
        blocks.push({ type: "question", n, item, asset: slot.answer, isAnswer: true });
        return;
      }
      if (slot.question instanceof Error) {
        blocks.push({ type: "question", n, item, error: slot.question });
      } else {
        blocks.push({ type: "question", n, item, asset: slot.question });
        if (o.writingSpace && !(o.writingSpace.skipTypes || []).includes(item.type)) {
          blocks.push({ type: "writingSpace", marks: item.marks, cfg: o.writingSpace, item });
        }
      }
    });
    return blocks;
  }

  // ---------- public entry ----------
  async function buildPaper(items, options) {
    const PDFLib = window.PDFLib;
    if (!PDFLib) throw new Error("pdf-lib not loaded");
    const o = { ...DEFAULTS, ...(PRESETS[options.preset] || {}), ...options };
    if (typeof o.fetchAsset !== "function") throw new Error("options.fetchAsset is required");
    if (!items.length) throw new Error("no questions selected");

    const assets = await prefetch(items, o);
    const skipped = [];
    for (const [item, slot] of assets) {
      if (slot.question instanceof Error) skipped.push({ item, kind: "question", error: slot.question.message });
      else if (slot.answer instanceof Error) skipped.push({ item, kind: "answer", error: slot.answer.message });
    }
    if (skipped.filter(s => s.kind === "question").length === items.length) {
      throw new Error("every question failed to load");
    }

    const blocks = planBlocks(items, assets, o, false);
    let answerBlocks = o.answers === "none" ? [] : planBlocks(items, assets, o, true);
    if (o.answers === "appended" && answerBlocks.length) {
      blocks.push({ type: "sectionHeader", text: "Answers" }, ...answerBlocks);
      answerBlocks = [];
    }

    const doc = await renderDoc(PDFLib, blocks, o);
    let answersOut = null;
    if (o.answers === "separate" && answerBlocks.length) {
      const adoc = await renderDoc(PDFLib, [{ type: "sectionHeader", text: "Answers" }, ...answerBlocks], o);
      answersOut = await adoc.save();
    }
    if (o.onProgress) o.onProgress({ stage: "save", done: 1, total: 1, item: null });
    return { paper: await doc.save(), answers: answersOut,
             skipped, pageCount: doc.getPageCount() };
  }

  window.PaperExport = { buildPaper, PRESETS, DEFAULTS };
})();
