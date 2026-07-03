#!/usr/bin/env python3
"""Score machine segmentation against human ground-truth annotations.

Compares papers/_work/<paperId>/boundaries.json (machine) with annotations.json
(human boxes from tools/annotate_app.py). Human box labels/numbers are ignored —
geometry is the ground truth. Machine display units = standalone questions plus the
lettered parts of booklet questions (>= 2 labelled parts).

Reports: 1:1 matches, machine units merging several human boxes (under-split),
human boxes straddling machine units (over-split), unmatched on either side, and
bottom-tightness (how far machine bottoms over-extend past human content bottoms).

    python3 tools/score_annotations.py "<paperId>"
"""
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def machine_units(boundaries, trimmed=True):
    """Display units with per-page y-extents: standalone questions whole, booklet
    questions (>=2 labelled parts) per lettered part."""
    units = []
    for q in boundaries.get("questions", []):
        labelled = [p for p in q.get("parts", []) if p.get("label")]
        # same display-unit rule as bake_questions.py: only BOOKLET questions
        # (>= 2 labelled parts AND >= 10 marks) split into parts
        booklet = len(labelled) >= 2 and (q.get("marks") or 0) >= 10
        groups = ([("part", p.get("label"), p.get("regions", []))
                   for p in labelled] if booklet else
                  [("question", None,
                    (q.get("stimulus") or []) + [r for p in q.get("parts", []) for r in p.get("regions", [])])])
        for kind, label, regs in groups:
            regs = [r for r in regs if not r.get("doc")]
            if not regs:
                continue
            pages = {}
            for r in regs:
                y1 = r["bbox"][3]
                if trimmed:
                    # effective crop bottom after line/content trimming (what ships)
                    for k in ("linesTopY", "contentBottomY"):
                        if r.get(k):
                            y1 = min(y1, r[k])
                a = pages.setdefault(r["page"], [1.0, 0.0])
                a[0] = min(a[0], r["bbox"][1]); a[1] = max(a[1], y1)
            units.append({"number": q.get("number"), "label": label, "pages": pages})
    return units


def main():
    pid = sys.argv[1]
    wd = WORK / pid
    raw = json.loads((wd / "annotations.json").read_text())["boxes"]
    ann = [b for b in raw if b.get("kind") != "lines"]   # lines boxes score separately
    include_lines = any(b.get("kind") == "lines" for b in raw)
    units = machine_units(json.loads((wd / "boundaries.json").read_text()),
                          trimmed=not include_lines)
    # judge only pages the human actually annotated — partial ground truth is fine
    ann_pages = {b["page"] for b in ann}
    units = [u for u in units if any(p in ann_pages for p in u["pages"])]
    for u in units:
        u["pages"] = {p: v for p, v in u["pages"].items() if p in ann_pages}

    def cover(h, u):
        """fraction of the human box covered by unit u (same page)."""
        if h["page"] not in u["pages"]:
            return 0.0
        y0, y1 = u["pages"][h["page"]]
        o = min(h["bbox"][3], y1) - max(h["bbox"][1], y0)
        return max(0.0, o) / max(1e-6, h["bbox"][3] - h["bbox"][1])

    def area(u):
        return sum(y1 - y0 for y0, y1 in u["pages"].values())

    # prefer the SMALLEST unit that covers a human box (ties on coverage go to the
    # tightest machine unit, not an enclosing one)
    h2u = {i: sorted(((cover(h, u), -area(units[j]), j)
                      for j, u in enumerate(units) for u in [units[j]]), reverse=True)
           for i, h in enumerate(ann)}
    best = {i: ((hits[0][0], hits[0][2]) if hits and hits[0][0] > 0.3 else None)
            for i, hits in h2u.items()}
    from collections import Counter
    unit_hits = Counter(j for v in best.values() if v for _, j in [v])

    one2one = sum(1 for i, v in best.items() if v and unit_hits[v[1]] == 1)
    merged = {j: c for j, c in unit_hits.items() if c > 1}
    missed = [i for i, v in best.items() if v is None]
    spurious = [j for j in range(len(units)) if j not in unit_hits]

    print(f"human units: {len(ann)}   machine display units: {len(units)}")
    print(f"1:1 matched: {one2one}")
    for j, c in merged.items():
        u = units[j]
        print(f"UNDER-SPLIT: machine Q{u['number']}{u['label'] or ''} covers {c} human boxes")
    for i in missed:
        h = ann[i]
        print(f"MISSED: human box p{h['page'] + 1} y{h['bbox'][1]:.2f}-{h['bbox'][3]:.2f} (Q{h.get('number')})")
    names = ["Q%s%s" % (units[j]["number"], units[j]["label"] or "") for j in spurious[:12]]
    print(f"machine units with no human box: {len(spurious)} ({names})")

    overs = []
    for i, v in best.items():
        if not v:
            continue
        h, u = ann[i], units[v[1]]
        if h["page"] in u["pages"]:
            overs.append(u["pages"][h["page"]][1] - h["bbox"][3])
    if overs:
        print(f"bottom over-extension (page fraction): median {statistics.median(overs):+.3f}  "
              f"p90 {sorted(overs)[int(len(overs) * 0.9)]:+.3f}  max {max(overs):+.3f}")


if __name__ == "__main__":
    main()
