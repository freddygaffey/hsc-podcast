#!/usr/bin/env python3
"""Compare two box sets (human annotations vs an AI vision segmenter's output).

Both files hold {"boxes": [{page, bbox, kind, number, part, marks}]} — the shape
tools/annotate_app.py saves and the vision agent writes. Matches question boxes by
page + IoU, reports agreement, and does the same for "lines" boxes. This is the
fitness function for iterating the vision-segmenter prompt until Claude draws the
same boxes a human would.

    python3 tools/compare_boxes.py <human.json|paperId> <ai.json>
"""
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def load(arg):
    p = Path(arg)
    if not p.exists():
        p = WORK / arg / "annotations.json"
    return json.loads(p.read_text())["boxes"]


def iou(a, b):
    if a["page"] != b["page"]:
        return 0.0
    ax0, ay0, ax1, ay1 = a["bbox"]
    bx0, by0, bx1, by1 = b["bbox"]
    ix = max(0, min(ax1, bx1) - max(ax0, bx0))
    iy = max(0, min(ay1, by1) - max(ay0, by0))
    inter = ix * iy
    if inter <= 0:
        return 0.0
    area = (ax1 - ax0) * (ay1 - ay0) + (bx1 - bx0) * (by1 - by0) - inter
    return inter / area


def match(hs, ais, label):
    pairs = sorted(((iou(h, a), i, j) for i, h in enumerate(hs) for j, a in enumerate(ais)),
                   reverse=True)
    used_h, used_a, matched = set(), set(), []
    for score, i, j in pairs:
        if score < 0.4 or i in used_h or j in used_a:
            continue
        used_h.add(i); used_a.add(j)
        matched.append((score, i, j))
    print(f"--- {label}: human {len(hs)} vs AI {len(ais)}")
    print(f"matched (IoU>0.4): {len(matched)}"
          + (f", median IoU {statistics.median(s for s, _, _ in matched):.2f}" if matched else ""))
    for i in set(range(len(hs))) - used_h:
        h = hs[i]
        print(f"  AI MISSED: p{h['page'] + 1} Q{h.get('number')} y{h['bbox'][1]:.2f}-{h['bbox'][3]:.2f}")
    for j in set(range(len(ais))) - used_a:
        a = ais[j]
        print(f"  AI EXTRA:  p{a['page'] + 1} Q{a.get('number')} y{a['bbox'][1]:.2f}-{a['bbox'][3]:.2f}")
    if label == "question boxes":
        agree = [(hs[i], ais[j]) for _, i, j in matched
                 if hs[i].get("marks") and ais[j].get("marks")]
        if agree:
            ok = sum(1 for h, a in agree if int(h["marks"]) == int(a["marks"]))
            print(f"marks agreement on boxes where both set marks: {ok}/{len(agree)}")
    return matched


def main():
    hs = load(sys.argv[1])
    ais = load(sys.argv[2])
    match([b for b in hs if b.get("kind") != "lines"],
          [b for b in ais if b.get("kind") != "lines"], "question boxes")
    match([b for b in hs if b.get("kind") == "lines"],
          [b for b in ais if b.get("kind") == "lines"], "lines boxes")


if __name__ == "__main__":
    main()
