# Parser pipeline rebuild (Gen 3) — architecture plan

> Status: **Plan, approved-in-principle.** Target: reliable, repeatable, near-100%-
> accurate question extraction at scale (hundreds of papers, many subjects).
> Supersedes the Gen 1 `tools/prompts/` workflow.

## Two structural principles (everything follows from these)

### 1. Metadata is the source of truth; crops are cache
Do **not** physically cut per-question PDFs as a pipeline stage. Instead:

- The immutable inputs are the rendered page images (pinned DPI/zoom — the image bytes
  are part of the cache key).
- Truth is a stack of layered metadata in **original paper coordinates** (page index +
  PDF points): `split.json` → `mask.json` → `tags.json` → `_corrections.jsonl` overlay.
- The oversized per-question PDF you wanted still exists — but it's a **deterministic
  bake of `split.json`**, not something an agent authors. A wrong split is fixed by
  editing one JSON record and rebaking; there are no downstream artifacts to chase.
- Mask regions are stored in paper coordinates too, so re-splitting never invalidates
  masks. Corrections stay append-only and beat AI at compile time (existing pattern).

### 2. The LLM chooses; it never draws
Measured: an LLM drawing boxes cold gets ~0.90 IoU on questions, ~0.74 on lines.
Continuous pixel outputs are never repeatable; discrete outputs can be exactly right and
exactly repeatable. So:

- A deterministic **over-segmentation** pass splits every page into typed, ID'd blocks:
  `heading`, `text`, `figure`, `ruled-lines`, `mc-options`, `furniture`. Uses the text
  layer + whitespace-valley detection + existing `detect_lines.py`.
- **SPLIT becomes an assignment problem**: assign each block to a question-unit (or to
  `FURNITURE` / `SPARE-WORKING` / `SOLUTIONS`). Same blocks in → same assignment out.
- **MASK becomes a labeling problem**: label each block in a unit `content` /
  `writing-space` / `dead-space` / `answer-structure`. Mostly deterministic; the LLM
  arbitrates only ambiguous blocks.
- Where vision must still draw (scans with no text layer), **snap** its boxes to the
  nearest block edge / whitespace valley. Snapping turns 0.90-IoU proposals into exact,
  stable boundaries.

## Where each decision lives

| Decision | Owner |
|---|---|
| Render / DPI / page images | Deterministic (pinned forever) |
| Block over-segmentation | Deterministic (text layer; OCR fallback) |
| Furniture detection ("- 7 -", "Please turn over", "End of paper") | Deterministic regex + position |
| Marks ("(N marks)", NESA right-margin digit x/W≈0.87) | Deterministic; LLM only confirms |
| Ruled-line geometry / `spaceHeight` | Deterministic (`detect_lines.py`) — vision never measures |
| "Is this one flow of working?" unit grouping | Deterministic default (<10 marks = whole; ≥2 letters AND ≥10 marks = split); **borderline 8–12-mark multi-letter → LLM/human** |
| Odd layouts, scans, garbled fonts | LLM vision (block-assignment, snapped) |
| Crop QA (clipped/merged/complete) | LLM funnel + deterministic invariants |
| Syllabus tagging (closed vocab) | LLM |
| Any gate failure / borderline / low confidence / audit | Human |

Vision is worth its cost only when the decision needs *meaning* (does (b) depend on (a);
is this diagram clipped). Never for anything a pixel histogram or regex can measure.

## Verification: four independent layers (independence is what gets you to ~100%)

- **L0 — deterministic invariants (free, always on):** numbering continuity + no dupes;
  count vs `syllabus.json` sections; **marks conservation** (extracted marks per section
  = printed section total — the single strongest, cheapest split-error detector);
  cross-check vs marking guideline; **page-coverage round-trip** (units+masks+furniture
  cover every page; "orphan ink" outside all regions on a content page → fail); schema +
  vocab (`validate_pipeline.py --strict`).
- **L1 — model funnel, made symmetric:** Haiku scans every crop; **Sonnet re-checks both
  Haiku's passes AND its fails** (today's funnel never rescues a Haiku false-fail — that
  floods the human queue at scale); Opus arbitrates disagreements + final-reviews/tags
  survivors (never bulk-scans — preserves the cost funnel).
- **L2 — adversarial verifier:** a *separate* prompt that sees only the crop + claimed
  metadata (never the producer's reasoning) and runs a falsification checklist: text
  clipped at any of 4 edges? two question numbers visible? marks printed vs claimed?
  lines region present when spaceHeight > 0?
- **L3 — human, targeted:** every gate failure; every borderline-rule firing; confidence
  < 0.7; **plus a random 3–5% audit of "clean" output** (the only true measure of
  residual error; every miss becomes a regression case). Hold measured error < 0.5%/question.

## Regression / ground-truth harness (build this BEFORE touching prompts)

- Freeze human annotations (ACE 2021, 2024 NESA to start) as `papers/_goldset/<paperId>/`:
  expected units, boxes, marks, spaceHeight, mask regions. Grow to 15–20 papers,
  stratified by layout family (born-digital NESA, scanned trial, booklet, lines-heavy,
  MC-heavy) and subject. **Every production correction + audit miss auto-joins the gold set.**
- `tools/regress.py`: run the pipeline on the gold set, emit a scorecard, exit non-zero on
  any hard-bar breach. Cache deterministic + unchanged-prompt LLM stages so a docs-only
  change is ~free to verify.
- **Hard bars:** unit count + 1:1 identity 100% exact; post-snap boundary error ≤ 4pt;
  marks 100% exact where printed + conservation holds; spaceHeight ±6pt; furniture leakage
  = 0; 3-run stability (identical unit structure).
- **Process rule:** no spec/prompt/examples edit lands without a green regress run.

## Failure handling at scale

- **Idempotency via stamps:** every stage writes `{input hashes, prompt hash, model ID,
  tool version}`; rerun skips when stamps match; outputs are superseded, never mutated.
- **Paper state machine:** `rendered → segmented → masked → qa'd → tagged → published`,
  plus `halted:<stage>:<reason>`. Halt-don't-advance stays absolute.
- **Batch tripwires (orchestrator-level):** stop the whole batch if >20% of papers halt,
  crop-QA fail >5%, or an invariant fails on ≥3 papers with the same signature — that's a
  systematic rule bug, not paper noise. This is what stops "one bad rule mis-crops thousands."
- **Per-subject canary:** 2 papers end-to-end through human review before fan-out.
- **Republish gate:** a rule/prompt change never auto-rebakes published questions; requires
  green regress + a boundary-diff report + explicit human ack.

## File layout (rules live in exactly ONE place)

```
.claude/skills/parse-papers/
  SKILL.md          # orchestrator ONLY: stage order, gates, thresholds, model routing,
                    #   batching, tripwires, escalation. ZERO segmentation rules.
  SPLIT.md          # canonical spec: numbered rules S1..Sn. Read by humans AND injected
                    #   verbatim into the split agent. (how_to_select_questions.md folds in here.)
  MASK.md           # canonical spec: rules M1..Mn incl. region taxonomy.
  EXAMPLES.md       # shared ground truth: examples/counterexamples keyed to rule IDs.
                    #   Every production bug becomes a named counterexample.
  prompts/
    split-agent.md  # thin wrapper: role, I/O schema, block-assignment procedure,
                    #   self-checks, "cite rule IDs". Includes SPLIT.md + EXAMPLES.md by ref.
    mask-agent.md   # same shape.
    qa-verifier.md  # the adversarial checklist (a distinct prompt).
tools/schemas/      # machine contracts — referenced, never duplicated.
papers/_goldset/    # frozen human annotations + regress.py manifest + the bars.
```

The failure mode of the "1 spec + 1 prompt" split is **rule drift** — rules edited in one,
not the other. Fix: the spec IS the rulebook for both audiences; the agent prompt is a thin
wrapper the orchestrator concatenates with spec + examples at spawn time.

## Mask taxonomy — four regions, not three

`content` (keep always) · `writing-space` (re-rule for non-compact, drop for compact) ·
`dead-space` (always drop) · **`answer-structure`** (grids, tables-to-complete, number
planes, MC bubbles — writing space you KEEP in both modes and never re-rule over). The
shared booklet heading/stimulus is a distinct region owned by the bundle, not any letter.

## Ordered implementation plan

1. **Metadata-first split**: define `split.json` (paper coords + rule-ID audit field);
   per-question PDF becomes a pure bake of it. Fold in `boxes_to_boundaries.py`; delete
   `extract_boxes.py`.
2. **Deterministic block over-segmentation** (extend textlayer/OCR + `detect_lines.py`
   into typed, ID'd blocks).
3. **Deterministic invariants suite** (marks conservation, numbering, coverage/orphan-ink)
   — gate every paper from day one.
4. **Regression harness** (`tools/regress.py` + `_goldset/` from the two annotated papers).
5. **Rewrite SPLIT agent** as snapped block-assignment; iterate against the harness to 100%
   unit identity on gold.
6. **MASK**: derive regions deterministically; LLM arbitration for ambiguous only; add
   `answer-structure`.
7. **Restructure QA funnel** (symmetric re-checks, Opus arbitration, adversarial verifier,
   0.7 confidence routing).
8. **Consolidate docs** (layout above); delete Gen 1 artifacts.
9. **Orchestrator hardening**: stamps/caching/state machine/tripwires/republish gate.
10. **Scale process**: per-subject canary, 3–5% audit, corrections→gold flywheel; expand
    gold set to 15–20 stratified papers.

**Steps 1–4 are almost entirely deterministic Python and come before any prompt work** —
they do more for the "last 10%" than any prompt engineering.
