#!/usr/bin/env python3
"""Step 3 of segmentation: bake per-question (and per-answer) PDFs from boundaries.json.

Deterministic — no LLM. Reads papers/_work/<paperId>/{info.json,boundaries.json}, crops each
question PART's region(s) from the ORIGINAL PDF. Files are named by QUESTION NUMBER and grouped
by PAPER, mirroring the UI (subject -> paper -> questions):

  R2 / bucket:  <subject>/papers/<paperSlug>/paper.pdf  (full original exam)
                <subject>/<paperSlug>/q<num><part>.pdf  (question, e.g. q17b.pdf, q01.pdf)
                <subject>/<paperSlug>/a<num><part>.pdf  (its answer, where a solution exists)
  local stage:  papers/_work/<paperId>/baked/
  meta:         content/<subject>/questions.json

Each record still carries the content hash as `id` (stable, dedupe-detection), but the file is
named by number. Granularity (D4): atomic unit = LETTER PART; romans bundled; shared stem rides.

    python3 tools/bake_questions.py "<paperId>"                    # bake locally
    python3 tools/bake_questions.py "<paperId>" --upload hsc-questions   # bake + push to R2
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"
WORK = PAPERS / "_work"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def paper_meta_for(paper_id):
    """(subjectSlug, paperSlug, sourcePath) from papers/_index.json. paperSlug is a readable
    folder name, e.g. '2019-hsc' or '2020-barker-trial'."""
    idx = PAPERS / "_index.json"
    if idx.exists():
        for p in json.loads(idx.read_text())["papers"]:
            if p["paperId"] == paper_id:
                subj = slug(p["subject"])
                year = p.get("year") or "unknown"
                sch = slug(p.get("school") or "")
                kind = p.get("kind") or "paper"
                var = slug(p.get("variant") or "")
                if kind == "hsc":
                    ps = f"{year}-hsc"
                elif kind in ("trial", "yearly") and sch:
                    ps = f"{year}-{sch}-{kind}"
                else:
                    ps = f"{year}-{kind}"
                if var:
                    ps += f"-{var}"
                return subj, ps, p["path"]
    return "misc", slug(paper_id), None


def numkey(number, label):
    """'17','b' -> '17b'; '1',None -> '01'; pads the numeric part for sorting."""
    num = (str(number) if number is not None else "").strip()
    m = re.match(r"(\d+)(.*)", num)
    base = (m.group(1).zfill(2) + slug(m.group(2))) if m else (slug(num) or "x")
    return f"{base}{(label or '').lower()}"


def bake_region_pdf(src, info, regions):
    """Stack the region rectangles vertically into one single-page PDF (bytes).

    `clip` is always given in DISPLAY (post-rotation) space — the same space
    pNN.png / boundaries.json bboxes use (`pg["wpt"]/["hpt"]` are the display
    dims). `get_pixmap(clip=...)` correctly honours the page's own /Rotate
    when given a display-space clip; `show_pdf_page(clip=...)` does NOT, so
    it's only safe to use on upright (rotation == 0) pages."""
    born = info["bornDigital"]
    pages = {p["page"]: p for p in info["pages"]}
    rects = []
    for r in regions:
        pg = pages[r["page"]]
        x0, y0, x1, y1 = r["bbox"]
        clip = fitz.Rect(x0 * pg["wpt"], y0 * pg["hpt"], x1 * pg["wpt"], y1 * pg["hpt"])
        rects.append((r["page"], clip, pg.get("rotation", 0) % 360))
    out = fitz.open()
    width = max(clip.width for _, clip, _ in rects)
    total_h = sum(clip.height for _, clip, _ in rects)
    page = out.new_page(width=width, height=total_h)
    y = 0.0
    for pno, clip, rotation in rects:
        dest = fitz.Rect(0, y, clip.width, y + clip.height)
        if born and rotation == 0:
            page.show_pdf_page(dest, src, pno, clip=clip)                    # vector
        else:
            pix = src[pno].get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip)   # raster (rotation-safe)
            page.insert_image(dest, pixmap=pix)
        y += clip.height
    data = out.tobytes(deflate=True, garbage=4)
    out.close()
    return data


def r2_put(bucket, key, path):
    subprocess.run(["wrangler", "r2", "object", "put", f"{bucket}/{key}",
                    "--file", str(path), "--remote"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    bucket = None
    if "--upload" in args:
        i = args.index("--upload")
        bucket = args[i + 1]
        del args[i:i + 2]
    paper_id = args[0]

    wd = WORK / paper_id
    info = json.loads((wd / "info.json").read_text())
    bounds = json.loads((wd / "boundaries.json").read_text())
    subj, paper_slug, src_rel = paper_meta_for(paper_id)
    if info.get("subject"):
        subj = info["subject"]
    baked = wd / "baked"
    baked.mkdir(exist_ok=True)
    for old in baked.glob("*.pdf"):        # clear stale files so re-bakes don't leave orphans
        old.unlink()
    src = fitz.open(ROOT / "papers" / info["path"])

    # Merge continuation entries ("Question 11 (continued)" pages are detected as a second
    # question with the same number) into their parent so the whole-question bake is complete.
    merged, by_num = [], {}
    for q in bounds["questions"]:
        num = str(q.get("number")) if q.get("number") is not None else None
        prev = by_num.get(num)
        if prev is not None and num is not None:
            prev["stimulus"] = (prev.get("stimulus") or []) + (q.get("stimulus") or [])
            if prev.get("parts") or q.get("parts"):
                prev["parts"] = (prev.get("parts") or []) + (q.get("parts") or [])
            else:
                prev["regions"] = (prev.get("regions") or []) + (q.get("regions") or [])
            prev["marks"] = prev.get("marks") or q.get("marks")
        else:
            merged.append(q)
            if num is not None:
                by_num[num] = q
    bounds = {**bounds, "questions": merged}

    records = []
    used = set()
    for qi, q in enumerate(bounds["questions"]):
        stim = q.get("stimulus", [])
        parts = q.get("parts") or [{"label": None, "marks": q.get("marks"),
                                    "type": q.get("type"), "regions": q.get("regions", []),
                                    "markingRegions": q.get("markingRegions", [])}]
        # Whole-question bake (the generator's display unit — parts are metadata only):
        # stem/stimulus once, then every part's regions in order. Partless questions fall
        # through to the loop below, which bakes the same thing under the same key.
        if q.get("parts"):
            wregions = stim + [r for part in parts for r in part.get("regions", [])]
            wmarking = [r for part in parts for r in part.get("markingRegions") or []]
            data = bake_region_pdf(src, info, wregions)
            qid = hashlib.sha256(data).hexdigest()[:12]
            name = numkey(q.get("number") or (qi + 1), None)
            base, k = name, 1
            while name in used:            # e.g. two number-less parted questions
                name = f"{base}-{k}"; k += 1
            used.add(name)
            (baked / f"q{name}.pdf").write_bytes(data)
            answer_key = None
            if wmarking:
                (baked / f"a{name}.pdf").write_bytes(bake_region_pdf(src, info, wmarking))
                answer_key = f"a{name}.pdf"
            pmarks = [p.get("marks") for p in parts]
            records.append({
                "id": qid, "subject": subj, "paperSlug": paper_slug,
                "assetKey": f"q{name}.pdf", "answerKey": answer_key,
                "paperId": info["paperId"], "questionNumber": q.get("number"),
                "partLabel": None,
                "marks": q.get("marks") or (sum(m for m in pmarks if m) or None),
                "questionMarks": q.get("marks"), "type": q.get("type"),
                "topic": q.get("topic"), "module": q.get("module"),
                "syllabusRefs": q.get("syllabusRefs") or [],
                "hasStimulus": bool(stim), "bytes": len(data),
                "unit": "question", "parts": [p.get("label") for p in parts if p.get("label")],
            })
        for part in parts:
            data = bake_region_pdf(src, info, stim + part["regions"])   # stem rides with part
            qid = hashlib.sha256(data).hexdigest()[:12]                 # content id (dedupe)
            name = numkey(q.get("number") or (qi + 1), part.get("label"))
            base = name
            k = 1
            while name in used:            # disambiguate rare collisions
                name = f"{base}-{k}"; k += 1
            used.add(name)
            (baked / f"q{name}.pdf").write_bytes(data)

            answer_key = None
            mr = part.get("markingRegions") or []
            if mr:                                                      # bake the paired answer
                adata = bake_region_pdf(src, info, mr)
                (baked / f"a{name}.pdf").write_bytes(adata)
                answer_key = f"a{name}.pdf"

            records.append({
                "id": qid, "subject": subj, "paperSlug": paper_slug,
                "assetKey": f"q{name}.pdf", "answerKey": answer_key,
                "paperId": info["paperId"], "questionNumber": q.get("number"),
                "partLabel": part.get("label"), "marks": part.get("marks"),
                "questionMarks": q.get("marks"), "type": part.get("type") or q.get("type"),
                "topic": q.get("topic"), "module": q.get("module"),
                "syllabusRefs": q.get("syllabusRefs") or [],
                "hasStimulus": bool(stim), "bytes": len(data),
                "unit": "question" if part.get("label") is None else "part",
            })

    (wd / "questions.json").write_text(json.dumps(
        {"subject": subj, "paperSlug": paper_slug, "questions": records}, indent=2))

    n_ans = sum(1 for r in records if r["answerKey"])
    total = sum(r["bytes"] for r in records)
    print(f"{paper_id}: {len(records)} parts ({n_ans} answers) -> {subj}/{paper_slug}/  "
          f"({total/1024:.0f} KB)")

    if bucket:
        # full original paper
        if src_rel and (PAPERS / src_rel).exists():
            r2_put(bucket, f"{subj}/papers/{paper_slug}/paper.pdf", PAPERS / src_rel)
        for r in records:
            r2_put(bucket, f"{subj}/papers/{paper_slug}/{r['assetKey']}", baked / r["assetKey"])
            if r["answerKey"]:
                r2_put(bucket, f"{subj}/papers/{paper_slug}/{r['answerKey']}", baked / r["answerKey"])
        print(f"  uploaded to {bucket}/{subj}/papers/{paper_slug}/")


if __name__ == "__main__":
    main()
