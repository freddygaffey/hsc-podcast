# Segmentation examples & counterexamples (human ground truth)

Learned from Fred's box annotations (tools/annotate_app.py ground truth on
`maths-advanced-ace-trial-2021-2u-abbotsleigh…` and `maths-advanced-hsc-nesa-2024-hsc-maths-adv`).
Any agent that draws or QAs question boxes MUST follow these. Score any box-producer with
`tools/compare_boxes.py` (box vs box) or `tools/score_annotations.py` (boundaries vs boxes);
iterate the prompt until it matches the human.

## What ONE question-unit is

✅ **A numbered question with connected sub-parts = ONE unit.**
2024 HSC Q14 (4 marks, parts (a) 1m + (b) 3m sharing one context) → one box `q14.pdf`.
Rule of thumb: total marks < 10 → whole question is the unit; parts are metadata only.

✅ **A booklet question bundling INDEPENDENT problems = one unit PER LETTERED PART.**
ACE 2021 "Question 11 (15 marks)" holding unrelated (a) evaluate…, (b) simplify…,
(c) integrate…, (d) Pareto chart → four units `q11a.pdf … q11d.pdf`.
Rule of thumb: ≥ 2 lettered parts AND ≥ 10 marks → split into parts.

✅ **Roman subparts (i)/(ii)/(iii) fold INTO their lettered parent** — they share context.
Only treat `(i)` as a letter when the previous part was `(h)`.

❌ **COUNTEREXAMPLE — don't split connected sub-parts**: 2024 HSC Q14(a)/(b) as two
display units is WRONG (human boxed them as one).
❌ **COUNTEREXAMPLE — don't ship the 15-mark bundle as a unit**: the ACE booklet
"Question 11" as one giant crop is WRONG (human drew four boxes).

## Box extent

✅ From the question number/heading down to the end of its content **and its answer
space** (ruled lines or blank gap) — then the pipeline strips the space out of the crop
and re-renders it at export (`spaceHeight`).
✅ A separate **lines box** tightly around each ruled-lines block gives the stripper its
ground truth (`linesTopY` matched human tops within ~1% of a page on the 2024 HSC).

❌ **COUNTEREXAMPLE — heading in part crops**: booklet part crops must NOT carry the
"Question 11 (15 marks)" heading/stimulus; that belongs to the bundle record.
❌ **COUNTEREXAMPLE — trailing whitespace**: regions used to run to the next heading
(median 18% of a page of blank space in crops). Crops end at content
(`contentBottomY`) or at the ruled block start (`linesTopY`).
❌ **COUNTEREXAMPLE — page furniture**: "- 7 -" page numbers, "Please turn over",
"Question 11 continues on next page", "End of paper" are NEVER content. Referral lines
terminate the region above them (END anchors); footers are clipped from crops.
❌ **COUNTEREXAMPLE — continuation fragments**: "Question 15 (continued)" + a page of
blank lines is NOT its own question. It folds into the whole-question unit and emits no
record. (This was the review items-122-125 bug.)
❌ **COUNTEREXAMPLE — solutions pages**: worked solutions/marking sections at the back
of "w. sol" papers must never produce question units.

## Metadata on each unit

- `marks`: from "(N marks)" in the heading OR the bare digit in the right margin
  (NESA style, x/W ≈ 0.87). Never from guesswork; `marksPrinted` records whether it's
  visible inside the crop.
- `spaceHeight` (points) is the writing-space metric — line COUNTS are not comparable
  across papers (different line gaps); 2024 HSC Q12: human lines box 288pt, machine 288pt.
- Provenance (paper/year/page/marks) is RENDER-time header content, never baked into
  crop bytes.

## Measured agreement (keep these bars)

- ACE 2021 (no lines, booklet): 22/22 human units matched 1:1, bottom overhang ≤ 8.9%.
- 2024 NESA HSC (lines-heavy): 9/9 units, 7/7 lines boxes (trim within 1.1% of a page,
  spaceHeight exact), marks agreement where both set them.
- Opus vision agent drawing boxes cold from this convention: 9/9 questions (median IoU
  0.90), 7/7 lines boxes (median IoU 0.74) vs human on the same pages.
