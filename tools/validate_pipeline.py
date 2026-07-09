#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Validate pipeline JSON artifacts against the contract in tools/schemas/.

Checks two layers:
  1. Shape — each artifact against its JSON Schema (draft 2020-12).
  2. Cross-file rules a schema can't express:
       - every syllabusRefs code exists in the subject's syllabus.json outcome list
       - every type exists in the subject's types taxonomy
       - every assetKey/answerKey in questions.json has a baked PDF on disk
       - tags.json keys refer to real assetKeys
       - no duplicate (paperId, assetKey) within a paper

Used as the gate between pipeline stages (the parse-papers skill refuses to advance a
paper whose artifacts fail) and by build_manifest.py before merging.

    python3 tools/validate_pipeline.py "<paperId>" [<paperId> ...]
    python3 tools/validate_pipeline.py --subject <slug>
    python3 tools/validate_pipeline.py --all
    python3 tools/validate_pipeline.py --manifest content/<subject>/questions.json

Exits non-zero if anything fails; prints a per-file error report. Unknown fields are
allowed everywhere (the contract is additive), but known fields must have the right
shape. Vocabulary checks (outcomes/types) only run when the subject has a syllabus.json
and only against fields that are set — legacy null/free-text records pass.
"""
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _subjects import load_syllabus, outcome_codes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
SCHEMAS = Path(__file__).resolve().parent / "schemas"

_validators = {}


def validator(name):
    if name not in _validators:
        schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text())
        _validators[name] = Draft202012Validator(schema)
    return _validators[name]


def schema_errors(name, data, label):
    errs = []
    for e in validator(name).iter_errors(data):
        path = "/".join(str(p) for p in e.absolute_path) or "(root)"
        errs.append(f"{label}: {path}: {e.message[:200]}")
    return errs


def load_json(path, name, errors):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except Exception as ex:
        errors.append(f"{path.name}: unreadable JSON ({ex})")
        return None


def check_paper(paper_dir, warnings=None):
    """Validate one _work/<paperId> dir. Returns list of error strings.

    File-existence problems (crop referenced but not on disk) go into `warnings`
    when a list is passed — legacy papers legitimately have cleaned baked/ dirs.
    The skill's per-paper gate passes warnings=None so they stay hard errors there.
    """
    errors = []
    files = errors if warnings is None else warnings
    pid = paper_dir.name

    boundaries = load_json(paper_dir / "boundaries.json", "boundaries", errors)
    if boundaries is not None:
        errors += schema_errors("boundaries", boundaries, "boundaries.json")

    questions = load_json(paper_dir / "questions.json", "questions", errors)
    tags = load_json(paper_dir / "tags.json", "tags", errors)
    if tags is not None:
        errors += schema_errors("tags", tags, "tags.json")

    if questions is None:
        return errors
    errors += schema_errors("questions", questions, "questions.json")

    subject = questions.get("subject")
    syl = load_syllabus(subject) if subject else None
    codes = set(outcome_codes(syl))
    types = set(syl.get("types", [])) if syl else set()

    baked = {p.name for p in (paper_dir / "baked").glob("*.pdf")}
    # crops may have been cleaned from baked/ after upload; the R2 mirror is the
    # other place a crop legitimately lives.
    mirror = WORK / "_bucket_mirror" / questions.get("subject", "") / "papers" / questions.get("paperSlug", "")
    mirrored = {p.name for p in mirror.glob("*.pdf")} if mirror.is_dir() else set()
    on_disk = baked | mirrored
    seen = set()
    for i, r in enumerate(questions.get("questions", [])):
        who = f"questions.json[{i}] ({r.get('assetKey')})"
        key = (r.get("paperId"), r.get("assetKey"))
        if key in seen:
            errors.append(f"{who}: duplicate (paperId, assetKey)")
        seen.add(key)
        if on_disk:
            if r.get("assetKey") and r["assetKey"] not in on_disk:
                files.append(f"{who}: assetKey has no baked or mirrored file")
            if r.get("answerKey") and r["answerKey"] not in on_disk:
                files.append(f"{who}: answerKey has no baked or mirrored file")
        if syl:
            for c in r.get("syllabusRefs") or []:
                if c not in codes:
                    errors.append(f"{who}: syllabusRefs code {c!r} not in {subject} syllabus.json")
            if r.get("type") and types and r["type"] not in types:
                errors.append(f"{who}: type {r['type']!r} not in {subject} types taxonomy")

    if tags is not None:
        asset_keys = {r.get("assetKey") for r in questions.get("questions", [])}
        for k, t in tags.get("tags", {}).items():
            if k not in asset_keys:
                errors.append(f"tags.json: {k}: no matching record in questions.json")
            if syl:
                for c in t.get("syllabusRefs") or []:
                    if c not in codes:
                        errors.append(f"tags.json: {k}: syllabusRefs code {c!r} not in syllabus.json")
                if t.get("type") and types and t["type"] not in types:
                    errors.append(f"tags.json: {k}: type {t['type']!r} not in types taxonomy")
        if tags.get("paperId") not in (pid, questions.get("questions", [{}])[0].get("paperId") if questions.get("questions") else pid):
            errors.append(f"tags.json: paperId {tags.get('paperId')!r} does not match dir {pid!r}")
    return errors


def check_manifest(path):
    errors = []
    data = load_json(Path(path), "manifest", errors)
    if data is None:
        return errors or [f"{path}: missing"]
    errors += schema_errors("manifest", data, Path(path).name)
    if data.get("count") != len(data.get("questions", [])):
        errors.append(f"{Path(path).name}: count {data.get('count')} != len(questions) {len(data.get('questions', []))}")
    syl = load_syllabus(data.get("subject", ""))
    if syl:
        codes, types = set(outcome_codes(syl)), set(syl.get("types", []))
        for i, r in enumerate(data.get("questions", [])):
            for c in r.get("syllabusRefs") or []:
                if c not in codes:
                    errors.append(f"[{i}] {r.get('assetKey')}: syllabusRefs {c!r} not in syllabus.json")
            if r.get("type") and types and r["type"] not in types:
                errors.append(f"[{i}] {r.get('assetKey')}: type {r['type']!r} not in types taxonomy")
    return errors


def check_corrections(path):
    errors = []
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except Exception:
            errors.append(f"{Path(path).name}:{n}: unparseable line")
            continue
        errors += schema_errors("corrections", rec, f"{Path(path).name}:{n}")
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paperIds", nargs="*")
    ap.add_argument("--all", action="store_true", help="validate every _work paper dir")
    ap.add_argument("--subject", help="validate every _work paper of one subject")
    ap.add_argument("--manifest", help="validate a shipped content/<subject>/questions.json")
    ap.add_argument("--corrections", action="store_true", help="also validate _corrections.jsonl")
    ap.add_argument("--strict", action="store_true",
                    help="treat missing crop files as errors (use for freshly baked papers)")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print failures + summary")
    args = ap.parse_args()

    targets = []
    if args.all or args.subject:
        for d in sorted(WORK.iterdir()):
            if not d.is_dir() or d.name.startswith("_"):
                continue
            if not (d / "boundaries.json").exists() and not (d / "questions.json").exists():
                continue
            if args.subject:
                qj = d / "questions.json"
                try:
                    if json.loads(qj.read_text()).get("subject") != args.subject:
                        continue
                except Exception:
                    continue
            targets.append(d)
    for pid in args.paperIds:
        d = WORK / pid
        if not d.is_dir():
            print(f"FAIL {pid}: no such _work dir", file=sys.stderr)
            sys.exit(2)
        targets.append(d)

    failed = warned = 0
    for d in targets:
        warns = None if args.strict else []
        errs = check_paper(d, warnings=warns)
        if errs:
            failed += 1
            print(f"FAIL {d.name}")
            for e in errs[:20]:
                print(f"    {e}")
            if len(errs) > 20:
                print(f"    ... {len(errs) - 20} more")
        elif not args.quiet:
            print(f"ok   {d.name}")
        if warns:
            warned += 1
            print(f"warn {d.name}: {len(warns)} crop file(s) referenced but not on disk")

    if args.manifest:
        errs = check_manifest(args.manifest)
        if errs:
            failed += 1
            print(f"FAIL {args.manifest}")
            for e in errs[:40]:
                print(f"    {e}")
        elif not args.quiet:
            print(f"ok   {args.manifest}")

    if args.corrections:
        cpath = WORK / "_corrections.jsonl"
        if cpath.exists():
            errs = check_corrections(cpath)
            if errs:
                failed += 1
                print(f"FAIL {cpath.name}")
                for e in errs[:40]:
                    print(f"    {e}")
            elif not args.quiet:
                print(f"ok   {cpath.name}")

    total = len(targets) + (1 if args.manifest else 0)
    print(f"validated {total} target(s): {failed} failed, {warned} with file warnings")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
