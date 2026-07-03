#!/usr/bin/env python3
"""Shared marks detection for the locate tools.

Two ways marks print on papers:
  1. Inline "(N marks)" in the question/part heading — matched by each tool's MARKS_RE
     at anchor time.
  2. NESA style: a bare digit in the right margin (x/W ≈ 0.87) on the anchor line.
     No locate regex catches these on its own; apply_margin_marks() sweeps every
     digit-only line at the right margin and assigns it to the part whose region
     contains it.

Both styles sit inside the baked crop column (0.06–0.95), so a matched part is
marksPrinted=True — bake_questions.py only stamps a marks badge on crops where
marks are known but NOT printed (marksPrinted=False).
"""
import re

MARGIN_DIGIT_RE = re.compile(r"^\d{1,2}$")
TRAILING_DIGIT_RE = re.compile(r"\s(\d{1,2})\s*$")
MARGIN_X = 0.78     # digit-only lines starting right of this are margin marks
TRAIL_X = 0.85      # lines must reach this far right for a trailing digit to be a mark
MAX_PART_MARKS = 15
HEADER_Y, FOOTER_Y = 0.05, 0.93   # corner page numbers live outside this band


def trailing_mark(text, x1):
    """Mark digit merged into the end of an anchor line (old OCR caches group the
    NESA margin digit into the text line). Only trusted when the line actually
    reaches the margin column and the value is a plausible part mark."""
    if x1 < TRAIL_X:
        return None
    m = TRAILING_DIGIT_RE.search(text)
    if m and 0 < int(m.group(1)) <= MAX_PART_MARKS:
        return int(m.group(1))
    return None


def margin_candidates(pages_lines):
    """pages_lines: per page, a list of {text, x0, y0, x1, y1} (normalised 0-1).
    Returns margin-mark candidates as {page, y (centre), marks}. Digits in the
    header/footer band are excluded — those are page numbers, not marks."""
    cands = []
    for pg, lines in enumerate(pages_lines):
        for l in lines:
            t = l["text"].strip()
            y = (l["y0"] + l["y1"]) / 2
            if MARGIN_DIGIT_RE.match(t) and l["x0"] >= MARGIN_X and HEADER_Y < y < FOOTER_Y:
                cands.append({"page": pg, "y": y, "marks": int(t)})
    return cands


def apply_margin_marks(questions, pages_lines):
    """Assign right-margin mark digits to the parts whose regions contain them.

    Fills part marks only when currently None ("(N marks)" anchors keep precedence)
    and sets marksPrinted=True on any part that contains a printed digit. Each part
    takes its topmost digit; a digit inside overlapping regions goes to the part
    whose region starts closest above it. Returns how many parts had marks filled.
    """
    parts = [p for q in questions for p in q["parts"]]
    for c in sorted(margin_candidates(pages_lines), key=lambda c: (c["page"], c["y"])):
        best, best_y0 = None, -1.0
        for p in parts:
            for r in p.get("regions", []):
                if r.get("doc"):
                    continue
                if (r["page"] == c["page"] and r["bbox"][1] <= c["y"] <= r["bbox"][3]
                        and r["bbox"][1] > best_y0):
                    best, best_y0 = p, r["bbox"][1]
        if best is not None and "_margin" not in best:
            best["_margin"] = c["marks"]

    filled = 0
    for p in parts:
        m = p.pop("_margin", None)
        if m is not None:
            if p.get("marks") is None:
                p["marks"] = m
                filled += 1
            p["marksPrinted"] = True
    return filled


def finalize_marks_printed(questions):
    """Set question-level marksPrinted and sensible part defaults.

    A whole-question crop contains every part region, so if each marked part prints
    its own marks the composed crop needs no badge. MC items count as printed —
    every MC is 1 mark and a "1 mark" badge on each would be noise.
    """
    for q in questions:
        for p in q["parts"]:
            if p.get("marksPrinted") is None:
                p["marksPrinted"] = bool(p.get("type") == "mc")
        if q.get("marksPrinted") is None:
            marked = [p for p in q["parts"] if p.get("marks") is not None]
            q["marksPrinted"] = bool(marked) and all(p["marksPrinted"] for p in marked)
