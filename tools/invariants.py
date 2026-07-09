#!/usr/bin/env python3
"""Deterministic invariants over a paper's split/boundaries — ZERO tokens.

These are the cheapest, strongest correctness gates in the Gen-3 pipeline (see
docs/parser-pipeline-plan.md, verification layer L0). They catch split errors that a
vision QA pass would miss, for free, every run:

  - dup            two units share the same (number, part)               [error]
  - marks-conserve section unit-marks != printed section total           [error]
  - numbering-gap  a question number is missing inside a section's range [warn]
  - count-min      fewer top-level questions than the section expects     [error]

Reads papers/_work/<paperId>/split.json when present (Gen-3), else falls back to the
current boundaries.json. Marks conservation only fires when every unit in a section has
a known mark; otherwise it reports coverage as info (never a false failure on a paper
whose marks aren't extracted yet).

    python3 tools/invariants.py "<paperId>" [<paperId> ...]
    python3 tools/invariants.py --all
Exit non-zero if any paper has an error-level violation.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _subjects import load_syllabus  # noqa: E402
from ocr_to_split import to_lines  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


class V:
    """One violation."""
    def __init__(self, level, code, msg):
        self.level, self.code, self.msg = level, code, msg

    def __str__(self):
        tag = {"error": "ERROR", "warn": "warn ", "info": "info "}[self.level]
        return f"  [{tag}] {self.code}: {self.msg}"


def load_units(pid):
    """Normalise split.json or boundaries.json to units [{number, part, marks, marksPrinted}]."""
    wd = WORK / pid
    sp = wd / "split.json"
    if sp.exists():
        d = json.loads(sp.read_text())
        units = [{"number": u.get("number"), "part": u.get("part"),
                  "marks": u.get("marks"), "marksPrinted": u.get("marksPrinted")}
                 for u in d.get("units", [])]
        return units, d.get("subject"), "split.json"
    bp = wd / "boundaries.json"
    if bp.exists():
        d = json.loads(bp.read_text())
        # question-level marks only — parts sum to the question, don't double count
        units = [{"number": q.get("number"), "part": None,
                  "marks": q.get("marks"), "marksPrinted": q.get("marksPrinted")}
                 for q in d.get("questions", [])]
        return units, d.get("subject"), "boundaries.json"
    return None, None, None


def parse_range(spec):
    """'1-10' -> (1, 10); '11-' -> (11, None); '5' -> (5, 5)."""
    m = re.match(r"^\s*(\d+)\s*-\s*(\d*)\s*$", str(spec))
    if m:
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else None
        return lo, hi
    if str(spec).strip().isdigit():
        n = int(spec)
        return n, n
    return None, None


def section_of(num, sections):
    for s in sections:
        lo, hi = parse_range(s.get("questions"))
        if lo is None:
            continue
        if num >= lo and (hi is None or num <= hi):
            return s
    return None


def numkey(n):
    try:
        return int(re.match(r"\d+", str(n)).group())
    except (TypeError, AttributeError):
        return None


def geometry(pid):
    """Box-geometry rules (need split.json regions + ocr.json): boxes must not overlap and no
    box edge may cross a line of text. Modular — independent of syllabus config."""
    wd = WORK / pid
    sp = wd / "split.json"
    if not sp.exists():
        return []
    d = json.loads(sp.read_text())
    units = d.get("units", [])
    op = wd / "ocr.json"
    ocr = json.loads(op.read_text()) if op.exists() else []
    out, bypage = [], {}
    for u in units:
        for r in u.get("regions", []):
            bypage.setdefault(r["page"], []).append((r["bbox"], u.get("id")))
    for p, boxes in bypage.items():                       # rule: no-overlap
        boxes.sort(key=lambda b: b[0][1])
        for (b1, i1), (b2, i2) in zip(boxes, boxes[1:]):
            if b2[1] < b1[3] - 0.006:
                out.append(V("error", "overlap", f"{i1} & {i2} overlap on p{p}"))
    for u in units:                                       # rule: no-line-cross
        for r in u.get("regions", []):
            lines = to_lines(ocr[r["page"] - 1]) if 0 <= r["page"] - 1 < len(ocr) else []
            for edge in (r["bbox"][1], r["bbox"][3]):
                if any((ln["x1"] - ln["x0"]) > 0.30 and ln["y0"] + 0.004 < edge < ln["y1"] - 0.004
                       for ln in lines):
                    out.append(V("error", "line-cross", f'{u.get("id")} crosses text on p{r["page"]}'))
                    break
    return out


def check(pid):
    units, subject, src = load_units(pid)
    out = []
    if units is None:
        return [V("error", "no-input", "no split.json or boundaries.json on disk")], src
    if not units:
        return [V("error", "empty", f"{src} has zero units")], src
    out += geometry(pid)                                  # box-geometry rules (split.json only)

    # 1. duplicate (number, part)
    seen = {}
    for u in units:
        k = (str(u["number"]), u["part"])
        seen[k] = seen.get(k, 0) + 1
    for (num, part), c in seen.items():
        if c > 1:
            out.append(V("error", "dup", f"{c} units share number={num} part={part}"))

    syl = load_syllabus(subject) if subject else None
    sections = (syl or {}).get("sections") if isinstance(syl, dict) else None
    if not sections:
        out.append(V("info", "no-sections", f"subject '{subject}' has no syllabus sections — skipped marks/count checks"))
        return out, src

    # bucket top-level question numbers into sections
    tops = {}  # number(int) -> section name
    per_section_marks = {}   # name -> [marks or None]
    for u in units:
        n = numkey(u["number"])
        if n is None:
            continue
        sec = section_of(n, sections)
        name = sec["name"] if sec else None
        tops.setdefault(n, name)
        per_section_marks.setdefault(name, []).append(u.get("marks"))

    # 2. marks conservation per section (only when fully known)
    for s in sections:
        name = s["name"]
        total = s.get("marks")
        marks = per_section_marks.get(name, [])
        if total is None or not marks:
            continue
        if any(m is None for m in marks):
            known = sum(m for m in marks if m is not None)
            out.append(V("info", "marks-conserve",
                         f"section {name}: marks incomplete ({sum(m is not None for m in marks)}/{len(marks)} units), "
                         f"known {known} of printed {total} — cannot verify"))
        else:
            got = sum(marks)
            if got != total:
                out.append(V("error", "marks-conserve",
                             f"section {name}: unit marks sum to {got}, printed total is {total} (Δ{got - total})"))

    # 3. numbering gaps + count within closed sections
    for s in sections:
        lo, hi = parse_range(s.get("questions"))
        if lo is None:
            continue
        present = sorted(n for n, nm in tops.items() if nm == s["name"])
        if hi is not None:
            missing = [n for n in range(lo, hi + 1) if n not in present]
            if missing:
                out.append(V("warn", "numbering-gap",
                             f"section {s['name']}: missing question numbers {missing}"))
            if len(present) < (hi - lo + 1):
                out.append(V("error", "count-min",
                             f"section {s['name']}: {len(present)} questions, expected {hi - lo + 1}"))
    return out, src


def main():
    args = sys.argv[1:]
    if args == ["--all"]:
        pids = sorted(p.name for p in WORK.iterdir()
                      if p.is_dir() and ((p / "split.json").exists() or (p / "boundaries.json").exists()))
    else:
        pids = args
    if not pids:
        raise SystemExit("usage: invariants.py <paperId> ... | --all")

    failed = 0
    for pid in pids:
        vs, src = check(pid)
        errs = [v for v in vs if v.level == "error"]
        status = "FAIL" if errs else "ok"
        print(f"{status}  {pid}  ({src or 'no input'})")
        for v in vs:
            print(v)
        if errs:
            failed += 1
    print(f"\n{len(pids)} paper(s), {failed} with errors")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
