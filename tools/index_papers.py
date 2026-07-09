#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Label the scraped past papers into a machine-readable catalogue.

The scraper (papers/_downloader.py, papers/_nesa.py) already encodes most metadata in the
folder path:  papers/<Subject>/<category>/<filename>.pdf  — this walks that tree, parses each
file, and writes papers/_index.json. No network, no API cost; it's pure path parsing.

Every entry gets a stable `paperId` (slug of subject+category+filename) so question records
can point back to their source paper. Marking guides and exams are linked by their shared
stem (NESA ships 2015-maths-hsc-exam.pdf + 2015-maths-hsc-mg.pdf).

    python3 tools/index_papers.py                 # index everything → papers/_index.json
    python3 tools/index_papers.py "Maths Advanced" # one subject only
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"
OUT = PAPERS / "_index.json"

# category dir -> (kind, board). Trial paper-variants share kind=trial.
CATEGORY = {
    "HSC-NESA":        ("hsc",    "nesa"),
    "Y12-HSC":         ("hsc",    "thsc"),   # THSC's copy of the official HSC
    "Y12-Trial":       ("trial",  "thsc"),
    "Y12-Trial-P1":    ("trial",  "thsc"),
    "Y12-Trial-P2-Adv":("trial",  "thsc"),
    "Y12-Trial-P2-Std":("trial",  "thsc"),
    "Y11-Yearly":      ("yearly", "thsc"),
}
VARIANT = {  # extra label pulled from the category suffix
    "Y12-Trial-P1": "Paper 1", "Y12-Trial-P2-Adv": "Paper 2 (Adv)", "Y12-Trial-P2-Std": "Paper 2 (Std)",
}

YEAR_RE = re.compile(r"(19[6-9]\d|20[0-4]\d)")          # 1960–2049
SOL_RE  = re.compile(r"\bw\.?\s*sol", re.I)             # "w. sol" / "w sol"


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def classify_role(name: str) -> str:
    n = name.lower()
    if re.search(r"\bmg\b|marking|guideline", n):    return "marking"
    if "notes" in n:                                  return "notes"
    return "exam"


def parse_school(stem: str, year: str, role: str) -> str | None:
    s = stem
    if year:            s = s.replace(year, " ")
    s = SOL_RE.sub(" ", s)
    # drop role / boilerplate tokens
    s = re.sub(r"\b(hsc|trial|exam|paper|maths?|mg|notes|advanced|standard|prelim|yearly)\b",
               " ", s, flags=re.I)
    s = re.sub(r"[-_]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip(" .-")
    return s.title() if s else None


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if not PAPERS.exists():
        sys.exit(f"no {PAPERS}")

    papers = []
    for pdf in sorted(PAPERS.rglob("*.pdf")):
        rel = pdf.relative_to(PAPERS)
        if any(part.startswith("_") for part in rel.parts):   # skip _work/, logs, staging
            continue
        if len(rel.parts) < 3:          # want <subject>/<category>/<file>
            continue
        subject, category = rel.parts[0], rel.parts[1]
        if only and subject != only:
            continue
        kind, board = CATEGORY.get(category, ("unknown", "unknown"))
        stem = pdf.stem
        ym = YEAR_RE.search(stem) or YEAR_RE.search(str(rel))
        year = ym.group(0) if ym else None
        role = classify_role(stem)
        school = None if board == "nesa" else parse_school(stem, year or "", role)

        papers.append({
            "paperId": slug(f"{subject}-{category}-{stem}"),
            "subject": subject,
            "kind": kind,               # hsc | trial | yearly | unknown
            "board": board,             # nesa | thsc
            "variant": VARIANT.get(category),
            "year": int(year) if year else None,
            "school": school,           # null for official HSC
            "role": role,               # exam | marking | notes
            "hasSolutions": bool(SOL_RE.search(stem)),  # solutions bundled in the exam PDF
            "path": str(rel),           # local path under papers/ (gitignored)
        })

    # Link each exam to its marking guide by shared stem prefix (NESA -exam/-mg pairs) or,
    # for THSC, the "w. sol" exam is its own guide.
    by_dir_year = {}
    for p in papers:
        by_dir_year.setdefault((str(Path(p["path"]).parent), p["year"]), []).append(p)
    for p in papers:
        if p["role"] != "exam":
            continue
        if p["hasSolutions"]:
            p["markingPaperId"] = p["paperId"]           # solutions inline
            continue
        siblings = by_dir_year.get((str(Path(p["path"]).parent), p["year"]), [])
        mg = next((s for s in siblings if s["role"] == "marking"), None)
        p["markingPaperId"] = mg["paperId"] if mg else None

    OUT.write_text(json.dumps({"papers": papers}, indent=2))

    # Summary
    exams = [p for p in papers if p["role"] == "exam"]
    subs = {}
    for p in exams:
        subs[p["subject"]] = subs.get(p["subject"], 0) + 1
    print(f"Indexed {len(papers)} files ({len(exams)} exams) -> {OUT.relative_to(ROOT)}")
    for s in sorted(subs, key=lambda k: -subs[k]):
        print(f"  {subs[s]:4d} exams  {s}")
    unmatched = [p for p in exams if not p.get("markingPaperId")]
    print(f"  {len(unmatched)} exams have no linked marking guide")


if __name__ == "__main__":
    main()
