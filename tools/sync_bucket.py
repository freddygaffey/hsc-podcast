#!/usr/bin/env python3
"""Mirror the bucket from local truth: stage everything the app serves from R2, then
rclone sync (deletes anything in the bucket that isn't staged).

Staged layout (= bucket layout, one public bucket behind audio.hsc.pebnum.com):

    <subject>/<episode>/<voice>.m4a           episode audio (from content/<subject>/<ep>/)
    <subject>/papers/<paperSlug>/q01a.pdf     baked question crops (from papers/_work/)
    <subject>/papers/<paperSlug>/a01a.pdf     answer crops
    <subject>/papers/<paperSlug>/paper.pdf    full original exam (revised D1)

NEVER staged: textbook source.pdf / pages.jsonl (copyright — local only), scripts,
quizzes, images (those deploy with the Pages site, not the bucket).

Default is rclone COPY (add-only). --delete switches to rclone sync — DANGEROUS: some
live audio exists ONLY in the bucket (voices.json-listed voices with no local .m4a,
e.g. the zz_eloquence_* set), so a mirror-delete breaks the app. Only use --delete if
every manifest voice is verified present locally first.

    python3 tools/sync_bucket.py [bucket] [--dry-run] [--delete]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PAPERS = ROOT / "papers"
WORK = PAPERS / "_work"
STAGE = WORK / "_bucket_mirror"

p = argparse.ArgumentParser()
p.add_argument("bucket", nargs="?", default="hsc-podcast-audio")
p.add_argument("--dry-run", action="store_true")
p.add_argument("--delete", action="store_true",
               help="rclone sync (mirror-delete) instead of copy — see docstring warning")
p.add_argument("--papers-only", action="store_true",
               help="skip audio staging (audio is reconciled server-side; papers only exist locally)")
a = p.parse_args()


def link(src: Path, key: str):
    tgt = STAGE / key
    tgt.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, tgt)
    except OSError:
        shutil.copy(src, tgt)


def main():
    if STAGE.exists():
        print("clearing previous stage …")
        shutil.rmtree(STAGE)

    # 1. Episode audio: content/<subject>/<ep>/*.m4a (episode dirs only — skip textbook/,
    #    papers/, sources/, template folders; those hold no bucket-served audio anyway).
    n_audio = 0
    for subj_dir in sorted(CONTENT.iterdir()) if not a.papers_only else []:
        if not subj_dir.is_dir() or subj_dir.name.startswith("_"):
            continue
        subj_n = 0
        for ep_dir in sorted(subj_dir.iterdir()):
            if not ep_dir.is_dir() or ep_dir.name.startswith("_"):
                continue
            for m4a in sorted(ep_dir.glob("*.m4a")):   # includes the _title.m4a intro clip
                link(m4a, f"{subj_dir.name}/{ep_dir.name}/{m4a.name}")
                subj_n += 1
        if subj_n:
            print(f"staging audio  {subj_dir.name}: {subj_n} files")
        n_audio += subj_n

    # 2. Baked papers: every per-paper work manifest, all subjects.
    src_index = {q["paperId"]: q["path"]
                 for q in json.loads((PAPERS / "_index.json").read_text())["papers"]}
    n_paper = 0
    per_subj = {}
    for qj in sorted(WORK.glob("*/questions.json")):
        data = json.loads(qj.read_text())
        subj, ps = data.get("subject") or "misc", data.get("paperSlug")
        if not ps:   # e.g. english papers not yet slugged — nothing addressable to serve
            continue
        baked = qj.parent / "baked"
        sp = src_index.get(qj.parent.name)
        if sp and (PAPERS / sp).exists():
            link(PAPERS / sp, f"{subj}/papers/{ps}/paper.pdf")
            per_subj[subj] = per_subj.get(subj, 0) + 1
        for r in data["questions"]:
            for key in (r.get("assetKey"), r.get("answerKey")):
                if key and (baked / key).exists():
                    link(baked / key, f"{subj}/papers/{ps}/{key}")
                    per_subj[subj] = per_subj.get(subj, 0) + 1
    for subj, n in sorted(per_subj.items()):
        print(f"staging papers {subj}: {n} files")
    n_paper = sum(per_subj.values())

    size = subprocess.run(["du", "-sh", str(STAGE)], capture_output=True, text=True).stdout.split()[0]
    print(f"staged {n_audio} audio + {n_paper} paper files ({size}) -> "
          f"rclone {'sync' if a.delete else 'copy'} r2:{a.bucket}/ "
          f"{'(DRY RUN)' if a.dry_run else ''}")

    cmd = ["rclone", "sync" if a.delete else "copy", str(STAGE), f"r2:{a.bucket}/",
           "--size-only", "--transfers", "64", "--checkers", "64",
           "--s3-no-check-bucket", "-P", "--stats", "20s"]
    if a.dry_run:
        cmd.append("--dry-run")
    rc = subprocess.run(cmd).returncode
    if rc:
        sys.exit(rc)
    print("done.")


if __name__ == "__main__":
    main()
