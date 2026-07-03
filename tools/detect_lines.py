#!/usr/bin/env python3
"""Count ruled answer/working lines per question part — deterministic, ZERO tokens.

Papers provision writing space as ruled lines under a part. Knowing how many lets the
generator reproduce the original paper's provisioning instead of guessing from marks.
Two printing styles exist (verified on the corpus):

  - dot-leader TEXT lines:  "..........."  (DT, English — lines of dots in the text layer)
  - vector rules:           thin horizontal strokes/rects from page.get_drawings()

Scanned papers get a raster fallback: per-row darkness over the rendered page PNGs with
a spacing-regularity guard so diagrams/tables don't count as ruling.

Besides lineCount, each region gets `linesTopY` — the normalised y where its TRAILING
block of ruled lines begins (lines sitting below the last text, running to the region
bottom). bake_questions.py trims crops there by default: the canonical crop stores the
question WITHOUT the ruled lines, and the generator re-renders lineCount clean lines
("screenshot on standard lined paper"). One image, no duplicate line-full copy.

Runs AFTER a locate step and BEFORE bake: writes lineCount per part and linesTopY per
region into papers/_work/<paperId>/boundaries.json (additive fields, re-runnable).

Known v1 limit: regions end at the next anchor or page bottom, so answer lines on
continuation pages are not counted toward the part that owns them (the continuation
region carries its own count).

    python3 tools/detect_lines.py "<paperId>" [<paperId> ...]
    python3 tools/detect_lines.py --all
"""
import json
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "papers" / "_work"

DOT_MIN = 30          # a text line with this many '.' is a dot-leader answer line
RULE_MIN_FRAC = 0.40  # a rule must span this fraction of the region width
EDGE_PT = 20          # ignore rules within this many points of page top/bottom
TRIM_PAD_PT = 6       # trim this far above the first trailing line
BOTTOM_SLACK_PT = 120 # trailing block must reach within this of the region bottom
FOOTER_PT = 75        # ignore text/rules in this bottom page band (page numbers, "Please turn over")
DARK_FRAC = 0.30      # raster: row is a line candidate at this dark-pixel fraction
DARK_DELTA = 40       # raster: "dark" = this much below the background level (faint rules)
MERGE_PX = 4          # raster: rows closer than this collapse into one line
MAX_THICK = 4         # raster: a rule is thin; thicker groups are text bands, not ruling
MIN_LINES = 3         # raster: fewer candidates than this → probably a diagram, count 0
MAX_SPACING_CV = 0.35 # raster: ruling is evenly spaced; diagrams aren't


def rule_ys(page, clip):
    """y positions (points) of distinct horizontal vector rules inside clip."""
    ys = {}
    for d in page.get_drawings():
        for item in d["items"]:
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                if abs(p1.y - p2.y) < 1 and clip.y0 <= p1.y <= clip.y1:
                    x0, x1 = sorted((p1.x, p2.x))
                    ys.setdefault(round(p1.y), []).append((max(x0, clip.x0), min(x1, clip.x1)))
            elif item[0] == "re":
                r = item[1]
                if r.height < 2 and clip.y0 <= r.y0 <= clip.y1:
                    ys.setdefault(round(r.y0), []).append((max(r.x0, clip.x0), min(r.x1, clip.x1)))
    out = []
    page_h = page.rect.height
    for y, segs in sorted(ys.items()):
        if y < EDGE_PT or y > page_h - FOOTER_PT:   # header/footer rules + footer separator
            continue
        x0 = min(s[0] for s in segs); x1 = max(s[1] for s in segs)
        if x1 - x0 >= RULE_MIN_FRAC * clip.width:  # dashed rules: grouped extent must span
            out.append(float(y))
    return out


def text_lines_in_clip(page, clip):
    """(dot-leader line ys, bottom y of the lowest NON-dot content text) in points.
    Text in the page's footer band (page numbers, "Please turn over", copyright)
    doesn't count as content — it sits below the writing lines and would mask them."""
    dots = []
    text_bottom = clip.y0
    footer_y = page.rect.height - FOOTER_PT
    for block in page.get_text("dict", clip=clip).get("blocks", []):
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(s["text"] for s in spans)
            y0 = min(s["bbox"][1] for s in spans)
            y1 = max(s["bbox"][3] for s in spans)
            if text.count(".") >= DOT_MIN:
                dots.append(y0)
            elif text.strip() and y0 < footer_y:
                text_bottom = max(text_bottom, y1)
    return sorted(dots), text_bottom


def raster_lines(img, bbox):
    """(lineCount, trimTopY normalised or None, spaceHeight normalised) for a bbox
    of a rendered page PNG."""
    W, H = img.size
    x0, y0, x1, y1 = int(bbox[0] * W), int(bbox[1] * H), int(bbox[2] * W), int(bbox[3] * H)
    if x1 - x0 < 20 or y1 - y0 < 10:
        return 0, None, 0.0
    cx0 = x0 + (x1 - x0) // 10
    cx1 = x1 - (x1 - x0) // 10
    g = img.convert("L").crop((cx0, y0, cx1, y1))
    px = g.load()
    w, h = g.size
    sample = sorted(px[x, y] for y in range(0, h, 7) for x in range(0, w, 7))
    background = sample[len(sample) * 3 // 4] if sample else 255
    thresh = background - DARK_DELTA
    cand = []
    for y in range(h):
        dark = sum(1 for x in range(0, w, 2) if px[x, y] < thresh) / max(1, w // 2)
        if dark >= DARK_FRAC:
            cand.append(y)
    groups = []
    for y in cand:
        if groups and y - groups[-1][-1] < MERGE_PX:
            groups[-1].append(y)
        else:
            groups.append([y])
    thin = [g_ for g_ in groups if g_[-1] - g_[0] < MAX_THICK]     # rules
    thick = [g_ for g_ in groups if g_[-1] - g_[0] >= MAX_THICK]   # text bands / images
    if len(thin) < MIN_LINES:
        return 0, None, 0.0
    centers = [sum(g_) / len(g_) for g_ in thin]
    gaps = [b - a for a, b in zip(centers, centers[1:])]
    mean = sum(gaps) / len(gaps)
    if mean <= 0 or (sum((x - mean) ** 2 for x in gaps) / len(gaps)) ** 0.5 / mean > MAX_SPACING_CV:
        return 0, None, 0.0
    count = len(thin)
    # trailing block: thin ruled lines below the last text band, nothing after them
    text_bottom = max((g_[-1] for g_ in thick), default=0)
    trailing = [g_ for g_ in thin if g_[0] > text_bottom]
    trim = None
    space_norm = 0.0
    if len(trailing) >= 2:
        trim = (y0 + trailing[0][0] - 4) / H
        centers = [sum(g_) / len(g_) for g_ in trailing]
        space_norm = block_space(centers) / H
    return count, trim, space_norm


def block_space(ys, default_gap=24.0):
    """Vertical extent (points/px) the ruled block provisions: span + one line gap.
    Line COUNTS aren't comparable across papers (different line spacing); the actual
    space is — the generator re-rules it at its own standard gap."""
    if not ys:
        return 0.0
    if len(ys) == 1:
        return default_gap
    gaps = sorted(b - a for a, b in zip(ys, ys[1:]))
    med = gaps[len(gaps) // 2]
    return (ys[-1] - ys[0]) + med


def region_lines(page, clip):
    """(lineCount, trimTopY normalised or None, spaceHeight pt) for a born-digital region."""
    dots, text_bottom = text_lines_in_clip(page, clip)
    rules = rule_ys(page, clip)
    line_ys = dots if len(dots) >= len(rules) else rules
    count = len(line_ys)
    if not line_ys:
        return 0, None, 0.0
    # trailing block = ruled lines with no content text below them (footer excluded);
    # whitespace after the block is fine — it gets trimmed along with the lines
    trailing = sorted(y for y in line_ys if y > text_bottom - 2)
    trim = None
    if trailing and (len(trailing) >= 2 or dots):
        trim = max(clip.y0, min(trailing) - TRIM_PAD_PT) / page.rect.height
    return count, trim, block_space(trailing if trailing else sorted(line_ys))


def content_bottom(img, bbox):
    """Normalised y of the last CONTENT row in a region of the rendered page PNG —
    tightens crops to actual content instead of running to the next heading. In
    papers with no ruled lines, the blank gap below content is the writing space."""
    W, H = img.size
    x0, y0, x1, y1 = int(bbox[0] * W), int(bbox[1] * H), int(bbox[2] * W), int(bbox[3] * H)
    if x1 - x0 < 20 or y1 - y0 < 10:
        return None
    g = img.convert("L").crop((x0, y0, x1, y1))
    px = g.load()
    w, h = g.size
    sample = sorted(px[x, y] for y in range(0, h, 7) for x in range(0, w, 7))
    background = sample[len(sample) * 3 // 4] if sample else 255
    thresh = background - 30
    last = None
    for y in range(h - 1, -1, -1):
        dark = sum(1 for x in range(0, w, 3) if px[x, y] < thresh)
        if dark >= max(2, (w // 3) * 0.008):
            last = y
            break
    if last is None:
        return None
    return (y0 + last + 8) / H       # small pad below the last content row


def count_for_regions(regions, info, doc, images):
    """(lineCount, spaceHeight pt) for one part's regions ((None, None) when no source);
    annotates regions with linesTopY (trailing ruled block) and contentBottomY (last
    real content — used to trim trailing whitespace out of crops)."""
    total = 0
    space = 0.0
    seen_any = False
    for r in regions:
        if r.get("doc"):          # marking-guide regions aren't writing space
            continue
        pg = r["page"]
        pinfo = info["pages"][pg]
        r.pop("linesTopY", None)
        r.pop("contentBottomY", None)
        if doc is not None and pinfo.get("rotation", 0) == 0:
            page = doc[pg]
            W, H = pinfo["wpt"], pinfo["hpt"]
            clip = fitz.Rect(r["bbox"][0] * W, r["bbox"][1] * H,
                             r["bbox"][2] * W, r["bbox"][3] * H)
            n, trim, sp = region_lines(page, clip)
        else:
            img = images.get(pg)
            n, trim, sp_norm = raster_lines(img, r["bbox"]) if img is not None else (0, None, 0.0)
            sp = sp_norm * pinfo["hpt"]      # normalised → points
        if trim is not None and trim > r["bbox"][1] + 0.005:
            r["linesTopY"] = round(trim, 5)
        elif n == 0 and images.get(pg) is not None:
            # no ruled lines in this region — tighten to content; the blank tail
            # below content is the provisioned (blank) writing space
            cb = content_bottom(images[pg], r["bbox"])
            if cb is not None and r["bbox"][3] - cb > 0.02:
                r["contentBottomY"] = round(min(cb, r["bbox"][3]), 5)
                gap_pt = (r["bbox"][3] - cb) * pinfo["hpt"]
                if gap_pt > 40:
                    sp += gap_pt
        seen_any = True
        total += n
        space += sp
    return (total, round(space, 1)) if seen_any else (None, None)


def run(paper_id):
    wd = WORK / paper_id
    info = json.loads((wd / "info.json").read_text())
    bpath = wd / "boundaries.json"
    if not bpath.exists():
        print(f"  SKIP {paper_id}: no boundaries.json (run a locate step first)")
        return None
    boundaries = json.loads(bpath.read_text())

    doc = None
    if info.get("bornDigital"):
        pdf = ROOT / "papers" / info["path"]
        if pdf.exists():
            doc = fitz.open(pdf)

    images = {}
    from PIL import Image
    for pinfo in info["pages"]:
        p = wd / pinfo["image"]
        if p.exists():
            images[pinfo["page"]] = Image.open(p)   # "page" is 0-based
    if doc is None and not images:
        print(f"  SKIP {paper_id}: scanned but no rendered pages (run render_paper.py)")
        return None

    parts_counted = trims = 0
    for q in boundaries.get("questions", []):
        q_total = q_space = None
        for p in q.get("parts", []):
            n, sp = count_for_regions(p.get("regions", []), info, doc, images)
            p["lineCount"] = n
            p["spaceHeight"] = sp
            if n is not None:
                q_total = (q_total or 0) + n
                q_space = round((q_space or 0.0) + (sp or 0.0), 1)
                if n:
                    parts_counted += 1
            trims += sum(1 for r in p.get("regions", []) if r.get("linesTopY"))
        q["lineCount"] = q_total
        q["spaceHeight"] = q_space
    bpath.write_text(json.dumps(boundaries, indent=2))
    nparts = sum(len(q.get("parts", [])) for q in boundaries.get("questions", []))
    print(f"  {paper_id}: lines on {parts_counted}/{nparts} parts, {trims} regions trimmable "
          f"[{'vector/dots' if doc is not None else 'raster'}]")
    return parts_counted


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--all":
        for wd in sorted(WORK.iterdir()):
            if wd.is_dir() and (wd / "boundaries.json").exists() and (wd / "info.json").exists():
                try:
                    run(wd.name)
                except Exception as e:
                    print(f"  ERROR {wd.name}: {e}")
    else:
        for pid in sys.argv[1:]:
            run(pid)


if __name__ == "__main__":
    main()
