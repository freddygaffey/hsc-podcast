#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Upgrade legacy quiz.json files to the new schema (type + source), in place.

Legacy episode quizzes were all AI-generated multiple-choice with no `type` or `source`.
This adds, non-destructively:
  - type: "mc"  (only if a question has no type)
  - source: { origin: "ai", ref: "Generated from episode script" }  (only if absent)

Past papers ("paper": true) already carry per-question `type`; for them we synthesise a
source from the paper metadata (origin hsc/trial from the title, ref "<year> ... Q<n>").

It NEVER overwrites a `type` or `source` that already exists, so it is safe to re-run and
safe over episodes that have already been hand-upgraded or regenerated.

Usage:
    python3 tools/migrate_quiz.py            # dry-run: report what would change
    python3 tools/migrate_quiz.py --write    # apply changes
    python3 tools/migrate_quiz.py --write content/dt/<EP>/quiz.json   # one file
"""
import json
import sys
from pathlib import Path


def paper_source(data, q):
    title = str(data.get("title", ""))
    origin = "trial" if "trial" in title.lower() else "hsc"
    year = q.get("year") or data.get("year")
    label = title or (f"{year} HSC" if year else "Past paper")
    qno = q.get("qNo")
    ref = f"{label} Q{qno}" if qno else label
    src = {"origin": origin, "ref": ref}
    if year:
        src["year"] = year
    return src


def migrate(path, write):
    data = json.loads(Path(path).read_text())
    qs = data.get("questions")
    if not isinstance(qs, list):
        return 0
    is_paper = bool(data.get("paper"))
    changed = 0
    for q in qs:
        # Normalise legacy cognitive-category types: a question that is really MC (has options +
        # an integer answer) but was labelled scenario/describe/compare/recall/etc. becomes
        # type "mc", with the old label preserved under "skill" so nothing is lost.
        if isinstance(q.get("options"), list) and isinstance(q.get("answer"), int) \
                and q.get("type") and q["type"] != "mc":
            q.setdefault("skill", q["type"])
            q["type"] = "mc"
            changed += 1
        if "type" not in q:
            q["type"] = "mc"
            changed += 1
        if "source" not in q or not isinstance(q.get("source"), dict):
            q["source"] = paper_source(data, q) if is_paper else {
                "origin": "ai", "ref": "Generated from episode script"
            }
            changed += 1
    if changed and write:
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return changed


def main(argv):
    args = [a for a in argv[1:] if a != "--write"]
    write = "--write" in argv
    files = [Path(a) for a in args] if args else sorted(Path("content").rglob("quiz.json"))
    total, touched = 0, 0
    for f in files:
        n = migrate(f, write)
        if n:
            touched += 1
            total += n
            print(f"{'WROTE' if write else 'would change'} {f}: +{n} field(s)")
    verb = "Applied" if write else "Dry-run:"
    print(f"\n{verb} {total} field addition(s) across {touched}/{len(files)} file(s).")
    if not write and total:
        print("Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
