#!/usr/bin/env python3
"""Locate questions via OCR of the rendered pages — deterministic, ZERO LLM tokens.

Why OCR and not the PDF text layer: many school PDFs have broken/subset font encodings, so
the extractable text is garbled ("4XHVWLRQ" for "Question") even though the page looks fine.
OCR reads the PIXELS, so it's immune to that AND works on scanned papers. Tesseract is local
and free. Output is the same boundaries.json the vision locate step produces (plus the OCR
`text` of each question/part, so classification can run on text — no images needed).

    python3 tools/locate_ocr.py "<paperId>"
    python3 tools/locate_ocr.py --all

Writes papers/_work/<paperId>/boundaries.json and caches papers/_work/<paperId>/ocr.json.
"""
import json
import re
import sys
from pathlib import Path

import pytesseract
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _marks import MARGIN_X, apply_margin_marks, finalize_marks_printed, trailing_mark  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

Q_RE    = re.compile(r"^\s*Question\s+(\d+)\b", re.I)
MC_RE   = re.compile(r"^\s*(\d{1,2})[.)]\s")            # "4." / "12)" MC item at left margin
MC_BARE_RE = re.compile(r"^\s*(\d{1,2})(?:\s+\S.*)?\s*$")  # NESA style: bare "1" (maybe + text)
PART_RE = re.compile(r"^\s*\(([a-z])\)")
MARKS_RE = re.compile(r"\((\d+)\s*marks?\)", re.I)
SOLN_RE = re.compile(r"\b(solution|sample answer|marking guidelines?|answers?)\b", re.I)
OPT_RE  = re.compile(r"^\s*[A-D][.)]\s")                # MC option line
CONTINUES_RE = re.compile(r"continues on (the )?(next )?page", re.I)  # pure page-referral, no content
END_RE = re.compile(r"end of (paper|section|question|exam)", re.I)    # terminates the region above it


def ocr_lines(img_path):
    """OCR one page → list of lines: {text, x0,y0,x1,y1} normalised, top-to-bottom."""
    img = Image.open(img_path)
    W, H = img.size
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    groups = {}
    for i, txt in enumerate(d["text"]):
        if not txt.strip() or int(d["conf"][i]) < 30:
            continue
        # split right-margin words (NESA bare mark digits) into their own line, so a
        # "2" printed beside the question text doesn't merge into that text line
        in_margin = d["left"][i] / W >= MARGIN_X
        key = (d["block_num"][i], d["par_num"][i], d["line_num"][i], in_margin)
        g = groups.setdefault(key, {"words": [], "x0": 1e9, "y0": 1e9, "x1": 0, "y1": 0})
        g["words"].append(txt)
        g["x0"] = min(g["x0"], d["left"][i]); g["y0"] = min(g["y0"], d["top"][i])
        g["x1"] = max(g["x1"], d["left"][i] + d["width"][i])
        g["y1"] = max(g["y1"], d["top"][i] + d["height"][i])
    lines = [{"text": " ".join(g["words"]), "x0": g["x0"]/W, "y0": g["y0"]/H,
              "x1": g["x1"]/W, "y1": g["y1"]/H} for g in groups.values()]
    lines.sort(key=lambda l: l["y0"])
    return lines


def segment(info):
    wd = WORK / info["paperId"]
    ocr_cache = wd / "ocr.json"
    if ocr_cache.exists():
        pages = json.loads(ocr_cache.read_text())
    else:
        pages = [ocr_lines(wd / p["image"]) for p in info["pages"]]
        ocr_cache.write_text(json.dumps(pages))

    # detect solution pages (their content becomes answers, not questions)
    soln = {pg for pg, lines in enumerate(pages)
            if any(SOLN_RE.search(l["text"]) for l in lines[:4])}

    anchors = []   # (kind, label, page, y_top, marks, text)
    seen_question_heading = False
    last_mc = None    # bare-digit MC items must ascend from 1 (rejects "10 marks" etc.)
    last_part = None  # previous part letter — tells (i) the letter from (i) the roman
    for pg, lines in enumerate(pages):
        if pg in soln:
            continue
        for l in lines:
            t = l["text"]
            if len(t.strip()) < 45 and (CONTINUES_RE.search(t) or END_RE.search(t)):
                # standalone referral/terminator line — END anchor caps the region above
                anchors.append(("END", None, pg, l["y0"], None, t))
                continue
            mq = Q_RE.match(t)
            if mq:
                seen_question_heading = True
                last_part = None
                mk = MARKS_RE.search(t)
                anchors.append(("Q", mq.group(1), pg, l["y0"], int(mk.group(1)) if mk else None, t))
                continue
            mp = PART_RE.match(t)
            if mp and l["x0"] < 0.22:
                label = mp.group(1)
                # (i)/(v)/(x) are roman SUBPARTS unless they follow the previous letter —
                # connected subparts stay inside their parent part
                if label in ("i", "v", "x") and last_part != chr(ord(label) - 1):
                    continue
                last_part = label
                mk = MARKS_RE.search(t)
                # old OCR caches merge the NESA margin mark digit into this line
                marks = int(mk.group(1)) if mk else trailing_mark(t, l["x1"])
                anchors.append(("P", label, pg, l["y0"], marks, t))
                continue
            if not seen_question_heading and l["x0"] < 0.16:   # MC section, left margin
                mc = MC_RE.match(t)
                if mc:
                    anchors.append(("MC", mc.group(1), pg, l["y0"], 1, t))
                    last_mc = int(mc.group(1))
                    continue
                mcb = MC_BARE_RE.match(t)
                if mcb:
                    n = int(mcb.group(1))
                    # bare digits are ambiguous ("10 marks", "3 hours") — only accept an
                    # ascending item sequence starting at 1, tolerating small OCR gaps
                    if (last_mc is None and n == 1) or (last_mc is not None and last_mc < n <= last_mc + 3):
                        anchors.append(("MC", str(n), pg, l["y0"], 1, t))
                        last_mc = n
    if not anchors:
        return [], soln, pages

    def region(pg, y0, y1):
        return {"page": pg, "bbox": [0.06, max(0.0, y0 - 0.008), 0.95, min(1.0, y1)]}

    questions, cur = [], None
    for i, (kind, label, pg, y, marks, text) in enumerate(anchors):
        if kind == "END":            # terminator only — caps the previous region
            continue
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
        else:
            if cur is None:
                cur = {"number": None, "marks": None, "topic": None, "module": None,
                       "syllabusRefs": [], "type": None, "marksPrinted": None,
                       "stimulus": [], "text": "", "parts": []}
                questions.append(cur)
            cur["parts"].append({"label": label, "marks": marks, "type": None,
                                 "marksPrinted": True if marks is not None else None,
                                 "regions": [reg], "markingRegions": [], "text": text})
    for q in questions:
        if not q["parts"]:
            q["parts"] = [{"label": None, "marks": q["marks"], "type": None,
                           "marksPrinted": True if q.get("marksPrinted") else None,
                           "regions": q["stimulus"], "markingRegions": [], "text": q["text"]}]
            q["stimulus"] = []
    # NESA papers print part marks as a bare digit in the right margin — sweep those in
    apply_margin_marks(questions, pages)
    finalize_marks_printed(questions)
    return questions, soln, pages


def run(paper_id):
    wd = WORK / paper_id
    info = json.loads((wd / "info.json").read_text())
    questions, soln, _ = segment(info)
    (wd / "boundaries.json").write_text(json.dumps(
        {"paperId": paper_id, "subject": info.get("subject"), "source": "ocr",
         "questions": questions}, indent=2))
    nparts = sum(len(q["parts"]) for q in questions)
    print(f"  {paper_id}: {len(questions)} questions, {nparts} parts, "
          f"{len(soln)} soln pages [ocr, 0 tokens]")
    return len(questions)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--all":
        tot = 0
        for wd in sorted(WORK.iterdir()):
            if (wd / "info.json").exists():
                try:
                    tot += run(wd.name) or 0
                except Exception as e:
                    print(f"  ERROR {wd.name}: {e}")
        print(f"done: {tot} questions across all papers")
    else:
        run(sys.argv[1])


if __name__ == "__main__":
    main()
