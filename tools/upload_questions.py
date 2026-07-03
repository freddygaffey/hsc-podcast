#!/usr/bin/env python3
"""Upload baked papers to R2, one folder per paper under a papers/ prefix:

    <subject>/papers/<paperSlug>/q01a.pdf    question crop
    <subject>/papers/<paperSlug>/a01a.pdf    its answer crop
    <subject>/papers/<paperSlug>/paper.pdf   full original exam (kept deliberately —
                                             revised D1, docs/past-paper-generator.md)

Stages files as hardlinks then pushes with one parallel `rclone copy` (the r2: remote
needs an R2 API token with object read/write). Idempotent (re-uploads overwrite).

    python3 tools/upload_questions.py [bucket] [--subject maths-advanced] [--limit N]
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
PAPERS = ROOT / "papers"
CONTENT = ROOT / "content"

import argparse
_p = argparse.ArgumentParser()
# hsc-podcast-audio backs audio.hsc.pebnum.com — the one shared public bucket.
_p.add_argument("bucket", nargs="?", default="hsc-podcast-audio")
_p.add_argument("--subject", default=None)
_p.add_argument("--limit", type=int, default=None)
_a = _p.parse_args()
bucket, subj_filter, limit = _a.bucket, _a.subject, _a.limit


def main():
    # Gather (key, localpath) upload jobs from every per-paper work manifest.
    jobs = {}   # key -> path (dedupe identical keys)
    # Full source papers come from papers/_index.json (paperId -> source path).
    src_index = {p["paperId"]: p["path"]
                 for p in json.loads((PAPERS / "_index.json").read_text())["papers"]}

    for qj in sorted(WORK.glob("*/questions.json")):
        pid = qj.parent.name
        data = json.loads(qj.read_text())
        subj = data.get("subject") or "misc"
        if not subj.startswith(("maths-", "physics")):
            continue
        if subj_filter and subj != subj_filter:
            continue
        ps = data.get("paperSlug")
        baked = qj.parent / "baked"
        sp = src_index.get(pid)
        if sp and (PAPERS / sp).exists():
            jobs[f"{subj}/papers/{ps}/paper.pdf"] = PAPERS / sp
        for r in data["questions"]:
            for key in (r.get("assetKey"), r.get("answerKey")):
                if key and (baked / key).exists():
                    jobs[f"{subj}/papers/{ps}/{key}"] = baked / key

    items = list(jobs.items())
    if limit:
        items = items[:limit]

    # Stage via hardlinks (instant, no disk copy), then one parallel rclone copy —
    # 14k tiny files in one process, not 14k wrangler spawns.
    import os, shutil
    stage = WORK / "_stage"
    if stage.exists():
        shutil.rmtree(stage)
    for key, path in items:
        tgt = stage / key
        tgt.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(path, tgt)
        except OSError:
            shutil.copy(path, tgt)
    print(f"staged {len(items)} files -> rclone copy to r2:{bucket}/ …")
    subprocess.run(["rclone", "copy", str(stage), f"r2:{bucket}/",
                    "--transfers", "64", "--checkers", "64",
                    "--s3-no-check-bucket", "--stats", "20s"], check=True)
    shutil.rmtree(stage)
    print("done.")


if __name__ == "__main__":
    main()
