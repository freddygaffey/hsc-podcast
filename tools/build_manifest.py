#!/usr/bin/env python3
"""Aggregate per-paper question records into the committed per-subject manifest.

Each baked paper writes papers/_work/<paperId>/questions.json (records with id, assetKey,
module, topic, syllabusRefs, marks, …). This merges them all, deduping by content-hash id
(recycled questions across papers collapse to one), into:

    content/<subject>/questions.json   →  { subject, count, questions: [...] }

which is what the app loads. Run after a bake pass.

Per-record merge order (all keyed by (paperId, assetKey)):
    1. base record from _work/<paperId>/questions.json
    2. _work/<paperId>/tags.json — AI classification fills NULL/empty fields only
       (never overrides locate-time or earlier agent-pass values)
    3. _work/_corrections.jsonl — human corrections always win
    4. --exclude-bad drops records whose _review.jsonl verdict is bad

Inputs failing the tools/schemas/ contract are skipped and reported; the output manifest
is validated before writing.

Bucket layout is readable per-paper folders under a papers/ prefix (revised D1, see
docs/past-paper-generator.md): <subject>/papers/<paperSlug>/{paper.pdf,q*.pdf,a*.pdf}.
The client builds URLs as <assetBaseUrl>/<subject>/papers/<paperSlug>/<assetKey>.

    python3 tools/build_manifest.py [--exclude-bad]     # all subjects found in _work
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _subjects import code_maps, load_syllabus  # noqa: E402
from validate_pipeline import check_manifest, schema_errors  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
CONTENT = ROOT / "content"

TAG_FIELDS = ("type", "topic", "module", "syllabusRefs")
BAD_VERDICTS = {"cut-off", "wrong-split", "other-bad", "not-right"}


def load_corrections():
    """(paperId, assetKey) -> {field: value}, latest line per field wins."""
    out = defaultdict(dict)
    cpath = WORK / "_corrections.jsonl"
    if cpath.exists():
        for line in cpath.read_text().splitlines():
            try:
                c = json.loads(line)
                out[(c["paperId"], c["assetKey"])][c["field"]] = c["value"]
            except Exception:
                continue
    return out


def load_verdicts():
    """(paperId, assetKey) -> latest verdict."""
    out = {}
    rpath = WORK / "_review.jsonl"
    if rpath.exists():
        for line in rpath.read_text().splitlines():
            try:
                v = json.loads(line)
                out[(v["paperId"], v["assetKey"])] = v["verdict"]
            except Exception:
                continue
    return out


def main():
    exclude_bad = "--exclude-bad" in sys.argv[1:]
    corrections = load_corrections()
    verdicts = load_verdicts() if exclude_bad else {}

    by_subject = defaultdict(dict)      # subject -> { id: record }
    papers = skipped = tagged = corrected = dropped = 0
    normalised = [0, 0]                 # [topics, modules] remapped to closed vocab
    archived = 0                        # old-syllabus papers kept as archives only
    _maps = {}
    for qj in WORK.glob("*/questions.json"):
        try:
            data = json.loads(qj.read_text())
        except Exception:
            continue
        errs = schema_errors("questions", data, qj.parent.name)
        if errs:
            skipped += 1
            print(f"  SKIP {qj.parent.name}: fails contract ({errs[0]}"
                  f"{' …' if len(errs) > 1 else ''})")
            continue
        # AI tag sidecar — fills gaps only
        tags = {}
        tpath = qj.parent / "tags.json"
        if tpath.exists():
            try:
                tdata = json.loads(tpath.read_text())
                if not schema_errors("tags", tdata, qj.parent.name):
                    tags = tdata.get("tags", {})
            except Exception:
                pass
        subj = data.get("subject") or "misc"
        if subj not in _maps:
            syl = load_syllabus(subj)
            _maps[subj] = (code_maps(syl), set((syl or {}).get("topics", [])),
                           set(m for m in (syl or {}).get("modules", []) if isinstance(m, str)),
                           (syl or {}).get("minYear"))
        (code_topic, code_module), topic_set, module_set, min_year = _maps[subj]
        # old-syllabus papers stay available as full-paper ARCHIVES in the bucket, but
        # their questions don't enter the segregated question bank
        if min_year:
            slug_year = (data.get("paperSlug") or "").split("-")[0]
            if slug_year.isdigit() and int(slug_year) < min_year:
                archived += 1
                continue
        for r in data.get("questions", []):
            qid = r.get("id")
            if not qid:
                continue
            key = (r.get("paperId"), r.get("assetKey"))
            if exclude_bad and verdicts.get(key) in BAD_VERDICTS:
                dropped += 1
                continue
            t = tags.get(r.get("assetKey")) or {}
            for f in TAG_FIELDS:
                if t.get(f) and not r.get(f):
                    r[f] = t[f]
                    tagged += 1
            # normalise topic/module to the subject's CLOSED vocabulary via the primary
            # syllabus code — collapses legacy free-text topics into ~14 categories.
            refs = r.get("syllabusRefs") or []
            if refs:
                if code_topic.get(refs[0]) and r.get("topic") not in topic_set:
                    r["topic"] = code_topic[refs[0]]
                    normalised[0] += 1
                if code_module.get(refs[0]) and r.get("module") not in module_set:
                    r["module"] = code_module[refs[0]]
                    normalised[1] += 1
            c = corrections.get(key, {})
            for f, val in c.items():
                if f != "tagFlag":
                    r[f] = val
                    corrected += 1
            prev = by_subject[subj].get(qid)
            # recycled question seen again: prefer the copy that has a baked answer
            if prev is None or (not prev.get("answerKey") and r.get("answerKey")):
                by_subject[subj][qid] = r
        papers += 1

    # only the fields the generator UI needs at runtime — keeps the manifest small.
    KEEP = ("paperSlug", "paperId", "assetKey", "answerKey", "questionNumber", "partLabel",
            "year", "page", "marks", "lineCount", "spaceHeight", "type", "topic", "module",
            "syllabusRefs", "unit", "parts")

    for subj, recs in sorted(by_subject.items()):
        out_dir = CONTENT / subj
        out_dir.mkdir(parents=True, exist_ok=True)
        records = [{k: r[k] for k in KEEP if k in r} for r in recs.values()]
        manifest = {"subject": subj, "count": len(records), "questions": records}
        errs = schema_errors("manifest", manifest, subj)
        if errs:
            print(f"  FAIL {subj}: output manifest fails contract, NOT written")
            for e in errs[:5]:
                print(f"    {e}")
            continue
        (out_dir / "questions.json").write_text(json.dumps(manifest, indent=2))
        withmod = sum(1 for r in records if r.get("module"))
        withans = sum(1 for r in records if r.get("answerKey"))
        withlines = sum(1 for r in records if r.get("lineCount"))
        print(f"  {subj}: {len(records)} questions  (module {withmod}, answers {withans}, "
              f"lines {withlines}) -> content/{subj}/questions.json")
    print(f"aggregated {papers} papers across {len(by_subject)} subjects"
          f" ({skipped} skipped, {tagged} fields AI-tagged, "
          f"{normalised[0]}+{normalised[1]} topics/modules normalised, {corrected} corrected, "
          f"{archived} old-syllabus papers archived (questions excluded)"
          + (f", {dropped} bad crops dropped" if exclude_bad else "") + ")")

    # cross-check written manifests against subject vocab (outcome codes, types)
    for subj in by_subject:
        mpath = CONTENT / subj / "questions.json"
        if mpath.exists():
            errs = check_manifest(mpath)
            if errs:
                print(f"  WARN {subj}: {len(errs)} manifest vocabulary issue(s), e.g. {errs[0]}")


if __name__ == "__main__":
    main()
