#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Convert vision-segmenter (or human annotator) boxes into boundaries.json.

Input: papers/_work/<paperId>/vision-boxes.json (or annotations.json) in the
annotate_app shape: {"boxes": [{page, bbox, kind: "question"|"lines", number, part,
marks}]}. Question boxes become question units (source "vision"); each lines box
attaches to the question box containing it — its top becomes the region's linesTopY
(the bake trims there) and its height becomes the part's spaceHeight in points.

    python3 tools/boxes_to_boundaries.py "<paperId>" [boxes-file]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def numkey(n):
    try:
        return (0, int(n))
    except (TypeError, ValueError):
        return (1, 0)


def main():
    pid = sys.argv[1]
    wd = WORK / pid
    src = Path(sys.argv[2]) if len(sys.argv) > 2 else (wd / "vision-boxes.json")
    boxes = json.loads(src.read_text())["boxes"]
    info = json.loads((wd / "info.json").read_text())

    qs = sorted((b for b in boxes if b.get("kind") != "lines"),
                key=lambda b: (b["page"], b["bbox"][1]))
    lines = [b for b in boxes if b.get("kind") == "lines"]

    questions = []
    for b in qs:
        hpt = info["pages"][b["page"]]["hpt"]
        region = {"page": b["page"], "bbox": [round(v, 4) for v in b["bbox"]]}
        space = 0.0
        for lb in lines:
            if lb["page"] != b["page"]:
                continue
            cy = (lb["bbox"][1] + lb["bbox"][3]) / 2
            if b["bbox"][1] <= cy <= b["bbox"][3]:
                if "linesTopY" not in region or lb["bbox"][1] < region["linesTopY"]:
                    region["linesTopY"] = round(lb["bbox"][1], 4)
                space += (lb["bbox"][3] - lb["bbox"][1]) * hpt
        marks = b.get("marks")
        try:
            n = int(b.get("number"))
        except (TypeError, ValueError):
            n = None
        qtype = "mc" if (marks == 1 and n is not None and n <= 10 and not b.get("part")) else None
        questions.append({
            "number": str(b["number"]) if b.get("number") is not None else None,
            "marks": marks, "marksPrinted": bool(marks), "topic": None, "module": None,
            "syllabusRefs": [], "type": qtype,
            "lineCount": None, "spaceHeight": round(space, 1) if space else None,
            "stimulus": [], "text": None,
            "parts": [{"label": b.get("part") or None, "marks": marks, "type": qtype,
                       "marksPrinted": bool(marks), "lineCount": None,
                       "spaceHeight": round(space, 1) if space else None,
                       "regions": [region], "markingRegions": [], "text": None}],
        })

    out = {"paperId": pid, "subject": info.get("subject"), "source": "vision",
           "questions": questions}
    (wd / "boundaries.json").write_text(json.dumps(out, indent=2))
    print(f"  {pid}: {len(questions)} vision units, {len(lines)} lines boxes -> boundaries.json")


if __name__ == "__main__":
    main()
