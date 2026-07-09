#!/usr/bin/env python3
"""Whole-paper SEMANTIC invariant (DeepSeek, text-only).

After geometry + the geometric rules, this reads the ENTIRE segmented paper as text and asks
a reasoning model whether each unit is ONE complete, coherent question — catching what
geometry can't: a part that's mis-split, two questions merged, half a question, a duplicate,
a missing part, or marks that don't total the paper. Flag-first: it records issues for review,
it never silently re-splits.

Unit text comes from the OCR already on disk (no vision, ~$0.001-0.002/paper).

    python3 tools/semantic_check.py <paperId> [--write]

Exit 0 if the model finds no issues, 1 otherwise.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import or_client as orc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

HINT = ("Consecutive LETTER labels (a),(b),(c) are SEPARATE top-level parts; roman numerals "
        "(i),(ii),(iii) — the italic ones — are SUB-PARTS that stay together (especially when a "
        "later one says 'hence' / 'using the above').")


def unit_text(ocr, regions, limit=320):
    words = []
    for r in regions:
        pg = r["page"]
        if not (0 <= pg - 1 < len(ocr)):
            continue
        x0, y0, x1, y1 = r["bbox"]
        for w in sorted(ocr[pg - 1], key=lambda w: (w["y0"], w["x0"])):
            cy = (w["y0"] + w["y1"]) / 2
            if y0 - 0.006 <= cy <= y1 + 0.006 and str(w.get("text", "")).strip():
                words.append(str(w["text"]).strip())
    return " ".join(words)[:limit]


def review(split, ocr):
    listing = []
    for u in split.get("units", []):
        tag = f'{u.get("section")}{" " + u["part"] if u.get("part") else ""}, marks={u.get("marks")}'
        listing.append(f'{u["id"]} [{tag}]: {unit_text(ocr, u.get("regions", []))}')
    prompt = (
        "Here is a fully segmented HSC Mathematics Extension 1 paper — every unit with the text "
        "inside its box. Expected structure: Section I = 10 multiple-choice (Q1-10, 1 mark each); "
        "Section II = Q11-14, each split into top-level parts (a),(b),… ; whole paper totals 70 "
        "marks (Section II = 60).\n\n" + HINT + "\n\n"
        "The text is raw OCR and WILL contain garbled math, spelling and symbol errors — "
        "IGNORE all of that. Judge ONLY the STRUCTURE / boundaries. Flag a unit ONLY if:\n"
        "- it clearly contains TWO separate unrelated questions merged into one, or\n"
        "- it is obviously HALF a question (starts or ends mid-problem, belongs with a neighbour), or\n"
        "- it DUPLICATES another unit, or a top-level part is clearly MISSING between two others, or\n"
        "- its label is wrong (e.g. tagged (a) but the text is really part (d)).\n"
        "Do NOT flag garbled options, OCR typos, missing marks, or diagrams-not-shown. If the "
        "boundaries look right, return no issues. Output STRICT JSON ONLY:\n"
        '{"ok": true, "issues": [{"unit": "q13c", "problem": "short description"}]}\n\n'
        "UNITS:\n" + "\n".join(listing))
    cost = 0.0
    out = None
    for reasoning_cap in (900, 400):                      # retry with less reasoning -> more room
        txt, u = orc.chat(orc.REASON_MODEL, [{"role": "user", "content": prompt}],
                          max_tokens=4500, reasoning={"max_tokens": reasoning_cap},
                          response_format={"type": "json_object"})
        cost += u.get("cost", 0)
        out = _parse_json(txt)
        if out is not None:
            break
    if out is None:
        out = {"ok": False, "issues": [{"unit": "?", "problem": "semantic check unparseable"}]}
    out["cost"] = cost
    return out


def _parse_json(txt):
    """Robust: strip fences, slice to the outermost braces, and repair the common truncation
    (an unterminated issues array) before giving up."""
    raw = (txt or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw[4:].strip() if raw.lower().startswith("json") else raw
    i, j = raw.find("{"), raw.rfind("}")
    if i >= 0 and j > i:
        raw = raw[i:j + 1]
    for candidate in (raw, re.sub(r",\s*[^}\]]*$", "", raw) + "]}", raw + '"}]}'):
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            continue
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    wd = WORK / a.paperId
    split = json.loads((wd / "split.json").read_text())
    ocr = json.loads((wd / "ocr.json").read_text()) if (wd / "ocr.json").exists() else []
    r = review(split, ocr)
    issues = r.get("issues") or []
    ok = bool(r.get("ok")) and not issues
    for it in issues:
        print(f"  [flag] {it.get('unit', '?')}: {it.get('problem', '')}")
    print(f"  => semantic {'OK' if ok else str(len(issues)) + ' issue(s)'}  (${r.get('cost', 0):.5f})")
    if a.write:
        split["semantic"] = {"ok": ok, "issues": issues}
        if not ok:
            for u in split["units"]:
                if any(i.get("unit") == u["id"] for i in issues):
                    u["confidence"] = min(u.get("confidence", 0.9) or 0.9, 0.5)
        (wd / "split.json").write_text(json.dumps(split, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
