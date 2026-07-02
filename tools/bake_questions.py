#!/usr/bin/env python3
"""Step 3 of segmentation: bake per-question PDFs from the locate step's boundaries.json.

Deterministic — no LLM. Reads papers/_work/<paperId>/{info.json,boundaries.json}, crops each
question's region(s) from the ORIGINAL PDF, and writes an anonymised per-question PDF keyed by
content hash (q_<hash>.pdf → non-enumerable + auto-dedup). Born-digital → vector clip
(show_pdf_page, tiny + print-perfect); scanned → raster crop.

Granularity (Fred's rule): the atomic baked unit is a LETTER PART (a, b, c). Roman sub-parts
(i, ii) stay bundled inside their letter part. The top-level question is a metadata GROUP whose
shared stem/stimulus rides along with every part (so a split-off part still makes sense). A
question with no letter parts bakes as a single unit (label null).

boundaries.json (produced by the Claude Code locate agent), coords NORMALISED 0–1, top-left:
  { "questions": [
      { "number":"14", "marks":5, "topic":"Probability",
        "stimulus":[ {"page":12,"bbox":[0.11,0.08,0.86,0.24]} ],   // shared, rides with each part
        "parts":[
          {"label":"a","marks":2,"type":"short","regions":[{"page":12,"bbox":[0.11,0.25,0.86,0.53]}]},
          {"label":"b","marks":1,"type":"short","regions":[{"page":12,"bbox":[0.11,0.55,0.86,0.68]}]}
        ] } ] }

    python3 tools/bake_questions.py "<paperId>" [--upload BUCKET]
"""
import hashlib
import json
import sys
from pathlib import Path

import fitz  # pymupdf

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"


def bake_region_pdf(src, info, regions):
    """Stack the region rectangles vertically into one single-page PDF (bytes)."""
    born = info["bornDigital"]
    pages = {p["page"]: p for p in info["pages"]}
    # Convert normalised bboxes → source-page point rects.
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
            page.show_pdf_page(dest, src, pno, clip=clip)          # vector
        else:
            pix = src[pno].get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip)  # raster
            page.insert_image(dest, pixmap=pix)
        y += clip.height
    data = out.tobytes(deflate=True, garbage=4)
    out.close()
    return data


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    paper_id = sys.argv[1]
    wd = WORK / paper_id
    info = json.loads((wd / "info.json").read_text())
    bounds = json.loads((wd / "boundaries.json").read_text())
    baked = wd / "baked"
    baked.mkdir(exist_ok=True)
    src = fitz.open(ROOT / "papers" / info["path"])

    records = []
    for q in bounds["questions"]:
        stim = q.get("stimulus", [])
        # A question with no letter parts → one implicit part carrying the whole question.
        parts = q.get("parts") or [{"label": None, "marks": q.get("marks"),
                                    "type": q.get("type"), "regions": q.get("regions", [])}]
        for part in parts:
            regions = stim + part["regions"]        # shared stem rides with every part
            data = bake_region_pdf(src, info, regions)
            key = "q_" + hashlib.sha256(data).hexdigest()[:12]
            (baked / f"{key}.pdf").write_bytes(data)
            records.append({
                "id": key,
                "assetKey": f"{key}.pdf",
                "paperId": info["paperId"],
                "questionNumber": q.get("number"),       # group metadata
                "partLabel": part.get("label"),          # a | b | c | null
                "marks": part.get("marks"),              # THIS part's marks
                "questionMarks": q.get("marks"),         # parent total
                "type": part.get("type") or q.get("type"),
                "topic": q.get("topic"),
                "hasStimulus": bool(stim),
                "bytes": len(data),
            })
    (wd / "questions.json").write_text(json.dumps({"questions": records}, indent=2))
    total = sum(r["bytes"] for r in records)
    print(f"{paper_id}: baked {len(records)} parts -> {baked.relative_to(ROOT)}  "
          f"({total/1024:.0f} KB total, avg {total/max(1,len(records))/1024:.1f} KB/part)")
    for r in records:
        lbl = f"Q{r['questionNumber']}{r['partLabel'] or ''}"
        print(f"  {r['assetKey']}  {lbl:6} {str(r['marks'])}m  stim={int(r['hasStimulus'])}  {r['bytes']/1024:.1f}KB  {r['topic']}")


if __name__ == "__main__":
    main()
