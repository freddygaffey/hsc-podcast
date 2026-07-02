Task: Generate the next episode's QUIZ from its script, then stop.

You are an expert HSC tutor and exam writer for **this subject** (read its name and module
codes from `subject.json`). Each run writes **exactly one `quiz.json`** — for one episode,
from that episode's own `script.md` — then stops. Run on a loop; it converges and ends itself
when every episode has a quiz.

**Run this once the scripts are written.** Quizzes are built from `script.md`, so they do **not**
need the audio — you can run this in parallel with the voice daemon (`./generate_all_voices.sh --daemon`)
still rendering `.m4a` files.

Working root: the subject folder that contains this `pipeline/` (e.g. `content/<subject>/`).

## HARD CONSTRAINTS — read first
- Work **directly in this one chat context**. Do **NOT** use Workflows or spawn subagents.
- Build each quiz **only** from material the listener actually heard — the episode's own
  `script.md` (same language, same mnemonics, same worked values). Don't introduce facts the
  listener never met.
- **Honest provenance.** Every question's `source.origin` must be truthful. If you wrote it
  from the script, it is `ai`. Only tag `hsc` / `trial` / `textbook` when the question really
  comes from that source AND you can cite it (`ref`, and a real `url`/`page` where available).
  **Never invent a paper reference or a URL.**

## Step 0 — Read the rules ONCE (skip if already in context)
- `QUIZ_STYLE_GUIDE.md` — the binding schema contract (types, `source`, FSRS, traceability).
- `_example-episode/quiz.json` — a worked example of the format and the question/type/source mix.

## Step 1 — Find the gap (deterministic; do ONE then stop)
In teaching order: the **first episode that has `script.md` but no `quiz.json`**. Write its
quiz (Step 2), then stop. Detect with `ls content/<EP>/` and `git status --short`.
If every episode already has a `quiz.json`, print `QUIZZES COMPLETE`, confirm a clean tree, and
end the loop. Honour an explicit target if given ("quiz M3-04").

## Step 2 — Write the quiz (`content/<EP>/quiz.json`), from that episode's `script.md`
Per `QUIZ_STYLE_GUIDE.md`. Valid JSON object `{"questions":[ … ]}`, **~10 questions**, JSON
only (no markdown fences inside the file).

**Every question carries:** `id` = `m<module><lesson>-q<NN>` (e.g. `m304-q01`); `type`; `q`
(an HSC exam verb); `explanation` (2–4 sentences, same language as the script, naming the
tempting distractor and any episode mnemonic); and a `source` object (see below).

**Type mix (per episode):**
- **`mc` (≈4–5)** — exactly 4 plausible options; `answer` is the zero-based index. The backbone.
- **`recall` (≈2)** — "what's the key point?" Provide `keyPoints` (2–4 bullets) the student
  self-checks against. No options.
- **`worked` (≈2 for quantitative subjects; skip for non-numeric ones)** — a calculation with
  `given`, a `working` array (**one step per line**, show every step), and where there's a
  numeric answer, `answerValue` (+ `answerUnit`, `tolerance`). **You may author these with
  `origin: "ai"` for maths/physics: if you know the correct answer, write the full working
  from it.** Keep the values identical to the episode's worked examples.
- **`short` / `extended` (≈1–2)** — a written response with `marks`, a `modelAnswer`, and
  `criteria`. Prefer a **real `hsc`/`trial` question** here when one fits the episode's topic
  (cite it); otherwise `ai` from the script.

**Source / provenance (required on each question):**
```json
"source": { "origin": "hsc|trial|textbook|ai", "ref": "…", "year": 0, "page": 0, "url": "…" }
```
- `ai` → `"ref": "Generated from episode script"`. Always labelled "AI-generated" in the app.
  AI questions are **tagged but not capped** — use them to cover the script thoroughly.
- `hsc`/`trial` → `ref` names the paper + question number; add a real `url` (public PDF,
  `#page=N` to deep-link) when you have it.
- `textbook` → `ref` + `page`; only add `url` if a hosted scan exists under `sources/`
  (login-gated). Otherwise omit `url` and the citation shows as text.

**Gate before committing** (must pass):
```
python3 tools/validate_quiz.py content/<EP>/quiz.json
```

## Step 3 — Commit
One focused commit per quiz, e.g. `M3-04: add quiz`. A pre-commit hook (or
`python3 tools/generate_manifest.py`) refreshes `manifest.json` so the quiz appears in the app.
End the commit message with the co-author trailer the harness specifies. Don't push unless asked.

## Step 4 — Report briefly, then continue or stop
- Which quiz was written (path), its type mix, and its provenance mix.
- The gate result, and the next episode lacking a quiz. If every episode has one, print
  `QUIZZES COMPLETE`.

If anything conflicts with `QUIZ_STYLE_GUIDE.md`, the guide wins.

---

## Loop usage

```
/loop Follow pipeline/GENERATE_QUIZ_PROMPT.md: do exactly one unit of work, then stop.
```

When this prints `QUIZZES COMPLETE`, the subject is content-complete: rebuild the manifest
(`python3 tools/generate_manifest.py`) and deploy (see the repo `DEPLOY.md`).
