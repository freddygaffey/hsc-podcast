# Past Papers — extract a subject's HSC exams into the app

This turns a subject's past **exam PDFs + marking guidelines** into practisable papers in the app.
Each paper becomes an episode under a synthetic **"Past Papers" (`EXAM`)** module — no app code
changes needed; the manifest discovers `content/<subject>/papers/p<N>/` automatically.

## Folder layout (per subject)

```
content/<subject>/papers/
  p1/   quiz.json  paper.json  paper.pdf  mg.pdf        ← one folder per exam (p1, p2, …)
  p2/   …
  images/   p3-img-1.png …                              ← shared stimulus images (optional)
```

- `quiz.json` — the questions (the app's existing `{questions:[...]}` contract + extras).
- `paper.json` — paper metadata (read by `tools/generate_manifest.py`, not the app).
- `paper.pdf` — a copy of the original exam (offered as a download + bundled into offline saves).
- `mg.pdf` — a copy of the marking guidelines (same).
- Images referenced as a **full repo path**: `content/<subject>/papers/images/p3-img-1.png`.

## subject.json — add the EXAM bucket (once per subject)

```jsonc
"groupNames": { "EXAM": "Past Papers", … },
"yearMap":    { "EXAM": "Past Papers", … },
"yearOrder":  ["Past Papers", "Case Studies", "Year 12", "Year 11", "Other"]   // declare in full
```

## quiz.json schema

```jsonc
{
  "paper": true,
  "year": 2024,
  "title": "2024 HSC — <Subject>",
  "time": { "reading": 5, "working": 90, "sections": { "I": 15, "II": 35, "III": 40 } },
  "questions": [
    { "id": "<subj>-2024-q01", "type": "mc", "qNo": 1, "marks": 1, "year": 2024, "section": "I",
      "topic": "...", "outcome": "H1.1", "verb": "identify",
      "q": "…", "options": ["…","…","…","…"], "answer": 2,        // index, FROM the MG key
      "explanation": "AI-written, accurate, syllabus-grounded — 1–2 sentences." },
    { "id": "<subj>-2024-q15", "type": "extended", "qNo": 15, "marks": 15, "year": 2024, "section": "III",
      "topic": "...", "outcome": "...", "verb": "assess",
      "q": "…(include any stimulus table as text; image via \"image\": \"content/<subj>/papers/images/…\")",
      "options": null, "answer": null,
      "criteria": [ { "marks": "13–15", "descriptor": "…verbatim from the marking guidelines…" }, … ],
      "modelAnswer": "concise, adapted from the MG sample answer (or null)" }
  ]
}
```

`type`: `mc` | `short` (≤4 marks) | `extended` (≥5). Multi-part questions → one object per part,
same `qNo`, with a `"part": "a"` field. `paper.json`:

```jsonc
{ "paper": "p1", "year": 2024, "title": "2024 HSC <Subject>", "subject": "<subj>", "examName": "HSC",
  "totalMarks": 40, "source": { "exam": "resources/.../exam.pdf", "markingGuidelines": "resources/.../mg.pdf" } }
```

## The master extraction prompt (run ONE agent per paper)

Fan out one agent per exam (they're independent). Fill the **«fields»**:

> Extract ONE past HSC «Subject» exam into the app's paper format. Accuracy is critical — students rely on this.
>
> PAPER: «year» HSC «Subject» → p-number «pN».
> OUTPUT FOLDER: `content/«subject»/papers/«pN»/` (create it).
> EXAM PDF: «exam path».  MARKING GUIDELINES PDF: «mg path».
> FORMAT REFERENCE — read and match EXACTLY: an existing `content/«subject»/papers/p1/quiz.json` and `paper.json` (or this doc's schema).
> SYLLABUS (ground explanations): `content/«subject»/resources/extracted/syllabus.md`.
>
> Older papers may DIFFER (number of MC, sections, marks, times, and the MG answer-key format). Reflect the REAL structure of THIS paper. NEVER guess an answer.
>
> 1. `pdftotext -layout "<exam>" -` and `pdftotext -layout "<mg>" -`.
> 2. Multiple choice: capture each stem + options A–D verbatim. The CORRECT answer comes from the MARKING-GUIDELINES answer key (A→0,B→1,C→2,D→3). Flag any unreadable key — do not guess.
> 3. Each MC: write a 1–2 sentence `explanation` (why right; why the main distractor is wrong) in accurate subject/syllabus terms. Your words, not the MG's.
> 4. Written questions: exact text, marks, section. Copy the MG marking-criteria bands into `criteria:[{marks,descriptor}]` faithfully. `type` short/extended by marks. `modelAnswer` = concise adaptation of the MG sample answer, else null. Parts (a)/(b) → one object per part sharing `qNo` with a `part` field.
> 5. From the exam cover read reading/working/per-section minutes → `time:{reading,working,sections:{…}}`. Tag each question `section`.
> 6. Write `quiz.json` + `paper.json` (schema above). Question ids `«subj»-«year»-qNN`.
> 7. `cp "<exam>" content/«subject»/papers/«pN»/paper.pdf` and `cp "<mg>" content/«subject»/papers/«pN»/mg.pdf`.
> 8. Validate both JSON files parse.
> RETURN: # MC + # written, total marks, the MC answer letters in order, and any low-confidence items.

## After extraction — QC, build, deploy

1. **Verify answer keys deterministically** — re-extract each MG answer-key table and diff against
   `quiz.json` answers (catches any index slip). A wrong MC answer is the one unacceptable error.
2. Confirm every `quiz.json`/`paper.json` parses and the schema matches.
3. `python3 tools/generate_manifest.py` → the EXAM module appears with one episode per paper
   (newest first; `papers/images/` ignored; `paper.pdf`/`mg.pdf` surfaced as `pdfPath`/`mgPdfPath`).
4. Deploy (`deploy.sh` ships `quiz.json`, `paper.json`, `paper.pdf`, `mg.pdf`, images; never audio).

## Provenance (important)

The **answer key + marking criteria are official (NESA marking guidelines)**; the **MC explanations
and written model answers are AI-authored** and labelled as such in the UI ("Answer from the official
NESA marking guidelines · explanation written by AI"). Keep that split honest.
