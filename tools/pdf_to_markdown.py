#!/usr/bin/env python3
"""Convert a PDF to Markdown, keeping images inline in reading order.

Usage: python3 tools/pdf_to_markdown.py <input.pdf> <output_dir>

Writes <output_dir>/<name>.md and <output_dir>/images/*. Image references are
inserted where each image sits on the page. Duplicate images (same bytes) are
saved once and reused. Lines beginning "Module" are promoted to `##` headings;
"Experimental setup"/"Experiment and results" style lines to `###`.
"""
import hashlib
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

SUBHEADS = re.compile(r"^(Experimental setup|Experiment and results|Results|Method|Setup|Significance|History)\b", re.I)


def main():
    pdf_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    img_dir = out_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    seen = {}          # image md5 -> saved filename
    img_count = 0
    md = [f"# {pdf_path.stem.strip('! ').strip()}\n"]

    for pno, page in enumerate(doc, 1):
        blocks = page.get_text("dict")["blocks"]
        # reading order: top-to-bottom, then left-to-right
        blocks.sort(key=lambda b: (round(b["bbox"][1] / 10), b["bbox"][0]))
        for b in blocks:
            if b["type"] == 1:  # image block
                data = b.get("image")
                if not data:
                    continue
                h = hashlib.md5(data).hexdigest()
                if h not in seen:
                    img_count += 1
                    ext = b.get("ext", "png")
                    name = f"img_{img_count:03d}.{ext}"
                    (img_dir / name).write_bytes(data)
                    seen[h] = name
                md.append(f"\n![](images/{seen[h]})\n")
            else:  # text block
                for line in b.get("lines", []):
                    text = "".join(span["text"] for span in line["spans"]).rstrip()
                    if not text:
                        continue
                    if text.strip().startswith("Module"):
                        md.append(f"\n## {text.strip()}\n")
                    elif SUBHEADS.match(text.strip()):
                        md.append(f"\n### {text.strip()}\n")
                    else:
                        md.append(text)

    out_md = out_dir / f"{pdf_path.stem.strip('! ').strip().replace(' ', '-').lower()}.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {out_md}")
    print(f"Pages: {len(doc)}  |  Images saved: {len(seen)} unique ({img_count} refs)  |  MD lines: {len(md)}")


if __name__ == "__main__":
    main()
