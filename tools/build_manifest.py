#!/usr/bin/env python3
"""Aggregate per-paper question records into the committed per-subject manifest.

Each baked paper writes papers/_work/<paperId>/questions.json (records with id, assetKey,
module, topic, syllabusRefs, marks, …). This merges them all, deduping by content-hash id
(recycled questions across papers collapse to one), into:

    content/<subject>/questions.json   →  { subject, count, questions: [...] }

which is what the app loads. Run after a bake pass.

    python3 tools/build_manifest.py            # all subjects found in _work
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
CONTENT = ROOT / "content"


def main():
    by_subject = defaultdict(dict)      # subject -> { id: record }
    papers = 0
    for qj in WORK.glob("*/questions.json"):
        try:
            data = json.loads(qj.read_text())
        except Exception:
            continue
        subj = data.get("subject") or "misc"
        for r in data.get("questions", []):
            key = f"{r.get('paperSlug')}/{r['assetKey']}"   # per-paper file (idempotent re-runs)
            by_subject[subj][key] = r
        papers += 1

    # only the fields the generator UI needs at runtime — keeps the manifest small.
    KEEP = ("paperSlug", "assetKey", "answerKey", "questionNumber", "partLabel",
            "marks", "type", "topic", "module", "syllabusRefs")

    for subj, recs in sorted(by_subject.items()):
        out_dir = CONTENT / subj
        out_dir.mkdir(parents=True, exist_ok=True)
        records = [{k: r[k] for k in KEEP if k in r} for r in recs.values()]
        (out_dir / "questions.json").write_text(json.dumps(
            {"subject": subj, "count": len(records), "questions": records}, indent=2))
        withmod = sum(1 for r in records if r.get("module"))
        withans = sum(1 for r in records if r.get("answerKey"))
        print(f"  {subj}: {len(records)} questions  (module {withmod}, answers {withans}) "
              f"-> content/{subj}/questions.json")
    print(f"aggregated {papers} papers across {len(by_subject)} subjects")


if __name__ == "__main__":
    main()
