# How to select questions

Your goal is to select questions for the paper generator. You draw boxes on the
rendered page; the pipeline crops what you box.

## The one test: does the working flow on?

**One single flow of working = one question.**

If I had a maths question that said "find the derivative of cos(x)", and then "now
find the stationary points" — that is **one** question. The second part only makes
sense because of the first. It flows on.

If the next bit does **not** logically flow on from what came before — new context,
you could answer it without having read the part above — it is a **new** question.

That single test decides everything below.

## Deciding the unit

- **Parts that flow on stay together as ONE unit.** A numbered question with
  connected sub-parts — `(a)` then `(b)` building on it, or roman `(i)/(ii)/(iii)` —
  is one box, one unit. Do not split them.
- **A booklet of independent problems splits into ONE unit PER LETTER.** Some
  "questions" are really a bundle: "Question 11 (15 marks)" holding an unrelated
  (a) evaluate…, (b) simplify…, (c) integrate…, (d) draw a chart. These don't flow
  on from each other — box each letter separately (`q11a`, `q11b`, …).
- **Rule of thumb when unsure:** under 10 marks → almost always one whole unit.
  ≥ 2 independent lettered parts **and** ≥ 10 marks → split per letter.
- **Roman sub-parts `(i)/(ii)` always fold into their letter parent** — they share
  context. Only treat `(i)` as a new letter if the part before it was `(h)`.

## Two boxes per question

For each question you draw **two** boxes:

1. **The question box** — the question number/heading down to the end of its
   content *and* its answer space (the ruled lines or the blank writing gap).
2. **A lines box** — a tight box around just the ruled-lines / writing-space block.

Why the lines box matters: the pipeline strips the writing space out of the crop and
records how much space there was. That lets the generator re-add clean lines for a
"write on it" paper, **or** leave them off for a compact study copy. No lines box →
the generator can't size the writing space. If a question has no ruled lines (just a
blank gap), still draw the lines box around that gap.

## DO

- Just select the text and lines of working.
- Box from the question number down to the end of the answer space.
- Draw the separate lines box around the writing space.
- Split a ≥10-mark booklet into one box per independent letter.
- Read the marks from "(N marks)" in the heading or the bare digit in the right
  margin — never guess.

## DON'T

- **Don't split up a question that flows on** — connected parts stay as one unit.
- **Don't ship a whole 15-mark booklet as one giant box** — split its letters.
- **Don't include page numbers** ("- 7 -"), "Please turn over", "Question 11
  continues on next page", or "End of paper". That is page furniture, never content.
- **Don't include the "Question X" heading in a split letter box** — the heading and
  shared stimulus belong to the bundle, not to each letter crop.
- **Don't include the margins.**
- **Don't box worked solutions / marking pages** at the back of "w. sol." papers.
- **Don't leave trailing whitespace** — the box ends at the last content or at the
  top of the ruled lines, not at the next heading.
- **Don't box a "(continued)" page of blank lines as its own question** — it folds
  into the whole question it continues.
- **Delete generic spare-working pages entirely.** Papers often leave blank ruled
  pages that belong to no specific question — "If you need more space for any
  question, use this page", "Extra writing space", a blank sheet between sections.
  They are not a question and not any question's writing space. Don't box them, don't
  fold them into a neighbour — drop them completely.
