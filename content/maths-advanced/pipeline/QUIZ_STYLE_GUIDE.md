# Quiz Style Guide

Each episode can have a `quiz.json` file in its content folder. The player loads it
automatically when the **Quiz** tab is opened. Past papers use the same schema with a few
extra fields — see `PAST_PAPERS.md`.

This file is the **binding contract**. The app engine and the generation prompts both key
off it. If a generated quiz disagrees with this guide, the guide wins.

## File location

```
content/{episode-folder}/quiz.json
```

Example: `content/M7-12-The-Photoelectric-Effect/quiz.json`

---

## Top-level format

```json
{
  "questions": [ /* … question objects … */ ]
}
```

Aim for **~10 questions** per episode across a mix of types (see "Question mix" below).

---

## Question types

Every question has a `type`. Five are supported. They share a common spine — `id`, `type`,
`q`, `explanation`, `source` — and add type-specific fields.

| `type` | What it tests | How it's marked |
|---|---|---|
| `mc` | Recognition / reasoning | Auto (pick the right option) → then FSRS self-grade |
| `recall` | Active recall of the key point | Self-marked against `keyPoints` → FSRS |
| `worked` | A calculation, with the working revealed | Optional numeric auto-check → FSRS |
| `short` | A 2–4 mark written response | Self-marked vs `modelAnswer` + `criteria` |
| `extended` | A 5+ mark extended response | Self-marked vs `modelAnswer` + `criteria` |

### Common fields (every question)

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique per episode. Pattern `m{module}{lesson}-q{nn}`, e.g. `m712-q01`. |
| `type` | string | One of `mc` `recall` `worked` `short` `extended`. |
| `q` | string | The question stem. Use an HSC exam verb (see table below). |
| `explanation` | string | 2–4 sentences shown after answering. Same language as the script. Optional on `worked` (the `working` carries it). |
| `source` | object | Provenance + traceability. **Required.** See "Source / provenance". |
| `image` | string | Optional. Path to a stimulus image (relative to the episode folder or `sources/`). |

### `type: "mc"` — multiple choice

```json
{
  "id": "m712-q01",
  "type": "mc",
  "q": "What decisive new rule did Einstein add to Planck's photon idea?",
  "options": [
    "An electron adds up energy from many photons over time",
    "A single photon transfers all its energy to one electron in one hit",
    "Photons travel slower in metals, giving electrons time to escape",
    "Light pushes electrons out by the pressure of its amplitude"
  ],
  "answer": 1,
  "explanation": "Einstein's one-photon-one-electron collision delivers the whole photon energy at once — explaining the no-delay and threshold results the wave model could not.",
  "source": { "origin": "ai", "ref": "Generated from episode script" }
}
```

| Field | Type | Notes |
|---|---|---|
| `options` | string[4] | **Exactly 4**, all plausible. Avoid absurd distractors. |
| `answer` | number | **Zero-based** index (0–3) of the correct option. |

### `type: "recall"` — active recall ("what's the key point?")

The student answers **from memory**, reveals the model points, then self-grades. There is no
auto-marking — the value is the retrieval effort.

```json
{
  "id": "m712-q05",
  "type": "recall",
  "q": "In your own words: why can't the wave model explain the photoelectric threshold frequency?",
  "keyPoints": [
    "Wave energy depends on intensity (brightness), not frequency.",
    "So a bright enough low-frequency light *should* eventually eject electrons — but it never does.",
    "Only the one-photon-one-electron model ties ejection to frequency via E = hf."
  ],
  "explanation": "If you recalled the intensity-vs-frequency mismatch and linked it to E = hf, mark it Good or Easy.",
  "source": { "origin": "ai", "ref": "Generated from episode script" }
}
```

| Field | Type | Notes |
|---|---|---|
| `keyPoints` | string[] | The bullet points the student checks their recall against. 2–4 is ideal. |

### `type: "worked"` — calculation with revealed working

The student enters a number (optional), then reveals the **step-by-step working**. If
`answerValue` is present the app auto-checks the number against `± tolerance`; either way the
student self-grades after seeing the working.

```json
{
  "id": "m712-q06",
  "type": "worked",
  "q": "I accelerate from rest at 1 m s⁻² for 1 s. What is my speed?",
  "given": "u = 0,  a = 1 m s⁻²,  t = 1 s",
  "working": [
    "v = u + at",
    "v = 0 + (1)(1)",
    "v = 1 m s⁻¹"
  ],
  "answerValue": 1,
  "answerUnit": "m s⁻¹",
  "tolerance": 0.01,
  "explanation": "Straight application of v = u + at with u = 0.",
  "source": { "origin": "textbook", "ref": "Jacaranda Physics 11", "page": 142,
              "url": "sources/jac-phy11/p142.jpg" }
}
```

| Field | Type | Notes |
|---|---|---|
| `given` | string | The known quantities, shown above the input. Optional but recommended. |
| `working` | string[] | The revealed solution, **one step per line**. Use LaTeX in `\\( … \\)`. **Required.** |
| `answerValue` | number | Optional. If present, the app auto-checks the typed number. Omit for non-numeric working. |
| `answerUnit` | string | Optional. Displayed next to the input (e.g. `m s⁻¹`). |
| `tolerance` | number | Optional. Absolute tolerance for the auto-check. Default `0` (exact). |

### `type: "short"` / `type: "extended"` — written response

The student types an answer, reveals the model answer + marking criteria, then self-marks out
of `marks`. `short` and `extended` differ only in expected length/marks.

```json
{
  "id": "m712-q08",
  "type": "short",
  "q": "Explain why increasing the intensity of light below the threshold frequency produces no photocurrent.",
  "marks": 3,
  "modelAnswer": "Below the threshold frequency each photon carries less energy than the work function (E = hf < φ). Intensity only increases the *number* of photons, not the energy of each. Since no single photon can free an electron, no current flows however bright the light.",
  "criteria": [
    { "marks": 1, "descriptor": "States photon energy depends on frequency (E = hf)." },
    { "marks": 1, "descriptor": "Links intensity to photon count, not photon energy." },
    { "marks": 1, "descriptor": "Concludes no electron is ejected → no current." }
  ],
  "explanation": "The crux is energy-per-photon vs number-of-photons.",
  "source": { "origin": "hsc", "ref": "2018 HSC Physics Q26", "year": 2018,
              "url": "papers/2018/phy.pdf#page=14" }
}
```

| Field | Type | Notes |
|---|---|---|
| `marks` | number | Total marks. Drives the self-mark pills (0…N) and suggested time. |
| `modelAnswer` | string | The model/sample answer, revealed on demand. |
| `criteria` | object[] | `{ "marks": n, "descriptor": "…" }` per mark band. |

---

## Source / provenance (required on every question)

Every question records **where it came from** so the student can trust it and trace it back.

```json
"source": {
  "origin": "hsc" | "trial" | "textbook" | "ai",
  "ref":    "2021 HSC Physics Q12",
  "year":   2021,
  "page":   142,
  "url":    "papers/2021/phy.pdf#page=4"
}
```

| Field | Type | Notes |
|---|---|---|
| `origin` | string | **Required.** `hsc` (NESA past paper), `trial` (a trial/exam paper), `textbook`, or `ai` (model-generated). |
| `ref` | string | **Required.** Human label shown on the badge, e.g. `2021 HSC Q12`, `Jacaranda Physics 11`. |
| `year` | number | Optional. For papers. |
| `page` | number | Optional. Textbook page. |
| `url` | string | Optional. Link the student can open to see the original. See "Traceability". |

### Origin rules

- **`hsc` / `trial`** — questions lifted from a real exam. `ref` names the paper + question
  number; `url` deep-links the public PDF (use `#page=N` to jump to the page).
- **`textbook`** — `ref` names the book, `page` the page, `url` points to a hosted scan
  **under `sources/`** (login-gated — see Traceability). If you don't have a hosted scan,
  omit `url` and the badge shows the citation as text only.
- **`ai`** — model-generated from the episode script. Always labelled in the UI as
  "AI-generated" so students know to verify it. AI questions are **tagged but not capped**;
  use them to fill gaps the real papers don't cover.

---

## Traceability — linking to the original

The app turns `source.url` into a "View source ↗" link in the answer feedback.

- **Past papers (public)** — NESA papers are public documents. Host the PDF and link it
  directly. `#page=N` anchors jump the reader to the right page.
- **Textbook scans (copyright)** — store page images/PDFs under `content/{subject}/sources/`,
  which is served **behind the auth-worker (login required)**. This keeps it a personal-study
  tool, not a public textbook mirror. Reference them by relative path, e.g.
  `sources/jac-phy11/p142.jpg`. Only host pages you have the right to use.
- **No asset** — omit `url`. The badge still shows `ref` (+ `page`) as a plain citation the
  student can look up themselves.

---

## Writing good questions

### HSC exam verbs

Match the verb to the cognitive level:

| Verb | Meaning | Marks |
|---|---|---|
| **Identify / Name / State** | Simple recall | 1–2 |
| **Outline / Describe** | Name + one characteristic | 2–3 |
| **Explain** | Reason or mechanism | 3–4 |
| **Distinguish / Compare** | Similarities and/or differences | 3–5 |
| **Evaluate / Justify / Recommend** | Weigh up, reach a conclusion | 5–6 |

### Distractors (for `mc`)

Good distractors are wrong for a specific, learnable reason:
- **Common misconception** — something students often confuse with the right answer
- **Partially correct** — true, but doesn't answer *this* question
- **Wrong word, right concept** — informal term instead of the syllabus term
- **Out of scope** — true for a different topic

Avoid: absurd options, trick wording, double negatives.

### Explanations / working / key points

The post-answer content is the most valuable part. It should:
1. Confirm **why the correct answer is correct** in the same language as the script.
2. Address the **most tempting wrong answer** specifically (for `mc`).
3. Reference any **mnemonic or exam technique** from the episode.
4. For `worked`: show **every step**, don't skip algebra.

### Question mix (per episode, ~10 questions)

| Type | Target share | Notes |
|---|---|---|
| `mc` | 40–50% | The backbone. Mix recall / explain / compare verbs. |
| `recall` | ~20% | At least 1–2 "what's the key point" prompts. |
| `worked` | ~20% | At least 1 calculation **for quantitative subjects**; skip for non-numeric subjects. |
| `short` / `extended` | ~10–20% | Especially where real HSC/trial questions exist — prefer `origin: "hsc"` over `ai` here. |

Provenance target: prefer **real exam questions** (`hsc`/`trial`) and **textbook** items where
they exist; use `ai` to fill gaps. Build each question **only** from material the listener
actually heard in the episode script (same values, same mnemonics).

---

## Spaced repetition behaviour (FSRS)

The player uses **FSRS** (the modern engine behind Anki), not SM-2.

- After answering an `mc`, `recall`, or `worked` question the student self-grades on a
  4-button scale — **Again · Hard · Good · Easy** (FSRS ratings 1–4) — each button previewing
  its next interval.
- New / never-seen cards are always due. A graded card's next due date is computed by FSRS
  from its stability and the chosen rating, against the user's target retention (Settings).
- `short` / `extended` use the self-mark pills (0…N) rather than FSRS grades.
- Past papers track simple right/wrong + self-marks **separately** (not FSRS) — they're sat
  like mock exams. See `PAST_PAPERS.md`.

Progress is stored in `localStorage` under `podcast-quiz-sr`, keyed by
`{episodeId}::{questionId}`, and synced when the user is signed in.

---

## Validation gate

Before committing a quiz, it must pass the validator:

```bash
python3 tools/validate_quiz.py content/{episode-folder}/quiz.json
```

It checks: valid JSON; every question has `id`, `type`, `q`, `source.origin`, `source.ref`;
`mc` has exactly 4 `options` and an in-range `answer`; `worked` has `working`; `short`/
`extended` have `marks` + `modelAnswer`; ids are unique within the file.

---

## Checking which episodes have quizzes

```bash
find content -name "quiz.json" | sort
```
