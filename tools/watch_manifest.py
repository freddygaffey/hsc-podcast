#!/usr/bin/env python3
"""Watch content/ and rebuild the unified manifest.json whenever episodes, voices.json,
or audio change. Run while authoring / while the voice daemon renders:

    python3 tools/watch_manifest.py

Polls every 5 seconds. Exits cleanly on Ctrl-C.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_manifest import CONTENT_DIR, build_manifest, write_manifest

POLL_INTERVAL = 5  # seconds


def content_signature() -> str:
    """Cheap fingerprint of content/<subject>/<episode>/ — subject.json + each episode's
    text/voices.json/audio (mtime + size). Detects new subjects, episodes, and audio."""
    parts: list[str] = []
    if not CONTENT_DIR.is_dir():
        return ""
    for subject in sorted(CONTENT_DIR.iterdir()):
        if not subject.is_dir() or subject.name.startswith("_"):
            continue
        cfg = subject / "subject.json"
        if cfg.exists():
            st = cfg.stat()
            parts.append(f"{subject.name}/subject.json:{int(st.st_mtime)}:{st.st_size}")
        for folder in sorted(subject.iterdir()):
            if not folder.is_dir() or folder.name.startswith("_"):
                continue
            watched = [folder / "script.md", folder / "supplementary.md",
                       folder / "quiz.json", folder / "voices.json", *folder.glob("*.m4a")]
            for f in sorted(watched):
                if f.exists():
                    st = f.stat()
                    parts.append(f"{subject.name}/{folder.name}/{f.name}:{int(st.st_mtime)}:{st.st_size}")
    return "\n".join(parts)


def rebuild() -> tuple[int, int, int]:
    manifest = build_manifest()
    write_manifest(manifest)
    subs = manifest["subjects"]
    mods = sum(len(s["modules"]) for s in subs)
    eps = sum(len(m["episodes"]) for s in subs for m in s["modules"])
    return len(subs), mods, eps


def main() -> None:
    print(f"Watching {CONTENT_DIR} — press Ctrl-C to stop")
    last_sig = ""
    try:
        last_sig = content_signature()
        subs, mods, eps = rebuild()
        print(f"[init] {subs} subjects, {mods} modules, {eps} episodes")
    except Exception as exc:
        print(f"[init] failed: {exc}", file=sys.stderr)

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            sig = content_signature()
            if sig == last_sig:
                continue
            added = sorted(set(sig.splitlines()) - set(last_sig.splitlines()))
            try:
                subs, mods, eps = rebuild()
                last_sig = sig
                print(f"[update] {subs} subjects, {mods} modules, {eps} episodes "
                      f"(+{len(added)} changed file(s))")
                for line in added[:6]:
                    print(f"         + {line.split(':')[0]}")
                if len(added) > 6:
                    print(f"         … and {len(added) - 6} more")
            except Exception as exc:
                print(f"[error] rebuild failed: {exc}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
