#!/usr/bin/env python3
"""annotate_app boxes  ->  split.json  (Gen-3 metadata-first SPLIT).

Question boxes (kind != "lines") become units, 1 box = 1 unit, in paper-normalised
coords. Lines boxes are NOT units — they feed the MASK stage (tools/build_masks.py).
This is the deterministic producer that lets a human annotation (or, later, the SPLIT
agent's boxes) drive the whole pipeline and be scored by tools/regress.py.

    python3 tools/boxes_to_split.py "<paperId>" [boxes-file]
Default boxes-file: papers/_work/<paperId>/annotations.json
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def main():
    pid = sys.argv[1]
    wd = WORK / pid
    src = Path(sys.argv[2]) if len(sys.argv) > 2 else (wd / "annotations.json")
    boxes = json.loads(src.read_text())["boxes"]
    info = json.loads((wd / "info.json").read_text())

    qs = sorted((b for b in boxes if b.get("kind") != "lines"),
                key=lambda b: (b["page"], b["bbox"][1]))
    units = []
    for b in qs:
        num = b.get("number")
        part = b.get("part") or None
        uid = "q" + (str(num) if num is not None else f"p{b['page']}y{b['bbox'][1]:.2f}")
        if part:
            uid += part
        units.append({
            "id": uid, "number": str(num) if num is not None else None,
            "part": part, "marks": b.get("marks"),
            "marksPrinted": b.get("marks") is not None,
            "type": None, "section": None,
            "ruleId": "human", "confidence": 1.0 if src.name == "annotations.json" else None,
            "regions": [{"page": b["page"], "bbox": [round(v, 4) for v in b["bbox"]]}],
        })

    out = {"paperId": pid, "subject": info.get("subject"), "source": "human", "units": units}
    (wd / "split.json").write_text(json.dumps(out, indent=2))
    print(f"  {pid}: {len(units)} units -> split.json")


if __name__ == "__main__":
    main()
