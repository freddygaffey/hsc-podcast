# Past-paper segmentation pipeline — runbook

Turns scraped exam PDFs into an **anonymised, per-subject question bank**: each question (and
its answer) baked to its own PDF, keyed by content hash, organised one folder per subject —
mirroring the audio bucket. Vision is **Claude Code (Max plan)** — no Anthropic API key.

## The steps

```
render (code) ──▶ locate + classify (Claude Code agent) ──▶ bake q + a (code) ──▶ R2
```

| Step | Tool / prompt | What it does |
|------|---------------|--------------|
| index | `tools/index_papers.py` | Labels `papers/` from folder paths → `papers/_index.json` |
| render | `tools/render_paper.py "<path>"` | Paper → `papers/_work/<paperId>/pNN.png` + `info.json`; flags born-digital vs scanned; prints the paperId |
| **locate** | **`tools/prompts/locate_questions.md`** | A Claude Code agent reads the page images → `boundaries.json`: where each question/part is, its **type + topic**, and the **marking region** for its answer. Does NOT transcribe. |
| bake | `tools/bake_questions.py "<paperId>" [--upload hsc-questions]` | Crops each **letter part** → `q_<id>.pdf`; if a marking region exists, also `a_<id>.pdf` (**same id**). Vector for born-digital, raster for scanned. Uploads under the subject folder. |
| batch | `tools/prompts/process_all_papers.md` | Driver to run the whole `papers/_index.json` and place everything in the right spots |

## Layout — one folder per subject (mirrors the audio bucket)

| Artifact | Where |
|----------|-------|
| Raw source PDF | `papers/<Subject>/…` — **local, gitignored, never uploaded** (it's the master) |
| Baked **question** | R2 `hsc-questions/<subject>/q_<id>.pdf` |
| Baked **answer** | R2 `hsc-questions/<subject>/a_<id>.pdf` — **same `<id>`** as its question |
| Metadata + classification | `content/<subject>/questions.json` (committed); `subject.json` carries `assetBaseUrl` |
| Local baked staging | `papers/_work/<paperId>/baked/` (gitignored, transient) |

`<id>` is `sha256(question-pdf)[:12]` → **non-enumerable** (can't scrape the bucket) and
**auto-deduping** (recycled questions hash to the same id). Question and answer share it, so
`q_<id>` ↔ `a_<id>` are always paired.

## Commands

```bash
python3 tools/index_papers.py                                     # once
python3 tools/render_paper.py "Maths Advanced/HSC-NESA/2020-hsc-mathematics-advanced.pdf"
#   → agent follows tools/prompts/locate_questions.md for the printed paperId
python3 tools/bake_questions.py "<paperId>" --upload hsc-questions
```

One-time R2: `wrangler r2 bucket create hsc-questions`, then enable public access (r2.dev URL
or a custom domain, e.g. `questions.hsc.pebnum.com`) → that becomes the subject's `assetBaseUrl`.

## Not the old approach

The template's `content/<subject>/papers/pN/` system (committed full `paper.pdf` + `mg.pdf` +
**transcribed** `quiz.json`) is the older, text-based, whole-paper-shipped method. This
pipeline deliberately replaces it: **screenshots not text** (no hallucination), full papers
never shipped (anonymised per-question), answers paired.
