# Structure guide — Mathematics Extension 1

> Per-subject knowledge for the segmentation + solution agents (read alongside the generic
> geometry/process rules in the prompt). To add a subject, write its own guide — no code change.
> Companions: `parse-rules.json` (layout knobs), `syllabus.json` (section counts + marks),
> `../maths-advanced/solution-style-guide.md` (how solutions render).

## Paper shape (verified on the corpus)

- **70 marks total** (NOT 100 — this is the biggest difference from Maths Advanced).
- **Section I — Multiple choice.** Questions **1–10**, 1 mark each, **10 marks**, ~pages 2–4.
  Printed on the cover as "Section I – 10 marks (pages 2–4) / Attempt Questions 1–10". Each MC
  question = a stem (often with a diagram) + **exactly four options A, B, C, D**. No writing space.
- **Section II — Long response.** Only **FOUR** questions: **11, 12, 13, 14**, each worth
  **15 marks**, **60 marks** total, ~pages 5–9. Cover says "Section II – 60 marks / Attempt
  Questions 11–14". Each question **starts on a new page** — its heading reads
  **"Question N (15 marks) Start a new page"**.
- **Marks conserve:** Section I = 10, Section II = 60, whole paper = 70.

## What counts as one unit

- **MC (Section I):** one unit per question, box holds the stem + all four options.
- **Section II:** one unit per **whole "Question N"** (11, 12, 13, 14) — the ENTIRE question
  including *all* its nested parts. **Do NOT split parts into separate units.** These questions are
  large and **span multiple pages**; a unit therefore has several regions (one per page it covers),
  from its "Question N (15 marks)" heading to just before the next "Question N+1" heading (or the
  end of Section II). Expect ~4 Section II units, each multi-page.

## Nesting & linkage (the Extension-1 specific bit)

Section II questions are **deeply nested**: parts **(a), (b), (c), (d), (e)** each with roman
sub-parts **(i), (ii), (iii)**. Per-part marks are printed in the **right margin** (x ≈ 0.87);
the question total is in the heading. The sub-parts are **heavily linked** — this is the norm, not
the exception:

- **"Hence"**, **"Hence, or otherwise"**, **"Hence noting that …"** — the intended method uses the
  previous sub-part's result (e.g. c(ii) "Hence, or otherwise, solve …" depends on c(i) "Show that …").
- A quantity/diagram defined in part (a) and reused in (b),(c)…

Because of this, **always keep the whole Question N together as one unit** — never serve a sub-part
without the parts it depends on. (Same principle as Advanced, but linkage is much denser here.)

## Furniture (never a question)

Cover; "Reading time / Working time"; "General Instructions"; "In Questions 11–14, show relevant
mathematical reasoning"; "Section I/II" banners; "Attempt Questions …"; **Student Name / Maths
class** fields; the **reference sheet** at the back; "BLANK PAGE"; page footers ("6 | Page"); the
"Start a new page" tail of a heading is part of the question heading, not separate furniture.

## Solutions

Trial papers named **"w-sol"** append worked solutions after the paper. Match each whole Section II
question (Q11–14) and each MC question to its solution. Gaps → human review (or AI-fill for
no-solution papers), per `../maths-advanced/solution-coverage` rules.
