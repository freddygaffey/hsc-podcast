# Driver — process ALL papers into the per-subject question bank

Batch-runs the whole pipeline over `papers/_index.json` and drops everything in the right
spots: baked question+answer PDFs to R2 under `<subject>/`, metadata to
`content/<subject>/questions.json`. Vision is Claude Code (Max) — no API key.

Hand this to a fresh Claude Code session, or run it as a Workflow (recommended for scale —
fan out one locate-agent per paper). **Validate on one paper first** before unleashing on
hundreds — one bad locate rule mis-crops thousands of questions.

## Inputs / scope

- `papers/_index.json` (from `tools/index_papers.py`) lists every paper with `paperId`,
  `subject`, `kind`, `role`, `path`. Process the `role == "exam"` entries.
- Filter to a subject to start, e.g. only `subject == "Maths Advanced"`, or `kind == "hsc"`.

## Per paper (idempotent — skip if `content/<subject>/questions.json` already has its records)

1. **Render:** `python3 tools/render_paper.py "<path>"` → note the printed `paperId`.
2. **Locate + classify:** follow `tools/prompts/locate_questions.md` exactly for that paperId.
   Read every `papers/_work/<paperId>/pNN.png`, write `boundaries.json` for the whole paper —
   every question, every letter part, with **type + topic classification** and, wherever the
   worked solution/marking guide is visible, the part's **`markingRegions`** (so its answer
   gets baked and paired).
3. **Bake + upload:** `python3 tools/bake_questions.py "<paperId>" --upload hsc-questions`.
   This writes `q_<id>.pdf` (+ `a_<id>.pdf` where an answer exists) under the subject folder in
   R2, and appends records to `content/<subject>/questions.json`.

## Where everything lands (the "right spots")

| Artifact | Location |
|----------|----------|
| Raw source PDF | `papers/<Subject>/…` — **local, gitignored, never uploaded** |
| Baked question | R2 `hsc-questions/<subject>/q_<id>.pdf` (+ mirror in `papers/_work/<paperId>/baked/`) |
| Baked answer | R2 `hsc-questions/<subject>/a_<id>.pdf` — same `<id>` as its question |
| Metadata / classification | `content/<subject>/questions.json` (committed) |

## Scaling as a Workflow

Fan out step 2 (locate) as one agent per paper — they're independent — then run step 3
deterministically over the results. Keep a running tally of papers done and, per subject,
merge each paper's records into `content/<subject>/questions.json`. Log anything skipped
(e.g. scanned papers that segmented poorly) — never silently drop papers.
