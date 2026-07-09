#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""split.json (+ lines boxes)  ->  mask.json  (Gen-3 MASK, deterministic).

For each unit, partitions its region vertically into labelled bands the generator acts
on: content (keep always) / writing-space (drop compact, re-rule non-compact) /
dead-space (drop always). Answer-structure is left for the LLM/human arbitration stage
— this deterministic pass only emits content/writing-space/dead-space.

Lines boxes are attached to a unit by GEOMETRY (a lines box whose centre-y sits inside
the unit region on the same page), never by the unreliable typed number. Source of
lines boxes: annotations.json when present (human ground truth), else the linesTopY /
spaceHeight already written into boundaries.json by detect_lines.py.

    python3 tools/build_masks.py "<paperId>" [lines-boxes-file]

Assumes single-region units (true for the current gold set); multi-region units keep
their extra regions as whole-content and are flagged.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
EPS = 0.008   # bands thinner than 0.8% of page height are noise, absorbed into neighbour


def lines_boxes(wd, override):
    src = Path(override) if override else (wd / "annotations.json")
    if src.exists():
        return [b for b in json.loads(src.read_text())["boxes"] if b.get("kind") == "lines"]
    return []


def main():
    pid = sys.argv[1]
    wd = WORK / pid
    split = json.loads((wd / "split.json").read_text())
    info = json.loads((wd / "info.json").read_text())
    lines = lines_boxes(wd, sys.argv[2] if len(sys.argv) > 2 else None)

    masks = []
    for u in split["units"]:
        r0 = u["regions"][0]
        page, (x0, y0, x1, y1) = r0["page"], r0["bbox"]
        hpt = info["pages"][page]["hpt"]

        mine = sorted(
            (lb for lb in lines
             if lb["page"] == page and y0 <= (lb["bbox"][1] + lb["bbox"][3]) / 2 <= y1),
            key=lambda lb: lb["bbox"][1])

        regions, cursor, space_frac = [], y0, 0.0
        for lb in mine:
            ly0, ly1 = max(lb["bbox"][1], y0), min(lb["bbox"][3], y1)
            if ly1 <= cursor + EPS:
                continue
            if ly0 > cursor + EPS:
                regions.append({"page": page, "bbox": [x0, round(cursor, 4), x1, round(ly0, 4)], "label": "content"})
            regions.append({"page": page, "bbox": [x0, round(ly0, 4), x1, round(ly1, 4)], "label": "writing-space"})
            space_frac += ly1 - ly0
            cursor = ly1
        if cursor < y1 - EPS:
            # trailing band: content when no lines were found at all, else blank -> dead-space
            regions.append({"page": page, "bbox": [x0, round(cursor, 4), x1, round(y1, 4)],
                            "label": "content" if not mine else "dead-space"})
        if not regions:
            regions.append({"page": page, "bbox": [x0, y0, x1, y1], "label": "content"})

        for extra in u["regions"][1:]:
            regions.append({"page": extra["page"], "bbox": extra["bbox"], "label": "content"})
            print(f"  note: unit {u['id']} has a continuation region (kept as content)")

        masks.append({"unitId": u["id"],
                      "spaceHeight": round(space_frac * hpt, 1) if space_frac else None,
                      "regions": regions})

    out = {"paperId": pid, "source": "deterministic", "masks": masks}
    (wd / "mask.json").write_text(json.dumps(out, indent=2))
    nws = sum(1 for m in masks if m["spaceHeight"])
    print(f"  {pid}: {len(masks)} masks, {nws} with writing-space -> mask.json")


if __name__ == "__main__":
    main()
