#!/usr/bin/env python3
"""Gen-3 exporter: split.json + mask.json + baked crops  ->  a printable paper.

The two output modes the whole rebuild is for:

  --mode exam     non-compact. Each unit's content shown at size; every writing-space
                  band re-ruled with clean lines to its ORIGINAL provisioned height
                  (spaceHeight). One question per page. Student writes on the paper.

  --mode compact  content only — writing-space dropped, dead-space dropped — flowed
                  back-to-back, then imposed 2-up: two logical A4 pages shrunk onto one
                  landscape A4 sheet (each ~A5). Prints on any A4 printer, saves paper;
                  student works in their own book.

Masks are metadata, so the SAME baked crop feeds both modes — nothing is re-cropped and
the original printed ruled lines never appear (they live in the writing-space band, which
is never shown; exam mode draws fresh lines instead).

    python3 tools/export_paper_v3.py "<paperId>" --mode exam    -o out.pdf
    python3 tools/export_paper_v3.py "<paperId>" --mode compact -o out.pdf
"""
import argparse
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
A4 = fitz.paper_rect("a4")
MARGIN = 42
GAP = 16
LINE_GAP = 26
INK = (0.10, 0.11, 0.14)
GREY = (0.42, 0.45, 0.50)
ACCENT = (0.18, 0.36, 0.92)
RULE = (0.80, 0.83, 0.88)


def bands_of(mask):
    """Ordered (label, f0, f1) fractions of the unit crop height, top to bottom."""
    r0 = mask["regions"][0]
    top = min(r["bbox"][1] for r in mask["regions"])
    bot = max(r["bbox"][3] for r in mask["regions"])
    span = bot - top or 1.0
    out = []
    for r in sorted(mask["regions"], key=lambda r: r["bbox"][1]):
        out.append((r["label"], (r["bbox"][1] - top) / span, (r["bbox"][3] - top) / span))
    return out


def draw_lines(page, x0, x1, y, height):
    yy = y + LINE_GAP
    n = 0
    while yy < y + height - 2:
        page.draw_line((x0, yy), (x1, yy), color=RULE, width=0.6)
        yy += LINE_GAP
        n += 1
    return n


def load(pid):
    wd = WORK / pid
    split = {u["id"]: u for u in json.loads((wd / "split.json").read_text())["units"]}
    order = [u["id"] for u in json.loads((wd / "split.json").read_text())["units"]]
    masks = {m["unitId"]: m for m in json.loads((wd / "mask.json").read_text())["masks"]}
    idx = {u["id"]: u for u in json.loads((wd / "baked_v3" / "index.json").read_text())["units"]}
    return wd, split, order, masks, idx


def place_content(page, crop_doc, f0, f1, dest, scale):
    """Show the [f0,f1] vertical slice of the crop into dest_x,dest_y at scale."""
    cp = crop_doc[0].rect
    clip = fitz.Rect(cp.x0, cp.y0 + f0 * cp.height, cp.x1, cp.y0 + f1 * cp.height)
    dx, dy = dest
    r = fitz.Rect(dx, dy, dx + cp.width * scale, dy + clip.height * scale)
    page.show_pdf_page(r, crop_doc, 0, clip=clip)
    return clip.height * scale


def header(page, unit, i):
    n = unit.get("number")
    tag = f"Question {n}" if n else f"Question {i}"
    if unit.get("part"):
        tag += f" ({unit['part']})"
    page.insert_text((MARGIN, MARGIN), tag, fontsize=12, color=ACCENT, fontname="hebo")
    m = unit.get("marks")
    if m:
        page.insert_text((A4.width - MARGIN - 60, MARGIN), f"{m} marks", fontsize=9, color=GREY)
    page.draw_line((MARGIN, MARGIN + 8), (A4.width - MARGIN, MARGIN + 8), color=RULE, width=0.8)


def export_exam(pid, out):
    wd, split, order, masks, idx = load(pid)
    doc = fitz.open()
    content_w = A4.width - 2 * MARGIN
    for i, uid in enumerate(order, 1):
        unit, mask, meta = split[uid], masks[uid], idx[uid]
        crop = fitz.open(wd / "baked_v3" / meta["file"])
        scale = min(content_w / meta["wpt"], 1.0)
        page = doc.new_page(width=A4.width, height=A4.height)
        header(page, unit, i)
        y = MARGIN + 22
        for label, f0, f1 in bands_of(mask):
            if y > A4.height - MARGIN - 20:
                break
            if label in ("content", "answer-structure"):
                y += place_content(page, crop, f0, f1, (MARGIN, y), scale)
            elif label == "writing-space":
                h = (f1 - f0) * meta["hpt"] * scale
                y += draw_lines(page, MARGIN, A4.width - MARGIN, y, h) * LINE_GAP + LINE_GAP
        crop.close()
    doc.save(out, deflate=True, garbage=4)
    return doc.page_count


def export_compact_flow(pid):
    """Flow content-only units down A4 pages; return an in-memory doc."""
    wd, split, order, masks, idx = load(pid)
    doc = fitz.open()
    content_w = A4.width - 2 * MARGIN
    page = doc.new_page(width=A4.width, height=A4.height)
    y = MARGIN
    for i, uid in enumerate(order, 1):
        unit, mask, meta = split[uid], masks[uid], idx[uid]
        crop = fitz.open(wd / "baked_v3" / meta["file"])
        scale = min(content_w / meta["wpt"], 1.0)
        content = [(f0, f1) for label, f0, f1 in bands_of(mask)
                   if label in ("content", "answer-structure")]
        block_h = 20 + sum((f1 - f0) * meta["hpt"] * scale for f0, f1 in content) + GAP
        if y + block_h > A4.height - MARGIN and y > MARGIN:
            page = doc.new_page(width=A4.width, height=A4.height)
            y = MARGIN
        n = unit.get("number")
        page.insert_text((MARGIN, y + 9), f"Q{n or i}" + (f" ({unit['part']})" if unit.get("part") else ""),
                         fontsize=10, color=ACCENT, fontname="hebo")
        m = unit.get("marks")
        if m:
            page.insert_text((A4.width - MARGIN - 50, y + 9), f"{m} marks", fontsize=8, color=GREY)
        y += 16
        for f0, f1 in content:
            y += place_content(page, crop, f0, f1, (MARGIN, y), scale)
        page.draw_line((MARGIN, y + 6), (A4.width - MARGIN, y + 6), color=RULE, width=0.4)
        y += GAP
        crop.close()
    return doc


def impose_2up(doc):
    """Two portrait A4 logical pages -> one landscape A4 sheet (each scaled 1/sqrt2)."""
    src = doc.tobytes()
    out = fitz.open()
    n = doc.page_count
    LW, LH = A4.height, A4.width          # landscape A4
    half = LW / 2
    for i in range(0, n, 2):
        sheet = out.new_page(width=LW, height=LH)
        for k in range(2):
            if i + k >= n:
                break
            srcdoc = fitz.open("pdf", src)
            sp = srcdoc[i + k].rect
            scale = min(half / sp.width, LH / sp.height)
            w, h = sp.width * scale, sp.height * scale
            x = k * half + (half - w) / 2
            dest = fitz.Rect(x, (LH - h) / 2, x + w, (LH - h) / 2 + h)
            sheet.show_pdf_page(dest, srcdoc, i + k)
            srcdoc.close()
        sheet.draw_line((half, 12), (half, LH - 12), color=RULE, width=0.4, dashes="[4 5] 0")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId")
    ap.add_argument("--mode", choices=["exam", "compact"], default="exam")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    if a.mode == "exam":
        pages = export_exam(a.paperId, a.out)
        print(f"  exam paper: {a.out} ({pages} pages, 1 question/page, re-ruled writing space)")
    else:
        flow = export_compact_flow(a.paperId)
        logical = flow.page_count
        sheet = impose_2up(flow)
        sheet.save(a.out, deflate=True, garbage=4)
        print(f"  compact paper: {a.out} ({logical} logical pages -> {sheet.page_count} landscape A4 2-up sheets)")


if __name__ == "__main__":
    main()
