#!/usr/bin/env python3
"""Locate questions from the PDF TEXT LAYER — deterministic, ZERO tokens (born-digital only).

For born-digital papers (a text layer exists), we don't need the vision model to find where
questions are: pymupdf gives every text span with its coordinates, so we regex for question
headings, letter parts, MC items and marks and read their positions directly. Output is the
same boundaries.json the OCR locate step produces (including the `text` of each anchor, so
classification can run on text), so bake_questions.py is unchanged.

Marks come from two styles: inline "(N marks)" in the heading, or the NESA bare digit in
the right margin (x/W ≈ 0.87) — the latter swept up by tools/_marks.py, which also stamps
marksPrinted so bake_questions.py knows whether a crop needs a marks badge.

Scanned papers (no text layer) fall back to locate_ocr.py — this tool skips them. Papers
with garbled font encodings come out with 0 questions; fall back to OCR for those too.

    python3 tools/locate_textlayer.py "<paperId>"
    python3 tools/locate_textlayer.py --all         # every born-digital paper in _work with info.json

Writes papers/_work/<paperId>/boundaries.json (and prints a summary).
"""
import json
import re
import sys
from pathlib import Path

import fitz

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _marks import apply_margin_marks, finalize_marks_printed  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

Q_RE   = re.compile(r"^\s*Question\s+(\d+)\b", re.I)            # "Question 14"
MC_RE  = re.compile(r"^\s*(\d{1,2})[.)]\s")                     # "4." / "12)" MC item at left margin
MC_BARE_RE = re.compile(r"^\s*(\d{1,2})(?:\s+\S.*)?\s*$")       # NESA style: bare "1" (maybe + text)
PART_RE = re.compile(r"^\s*\(([a-z])\)")                        # "(a)" at line start
MARKS_RE = re.compile(r"\((\d+)\s*marks?\)", re.I)             # "(5 marks)"
SOLN_RE = re.compile(r"\b(solution|answer|marking|sample answer|worked)\b", re.I)
CONTINUES_RE = re.compile(r"continues on (the )?(next )?page", re.I)  # pure page-referral, no content
END_RE = re.compile(r"end of (paper|section|question|exam)", re.I)    # terminates the region above it


def lines_with_pos(page):
    """Yield (text, x0, y0, x1, y1) per line, top-to-bottom (point units)."""
    d = page.get_text("dict")
    out = []
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            xs0 = min(s["bbox"][0] for s in spans); ys0 = min(s["bbox"][1] for s in spans)
            xs1 = max(s["bbox"][2] for s in spans); ys1 = max(s["bbox"][3] for s in spans)
            out.append((text, xs0, ys0, xs1, ys1))
    out.sort(key=lambda t: t[2])
    return out


def segment(info, doc):
    """Return (questions, solution_pages, pages_norm) — questions with normalised bboxes."""
    margin_x0, margin_x1 = 0.06, 0.95      # generous body column
    # 1) find every question heading, letter part and MC item, with (page, y).
    anchors = []      # (kind, label, page, y, marks, text)
    solution_pages = set()
    pages_norm = []   # per page: [{text, x0, y0, x1, y1} normalised] — for the margin-marks sweep
    seen_question_heading = False
    last_mc = None    # bare-digit MC items must ascend from 1 (rejects "10 marks" etc.)
    last_part = None  # previous part letter — used to tell (i) the letter from (i) the roman
    for pg in range(info["pageCount"]):
        page = doc[pg]
        W = info["pages"][pg]["wpt"]; H = info["pages"][pg]["hpt"]
        page_lines = lines_with_pos(page)
        pages_norm.append([{"text": t, "x0": x0 / W, "y0": y0 / H, "x1": x1 / W, "y1": y1 / H}
                           for t, x0, y0, x1, y1 in page_lines])
        if any(SOLN_RE.search(t) for t, *_ in page_lines[:4]):
            solution_pages.add(pg)
            continue
        for text, x0, y0, x1, y1 in page_lines:
            if len(text.strip()) < 45 and (CONTINUES_RE.search(text) or END_RE.search(text)):
                # standalone referral/terminator line ("Question 11 continues on next
                # page", "End of paper"): not content — an END anchor caps the region
                # above it (length guard keeps prose mentioning "end of exam" as content)
                anchors.append(("END", None, pg, y0 / H, None, text))
                continue
            mq = Q_RE.match(text)
            if mq:
                seen_question_heading = True
                last_part = None
                mk = MARKS_RE.search(text)
                anchors.append(("Q", mq.group(1), pg, y0 / H,
                                int(mk.group(1)) if mk else None, text))
                continue
            mp = PART_RE.match(text)
            if mp and x0 / W < 0.20:     # parts sit at the left margin
                label = mp.group(1)
                # (i)/(v)/(x) are roman SUBPARTS unless they alphabetically follow the
                # previous letter part — connected subparts stay inside their parent
                # (human ground truth: sub-parts sharing context are ONE unit)
                if label in ("i", "v", "x") and last_part != chr(ord(label) - 1):
                    continue
                last_part = label
                mk = MARKS_RE.search(text)
                anchors.append(("P", label, pg, y0 / H,
                                int(mk.group(1)) if mk else None, text))
                continue
            if not seen_question_heading and x0 / W < 0.16:   # MC section, left margin
                mc = MC_RE.match(text)
                if mc:
                    anchors.append(("MC", mc.group(1), pg, y0 / H, 1, text))
                    last_mc = int(mc.group(1))
                    continue
                mcb = MC_BARE_RE.match(text)
                if mcb:
                    n = int(mcb.group(1))
                    # bare digits are ambiguous ("10 marks", "3 hours") — only accept an
                    # ascending item sequence starting at 1, tolerating small OCR gaps
                    if (last_mc is None and n == 1) or (last_mc is not None and last_mc < n <= last_mc + 3):
                        anchors.append(("MC", str(n), pg, y0 / H, 1, text))
                        last_mc = n
    # ignore anything on solution pages (those become answers, not questions)
    anchors = [a for a in anchors if a[2] not in solution_pages]
    if not anchors:
        return [], solution_pages, pages_norm

    # 2) walk anchors, grouping parts under their question.
    def region(page, y_top, y_bot):
        return {"page": page, "bbox": [margin_x0, max(0.0, y_top - 0.005),
                                       margin_x1, min(1.0, y_bot)]}

    # end of an anchor = next anchor on same page, else bottom of page.
    questions = []
    cur = None
    for i, (kind, label, pg, y, marks, text) in enumerate(anchors):
        if kind == "END":            # terminator only — caps the previous region
            continue
        # find y_bot: next anchor on same page, else page bottom (1.0)
        y_bot = 1.0
        for (k2, l2, p2, y2, m2, t2) in anchors[i + 1:]:
            if p2 == pg and y2 > y:
                y_bot = y2; break
            if p2 != pg:
                break
        reg = region(pg, y, y_bot)
        if kind in ("Q", "MC"):
            cur = {"number": label, "marks": marks, "topic": None, "module": None,
                   "syllabusRefs": [], "type": "mc" if kind == "MC" else None,
                   "marksPrinted": True if (kind == "Q" and marks is not None) else None,
                   "stimulus": [] if kind == "MC" else [reg],
                   "text": text,
                   "parts": ([{"label": None, "marks": marks, "type": "mc",
                               "marksPrinted": None,
                               "regions": [reg], "markingRegions": [], "text": text}]
                             if kind == "MC" else [])}
            questions.append(cur)
        else:  # part
            if cur is None:
                cur = {"number": None, "marks": None, "topic": None, "module": None,
                       "syllabusRefs": [], "type": None, "marksPrinted": None,
                       "stimulus": [], "text": "", "parts": []}
                questions.append(cur)
            cur["parts"].append({"label": label, "marks": marks, "type": None,
                                 "marksPrinted": True if marks is not None else None,
                                 "regions": [reg], "markingRegions": [], "text": text})
    # questions with no letter parts → single null part covering the stimulus region
    for q in questions:
        if not q["parts"]:
            q["parts"] = [{"label": None, "marks": q["marks"], "type": None,
                           "marksPrinted": True if q.get("marksPrinted") else None,
                           "regions": q["stimulus"], "markingRegions": [], "text": q["text"]}]
            q["stimulus"] = []
    # NESA papers print part marks as a bare digit in the right margin — sweep those in
    apply_margin_marks(questions, pages_norm)
    finalize_marks_printed(questions)
    return questions, solution_pages, pages_norm


def run(paper_id):
    wd = WORK / paper_id
    info = json.loads((wd / "info.json").read_text())
    if not info.get("bornDigital"):
        print(f"  SKIP {paper_id}: scanned (needs OCR fallback)")
        return None
    doc = fitz.open(ROOT / "papers" / info["path"])
    questions, soln, _ = segment(info, doc)
    (wd / "boundaries.json").write_text(json.dumps(
        {"paperId": paper_id, "subject": info.get("subject"), "source": "textlayer",
         "questions": questions}, indent=2))
    nparts = sum(len(q["parts"]) for q in questions)
    print(f"  {paper_id}: {len(questions)} questions, {nparts} parts "
          f"({len(soln)} solution pages) [textlayer, 0 tokens]")
    return len(questions)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--all":
        done = 0
        for wd in sorted(WORK.iterdir()):
            if (wd / "info.json").exists():
                if run(wd.name):
                    done += 1
        print(f"segmented {done} born-digital papers")
    else:
        run(sys.argv[1])


if __name__ == "__main__":
    main()
