#!/usr/bin/env python3
"""Step 1 of segmentation: render a paper's pages to images for the locate step.

Deterministic prep — no LLM. Produces page PNGs that a Claude Code agent (the "locate" step)
reads to emit boundaries.json, and an info.json the bake step reuses. Also flags whether the
paper is born-digital (has a text layer → vector crops later) or scanned (→ raster crops).

    python3 tools/render_paper.py "<paperId>"          # from papers/_index.json
    python3 tools/render_paper.py "Maths Advanced/HSC-NESA/2020-hsc-mathematics-advanced.pdf"

Output: papers/_work/<paperId>/p01.png … + info.json   (papers/ is gitignored)
"""
import json
import sys
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"
WORK = PAPERS / "_work"
DPI = 150  # enough for the agent to read question numbers / marks; keep images light


def resolve(arg):
    """arg is a paperId (from _index.json) or a path relative to papers/."""
    idx = PAPERS / "_index.json"
    if idx.exists():
        for p in json.loads(idx.read_text())["papers"]:
            if p["paperId"] == arg:
                return p["paperId"], PAPERS / p["path"]
    pdf = (PAPERS / arg)
    if pdf.exists():
        return arg.replace("/", "-").replace(".pdf", "").lower(), pdf
    sys.exit(f"not found: {arg}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    paper_id, pdf_path = resolve(sys.argv[1])
    out = WORK / paper_id
    out.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    zoom = DPI / 72.0
    mat = fitz.Matrix(zoom, zoom)
    text_pages = 0
    pages = []
    for i, page in enumerate(doc):
        # Render (derotates automatically — pixmap is upright).
        pix = page.get_pixmap(matrix=mat)
        name = f"p{i + 1:02d}.png"
        pix.save(out / name)
        has_text = bool(page.get_text("text").strip())
        text_pages += has_text
        pages.append({
            "page": i,                       # 0-based, as fitz indexes
            "image": name,
            "wpt": page.rect.width,          # PDF points (for bbox → points conversion)
            "hpt": page.rect.height,
            "rotation": page.rotation,
            "hasText": has_text,
        })

    born_digital = text_pages >= max(1, len(doc) // 2)  # majority have a text layer
    info = {
        "paperId": paper_id,
        "path": str(pdf_path.relative_to(PAPERS)),
        "pageCount": len(doc),
        "bornDigital": born_digital,
        "dpi": DPI,
        "pages": pages,
    }
    (out / "info.json").write_text(json.dumps(info, indent=2))
    print(f"{paper_id}: {len(doc)} pages -> {out.relative_to(ROOT)}  "
          f"({'born-digital' if born_digital else 'SCANNED'}, {text_pages}/{len(doc)} text pages)")


if __name__ == "__main__":
    main()
