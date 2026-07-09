#!/usr/bin/env python3
"""Deterministic OCR-block -> split.json producer (Gen-3 SPLIT, source:"auto").

The plan's spine (docs/parser-pipeline-plan.md): OCR already read the pixels
(papers/_work/<pid>/ocr.json, word boxes in paper-normalised coords). We assemble those
words into question units WITHOUT a vision model drawing anything — the LLM only
double-checks later (tools review pass). Everything here is a pure function of ocr.json,
so same input -> same split, every run.

Rules enforced (see chat / SPLIT spec):
  R1  section map is read from the printed cover ("Attempt Questions 1-10",
      "Section I - N marks (pages a-b)"): MC = Q1..Qk, Section II = the rest.
  R2  a unit box never crosses a line of text — every top/bottom boundary is snapped
      into the whitespace VALLEY between two OCR text-lines, so a question is never cut
      in half and never bleeds into the next.
  R3  each MC unit spans its stem + all its options (A/B/C/D). Option rows are counted;
      < the expected option count is flagged for the QA/human pass.
  R4  paper front-matter (cover, section-cover, blank/reference pages) is furniture and
      is dropped — it is not a question.

Marks: MC questions carry no printed per-question mark (Section I total = k marks, 1 each);
Section II marks come from tools/_marks.py (inline "(N marks)" or NESA right-margin digit).

    python3 tools/ocr_to_split.py "<paperId>" [--dry]
Writes papers/_work/<pid>/split.json (source:"auto"). Run tools/invariants.py after.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _subjects import load_syllabus  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
CONTENT = ROOT / "content"

# Detection regexes are structural (question wording), not layout — they stay in code.
OPT_RE = re.compile(r"^\(?\s*([A-D])[.)]", re.I)     # "A." "B)" ; OCR-noise tolerant-ish
QNUM_RE = re.compile(r"^\s*(\d{1,2})\b")
QHEAD_RE = re.compile(r"^\s*Question\s+(\d{1,2})\b", re.I)
SEC1_PAGES = re.compile(r"Section\s*I\b.*?pages?\s+(\d+)\s*[-–]\s*(\d+)", re.I)
SEC1_RANGE = re.compile(r"Attempt\s+Questions?\s+(\d+)\s*[-–]\s*(\d+)", re.I)

# Layout knobs — overwritten per-subject from content/<subject>/parse-rules.json in main().
LEFT_MARGIN = 0.15          # a question NUMBER sits at/left of here; body text is indented
OPT_NOISE = {"cc": "C", "on": "C", "co": "C"}         # tesseract slips for option letters
FURNITURE_RE = re.compile(  # section headers, instructions, footers, blanks — not questions
    r"^(section\b|\d+\s*marks\b|attempt\s+questions|allow\s+about|use\s+the\s+multiple"
    r"|blank\s+page|do\s+not\s+write|use\s+only|instructions\b|end\s+of\s+(paper|section)"
    r"|[-–—\s]*\d+[-–—\s]*$)", re.I)

DEFAULT_RULES = {"leftMarginX": 0.15, "optionNoise": {"cc": "C", "on": "C", "co": "C"},
                 "furniture": [FURNITURE_RE.pattern]}


def load_rules(subject):
    """Per-subject layout knobs. content/<subject>/parse-rules.json overrides the defaults;
    installs them into the module globals the detectors read."""
    global LEFT_MARGIN, OPT_NOISE, FURNITURE_RE
    p = CONTENT / (subject or "") / "parse-rules.json"
    rules = dict(DEFAULT_RULES)
    if p.exists():
        rules.update(json.loads(p.read_text()))
    LEFT_MARGIN = rules.get("leftMarginX", 0.15)
    OPT_NOISE = {k.lower(): v.upper() for k, v in rules.get("optionNoise", {}).items()}
    fp = rules.get("furniture")
    if fp:
        FURNITURE_RE = re.compile("(?:" + "|".join(fp) + ")", re.I)
    return rules


def parse_range(spec):
    """'1-10' -> (1,10); '11-' -> (11,None); '5' -> (5,5)."""
    m = re.match(r"^\s*(\d+)\s*-\s*(\d*)\s*$", str(spec))
    if m:
        return int(m.group(1)), (int(m.group(2)) if m.group(2) else None)
    if str(spec).strip().isdigit():
        return int(spec), int(spec)
    return None, None


def to_lines(words, ytol=0.010):
    """Group OCR words into visual text-lines, top-to-bottom. Each -> {y0,y1,x0,text,words}."""
    ws = sorted(words, key=lambda w: (w["y0"], w["x0"]))
    lines, cur, cy = [], [], None
    for w in ws:
        if cy is None or abs(w["y0"] - cy) <= ytol:
            cur.append(w)
        else:
            lines.append(cur)
            cur = [w]
        cy = w["y0"] if cy is None else (cy + w["y0"]) / 2
    if cur:
        lines.append(cur)
    out = []
    for ln in lines:
        out.append({
            "y0": min(w["y0"] for w in ln),
            "y1": max(w["y1"] for w in ln),
            "x0": min(w["x0"] for w in ln),
            "x1": max(w["x1"] for w in ln),
            "text": " ".join(w["text"] for w in ln).strip(),
            "words": ln,
        })
    return out


def valley(lines, i):
    """Whitespace midpoint between line i-1 and line i (R2 snap point). 0 at top."""
    if i <= 0:
        return max(0.0, lines[0]["y0"] - 0.01) if lines else 0.0
    return round((lines[i - 1]["y1"] + lines[i]["y0"]) / 2, 4)


def is_option(line):
    t = line["text"]
    if OPT_RE.match(t):
        return OPT_RE.match(t).group(1).upper()
    head = re.sub(r"[^a-z]", "", t.split(" ")[0].lower())[:2]
    if head in OPT_NOISE and line["x0"] > LEFT_MARGIN:
        return OPT_NOISE[head]
    return None


# "Section I - 10 marks (pages 2 - 6)". The roman is often OCR-mangled (I->|,l,1; II->ll,11),
# so capture it loosely and normalise, then classify the range by the ACTUAL section number.
SEC_PAGES = re.compile(
    r"section\s+([ivxl0-9|ı]{1,4})\s*[-–].*?pages?\s+(\d+)\s*[-–]\s*(\d+)", re.I)


def _roman_num(s):
    s = s.lower().replace("|", "i").replace("1", "i").replace("l", "i").replace("ı", "i")
    return {"i": 1, "ii": 2, "iii": 3, "iv": 4}.get(s)


def section_map(ocr):
    """Read each 'Section N ... (pages a-b)' off the cover. Returns
    {mcPages:(lo,hi), sec2Start:n} keyed by the real section number, not page order."""
    for page in ocr[:3]:
        secs = {}
        for ln in to_lines(page):
            for m in SEC_PAGES.finditer(ln["text"]):
                n = _roman_num(m.group(1))
                if n:
                    secs.setdefault(n, (int(m.group(2)), int(m.group(3))))
        if 1 in secs:
            return {"mcPages": secs[1],
                    "sec2Start": secs[2][0] if 2 in secs else secs[1][1] + 1}
    return None


def mc_units(ocr, mc_lo, mc_hi, page_lo, page_hi):
    """One unit per MC question, Q(mc_lo)..Q(mc_hi). MC numbers are often un-OCR'd at the
    margin, but every MC question carries an A/B/C/D option block — so we anchor on the
    'A' option (a question start) rather than the number, which survives missing digits.
    A question spans from the previous question's end (snapped valley below its last option)
    down to the valley below its OWN last option; its stem sits above the A. Numbers are
    assigned in reading order and cross-checked against any margin digit we do see."""
    expected = list(range(mc_lo, mc_hi + 1))
    qs = []                         # {page, top, bot, opts, seen_num}
    for p in range(page_lo, page_hi + 1):
        if p - 1 >= len(ocr):
            break
        lines = to_lines(ocr[p - 1])
        # header furniture at the top of the first MC page -> where Q content may start
        page_top = 0.06
        for i, ln in enumerate(lines):
            if FURNITURE_RE.match(ln["text"]) and ln["y0"] < 0.22:
                page_top = valley(lines, i + 1)
        # option rows on this page, in order
        opts = [(i, is_option(ln)) for i, ln in enumerate(lines) if is_option(ln)]
        starts = [i for i, o in opts if o == "A"]      # each 'A' begins a question's options
        if not starts:
            continue
        prev_bot = page_top
        for s, ai in enumerate(starts):
            # last option line of THIS question = last opt before the next 'A' start
            nxt_a = starts[s + 1] if s + 1 < len(starts) else len(lines)
            blk = [i for i, o in opts if ai <= i < nxt_a]
            last_opt = blk[-1] if blk else ai
            bot = valley(lines, last_opt + 1) if last_opt + 1 < len(lines) \
                else round(min(0.97, lines[last_opt]["y1"] + 0.015), 4)
            letters = sorted({o for i, o in opts if ai <= i <= last_opt})
            # a margin number sitting in this question's stem band, if OCR caught it
            seen = None
            for i, ln in enumerate(lines):
                if prev_bot <= ln["y0"] < valley(lines, ai) and ln["x0"] <= LEFT_MARGIN:
                    m = QNUM_RE.match(ln["text"])
                    if m and not FURNITURE_RE.match(ln["text"]):
                        seen = int(m.group(1))
            qs.append({"page": p, "top": round(prev_bot, 4), "bot": round(bot, 4),
                       "opts": letters, "seen": seen})
            prev_bot = bot
    # Numbering: a detected block carries its REAL number when OCR caught the margin digit
    # (seen). Trust that over a naive 1..n resequence — otherwise a mid-section miss
    # renumbers everything and mislabels the rest (Barker: blocks are Q1,2,4,5,_,8,9,10, so
    # the true gaps are Q3 and Q7, not "the last two"). Blocks with no digit fill the next
    # free slot. Gaps then surface honestly in invariants' numbering-gap/count-min.
    units, expect = [], mc_lo
    for q in qs:
        seen = q["seen"]
        num = seen if (seen is not None and mc_lo <= seen <= mc_hi and seen >= expect) else expect
        expect = num + 1
        units.append({
            "number": str(num), "part": None, "marks": None, "marksPrinted": False,
            "type": "mc", "section": "I", "ruleId": "ocr-mc-options",
            "confidence": 1.0 if len(q["opts"]) >= 4 and seen == num else 0.5,
            "optionsFound": q["opts"],
            "seenNumber": q["seen"],
            "regions": [{"page": q["page"], "bbox": [0.10, q["top"], 0.90, q["bot"]]}],
        })
    return units, expected


def sec2_units(ocr, start_page):
    """Best-effort Section II: one unit per 'Question N' heading. A unit ends where the next
    heading on the SAME page begins (so consecutive boxes tile instead of overlapping to
    0.95); the last question on a page runs to the page bottom."""
    heads, seen = [], set()
    for idx in range(start_page - 1, len(ocr)):
        lines = to_lines(ocr[idx])
        for i, ln in enumerate(lines):
            m = QHEAD_RE.match(ln["text"])
            if not m or m.group(1) in seen:        # first 'Question N' wins; skip "N continued"
                continue
            seen.add(m.group(1))
            heads.append({"page": idx + 1, "number": m.group(1), "top": round(valley(lines, i), 4)})
    units = []
    for j, h in enumerate(heads):
        bot = 0.95
        if j + 1 < len(heads) and heads[j + 1]["page"] == h["page"]:
            bot = heads[j + 1]["top"]
        units.append({
            "number": h["number"], "part": None, "marks": None, "marksPrinted": False,
            "type": None, "section": "II", "ruleId": "ocr-qhead", "confidence": 0.6,
            "regions": [{"page": h["page"], "bbox": [0.10, h["top"], 0.90, round(bot, 4)]}],
        })
    return sorted(units, key=lambda u: int(u["number"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId")
    ap.add_argument("--dry", action="store_true", help="print, don't write")
    args = ap.parse_args()
    wd = WORK / args.paperId
    ocr = json.loads((wd / "ocr.json").read_text())
    info = json.loads((wd / "info.json").read_text())
    subject = info.get("subject")
    load_rules(subject)                        # per-subject layout knobs (globals)

    # Section STRUCTURE is authoritative from syllabus.json (also read by invariants.py):
    # the 'mc'-style section gives the MC number range; the next section is long-response.
    syl = load_syllabus(subject) or {}
    sections = syl.get("sections") or []
    mc_sec = next((s for s in sections if s.get("style") == "mc"), None)
    if not mc_sec:
        raise SystemExit(f"subject '{subject}' has no mc-style section in syllabus.json")
    mc_lo, mc_hi = parse_range(mc_sec.get("questions"))
    # MC/Section-II PAGE ranges aren't in the syllabus — read them from the printed cover.
    sm = section_map(ocr) or {}
    page_lo, page_hi = sm.get("mcPages", (2, 8))
    sec2_start = sm.get("sec2Start", page_hi + 1)

    mc, expected = mc_units(ocr, mc_lo, mc_hi, page_lo, page_hi)
    s2 = sec2_units(ocr, sec2_start)

    units = mc + s2
    for i, u in enumerate(units):
        u["id"] = "q" + u["number"] + (u["part"] or "")
    out = {"paperId": args.paperId, "subject": info.get("subject"),
           "source": "auto", "units": units}

    short = [u["number"] for u in mc if len(u.get("optionsFound", [])) < 4]
    print(f"  MC: {len(mc)}/{len(expected)} units (Q{mc_lo}-{mc_hi})"
          + (f"  ⚠ <4 options: Q{', Q'.join(short)}" if short else "  ✓ all have A-D"))
    print(f"  Section II: {len(s2)} 'Question N' units on pages {sec2_start}+")
    if args.dry:
        print(json.dumps(out["units"][:3], indent=2))
        return
    (wd / "split.json").write_text(json.dumps(out, indent=2))
    print(f"  wrote {wd / 'split.json'} — {len(units)} units (source:auto)")


if __name__ == "__main__":
    main()
