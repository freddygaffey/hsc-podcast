# Structure guide — Mathematics Advanced

> Per-subject knowledge for the segmentation + solution agents. This describes how a Maths
> Advanced paper is built, what counts as one unit, and how to tell whether parts are linked.
> The agent reads this **alongside** the generic geometry/process rules in its prompt; those
> rules are subject-agnostic, everything specific to this subject lives here. To add a new
> subject, write its own `content/<subject>/structure-guide.md` — no code or prompt change.

Companions: `parse-rules.json` (machine layout knobs — margins, option letters, furniture
regex), `syllabus.json` (section counts + marks), `solution-style-guide.md` (how solutions render).

## Paper shape

- **Section I — Multiple choice.** Questions **1–10**, 1 mark each, **10 marks** total. Printed
  on the cover as "Section I – 10 marks (pages a–b)" / "Attempt Questions 1–10". Answered on a
  separate MC sheet. Each question = a stem (often with a graph/diagram/table) + **exactly four
  options A, B, C, D**. No writing space.
- **Section II — Long response.** Questions **11 onward** (11–31, 11–32, or as few as 11–16 in
  older "6 big questions" papers), **90 marks** total. Usually a separate "Answer Booklet" with
  a "Question N (X marks)" heading, lettered parts (a), (b)(i)… and **ruled working lines** under
  each part. One question per page or a few; long questions continue across pages
  ("Question N continues on the next page").
- **Marks conserve:** Section I sums to 10, Section II to 90, whole paper 100. This is the single
  strongest correctness check.

## What counts as one unit

- **One unit = one whole question** a student attempts as a self-contained problem.
- **MC (Section I):** one unit per question, box holds the stem + all four options.
- **Section II:** one unit per "Question N" — the whole question **including all its lettered
  parts and their working space**. Do **not** split lettered parts into separate units.

## Are the parts linked? (the granularity judgement)

A question's parts are usually a chain of reasoning, so they stay together as one unit. Even so,
recognising the linkage matters for tagging and for never serving a part without its setup. Cues
that part (b) **depends on** an earlier part — keep welded, never separate:

- **"Hence"** or **"Hence, or otherwise"** — the intended method uses the previous result.
- **"Hint:"** — usually points back to earlier working.
- **"Using the result in part (a)…"**, "from part (i)", "the value found above".
- A function, diagram, table or scenario **defined once** in the stem/earlier part and reused.

When parts share none of these and each stands alone, they *could* be independent — but the safe
default is **keep the question together**; over-grouping is coarse, over-splitting produces a
broken, unanswerable item. When in doubt, do not split.

## Furniture (never a question) — Maths Advanced specifics

Cover page; "Reading time / Working time"; "General Instructions"; "Section I/II" banners;
"Attempt Questions…"; "Use the multiple-choice answer sheet"; **Student Number / Centre Number**
fields at the top of booklet pages; the **reference sheet** at the back; "BLANK PAGE"; page
footers ("– 8 –"); "End of Section I", "End of paper".

## Solutions

Trial papers named **"w-sol" / "with solutions"** append worked solutions after the question
paper (record where they start). They may be a clean typed table (question № · working · MC
letter) or the question paper re-printed with handwritten working. Every question must map to a
solution; gaps are AI-filled and **watermarked** — see `solution-style-guide.md`.
