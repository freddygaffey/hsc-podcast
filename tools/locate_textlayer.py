#!/usr/bin/env python3
"""Locate questions from the PDF TEXT LAYER — deterministic, ZERO tokens (born-digital only).

For born-digital papers (a text layer exists), we don't need the vision model to find where
questions are: pymupdf gives every text span with its coordinates, so we regex for question
headings, letter parts, and marks and read their positions directly. Output is the same
boundaries.json the vision locate step produces, so bake_questions.py is unchanged.

Scanned papers (no text layer) fall back to the vision agent — this tool skips them.

    python3 tools/locate_textlayer.py "<paperId>"
    python3 tools/locate_textlayer.py --all         # every born-digital paper in _work with info.json

Writes papers/_work/<paperId>/boundaries.json (and prints a summary).
"""
import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

Q_RE   = re.compile(r"^\s*Question\s+(\d+)\b", re.I)            # "Question 14"
PART_RE = re.compile(r"^\s*\(([a-z])\)")                        # "(a)" at line start
MARKS_RE = re.compile(r"\((\d+)\s*marks?\)", re.I)             # "(5 marks)"
SOLN_RE = re.compile(r"\b(solution|answer|marking|sample answer|worked)\b", re.I)


def lines_with_pos(page):
    """Yield (text, x0, y0, x1, y1) per line, top-to-bottom."""
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
    """Return a list of question dicts with normalised bboxes, from the text layer."""
    W = info["pages"][0]["wpt"]; H = info["pages"][0]["hpt"]
    margin_x0, margin_x1 = 0.06, 0.95      # generous body column
    # 1) find every question heading + letter part, with (page, y).
    anchors = []      # (kind, label, page, y, marks)
    solution_pages = set()
    for pg in range(info["pageCount"]):
        page = doc[pg]
        page_lines = lines_with_pos(page)
        if any(SOLN_RE.search(t) for t, *_ in page_lines[:4]):
            solution_pages.add(pg)
        for text, x0, y0, x1, y1 in page_lines:
            mq = Q_RE.match(text)
            if mq:
                mk = MARKS_RE.search(text)
                anchors.append(("Q", mq.group(1), pg, y0 / info["pages"][pg]["hpt"],
                                int(mk.group(1)) if mk else None))
                continue
            mp = PART_RE.match(text)
            if mp and x0 / info["pages"][pg]["wpt"] < 0.20:     # parts sit at the left margin
                mk = MARKS_RE.search(text)
                anchors.append(("P", mp.group(1), pg, y0 / info["pages"][pg]["hpt"],
                                int(mk.group(1)) if mk else None))
    # ignore anything on solution pages (those become answers, not questions)
    anchors = [a for a in anchors if a[2] not in solution_pages]
    if not anchors:
        return [], solution_pages

    # 2) walk anchors, grouping parts under their question.
    def region(page, y_top, y_bot):
        h = info["pages"][page]["hpt"]
        return {"page": page, "bbox": [margin_x0, max(0.0, y_top - 0.005),
                                       margin_x1, min(1.0, y_bot)]}

    # end of an anchor = next anchor on same page, else bottom of page.
    questions = []
    cur = None
    for i, (kind, label, pg, y, marks) in enumerate(anchors):
        # find y_bot: next anchor on same page, else page bottom (1.0)
        y_bot = 1.0
        for (k2, l2, p2, y2, m2) in anchors[i + 1:]:
            if p2 == pg and y2 > y:
                y_bot = y2; break
            if p2 != pg:
                break
        if kind == "Q":
            cur = {"number": label, "marks": marks, "topic": None,
                   "stimulus": [region(pg, y, y_bot)], "parts": []}
            questions.append(cur)
        else:  # part
            if cur is None:
                cur = {"number": None, "marks": None, "topic": None, "stimulus": [], "parts": []}
                questions.append(cur)
            cur["parts"].append({"label": label, "marks": marks, "type": None,
                                 "regions": [region(pg, y, y_bot)], "markingRegions": []})
    # questions with no letter parts → single null part covering the stimulus region
    for q in questions:
        if not q["parts"]:
            q["parts"] = [{"label": None, "marks": q["marks"], "type": None,
                           "regions": q["stimulus"], "markingRegions": []}]
            q["stimulus"] = []
    return questions, solution_pages


def run(paper_id):
    wd = WORK / paper_id
    info = json.loads((wd / "info.json").read_text())
    if not info.get("bornDigital"):
        print(f"  SKIP {paper_id}: scanned (needs vision fallback)")
        return None
    doc = fitz.open(ROOT / "papers" / info["path"])
    questions, soln = segment(info, doc)
    (wd / "boundaries.json").write_text(json.dumps(
        {"paperId": paper_id, "source": "textlayer", "questions": questions}, indent=2))
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
