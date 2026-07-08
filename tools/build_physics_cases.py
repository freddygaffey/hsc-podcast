#!/usr/bin/env python3
"""Slice the curated Physics-experiments doc into per-case-study material.

Deterministic — no model paraphrasing. Each experiment section becomes a staged
case-study folder with a faithful supplementary.md (the doc's text, verbatim, with
its inline images copied in and re-referenced) plus a title carrying the star
priority. Also emits case-map.json (the reviewable spine).

Staged under content/physics/_case_staging/<slug>/ (underscore prefix → the
manifest generator skips it) so nothing in the live tree is touched yet.

Run: python3 tools/build_physics_cases.py
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "physics" / "sources" / "experiments"
MD = SRC / "physics-experiments.md"
STAGE = ROOT / "content" / "physics" / "_case_staging"
IMG_RE = re.compile(r"!\[\]\(images/([^)]+)\)")
STAR = "⭐"


def module_prefix(heading: str) -> str:
    m = re.search(r"Module\s+(\d)", heading)
    return f"M{m.group(1)}" if m else "M?"


def slug_of(title: str) -> str:
    t = title.lstrip(STAR).strip()
    t = re.sub(r"\([^)]*\)", "", t)          # drop parentheticals (dates, speeds, notes)
    t = t.split(":")[-1] if ":" in t else t  # keep the specific part after "Discovery of X:"
    t = t.lower()
    t = re.sub(r"[’'\"]", "", t)
    t = re.sub(r"[^a-z0-9]+", "_", t).strip("_")
    return "case_" + "_".join(t.split("_")[:6])


def main():
    lines = MD.read_text(encoding="utf-8").splitlines()
    # Content starts at the SECOND "## Module 5" (the first block is the star index).
    mod5 = [i for i, l in enumerate(lines) if l.startswith("## Module 5")]
    start = mod5[1] if len(mod5) > 1 else 0

    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    cases, cur_mod, cur = [], "M?", None

    def flush():
        if cur:
            cases.append(cur)

    for l in lines[start:]:
        if l.startswith("## "):
            flush(); cur = None
            cur_mod = module_prefix(l)
            continue
        if l.startswith(STAR):
            flush()
            stars = len(l) - len(l.lstrip(STAR))
            title = l.lstrip(STAR).strip()
            cur = {"module": cur_mod, "stars": stars, "title": title,
                   "slug": slug_of(l), "body": [], "images": []}
            continue
        if cur is not None:
            m = IMG_RE.search(l)
            if m:
                cur["images"].append(m.group(1))
            cur["body"].append(l)

    flush()

    # de-dupe slugs
    seen = {}
    for c in cases:
        s = c["slug"]; n = seen.get(s, 0) + 1; seen[s] = n
        if n > 1:
            c["slug"] = f"{s}_{n}"

    manifest = []
    for c in cases:
        folder = STAGE / c["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        # copy + rename images, rewrite refs to the FINAL live path
        body = "\n".join(c["body"]).strip()
        for i, img in enumerate(c["images"], 1):
            ext = img.rsplit(".", 1)[-1]
            newname = f"{c['slug'].replace('case_', '')}-{i:02d}.{ext}"
            src = SRC / "images" / img
            if src.exists():
                shutil.copy(src, folder / newname)
            body = body.replace(f"images/{img}",
                                f"content/physics/{c['slug']}/{newname}")
        title = f"{STAR * c['stars']} {c['title']}"
        supp = f"---\ntitle: \"{title}\"\nmodule: {c['module']}\nstars: {c['stars']}\n---\n\n{body}\n"
        (folder / "supplementary.md").write_text(supp, encoding="utf-8")
        manifest.append({"slug": c["slug"], "module": c["module"], "stars": c["stars"],
                         "title": c["title"], "images": len(c["images"])})

    (SRC / "case-map.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    from collections import Counter
    bymod = Counter(c["module"] for c in manifest)
    bystar = Counter(c["stars"] for c in manifest)
    print(f"Staged {len(manifest)} case studies under {STAGE.relative_to(ROOT)}")
    print("  by module:", dict(sorted(bymod.items())))
    print("  by stars :", dict(sorted(bystar.items(), reverse=True)))
    print(f"  map: {(SRC / 'case-map.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
