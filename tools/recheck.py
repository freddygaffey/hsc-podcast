#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Vision RE-CHECK for mis-split Section II questions.

Trigger: a question whose parts OVERLAP (geometry) or whose marks don't add up (with gaps).
Action: re-ask Qwen-VL, showing the question's page(s) and the current part list, "which of
these are really ONE part?" — a diagram/graph/table or a lone continuation line is NOT its own
top-level part. Then MERGE the current units that map to the same corrected top-level part
(union their boxes) and relabel a,b,c,… . Fixes the q14 b/c/d case automatically.

    python3 tools/recheck.py <paperId> [--dry]
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vision_seg as vs  # noqa: E402
import or_client as orc  # noqa: E402

WORK = vs.WORK
PROMPT = (
    "This is Question {q} from Section II of an HSC Mathematics Extension 1 paper (page images "
    "attached). It was auto-split, top to bottom, into these TOP-LEVEL parts: {parts}.\n\n"
    "Some may be WRONGLY split. A diagram/graph, a table, or a single continuation line is NOT a "
    "separate top-level part — it belongs to the lettered part above it. Consecutive LETTER "
    "labels (a),(b),(c) ARE separate top-level parts; roman numerals (i),(ii) are sub-parts that "
    "stay INSIDE their letter. Return the CORRECT list of top-level parts, in order, each with its "
    "letter and the first ~6 words of its first line (verbatim). STRICT JSON only:\n"
    '{"parts":[{"part":"a","anchor":"..."}]}')


def _is_ii(u):
    return "II" in str(u.get("section", "")).replace(" ", "").upper()


def flagged_questions(split):
    q = defaultdict(list)
    for u in split["units"]:
        if _is_ii(u):
            q[u["number"]].append(u)
    out = []
    for num, parts in q.items():
        parts.sort(key=lambda u: u["regions"][0]["bbox"][1])
        overlap = any(b["regions"][0]["bbox"][1] < a["regions"][-1]["bbox"][3] - 0.006
                      for a, b in zip(parts, parts[1:])
                      if a["regions"][-1]["page"] == b["regions"][0]["page"])
        marks = [u.get("marks") for u in parts]
        marks_bad = (None in marks) and sum(m or 0 for m in marks) < 14
        if overlap or marks_bad:
            out.append((num, parts, "overlap" if overlap else "marks"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    wd = WORK / a.paperId
    split = json.loads((wd / "split.json").read_text())
    ocr = json.loads((wd / "ocr.json").read_text())
    cost = 0.0
    changed = False
    keep = [u for u in split["units"] if not _is_ii(u)]        # MC untouched
    by_q = defaultdict(list)
    for u in split["units"]:
        if _is_ii(u):
            by_q[u["number"]].append(u)
    flags = {n for n, _, _ in flagged_questions(split)}

    for num, parts in by_q.items():
        parts.sort(key=lambda u: u["regions"][0]["bbox"][1])
        if num not in flags:
            keep.extend(parts)
            continue
        pages = sorted({r["page"] for u in parts for r in u["regions"]})
        cur = ", ".join(f'({u.get("part")})' for u in parts)
        content = [{"type": "text", "text": PROMPT.replace("{q}", str(num)).replace("{parts}", cur)}]
        for pg in pages:
            content.append({"type": "image_url",
                            "image_url": {"url": orc._data_uri(str(wd / f"p{pg:02d}.png"))}})
        txt, u = orc.chat(orc.VISION_MODEL, [{"role": "user", "content": content}],
                          max_tokens=1200, response_format={"type": "json_object"})
        cost += u.get("cost", 0)
        raw = (txt or "").strip().strip("`")
        raw = raw[4:] if raw.lower().startswith("json") else raw
        try:
            corrected = json.loads(raw).get("parts", [])
        except json.JSONDecodeError:
            corrected = []
        corr = [(str(p.get("part", "")).strip("().").lower()[:1], p.get("anchor", "")) for p in corrected]
        corr = [(c, anc) for c, anc in corr if c in "abcdefg"]
        if not corr or len(corr) >= len(parts):
            keep.extend(parts)                                # nothing to merge -> leave as-is
            continue
        # each current part's text, and which CORRECTED part its anchor best matches (its start)
        cur_text = [_utext(ocr, u["regions"]) for u in parts]
        starts = []                                           # corrected index -> current index it starts at
        for c, anc in corr:
            aw = vs._words(anc)
            starts.append(max(range(len(parts)),
                              key=lambda i: len(aw & vs._words(cur_text[i])) / max(1, len(aw))))
        groups = defaultdict(list)                            # corrected index -> [current parts]
        for i, u in enumerate(parts):
            ci = max([c for c in range(len(corr)) if starts[c] <= i], default=0)
            groups[ci].append(u)
        merged = [_merge(groups[ci], corr[ci][0]) for ci in sorted(groups)]
        for u in merged:
            u["id"] = f'q{num}{u["part"]}'
        keep.extend(merged)
        changed = True
        print(f"  Q{num}: {len(parts)} -> {len(merged)} parts "
              f"[{','.join(u['part'] for u in merged)}]")

    print(f"recheck cost ${cost:.4f}" + (" (no changes)" if not changed else ""))
    if changed and not a.dry:
        split["units"] = keep
        (wd / "split.json").write_text(json.dumps(split, indent=2))


def _utext(ocr, regions, limit=200):
    words = []
    for r in regions:
        pg = r["page"]
        if not (0 <= pg - 1 < len(ocr)):
            continue
        y0, y1 = r["bbox"][1], r["bbox"][3]
        for w in sorted(ocr[pg - 1], key=lambda w: w["y0"]):
            if y0 - 0.006 <= (w["y0"] + w["y1"]) / 2 <= y1 + 0.006 and str(w.get("text", "")).strip():
                words.append(str(w["text"]).strip())
    return " ".join(words)[:limit]


def _merge(units, letter):
    if len(units) == 1:
        u = dict(units[0])
        u["part"] = letter
        return u
    bypage = defaultdict(list)
    for u in units:
        for r in u["regions"]:
            bypage[r["page"]].append(r["bbox"])
    regs = [{"page": pg, "bbox": [min(b[0] for b in bbs), min(b[1] for b in bbs),
                                  max(b[2] for b in bbs), max(b[3] for b in bbs)]}
            for pg, bbs in sorted(bypage.items())]
    m = dict(units[0])
    m["part"], m["regions"] = letter, regs
    m["marks"] = sum(u.get("marks") or 0 for u in units) or None
    m["note"] = "merged by vision re-check"
    return m


if __name__ == "__main__":
    main()
