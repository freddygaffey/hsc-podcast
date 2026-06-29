#!/usr/bin/env python3
"""Upload subject audio to the unified R2 bucket via wrangler.

Objects are keyed <subject>/<episode>/<voice>.m4a — exactly what the unified manifest points
at (audioBaseUrl/<subject>/<episode>/<voice>.m4a). Uses your `wrangler login`; no S3 keys.

Two source layouts are scanned (deduped, unified wins):
  • Unified  content/<subject>/<episode>/*.m4a       — the ongoing pipeline (where the voice
    daemon renders new episodes)
  • Legacy   <legacy-app>/content/<episode>/*.m4a    — the one-time migration source

Modes:
  python3 tools/upload_audio.py            # one-shot: upload new/changed, then exit
  python3 tools/upload_audio.py --watch    # DAEMON: upload audio as it's rendered, and
                                           #   refresh manifest.json once uploads go quiet

Flags:
  --force        re-upload everything, ignoring the upload cache
  --no-manifest  (watch) don't regenerate the manifest after uploads settle
  --deploy       (watch) also run ./deploy.sh after uploads settle

Env: R2_BUCKET (default hsc-podcast-audio), UPLOAD_JOBS (8), POLL (5s), QUIET (20s).
Resumable: tools/.upload-state.json records (mtime,size) per key, so re-runs skip done files.
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
POLL = int(os.environ.get("POLL", "5"))     # seconds between scans in --watch
QUIET = int(os.environ.get("QUIET", "20"))  # idle seconds before manifest/deploy in --watch

# Legacy migration source dirs -> subject folder in the bucket.
LEGACY_SUBJECTS = [("hsc-phy-podcast", "physics"), ("hsc-sdd-podcast", "software")]

_state_lock = threading.Lock()


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state))


def all_audio() -> list[tuple[Path, str]]:
    """(local path, dest key) for every .m4a, from the unified layout then the legacy dirs.
    Keys are <subject>/<episode>/<voice>.m4a; a key from the unified tree wins over legacy."""
    out, seen = [], set()
    content = ROOT / "content"
    if content.is_dir():
        for subj in sorted(content.iterdir()):
            if not subj.is_dir() or subj.name.startswith("_"):
                continue
            for path in sorted(subj.glob("*/*.m4a")):
                key = f"{subj.name}/{path.relative_to(subj)}"
                if key not in seen:
                    seen.add(key); out.append((path, key))
    for app, subject in LEGACY_SUBJECTS:
        c = ROOT / app / "content"
        if not c.is_dir():
            continue
        for path in sorted(c.glob("*/*.m4a")):
            key = f"{subject}/{path.relative_to(c)}"
            if key not in seen:
                seen.add(key); out.append((path, key))
    return out


def upload_one(path: Path, key: str) -> None:
    subprocess.run(
        WRANGLER + ["r2", "object", "put", f"{BUCKET}/{key}",
                    "--file", str(path), "--remote", "--content-type", "audio/mp4"],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def upload_changed(state: dict, force: bool = False, quiet: bool = False) -> int:
    """Upload every new/changed .m4a (concurrently). Returns the count uploaded."""
    files = all_audio()
    todo = []
    for path, key in files:
        st = path.stat()
        sig = [int(st.st_mtime), st.st_size]
        if not force and state.get(key) == sig:
            continue
        todo.append((path, key, sig))
    if not todo:
        return 0
    if not quiet:
        print(f"Bucket '{BUCKET}': {len(files)} files, {len(files) - len(todo)} already up, "
              f"{len(todo)} to upload ({JOBS} at a time).")
    done, failed, t0 = 0, [], time.time()

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
                continue
            with _state_lock:
                state[key] = sig
                save_state(state)
            done += 1
            if not quiet and (done % 25 == 0 or done == len(todo)):
                rate = done / max(1e-6, time.time() - t0)
                eta = (len(todo) - done) / max(1e-6, rate)
                print(f"  {done}/{len(todo)} uploaded  ({rate:.1f}/s, ETA {eta/60:.0f} min)")
    if failed and not quiet:
        print(f"  {len(failed)} failed (re-run to retry).", file=sys.stderr)
    return done


def refresh_manifest() -> None:
    print("  → refreshing manifest.json")
    subprocess.run(["python3", "tools/generate_manifest.py"], cwd=ROOT, check=False)


def run_deploy() -> None:
    print("  → deploying (./deploy.sh)")
    subprocess.run(["bash", "deploy.sh"], cwd=ROOT, env=dict(os.environ), check=False)


def main() -> None:
    ap = argparse.ArgumentParser(description="Upload subject audio to the unified R2 bucket.")
    ap.add_argument("--watch", action="store_true", help="run as a daemon")
    ap.add_argument("--force", action="store_true", help="re-upload everything")
    ap.add_argument("--no-manifest", action="store_true", help="(watch) skip manifest refresh")
    ap.add_argument("--deploy", action="store_true", help="(watch) run ./deploy.sh after uploads settle")
    args = ap.parse_args()
    state = load_state()

    if not args.watch:
        n = upload_changed(state, force=args.force)
        print(f"Uploaded {n} file(s) to '{BUCKET}'." if n else "Nothing to upload — all in sync.")
        return

    print(f"Upload daemon watching content/ → R2 '{BUCKET}' (poll {POLL}s) — Ctrl-C to stop.")
    n = upload_changed(state, force=args.force)
    if n:
        print(f"[init] uploaded {n} file(s)")
    dirty, last = n > 0, time.time()
    try:
        while True:
            time.sleep(POLL)
            n = upload_changed(state, quiet=True)
            if n:
                dirty, last = True, time.time()
                print(f"[{time.strftime('%H:%M:%S')}] uploaded {n} new file(s)")
            elif dirty and (time.time() - last) >= QUIET:
                if not args.no_manifest:
                    refresh_manifest()
                if args.deploy:
                    run_deploy()
                dirty = False
                print("[idle] in sync — waiting for more audio.")
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
