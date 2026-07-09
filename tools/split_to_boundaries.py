#!/usr/bin/env python3
"""Bridge the corrected split.json (vision segmenter + human review in the /review editor) into
boundaries.json, the input bake_questions.py expects. Groups split units by QUESTION number;
each unit (a lettered part, or a whole MC question) becomes a PART with its corrected region(s).

    python3 tools/split_to_boundaries.py "<paperId>"
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def numkey(n):
    digits = "".join(c for c in str(n) if c.isdigit())
    return (int(digits) if digits else 999, str(n))


def main():
    pid = sys.argv[1]
    wd = WORK / pid
    split = json.loads((wd / "split.json").read_text())
    units = split.get("units", [])

    byq, order = defaultdict(list), []
    for u in units:
        n = str(u.get("number"))
        if n not in byq:
            order.append(n)
        byq[n].append(u)

    questions = []
    for n in sorted(order, key=numkey):
        us = sorted(byq[n], key=lambda u: (u["regions"][0]["page"], u["regions"][0]["bbox"][1])
                    if u.get("regions") else (99, 0.0))                # visual (top-to-bottom) order
        is_mc = any(str(x.get("section", "")).strip() == "I" or x.get("type") == "mc" for x in us)
        parts = []
        for u in us:
            parts.append({
                "label": u.get("part"),
                "marks": u.get("marks"),
                "type": u.get("type") or ("mc" if is_mc else None),
                "marksPrinted": bool(u.get("marksPrinted")),
                "regions": [{"page": r["page"], "bbox": r["bbox"]} for r in u.get("regions", [])],
                "markingRegions": [],
                "text": "",
            })
        marks = sum((p["marks"] or 0) for p in parts) or None
        questions.append({
            "number": n, "marks": marks, "topic": None, "module": None, "syllabusRefs": [],
            "type": "mc" if is_mc else None,
            "marksPrinted": any(p["marksPrinted"] for p in parts),
            "stimulus": [], "text": "", "parts": parts,
        })

    out = {"paperId": pid, "subject": split.get("subject"), "source": "split-corrected",
           "sectionIIStartPage": split.get("sectionIIStartPage"),
           "solutionsStartPage": split.get("solutionsStartPage"), "questions": questions}
    (wd / "boundaries.json").write_text(json.dumps(out, indent=1))
    print(f"{pid[18:]}: {len(questions)} questions, "
          f"{sum(len(q['parts']) for q in questions)} parts -> boundaries.json")


if __name__ == "__main__":
    main()
