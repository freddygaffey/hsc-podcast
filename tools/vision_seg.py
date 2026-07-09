#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Vision box pass (Qwen3-VL via OpenRouter) — the boxes OCR can't do reliably.

Runs on top of the deterministic ext1_split (which is kept for the Section II page ranges
and printed marks). Produces:
  - Section I : one box per MC question (numbers OCR often drops on math pages).
  - Section II: one box per LETTERED PART (a),(b),(c)… — a Section II question is NEVER one
    unit. Roman sub-parts (i),(ii),(iii) stay INSIDE their letter's box.

Merges into split.json. Cheap (~$0.002/page). Key: ~/.config/hsc/openrouter.key.

    python3 tools/vision_seg.py <paperId> [--dry]
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import or_client as orc  # noqa: E402
from ocr_to_split import to_lines  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def margin_marks(ocr, page, y0, y1):
    """Sum the printed per-part marks — the small right-margin digits (x ~0.80-0.95) inside a
    unit's vertical band. Also accepts a digit at the END of a right-margin token ('… 3').
    None if none found."""
    if not (0 <= page - 1 < len(ocr)):
        return None
    total, found = 0, False
    for w in ocr[page - 1]:
        cy = (w["y0"] + w["y1"]) / 2
        if w.get("x0", 0) >= 0.74 and y0 - 0.02 <= cy <= y1 + 0.02:
            t = str(w.get("text", "")).strip()
            m = re.match(r"^\(?\s*([1-9])\s*\)?$", t) or re.search(r"(?<!\d)([1-9])\s*$", t)
            if m:
                total += int(m.group(1))
                found = True
    return total if found else None


def whitespace_rows(pid, page, boxes=None, band=4):
    """Cut-safe rows = clear of BOTH text ink AND any vision box. Painting the vision boxes as
    'occupied' means a boundary can only land in the GAP BETWEEN boxes (never inside one, so it
    can't cut between two option rows). A row is safe only if it's in a contiguous clear band
    (>= +/-`band` rows), so tall math (fraction bars) is never cut. Returns (bool-per-row, h)."""
    try:
        import numpy as np
        from PIL import Image
    except Exception:
        return None, 0
    p = WORK / pid / f"p{page:02d}.png"
    if not p.exists():
        return None, 0
    arr = np.asarray(Image.open(p).convert("L"))
    h, w = arr.shape
    clear = (arr < 170).sum(axis=1) < max(3, w * 0.004)     # no text ink
    for bb in (boxes or []):                                # AND not inside a vision box
        clear[max(0, int(bb[1] * h)):min(h, int(bb[3] * h))] = False
    safe = clear.copy()
    for d in range(1, band + 1):
        safe[d:] &= clear[:-d]
        safe[:-d] &= clear[d:]
    return safe, h


def snap_ws(ws, h, y, window=0.05):
    """Move a boundary at normalised y to the nearest all-white PNG row within +/-window,
    so the cut lands in real whitespace (never through ink). No-op if no clear row is near."""
    if ws is None or h == 0:
        return y
    yr = int(y * h)
    lo, hi = max(0, int((y - window) * h)), min(h - 1, int((y + window) * h))
    cand = [r for r in range(lo, hi + 1) if ws[r]]
    return round(min(cand, key=lambda r: abs(r - yr)) / h, 4) if cand else y


def _words(s):
    return set(re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split())


FURNITURE_RE = re.compile(
    r"^(examination continues|end of (paper|section|examination)|question \d+ \(|blank page"
    r"|\d+\s*$|.{0,3}\|\s*p\s*a\s*g\s*e|section (i|ii)\b)", re.I)


def _content_bottom(lines):
    """Bottom of the LAST real content line — skips furniture (footers, 'continues overleaf',
    the next 'Question N' heading, page numbers) so a box doesn't trail into dead space."""
    body = [ln for ln in lines if not FURNITURE_RE.match(ln.get("text", "").strip())]
    return min(0.975, (body[-1]["y1"] if body else 0.95) + 0.012)


def _out(ws, h, y, step):
    """Move a boundary at normalised y OUTWARD (step=-1 up / +1 down) until it reaches a
    cut-safe whitespace band — so an edge only grows to stop obscuring text, never cuts in."""
    if ws is None or h == 0:
        return y
    r = int(y * h)
    while 0 < r < h - 1 and not ws[r]:
        r += step
    return round(r / h, 4)


def _row_profile(pid, page):
    """Per-row darkness of a page PNG -> (ink, clear, darkfrac, h). ink = row has text; clear =
    row is essentially blank. Cached-free; the one place the raw pixel profile is computed."""
    try:
        import numpy as np
        from PIL import Image
    except Exception:
        return None, None, None, 0
    p = WORK / pid / f"p{page:02d}.png"
    if not p.exists():
        return None, None, None, 0
    arr = np.asarray(Image.open(p).convert("L"))
    h, w = arr.shape
    darkfrac = (arr < 170).mean(axis=1)
    ink = darkfrac >= max(3, w * 0.004) / w
    clear = darkfrac < 0.012
    return ink, clear, darkfrac, h


def _detect_rules(darkfrac, clear):
    """Rows that are a real HORIZONTAL RULE: a strong full-width line with a genuine whitespace
    BUFFER above AND below (a section divider). The buffer is enforced hard (both ~9-row bands
    must be >=85% blank) so a graph axis / diagram edge — which has figure ink hugging it — is
    NEVER mistaken for a rule. Returns a boolean row mask."""
    import numpy as np
    h = len(darkfrac)
    rule = np.zeros(h, bool)
    for r in np.where(darkfrac > 0.55)[0]:
        above, below = clear[max(0, r - 12):max(1, r - 3)], clear[r + 4:r + 13]
        if above.size and below.size and above.mean() > 0.85 and below.mean() > 0.85:
            rule[r] = True
    return rule


def rule_rows(pid, page):
    """Row indices of true horizontal rules on a page (for the debug overlay)."""
    ink, clear, darkfrac, h = _row_profile(pid, page)
    if darkfrac is None:
        return [], 0
    import numpy as np
    return list(np.where(_detect_rules(darkfrac, clear))[0]), h


def _gap_mid(clear, h, y_lo, y_hi):
    """Normalised y at the MIDDLE of the widest blank run in [y_lo, y_hi], or None if the band
    has no blank row. This is where a boundary between two parts belongs — dead centre of the
    whitespace that separates them, so the cut can't touch either part's ink."""
    if clear is None or h == 0:
        return None
    r0, r1 = max(0, int(y_lo * h)), min(h - 1, int(y_hi * h))
    if r1 <= r0:
        return None
    best, s = (0, -1), None
    for r in range(r0, r1 + 1):
        if clear[r]:
            s = r if s is None else s
        elif s is not None:
            best, s = ((s, r) if r - s > best[1] - best[0] else best), None
    if s is not None and r1 - s > best[1] - best[0]:
        best = (s, r1)
    return round((best[0] + best[1]) / 2 / h, 4) if best[1] >= best[0] else None


def _grow_edge(clear, h, y, up, min_gap=0.018, stop=None):
    """Grow an outer edge (top of the first part / bottom of the last) OUTWARD from y until it
    sits inside the first blank band >= min_gap — i.e. stop at the first real gap, 'not too big
    nor too small'. STOPS at a horizontal rule (a section divider) so a first part never grows up
    past the rule into header furniture. Falls back to the page edge if none is found."""
    if clear is None or h == 0:
        return round(y, 4)
    step, g, run = (-1 if up else 1), int(min_gap * h), 0
    r, end = int(y * h), (0 if up else h - 1)
    while r != end:
        if stop is not None and 0 <= r < len(stop) and stop[r]:   # a rule bounds the growth
            return round((r - step) / h, 4)                       # settle just inside the rule
        run = run + 1 if clear[r] else 0
        if run >= g:
            return round((r + (run // 2) * (1 if up else -1)) / h, 4)
        r += step
    return round(max(0, min(h - 1, r)) / h, 4)


def content_blocks(pid, page, min_gap=0.032):
    """The PNG's real content blocks: runs of ink separated by clear gaps >= min_gap of page
    height, AND force-split at HORIZONTAL RULE lines. Kept for the debug overlay (purple bars);
    the tiler no longer derives boxes from these. Returns [(top, bottom)] normalised."""
    ink, clear, darkfrac, h = _row_profile(pid, page)
    if darkfrac is None:
        return []
    rule = _detect_rules(darkfrac, clear)
    g = int(min_gap * h)
    out, start, last, run = [], None, None, 0
    for r in range(h):
        if rule[r]:                                       # a divider ends the current block
            if start is not None:
                out.append((round(start / h, 4), round(last / h, 4)))
            start, run = None, g
            continue
        if ink[r]:
            if start is None:
                start = r
            last, run = r, 0
        elif start is not None:
            run += 1
            if run >= g:
                out.append((round(start / h, 4), round(last / h, 4)))
                start = None
    if start is not None:
        out.append((round(start / h, 4), round(last / h, 4)))
    return out


def ink_bbox(pid, page, y0, y1, padx=0.008, pady=0.012):
    """Shrink-wrap: the tight bounding box of the actual ink between y0..y1, plus a small pad.
    Trims wasted side margins and blank space (e.g. below a part, before the footer)."""
    try:
        import numpy as np
        from PIL import Image
    except Exception:
        return None
    p = WORK / pid / f"p{page:02d}.png"
    if not p.exists():
        return None
    arr = np.asarray(Image.open(p).convert("L"))
    h, w = arr.shape
    r0, r1 = max(0, int(y0 * h)), min(h, int(y1 * h))
    sub = arr[r0:r1] < 170
    if r1 <= r0 or not sub.any():
        return None
    rows, cols = np.where(sub.any(axis=1))[0], np.where(sub.any(axis=0))[0]
    return [round(max(0.0, cols[0] / w - padx), 4), round(max(0.0, (r0 + rows[0]) / h - pady), 4),
            round(min(1.0, cols[-1] / w + padx), 4), round(min(1.0, (r0 + rows[-1]) / h + pady), 4)]


def _page_dark(pid, page):
    """The page PNG as a boolean ink mask (True = dark/text) plus its (H, W). One read."""
    try:
        import numpy as np
        from PIL import Image
    except Exception:
        return None, 0, 0
    p = WORK / pid / f"p{page:02d}.png"
    if not p.exists():
        return None, 0, 0
    arr = np.asarray(Image.open(p).convert("L"))
    return (arr < 170), arr.shape[0], arr.shape[1]


def _text_runs(rowtext, buf, rules=None):
    """Merge rows of text into runs, joining gaps <= buf rows. A gap > buf is REAL whitespace; a
    gap <= buf is treated as inside content (the dot-of-an-'i' / fraction-bar gap), so a single
    clear row never breaks a run. A horizontal RULE is a hard break too — it always ends a run.
    Returns [(top_row, bottom_row)]."""
    runs, start, last = [], None, None
    for i, t in enumerate(rowtext):
        if rules is not None and rules[i]:                  # a rule divider ends the run
            if start is not None:
                runs.append((start, last))
                start = None
            continue
        if t:
            start = i if start is None else start
            last = i
        elif start is not None and i - last > buf:
            runs.append((start, last))
            start = None
    if start is not None:
        runs.append((start, last))
    return runs


def _run_edge(runs, row, buf, top):
    """The top (or bottom) row of the merged run that contains/touches `row`; `row` itself if
    none (so the caller's contain-the-vision-box clamp then decides)."""
    for a, b in runs:
        if a - buf <= row <= b + buf:
            return a if top else b
    return row


def _clear_mid(rowtext, H, y_a, y_b, rules=None):
    """Normalised y where a shared boundary between two overlapping units belongs — real
    whitespace (or a rule), never text. Prefers snapping to a horizontal RULE between them (a
    rule IS a break); otherwise the middle of the WIDEST whitespace run. None if neither exists."""
    r0, r1 = max(0, int(min(y_a, y_b) * H)), min(H - 1, int(max(y_a, y_b) * H))
    if rules is not None:                                    # a rule between them is the break
        rr = [r for r in range(r0, r1 + 1) if rules[r]]
        if rr:
            return round(rr[len(rr) // 2] / H, 4)
    best, s = (0, -1), None
    for r in range(r0, r1 + 1):
        if not rowtext[r]:
            s = r if s is None else s
        elif s is not None:
            best, s = ((s, r) if r - s > best[1] - best[0] else best), None
    if s is not None and r1 - s > best[1] - best[0]:
        best = (s, r1)
    return round((best[0] + best[1]) / 2 / H, 4) if best[1] >= best[0] else None


# Buffer sizing (fractions of page height). buf = the whitespace band that counts as a REAL gap
# — bigger than a within-character gap, smaller than the gap between two questions/parts. Tunable
# live from the annotated view; these are just the defaults.
BUF_FRAC, PAD_FRAC = 0.02, 0.006


def tile_page(items, lines, ws=None, h=0, blocks=None, pid=None, page=None, x0=0.04, x1=0.93,
              buf_frac=BUF_FRAC, pad_frac=PAD_FRAC, padx=0.008):
    """ONE output box per vision box. Rule (per the human spec): the green box always CONTAINS the
    blue vision box vertically (never shorter up/down, so text is never cut), and only ever grows
    OUTWARD from it — through any text the vision box clipped — stopping at the first REAL gap. A
    real gap is a band of whitespace >= `buf` rows; a thinner clear strip (a character/fraction
    gap) does not count, so an edge can't settle inside a glyph. Horizontally the box shrink-wraps
    to its own ink (+pad). Edges are clamped to the mid-gap with each neighbour so a box can never
    reach into an adjacent unit."""
    if not items:
        return []
    items = sorted(items, key=lambda it: it.get("vy0", 0.0))
    dark, H, W = _page_dark(pid, page) if pid else (None, 0, 0)
    n = len(items)
    if dark is None:                                          # no pixels -> stack by vision boxes
        return [(it, [x0, round(it.get("vy0", 0.0), 4), x1,
                      round(it.get("vy1", it.get("vy0", 0.0) + 0.05), 4)]) for it in items]
    import numpy as np
    cx0, cx1 = int(0.03 * W), int(0.97 * W)                  # ignore the extreme page margins
    rowtext = dark[:, cx0:cx1].sum(axis=1) >= max(3, 0.004 * (cx1 - cx0))
    darkfrac = dark.mean(axis=1)
    rules = _detect_rules(darkfrac, darkfrac < 0.012)        # horizontal rules = hard breaks
    buf = max(2, int(buf_frac * H))
    pad = pad_frac
    runs = _text_runs(rowtext, buf, rules)

    # pass 1 — each box contains its vision box and extends outward through any clipped text
    # (the merged run covering the vision edge); top only moves up, bottom only down.
    tops, bots, cens = [], [], []
    for it in items:
        vy0 = it.get("vy0", 0.0)
        vy1 = it.get("vy1", vy0 + 0.05)
        r0, r1 = int(vy0 * H), int(vy1 * H)
        tops.append(max(0.0, min(_run_edge(runs, r0, buf, top=True), r0) / H - pad))
        bots.append(min(1.0, max(_run_edge(runs, r1, buf, top=False), r1) / H + pad))
        cens.append((vy0 + vy1) / 2)
    # only trim FOOTER furniture that sits BELOW the last vision box — never cut real content
    # (OCR can miss lower options, so an OCR-based "content end" must not override the vision box)
    foot = min([ln["y0"] for ln in (lines or [])
                if FURNITURE_RE.match(ln.get("text", "").strip())
                and ln["y0"] > items[-1].get("vy1", 1.0) + 0.01], default=None)
    if foot is not None:
        bots[-1] = min(bots[-1], foot - 0.004)

    # pass 2 — where two boxes overlap (Qwen's boxes can overlap each other), drop the shared
    # boundary into the whitespace gap BETWEEN the two text bodies, so neither crosses text.
    for i in range(n - 1):
        if tops[i + 1] < bots[i] - 1e-4:
            m = _clear_mid(rowtext, H, cens[i], cens[i + 1], rules)
            if m is None or not (tops[i] < m < bots[i + 1]):
                m = round((cens[i] + cens[i + 1]) / 2, 4)
            bots[i] = min(bots[i], m)
            tops[i + 1] = max(tops[i + 1], m)

    out = []
    for i, it in enumerate(items):
        top, bot = tops[i], max(tops[i] + 0.005, bots[i])
        sub = dark[int(top * H):max(int(top * H) + 1, int(bot * H))]   # sides: shrink-wrap to ink
        cols = np.where(sub.any(axis=0))[0]
        lx = max(0.0, cols[0] / W - padx) if cols.size else x0
        rx = min(1.0, cols[-1] / W + padx) if cols.size else x1
        out.append((it, [round(lx, 4), round(top, 4), round(rx, 4), round(bot, 4)]))
    return out

MC_PROMPT = (
    "This is one page of an HSC Mathematics Extension 1 multiple-choice section. Find every "
    "multiple-choice question on this page. For EACH return its number, an 'anchor' = the first "
    "~8 words of the question stem VERBATIM, and a box containing the number, stem, any "
    "diagram AND all four options (A)(B)(C)(D). Output STRICT JSON only:\n"
    '{"questions":[{"number":1,"anchor":"What is the derivative of","bbox":[x0,y0,x1,y1]}]}\n'
    "coords are FRACTIONS of the page (0-1), origin top-left. Empty list if none.")

SEC2_PROMPT = (
    "This page is from Section II (long response) of an HSC Mathematics Extension 1 paper. "
    "It contains parts of question(s): {qs}.\n\n"
    "A Section II question is NEVER one unit — split it into ONE UNIT PER TOP-LEVEL "
    "SUB-QUESTION. The top level is USUALLY lettered (a), (b), (c), … but some papers use "
    "roman (i),(ii) or numbers 1.,2. at the top level instead — split at whatever the "
    "top-level labels are. The NEXT level down (e.g. roman (i),(ii) under a letter) stays "
    "TOGETHER inside its parent's box — never split the deeper level out.\n\n"
    "For each top-level part on THIS page, return its QUESTION number (from the list above), "
    "its part label, an 'anchor' = the first ~8 words of that part's FIRST line VERBATIM "
    "(include the label, e.g. '(a) A ball is thrown from'), and a box. STRICT JSON only:\n"
    '{"parts":[{"question":14,"part":"a","anchor":"(a) A ball is thrown from","bbox":[x0,y0,x1,y1]}]}\n'
    "coords are FRACTIONS of the page (0-1), origin top-left, left edge ~0.04. A part "
    "continuing from the previous page (no new label at the top) still gets a box with its "
    "letter. Empty list if this page has no question parts (blank / instructions / reference).")


MC_ID_PROMPT = (
    "Below is the OCR text of ONE page from the multiple-choice section of an HSC Mathematics "
    "Extension 1 paper. The OCR is noisy (garbled math) — ignore that. List EVERY multiple-choice "
    "question that STARTS on this page (each begins with a number 1-10). For each give its number "
    "and 'anchor' = the first ~8 words of its stem, copied verbatim from the OCR. STRICT JSON only:\n"
    '{"questions":[{"number":1,"anchor":"What is the magnitude of"}]}\n\nOCR TEXT:\n')

SEC2_ID_PROMPT = (
    "Below is the OCR text of ONE page from Section II of an HSC Mathematics Extension 1 paper. "
    "It contains parts of question(s): {qs}. The OCR is noisy — ignore garbled math.\n\n"
    "List each TOP-LEVEL part on this page. HINT: consecutive LETTER labels (a),(b),(c) are "
    "SEPARATE top-level parts; roman numerals (i),(ii) are SUB-parts that stay INSIDE their "
    "letter — do NOT list sub-parts as top-level. If a part continues from the previous page with "
    "no label, still list it with its letter. For each top-level part give its question number, "
    "its part label, and 'anchor' = the first ~8 words of that part's first line copied verbatim "
    "from the OCR. STRICT JSON only:\n"
    '{"parts":[{"question":14,"part":"a","anchor":"(a) In triangle ABC AM is"}]}\n\nOCR TEXT:\n')


def page_text(ocr, page):
    if not (0 <= page - 1 < len(ocr)):
        return ""
    ws = sorted(ocr[page - 1], key=lambda w: (round(w["y0"], 3), w["x0"]))
    return "\n".join(w.get("text", "").strip() for w in ws if str(w.get("text", "")).strip())


def _identify(prompt, key, cache=None):
    """DeepSeek reads OCR TEXT and lists the units (no vision). Returns (items, cost)."""
    ck = f"id:{key}:{hashlib.md5(prompt.encode()).hexdigest()[:10]}"
    if cache is not None and ck in cache:
        txt, cost = cache[ck], 0.0
    else:
        txt, u = orc.chat(orc.REASON_MODEL, [{"role": "user", "content": prompt}],
                          max_tokens=2000, reasoning={"max_tokens": 900},
                          response_format={"type": "json_object"})
        cost = u.get("cost", 0)
        if cache is not None:
            cache[ck] = txt
    raw = (txt or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`").lstrip("json").strip()
    try:
        return json.loads(raw).get(key, []), cost
    except json.JSONDecodeError:
        return [], cost


def _norm(v):
    return v / 1000.0 if v > 1.5 else v


def _boxes(pid, page, prompt, key, cache=None):
    # reuse a cached model response when the prompt is unchanged (keyed by prompt hash), so
    # iterating on the deterministic tiler/rules never re-calls (or re-pays for) the model.
    ck = f"{key}:{page}:{hashlib.md5(prompt.encode()).hexdigest()[:10]}"
    if cache is not None and ck in cache:
        txt, cost = cache[ck], 0.0
    else:
        img = WORK / pid / f"p{page:02d}.png"
        txt, u = orc.ask_image(orc.VISION_MODEL, str(img), prompt, max_tokens=1400,
                               response_format={"type": "json_object"})
        cost = u.get("cost", 0)
        if cache is not None:
            cache[ck] = txt
    raw = (txt or "").strip()
    if raw.startswith("```"):
        raw = raw.strip("`").lstrip("json").strip()
    try:
        items = json.loads(raw).get(key, [])
    except json.JSONDecodeError:
        items = []
    out = []
    for it in items:
        bb = it.get("bbox") or []
        if len(bb) == 4:
            x0, y0, x1, y1 = (_norm(float(v)) for v in bb)
            if x1 > x0 and y1 > y0:
                it["bbox"] = [round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4)]
                out.append(it)
    return out, cost


def _is_ii(s):
    return "II" in str(s or "").replace(" ", "").upper()


def page_boxes(pid, page, buf_frac=BUF_FRAC, pad_frac=PAD_FRAC):
    """Compute one page's final (green) boxes LIVE from the cached vision responses (no model
    cost), with tunable buffers. Returns [(label, [x0,y0,x1,y1])]. Lets the annotated view retune
    `buf`/`pad` and re-render without rewriting split.json."""
    wd = WORK / pid
    split = json.loads((wd / "split.json").read_text())
    ocr = json.loads((wd / "ocr.json").read_text()) if (wd / "ocr.json").exists() else []
    cp = wd / "vision_cache.json"
    cache = json.loads(cp.read_text()) if cp.exists() else {}
    lines = to_lines(ocr[page - 1]) if 0 <= page - 1 < len(ocr) else []
    sec2 = split.get("sectionIIStartPage") or 5

    if page < sec2:                                          # Section I: one box per MC question
        b, _ = _boxes(pid, page, MC_PROMPT, "questions", cache)
        items = [{"n": int(it["number"]), "vy0": it["bbox"][1], "vy1": it["bbox"][3]}
                 for it in b if str(it.get("number", "")).strip().isdigit()
                 and 1 <= int(it["number"]) <= 10]
        return [(f'q{it["n"]}', bb) for it, bb in
                tile_page(items, lines, pid=pid, page=page, buf_frac=buf_frac, pad_frac=pad_frac)]

    page_q = {}                                              # Section II: parts on this page
    for u in split.get("units", []):
        if _is_ii(u.get("section")):
            for r in u.get("regions", []):
                page_q.setdefault(r["page"], [])
                if u["number"] not in page_q[r["page"]]:
                    page_q[r["page"]].append(u["number"])
    qs = page_q.get(page)
    if not qs:
        return []
    prompt = SEC2_PROMPT.replace("{qs}", ", ".join(str(x) for x in sorted(qs, key=int)))
    parts, _ = _boxes(pid, page, prompt, "parts", cache)
    items = []
    for it in parts:
        q = str(it.get("question", qs[0]))
        letter = str(it.get("part", "")).strip().lower().strip("().")[:3]
        if letter:
            items.append({"q": q, "letter": letter, "vy0": it["bbox"][1], "vy1": it["bbox"][3]})
    return [(f'q{it["q"]}{it["letter"]}', bb) for it, bb in
            tile_page(items, lines, pid=pid, page=page, buf_frac=buf_frac, pad_frac=pad_frac)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paperId")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    wd = WORK / a.paperId
    split = json.loads((wd / "split.json").read_text())
    ocr = json.loads((wd / "ocr.json").read_text())

    def lines_for(p):
        return to_lines(ocr[p - 1]) if 0 <= p - 1 < len(ocr) else []

    ws_cache = {}

    def ws_for(p):
        if p not in ws_cache:
            ws_cache[p] = whitespace_rows(a.paperId, p)
        return ws_cache[p]
    sec2 = split.get("sectionIIStartPage") or 5
    sol = split.get("solutionsStartPage")
    cost = 0.0
    cache_path = wd / "vision_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    # ── Section I: Qwen-VL identifies + reads each MC (reliable on garbled OCR); positioned
    #    by its anchor text -> OCR line -> PNG whitespace ──
    mc_by_n = {}
    for p in range(2, sec2):
        b, c = _boxes(a.paperId, p, MC_PROMPT, "questions", cache)
        cost += c
        items = [{"n": int(it["number"]), "vy0": it["bbox"][1], "vy1": it["bbox"][3],
                  "anchor": it.get("anchor")}
                 for it in b if str(it.get("number", "")).strip().isdigit()
                 and 1 <= int(it["number"]) <= 10]
        wsp, hp = whitespace_rows(a.paperId, p, [it["bbox"] for it in b if it.get("bbox")])
        for it, bbox in tile_page(items, lines_for(p), wsp, hp, content_blocks(a.paperId, p), a.paperId, p):
            n = it["n"]
            if n not in mc_by_n:                        # first occurrence wins
                mc_by_n[n] = {"id": f"q{n}", "number": str(n), "part": None, "section": "I",
                              "marks": 1, "marksPrinted": False, "type": "mc",
                              "ruleId": "vision-qwen3vl", "confidence": 0.9,
                              "ruleException": None, "writingSpace": [], "note": "",
                              "regions": [{"page": p, "bbox": bbox}]}
    mc = [mc_by_n[n] for n in sorted(mc_by_n)]

    # page -> candidate question numbers (a page can hold the end of one Q and start of next)
    page_q = {}
    for u in split.get("units", []):
        if _is_ii(u.get("section")):
            for r in u.get("regions", []):
                page_q.setdefault(r["page"], [])
                if u["number"] not in page_q[r["page"]]:
                    page_q[r["page"]].append(u["number"])
    last = (sol - 1) if sol else (max(page_q) if page_q else sec2)

    # ── Section II: one unit per top-level part (tiled per page, shared boundaries) ──
    # Qwen IDENTIFIES the parts + rough start; tile_page snaps to OCR lines and tiles so the
    # boxes are exact, complete and can't overlap.
    part_units = {}
    for p in range(sec2, last + 1):
        qs = page_q.get(p)
        if not qs:
            continue
        prompt = SEC2_PROMPT.replace("{qs}", ", ".join(str(x) for x in sorted(qs, key=int)))
        parts, c = _boxes(a.paperId, p, prompt, "parts", cache)
        cost += c
        items = []
        for it in parts:
            q = str(it.get("question", qs[0]))
            letter = str(it.get("part", "")).strip().lower().strip("().")[:3]
            if letter:
                items.append({"q": q, "letter": letter, "vy0": it["bbox"][1],
                              "vy1": it["bbox"][3], "anchor": it.get("anchor")})
        wsp, hp = whitespace_rows(a.paperId, p, [it["bbox"] for it in parts if it.get("bbox")])
        for it, bbox in tile_page(items, lines_for(p), wsp, hp, content_blocks(a.paperId, p), a.paperId, p):
            key = (it["q"], it["letter"])
            reg = {"page": p, "bbox": bbox}
            mk = margin_marks(ocr, p, bbox[1], bbox[3])   # per-part marks from right margin
            if key in part_units:
                part_units[key]["regions"].append(reg)
                if mk is not None:
                    part_units[key]["marks"] = (part_units[key]["marks"] or 0) + mk
            else:
                part_units[key] = {"id": f'q{it["q"]}{it["letter"]}', "number": it["q"],
                                   "part": it["letter"], "section": "II", "marks": mk,
                                   "marksPrinted": mk is not None, "type": None,
                                   "ruleId": "vision-qwen3vl", "confidence": 0.9,
                                   "ruleException": None, "writingSpace": [], "note": "",
                                   "_order": (int(it["q"]) if it["q"].isdigit() else 99, it["letter"]),
                                   "regions": [reg]}

    def s2key(u):
        return u["_order"]
    s2 = sorted(part_units.values(), key=s2key)
    for u in s2:
        u.pop("_order", None)

    cache_path.write_text(json.dumps(cache))              # persist model responses for reuse
    print(f"  MC {len(mc)}/10  ·  Section II {len(s2)} part-units "
          f"({', '.join(u['id'] for u in s2)})  ·  ${cost:.4f}")
    if a.dry:
        return
    split["units"] = mc + s2
    split.setdefault("_vision", {}).update({"mc": "qwen3vl", "sec2": "qwen3vl-parts"})
    (wd / "split.json").write_text(json.dumps(split, indent=2))
    print(f"  merged -> split.json ({len(mc)} MC + {len(s2)} Section II part-units)")


if __name__ == "__main__":
    main()
