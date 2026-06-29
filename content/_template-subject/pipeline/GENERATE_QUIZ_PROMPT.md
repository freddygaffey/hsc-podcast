Task: Generate the next episode's QUIZ from its script, then stop.

You are an expert HSC tutor and exam writer for **this subject** (read its name and module
codes from `subject.json`). Each run writes **exactly one `quiz.json`** — for one episode,
from that episode's own `script.md` — then stops. Run on a loop; it converges and ends itself
when every episode has a quiz.

**Run this once the scripts are written.** Quizzes are built from `script.md`, so they do **not**
need the audio — you can run this in parallel with the voice daemon (`./generate_all_voices.sh --daemon`)
still rendering `.m4a` files. They're kept separate from script-writing so each lesson's quiz is
authored from its final script.

Working root: the subject folder that contains this `pipeline/` (e.g. `content/<subject>/`).

## HARD CONSTRAINTS — read first
- Work **directly in this one chat context**. Do **NOT** use Workflows or spawn subagents.
- Build each quiz **only** from the episode's own `script.md` — same language, same mnemonics,
  same worked values. Don't introduce facts the listener never heard.

## Step 0 — Read the rules ONCE (skip if already in context)
- `QUIZ_STYLE_GUIDE.md` — the binding quiz contract.
- `_example-episode/quiz.json` — a worked example of the format and question mix.

## Step 1 — Find the gap (deterministic; do ONE then stop)
In teaching order: the **first episode that has `script.md` but no `quiz.json`**. Write its
quiz (Step 2), then stop. Detect with `ls content/<EP>/` and `git status --short`.
If every episode already has a `quiz.json`, print `QUIZZES COMPLETE`, confirm a clean tree, and
end the loop. Honour an explicit target if given ("quiz M3-04").

## Step 2 — Write the quiz (`content/<EP>/quiz.json`), from that episode's `script.md`
Per `QUIZ_STYLE_GUIDE.md`:
- Valid JSON object `{"questions":[ … ]}`, **exactly 10** questions. JSON only — no markdown
  fences inside the file.
- Each question: `id` = `m<module><lesson>-q<NN>` (e.g. `m304-q01`); `q` (an HSC exam verb);
  `options` (**exactly 4**, all plausible); `answer` (**zero-based** index 0–3 of the correct
  option); `explanation` (2–4 sentences, same language as the script, naming the tempting
  distractor and any episode mnemonic).
- Mix: ~2–3 recall, 3–4 describe/explain, 2–3 compare, **≥1 scenario/calculation** with 4
  plausible numeric options. Use exact syllabus terminology.

**Gate before committing:**
`python3 -c "import json;d=json.load(open(PATH));qs=d['questions'];assert len(qs)==10;assert all(len(q['options'])==4 and q['answer'] in range(4) for q in qs)"`
must pass.

## Step 3 — Commit
One focused commit per quiz, e.g. `M3-04: add quiz`. A pre-commit hook (or
`python3 tools/generate_manifest.py`) refreshes `manifest.json` so the quiz appears in the app.
End the commit message with the co-author trailer the harness specifies. Don't push unless asked.

## Step 4 — Report briefly, then continue or stop
- Which quiz was written (path) and its question mix.
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
