#!/usr/bin/env python3
"""Upload baked papers to R2, grouped by paper: <subject>/<paperSlug>/{paper.pdf,q*,a*}.

Uses wrangler (OAuth, account-wide) because the rclone `r2:` token is denied on this bucket.
Parallelised across files. Idempotent-ish (re-uploads overwrite).

    python3 tools/upload_questions.py [bucket] [--subject maths-advanced] [--limit N]
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"
PAPERS = ROOT / "papers"
CONTENT = ROOT / "content"

args = sys.argv[1:]
bucket = next((a for a in args if not a.startswith("--") and a != ""), "hsc-questions")
subj_filter = None
if "--subject" in args:
    subj_filter = args[args.index("--subject") + 1]
limit = None
if "--limit" in args:
    limit = int(args[args.index("--limit") + 1])


def put(key, path):
    subprocess.run(["wrangler", "r2", "object", "put", f"{bucket}/{key}",
                    "--file", str(path), "--remote"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return key


def main():
    # Gather (key, localpath) upload jobs from every subject manifest.
    jobs = {}   # key -> path (dedupe identical keys)
    subjects = [p.parent.name for p in CONTENT.glob("*/questions.json")
                if p.parent.name.startswith(("maths-", "physics"))]
    if subj_filter:
        subjects = [s for s in subjects if s == subj_filter]

    src_index = {p["paperId"]: p["path"]
                 for p in json.loads((PAPERS / "_index.json").read_text())["papers"]}

    for subj in sorted(subjects):
        recs = json.loads((CONTENT / subj / "questions.json").read_text())["questions"]
        papers_seen = set()
        for r in recs:
            ps = r.get("paperSlug"); pid = r["paperId"]
            baked = WORK / pid / "baked"
            # full paper.pdf once per paper
            if ps not in papers_seen:
                papers_seen.add(ps)
                sp = src_index.get(pid)
                if sp and (PAPERS / sp).exists():
                    jobs[f"{subj}/{ps}/paper.pdf"] = PAPERS / sp
            for key in (r.get("assetKey"), r.get("answerKey")):
                if key and (baked / key).exists():
                    jobs[f"{subj}/{ps}/{key}"] = baked / key

    items = list(jobs.items())
    if limit:
        items = items[:limit]
    print(f"uploading {len(items)} objects to r2:{bucket}/ (wrangler, 8-way) …")
    done = fail = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(put, k, p): k for k, p in items}
        for f in as_completed(futs):
            try:
                f.result(); done += 1
            except Exception:
                fail += 1
            if (done + fail) % 200 == 0:
                print(f"  {done+fail}/{len(items)} ({fail} failed)")
    print(f"done: {done} uploaded, {fail} failed")


if __name__ == "__main__":
    main()
