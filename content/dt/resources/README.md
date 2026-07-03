# resources/ — dump raw source material here

This is the **input** to the plan-generation step. The plan prompt
(`../pipeline/GENERATE_PLAN_PROMPT.md`) reads everything in here, so put the real source
material here, not summaries.

## What to put here

- **Syllabus** — the official NESA syllabus for the subject (PDF or extracted text). This is
  the authority on outcomes, content dot-points, and module structure. Prefer an extracted
  `.txt`/`.md` over a big PDF so the prompt can `grep` it cheaply.
- **Textbook / course notes** — the main teaching text. If it's a large PDF, **extract the
  text first** into `resources/extracted/` (e.g. one `.md`/`.txt` per chapter). Never make
  the prompt open a 30 MB+ PDF — it's slow and expensive; point it at the extracted text.
- **Data / formula / reference sheets** — anything students are given in the exam.
- **Reference links** — a `links.md` listing authoritative URLs (and what each is for).
- **Past papers / marking guidelines** (optional but valuable) — they reveal exam phrasing
  and the verbs that earn marks.

## Suggested layout

```
resources/
  syllabus.pdf                 (or syllabus.md once extracted)
  textbook.pdf                 (keep the original, but ALSO extract it)
  extracted/
    ch01_<topic>.md
    ch02_<topic>.md
    ...
  data-sheet.pdf
  links.md
```

## Notes

- Large binaries (textbook PDFs, data sheets) are typically git-ignored. Keep them locally;
  commit the **extracted** text so the pipeline is reproducible.
- The richer and more exam-accurate the sources, the less the model has to guess — which is
  the whole point of dumping them here rather than relying on its prior knowledge.
