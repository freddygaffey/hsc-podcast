#!/usr/bin/env python3
"""Regression harness — score current pipeline output against frozen human ground truth.

The gate that stops a prompt/rule change from silently regressing accuracy
(docs/parser-pipeline-plan.md, layer L-regress). Gold papers live in
papers/_goldset/<paperId>/gold.json (annotate_app box shape); bars live in
papers/_goldset/manifest.json.

For each gold paper it finds the current candidate output, matches boxes to gold by
page+IoU (greedy, same fitness function as tools/compare_boxes.py), and scores:

  - question units : count exact? matched? median IoU?
  - lines boxes    : matched? median IoU? (only when the candidate carries lines boxes)
  - marks          : exact where the human recorded a mark?

Candidate resolution per paper (first that exists):
  split.json (Gen-3) -> vision-boxes.json -> annotations.json -> boundaries.json
The candidate is converted to the box shape before matching.

    python3 tools/regress.py             # all gold papers, scorecard, exit non-zero on breach
    python3 tools/regress.py <paperId>   # one paper
    python3 tools/regress.py --candidate split.json   # force a candidate filename
Exit non-zero if any HARD bar is breached.
"""
import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
GOLD = ROOT / "papers" / "_goldset"


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
    return inter / ((ax1 - ax0) * (ay1 - ay0) + (bx1 - bx0) * (by1 - by0) - inter)


def greedy_match(gs, cs, thresh):
    pairs = sorted(((iou(g, c), i, j) for i, g in enumerate(gs) for j, c in enumerate(cs)),
                   reverse=True)
    ug, uc, matched = set(), set(), []
    for score, i, j in pairs:
        if score < thresh or i in ug or j in uc:
            continue
        ug.add(i); uc.add(j); matched.append((score, i, j))
    return matched, ug, uc


def is_lines(box):
    return box.get("kind") == "lines"


def candidate_boxes(pid, forced=None):
    """Return (boxes, filename) for the first available candidate, converted to box shape."""
    wd = WORK / pid
    order = [forced] if forced else ["split.json", "vision-boxes.json", "annotations.json", "boundaries.json"]
    for name in order:
        fp = wd / name
        if not fp.exists():
            continue
        d = json.loads(fp.read_text())
        if name == "split.json":
            boxes = []
            for u in d.get("units", []):
                for r in u.get("regions", []):
                    boxes.append({"page": r["page"], "bbox": r["bbox"], "kind": None,
                                  "number": u.get("number"), "part": u.get("part"), "marks": u.get("marks")})
            return boxes, name
        if name == "boundaries.json":
            boxes = []
            for q in d.get("questions", []):
                for part in q.get("parts", []):
                    for r in part.get("regions", []):
                        boxes.append({"page": r["page"], "bbox": r["bbox"], "kind": None,
                                      "number": q.get("number"), "part": part.get("label"), "marks": q.get("marks")})
            return boxes, name
        return d["boxes"], name        # vision-boxes / annotations already box shape
    return None, None


def score_paper(entry, forced, bars):
    pid = entry["paperId"]
    gold = json.loads((GOLD / pid / "gold.json").read_text())["boxes"]
    gq = [b for b in gold if not is_lines(b)]
    gl = [b for b in gold if is_lines(b)]
    cand, cname = candidate_boxes(pid, forced)

    row = {"paperId": pid, "family": entry.get("family"), "candidate": cname,
           "goldUnits": len(gq), "candUnits": None, "matched": None,
           "qIoU": None, "linesMatched": None, "lIoU": None, "marksOk": None, "breaches": []}
    if cand is None:
        row["breaches"].append("no-candidate")
        return row

    cq = [b for b in cand if not is_lines(b)]
    cl = [b for b in cand if is_lines(b)]
    row["candUnits"] = len(cq)

    m, ug, uc = greedy_match(gq, cq, bars["unit_iou_min"])
    row["matched"] = len(m)
    row["qIoU"] = round(statistics.median(s for s, _, _ in m), 3) if m else None

    if cl:
        lm, _, _ = greedy_match(gl, cl, bars["unit_iou_min"])
        row["linesMatched"] = f"{len(lm)}/{len(gl)}"
        row["lIoU"] = round(statistics.median(s for s, _, _ in lm), 3) if lm else None

    # marks: only over gold boxes that recorded a mark and matched a candidate
    marks_checked = marks_ok = 0
    gi_to_ci = {i: j for _, i, j in m}
    for i, g in enumerate(gq):
        if g.get("marks") is None or i not in gi_to_ci:
            continue
        marks_checked += 1
        if cq[gi_to_ci[i]].get("marks") == g["marks"]:
            marks_ok += 1
    row["marksOk"] = f"{marks_ok}/{marks_checked}" if marks_checked else "n/a"

    # hard bars
    if bars.get("unit_count_exact") and len(cq) != len(gq):
        row["breaches"].append(f"unit-count {len(cq)}!={len(gq)}")
    if bars.get("unit_count_exact") and len(m) != len(gq):
        row["breaches"].append(f"unmatched {len(gq) - len(m)} units")
    if row["qIoU"] is not None and row["qIoU"] < bars["question_iou_median_min"]:
        row["breaches"].append(f"qIoU {row['qIoU']}<{bars['question_iou_median_min']}")
    if bars.get("marks_exact_where_printed") and marks_checked and marks_ok != marks_checked:
        row["breaches"].append(f"marks {marks_ok}/{marks_checked}")
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId", nargs="?")
    ap.add_argument("--candidate", help="force a candidate filename (e.g. split.json)")
    a = ap.parse_args()

    man = json.loads((GOLD / "manifest.json").read_text())
    bars = man["bars"]
    papers = [p for p in man["papers"] if not a.paperId or p["paperId"] == a.paperId]
    if not papers:
        raise SystemExit(f"no gold paper matches {a.paperId!r}")

    print(f"{'status':6} {'units':>11}  {'matched':>7}  {'qIoU':>5}  {'lines':>6}  {'lIoU':>5}  {'marks':>6}  paper")
    breached = 0
    for entry in papers:
        r = score_paper(entry, a.candidate, bars)
        ok = not r["breaches"]
        breached += 0 if ok else 1
        units = f"{r['candUnits']}/{r['goldUnits']}" if r["candUnits"] is not None else "-"
        print(f"{'ok' if ok else 'FAIL':6} {units:>11}  {str(r['matched'] or '-'):>7}  "
              f"{str(r['qIoU'] or '-'):>5}  {str(r['linesMatched'] or '-'):>6}  {str(r['lIoU'] or '-'):>5}  "
              f"{r['marksOk'] or '-':>6}  {r['paperId']}  [{r['candidate'] or 'none'}]")
        for b in r["breaches"]:
            print(f"       ↳ {b}")
    print(f"\n{len(papers)} gold paper(s), {breached} breaching hard bars")
    sys.exit(1 if breached else 0)


if __name__ == "__main__":
    main()
