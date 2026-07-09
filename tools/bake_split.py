#!/usr/bin/env python3
"""split.json + source PDF  ->  one lossless oversized PDF per unit (Gen-3 bake).

The bake is a deterministic *cache* of split.json, not a stage with its own truth: it
crops each unit's region from the source PDF, vectors preserved, onto a page exactly the
region's size (no A4 fitting, nothing clipped). The generator later applies mask.json to
this crop to decide content vs writing-space vs dead-space per output mode.

    python3 tools/bake_split.py "<paperId>"
Writes papers/_work/<paperId>/baked_v3/<unitId>.pdf and an index.json.
"""
import json
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def _resolve_src(pid, info):
    """Find the source PDF via the LIVE index (paperId -> current path) first, so a rework
    of papers/ doesn't break the bake; fall back to the frozen info.json path."""
    idxp = ROOT / "papers" / "_index.json"
    if idxp.exists():
        for p in json.loads(idxp.read_text()).get("papers", []):
            if p.get("paperId") == pid and p.get("path"):
                cand = ROOT / "papers" / p["path"]
                if cand.exists():
                    return cand
    cand = ROOT / "papers" / info.get("path", "")
    if cand.exists():
        return cand
    raise SystemExit(f"source PDF not found for {pid} (index + info.json path both stale)")


def main():
    pid = sys.argv[1]
    wd = WORK / pid
    split = json.loads((wd / "split.json").read_text())
    info = json.loads((wd / "info.json").read_text())
    src = fitz.open(_resolve_src(pid, info))

    out_dir = wd / "baked_v3"
    out_dir.mkdir(exist_ok=True)
    index = []
    for u in split["units"]:
        doc = fitz.open()
        for r in u["regions"]:                     # all regions -> one crop (multi-page = continuation)
            pidx = r["page"] - 1                    # split.json page is 1-based; fitz + info.pages are 0-based
            if not (0 <= pidx < src.page_count) or pidx >= len(info["pages"]):
                continue
            pg = info["pages"][pidx]
            wpt, hpt = pg["wpt"], pg["hpt"]
            x0, y0, x1, y1 = r["bbox"]
            clip = fitz.Rect(x0 * wpt, y0 * hpt, x1 * wpt, y1 * hpt)
            np_ = doc.new_page(width=clip.width, height=clip.height)
            np_.show_pdf_page(fitz.Rect(0, 0, clip.width, clip.height), src, pidx, clip=clip)
        if doc.page_count == 0:
            doc.close()
            continue
        fp = out_dir / f"{u['id']}.pdf"
        doc.save(fp, deflate=True, garbage=4)
        w0, h0 = doc[0].rect.width, doc[0].rect.height
        doc.close()
        index.append({"id": u["id"], "number": u.get("number"), "section": u.get("section"),
                      "file": fp.name, "pages": len(u["regions"]),
                      "wpt": round(w0, 2), "hpt": round(h0, 2)})

    (out_dir / "index.json").write_text(json.dumps({"paperId": pid, "units": index}, indent=2))
    print(f"  {pid}: baked {len(index)} unit crops (index-resolved, page-correct) -> baked_v3/")


if __name__ == "__main__":
    main()
