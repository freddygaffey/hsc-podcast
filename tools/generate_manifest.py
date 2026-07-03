#!/usr/bin/env python3
"""Scan content/<subject>/ and generate the unified manifest.json.

Output shape: {"subjects": [ {id, name, shortName, groupNames, yearMap, yearOrder,
repoUrl, modules:[...]}, ... ]}. Each subject is a folder under content/ containing a
subject.json (its metadata) and episode folders. Adding a subject = drop in such a folder;
no code change here.

Audio durations come from local <voice>.m4a if present (an authoring machine that just
rendered them), otherwise from the committed voices.json the port wrote (so the repo needs
no local audio — audio is served from R2 via the subject's audioBaseUrl).

Importable: build_manifest() returns the dict; reused by serve.py / watch_manifest.py."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
OUTPUT = ROOT / "manifest.json"

# Episode folders are MODULE-LL-Title (MODULE = letters + optional digits, e.g. M6, PF11);
# LL is the lesson number. Case-study folders are case_<slug>, grouped under a synthetic
# "CASE" module.
FOLDER_RE = re.compile(r"^([A-Z]+\d*)-(\d+)(?:-(\d+))?-(.+)$")
CASE_RE = re.compile(r"^case_(.+)$")
# Past papers live under content/<subject>/papers/p<N>/ (one folder per exam paper),
# grouped under a synthetic "EXAM" module. Shared stimulus images sit in papers/images/.
PAPER_RE = re.compile(r"^p(\d+)$")
_ACRONYMS = {"ligo": "LIGO", "emf": "EMF", "led": "LED", "uv": "UV", "dc": "DC", "ac": "AC",
             "ai": "AI", "ml": "ML", "ddos": "DDoS", "dns": "DNS", "xz": "XZ", "npm": "npm",
             "y2k": "Y2K", "compas": "COMPAS", "737": "737", "mcas": "MCAS"}


def case_title(slug: str) -> str:
    return " ".join(_ACRONYMS.get(w.lower(), w.capitalize()) for w in slug.split("_"))


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return round(float(result.stdout.strip()), 1)


def audio_url(audio_base: str, subject_id: str, ep: str, voice: str) -> str:
    """Where the app fetches a voice file. Audio lives in ONE R2 bucket with a folder per
    subject, so keys are <subject>/<ep>/<voice>.m4a behind a single audioBaseUrl
    (e.g. https://audio.hsc.pebnum.com). The local-dev sentinel "content" serves the same
    relative layout from the repo."""
    if audio_base in ("", "content"):
        return f"content/{subject_id}/{ep}/{voice}.m4a"
    return f"{audio_base.rstrip('/')}/{subject_id}/{ep}/{voice}.m4a"


def build_voices(folder: Path, subject_id: str, audio_base: str) -> list[dict]:
    """Voice list + durations for one episode. Prefer local .m4a (probe); fall back to the
    committed voices.json (name + duration only)."""
    ep = folder.name
    # Underscore-prefixed clips (e.g. _title.m4a, the spoken-title intro) are not selectable voices.
    local = sorted(m for m in folder.glob("*.m4a") if not m.name.startswith("_"))
    if local:
        voices = []
        for m4a in local:
            try:
                dur = ffprobe_duration(m4a)
            except subprocess.CalledProcessError:
                print(f"WARN  unreadable audio, skipping: {subject_id}/{ep}/{m4a.name}", file=sys.stderr)
                continue
            voices.append({"name": m4a.stem,
                           "file": audio_url(audio_base, subject_id, ep, m4a.stem),
                           "duration": dur})
        return voices
    cache = folder / "voices.json"
    if cache.exists():
        return [{"name": v["name"],
                 "file": audio_url(audio_base, subject_id, ep, v["name"]),
                 "duration": v["duration"]}
                for v in json.loads(cache.read_text())]
    return []


def build_episode(folder: Path, subject_id: str, audio_base: str, title: str, unit) -> dict:
    ep = folder.name
    return {
        "id": ep,
        "title": title,
        "unit": unit,
        "scriptPath": f"content/{subject_id}/{ep}/script.md" if (folder / "script.md").exists() else None,
        "supplementaryPath": f"content/{subject_id}/{ep}/supplementary.md" if (folder / "supplementary.md").exists() else None,
        "quizPath": f"content/{subject_id}/{ep}/quiz.json" if (folder / "quiz.json").exists() else None,
        "titleAudio": audio_url(audio_base, subject_id, ep, "_title") if (folder / "_title.m4a").exists() else None,
        "voices": build_voices(folder, subject_id, audio_base),
    }


def build_episode_at(folder: Path, subject_id: str, rel: str, title: str, unit) -> dict:
    """Like build_episode but for a folder nested under the subject (e.g. papers/p1).
    `rel` is the path segment under content/<subject>/ (e.g. "papers/p1"). Past papers
    carry no audio, so voices is always []."""
    base = f"content/{subject_id}/{rel}"
    return {
        "id": f"{subject_id}-{rel.replace('/', '-')}",
        "title": title,
        "unit": unit,
        "scriptPath": f"{base}/script.md" if (folder / "script.md").exists() else None,
        "supplementaryPath": f"{base}/supplementary.md" if (folder / "supplementary.md").exists() else None,
        "quizPath": f"{base}/quiz.json" if (folder / "quiz.json").exists() else None,
        "pdfPath": f"{base}/paper.pdf" if (folder / "paper.pdf").exists() else None,
        "mgPdfPath": f"{base}/mg.pdf" if (folder / "mg.pdf").exists() else None,
        "voices": [],
    }


def build_papers_module(subject_dir: Path, subject_id: str) -> dict | None:
    """Synthetic "EXAM" module from content/<subject>/papers/p<N>/. Each paper folder with a
    quiz.json becomes an episode; papers/images/ (shared stimulus images) is ignored. Episodes
    sort newest-first via unit = -year."""
    papers_dir = subject_dir / "papers"
    if not papers_dir.is_dir():
        return None
    episodes = []
    for folder in sorted(papers_dir.iterdir()):
        if not folder.is_dir() or folder.name == "images" or folder.name.startswith("_"):
            continue
        if not PAPER_RE.match(folder.name):
            continue
        if not (folder / "quiz.json").exists():
            continue
        meta = json.loads((folder / "paper.json").read_text()) if (folder / "paper.json").exists() else {}
        year = meta.get("year")
        title = meta.get("title") or f"Paper {folder.name[1:]}"
        ep = build_episode_at(folder, subject_id, f"papers/{folder.name}", title,
                              unit=(-year if year else 0))
        ep["paper"] = True
        if year:
            ep["year"] = year
        episodes.append(ep)
    if not episodes:
        return None
    return {"id": "EXAM", "prefix": "EXAM", "moduleNum": 0, "episodes": episodes}


def build_subject(subject_dir: Path) -> dict | None:
    cfg_path = subject_dir / "subject.json"
    if not cfg_path.exists():
        return None
    cfg = json.loads(cfg_path.read_text())
    subject_id = cfg.get("id", subject_dir.name)
    audio_base = cfg.get("audioBaseUrl", "content")

    modules: dict[str, dict] = {}
    for folder in sorted(subject_dir.iterdir()):
        if not folder.is_dir() or folder.name.startswith("_"):
            continue
        if not (folder / "script.md").exists() and not list(folder.glob("*.m4a")) \
           and not (folder / "voices.json").exists():
            continue
        m = FOLDER_RE.match(folder.name)
        case = CASE_RE.match(folder.name)
        if m:
            prefix, lesson_num, _sub, title_slug = m.groups()
            digits = re.search(r"\d+", prefix)
            module_num = int(digits.group()) if digits else 0
            module = modules.setdefault(prefix,
                {"id": prefix, "prefix": prefix, "moduleNum": module_num, "episodes": []})
            module["episodes"].append(
                build_episode(folder, subject_id, audio_base, title_slug.replace("-", " "), int(lesson_num)))
        elif case:
            module = modules.setdefault("CASE",
                {"id": "CASE", "prefix": "CASE", "moduleNum": 0, "episodes": []})
            module["episodes"].append(
                build_episode(folder, subject_id, audio_base, case_title(case.group(1)), None))

    papers_module = build_papers_module(subject_dir, subject_id)
    if papers_module:
        modules["EXAM"] = papers_module

    module_list = []
    for module in sorted(modules.values(), key=lambda m: (m["moduleNum"], m["prefix"])):
        module["episodes"].sort(key=lambda e: (e["unit"] or 0, e["title"]))
        module_list.append(module)

    return {
        "id": subject_id,
        "name": cfg.get("name", subject_id),
        "shortName": cfg.get("shortName", cfg.get("name", subject_id)),
        "description": cfg.get("description", ""),
        "repoUrl": cfg.get("repoUrl", ""),
        "groupNames": cfg.get("groupNames", {}),
        "yearMap": cfg.get("yearMap", {}),
        "yearOrder": cfg.get("yearOrder", ["Case Studies", "Year 12", "Year 11", "Other"]),
        "modules": module_list,
    }


def build_manifest() -> dict:
    subjects = []
    for subject_dir in sorted(CONTENT_DIR.iterdir()):
        if not subject_dir.is_dir() or subject_dir.name.startswith("_"):
            continue
        subj = build_subject(subject_dir)
        if subj and subj["modules"]:
            subjects.append(subj)
    return {"subjects": subjects}


def write_manifest(manifest: dict, output: Path = OUTPUT) -> None:
    output.write_text(json.dumps(manifest, indent=2))


def main() -> None:
    output = Path(os.environ["MANIFEST_OUTPUT"]).resolve() if os.environ.get("MANIFEST_OUTPUT") else OUTPUT
    manifest = build_manifest()
    write_manifest(manifest, output)
    subs = manifest["subjects"]
    total_eps = sum(len(m["episodes"]) for s in subs for m in s["modules"])
    print(f"Wrote {output}: {len(subs)} subjects, "
          f"{sum(len(s['modules']) for s in subs)} modules, {total_eps} episodes")
    for s in subs:
        eps = sum(len(m["episodes"]) for m in s["modules"])
        print(f"  {s['id']:9} {len(s['modules'])} modules, {eps} episodes  (audio: {json.loads((CONTENT_DIR/s['id']/'subject.json').read_text()).get('audioBaseUrl')})")


if __name__ == "__main__":
    main()
