#!/usr/bin/env python3
"""Step 1 of segmentation: render a paper's pages to images for the locate step.

Deterministic prep — no LLM. Produces page PNGs that a Claude Code agent (the "locate" step)
reads to emit boundaries.json, and an info.json the bake step reuses. Records the subject slug
so bake routes to the right per-subject folder. Flags born-digital (text layer) vs scanned.

    python3 tools/render_paper.py "<paperId>"          # from papers/_index.json
    python3 tools/render_paper.py "Maths Standard 2/Y12-Trial/Abbotsleigh 2021.pdf"

Output: papers/_work/<paperId>/p01.png … + info.json   (papers/ is gitignored)
Prints the resolved paperId — pass that to bake_questions.py.
"""
import json
import re
import sys
from pathlib import Path

import fitz  # pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _subjects import content_slug  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"
WORK = PAPERS / "_work"
DPI = int(sys.argv[2]) if len(sys.argv) > 2 else 110  # locate only needs to read numbers/marks


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def resolve(arg):
    """arg is a paperId or a path relative to papers/. Returns (clean paperId, pdf path,
    subject slug) — always slug the id so downstream dirs/lookups are space-free."""
    idx = PAPERS / "_index.json"
    if idx.exists():
        for p in json.loads(idx.read_text())["papers"]:
            if p["paperId"] == arg or p["path"] == arg:
                # alias tree slugs to the committed content/ slug (design-technology -> dt)
                return p["paperId"], PAPERS / p["path"], content_slug(_slug(p["subject"]))
    pdf = (PAPERS / arg)
    if pdf.exists():
        return _slug(arg.replace(".pdf", "")), pdf, "misc"
    sys.exit(f"not found: {arg}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    paper_id, pdf_path, subject = resolve(sys.argv[1])
    out = WORK / paper_id
    out.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(DPI / 72.0, DPI / 72.0)
    text_pages = 0
    pages = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=mat)          # derotates automatically → upright
        name = f"p{i + 1:02d}.png"
        pix.save(out / name)
        has_text = bool(page.get_text("text").strip())
        text_pages += has_text
        pages.append({
            "page": i, "image": name,
            "wpt": page.rect.width, "hpt": page.rect.height,
            "rotation": page.rotation, "hasText": has_text,
        })

    born_digital = text_pages >= max(1, len(doc) // 2)
    (out / "info.json").write_text(json.dumps({
        "paperId": paper_id, "subject": subject, "path": str(pdf_path.relative_to(PAPERS)),
        "pageCount": len(doc), "bornDigital": born_digital, "dpi": DPI, "pages": pages,
    }, indent=2))
    print(f"paperId: {paper_id}  subject: {subject}")
    print(f"  {len(doc)} pages @ {DPI}dpi -> {out.relative_to(ROOT)}  "
          f"({'born-digital' if born_digital else 'SCANNED'}, {text_pages}/{len(doc)} text)")


if __name__ == "__main__":
    main()
