Task: Generate the next module's podcast PLAN from this subject's sources, then stop.

You are an expert HSC tutor and course designer for **this subject** (read its name, module
codes, and Year 11/12 split from `subject.json` in this subject folder). Each time you run
this you produce **exactly one unit of work** — usually one module's plan — then stop. Run on
a loop; it converges and ends itself when every module has a plan.

A *plan* is the spine of the course: for one module, it lists every episode and seeds each one
with dot-points, recaps, interleaving links, mnemonics, and worked examples. The episode
prompt (`GENERATE_EPISODE_PROMPT.md`) later turns each seeded episode into a script. Plans
first, scripts second — never write scripts from this prompt.

Working root: the subject folder that contains this `pipeline/` (e.g. `content/<subject>/`).

## HARD CONSTRAINTS — read first
- Work **directly in this one chat context**. Do **NOT** use Workflows or spawn subagents —
  that re-reads every spec per agent and burns huge usage. Read the spec/source files **once
  per session** and reuse the loaded context across loop iterations.
- **Never open giant PDFs.** If `resources/` has a big textbook/syllabus PDF, use the
  extracted text in `resources/extracted/` instead (see `resources/README.md`). Find a topic
  with `grep -n`, don't read the whole file.
- This step writes **plans only** (`_plans/<MODULE>-PODCAST_PLAN.md`). No episode folders, no
  `script.md`, no audio.

## Step 0 — Read the rules and sources ONCE (skip anything already in context)
- `subject.json` — the subject name, the module codes (`groupNames`), and which year each
  belongs to (`yearMap`). These define what modules exist and their teaching order.
- `STYLE.md` (binding — §5 the teaching shape, §5.3 reviews, §5.7 case studies), and
  `CASE_STUDY_LESSON_PLAN.md` — so the plan's seeds match the form scripts must take.
- `_plans/README.md` — the plan index, conventions, and current status.
- The **sources in `resources/`** for the module you're planning — above all the **syllabus**
  (lift outcomes and content dot-points verbatim) and the **textbook chapter(s)** that map to
  this module (for the real concepts, values, and worked examples).
- One **finished plan** as a model once any exists; until then, `_example-episode/` shows the
  depth of a single episode the plan must seed.

## Step 1 — Find the gap (deterministic; do ONE then stop)
In teaching order (Year 11 modules before Year 12; within a year, the order implied by the
module codes / syllabus):
1. **Missing plan.** First module (per `subject.json` `groupNames`) with no
   `_plans/<MODULE>-PODCAST_PLAN.md`. Write it (Step 2), update `_plans/README.md`, commit, stop.
2. **Missing case-study master list.** Else if no case-study table exists in `_plans/README.md`,
   add it (story · file `case_...` · which lessons cash it in), commit, stop.
3. **Done.** Else print `PLANS COMPLETE`, confirm a clean tree, and end the loop.

Honour an explicit target if given ("plan module M3").

## Step 2 — Write the module plan (`_plans/<MODULE>-PODCAST_PLAN.md`)
Decide the **episode list** for the module: one episode per syllabus section/sub-topic, in
teaching order, named `<MODULE>-LL-Title` (lesson `LL` = two digits). Split an oversized
section into `-Part-1` / `-Part-2`. Add a module review `<MODULE>-99-Module-Review-...`
(plus a mid-module review if the module exceeds ~8 episodes — `STYLE.md` §5.3).

Then write the plan file with an intro (what these episodes are / aren't, the
extended-response problem they fix, the target listener) followed by **one section per
episode**, `### <MODULE>-LL — Title`, each containing:

- **Theory focus** — the one home topic; what to teach vs assume known.
- **Extended-response prep** — the headline exam question, with a **weak-vs-strong answer
  contrast** (what loses marks vs what earns them, in real NESA-verb phrasing).
- **Syllabus dot-points served** — lifted **verbatim** from the syllabus in `resources/`
  (include outcome codes where the syllabus uses them).
- **Memorisable lists needing mnemonics** (`STYLE.md` §5.4) — flag each list a student must
  recall; coin a marquee mnemonic and record it once in `_plans/README.md` so its wording
  stays identical everywhere it recurs.
- **Cross-links / interleaving** — concrete back- and forward-references (including
  cross-module and Year 11 → Year 12), plus any case study (`case_...`) this episode cashes in.
- **Worked examples / values** — the specific numbers, derivations, or listings the
  `supplementary.md` will need, taken from the textbook (not invented).

End with a **Recommended Production Order** table for the module's episodes. Keep every claim
anchored to the sources in `resources/` — when unsure of a value or definition, grep the
extracted text rather than guessing.

## Step 3 — Update the index and commit
Add/refresh the module's entry in `_plans/README.md` (and the mnemonic + case-study lists).
Then make **one focused commit**, e.g. `M3: add waves module podcast plan`. End the commit
message with the co-author trailer the harness specifies. Don't push unless asked.

## Step 4 — Report briefly, then continue or stop
- Which plan was written (path), its episode count, and the modules still unplanned.
- The mnemonics coined and the case studies seeded.
- The next gap the loop will pick up. If every module is planned, print `PLANS COMPLETE`.

Write the plan, not a summary of one. If anything conflicts with `STYLE.md`, `STYLE.md` wins.

---

## Loop usage

```
/loop Follow pipeline/GENERATE_PLAN_PROMPT.md: do exactly one unit of work, then stop.
```

Each iteration writes one module's plan (or the case-study list); the loop re-fires and
terminates itself when every module in `subject.json` has a plan (`PLANS COMPLETE`). Then move
on to `GENERATE_EPISODE_PROMPT.md`.
