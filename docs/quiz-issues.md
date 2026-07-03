# Quiz / Review — known issues (to fix later)

_Logged 2026-07-02. The Review / daily-quiz feature works but needs more design work.
These are the outstanding conceptual + correctness problems, most important first._

---

## Q1 — Question provenance is mislabelled ("TEXTBOOK" on AI-generated questions)

**Severity:** high (correctness / trust — it misleads students about where a question came from)

**Symptom.** In the Review / daily quiz, multiple-choice questions show a **TEXTBOOK**
badge even though the textbook contains no such MC questions. Example (Physics, "Stellar
Spectra"):

> "Using the Doppler effect, how are the absorption lines in a star's spectrum shifted
> when the star is moving towards us, and what does the size of the shift reveal?" — badged **TEXTBOOK**

**Reality.** These are **AI-generated** questions *derived from* a textbook page, not
questions the textbook actually poses. The badge overstates provenance.

**Evidence.**
- `content/physics/M8-13-Reading-The-Stars-Spectra-And-Redshift/quiz.json` — the Doppler
  question carries:
  `source: { origin: "textbook", ref: "Jacaranda Physics for NSW 12 (4th ed.)", page: 216, url: "sources/phy12/p216.jpg" }`
- Across physics quizzes there are **~328 MC questions tagged `origin: "textbook"`** (plus
  133 `worked`, 73 `recall`, 11 `short`). Page 216 is prose — it does not contain that MC item.

**Where it lives.**
- Set by the **quiz-generation pipeline** (whatever writes `quiz.json`), not the UI.
- Rendered by `sourceBadgeHtml()` / `ORIGIN_META` in `app.js` (maps `origin: "textbook"` → the
  "TEXTBOOK" label).

**Fix directions (later).**
- Tag AI-authored questions as `origin: "ai"` and carry the textbook page as a *"derived from /
  reference"* field, not as the question's origin.
- Or relabel the badge so it's clear the item is AI-generated *from* a source, vs. verbatim
  *from* the source. Consider distinguishing "verbatim from source" from "AI-generated from source".

---

## Q2 — Spaced-repetition flashcards are conflated with HSC / past-paper drilling

**Severity:** high (conceptual — the core learning model is wrong)

**The problem.** Two *different learning modalities* are being treated as one:

- **Spaced-repetition flashcards (FSRS / Anki).** Atomic recall, scheduled over time to build
  long-term memory. Cards should be small, single-fact, and graded on recall.
- **HSC / past-paper drilling.** Volume practice of exam-style questions (MC, short, extended,
  worked). Builds exam skill through repetition and marking — *not* via SR scheduling.

Right now the **Review / daily quiz runs AI-generated exam-style questions (MC / short /
extended / worked) through the FSRS engine and presents them as "flashcards."** Scheduling a
multi-mark extended-response question via FSRS doesn't match how either mode should work. The
result muddies both: the SR system isn't fed clean atomic memory cards, and exam practice isn't
presented as timed/marked drilling.

**Desired model.** Keep the two conceptually separate:
1. **SR flashcards** — the daily-quiz / memory system (Anki-style).
2. **HSC / past-paper drilling** — the Past Papers mode (timed, marked, exam-style).

**Where it lives.**
- `renderReviewHub()`, `loadAllQuestions()`, `classifyCard()` and the FSRS wiring in `app.js`.
- `quiz.json` content mixes question *types* with no notion of "is this a flashcard or an exam
  question."
- Note: `loadAllQuestions()` already **excludes past-paper questions** from the SR hub by
  default — but ordinary episode quiz questions of *all* types still flow through FSRS.

**Fix directions (later).**
- Decide what a "flashcard" *is* (a card type distinct from question type) — authored or
  generated specifically as atomic recall.
- Route exam-style questions (extended / worked, and probably most MC) to a **separate drilling
  mode**, not the SR queue. Don't FSRS-schedule multi-mark written questions.
- This needs a data-model decision (card-type vs question-type) and likely separate content.

---

## Q3 — Redundant / unstyled Exit control in the Review overlay (minor UI)

**Severity:** low (cosmetic)

**Symptom.** Inside the Review overlay there are **two close controls**: the sheet's circular
**✕** (top-right) and an in-quiz **"✕ Exit"** (top-left). The "✕ Exit" also renders as plain grey
text — an intended pill restyle silently failed (the apply-script's "already applied" check
false-matched `display: inline-flex;` elsewhere in `style.css`, so `.quiz-exit-btn` kept its
original plain style).

**Fix directions (ready to do, CSS-only).**
- Hide the in-quiz Exit inside `#review-content` (the sheet's ✕ is enough there).
- Properly style `.quiz-exit-btn` as a pill where it *is* the sole exit (the inline episode quiz).
- Also: the subject chip only got inserted into 2 of the 4 quiz-header renderers — make it
  consistent across MC / short / extended / worked.

---

_Not started — parked for a later session. Q1 and Q2 should be settled before more polish, since
they change what the questions are and how they're scheduled._
