# Master prompt — LOCATE questions in a rendered past paper

You are the **locate** step of the past-paper segmentation pipeline. Given the rendered page
images of ONE exam paper, produce a `boundaries.json` that says **where every question and
part is**, so deterministic code can crop them. **You do NOT transcribe questions** — you only
locate and label. The pixels are cropped from the original PDF later; never retype content.

## Inputs (already on disk for the paper you're given)

- `papers/_work/<paperId>/info.json` — page list, page sizes, `bornDigital` flag.
- `papers/_work/<paperId>/pNN.png` — one image per page (150 dpi, upright, top-left origin).

## Steps

1. Read `info.json` to get the page list (`pages[].page` is the 0-based index to use).
2. Read **every** page image (`Read` each `pNN.png`).
3. Identify each question, its parts, marks, type, and topic.
4. Write `papers/_work/<paperId>/boundaries.json` in the schema below. Output the file only —
   no commentary. Ensure it parses as JSON.

## Coordinates

- Each region: `"bbox": [x0, y0, x1, y1]` — **normalised 0–1, top-left origin**, relative to
  the page image the region sits on. `"page"` = the 0-based page index from `info.json`.
- Be **generous**: include the full question text, every diagram/graph/table, the marks digit
  in the right margin, and answer space — but do **not** overlap the next question. Pad ~1%.
- A part that spans a page break → give it two regions, one per page.

## Granularity (strict — this is the product rule)

- The **atomic unit is a LETTER PART** — `(a)`, `(b)`, `(c)`. Each is one entry in `parts`.
- **Roman sub-parts `(i)`, `(ii)` stay BUNDLED** inside their letter part's region — never
  split them out.
- The **top-level question is a metadata group**. Put its shared stem / intro / stimulus (the
  text or diagram every part needs) in `stimulus`; it is attached to every part automatically.
- A question with **no letter parts** (a Section I multiple-choice question, or a plain
  "Question 5 (3 marks)") → one part with `"label": null` covering the whole question.

## Field rules

- **Multiple choice (Section I):** each numbered MC question is its own `question` with a
  single `null`-label part; the region covers the stem **and** all options A–D; `"type":"mc"`.
- **Marks:** read the value printed in the right margin for each part → that part's `"marks"`.
  The question's `"marks"` = the printed total (e.g. "Question 14 (5 marks)" → 5).
- **type** (per part): one of `mc` | `short` | `extended` | `calculation` | `worked`.
- **topic:** the maths syllabus topic, best-effort (e.g. "Probability",
  "Calculus — Integration", "Trigonometry", "Financial Mathematics").
- **Skip** non-question pages: cover, instructions, formula/reference sheet, blank pages, and
  the "Office Use Only" footer strip.
- **Marking guidelines:** if this paper bundles worked solutions / a marking guide (its
  filename had "w. sol." or a sibling `-mg`) and you can see the marking region for a part on
  these pages, add it to that part's `markingRegions`. Otherwise omit the field.

## Output schema

```jsonc
{
  "paperId": "<paperId>",
  "questions": [
    {
      "number": "14",
      "marks": 5,                       // printed total for the question
      "topic": "Probability",
      "stimulus": [ { "page": 12, "bbox": [0.11, 0.08, 0.86, 0.24] } ],  // [] if none
      "parts": [
        {
          "label": "a",                 // "a" | "b" | ... | null (no letter parts)
          "marks": 2,
          "type": "short",
          "regions": [ { "page": 12, "bbox": [0.11, 0.25, 0.86, 0.53] } ],
          "markingRegions": []          // optional; omit if no guideline visible
        }
      ]
    }
  ]
}
```

## Quality bar

- Every printed question and part accounted for; none merged, none dropped.
- No region clips a diagram, a marks digit, or the last line of a part.
- When unsure whether something is stem-vs-part, put shared context in `stimulus`.
