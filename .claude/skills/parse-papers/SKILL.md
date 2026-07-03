---
name: parse-papers
description: Parse a subject's past papers end-to-end — crop every question to its own PDF with metadata (origin paper, marks, working lines, type, syllabus outcomes), QA the crops through a Haiku→Sonnet→Opus vision funnel, and build the generator manifest. Use when the user wants papers parsed, cropped, ingested, tagged, or swept into the question bank.
argument-hint: <subject> [paperId] [--limit N]
---

# Parse papers: crop + metadata pipeline (per subject)

You orchestrate the deterministic Python pipeline plus an AI vision/classification funnel
for ONE subject per invocation (each subject's papers are formatted differently; the
differences live in `content/<subject>/syllabus.json`, not in this prompt).

Arguments: `$ARGUMENTS` → first token = subject slug (e.g. `dt`, `maths-advanced`);
optional second token = a single paperId to (re)process; `--limit N` caps how many
unprocessed papers to take this run (default 5 — tell the user how many remain).

## 0. Preconditions (STOP if missing)

1. `content/<subject>/syllabus.json` must exist. If missing, STOP and tell the user to
   copy `content/_template-subject/syllabus.json` and fill in the outcome list and type
   taxonomy — offer to draft it from the official syllabus if they give you the outcomes.
   Load it now: the `outcomes[].code` list and `types` list feed the Opus stage verbatim.
   (Subjects whose papers-tree name differs from the content slug are aliased in
   `tools/_subjects.py` SUBJECT_ALIASES, e.g. `design-technology` → `dt`.)
2. `papers/_index.json` must list the subject's PDFs. If the user dropped new files, see
   **Ingesting a content dump** below, then run `python3 tools/index_papers.py`.

## 1. Pick the work

From `papers/_index.json`: entries whose slugged subject (after aliasing) matches, with
`role == "exam"`. Respect `syllabus.json` `minYear` — papers older than it are on a
superseded syllabus and are OUT OF SCOPE (skip them; never count them as remaining work).
A paper is *unprocessed* when `papers/_work/<paperId>/questions.json` does not exist. Respect `--limit`; process papers one at a time (steps 2–4), but you may
run step-4 funnels for paper N while paper N+1 goes through step 2–3.

## 1b. Segmentation convention (READ EXAMPLES.md)

Read `EXAMPLES.md` in this skill folder BEFORE any locate/QA/box-drawing step — it holds
the human ground-truth examples AND counterexamples for what one question-unit is, box
extents, and metadata. When the deterministic locate output looks wrong for a paper
(odd question counts, weird layouts), spawn a VISION segmenter instead: an agent that
Reads the page PNGs and draws boxes per EXAMPLES.md, writing the annotate_app box shape;
score it with `tools/compare_boxes.py` against any available human annotations, or
convert and proceed. The regex locate is only the cheap first pass.

## 2. Deterministic pipeline (per paper)

Run each step; after each, gate with the validator — a failing paper is halted and
reported at the end, never advanced:

```bash
python3 tools/render_paper.py "<paperId>"           # pages → _work/<paperId>/pNN.png + info.json
python3 tools/locate_textlayer.py "<paperId>"       # born-digital papers
python3 tools/locate_ocr.py "<paperId>"             # ONLY if scanned, or textlayer found 0 questions
python3 tools/detect_lines.py "<paperId>"           # working-lines count + trim marks per part
python3 tools/locate_marking.py "<paperId>"         # answer regions from the linked mg PDF
python3 tools/bake_questions.py "<paperId>"         # crops → _work/<paperId>/baked/ + questions.json
#   crops ship WITHOUT their printed ruled writing lines (lineCount metadata lets the
#   generator re-rule clean "standard lined paper" space at export; --keep-lines opts out);
#   continuation line-pages fold into the whole-question crop and emit no fragment records
python3 tools/validate_pipeline.py --strict "<paperId>"
```

Routing rule: `info.json bornDigital: true` → textlayer; if it reports 0 questions
(garbled font encodings) or the paper is scanned → OCR. Sanity-check the locate output
against `syllabus.json` `sections` (e.g. DT = 10 MC + Q11–15): question count wildly off
→ treat as a locate failure, halt the paper.

## 3. Render crops for the funnel

Render every baked crop to PNG (about 1.5x zoom is plenty) into the scratchpad:

```python
import fitz, pathlib
src = pathlib.Path("papers/_work/<paperId>/baked")
out = pathlib.Path("<scratchpad>/crops/<paperId>"); out.mkdir(parents=True, exist_ok=True)
for pdf in src.glob("q*.pdf"):
    d = fitz.open(pdf)
    d[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(out / (pdf.stem + ".png"))
```

## 4. Vision-QA + classification funnel (fixed model mapping)

Batch crops ~20 per agent so context stays sane. Pass each agent the crop PNG paths plus
the record metadata (questionNumber, partLabel, marks, lineCount, type) from
`_work/<paperId>/questions.json`. Run batches in parallel.

| Stage | Model (Agent tool `model:`) | Task |
|---|---|---|
| 1. Bulk QA loop | `haiku` | Look at EVERY crop image. Verdict per crop: `good`, `cut-off` (text/diagram clipped), `wrong-split` (two questions merged / fragment), `bad-marks` (marks in metadata contradict what's printed). One line of reasoning each. |
| 2. Check pass | `sonnet` | Re-check ONLY the crops Haiku passed, same verdict set — demote false passes. |
| 3. Final review + classification | `opus` | Crops passing both: final verdict AND classify — `type` (choose from syllabus.json `types`), `syllabusRefs` (choose ONLY from `outcomes[].code`, usually 1–2), `topic` (short free text), `module` (from `modules` when set), `confidence` 0–1. |

Rules:
- Opus NEVER sees a crop that failed Haiku or Sonnet (that's the cost funnel).
- Every stage returns JSON; you (the orchestrator) merge Opus results into
  `papers/_work/<paperId>/tags.json`:
  `{"paperId": ..., "model": "claude-opus", "ts": <epoch>, "tags": {"q13.pdf": {"syllabusRefs": [...], "type": ..., "topic": ..., "module": ..., "confidence": 0.9, "qaVerdict": "good", "qaStage": "opus"}}}`
- Stage-1/2 failures: append one line per crop to `papers/_work/_review.jsonl` —
  `{"paperId": ..., "assetKey": ..., "verdict": "<cut-off|wrong-split|other-bad>", "ts": <epoch ms>}`
  so the human review UI surfaces them pre-flagged. Map `bad-marks` → `other-bad`.
- Drop any outcome code the model returns that is not in the syllabus list; if that
  leaves none, set `confidence` ≤ 0.4 so the review UI's low-confidence filter catches it.
- Never overwrite an existing `tags.json` entry unless the user asked for a re-tag.
- Validate afterwards: `python3 tools/validate_pipeline.py --strict "<paperId>"`.

## 5. Manifest + handoff

```bash
python3 tools/build_manifest.py        # merges base → tags → human corrections
```

Then report a summary the user can act on:
- papers processed / halted (and why), questions + answer crops baked
- marks coverage, lineCount coverage, tag counts, low-confidence count, QA fail count
- remind: `python3 tools/review_app.py` → filter `low-confidence` / `tag-flagged` /
  `unreviewed` for the human pass; corrections there beat every AI tag at manifest time
- when the user is happy: upload crops with
  `python3 tools/bake_questions.py "<paperId>" --upload hsc-podcast-audio` (or
  `tools/upload_questions.py` for bulk), and make sure the subject is listed in
  `generator.html` `SUBJECTS` and `content/<subject>/subject.json` has `assetBaseUrl`.

## Ingesting a content dump

When the user points at a folder of mixed files instead of an indexed subject:

1. Classify each PDF by filename first, content page 1 only when ambiguous:
   *exam paper* / *marking guideline* (`mg`, "marking", "guidelines", "solutions") /
   *textbook or notes* / *junk*.
2. File papers into the tree the indexer expects:
   `papers/<Subject Name>/<category>/<year>-<slug>.pdf` (categories: `HSC-NESA`,
   `Y12-Trial`, `Y12-Yearly`, `Y11-Yearly`…). Keep an exam and its marking guide in the
   same directory with the same year so `index_papers.py` links them (`mg` in the
   filename marks the guide).
3. `python3 tools/index_papers.py`, then continue from step 1 as normal.
4. **Textbooks are out of scope for this skill** — note them to the user; textbook
   ingestion (chapter split → episode/quiz content via `tools/ingest_textbook.py`) is a
   separate flow to be built on this same pattern later.

## Contract

Every artifact this pipeline writes is schema'd in `tools/schemas/` and checked by
`tools/validate_pipeline.py` (shape + vocabulary + files-on-disk). If you generate JSON
yourself (tags, review lines), it must pass those schemas — run the validator rather than
assuming.
