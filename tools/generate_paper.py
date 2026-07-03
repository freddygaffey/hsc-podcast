#!/usr/bin/env python3
"""The generator/converter: build a custom practice paper from the classified question bank.

Reads content/<subject>/questions.json, filters by module/topic/type, picks questions, and
merges their baked per-question PDFs into one print-ready paper — provenance label + writing
space per question, optional answer booklet. This is the engine the UI will wrap.

    python3 tools/generate_paper.py maths-standard-2 --topic "Financial" --count 6 --answers
    python3 tools/generate_paper.py physics --module "Module 5" --count 8 -o /tmp/paper.pdf
"""
import argparse
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
A4 = fitz.paper_rect("a4")
MARGIN = 48
INK = (0.1, 0.11, 0.14)
GREY = (0.42, 0.45, 0.5)
ACCENT = (0.18, 0.36, 0.92)
LINE = (0.8, 0.83, 0.88)


def label_for(r):
    src = r.get("paperSlug", "").replace("-", " ").title()
    m = r.get("marks")
    return f"{src}  ·  {r.get('topic') or r.get('module') or ''}" + (f"  ·  {m} marks" if m else "")


def add_writing_space(page, y, marks):
    """Ruled lines proportional to marks, down the rest of the page."""
    lines = min(max((marks or 1) * 3, 3), int((A4.height - y - MARGIN) / 26))
    for i in range(lines):
        yy = y + 22 + i * 26
        if yy > A4.height - MARGIN:
            break
        page.draw_line((MARGIN, yy), (A4.width - MARGIN, yy), color=LINE, width=0.6)


def place_crop(out, r, qnum, answer=False):
    key = r["answerKey"] if answer else r["assetKey"]
    fp = WORK / r["paperId"] / "baked" / key
    if not fp.exists():
        return
    qpdf = fitz.open(fp)
    qr = qpdf[0].rect
    cw = A4.width - 2 * MARGIN
    scale = min(cw / qr.width, (A4.height * 0.62) / qr.height)   # fit width, cap height
    qh = qr.height * scale
    page = out.new_page(width=A4.width, height=A4.height)
    # header
    tag = f"Answer {qnum}" if answer else f"Question {qnum}"
    page.insert_text((MARGIN, MARGIN), tag, fontsize=12, color=ACCENT, fontname="hebo")
    page.insert_text((MARGIN, MARGIN + 15), label_for(r), fontsize=8.5, color=GREY)
    page.draw_line((MARGIN, MARGIN + 24), (A4.width - MARGIN, MARGIN + 24), color=LINE, width=0.8)
    top = MARGIN + 38
    page.show_pdf_page(fitz.Rect(MARGIN, top, MARGIN + qr.width * scale, top + qh), qpdf, 0)
    if not answer:
        add_writing_space(page, top + qh, r.get("marks"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")
    ap.add_argument("--module", default="")
    ap.add_argument("--topic", default="")
    ap.add_argument("--type", default="")
    ap.add_argument("--count", type=int, default=8)
    ap.add_argument("--answers", action="store_true")
    ap.add_argument("-o", "--out", default="/tmp/practice_paper.pdf")
    a = ap.parse_args()

    recs = json.loads((ROOT / "content" / a.subject / "questions.json").read_text())["questions"]
    def keep(r):
        return ((not a.module or a.module.lower() in (r.get("module") or "").lower())
                and (not a.topic or a.topic.lower() in (r.get("topic") or "").lower())
                and (not a.type or a.type == r.get("type"))
                and (WORK / r["paperId"] / "baked" / r["assetKey"]).exists())
    pool = [r for r in recs if keep(r)]
    if a.answers:
        pool = [r for r in pool if r.get("answerKey")]
    picked = pool[:a.count]
    if not picked:
        raise SystemExit("no questions match those filters")

    out = fitz.open()
    total = sum(r.get("marks") or 0 for r in picked)
    cover = out.new_page(width=A4.width, height=A4.height)
    cover.insert_text((MARGIN, 130), "HSC Practice Paper", fontsize=26, color=INK, fontname="hebo")
    sub = a.subject.replace("-", " ").title()
    filt = " · ".join(x for x in [a.module, a.topic, a.type] if x) or "Mixed"
    cover.insert_text((MARGIN, 165), f"{sub}   —   {filt}", fontsize=12, color=GREY)
    cover.insert_text((MARGIN, 210), f"{len(picked)} questions", fontsize=11, color=INK)
    cover.insert_text((MARGIN, 228), f"{total} marks", fontsize=11, color=INK)
    cover.insert_text((MARGIN, 246), f"Suggested time: {round(total*1.8)} min", fontsize=11, color=INK)
    cover.insert_text((MARGIN, A4.height - 60),
                      "Generated from real HSC past-paper questions · every question traceable to its source",
                      fontsize=8, color=GREY)

    for i, r in enumerate(picked, 1):
        place_crop(out, r, i)
    if a.answers:
        div = out.new_page(width=A4.width, height=A4.height)
        div.insert_text((MARGIN, 130), "Answers", fontsize=22, color=INK, fontname="hebo")
        for i, r in enumerate(picked, 1):
            place_crop(out, r, i, answer=True)

    out.save(a.out, deflate=True, garbage=4)
    print(f"generated {a.out}: {len(picked)} questions, {total} marks, {out.page_count} pages"
          + (" (+answers)" if a.answers else ""))


if __name__ == "__main__":
    main()
