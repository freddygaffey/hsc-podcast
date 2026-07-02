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

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

Q_RE    = re.compile(r"^\s*Question\s+(\d+)\b", re.I)
MC_RE   = re.compile(r"^\s*(\d{1,2})[.)]\s")            # "4." / "12)" MC item at left margin
PART_RE = re.compile(r"^\s*\(([a-z])\)")
MARKS_RE = re.compile(r"\((\d+)\s*marks?\)", re.I)
SOLN_RE = re.compile(r"\b(solution|sample answer|marking guidelines?|answers?)\b", re.I)
OPT_RE  = re.compile(r"^\s*[A-D][.)]\s")                # MC option line


def ocr_lines(img_path):
    """OCR one page → list of lines: {text, x0,y0,x1,y1} normalised, top-to-bottom."""
    img = Image.open(img_path)
    W, H = img.size
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    groups = {}
    for i, txt in enumerate(d["text"]):
        if not txt.strip() or int(d["conf"][i]) < 30:
            continue
        key = (d["block_num"][i], d["par_num"][i], d["line_num"][i])
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
    for pg, lines in enumerate(pages):
        if pg in soln:
            continue
        for l in lines:
            t = l["text"]
            mq = Q_RE.match(t)
            if mq:
                seen_question_heading = True
                mk = MARKS_RE.search(t)
                anchors.append(("Q", mq.group(1), pg, l["y0"], int(mk.group(1)) if mk else None, t))
                continue
            mp = PART_RE.match(t)
            if mp and l["x0"] < 0.22:
                mk = MARKS_RE.search(t)
                anchors.append(("P", mp.group(1), pg, l["y0"], int(mk.group(1)) if mk else None, t))
                continue
            mc = MC_RE.match(t)
            if mc and not seen_question_heading and l["x0"] < 0.16:   # MC section, left margin
                anchors.append(("MC", mc.group(1), pg, l["y0"], 1, t))
    if not anchors:
        return [], soln, pages

    def region(pg, y0, y1):
        return {"page": pg, "bbox": [0.06, max(0.0, y0 - 0.008), 0.95, min(1.0, y1)]}

    questions, cur = [], None
    for i, (kind, label, pg, y, marks, text) in enumerate(anchors):
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
                   "stimulus": [] if kind == "MC" else [reg],
                   "text": text,
                   "parts": ([{"label": None, "marks": marks, "type": "mc",
                               "regions": [reg], "markingRegions": [], "text": text}]
                             if kind == "MC" else [])}
            questions.append(cur)
        else:
            if cur is None:
                cur = {"number": None, "marks": None, "topic": None, "module": None,
                       "syllabusRefs": [], "type": None, "stimulus": [], "text": "", "parts": []}
                questions.append(cur)
            cur["parts"].append({"label": label, "marks": marks, "type": None,
                                 "regions": [reg], "markingRegions": [], "text": text})
    for q in questions:
        if not q["parts"]:
            q["parts"] = [{"label": None, "marks": q["marks"], "type": None,
                           "regions": q["stimulus"], "markingRegions": [], "text": q["text"]}]
            q["stimulus"] = []
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
