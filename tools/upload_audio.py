#!/usr/bin/env python3
"""Upload every subject's episode audio to the unified R2 bucket via wrangler.

Source = the legacy app content dirs (which hold the actual .m4a); dest = ONE bucket with a
folder per subject, keyed <subject>/<episode>/<voice>.m4a — exactly what the unified manifest
points at (audioBaseUrl/<subject>/<episode>/<voice>.m4a). Uses your `wrangler login`; no
rclone, no S3 keys.

  python3 tools/upload_audio.py            # upload new/changed, then exit
  python3 tools/upload_audio.py --force    # re-upload everything, ignore the cache

Env: R2_BUCKET (default hsc-podcast-audio), UPLOAD_JOBS (default 8 concurrent uploads).
Resumable: an .upload-state.json ledger records (mtime,size) per key, so re-runs skip
already-uploaded files and an interrupted run picks up where it left off.
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "tools" / ".upload-state.json"
WRANGLER = ["wrangler"]  # system wrangler on PATH
BUCKET = os.environ.get("R2_BUCKET", "hsc-podcast-audio")
JOBS = int(os.environ.get("UPLOAD_JOBS", "8"))

# (legacy app dir under the unified repo) -> subject folder in the bucket
SUBJECTS = [("hsc-phy-podcast", "physics"), ("hsc-sdd-podcast", "software")]

_state_lock = threading.Lock()


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state))


def all_audio() -> list[tuple[Path, str]]:
    """(local path, dest key) for every .m4a across all subjects."""
    out = []
    for app, subject in SUBJECTS:
        content = ROOT / app / "content"
        for path in sorted(content.glob("*/*.m4a")):
            out.append((path, f"{subject}/{path.relative_to(content)}"))
    return out


def upload_one(path: Path, key: str) -> None:
    subprocess.run(
        WRANGLER + ["r2", "object", "put", f"{BUCKET}/{key}",
                    "--file", str(path), "--remote", "--content-type", "audio/mp4"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Upload subject audio to the unified R2 bucket.")
    ap.add_argument("--force", action="store_true", help="re-upload everything")
    args = ap.parse_args()

    state = load_state()
    files = all_audio()
    todo = []
    for path, key in files:
        st = path.stat()
        sig = [int(st.st_mtime), st.st_size]
        if not args.force and state.get(key) == sig:
            continue
        todo.append((path, key, sig))

    total = len(files)
    skipped = total - len(todo)
    print(f"Bucket '{BUCKET}': {total} audio files, {skipped} already uploaded, "
          f"{len(todo)} to upload ({JOBS} at a time).")
    if not todo:
        print("Nothing to do — all in sync.")
        return

    done = 0
    failed = []
    t0 = time.time()

    def work(item):
        path, key, sig = item
        upload_one(path, key)
        return key, sig

    with ThreadPoolExecutor(max_workers=max(1, JOBS)) as ex:
        futures = {ex.submit(work, it): it for it in todo}
        for fut in as_completed(futures):
            path, key, sig = futures[fut]
            try:
                fut.result()
            except subprocess.CalledProcessError:
                failed.append(key)
                print(f"  ! failed: {key}", file=sys.stderr)
                continue
            with _state_lock:
                state[key] = sig
                save_state(state)
            done += 1
            if done % 25 == 0 or done == len(todo):
                rate = done / max(1e-6, time.time() - t0)
                eta = (len(todo) - done) / max(1e-6, rate)
                print(f"  {done}/{len(todo)} uploaded  ({rate:.1f}/s, ETA {eta/60:.0f} min)")

    print(f"Done: {done} uploaded, {skipped} skipped, {len(failed)} failed.")
    if failed:
        print("Failed keys (re-run to retry):", file=sys.stderr)
        for k in failed[:20]:
            print(f"  {k}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
