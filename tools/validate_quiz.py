#!/usr/bin/env python3
"""Validate quiz.json files against the schema in QUIZ_STYLE_GUIDE.md.

Usage:
    python3 tools/validate_quiz.py content/physics/<EP>/quiz.json   # one file
    python3 tools/validate_quiz.py                                  # all quiz.json under content/

Exit code 0 if every file passes, 1 otherwise. Past papers ("paper": true) are checked with
the same per-question rules but skip the ~10-question count guidance.
"""
import json
import sys
from pathlib import Path

TYPES = {"mc", "recall", "worked", "short", "extended"}
ORIGINS = {"hsc", "trial", "textbook", "ai"}


def check_question(q, idx):
    errs = []
    qid = q.get("id") or f"#{idx}"
    if not q.get("id"):
        errs.append(f"{qid}: missing 'id'")
    t = q.get("type")
    if t not in TYPES:
        errs.append(f"{qid}: type must be one of {sorted(TYPES)}, got {t!r}")
    if not q.get("q"):
        errs.append(f"{qid}: missing 'q'")

    # Provenance — required on every question.
    s = q.get("source")
    if not isinstance(s, dict):
        errs.append(f"{qid}: 'source' must be an object {{origin, ref, ...}}")
    else:
        if s.get("origin") not in ORIGINS:
            errs.append(f"{qid}: source.origin must be one of {sorted(ORIGINS)}, got {s.get('origin')!r}")
        if not s.get("ref"):
            errs.append(f"{qid}: source.ref is required")

    # Type-specific requirements.
    if t == "mc":
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) != 4:
            errs.append(f"{qid}: mc needs exactly 4 'options'")
        if not isinstance(q.get("answer"), int) or not (0 <= q.get("answer", -1) <= 3):
            errs.append(f"{qid}: mc 'answer' must be an int 0-3")
    elif t == "recall":
        kp = q.get("keyPoints")
        if not isinstance(kp, list) or not kp:
            errs.append(f"{qid}: recall needs a non-empty 'keyPoints' array")
    elif t == "worked":
        wk = q.get("working")
        if not isinstance(wk, list) or not wk:
            errs.append(f"{qid}: worked needs a non-empty 'working' array")
        if "answerValue" in q and not isinstance(q["answerValue"], (int, float)):
            errs.append(f"{qid}: worked 'answerValue' must be a number when present")
    elif t in ("short", "extended"):
        if not isinstance(q.get("marks"), int) or q["marks"] < 1:
            errs.append(f"{qid}: {t} needs integer 'marks' >= 1")
        # Need something to self-mark against: a model answer or non-empty marking criteria
        # (real past papers often ship criteria from the NESA guidelines but no model answer).
        if not q.get("modelAnswer") and not q.get("criteria"):
            errs.append(f"{qid}: {t} needs a 'modelAnswer' or 'criteria'")
    return errs


def validate_file(path):
    errs = []
    try:
        data = json.loads(Path(path).read_text())
    except Exception as e:  # noqa: BLE001
        return [f"{path}: invalid JSON — {e}"]
    qs = data.get("questions")
    if not isinstance(qs, list) or not qs:
        return [f"{path}: 'questions' must be a non-empty array"]
    seen = set()
    for i, q in enumerate(qs):
        for e in check_question(q, i):
            errs.append(f"{path} :: {e}")
        qid = q.get("id")
        if qid in seen:
            errs.append(f"{path} :: duplicate id {qid!r}")
        seen.add(qid)
    return errs


def main(argv):
    targets = argv[1:]
    if targets:
        files = [Path(t) for t in targets]
    else:
        files = sorted(Path("content").rglob("quiz.json"))
    all_errs = []
    for f in files:
        all_errs.extend(validate_file(f))
    if all_errs:
        for e in all_errs:
            print("FAIL", e)
        print(f"\n{len(all_errs)} problem(s) across {len(files)} file(s).")
        return 1
    print(f"OK — {len(files)} quiz file(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
