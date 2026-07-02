# pipeline/ — the content engine for this subject

Everything needed to take a subject from **raw sources → finished, deployable episodes**.
It's copied into every subject so each one is self-contained.

## The prompts (the moving parts)

| # | Prompt | Reads | Writes | When |
|---|--------|-------|--------|------|
| 2 | `INIT_SUBJECT_PROMPT.md`     | the syllabus in `../resources/` (+ the user) | fills `../subject.json` + specialises the copied docs | Once, right after copying the template |
| 3 | `GENERATE_PLAN_PROMPT.md`    | `../resources/` + `subject.json` | `../_plans/<MODULE>-PODCAST_PLAN.md` | Once per module, up front |
| 5 | `GENERATE_EPISODE_PROMPT.md` | `../_plans/` + the contracts below | `../<MODULE-LL-Title>/script.md` + `supplementary.md` | On a loop, one episode per run |
| 6 | `GENERATE_QUIZ_PROMPT.md`    | each episode's `script.md` + `QUIZ_STYLE_GUIDE.md` | `../<MODULE-LL-Title>/quiz.json` | On a loop, once scripts exist |

Run them with `/loop` (self-paced). Each does **exactly one unit of work, then stops**; the
loop converges and ends itself when its stage is complete.

**Plans, then scripts — with audio rendering in parallel:**

1. `GENERATE_PLAN_PROMPT` loops until `PLANS COMPLETE`.
2. **Start the voice daemon** (`./generate_all_voices.sh --daemon`) in a terminal. It renders each script's
   `.m4a` files in the background **as they're written** — audio is never a blocking step, and
   the model never writes `.m4a` itself.
3. `GENERATE_EPISODE_PROMPT` loops, writing scripts only; the daemon renders behind it.
4. `GENERATE_QUIZ_PROMPT` loops until `QUIZZES COMPLETE`. Quizzes come from the scripts, so they
   don't wait on the audio — run them as soon as scripts exist.

Quizzes are kept separate from script-writing (authored from each final script), but they run
**in parallel** with audio rendering, not after it.

## The format contracts (the binding rules — read, don't rewrite)

These define the *form* every episode takes, the same for every subject:

- **`AUTHORING.md`** — the exact files to produce and copyable templates (the *what*).
- **`STYLE.md`** — how the spoken script is written: two voices, teaching shape, spaced-rep
  opener, mnemonics, exam framing. **Binding — §9 is the gate.** If anything conflicts with
  STYLE.md, STYLE.md wins.
- **`SUPPLEMENTARY.md`** — the `supplementary.md` format contract (`### Listing N —`,
  ` ```text ` fences, tables).
- **`QUIZ_STYLE_GUIDE.md`** — the `quiz.json` contract (10 questions, 4 options, zero-based
  `answer`, exam verbs, explanation naming the distractor).
- **`CASE_STUDY_LESSON_PLAN.md`** — how to plan and write the story-first case studies.

## The whole flow (see `../README.md` for the full runbook)

```
INIT_SUBJECT_PROMPT  ──▶  subject.json + subject-specific docs filled in
      │
../resources/  ──▶  GENERATE_PLAN_PROMPT      ──▶  ../_plans/*.md
                                                       │
                    GENERATE_EPISODE_PROMPT   ◀────────┘
                            │  (loops, one script each)
                            ▼
        ../<MODULE-LL-Title>/{script.md, supplementary.md}
                            │
   ┌────────────────────────┴───────────────────────────┐
   ▼  (in parallel)                                      ▼
 ./generate_all_voices.sh --daemon  daemon                  GENERATE_QUIZ_PROMPT
   renders <voice>.m4a as scripts land            ──▶ ../<MODULE-LL-Title>/quiz.json
   └────────────────────────┬───────────────────────────┘
                            ▼
        tools/generate_manifest.py ──▶ manifest.json ──▶ deploy
```

> These prompts are **subject-agnostic**: they read the subject's name, module codes, and
> teaching order from `subject.json` and `_plans/`, not from hard-coded values. Adapt the
> seeds in the plans, not the prompts.
