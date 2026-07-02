Task: Initialise a freshly-copied subject folder — turn the generic template into THIS subject.

You run this **once**, right after copying the generic template:

```
cp -r content/_template-subject content/<your-subject-slug>
```

Your job is to **edit the duplicated files in place** so the folder stops being generic and
becomes specific to one HSC subject. You fill in `subject.json` and adapt the subject-specific
placeholders in the copied docs. You do **not** write plans, scripts, quizzes, or audio — those
are the later pipeline stages. Do exactly this initialisation, then stop.

Working root: the new subject folder you're initialising (e.g. `content/<subject>/`).

## Step 0 — Establish the subject's identity
Get these from the user if not already obvious, or infer them from the **syllabus** in
`resources/` (so dump the syllabus there first — see `resources/README.md`):
- **slug** — the folder name / URL id (lowercase, hyphenated), e.g. `chemistry`, `biology`,
  `maths-ext1`. It's also the audio R2 key prefix.
- **full name** — e.g. "HSC Chemistry"; **short name** — e.g. "Chemistry".
- **module structure** — the syllabus modules, each with a short **code** you'll use in episode
  folder names (e.g. `M1`…`M8`, or syllabus-native codes like `IQ1`), its human **title**, and
  which **HSC year** (11 or 12) it belongs to. Read the syllabus's module list; don't invent it.

If the syllabus isn't in `resources/` yet, ask the user for the module list (codes, titles,
years) before continuing — everything keys off it.

## Step 1 — Fill in `subject.json`
Edit `subject.json`:
- `id` = slug · `name` = full name · `shortName` = short name · `description`.
- `repoUrl` = this repo's URL.
- `audioBaseUrl` = this subject's public audio origin (its R2 bucket's custom domain),
  e.g. `https://audio.<slug>.pebnum.com`. Use `"content"` if serving audio locally for now.
- `groupNames` = **every module code → its title**, plus `"CASE": "Case Studies"`.
- `yearMap` = every module code → `"Year 11"` or `"Year 12"`, plus `"CASE": "Case Studies"`.
- `yearOrder` = keep the default unless this subject needs a different section order.
- **Delete the `_comments` block.**
Then validate: `python3 -c "import json;json.load(open('subject.json'));print('ok')"`.

## Step 2 — Specialise the placeholders in the copied docs
The copied files carry generic placeholders and another subject's examples. Adapt the
**subject-specific** parts (leave the generic format rules alone):
- `_plans/README.md` — replace the placeholder module list under "Modules" with this subject's
  real modules (code · title · year), matching `subject.json`.
- `pipeline/STYLE.md` — wherever it pins down **module codes / naming** for a specific subject
  (e.g. its "module codes" section), rewrite that to this subject's codes from `subject.json`.
  Do **not** rewrite the teaching-style rules themselves — those are binding and subject-agnostic.
- Any remaining literal `REPLACE-ME` / another-subject example that names the wrong subject in
  `README.md`, `resources/README.md`, or `_plans/README.md` — fix it to this subject.
- `_example-episode/` is a **cross-subject format reference** (it may be from another subject).
  Leave its content as-is — it shows the file *format and depth*, not this subject's material.
  Just confirm `_example-episode/NOTE.md` makes that clear.

Don't touch `AUTHORING.md`, `SUPPLEMENTARY.md`, `QUIZ_STYLE_GUIDE.md`,
`CASE_STUDY_LESSON_PLAN.md` beyond fixing a stray wrong-subject example — they're generic.

## Step 3 — Sanity check, then commit
- `subject.json` is valid and has no `_comments` block.
- Every code in `groupNames` also appears in `yearMap` (and vice versa), `CASE` included.
- No `REPLACE-ME` strings remain anywhere in the subject folder:
  `grep -rn "REPLACE-ME" content/<slug> || echo "clean"`.
Then one commit, e.g. `<slug>: initialise subject from template`. End with the co-author
trailer the harness specifies. Don't push unless asked.

## Step 4 — Report + hand off
State: the slug/name, the module table you wrote (code · title · year), and what you adapted.
Then point to the next stages, in order:
1. **Get content** — finish dumping sources into `resources/` (syllabus + textbook extracts).
2. **`GENERATE_PLAN_PROMPT.md`** — write the per-module plans.
3. **Start `./generate_all_voices.sh --daemon`** — the voice daemon (renders audio in parallel).
4. **`GENERATE_EPISODE_PROMPT.md`** — write the scripts.
5. **`GENERATE_QUIZ_PROMPT.md`** — write the quizzes.

Do the initialisation, not a description of one. Stop after Step 4 — don't start writing plans.
