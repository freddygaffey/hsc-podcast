#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Locate answer regions in a paper's MARKING-GUIDE PDF — deterministic, ZERO tokens.

NESA exams link to a separate marking-guidelines PDF (markingPaperId in papers/_index.json)
holding sample answers / criteria per question. This finds "Question N" / "(a)" anchors in
that PDF and writes the blocks into the EXAM's boundaries.json as markingRegions tagged
{"doc": "marking"}, which bake_questions.py crops from the marking PDF into a<name>.pdf
answer crops. Regions without the doc tag keep pointing at the exam PDF (in-paper solutions),
so existing boundaries behave exactly as before.

MC items (type mc) all get the answer-key table block (the "1 B / 2 D ..." table near the
start of NESA guides) — per-item MC answers are a later refinement.

Run AFTER a locate step, BEFORE bake:

    python3 tools/locate_marking.py "<paperId>"
    python3 tools/locate_marking.py --all      # every _work paper with a linked marking guide
"""
import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"
WORK = PAPERS / "_work"

Q_RE = re.compile(r"^\s*Question\s+(\d+)\b", re.I)
PART_RE = re.compile(r"^\s*\(([a-z]+)\)")
KEY_ROW_RE = re.compile(r"^\s*(\d{1,2})[.)]?\s+([A-D])\s*$")   # MC answer-key table row (OCR)
KEY_HEAD_RE = re.compile(r"multiple.?choice\s+answer\s+key", re.I)
BODY_X0, BODY_X1 = 0.04, 0.97


def page_lines(page):
    """[{text, x0, y0, x1, y1} normalised] top-to-bottom for one page."""
    W, H = page.rect.width, page.rect.height
    out = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            out.append({"text": text,
                        "x0": min(s["bbox"][0] for s in spans) / W,
                        "y0": min(s["bbox"][1] for s in spans) / H,
                        "x1": max(s["bbox"][2] for s in spans) / W,
                        "y1": max(s["bbox"][3] for s in spans) / H})
    out.sort(key=lambda l: l["y0"])
    return out


def ocr_page_lines(page):
    """OCR fallback for scanned marking guides."""
    import io
    import pytesseract
    from PIL import Image
    pix = page.get_pixmap(matrix=fitz.Matrix(110 / 72, 110 / 72))
    img = Image.open(io.BytesIO(pix.tobytes("png")))
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
    lines = [{"text": " ".join(g["words"]), "x0": g["x0"] / W, "y0": g["y0"] / H,
              "x1": g["x1"] / W, "y1": g["y1"] / H} for g in groups.values()]
    lines.sort(key=lambda l: l["y0"])
    return lines


def marking_anchors(doc):
    """Scan the marking PDF. Returns (anchors, key_block):
    anchors = [(number, partLabel|None, page, y)], key_block = (page, y0, y1) of the
    MC answer-key table (None when absent)."""
    born = any(doc[i].get_text("text").strip() for i in range(min(3, len(doc))))
    anchors = []
    key_rows = []      # (page, y0, y1) of "1 B"-style rows (OCR guides)
    key_head = None    # (page, y0) of the "Multiple-choice Answer Key" heading
    key_bottom = {}    # page -> last content line y1
    cur_q = None
    for pg in range(len(doc)):
        lines = page_lines(doc[pg]) if born else ocr_page_lines(doc[pg])
        for l in lines:
            t = l["text"]
            if t.strip():
                key_bottom[pg] = max(key_bottom.get(pg, 0.0), l["y1"])
            if key_head is None and KEY_HEAD_RE.search(t):
                key_head = (pg, l["y0"])
            mq = Q_RE.match(t)
            if mq:
                cur_q = mq.group(1)
                anchors.append((cur_q, None, pg, l["y0"]))
                continue
            mp = PART_RE.match(t)
            if mp and l["x0"] < 0.30 and cur_q is not None:
                anchors.append((cur_q, mp.group(1), pg, l["y0"]))
                continue
            mk = KEY_ROW_RE.match(t)
            if mk and cur_q is None:      # answer-key table sits before the worked answers
                key_rows.append((pg, l["y0"], l["y1"]))
    key_block = None
    if key_head is not None:
        # born-digital guides render the key table as loose cells, not "1 B" lines —
        # crop from the heading to the last content on that page
        pg, y0 = key_head
        key_block = (pg, max(0.0, y0 - 0.01), min(1.0, key_bottom.get(pg, 1.0) + 0.01))
    elif key_rows:
        pg = key_rows[0][0]
        rows = [r for r in key_rows if r[0] == pg]
        key_block = (pg, max(0.0, min(r[1] for r in rows) - 0.02),
                     min(1.0, max(r[2] for r in rows) + 0.01))
    return anchors, key_block


def regions_from_anchors(anchors, page_count):
    """Each anchor's block runs to the next anchor (same page) or the page bottom,
    plus full following pages until the next anchor's page. Returns
    {(number, label): [region, ...]}."""
    out = {}
    for i, (num, label, pg, y) in enumerate(anchors):
        nxt = anchors[i + 1] if i + 1 < len(anchors) else None
        regs = []
        if nxt and nxt[2] == pg:
            regs.append((pg, y, nxt[3]))
        else:
            regs.append((pg, y, 1.0))
            end_pg = nxt[2] if nxt else min(pg + 3, page_count)   # cap runaway spans
            for p in range(pg + 1, end_pg):
                regs.append((p, 0.0, 1.0))
        out[(num, label)] = [
            {"page": p, "bbox": [BODY_X0, max(0.0, y0 - 0.005), BODY_X1, y1], "doc": "marking"}
            for p, y0, y1 in regs]
    return out


def run(paper_id):
    wd = WORK / paper_id
    bpath = wd / "boundaries.json"
    if not bpath.exists():
        print(f"  SKIP {paper_id}: no boundaries.json (run a locate step first)")
        return None
    idx = json.loads((PAPERS / "_index.json").read_text())["papers"]
    me = next((p for p in idx if p["paperId"] == paper_id), None)
    mg = me and me.get("markingPaperId") and next(
        (p for p in idx if p["paperId"] == me["markingPaperId"]), None)
    if not mg or not (PAPERS / mg["path"]).exists():
        print(f"  SKIP {paper_id}: no marking guide linked/found")
        return None

    doc = fitz.open(PAPERS / mg["path"])
    anchors, key_block = marking_anchors(doc)
    blocks = regions_from_anchors(anchors, len(doc))
    boundaries = json.loads(bpath.read_text())

    matched = 0
    for q in boundaries.get("questions", []):
        num = str(q.get("number")) if q.get("number") is not None else None
        if num is None:
            continue
        if q.get("type") == "mc":
            if key_block:
                pg, y0, y1 = key_block
                region = {"page": pg, "bbox": [BODY_X0, y0, BODY_X1, y1], "doc": "marking"}
                for p in q["parts"]:
                    p["markingRegions"] = [r for r in (p.get("markingRegions") or [])
                                           if not r.get("doc")] + [region]
                matched += 1
            continue
        qregions = blocks.get((num, None), [])
        leftovers = list(qregions)
        got_any = False
        for p in q["parts"]:
            pr = blocks.get((num, (p.get("label") or "").lower()))
            if pr:
                p["markingRegions"] = [r for r in (p.get("markingRegions") or [])
                                       if not r.get("doc")] + pr
                got_any = True
        if not got_any and leftovers:
            # no per-part match — hang the whole question block off the first part so the
            # whole-question answer bake is complete
            p0 = q["parts"][0]
            p0["markingRegions"] = [r for r in (p0.get("markingRegions") or [])
                                    if not r.get("doc")] + leftovers
            got_any = True
        matched += got_any
    bpath.write_text(json.dumps(boundaries, indent=2))
    print(f"  {paper_id}: marking regions for {matched}/{len(boundaries.get('questions', []))} "
          f"questions from {mg['path']}" + (" (+ MC key table)" if key_block else ""))
    return matched


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--all":
        for wd in sorted(WORK.iterdir()):
            if wd.is_dir() and (wd / "boundaries.json").exists():
                try:
                    run(wd.name)
                except Exception as e:
                    print(f"  ERROR {wd.name}: {e}")
    else:
        for pid in sys.argv[1:]:
            run(pid)


if __name__ == "__main__":
    main()
