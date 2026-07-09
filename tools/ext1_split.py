#!/usr/bin/env python3
"""Deterministic Mathematics Extension-1 splitter  (source:"auto-ext1").

Ext-1 papers are formulaic, so segmentation is an ANCHOR problem, not a vision problem:

  Section I  = 10 multiple-choice questions (Q1-10), each a stem + options A/B/C/D.
  Section II = 4 long questions (Q11-14), each a stack of parts (a)-(e) with sub-parts
               (i)-(iii); the question total is in the "Question N (15 marks)" heading and
               per-part marks sit in the right margin.

Every boundary is placed just above the NEXT printed anchor — the next "Question N"
heading, the next part, the next sub-part ("the next (i) lot") — and dropped into the
WHITESPACE VALLEY between two OCR text-lines, so a cut NEVER crosses printed text. The
only black line a box edge may cross is the page-margin rule near the edge (that is what
the left edge at x=0.04 does on purpose).

A whole Question N is ONE unit spanning ALL of its pages (one region per page, walked
deterministically from its heading to just before the next heading) — so a multi-page
question is never truncated. MC questions are one unit each.

If a clean whitespace cut is genuinely impossible somewhere (adjacent content with no
gap), that ONE unit is flagged with a ruleException and a very low confidence for a human
to look at. This should happen at most ~once per paper; more means the OCR/anchors are off
and the whole paper wants review.

Diagrams/graphs are the ONLY thing this layer leaves for a vision model; it does not draw
or judge them.

    python3 tools/ext1_split.py "<paperId>" [--dry]

Writes papers/_work/<pid>/split.json in the grouped shape the eval UI + persist read.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ocr_to_split import to_lines, valley, is_option, load_rules, section_map  # noqa: E402
from _subjects import load_syllabus  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

# ── anchors (structural wording, OCR-noise tolerant where it matters) ──
WORDNUM = {"eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
           "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18"}
QHEAD_DIGIT_RE = re.compile(r"Question\s+(1[1-8])\b", re.I)                    # "Question 11"
QHEAD_WORD_RE = re.compile(r"Question\s+(" + "|".join(WORDNUM) + r")\b", re.I)  # "QUESTION ELEVEN"
MARKS_RE = re.compile(r"\(\s*(\d+)\s*marks?\s*\)", re.I)
MCNUM_RE = re.compile(r"^\s*(\d{1,2})\s*[.,)]")         # "1." / "1," / "2)" MC question number
# markers that end the question paper (bound the LAST question): a worked-solutions heading,
# an end-of-paper marker, a detached answer sheet, or the reference sheet. NB: the bare word
# "solution" is deliberately NOT here — it appears in question text (a chemical "solution", the
# "solutions of an equation"), which was truncating the last question. A solutions section is
# instead recognised by an unambiguous phrase OR a capitalised SOLUTIONS/Solutions heading.
POST_RE = re.compile(
    r"\b(marking\s+guidelines?|suggested\s+(solutions?|answers?)"
    r"|sample\s+answers?|worked\s+solutions?|answer\s+key"
    r"|multiple\s+choice\s+answer\s+sheet|reference\s+sheet)\b", re.I)
SOL_HEAD_RE = re.compile(r"\b(SOLUTIONS?|Solutions?)\b")   # capitalised heading (case-sensitive)
# "End of paper/exam" sits at the FOOT of the last QUESTION page (questions above it) — so the
# solutions start on the NEXT page, unlike a solutions heading which IS the first solutions page.
END_RE = re.compile(r"end\s+of\s+(the\s+)?(paper|exam(ination)?)\b", re.I)
CONT_RE = re.compile(r"continued", re.I)                   # a '(continued)' page is still a question


def head_num(text):
    """Section II question number from a heading, digits ('Question 11') or words
    ('QUESTION ELEVEN'). None if the line is not a question heading."""
    m = QHEAD_DIGIT_RE.search(text)
    if m:
        return m.group(1)
    m = QHEAD_WORD_RE.search(text)
    return WORDNUM[m.group(1).lower()] if m else None
PART_RE = re.compile(r"^\(?\s*([a-e])\s*\)")               # "(a)" / "a)"
SUB_RE = re.compile(r"^\(?\s*(i{1,3}|iv|v)\s*\)", re.I)     # "(i)".."(v)"
FURNITURE_RE = re.compile(
    r"^(section\b|\d+\s*marks\b|attempt\s+questions|allow\s+about|in\s+questions"
    r"|start\s+each|your\s+responses|or\s+calculations|use\s+the\s+multiple|blank\s+page"
    r"|do\s+not\s+write|end\s+of\s+(paper|section|examination)|reference\s+sheet"
    r"|\d+\s*\|\s*p\s*a\s*g\s*e|[-–—\s]*\d+[-–—\s]*$)", re.I)

# geometry knobs (Ext-1): left edge sits in the margin (crosses only the margin rule),
# right edge past the mark digits.
X0, X1 = 0.04, 0.93
MARK_X = 0.80              # a right-margin digit has x0 beyond this
THIN_GAP = 0.008          # a valley thinner than this can't be cut cleanly -> flag
MIN_BAND = 0.045          # a writing-space band must be at least this tall


def rows_for(ocr, page):
    """OCR text-lines for a 1-based page, top-to-bottom. Each already carries y0,y1,x0,x1,
    text and `words` (the raw OCR entries, so margin-digit marks stay inspectable)."""
    if page - 1 >= len(ocr):
        return []
    return to_lines(ocr[page - 1])


def is_furniture(line):
    return bool(FURNITURE_RE.match(line["text"].strip()))


def content_bounds(rows):
    """(top_valley, bottom_valley) around the non-furniture body of a page, or None."""
    body = [r for r in rows if not is_furniture(r)]
    if not body:
        return None
    return (max(0.0, body[0]["y0"] - 0.008), min(1.0, body[-1]["y1"] + 0.010))


def margin_mark(row):
    """A small integer sitting in the right margin of this row -> its printed marks."""
    for w in row.get("words", []):
        if w["x0"] >= MARK_X:
            m = re.match(r"^\(?\s*(\d)\s*\)?$", w["text"].strip())
            if m:
                return int(m.group(1))
    return None


def crosses_text(rows, y):
    """True if a horizontal cut at `y` would slice through a WIDE prose text-line (not just
    clip a superscript/subscript in dense math). Cuts are placed in valleys, so this should
    essentially never fire — when it does, that one unit is flagged for human review."""
    for r in rows:
        if (r["x1"] - r["x0"]) > 0.30 and r["y0"] + 0.004 < y < r["y1"] - 0.004:
            return True
    return False


# ── Section I: one unit per MC question, anchored on its NUMBER at the left margin ──
# (options are OCR-mangled math; the "1." "2." numbers are clean, and a box that runs from
#  number N to number N+1 necessarily contains all of N's options.)
def mc_units(ocr, page_lo, page_hi, mc_lo, mc_hi):
    per_page, anchors = {}, []
    for p in range(page_lo, page_hi + 1):
        rows = rows_for(ocr, p)
        per_page[p] = rows
        for i, r in enumerate(rows):
            if is_furniture(r) or r["x0"] > 0.20:         # a stem sits at the left margin
                continue
            m = MCNUM_RE.match(r["text"])
            if not m:
                continue
            num = int(m.group(1))
            rest = MCNUM_RE.sub("", r["text"], 1).strip()
            if mc_lo <= num <= mc_hi and len(rest) >= 3:  # has a stem, not a bare margin digit
                anchors.append({"page": p, "i": i, "num": num})
    anchors.sort(key=lambda a: (a["page"], a["i"]))
    units = []
    for k, a in enumerate(anchors):
        rows = per_page[a["page"]]
        top = valley(rows, a["i"])
        nxt = anchors[k + 1] if k + 1 < len(anchors) else None
        if nxt and nxt["page"] == a["page"]:
            bot = valley(rows, nxt["i"])
        else:
            cb = content_bounds(rows)
            bot = cb[1] if cb else 0.97
        exc, conf = None, 1.0
        if nxt and nxt["num"] not in (a["num"] + 1, a["num"]) and nxt["page"] == a["page"]:
            exc = {"rule": "one-mc-per-box", "reason": f"next detected number is {nxt['num']}, "
                   f"not {a['num']+1} — a number between was not OCR'd",
                   "deviation": "box may span the missing question"}
            conf = 0.3
        units.append(_unit(str(a["num"]), None, "I", 1,
                     [{"page": a["page"], "bbox": [X0, round(top, 4), X1, round(bot, 4)]}],
                     conf, exc, optionsComplete=None))
    return units


# ── Section II: whole "Question N" units spanning every page up to the next heading ──
def find_heads(ocr, sec2_start):
    """First occurrence of each 'Question N' heading across the whole paper. First wins, so a
    worked-solution that repeats 'Question 11' later is ignored."""
    heads, seen = [], set()
    for p in range(sec2_start, len(ocr) + 1):
        rows = rows_for(ocr, p)
        for i, r in enumerate(rows):
            num = head_num(r["text"])
            if not num or num in seen:
                continue
            seen.add(num)
            mk = MARKS_RE.search(r["text"])
            heads.append({"num": num, "page": p, "top": round(valley(rows, i), 4),
                          "marks": int(mk.group(1)) if mk else None, "row": i})
    return sorted(heads, key=lambda h: int(h["num"]))


def writing_bands(rows, top, bot):
    """Answer space inside [top,bot] on a page = the tall gaps that follow a part/sub-part
    label (or the stem) with no printed text until the next anchor. Bands are valley-bounded
    so they never overlap printed text. Diagrams (text-free image regions) are NOT ruled
    lines — this heuristic can't tell them apart, so bands are advisory (a vision pass
    refines them); question boxes never depend on them."""
    body = [r for r in rows if top <= r["y0"] <= bot and not is_furniture(r)]
    bands = []
    for a, b in zip(body, body[1:]):
        gap0, gap1 = a["y1"] + 0.004, b["y0"] - 0.004
        if gap1 - gap0 >= MIN_BAND:
            bands.append({"page": None, "bbox": [0.06, round(gap0, 4), X1, round(gap1, 4)]})
    if body:                                              # trailing space after the last line
        g0 = body[-1]["y1"] + 0.004
        if bot - g0 >= MIN_BAND:
            bands.append({"page": None, "bbox": [0.06, round(g0, 4), X1, round(bot, 4)]})
    return bands


def sec2_units(ocr, heads, sol_start, npages):
    units = []
    for j, h in enumerate(heads):
        if j + 1 < len(heads):
            ep, et = heads[j + 1]["page"], heads[j + 1]["top"]
        else:                                             # last question -> run to solutions
            ep, et = (sol_start - 1) if sol_start else npages, None
        regions, wbands, flagged, part_marks = [], [], None, 0
        for p in range(h["page"], ep + 1):
            rows = rows_for(ocr, p)
            cb = content_bounds(rows)
            if cb is None:                                # blank continuation = answer space
                if p != ep or et is None:
                    regions.append({"page": p, "bbox": [X0, 0.04, X1, 0.96]})
                continue
            ctop, cbot = cb
            top = h["top"] if p == h["page"] else ctop
            if p == ep and et is not None:
                if et <= ctop + 1e-3:                     # next heading is first thing here
                    continue
                bot = et
            else:
                bot = cbot
            if bot - top < 0.02:
                continue
            if crosses_text(rows, top) or crosses_text(rows, bot):
                flagged = {"rule": "cut-in-whitespace",
                           "reason": "no clean gap between adjacent content at a page boundary",
                           "deviation": "cut placed at the tightest available gap"}
            regions.append({"page": p, "bbox": [X0, round(top, 4), X1, round(bot, 4)]})
            for b in writing_bands(rows, top, bot):
                b["page"] = p
                wbands.append(b)
            for r in rows:
                if (PART_RE.match(r["text"]) or SUB_RE.match(r["text"])):
                    mm = margin_mark(r)
                    if mm:
                        part_marks += mm
        marks = h["marks"] or (part_marks or None)
        conf = 0.9 if (h["marks"] and not flagged) else (0.3 if flagged else 0.7)
        units.append(_unit(h["num"], None, "II", marks, regions, conf, flagged,
                           writingSpace=wbands,
                           note=(f"per-part marks sum={part_marks}" if part_marks and
                                 h["marks"] and part_marks != h["marks"] else "")))
    return units


def _unit(number, part, section, marks, regions, confidence, exc, **extra):
    u = {"id": "q" + number + (part or ""), "number": number, "part": part,
         "section": section, "marks": marks, "marksPrinted": marks is not None,
         "type": "mc" if section == "I" else None, "ruleId": "auto-ext1",
         "confidence": round(confidence, 3), "ruleException": exc,
         "writingSpace": [], "regions": regions, "note": ""}
    u.update(extra)
    return u


def paper_end(ocr, after_page):
    """First page AFTER the last question heading that begins the post-question material —
    a worked-solutions heading, an end-of-paper marker, a detached answer sheet, or the
    reference sheet. Used to bound the LAST question so it doesn't swallow the solutions.
    The short-line test keeps the word 'solution' inside a question sentence from matching.
    None -> nothing found; the last question runs to the final page."""
    for p in range(after_page + 1, len(ocr) + 1):
        rows = rows_for(ocr, p)
        if any(CONT_RE.search(r["text"]) for r in rows):     # '(continued)' -> still a question
            continue
        for r in rows:
            t = r["text"]
            if len(t) > 45 or head_num(t) is not None:
                continue
            if END_RE.search(t):                             # last question page -> solutions next
                return p + 1 if p < len(ocr) else None
            if POST_RE.search(t) or SOL_HEAD_RE.search(t):   # this page IS the solutions start
                return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    wd = WORK / args.paperId
    ocr = json.loads((wd / "ocr.json").read_text())
    info = json.loads((wd / "info.json").read_text())
    subject = info.get("subject")
    load_rules(subject)

    syl = load_syllabus(subject) or {}
    secs = syl.get("sections") or []
    mc_sec = next((s for s in secs if s.get("style") == "mc"), {"questions": "1-10"})
    mc_lo, mc_hi = (int(x) for x in str(mc_sec["questions"]).split("-"))

    sm = section_map(ocr) or {}
    page_lo = sm.get("mcPages", (2, 4))[0]

    # Section II begins at the FIRST real 'Question N' heading — more reliable than the cover's
    # page range. MC therefore occupies every page from the cover up to that heading.
    heads = find_heads(ocr, max(3, sm.get("sec2Start", 4) - 1))
    sec2_start = heads[0]["page"] if heads else sm.get("sec2Start", 5)
    last_head_page = max((h["page"] for h in heads), default=sec2_start)
    sol_start = paper_end(ocr, last_head_page)               # bound the last question
    mc = mc_units(ocr, page_lo, sec2_start - 1, mc_lo, mc_hi)
    s2 = sec2_units(ocr, heads, sol_start, len(ocr))
    units = mc + s2

    found_mc = {int(u["number"]) for u in mc}
    missing_mc = [n for n in range(mc_lo, mc_hi + 1) if n not in found_mc]
    nflag = sum(1 for u in units if u.get("ruleException"))
    out = {"paperId": args.paperId, "subject": subject, "source": "auto-ext1",
           "sectionIIStartPage": sec2_start, "solutionsStartPage": sol_start,
           "missingMC": missing_mc, "units": units}

    print(f"  MC {len(mc)}/{mc_hi - mc_lo + 1}"
          f"{'  ⚠missing Q'+','.join(map(str,missing_mc)) if missing_mc else ''}  ·  "
          f"Section II {len(s2)} units "
          f"(Q{'-'.join(h['num'] for h in heads[:1]+heads[-1:]) if heads else '?'})  ·  "
          f"solStart={sol_start}  ·  flagged={nflag}")
    for u in s2:
        pages = sorted({r["page"] for r in u["regions"]})
        print(f"    Q{u['number']}: marks={u['marks']} conf={u['confidence']} "
              f"pages={pages} ws={len(u['writingSpace'])}"
              + ("  ⚠FLAG" if u["ruleException"] else ""))
    if args.dry:
        return
    (wd / "split.json").write_text(json.dumps(out, indent=2))
    print(f"  wrote split.json — {len(units)} units (source:auto-ext1)")


if __name__ == "__main__":
    main()
