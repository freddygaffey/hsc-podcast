#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Ingest a copyright textbook PDF WITHOUT ever exposing the whole book.

The raw PDF and the extracted full text stay LOCAL (gitignored). The only thing that ever
reaches the repo / deploy is an individual *cited* page image, rendered on demand into the
deployable, login-gated content/<subject>/sources/ tree.

Layout (per book):
    content/<subject>/textbook/<dir>/source.pdf   # you drop this here (LOCAL ONLY, gitignored)
    content/<subject>/textbook/<dir>/book.json    # {slug,title,edition,year,pageOffset}
    content/<subject>/textbook/<dir>/pages.jsonl  # extracted text, generated (gitignored)
    content/<subject>/sources/<slug>/p<NN>.jpg    # one cited page, committed + deployed

`pageOffset` maps a printed page number to a PDF page: pdf_page = printed_page + pageOffset.

Commands:
    extract <textbook_dir>                  # source.pdf -> pages.jsonl (run once per book)
    render  <textbook_dir> <page> [page..]  # render printed page(s) -> sources/<slug>/pNN.jpg
    pages-for-quiz <quiz.json> <textbook_dir>   # render every textbook page that quiz cites
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def _book(textbook_dir):
    cfg = Path(textbook_dir) / "book.json"
    if not cfg.exists():
        sys.exit(f"missing {cfg} — create it with {{slug,title,edition,year,pageOffset}}")
    return json.loads(cfg.read_text())


def _pdf(textbook_dir):
    p = Path(textbook_dir) / "source.pdf"
    if not p.exists():
        sys.exit(f"missing {p} — drop the textbook PDF there (it stays local / gitignored)")
    return p


def _subject_root(textbook_dir):
    # content/<subject>/textbook/<dir> -> content/<subject>
    return Path(textbook_dir).resolve().parents[1]


def extract(textbook_dir):
    book = _book(textbook_dir)
    pdf = _pdf(textbook_dir)
    offset = int(book.get("pageOffset", 0))
    # One pdftotext pass; pages are separated by form-feed (\x0c).
    full = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
    pages = full.split("\x0c")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    out = Path(textbook_dir) / "pages.jsonl"
    with out.open("w") as f:
        for i, txt in enumerate(pages, start=1):
            f.write(json.dumps({
                "pdfPage": i,
                "page": i - offset,                 # printed page number
                "text": re.sub(r"\s+", " ", txt).strip(),
            }, ensure_ascii=False) + "\n")
    print(f"extracted {len(pages)} pages -> {out}  (LOCAL ONLY; gitignored)")


def render(textbook_dir, pages):
    book = _book(textbook_dir)
    pdf = _pdf(textbook_dir)
    slug = book["slug"]
    offset = int(book.get("pageOffset", 0))
    dest = _subject_root(textbook_dir) / "sources" / slug
    dest.mkdir(parents=True, exist_ok=True)
    for printed in pages:
        pdf_page = int(printed) + offset
        stem = dest / f"p{printed}"
        subprocess.run(
            ["pdftoppm", "-jpeg", "-r", "150", "-f", str(pdf_page), "-l", str(pdf_page),
             "-singlefile", str(pdf), str(stem)],
            check=True,
        )
        print(f"rendered printed p{printed} (pdf {pdf_page}) -> {stem}.jpg")
    print(f"\nCite these as  \"url\": \"sources/{slug}/p<NN>.jpg\"")


def pages_for_quiz(quiz_path, textbook_dir):
    book = _book(textbook_dir)
    slug = book["slug"]
    data = json.loads(Path(quiz_path).read_text())
    pages = set()
    for q in data.get("questions", []):
        s = q.get("source") or {}
        if s.get("origin") == "textbook" and s.get("page") and slug in (s.get("url", "") or s.get("ref", "")):
            pages.add(int(s["page"]))
    if not pages:
        print("no textbook citations for this book in that quiz")
        return
    render(textbook_dir, sorted(pages))


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd = argv[1]
    if cmd == "extract":
        extract(argv[2])
    elif cmd == "render":
        render(argv[2], argv[3:])
    elif cmd == "pages-for-quiz":
        pages_for_quiz(argv[2], argv[3])
    else:
        sys.exit(f"unknown command {cmd!r}\n{__doc__}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
