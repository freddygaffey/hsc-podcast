#!/usr/bin/env python3
"""Compose an annotation PDF from baked crops so a human can mark them up by hand.

One entry per record: a header line (assetKey · Q# · page · marks · lines/space · type ·
refs), a RIGHT / NOT RIGHT checkbox line with room for notes, then the crop itself.
Print it or annotate in a PDF viewer, hand it back, and the pipeline learns from it.

    python3 tools/eval_sheet.py <out.pdf> "<paperId>" [<paperId> ...]
"""
import json
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

PAGE_W, PAGE_H = 595, 842   # A4 pt
M = 36                       # margin
HEADER_H = 30                # metadata + checkbox band per entry
GAP = 14


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out_path = sys.argv[1]
    out = fitz.open()
    page = None
    y = 0.0

    def new_page():
        nonlocal page, y
        page = out.new_page(width=PAGE_W, height=PAGE_H)
        y = M
        return page

    def text(s, size=8, dy=10, bold=False, color=(0.25, 0.25, 0.25)):
        nonlocal y
        page.insert_text((M, y + dy - 2), s, fontsize=size,
                         fontname="hebo" if bold else "helv", color=color)
        y += dy

    new_page()
    n_entries = 0
    for pid in sys.argv[2:]:
        wd = WORK / pid
        q = json.loads((wd / "questions.json").read_text())
        # paper divider
        if y > PAGE_H - 100:
            new_page()
        text(f"PAPER: {q['paperSlug']}   ({q['subject']})   —   {pid}", size=11, dy=20, bold=True, color=(0, 0, 0))
        page.draw_line((M, y), (PAGE_W - M, y), width=1)
        y += 8

        for r in sorted(q["questions"], key=lambda r: r["assetKey"]):
            pdf = wd / "baked" / r["assetKey"]
            if not pdf.exists():
                continue
            src = fitz.open(pdf)
            box = src[0].rect
            scale = min((PAGE_W - 2 * M) / box.width, 1.0)
            crop_h = box.height * scale
            entry_h = HEADER_H + min(crop_h, PAGE_H - 2 * M - HEADER_H) + GAP
            if y + min(entry_h, PAGE_H - 2 * M) > PAGE_H - M:
                new_page()

            meta = [r["assetKey"],
                    f"Q{r.get('questionNumber') or '?'}{r.get('partLabel') or ''}",
                    f"p{r.get('page')}" if r.get("page") else None,
                    f"{r.get('marks')} marks" if r.get("marks") is not None else "marks:?",
                    (f"{r.get('lineCount')} lines/{round(r.get('spaceHeight') or 0)}pt"
                     if r.get("lineCount") is not None else None),
                    r.get("type"), ",".join(r.get("syllabusRefs") or []) or None,
                    r.get("topic")]
            text("  ·  ".join(str(m) for m in meta if m), size=8, dy=11, bold=True)
            text("RIGHT [  ]     NOT RIGHT [  ]     fix: ________________________________"
                 "________________________________________", size=8, dy=12, color=(0.45, 0.45, 0.45))
            y += 4

            if crop_h > PAGE_H - y - M:            # very tall crop: shrink to fit rest of page
                scale2 = min(scale, (PAGE_H - y - M) / box.height)
                crop_h = box.height * scale2
                w = box.width * scale2
            else:
                w = box.width * scale
            dest = fitz.Rect(M, y, M + w, y + crop_h)
            page.draw_rect(dest, color=(0.8, 0.8, 0.8), width=0.5)
            page.show_pdf_page(dest, src, 0)
            y += crop_h + GAP
            n_entries += 1
            src.close()

    out.save(out_path, deflate=True, garbage=4)
    print(f"{out_path}: {n_entries} crops across {len(out)} pages")


if __name__ == "__main__":
    main()
