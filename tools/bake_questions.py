#!/usr/bin/env python3
"""Step 3 of segmentation: bake per-question (and per-answer) PDFs from boundaries.json.

Deterministic — no LLM. Reads papers/_work/<paperId>/{info.json,boundaries.json}, crops each
question PART's region(s) from the ORIGINAL PDF into an anonymised per-part PDF keyed by
content hash. If the part has markingRegions (worked solution / marking guide visible in the
paper), the ANSWER is baked too and PAIRED by the same id: q_<id>.pdf + a_<id>.pdf.

Layout (one folder per subject, mirroring the audio bucket):
  R2:    <subjectSlug>/q_<id>.pdf   and   <subjectSlug>/a_<id>.pdf
  local: papers/_work/<paperId>/baked/   (transient staging; gitignored)
  meta:  content/<subjectSlug>/questions.json  (records; committed)

Granularity (D4): atomic unit = LETTER PART (a, b, c). Roman sub-parts (i, ii) stay bundled.
Top-level question is a metadata GROUP whose shared stem/stimulus rides with every part.

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


def subject_slug_for(paper_id):
    """Map a paperId → its subject slug via papers/_index.json (fallback: 'misc')."""
    idx = PAPERS / "_index.json"
    if idx.exists():
        for p in json.loads(idx.read_text())["papers"]:
            if p["paperId"] == paper_id:
                return slug(p["subject"])
    return "misc"


def bake_region_pdf(src, info, regions):
    """Stack the region rectangles vertically into one single-page PDF (bytes)."""
    born = info["bornDigital"]
    pages = {p["page"]: p for p in info["pages"]}
    rects = []
    for r in regions:
        pg = pages[r["page"]]
        x0, y0, x1, y1 = r["bbox"]
        rects.append((r["page"], fitz.Rect(x0 * pg["wpt"], y0 * pg["hpt"],
                                           x1 * pg["wpt"], y1 * pg["hpt"])))
    out = fitz.open()
    width = max(rc.width for _, rc in rects)
    total_h = sum(rc.height for _, rc in rects)
    page = out.new_page(width=width, height=total_h)
    y = 0.0
    for pno, clip in rects:
        dest = fitz.Rect(0, y, clip.width, y + clip.height)
        if born:
            page.show_pdf_page(dest, src, pno, clip=clip)                    # vector
        else:
            pix = src[pno].get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip)   # raster
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
    subj = subject_slug_for(paper_id)                    # R2/manifest folder for this subject
    baked = wd / "baked"
    baked.mkdir(exist_ok=True)
    src = fitz.open(ROOT / "papers" / info["path"])

    records = []
    for q in bounds["questions"]:
        stim = q.get("stimulus", [])
        parts = q.get("parts") or [{"label": None, "marks": q.get("marks"),
                                    "type": q.get("type"), "regions": q.get("regions", []),
                                    "markingRegions": q.get("markingRegions", [])}]
        for part in parts:
            data = bake_region_pdf(src, info, stim + part["regions"])   # stem rides with part
            qid = hashlib.sha256(data).hexdigest()[:12]                 # shared id for q + a
            (baked / f"q_{qid}.pdf").write_bytes(data)

            answer_key = None
            mr = part.get("markingRegions") or []
            if mr:                                                      # bake the paired answer
                adata = bake_region_pdf(src, info, mr)
                (baked / f"a_{qid}.pdf").write_bytes(adata)
                answer_key = f"a_{qid}.pdf"

            records.append({
                "id": qid, "subject": subj,
                "assetKey": f"q_{qid}.pdf", "answerKey": answer_key,
                "paperId": info["paperId"], "questionNumber": q.get("number"),
                "partLabel": part.get("label"), "marks": part.get("marks"),
                "questionMarks": q.get("marks"), "type": part.get("type") or q.get("type"),
                "topic": q.get("topic"), "hasStimulus": bool(stim), "bytes": len(data),
            })

    (wd / "questions.json").write_text(json.dumps({"subject": subj, "questions": records}, indent=2))

    n_ans = sum(1 for r in records if r["answerKey"])
    total = sum(r["bytes"] for r in records)
    print(f"{paper_id}: baked {len(records)} parts ({n_ans} with answers) -> {baked.relative_to(ROOT)}")
    print(f"  subject folder: {subj}/   ({total/1024:.0f} KB questions)")
    for r in records:
        lbl = f"Q{r['questionNumber']}{r['partLabel'] or ''}"
        print(f"  {subj}/q_{r['id']}.pdf  {lbl:7} {str(r['marks'])}m  "
              f"{'+a' if r['answerKey'] else '  '}  {r['topic']}")

    if bucket:
        print(f"Uploading to R2 '{bucket}' under {subj}/ …")
        for r in records:
            r2_put(bucket, f"{subj}/{r['assetKey']}", baked / r["assetKey"])
            if r["answerKey"]:
                r2_put(bucket, f"{subj}/{r['answerKey']}", baked / r["answerKey"])
        print("  done.")


if __name__ == "__main__":
    main()
