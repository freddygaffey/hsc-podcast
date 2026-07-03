#!/usr/bin/env python3
"""Step 3 of segmentation: bake per-question (and per-answer) PDFs from boundaries.json.

Deterministic — no LLM. Reads papers/_work/<paperId>/{info.json,boundaries.json}, crops each
question PART's region(s) from the ORIGINAL PDF. Files are named by QUESTION NUMBER and grouped
by PAPER, mirroring the UI (subject -> paper -> questions):

  R2 / bucket:  <subject>/papers/<paperSlug>/paper.pdf  (full original exam)
                <subject>/<paperSlug>/q<num><part>.pdf  (question, e.g. q17b.pdf, q01.pdf)
                <subject>/<paperSlug>/a<num><part>.pdf  (its answer, where a solution exists)
  local stage:  papers/_work/<paperId>/baked/
  meta:         content/<subject>/questions.json

Each record still carries the content hash as `id` (stable, dedupe-detection), but the file is
named by number. Granularity (D4): atomic unit = LETTER PART; romans bundled; shared stem rides.

    python3 tools/bake_questions.py "<paperId>"                    # bake locally
    python3 tools/bake_questions.py "<paperId>" --upload hsc-questions   # bake + push to R2
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"
WORK = PAPERS / "_work"
FOOTER_CLIP_PT = 40   # trim page numbers/footers off crop bottoms that reach the page edge


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def paper_meta_for(paper_id):
    """(subjectSlug, paperSlug, sourcePath, year) from papers/_index.json. paperSlug is a
    readable folder name, e.g. '2019-hsc' or '2020-barker-trial'."""
    idx = PAPERS / "_index.json"
    if idx.exists():
        for p in json.loads(idx.read_text())["papers"]:
            if p["paperId"] == paper_id:
                subj = slug(p["subject"])
                year = p.get("year") or "unknown"
                sch = slug(p.get("school") or "")
                kind = p.get("kind") or "paper"
                var = slug(p.get("variant") or "")
                if kind == "hsc":
                    ps = f"{year}-hsc"
                elif sch:
                    # use the school for ANY kind — "unknown"-kind papers from the same
                    # year used to collapse onto one slug and collide in the bucket/UI
                    ps = f"{year}-{sch}" + (f"-{kind}" if kind not in ("unknown", "paper") else "")
                else:
                    ps = f"{year}-{kind}"
                if var:
                    ps += f"-{var}"
                if ps == f"{year}-unknown":
                    # last resort: keep the slug unique per source paper
                    ps = f"{year}-{hashlib.md5(paper_id.encode()).hexdigest()[:6]}"
                return subj, ps, p["path"], p.get("year")
    return "misc", slug(paper_id), None, None


def marking_doc_for(paper_id):
    """Open the linked marking-guide PDF for regions tagged doc:"marking".
    Returns (fitz doc, bornDigital) or None when no marking guide is linked."""
    idx = PAPERS / "_index.json"
    if not idx.exists():
        return None
    papers = json.loads(idx.read_text())["papers"]
    me = next((p for p in papers if p["paperId"] == paper_id), None)
    if not me or not me.get("markingPaperId"):
        return None
    mg = next((p for p in papers if p["paperId"] == me["markingPaperId"]), None)
    if not mg or not (PAPERS / mg["path"]).exists():
        return None
    doc = fitz.open(PAPERS / mg["path"])
    born = any(doc[i].get_text("text").strip() for i in range(min(3, len(doc))))
    return doc, born


def stamp_marks(page, marks):
    """Draw a small "N marks" badge top-right — used when marks are known but the
    printed marks fell outside the crop, so the student still sees the weighting."""
    label = f"{marks} mark" + ("s" if marks != 1 else "")
    w = fitz.get_text_length(label, fontname="helv", fontsize=8) + 10
    r = fitz.Rect(page.rect.x1 - w - 6, 4, page.rect.x1 - 6, 18)
    page.draw_rect(r, color=(0.45, 0.45, 0.45), fill=(0.97, 0.97, 0.97), width=0.5, radius=0.3)
    page.insert_textbox(r, label, fontname="helv", fontsize=8,
                        align=fitz.TEXT_ALIGN_CENTER, color=(0.2, 0.2, 0.2))


def numkey(number, label):
    """'17','b' -> '17b'; '1',None -> '01'; pads the numeric part for sorting."""
    num = (str(number) if number is not None else "").strip()
    m = re.match(r"(\d+)(.*)", num)
    base = (m.group(1).zfill(2) + slug(m.group(2))) if m else (slug(num) or "x")
    return f"{base}{(label or '').lower()}"


def bake_region_pdf(src, info, regions, marking=None, badge_marks=None, strip_lines=True):
    """Stack the region rectangles vertically into one single-page PDF (bytes).

    `clip` is always given in DISPLAY (post-rotation) space — the same space
    pNN.png / boundaries.json bboxes use (`pg["wpt"]/["hpt"]` are the display
    dims). `get_pixmap(clip=...)` correctly honours the page's own /Rotate
    when given a display-space clip; `show_pdf_page(clip=...)` does NOT, so
    it's only safe to use on upright (rotation == 0) pages.

    Regions tagged doc:"marking" crop from the linked marking-guide PDF
    (`marking` = (doc, bornDigital)); their dims come from that doc's pages.
    `badge_marks` stamps an "N marks" badge top-right — output is byte-identical
    to the pre-badge bake when it is None.

    `strip_lines` (default): regions annotated with linesTopY by detect_lines.py are
    trimmed there — the canonical crop excludes the printed ruled writing lines, and
    the generator re-renders `lineCount` clean lines at export time. Regions that
    were nothing but lines vanish; returns None when every region does."""
    born = info["bornDigital"]
    pages = {p["page"]: p for p in info["pages"]}
    rects = []
    for r in regions:
        x0, y0, x1, y1 = r["bbox"]
        if strip_lines and not r.get("doc"):
            if r.get("linesTopY"):
                y1 = min(y1, r["linesTopY"])
            elif r.get("contentBottomY"):     # tighten to content (blank-space papers)
                y1 = min(y1, r["contentBottomY"])
        if r.get("doc") == "marking":
            if marking is None:
                continue
            mdoc, mborn = marking
            mp = mdoc[r["page"]]
            W, H = mp.rect.width, mp.rect.height
            clip = fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H)
            rects.append((mdoc, r["page"], clip, mp.rotation % 360, mborn))
        else:
            pg = pages[r["page"]]
            # page numbers/footers don't belong in the crop — provenance renders
            # in the header at export time instead
            y1c = min(y1, 1.0 - FOOTER_CLIP_PT / pg["hpt"]) if y1 > 0.9 else y1
            clip = fitz.Rect(x0 * pg["wpt"], y0 * pg["hpt"], x1 * pg["wpt"], y1c * pg["hpt"])
            if clip.height < 8:      # region was nothing but ruled lines — drop it
                continue
            rects.append((src, r["page"], clip, pg.get("rotation", 0) % 360, born))
    if not rects:
        return None
    out = fitz.open()
    width = max(clip.width for _, _, clip, _, _ in rects)
    total_h = sum(clip.height for _, _, clip, _, _ in rects)
    page = out.new_page(width=width, height=total_h)
    y = 0.0
    for doc, pno, clip, rotation, b in rects:
        dest = fitz.Rect(0, y, clip.width, y + clip.height)
        if b and rotation == 0:
            page.show_pdf_page(dest, doc, pno, clip=clip)                    # vector
        else:
            pix = doc[pno].get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip)   # raster (rotation-safe)
            page.insert_image(dest, pixmap=pix)
        y += clip.height
    if badge_marks is not None:
        stamp_marks(page, badge_marks)
    data = out.tobytes(deflate=True, garbage=4)
    out.close()
    return data


def r2_put(bucket, key, path):
    subprocess.run(["wrangler", "r2", "object", "put", f"{bucket}/{key}",
                    "--file", str(path), "--remote"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    bucket = None
    if "--upload" in args:
        i = args.index("--upload")
        bucket = args[i + 1]
        del args[i:i + 2]
    strip_lines = "--keep-lines" not in args
    if not strip_lines:
        args.remove("--keep-lines")
    # the marks badge is a RENDER-time concern now (provenance header); only stamp
    # into the crop bytes when explicitly asked
    stamp = "--stamp-marks" in args
    if stamp:
        args.remove("--stamp-marks")
    paper_id = args[0]

    wd = WORK / paper_id
    info = json.loads((wd / "info.json").read_text())
    bounds = json.loads((wd / "boundaries.json").read_text())
    subj, paper_slug, src_rel, paper_year = paper_meta_for(paper_id)
    if info.get("subject"):
        subj = info["subject"]
    baked = wd / "baked"
    baked.mkdir(exist_ok=True)
    for old in baked.glob("*.pdf"):        # clear stale files so re-bakes don't leave orphans
        old.unlink()
    src = fitz.open(ROOT / "papers" / info["path"])
    # open the marking-guide PDF only when some region actually points at it
    marking = None
    if any(r.get("doc") == "marking"
           for q in bounds["questions"] for p in (q.get("parts") or [])
           for r in (p.get("markingRegions") or [])):
        marking = marking_doc_for(paper_id)
        if marking is None:
            print(f"  WARN {paper_id}: doc:'marking' regions but no marking guide resolvable")

    # Merge continuation entries ("Question 11 (continued)" pages are detected as a second
    # question with the same number) into their parent so the whole-question bake is complete.
    merged, by_num = [], {}
    for q in bounds["questions"]:
        num = str(q.get("number")) if q.get("number") is not None else None
        prev = by_num.get(num)
        if prev is not None and num is not None:
            prev["stimulus"] = (prev.get("stimulus") or []) + (q.get("stimulus") or [])
            if prev.get("parts") or q.get("parts"):
                prev["parts"] = (prev.get("parts") or []) + (q.get("parts") or [])
            else:
                prev["regions"] = (prev.get("regions") or []) + (q.get("regions") or [])
            prev["marks"] = prev.get("marks") or q.get("marks")
            if prev.get("lineCount") is not None or q.get("lineCount") is not None:
                prev["lineCount"] = (prev.get("lineCount") or 0) + (q.get("lineCount") or 0)
            if prev.get("spaceHeight") is not None or q.get("spaceHeight") is not None:
                prev["spaceHeight"] = round((prev.get("spaceHeight") or 0.0)
                                            + (q.get("spaceHeight") or 0.0), 1)
            if q.get("marksPrinted"):
                prev["marksPrinted"] = True
        else:
            merged.append(q)
            if num is not None:
                by_num[num] = q
    bounds = {**bounds, "questions": merged}

    records = []
    used = set()
    for qi, q in enumerate(bounds["questions"]):
        stim = q.get("stimulus", [])
        parts = q.get("parts") or [{"label": None, "marks": q.get("marks"),
                                    "type": q.get("type"), "regions": q.get("regions", []),
                                    "markingRegions": q.get("markingRegions", [])}]
        # Whole-question bake (the generator's display unit — parts are metadata only):
        # stem/stimulus once, then every part's regions in order. Only for questions with
        # LABELLED parts — partless questions (locate's single null-label fallback part)
        # are baked once by the loop below; baking them here too produced byte-identical
        # qNN.pdf / qNN-1.pdf duplicate crops.
        # Booklet-style questions ("Question 11 (15 marks)" holding independent lettered
        # parts) display as PARTS, not the 15-mark bundle — matches human annotation
        # ground truth. The whole-question record stays for answers/reference as a
        # "bundle" unit the generator doesn't list.
        n_labelled = sum(1 for p in parts if p.get("label"))
        booklet = n_labelled >= 2 and (q.get("marks") or 0) >= 10
        if any(p.get("label") for p in parts):
            wregions = stim + [r for part in parts for r in part.get("regions", [])]
            wmarking = [r for part in parts for r in part.get("markingRegions") or []]
            pmarks = [p.get("marks") for p in parts]
            wmarks = q.get("marks") or (sum(m for m in pmarks if m) or None)
            # badge only on an explicit marksPrinted=False AND --stamp-marks — the render
            # header shows marks by default, keeping crop bytes clean
            badge = wmarks if (stamp and wmarks is not None and q.get("marksPrinted") is False) else None
            data = bake_region_pdf(src, info, wregions, marking=marking, badge_marks=badge,
                                   strip_lines=strip_lines)
            if data is None:      # every region was ruled lines only — nothing to ship
                continue
            qid = hashlib.sha256(data).hexdigest()[:12]
            name = numkey(q.get("number") or (qi + 1), None)
            base, k = name, 1
            while name in used:            # e.g. two number-less parted questions
                name = f"{base}-{k}"; k += 1
            used.add(name)
            (baked / f"q{name}.pdf").write_bytes(data)
            answer_key = None
            if wmarking:
                adata = bake_region_pdf(src, info, wmarking, marking=marking)
                if adata is not None:
                    (baked / f"a{name}.pdf").write_bytes(adata)
                    answer_key = f"a{name}.pdf"
            wpage = next((r["page"] + 1 for r in wregions if not r.get("doc")), None)
            records.append({
                "id": qid, "subject": subj, "paperSlug": paper_slug,
                "assetKey": f"q{name}.pdf", "answerKey": answer_key,
                "paperId": info["paperId"], "questionNumber": q.get("number"),
                "partLabel": None, "year": paper_year, "page": wpage,
                "marks": wmarks,
                "questionMarks": q.get("marks"), "type": q.get("type"),
                "topic": q.get("topic"), "module": q.get("module"),
                "syllabusRefs": q.get("syllabusRefs") or [],
                "lineCount": q.get("lineCount"), "spaceHeight": q.get("spaceHeight"),
                "marksPrinted": q.get("marksPrinted"),
                "hasStimulus": bool(stim), "bytes": len(data),
                "unit": "bundle" if booklet else "question",
                "parts": [p.get("label") for p in parts if p.get("label")],
            })
        for part in parts:
            # continuation pages ("Question 15 (continued)" + ruled lines) are already
            # inside the whole-question bake; with lines stripped they'd be header-only
            # fragments, so don't emit them as their own records
            if (strip_lines and part.get("label") is None
                    and re.search(r"\bcontinued\b", part.get("text") or "", re.I)):
                continue
            badge = (part["marks"] if (stamp and part.get("marks") is not None
                                       and part.get("marksPrinted") is False) else None)
            # booklet parts are independent problems — the "Question N (15 marks)"
            # heading/stimulus belongs to the bundle, not to each part's crop
            pstim = [] if (booklet and part.get("label")) else stim
            data = bake_region_pdf(src, info, pstim + part["regions"],  # stem rides with part
                                   marking=marking, badge_marks=badge,
                                   strip_lines=strip_lines)
            if data is None:      # pure ruled-lines fragment (continuation page) — drop it
                continue
            qid = hashlib.sha256(data).hexdigest()[:12]                 # content id (dedupe)
            name = numkey(q.get("number") or (qi + 1), part.get("label"))
            base = name
            k = 1
            while name in used:            # disambiguate rare collisions
                name = f"{base}-{k}"; k += 1
            used.add(name)
            (baked / f"q{name}.pdf").write_bytes(data)

            answer_key = None
            mr = part.get("markingRegions") or []
            if mr:                                                      # bake the paired answer
                adata = bake_region_pdf(src, info, mr, marking=marking)
                if adata is not None:
                    (baked / f"a{name}.pdf").write_bytes(adata)
                    answer_key = f"a{name}.pdf"

            ppage = next((r["page"] + 1 for r in (pstim + part["regions"]) if not r.get("doc")), None)
            records.append({
                "id": qid, "subject": subj, "paperSlug": paper_slug,
                "assetKey": f"q{name}.pdf", "answerKey": answer_key,
                "paperId": info["paperId"], "questionNumber": q.get("number"),
                "partLabel": part.get("label"), "year": paper_year, "page": ppage,
                "marks": part.get("marks"),
                "questionMarks": q.get("marks"), "type": part.get("type") or q.get("type"),
                "topic": q.get("topic"), "module": q.get("module"),
                "syllabusRefs": q.get("syllabusRefs") or [],
                "lineCount": part.get("lineCount"), "spaceHeight": part.get("spaceHeight"),
                "marksPrinted": part.get("marksPrinted"),
                "hasStimulus": bool(pstim), "bytes": len(data),
                "unit": ("question" if part.get("label") is None
                         else ("question" if booklet else "part")),
            })

    (wd / "questions.json").write_text(json.dumps(
        {"subject": subj, "paperSlug": paper_slug, "questions": records}, indent=2))

    n_ans = sum(1 for r in records if r["answerKey"])
    total = sum(r["bytes"] for r in records)
    print(f"{paper_id}: {len(records)} parts ({n_ans} answers) -> {subj}/{paper_slug}/  "
          f"({total/1024:.0f} KB)")

    if bucket:
        # full original paper
        if src_rel and (PAPERS / src_rel).exists():
            r2_put(bucket, f"{subj}/papers/{paper_slug}/paper.pdf", PAPERS / src_rel)
        for r in records:
            r2_put(bucket, f"{subj}/papers/{paper_slug}/{r['assetKey']}", baked / r["assetKey"])
            if r["answerKey"]:
                r2_put(bucket, f"{subj}/papers/{paper_slug}/{r['answerKey']}", baked / r["answerKey"])
        print(f"  uploaded to {bucket}/{subj}/papers/{paper_slug}/")


if __name__ == "__main__":
    main()
