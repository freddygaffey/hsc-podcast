# HSC Podcast

A Progressive Web App that turns HSC study content into a podcast-style audio
feed (text-to-speech generation, offline playback, per-episode progress). Content
lives under `content/`, the app shell is the root `index.html` / `app.js` /
`service-worker.js`, and voice generation is handled by the `*_tts.py` /
`generate_*` scripts.

This repo also includes tooling to bulk-download **HSC past exam papers** (see
below), used as source material.

---

# HSC Past-Paper Downloaders

Scripts in `papers/` bulk-download HSC/Prelim exam papers, organised by subject.
There are **two independent sources**, each with its own script:

| Script | Source | Rate limit? | Coverage |
|--------|--------|-------------|----------|
| `papers/_nesa.py`       | **NESA official** (`nsw.gov.au`)          | none                 | Official HSC papers + marking guidelines, ~2014–2025 |
| `papers/_downloader.py` | **THSC Online** (`thsconline.github.io`)  | yes (shared, gentle) | HSC + **Trial** papers + Year 11 Yearly, back to the 1990s |

Use **NESA** for the official papers (fast, unlimited). Use **THSC** for the huge
library of school **trial** papers, which NESA doesn't host. Everything saves to
`papers/<Subject>/<category>/*.pdf` and is **resumable** (re-running skips files
already on disk). The `papers/` folder is git-ignored so PDFs are never committed.

```
papers/
  Maths Advanced/
    HSC-NESA/     ← _nesa.py   (official)
    Y12-HSC/      ← _downloader.py
    Y12-Trial/
    Y11-Yearly/
  Physics/  English Advanced/  ...
```

> Full details, tuning knobs, and two-machine/sync setup are in
> [`papers/README.md`](papers/README.md). Quick reference below.

## NESA official papers — `papers/_nesa.py`

No rate limit — just run it:

```bash
cd papers && python3 _nesa.py        # logs to _nesa.log, saves to <Subject>/HSC-NESA/
```

It queries NESA's public Elasticsearch API for every `hsc-exam-papers` page, then
pulls the PDF assets off each exam-pack page.

**Add any subject:** edit the `SUBJECTS` dict — key is NESA's URL slug, value is
the folder name. Each subject has a current slug and usually an `-archive` slug
for older years (map both to the same folder):

```python
SUBJECTS = {
    "chemistry": "Chemistry",
    "chemistry-archive": "Chemistry",
    "biology": "Biology",
}
```

List every available slug from the API:

```bash
curl -s -H "Content-Type: application/json" \
  -X POST "https://www.nsw.gov.au/api/v1/elasticsearch/prod_content/_search" \
  -d '{"size":2000,"_source":["url"],"query":{"wildcard":{"url":"*hsc-exam-papers*"}}}' \
| python3 -c 'import sys,json,re;from collections import defaultdict;\
d=json.load(sys.stdin);s=defaultdict(set);\
[s[m.group(1)].add(m.group(2)) for h in d["hits"]["hits"] \
 for u in [h["_source"]["url"][0] if isinstance(h["_source"]["url"],list) else h["_source"]["url"]] \
 for m in [re.search(r"/hsc-exam-papers/([^/]+)/(\d{4})$",u)] if m];\
[print(k, sorted(v)[0]+"-"+sorted(v)[-1]) for k in sorted(s)]'
```

## THSC papers, incl. trials — `papers/_downloader.py`

THSC fronts a Google Apps Script / Drive backend with a **shared, per-base rate
limit** (it returns a placeholder PDF when a "base" is hit too hard). This is a
free resource students rely on, so the script is deliberately gentle:
round-robins across bases, 30-min cooldown on any throttled base, ~25 s between
requests. A full run therefore trickles over **several days**; it's resumable.

```bash
cd papers
python3 _downloader.py                                   # everything
python3 _downloader.py "Maths Advanced" "Maths Extension 1"   # subject filter (substring match)
python3 _downloader.py Physics
```

Each listing page links every paper through one aggregate "base" id; the script
extracts every `(base, title)` from the page automatically — **you only need the
page URL, never the ids.**

**Add any subject:** add rows to the `PAGES` list —
`(subject_folder, category_tag, page_path)`, where `page_path` is relative to
`https://thsconline.github.io/s/`:

```python
PAGES = [
    ("Chemistry", "Y12-HSC",    "yr12/Chemistry/hscpapers.html"),
    ("Chemistry", "Y12-Trial",  "yr12/Chemistry/trialpapers.html"),
    ("Chemistry", "Y11-Yearly", "yr11/Chemistry/prelimpapers.html"),
]
```

Discover a subject's page filenames:

```bash
curl -s "https://thsconline.github.io/s/yr12/Chemistry/" \
  | grep -oiE 'href="[^"]*\.html"[^>]*>[^<]*</a>'
```

Common pages: `hscpapers.html`, `trialpapers.html`, `prelimpapers.html`
(Year 11). Maths splits by course (`hscpapers_advanced.html`, …); English splits
trials by paper (`trialpapers_paper1.html`, …). Pacing knobs (`GLOBAL_GAP`,
`PER_BASE_GAP`, `COOLDOWN`) are near the top of the script — keep them gentle.

## Progress

```bash
cd papers
tail -f _download.log            # or _nesa.log / _sync.log
find . -name '*.pdf' | wc -l     # total papers on disk
```
