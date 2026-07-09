#!/usr/bin/env python3
"""Dual segmentation + annotation, for visibility.

Runs BOTH pipelines on a paper and draws both on the FULL page images (uncropped, so you see
the context) so you can see where each model places boundaries and where they agree/disagree:
  - VISION   (Qwen-VL, raw boxes)   -> BLUE   (label on the left)
  - DeepSeek (OCR text -> positioned) -> ORANGE (label on the right)

Agreement between them is the confidence signal. Writes papers/_work/<pid>/annotated/pNN.png
and prints a per-page agreement summary.

    python3 tools/dual_annotate.py <paperId>
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vision_seg as vs  # noqa: E402

WORK = Path(__file__).resolve().parent.parent / "papers" / "_work"
BLUE, ORANGE, GREEN = (30, 90, 220), (230, 120, 0), (15, 160, 60)


def _box(dr, W, H, bbox, color, label, right=False, width=3):
    x0, y0, x1, y1 = bbox[0] * W, bbox[1] * H, bbox[2] * W, bbox[3] * H
    dr.rectangle([x0, y0, x1, y1], outline=color, width=width)
    tx = (x1 - 42) if right else (x0 + 3)
    dr.rectangle([tx - 1, y0, tx + 42, y0 + 12], fill=color)
    dr.text((tx, y0 + 1), label, fill=(255, 255, 255))


def _letter(it):
    return str(it.get("part", "")).strip().lower().strip("().")[:2]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    pid = args[0]
    deepseek = "--deepseek" in sys.argv          # the ORANGE layer costs DeepSeek calls; opt-in
    wd = WORK / pid
    split = json.loads((wd / "split.json").read_text())
    ocr = json.loads((wd / "ocr.json").read_text())
    cp = wd / "vision_cache.json"
    cache = json.loads(cp.read_text()) if cp.exists() else {}

    def lines_for(p):
        return vs.to_lines(ocr[p - 1]) if 0 <= p - 1 < len(ocr) else []
    wsc = {}

    def ws_for(p):
        wsc.setdefault(p, vs.whitespace_rows(pid, p))
        return wsc[p]

    sec2 = split.get("sectionIIStartPage") or 5
    sol = split.get("solutionsStartPage")
    page_q = {}
    for u in split.get("units", []):
        if vs._is_ii(u.get("section")):
            for r in u.get("regions", []):
                page_q.setdefault(r["page"], [])
                if u["number"] not in page_q[r["page"]]:
                    page_q[r["page"]].append(u["number"])
    last = (sol - 1) if sol else (max(page_q) if page_q else sec2)
    out = wd / "annotated"
    out.mkdir(exist_ok=True)

    for p in range(2, last + 1):
        png = wd / f"p{p:02d}.png"
        if not png.exists():
            continue
        img = Image.open(png).convert("RGB")
        W, H = img.size
        dr = ImageDraw.Draw(img)
        wsp, hp = ws_for(p)
        vset, dset = set(), set()
        if p < sec2:
            vb, _ = vs._boxes(pid, p, vs.MC_PROMPT, "questions", cache)
            for it in vb:
                if it.get("bbox") and str(it.get("number", "")).strip().isdigit():
                    _box(dr, W, H, it["bbox"], BLUE, f'V Q{it["number"]}')
                    vset.add(f'q{it["number"]}')
            if deepseek:
                draw, _ = vs._identify(vs.MC_ID_PROMPT + vs.page_text(ocr, p), "questions", cache)
                ditems = [{"n": int(it["number"]), "anchor": it.get("anchor")} for it in draw
                          if str(it.get("number", "")).strip().isdigit()]
                for it, bbox in vs.tile_page(ditems, lines_for(p), wsp, hp):
                    _box(dr, W, H, bbox, ORANGE, f'D Q{it["n"]}', right=True)
                    dset.add(f'q{it["n"]}')
        else:
            qs = page_q.get(p) or ([max(page_q)] if page_q else [11])
            vb, _ = vs._boxes(pid, p, vs.SEC2_PROMPT.replace("{qs}", ", ".join(map(str, qs))),
                              "parts", cache)
            for it in vb:
                if it.get("bbox") and _letter(it):
                    _box(dr, W, H, it["bbox"], BLUE, f'V {it.get("question", "?")}{_letter(it)}')
                    vset.add(f'q{it.get("question")}{_letter(it)}')
            if deepseek:
                draw, _ = vs._identify(
                    vs.SEC2_ID_PROMPT.replace("{qs}", ", ".join(map(str, qs))) + vs.page_text(ocr, p),
                    "parts", cache)
                ditems = [{"q": str(it.get("question", qs[0])), "letter": _letter(it),
                           "anchor": it.get("anchor")} for it in draw if _letter(it)]
                for it, bbox in vs.tile_page(ditems, lines_for(p), wsp, hp):
                    _box(dr, W, H, bbox, ORANGE, f'D {it["q"]}{it["letter"]}', right=True)
                    dset.add(f'q{it["q"]}{it["letter"]}')
        # RAW layers for debugging:
        # content blocks -> purple bars on the far-left margin
        for bt, bb in vs.content_blocks(pid, p):
            dr.rectangle([2, bt * H, 15, bb * H], fill=(150, 60, 200))
        # horizontal rules (buffer-enforced, so diagrams aren't flagged) -> red full-width lines
        rrows, rh = vs.rule_rows(pid, p)
        for r in rrows:
            y = r * H / rh if rh else r
            dr.line([0, y, W, y], fill=(220, 30, 30), width=2)
        # FINAL boxes (from split.json) -> green
        for u in split.get("units", []):
            for r in u.get("regions", []):
                if r["page"] == p:
                    _box(dr, W, H, r["bbox"], GREEN, f'{u["id"]}', width=2)
        img.save(out / f"p{p:02d}.png")
        agree = vset & dset
        print(f"  p{p}: vision={sorted(vset)}  deepseek={sorted(dset)}  "
              f"agree={len(agree)}/{len(vset | dset)}")
    cp.write_text(json.dumps(cache))
    print(f"annotated pages -> {out}")


if __name__ == "__main__":
    main()
