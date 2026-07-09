#!/usr/bin/env python3
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
"""Resilient textbook grabber for the Year 12 Textbook Library Drive folder.

gdown --folder aborts the whole run on the first un-downloadable file (e.g. a
big popular book that hit Google Drive's per-file download quota). This lists
every file up-front, then downloads each individually: skips ones already on
disk, and CONTINUES past any blocked file (logging it) instead of aborting.
Re-run anytime — it resumes.
"""
import os, sys, time, traceback
import gdown

URL = "https://drive.google.com/drive/folders/1uvKl6Ju-8PaBPKsHaTBZgaPrZOmOfKyg"
OUT = os.path.expanduser("~/hsc-textbooks")
LOG = os.path.expanduser("~/hsc-textbooks/_grab.log")

def log(m):
    line = time.strftime("%H:%M:%S ") + m
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

# 1. enumerate the whole folder tree (no downloads)
files = gdown.download_folder(url=URL, output=OUT, skip_download=True, quiet=True)
log(f"enumerated {len(files)} files")

ok = skip = blocked = 0
blocked_ids = []
for i, f in enumerate(files, 1):
    # gdown returns objects with .id and .local_path (or .path)
    fid = getattr(f, "id", None)
    dest = getattr(f, "local_path", None) or getattr(f, "path", None)
    if dest and not os.path.isabs(dest):
        dest = os.path.join(OUT, dest)
    if not fid or not dest:
        continue
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        skip += 1
        continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        got = gdown.download(id=fid, output=dest, quiet=True, resume=True)
        if got and os.path.exists(dest) and os.path.getsize(dest) > 0:
            ok += 1
            log(f"[{i}/{len(files)}] OK {os.path.relpath(dest, OUT)} ({os.path.getsize(dest)//1024//1024} MB)")
        else:
            blocked += 1; blocked_ids.append((fid, dest))
            log(f"[{i}/{len(files)}] BLOCKED (no file) {os.path.relpath(dest, OUT)}")
    except Exception as e:
        blocked += 1; blocked_ids.append((fid, dest))
        log(f"[{i}/{len(files)}] BLOCKED {os.path.relpath(dest, OUT)}: {str(e).splitlines()[0][:80]}")
    time.sleep(0.2)

log(f"=== grab done: ok={ok} skip={skip} blocked={blocked} ===")
if blocked_ids:
    log("blocked files (Drive per-file quota or perms — retry later / browser):")
    for fid, dest in blocked_ids:
        log(f"    {os.path.relpath(dest, OUT)}   https://drive.google.com/uc?id={fid}")
