# _plans/ — per-module episode plans

This folder holds the **plans that drive script generation** — one file per module,
named `<MODULE>-PODCAST_PLAN.md` (e.g. `M1-PODCAST_PLAN.md`, `PF11-PODCAST_PLAN.md`).

They are the **output of step 3** (`../pipeline/GENERATE_PLAN_PROMPT.md`) and the **input to
step 4** (`../pipeline/GENERATE_EPISODE_PROMPT.md`). A plan gives each episode its *seeds*
(dot-points, recaps, interleaving, mnemonics, worked examples); `STYLE.md` gives the *form*;
`AUTHORING.md` gives the *files*.

This index fills in as you generate. Keep it current — the episode prompt reads it to know
what should exist.

## Modules

> Replace with this subject's real modules once the plans are generated.

**Year 11 (Preliminary):**

- `M1-PODCAST_PLAN.md` — M1, First Module Name

**Year 12 (HSC):**

- `M2-PODCAST_PLAN.md` — M2, Second Module Name

## Conventions (all modules)

- **Episode = one syllabus section = one folder.** `content/<subject>/<MODULE-LL-Title>/`
  holds `script.md`, `supplementary.md`, `quiz.json`, and the generated `<voice>.m4a` files.
  The **module code is in the folder name** (e.g. `M1-03-...`); the section number is the
  `lesson:` in frontmatter.
- **Oversized sections split** into `-Part-1` / `-Part-2` (same lesson number).
- **Module reviews** (`STYLE.md` §5.3): `XX-99-Module-Review-...` — one per module, plus a
  mid-module review where a block exceeds ~8 episodes.
- **Case studies** (`STYLE.md` §5.7): `case_...`, story-first, tied in later by a teaching
  episode. Maintain a master case-study list here (file · story · cashed in by which lessons).
- **Marquee mnemonics** — list them here and keep the wording **identical everywhere** they
  recur, so the spaced-repetition recaps line up across episodes.

## Status

- Plans: _not started_ — run `../pipeline/GENERATE_PLAN_PROMPT.md`.
- Built: _none yet_ — then run `../pipeline/GENERATE_EPISODE_PROMPT.md`.
- Reference episode: `../_example-episode/` (the worked two-file format + quiz).
