#!/usr/bin/env python3
"""Mac-side OCR of past papers, priority subjects first.

Text-layer extraction (fast, PyMuPDF) where a PDF has one; Tesseract fallback
(pdftoppm -> tesseract) for scanned pages. Output: mac_ocr_out/<same relpath>.txt.
Resumable (skips non-empty outputs). Priority subjects are done first, in order.

    python3 tools/mac_ocr.py                 # priority subjects, then the rest
    python3 tools/mac_ocr.py --priority-only # ONLY the priority subjects, then stop
"""
import glob, subprocess, sys, tempfile
from pathlib import Path
import fitz

ROOT = Path("/Users/fred/hsc-podcast")
PAPERS = ROOT / "papers"
OUT = ROOT / "mac_ocr_out"
PRIORITY = ["Maths Extension 1", "English Standard"]   # first, in this order

def subjects_ordered():
    subs = [p.name for p in PAPERS.iterdir() if p.is_dir() and not p.name.startswith("_")]
    pri = [s for s in PRIORITY if s in subs]
    rest = sorted(s for s in subs if s not in PRIORITY)
    return pri + rest

def ocr_scanned(pdf):
    parts = []
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", "200", "-png", str(pdf), f"{td}/p"],
                       check=False, stderr=subprocess.DEVNULL)
        for img in sorted(glob.glob(f"{td}/p*.png")):
            r = subprocess.run(["tesseract", img, "stdout"],
                               capture_output=True, text=True, stderr=subprocess.DEVNULL)
            parts.append(r.stdout)
    return "\n".join(parts)

def process(pdf):
    dst = OUT / pdf.relative_to(PAPERS).with_suffix(".txt")
    if dst.exists() and dst.stat().st_size > 0:
        return "skip"
    try:
        doc = fitz.open(pdf)
        text = "\n".join(pg.get_text("text") for pg in doc)
        doc.close()
    except Exception:
        text = ""
    if len(text.strip()) < 100:          # no/low text layer -> real OCR
        try:
            text = ocr_scanned(pdf)
        except Exception as e:
            return f"fail:{e}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)
    return "ok"

def main():
    only = "--priority-only" in sys.argv
    subs = [s for s in subjects_ordered() if not only or s in PRIORITY]
    ok = skip = fail = 0
    for subj in subs:
        pdfs = sorted((PAPERS / subj).rglob("*.pdf"))
        if not pdfs:
            continue
        print(f"=== {subj}: {len(pdfs)} papers ===", flush=True)
        for pdf in pdfs:
            r = process(pdf)
            if r == "ok": ok += 1
            elif r == "skip": skip += 1
            else: fail += 1
            if (ok + skip + fail) % 50 == 0:
                print(f"  [{subj}] ok={ok} skip={skip} fail={fail}", flush=True)
    print(f"=== mac_ocr done: ok={ok} skip={skip} fail={fail} ===", flush=True)

if __name__ == "__main__":
    main()
