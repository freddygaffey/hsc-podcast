Task: Generate the next podcast EPISODE from the plans (script + supplementary), then stop.

You are an expert HSC tutor and scriptwriter for **this subject** (read its name, module
codes, and Year 11/12 split from `subject.json`). Each time you run this you write **exactly
one episode** — `script.md` + `supplementary.md` — then stop. Run on a loop; it converges and
ends itself when every episode in the plans exists.

**This stage produces scripts only** (`script.md` + `supplementary.md`) — do NOT write
`quiz.json` (that's `GENERATE_QUIZ_PROMPT.md`) and never write `.m4a` audio.

**Audio renders in parallel via a daemon — you don't stop for it.** Before looping this
prompt, the user starts the voice daemon (`./generate_all_voices.sh --daemon`) in a terminal. It watches
`content/` and renders each script's voices in the background **as soon as you commit it**, so
authoring and audio happen at the same time. If the user hasn't started it yet, remind them
once (Step 0), then keep writing — the daemon will catch up on every pending script when it
starts. You never block on audio.

Working root: the subject folder that contains this `pipeline/` (e.g. `content/<subject>/`).

## HARD CONSTRAINTS — read first
- Work **directly in this one chat context**. Do **NOT** use Workflows or spawn subagents —
  that re-reads every spec per agent and burns huge usage. Read the spec files **once per
  session** and reuse the loaded context across loop iterations.
- Prerequisite: the module's plan must exist in `_plans/`. If it doesn't, stop and say so —
  run `GENERATE_PLAN_PROMPT.md` first.
- Never open giant PDFs; use the extracted text in `resources/extracted/` and `grep`.

## Step 0 — Read the rules ONCE (skip anything already in context)
- **Check the voice daemon is running.** On the first iteration, remind the user (once):
  *"Start the voice daemon so audio renders in parallel: run `./generate_all_voices.sh --daemon` (or
  `CONTENT_DIR=content/<subject> ./generate_all_voices.sh --daemon` in the unified repo) in a terminal."*
  Then proceed regardless — it backfills any scripts written before it was started.
- `AUTHORING.md` — the exact files to produce (episode folder, `script.md`, `supplementary.md`).
- `STYLE.md` — binding. **§9 is the gate; §5 the teaching shape; §5.7 the case-study format.**
- `SUPPLEMENTARY.md` — the `supplementary.md` contract (`### Listing N —`, ` ```text ` fences, tables).
- The relevant `_plans/<MODULE>-PODCAST_PLAN.md` — the per-episode spec (theory focus,
  weak-vs-strong answer, dot-points, cross-links, mnemonics, worked values) for the gap you fill.
- `_example-episode/` (both files) — the gold standard. Match its depth, voice, and listing style.

## Step 1 — Find the gap (deterministic; do ONE then stop)
In teaching order (Year 11 modules before Year 12; within a module, lesson order from the plan):
1. **Incomplete episode.** First episode the plans say should exist whose folder is missing, or
   missing `script.md` or `supplementary.md`, or whose files are empty / lack valid frontmatter.
   Write the missing file(s) for that ONE episode (Steps 2–3), then stop. Detect with
   `ls content/<EP>/` and `git status --short`.
2. **Case study.** Else the next `case_...` named in the plan's case-study list that has no
   folder. Write it in case-study mode (Steps 2–3), then stop.
3. **All scripts done.** Else every planned episode + case study has both `.md` files. Print
   the completion notice (Step 4) and end the loop.

Honour an explicit target if given ("write M3-04", "do the case study X").

## Step 2 — Gather material for that one episode
- Follow its section in the plan closely (theory focus, the weak-vs-strong contrast, dot-points,
  cross-links, mnemonics, worked values).
- Read the relevant extracted source in `resources/` for exact concepts/values/worked numbers —
  grep for the topic; never invent values.
- For the spaced-rep opener, glance at the adjacent already-written episodes on disk for their
  exact key terms so the recap is accurate (not the full prior scripts).
- For a case study: gather the narrative — people, timeline beat by beat, stakes, the technical "how".

## Step 3 — Write the episode to spec (two Markdown files; see AUTHORING.md)
`script.md` must satisfy every `STYLE.md` §9 box.
- **`script.md` frontmatter:** `title, module, lesson, kind` (lesson | case-study | module-review),
  `supplementary: supplementary.md`.
- **Two voices only:** `NARRATOR:` (teaches) and `QUESTION:` (only ever asks); ~80%+ narrator.
- **Speakable prose:** no equations, symbols, scientific notation, or markdown anywhere in the
  spoken body — spell everything out. No `## Appendix` in `script.md`.
- **`supplementary.md`:** own frontmatter (`…, script: script.md`), `# Supplementary Materials`
  heading, then `### Listing N — …` items (equations/derivations/worked solutions in ` ```text `
  fences, one step per line; data in Markdown tables). Every listing is referenced by label in
  the narration, and the narration never says "as you can see here".
- **~4500–6500 spoken words** (module reviews may run longer).
- **Teaching episode** (full §5 shape): one home topic; ~5-min spaced-rep opener recapping the
  last up-to-5 episodes (reuse the plan's mnemonics); weak-vs-strong contrast; **≥2 real
  interleaving links**; a mnemonic for every memorisable list; **≥1 "pause the player"
  retrieval** `QUESTION:`; **3–5 closing exam questions** in NESA-verb format with full model
  answers (calcs referenced to a Listing).
- **Module review** (`kind: module-review`, §5.3): integrative, second-voice-heavy, multi-topic.
- **Case study** (§5.7): one real story, gripping; **no** spaced-rep opener, **no** forced
  interleaving, **no** exam framing during the story.

**Format gate before committing:** `script.md` has valid frontmatter + only `NARRATOR:`/
`QUESTION:` labels + no leaked symbols/equations/markdown in the spoken body; `supplementary.md`
has valid frontmatter + `# Supplementary Materials` + balanced ` ```text ` fences + every
referenced Listing present. Then **one focused commit per episode** (e.g. `M3-04: add
refraction episode`), ending with the co-author trailer the harness specifies. Don't push unless asked.

## Step 4 — All scripts done (no blocking)
When Step 1 finds no missing scripts, the writing stage is complete. Audio has been (or is
being) rendered in parallel by the voice daemon — there is **no gate to wait at**. Print:

> ✅ All episode scripts for **<subject>** are written.
> • Audio: the voice daemon (`./generate_all_voices.sh --daemon`) renders these in the background. If it
>   wasn't running, start it now (or run a one-off catch-up: `./generate_all_voices.sh --once`);
>   check progress with `git status` / the folder's `.m4a` files.
> • Next: generate the quizzes with `GENERATE_QUIZ_PROMPT.md` (it reads the finished scripts
>   and does **not** need the audio, so you can start it immediately).

Then **end the loop** — don't write quizzes here.

## Step 5 — Report briefly
Per episode: path + kind + target duration; dot-points covered, spaced-rep targets, interleaving
links, mnemonics reused vs coined, listings added; the `STYLE.md` §9 checklist ticked (flag any
you couldn't satisfy). State the next gap, or print the completion notice (Step 4) if scripts
are complete.

Write the script, not a summary of one. If anything conflicts with `STYLE.md`, `STYLE.md` wins.

---

## Loop usage

```
/loop Follow pipeline/GENERATE_EPISODE_PROMPT.md: do exactly one unit of work, then stop.
```

Each iteration writes and commits one episode; the loop re-fires for the next and ends when
every planned script exists. The voice daemon (`./generate_all_voices.sh --daemon`) renders audio in
parallel the whole time. When scripts are done, move on to `GENERATE_QUIZ_PROMPT.md` (it
doesn't wait on audio).
