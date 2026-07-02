# `_template-subject` — add a new HSC subject

Copy this whole folder to create a new subject. The leading `_` keeps it out of the
manifest scan, so the template itself never appears in the app.

```
cp -r content/_template-subject content/<your-subject-slug>
```

Then work through the pipeline below. Everything you need is **inside this folder** —
the format contracts and the generation prompts live in `pipeline/`. This template is
generic; `INIT_SUBJECT_PROMPT.md` edits the copy to make it subject-specific.

```
<your-subject>/
  subject.json        ← config (filled in by INIT_SUBJECT_PROMPT from the syllabus)
  resources/          ← dump raw sources here (syllabus, textbook, data sheets, links)
  _plans/             ← per-module episode plans land here  (pipeline step 3)
  pipeline/           ← the runbook + prompts + format contracts (self-contained)
    README.md
    INIT_SUBJECT_PROMPT.md        step 2: specialise the copied files → this subject
    GENERATE_PLAN_PROMPT.md       step 3: resources  → _plans/
    GENERATE_EPISODE_PROMPT.md    step 5: _plans/     → episode scripts
    GENERATE_QUIZ_PROMPT.md       step 6: scripts     → quiz.json
    AUTHORING.md  STYLE.md  SUPPLEMENTARY.md  QUIZ_STYLE_GUIDE.md  CASE_STUDY_LESSON_PLAN.md
  _example-episode/   ← a finished gold-standard episode to copy depth/voice/format from
  <MODULE-LL-Title>/  ← episode folders get created here by step 5
```

## The pipeline, in order

The shape is **plans → scripts**, with **audio rendering in parallel** the whole time (a
daemon, not a blocking gate) and **quizzes** authored from the scripts alongside it. Each
prompt does one unit of work per run and loops until its stage is done.

0. **Copy the template** — `cp -r content/_template-subject content/<your-subject-slug>`. The
   template itself stays generic; everything below specialises the copy.

1. **Get the content** — drop the syllabus, textbook/extracts, data sheets, and any reference
   links into `resources/` (see `resources/README.md`). Everything downstream is built from
   these sources, so gather the real material here first — the syllabus especially, since the
   next step reads it to discover the modules.

2. **Initialise the subject** — run `pipeline/INIT_SUBJECT_PROMPT.md`. It reads the syllabus and
   **edits the copied files** to make them subject-specific: fills in `subject.json` (id, name,
   module codes → titles, Year 11/12 split, `audioBaseUrl`) and adapts the placeholders in the
   docs. After this the folder is no longer generic.

3. **Make the plans** — run `pipeline/GENERATE_PLAN_PROMPT.md`. It reads `resources/` and the
   syllabus and writes one `_plans/<MODULE>-PODCAST_PLAN.md` per module: the episode list,
   dot-points, recaps, interleaving, mnemonics, and a case-study list. The spine of the course.

4. **Start the voice daemon** (you do this, once) — in a terminal, run
   `CONTENT_DIR=content/<subject> ./generate_all_voices.sh --daemon`. It watches `content/` and renders
   each script's `<voice>.m4a` files **as soon as they're written**, so audio is produced in
   parallel with authoring instead of in a stop-the-world batch. Leave it running; it needs the
   local TTS environment. (You can also do a one-off pass any time with `./generate_all_voices.sh --once`.)

5. **Make the episodes** — run `pipeline/GENERATE_EPISODE_PROMPT.md` on a loop. Each run writes
   ONE episode's `script.md` + `supplementary.md`, then stops; the daemon from step 4 renders
   its audio behind it. **No quizzes yet.** Loops until every planned script exists.

6. **Generate the quizzes** — run `pipeline/GENERATE_QUIZ_PROMPT.md` on a loop. Each run writes
   ONE episode's `quiz.json` from its finished `script.md`, then stops. Quizzes don't depend on
   the audio, so this can run as soon as scripts exist (even while the daemon is still
   rendering). Loops until `QUIZZES COMPLETE`.

7. **Build the manifest** — `python3 tools/generate_manifest.py` rescans `content/` and
   regenerates `manifest.json` so the new subject + episodes + quizzes appear in the app.
   (Tip: run `python3 tools/watch_manifest.py` too and the manifest republishes itself as the
   daemon's new `.m4a` files land.)

8. **Deploy** — push the app shell + markdown/quiz to Cloudflare Pages and upload audio to
   this subject's R2 bucket (see the repo `DEPLOY.md`). The unified app picks the subject up
   automatically from `subject.json`; no app code changes are needed to add a subject.

## What's subject-specific vs shared

- **Subject-specific (lives here):** `subject.json`, `resources/`, `_plans/`, and the
  episode folders. The module codes, mnemonics, and teaching order are yours to define.
- **Shared/generic (format contracts, copied in for convenience):** `AUTHORING.md`,
  `STYLE.md`, `SUPPLEMENTARY.md`, `QUIZ_STYLE_GUIDE.md`, `CASE_STUDY_LESSON_PLAN.md`. These
  define the *form* every episode takes regardless of subject — read them, don't rewrite the
  rules. If you improve one, fold the improvement back into the canonical copy too.
