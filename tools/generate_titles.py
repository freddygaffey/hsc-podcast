#!/usr/bin/env python3
"""Render a short spoken-title clip (`_title.m4a`) for each audio episode.

The app plays this (a brief break, then the title) before the episode itself, so listeners
hear what's coming when episodes auto-advance — WITHOUT re-rendering the episode bodies.
Titles are spoken in the QUESTION (second) voice so they read as a distinct announcer.

  .tts-venv/bin/python tools/generate_titles.py [--subject dt] [--voice bm_fable] [--force]

Loads the Kokoro model ONCE and loops, so it's fast despite many short clips. Output keys
match the audio convention (`<subject>/<episode>/_title.m4a`); upload with tools/upload_audio.py.
The manifest excludes `_`-prefixed clips from the voice picker and exposes `_title.m4a` as
`titleAudio`.
"""
import argparse, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SR = 24000
FOLDER_RE = re.compile(r"^([A-Z]+\d*)-(\d+)(?:-(\d+))?-(.+)$")
CASE_RE = re.compile(r"^case_(.+)$")
_ACRONYMS = {"ligo": "LIGO", "emf": "EMF", "led": "LED", "uv": "UV", "dc": "DC", "ac": "AC",
             "ai": "AI", "ml": "ML", "ddos": "DDoS", "dns": "DNS", "y2k": "Y2K"}

def case_title(slug): return " ".join(_ACRONYMS.get(w.lower(), w.capitalize()) for w in slug.split("_"))

def episode_title(name):
    m = FOLDER_RE.match(name)
    if m: return m.group(4).replace("-", " ")
    c = CASE_RE.match(name)
    if c: return case_title(c.group(1))
    return None  # not an audio episode folder (e.g. papers/, images/)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default=None, help="limit to one subject id (default: all)")
    ap.add_argument("--voice", default="bm_fable", help="question/announcer voice")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--force", action="store_true", help="re-render even if _title.m4a exists")
    args = ap.parse_args()

    # Collect work first (so we can load the model only if there's anything to do).
    jobs = []
    subjects = [CONTENT / args.subject] if args.subject else sorted(CONTENT.iterdir())
    for subj in subjects:
        if not subj.is_dir() or subj.name.startswith("_"): continue
        for folder in sorted(subj.iterdir()):
            if not folder.is_dir() or folder.name.startswith("_"): continue
            if not (folder / "script.md").exists(): continue   # audio episodes only
            title = episode_title(folder.name)
            if not title: continue
            out = folder / "_title.m4a"
            if out.exists() and not args.force: continue
            jobs.append((title, out))
    print(f"{len(jobs)} title clip(s) to render (voice={args.voice})")
    if not jobs: return

    lang = args.voice[0] if args.voice[:1] in ("a", "b") else "a"
    from kokoro import KPipeline
    pipe = KPipeline(lang_code=lang, device=args.device, repo_id="hexgrad/Kokoro-82M")

    for i, (title, out) in enumerate(jobs, 1):
        chunks = [np.asarray(a, dtype=np.float32) for _g, _p, a in pipe(title + ".", voice=args.voice, speed=args.speed)]
        if not chunks:
            print(f"  [{i}/{len(jobs)}] EMPTY: {out.parent.name}", file=sys.stderr); continue
        full = np.concatenate(chunks)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            wav = tf.name
        sf.write(wav, full, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "aac", "-b:a", "96k",
                        "-metadata", f"comment=title-clip voice={args.voice}", str(out)], check=True)
        Path(wav).unlink(missing_ok=True)
        print(f"  [{i}/{len(jobs)}] {out.parent.parent.name}/{out.parent.name}  ({len(full)/SR:.1f}s)")
    print("Done. Upload with: python3 tools/upload_audio.py")

if __name__ == "__main__":
    main()
