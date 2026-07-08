# Bug-fix list

_Running list of concrete UI / behaviour bugs to fix later. Design-level quiz issues
(provenance labelling, flashcards-vs-HSC-drilling) live in [`quiz-issues.md`](quiz-issues.md).
Logged 2026-07-02._

## Overnight session status (2026-07-02)

**Fixed & committed to `main` (not yet deployed — awaiting go-ahead):**
- ✅ **BUG-1** scroll-lock — commit `12629ad`
- ✅ **BUG-3** no play button on papers — commit `fe5703d`
- ✅ **BUG-4** drop "HSC" prefix — commit `ed81632`

**Not fixed (can't be done blind — needs your input):**
- ⏸ **BUG-2** — the in-app paper/quiz/config CSS is already fully theme-aware (`var(--bg-*)`,
  `var(--text)`, `var(--border)`). I couldn't reproduce the dark-mode fault from code alone; it
  needs a **screenshot** of the exact offending element, or it lives in the custom-materials tool
  (see BUG-5).
- ⏸ **BUG-5** — the "generate quizzes from custom materials" UI is **not in this web codebase**
  (grep finds nothing). It's a separate tool/pipeline; can't fix it from here without its source.
- ⏸ **BUG-6** — feature work (new flashcard card-types / graphics), explicitly deferred; depends on
  the Q2 decision in `quiz-issues.md`. The in-app image style (`.quiz-stimulus`) itself is fine.

---

## BUG-1 — Background scrolls behind open overlays / sheets

**Severity:** medium (feels broken; content behind the sheet moves while you interact with it)

**Symptom.** With the **Settings** sheet open you can scroll the page content *behind* it.
Same pattern applies to the other sheets (Stats, Review, Queue) — they share the overlay code.
The body should be scroll-locked while any sheet is open.

**Cause (confirmed).** `openSheet()` / `closeSheet()` (`app.js`, ~line 133) only toggle the
overlay's `hidden` attribute — they never lock body scroll. There is no `overflow: hidden` /
`no-scroll` on `<body>` anywhere.

**Fix direction.**
- On `openSheet`, lock the body (`document.body.classList.add("sheet-open")` +
  `body.sheet-open { overflow: hidden; }`), and on `closeSheet` unlock — but only when the
  *last* open sheet closes (multiple overlays share the state).
- For iOS Safari, `overflow:hidden` alone can leak; the `position: fixed` + saved-scroll-top
  technique is more reliable.
- Add `overscroll-behavior: contain` to the scrollable `.stats-panel` / `.stats-content`.

---

## BUG-2 — Dark mode looks bad on the "generate quiz" / past-paper tab

**Severity:** low–medium (cosmetic, but jarring)

**Symptom.** In dark mode, the **generate-quiz / past-paper** tab renders poorly (light panels /
low-contrast text where the rest of the app is dark).

**Likely cause.** Some of the paper/quiz-generation styles (`.paper-*`, `.quiz-*`, filter chips,
the config screen) use hardcoded light colours (`#fff`, light greys) instead of the theme
variables (`--bg-*`, `--text`, `--border`), so they don't invert with the theme.

**Fix direction.** Audit the generate/quiz styles to use theme tokens, not hardcoded colours;
verify in dark mode. _Needs a screenshot to pinpoint the exact offending elements._

---

## BUG-3 — Past papers show a play button (they're not podcasts)

**Severity:** medium (nonsensical control; implies audio that doesn't exist)

**Symptom.** Past-paper entries (and the Past Papers / `EXAM` module header) display a **play
button** as if they were audio episodes. Papers have no audio — a play button makes no sense.

**Cause.** `renderEpisodeRow()` renders `.ep-play` (plus download / queue buttons) for *every*
episode, and the module header renders a `.module-start` play button — with no special-casing
for paper episodes (`ep.paper === true`) or the `EXAM` module.

**Fix direction.** For paper episodes, hide the play / download / queue controls and have the
row open the paper directly; for the `EXAM` module header, drop the play / download controls.
Papers should simply open the paper config screen.

---

## BUG-4 — Redundant "HSC" prefix on every subject name

**Severity:** low (polish)

**Symptom.** Subjects read "HSC Design and Technology", "HSC Software Engineering", "HSC Physics"
— "HSC" repeats on every tile. Redundant, since the whole app is HSC ("HSC Study").

**Where.** The `name` (and possibly `shortName`) field in each `content/<subject>/subject.json`;
surfaced on the subject tiles / hub and baked into `manifest.json`.

**Fix direction.** Drop the "HSC " prefix from each subject's `name`, then regenerate
`manifest.json`. Keep the overall app title as "HSC Study".

---

## BUG-5 — Generate-quizzes-from-custom-materials UI is hard to use on iOS

**Severity:** medium (usability — blocks a key workflow on the most common device)

**Symptom.** The **generate quizzes from custom materials** UI is difficult to use on an iOS
device (touch targets / layout / file input).

**Where.** The custom-materials quiz-generation flow (same area as BUG-2's dark-mode issue).

**Fix direction.** Audit touch-target sizes, input / upload controls, and layout on iOS; test in
the installed PWA. _Needs specifics / a screenshot to pinpoint the worst offenders._ Related to
BUG-2 (dark mode on the same tab).

---

## BUG-6 — Weak graphics support + thin flashcard / memorisation feature set

**Severity:** medium (feature gap — the memorisation side is underdeveloped)

**Symptom.** Graphics don't work very well, and there isn't much built for **flashcards /
memorising** — the memorisation experience is thin (few card types, limited visual aids).

**Where.** Quiz/flashcard rendering (image handling, e.g. `.quiz-stimulus`) and the overall
flashcard feature set. Closely tied to the conceptual gap in
[`quiz-issues.md`](quiz-issues.md) → Q2 (spaced-repetition flashcards aren't modelled as a
distinct thing from exam questions).

**Fix direction.**
- Fix image rendering/scaling in cards so graphics display reliably.
- Add memorisation-oriented card types and aids — e.g. image occlusion, cloze / fill-in-the-blank,
  diagram labelling, visual mnemonics.
- This depends on the Q2 decision about what a "flashcard" actually is (a real card type distinct
  from an exam question).

---

## BUG-7 — Page scrolls sideways on phones, clipping the left edge (wide equations)

**Severity:** medium (content becomes unreadable — left edge of everything cut off)

**Symptom.** Intermittently on a phone, the whole page shifts left and the left edge of every
element is clipped (header, episode title, headings, body text). Seen on an episode with block
math (Millikan's Oil Drop, Physics).

**Cause (confirmed).** KaTeX **display math had no width containment** (code blocks did, via
`pre code { overflow-x: auto }`, but math did not), and there's no horizontal-overflow guard on
`html`/`body`. A single wide block equation renders past the viewport width → the page becomes
wider than the screen → it scrolls horizontally → everything shifts and the left is cut off.

**Status:** ✅ **Fixed** — commit `109ea84` (on `main`, pending deploy). Display math now scrolls
inside its own box (`.katex-display { overflow-x: auto; max-width: 100% }`).

_Optional extra robustness (not done): a body-level `overflow-x` guard — skipped because it can
break the sticky header; containing the math resolves the observed case._

---

## BUG-8 — Home screen (daily-quiz button) breaks if manifest.json fails to load

**Severity:** low (only reproduced by an artificial trigger) — but a real robustness gap

**Symptom.** Holding Ctrl+Shift+R for a few seconds fires hundreds of hard reloads; afterwards the
"Start your daily quiz" button (and the rest of the home screen) is gone.

**Cause (confirmed by code).** The home screen only renders *after* `fetch("manifest.json")`
resolves (`app.js` init, ~line 3503). On failure the `.catch` replaces the view with a
"Couldn't load the library" error — **no retry, no fallback**. Normally the service worker serves
`manifest.json` network-first with a **cache fallback**, so blips are invisible — but a **hard
reload bypasses the service worker**, so the storm of SW-bypassing requests gets aborted /
rate-limited and the fetch fails with nothing to fall back to. A normal reload recovers (SW cache
fallback returns).

**Fix direction (safe, unverified — touches the critical load path, so do with care).**
- Retry the manifest fetch 2–3× with short backoff before showing the error.
- Cache the last-good manifest in `localStorage` and fall back to it if the fetch fails (survives
  even a SW-bypassing hard reload).
- The daily-quiz button itself doesn't depend on the manifest — it could render before the fetch,
  so it survives a manifest failure.

**Status:** not fixed — deliberately left blind-unfixed (init path is load-critical and I can't
verify here). Low priority given the artificial trigger.

---

## BUG-9 — "Choose specific topics" quiz button appears on some builds, not others

**Severity:** low (confusing, but a symptom of branch divergence, not a code defect)

**Symptom.** The "Choose specific topics & how many" button below the blue daily-quiz box
sometimes shows, sometimes doesn't.

**Cause (confirmed).** The button (`dq-tune`) was added in commit `90bcbcf` on the
**`glossary-content`** branch and is **not on `main`** (which is what's deployed). So builds from
`glossary-content` have it; builds from `main` don't. Combined with service-worker build caching
(see BUG-8), different loads can serve different cached builds → the button flickers in and out.
It's unconditional where it exists — this is a **branch-divergence / mixed-deploy** artifact, not
a rendering condition.

**Root cause is bigger:** `main` and `glossary-content` have diverged and deploys have gone out
from both. The lasting fix is to **reconcile the two branches** (decide the canonical one, land
90bcbcf's "topic fine-tuning + per-subject split" on it or drop it) and only ever deploy from that.

**Status:** not fixed — needs a branch-reconciliation decision (which is yours to make).

---

## BUG-10 — Headphone / lock-screen button can't pause an episode

**Severity:** medium (real, common annoyance — you can't pause without pulling out the phone)

**Symptom.** Pressing pause on wired/Bluetooth headphones (and likely the lock-screen control)
doesn't pause the episode; you have to use the on-screen button. Seen on a phone at 4.5× speed.

**Likely cause.** Playback runs through the **Web Audio pitch-preserving speed engine**
(`speed-engine.js`) — used for pitch preservation and required above ~4× (browsers mute plain
`<audio>.playbackRate` past ~4×). iOS routes Media Session / headphone / lock-screen controls to a
real **HTMLMediaElement**, not a Web Audio `AudioContext`. So when sound comes from the engine, the
headphone "pause" either never reaches the app, or fires `audio.pause()` on the raw element that
isn't the audible source — while the engine keeps playing. The on-screen button works because it
goes through the app's engine-aware toggle. (`setupMediaSession()` ~line 723; the handlers call
`audio.pause()`/`audio.play()` directly.)

**Fix direction (needs on-device testing — not fixable blind).**
- Route the Media Session `play`/`pause` handlers to the **same engine-aware toggle** the on-screen
  button uses, not raw `audio.pause()`.
- Keep a silent HTMLMediaElement "playing" so iOS surfaces and routes the media controls while the
  engine produces the actual sound; keep `navigator.mediaSession.playbackState` in sync.
- Verify at 1× (raw audio) vs >4× (engine) — the behaviour may differ between the two paths.

**Status:** not fixed — device-specific (iOS Media Session + Web Audio), can't verify here.

---

## BUG-11 — Software Engineering "Software Automation": AI-vs-ML episode out of order

**Type:** content / ordering. **Severity:** medium (breaks the intended learning sequence).
The "What is AI vs ML" episode (`content/software/SA-20-01-What-is-AI-vs-ML`) appears **last** in the
Software Automation module but should be **first** — it's the conceptual intro. Its folder is
numbered `20-01`, so it *should* sort first; something in the module/unit sort
(`tools/generate_manifest.py` sort, or the `SA-20`/`SA-22` prefix split) is putting it last. Fix the
sort so `SA-20-01` leads.

## BUG-12 — Page can still scroll sideways (beyond the math fix)

**Type:** UI. **Severity:** medium. Horizontal sideways-scroll still reported after BUG-7 (which
only contained KaTeX). So another wide element is overflowing the viewport. Needs the offending
screen identified; likely fix is the deferred body-level guard (`overflow-x: clip` on a non-sticky
wrapper) plus containing whatever the wide element is (long table? code line? image?).

## BUG-13 — Episode scripts over-link / interleave → too verbose

**Type:** content style. **Severity:** low–medium. Episodes cross-reference other topics too much
("Interleave backward…", "Back in Programming for the Web…"), making narration verbose. Dial down
the density of interleaving/linking in the script-generation prompt.

## BUG-14 — Module download icon doesn't show "downloaded" when all episodes are

**Type:** UI. **Severity:** low. When every episode in a sub-section is downloaded individually, the
module-level download icon should show the downloaded (✓) state. Logic exists
(`syncModuleDlBtn`, `app.js` ~1375, toggles `dl-done` on `allDl`) but isn't reliably reflecting the
all-downloaded state — check it's called after each episode download completes.

## BUG-15 — Won't stream on mobile data (should stream, not download-then-play)

**Type:** playback. **Severity:** medium. On mobile data an episode won't play / seems to require a
full download first; it should **stream** from R2. The block-mobile-data guard (`mayDownload`,
`blockMobileData`) is meant to gate *downloads*, not streaming — check `guardPlayable`/`loadEpisode`
aren't blocking plain streaming on a cellular link.

## BUG-16 — Inter-question audio breaks too short (want ~3s wall-time)

**Type:** content / audio generation. **Severity:** low. The pause between quiz questions in an
episode should be ~3 seconds of wall time so the listener can answer. These silences are baked into
the generated audio (the app-side only has a 1200ms *title* break), so this is an
audio-generation-pipeline change, not app code.

## BUG-17 — Glossaries frequently missing (e.g. AI vs ML) — recurring

**Type:** content pipeline. **Severity:** medium (recurring). **Why it keeps happening:** the
glossary is a **single subject-wide file** (`content/software/GLOSSARY.md`), created by a separate
manual step — it is **not generated per episode**. So any new/updated episode (AI vs ML) has no
glossary coverage until someone regenerates the whole subject glossary. Fix: generate/merge glossary
terms **per episode** as part of the episode pipeline, so coverage can't drift.

## FEATURE-1 — Run Python code in the app

**Type:** feature (not a bug). For the Software Engineering course — an in-app Python runner. Would
need a sandboxed interpreter (e.g. Pyodide/WASM) loaded on demand. Sizeable; scope separately.

## FEATURE-2 — "Jump to current position" button in the script

**Type:** feature. **Severity:** medium (navigation — easy to get lost after scrolling).
When reading the episode script/transcript, the user can scroll away from where the audio is
currently playing and then can't easily get back. Add a button that **scrolls the script back to
the line/position currently being played**. Should appear (or highlight) when the view is scrolled
away from the active position; tapping it re-centres on the current playback point.

**Status:** ✅ **Built** (glossary-content, not deployed). Floating "Now playing" pill on the Script
tab; appears when the active paragraph scrolls off-screen, taps to re-centre. Built on the existing
`syncActiveEl` transcript sync (`updateJumpCurrentBtn`, `btn-jump-current`). Not yet device-verified.

## FEATURE-3 — Settings toggle: "high-speed" vs "screen-off / low-speed" playback mode

**Type:** feature. **Severity:** medium (the two modes have a real trade-off today).
Add a toggle switch in **Settings** letting the user choose whether the player is optimised for:
- **High speed** — the Web Audio pitch-preserving speed engine (`speed-engine.js`), needed above
  ~4× (see BUG-22), but fragile with screen off / backgrounded.
- **Low speed, screen-off** — native `<audio>` playback, which keeps playing reliably with the
  screen off / app backgrounded but can't hit the very high tempos.

The toggle picks which engine drives playback. Ties into BUG-10 / BUG-22 (Media Session +
AudioContext backgrounding). Should also drive FEATURE-5's speed control (see below).

**Status:** ✅ **Built as a real engine change** (glossary-content, not deployed). Confirmed from the
code that this *must* be an engine change, not UI-only: native `<audio>` backgrounds but browsers
mute `playbackRate` >~4×; the Web Audio engine does 16× but its `AudioContext` **cannot** play in the
background on iOS (OS limit — not fixable). So the **"Screen-off mode" toggle** switches the backend:
ON → native (0.5–2× dropdown, plays screen-off); OFF → Web Audio engine (to 16×, screen must stay on).
Reconciler `syncEngine()` + intent key `podcast-hs-engine` so it composes with the old alt-engine
toggle without clobbering it. **Default: ON (screen-off)** — a one-time migration keeps existing
high-speed users (engine on, or saved speed >2×) in high-speed mode. ⚠️ Background behaviour needs
on-device (iOS) verification. NB: contradicts the `audio-speed-priorities` memory (high speed
imperative) — default was a deliberate user call on 2026-07-08.

## FEATURE-4 — Cross (×) button to minimise the now-playing episode

**Type:** feature. **Severity:** medium (the now-playing panel eats valuable screen space).
The currently-playing episode panel takes up too much room. Add a **cross / close (×) button** that
**minimises** it (collapse to a compact mini-player bar) without stopping playback, freeing up the
space. Tapping the minimised bar should restore the full panel.

**Status:** ✅ **Built** (glossary-content, not deployed). Chevron/✕ button collapses `#player-bar`
to a slim title + mini play button (`applyPlayerMin`, `PLAYER_MIN_KEY`); tap the bar to expand.
Persisted. Not yet device-verified.

## FEATURE-5 — Dropdown speed picker (in low-speed mode) instead of the large slider

**Type:** feature. **Severity:** medium. When the user has selected the **low-speed / screen-off**
option (FEATURE-3), replace the large speed **slider** with a compact **speed button** that, when
tapped, **opens a dropdown menu** of preset speeds to choose from:

> **0.5 · 0.75 · 1 · 1.25 · 1.5 · 1.75 · 2**

Tapping the button opens the menu; selecting a value sets the speed and closes it. (Preferred over a
cyclic toggle — direct selection, no tapping through every step.) The large slider stays for
high-speed mode where the wide continuous range matters.

**Status:** ✅ **Built** (glossary-content, not deployed). In screen-off mode the slider is replaced
by `#speed-picker-btn`, which opens a dropdown of 0.5·0.75·1·1.25·1.5·1.75·2 (`buildSpeedPickerMenu`).
Gated by the FEATURE-3 mode (`applySpeedUI`). Not yet device-verified.

## FEATURE-6 — Onboarding: suggest & search subjects when no preferences exist (scales to ~100+ subjects)

**Type:** feature. **Severity:** high (blocker for scaling — the current UI can't handle ~100
subjects). A large batch of subjects (~100+) is about to be added; the current subject UI (tile
grid / hub) doesn't scale to that many. Add an **onboarding step** that triggers **when there are no
preferences at all in `localStorage`** (first run / clean state):

- On first run with no saved preferences, present a **subject picker with search** — the user
  searches for the subjects they want and selects them, rather than scrolling a wall of ~100 tiles.
- Persist the chosen subjects to `localStorage`; thereafter the hub shows only the selected
  subjects (with a way to edit the selection later, e.g. in Settings).
- This gates the whole app behind a manageable, searchable selection instead of rendering every
  subject up front.

**Status:** ✅ **Built** (glossary-content, not deployed). First-run picker (`#subjects-overlay`,
`openSubjectPicker`/`maybeOnboard`) fires when `podcast-onboarded` is unset; searchable checklist of
all subjects (manifest + generator banks); saves ids to `podcast-subjects`; `renderSubjects()` filters
to the chosen set; "Edit subjects" in Settings and on the grid re-opens it. Not yet device-verified.

## FEATURE-7 — Transfer the past-paper generator to the canonical papers structure

**Type:** feature / refactor. **Severity:** high (unblocks clean, current-syllabus paper
generation and scales as papers keep arriving). A canonical papers layout now exists and is
documented as a contract in [`docs/papers-structure.md`](papers-structure.md): raw ingest lives
in `papers/` (source of truth), and `tools/organize_papers.py` derives `papers_organized/<Subject>/{Papers/{HSC,Trial,Yearly-Y11}, Other, Resources, Archive-pre-<cutoff>}`
from it (cutoffs in `tools/syllabus_cutoffs.json`).

The generator ingestion currently reads the **raw** layout via `papers/_index.json`, so it mixes
syllabus eras and content types (old-syllabus papers, notes, half-yearlies all together). Migrate
it to consume the **organized contract** instead:

- Build the question bank from **`Papers/**` only** (current-syllabus HSC + Trial + Yearly-Y11);
  **exclude `Archive-pre-*`** from default generation (optionally selectable as "older syllabus").
- Treat **`Resources/`** as supplementary (notes/essays) — never questions — and **`Other/`** as
  opt-in non-standard material, not part of the core exam bank.
- Drive off the layout / `papers_organized/_MANIFEST.json` (subject + bucket + cutoff), not raw
  category folders, so new years and new papers flow in with no code change.
- Update the ingestion stages (`tools/index_papers.py` → parse-papers → generator manifest) and the
  ingestion section of [`docs/past-paper-generator.md`](past-paper-generator.md) §4 to point at the
  organized tree.
- Follow-on: add authoritative syllabus cutoffs for the language/VET subjects (see
  `docs/papers-structure.md` §4) so their archives are correct too.

## CONTENT-1 — Verify AI-vs-ML narration accuracy

**Type:** content review. The pasted "AI vs ML" narration is **substantially correct** for HSC
(expert systems = rule-based AI that doesn't learn; ML = subset of AI that learns patterns from
data; if-statements ≠ AI; ML is one technique to achieve AI; big-data 3 Vs as ML fuel). **One
overstatement to fix:** "no big data, no machine learning" — ML does **not** strictly require big
data (small-data ML exists); big data made *deep learning* powerful. Soften that line.

---

## BUG-18 — Starting the title/quiz voice doesn't pause the playing episode

**Type:** playback. **Severity:** medium. When the spoken title-intro / quiz voice starts, the
currently-playing episode audio doesn't pause — the two overlap. Check `playTitleIntro`
(`app.js` ~906) and the load path pause the main `audio` before the intro/quiz clip plays.

**Re-reported 2026-07-08 (same bug, raise priority):** on starting an episode the **title TTS and the
episode audio play at the same time** — two voices at once from the very first moment. Confirms the
title intro isn't gating the main `audio.play()` (or vice-versa). Ensure the title clip finishes (or
is skippable) before the episode audio begins.

## BUG-19 — Progress not saved when advancing to the next episode offline

**Type:** playback / persistence. **Severity:** medium. Jumping to the next episode while offline
loses the outgoing episode's progress. `persistProgress()` fires on `pause` (~738) and periodically
(~789), but the auto-advance / "next" path (~888) may switch episodes without persisting the
outgoing one first. Ensure `persistProgress()` runs for the current episode *before* the src
changes. (localStorage works offline, so this is an ordering issue, not a network one.)

## BUG-20 — Quiz reveals the correct answer (in blue) before you answer

**Type:** quiz. **Severity:** high (defeats the quiz — you can just pick the highlighted one).
The correct option is visually flagged before the user chooses. The reveal that adds
`opt-correct`/`opt-wrong` (`app.js` ~2519 / ~2681) should only run *after* an answer is submitted —
right now it appears to fire early (or a selected/accent style is applied to the correct option on
render). Repro/screenshot would pin which path. Also check the `.quiz-option` colours — the reveal
is meant to be green/red, not accent-blue.

## BUG-21 — Multiple-choice questions are treated as flashcard "quizzes"

**Type:** quiz design. **Severity:** high. MC questions are being run as spaced-repetition quizzes
when they shouldn't be; the desired experience is **open-ended recall** questions (e.g. "Name three
types of models"), not pick-one MC. This is the concrete form of the conceptual split already in
[`quiz-issues.md`](quiz-issues.md) → **Q2** (flashcards vs exam-question drilling). Needs the
card-type model: separate "recall flashcard" from "multiple-choice question", and don't feed MC
into the SR flashcard queue.

## BUG-22 — Audio drops out ~every 1–2s at 7×; orientation change can stop playback

**Type:** audio engine. **Severity:** HIGH (user-flagged priority — high speeds unusable; fragile). At ~7× the Web
Audio speed engine (`speed-engine.js`) drops audio every second or two (buffer underruns in the
time-stretch worklet at high tempo), and rotating the phone can stop playback entirely (AudioContext
suspends on the visibility/orientation change and doesn't resume). Same subsystem as BUG-10; the
engine is fragile at extreme tempo. Fix direction: larger/again-filled worklet buffers at high
tempo; resume the `AudioContext` on `visibilitychange`/`resize`/orientation events.

**Status (partial):** ✅ **Orientation/backgrounding half fixed** — commit `48dd671` (on `main`,
pending deploy): the AudioContext now auto-resumes when suspended while the user intends to play.
⏸ **7× dropout NOT fixed** — it's in the WSOLA time-stretch DSP / audio-thread buffering; can't be
changed safely blind (risks breaking all audio), needs on-device profiling + listening.

---

## FEATURE-7 — Software study decks (Memorisation + Episode Content) + a "Review deck" setting

**Type:** feature (flashcards / review). **Status:** _content DONE, app-logic NOT started — this is a
handoff to whoever owns the UI._ Fills out BUG-6 and is the concrete home for the card-type split in
BUG-21 / `quiz-issues.md` → Q2.

**What already exists (content side, on the `glossary-content` working tree — do not redo):**
Two new module prefixes under `content/software/`, each a set of **card-only, audio-less** episodes
(`quiz.json` + a stub `script.md`; picked up by `tools/generate_manifest.py`, already in
`manifest.json`):

| Prefix | Section name (subject.json `groupNames`) | Episodes | Cards | `source.origin` |
|---|---|---|---|---|
| `MEM-*` | **Memorisation** | SSA · PFW · SA · SEE syllabus-list recall + one **Acronyms & Abbreviations** set (5 episodes) | `type:"recall"` rote lists / acronyms | `"syllabus"` |
| `EPC-*` | **Episode Content** | SSA · PFW · SA · SEE (4 episodes) | `type:"recall"` concept cards distilled from the episode scripts | `"ai"` |

`subject.json` maps both prefixes to a `"Revision decks"` year bucket so they surface as two sections
above the normal modules. Generator for the rote cards: `tools/build_mem_deck.py`. All cards use the
existing `type:"recall"` shape (front `q` → reveal `keyPoints[]` → FSRS self-grade), so **no new
renderer is needed** — DT episodes already render this type.

**What the UI/app needs (deliberately left unimplemented so it doesn't collide with your work):**

1. **Deck tagging.** In `loadAllQuestions()` (~app.js:3232) tag each question by its module prefix, e.g.
   `q._deck = q.deck || (prefix === "MEM" ? "memorise" : prefix === "EPC" ? "content" : "quiz")`.

2. **"Review deck" setting** in Settings → Flashcards. A `<select id="root-review-deck">` persisted to
   localStorage key `podcast-root-review-deck`. **Recommended options:** _Memorisation_ (`memorise`),
   _Episode Content_ (`content`), _Applied — episode questions_ (`quiz`), _All mixed_ (`both`).
   **Default `memorise`** (confirmed product decision — root review is rote recall by default; the 840
   applied cards stay reachable per-episode and via this setting). Load the value when the settings
   sheet opens; save on `change`; refresh the review badge.

3. **Filter the ROOT review only, with per-subject graceful fallback.** Apply the setting where the
   root pool is built — `startDailyQuiz()` (~app.js:3400) and `renderReviewHub()` (~3275) — via a helper.
   Fallback is essential: only Software has MEM/EPC decks, so Physics/DT must fall back to their own
   cards instead of showing an empty review:
   ```js
   function applyDeck(list){
     const d = rootReviewDeck();            // localStorage podcast-root-review-deck, default "memorise"
     if (d === "both") return list;
     const by = {};
     list.forEach(q => (by[q._subject] || (by[q._subject] = [])).push(q));
     const out = [];
     Object.values(by).forEach(arr => {
       const f = arr.filter(q => (q._deck || "quiz") === d);
       out.push(...(f.length ? f : arr));   // empty in this subject → keep its own cards
     });
     return out;
   }
   // then:  const all = applyDeck(await loadAllQuestions());
   ```
   Verified against the real manifest (Node/Python sim, since the Chrome tool can't reach localhost):
   default `memorise` → Software root review = its 145 memorisation cards only; Physics/DT fall back to
   their applied cards; `quiz` → Software's 840 applied cards, no MEM/EPC; `both` → everything.

4. **Do NOT filter the per-episode quiz.** The Quiz tab shown after an episode (`renderQuizTab`) must keep
   serving that episode's own cards regardless of the setting — don't route it through `applyDeck`.

5. **Two-section browse display.** Render the `MEM` and `EPC` modules as two labelled sections
   ("Memorisation", "Episode Content"), each listing its topic episodes. They are audio-less/read-only
   (already handled ~app.js:883) — opening one shows the short intro script + the Quiz tab of recall
   cards, and must show **no play button** (cf. BUG-3).

6. **Badge (optional).** Decide whether `reviewsDueCount()` counts only the active deck or all decks.
   Today it scans SR keys by subject prefix and is deck-agnostic; a mismatch (badge counts a card the
   session won't serve) is acceptable for v1 — just note it.

**Open product call for you/user:** whether the setting exposes Episode Content as its own option (4-way,
as recommended above) or folds MEM+EPC into a single "revision" value (3-way: Revision / Applied / Both).
The content supports either; `applyDeck` above handles any `_deck` value.

Cross-refs: **BUG-6** (thin flashcard/memorisation feature set — this is the fill), **BUG-21** (keep MC out
of the SR flashcard queue / recall-vs-MC card types), `quiz-issues.md` → **Q2**.

---

## Related (logged elsewhere)
- **Redundant / unstyled Exit in the Review overlay** — see `quiz-issues.md` → Q3.

_None started — parked for a later session._

---

## FEATURE-8 — Generator top-level mode toggle: "Browse raw papers" vs "Build revision paper"

**Type:** feature (past-paper generator UX). **Severity:** medium — shapes the generator's whole entry point.

**Want.** A toggle at the top of the past-paper generator to choose what you're doing:

1. **Browse raw papers** — view whole past papers *as-is* (the original paper, unmodified), with
   filters: **school / source**, **year range**, **exam type** (HSC / Trial / Yearly / Half-yearly).
   Pick a paper → view or print the whole thing (and its solutions, once the solutions pipeline lands).
   This is for revising a specific real paper, or printing a full paper to sit.
2. **Build revision paper** — the existing custom-assembly flow (hand-pick basket + "build by recipe")
   that generates a *new* revision paper from past-paper question material.

**Why.** Right now the generator only does mode 2 (assemble your own). Users often just want to do a
whole real past paper — browse by school/year and print it — without building anything. The toggle makes
both first-class instead of burying "view a real paper" inside the question-picker.

**Direction.**
- Top-level segmented toggle (like the existing hand/recipe control, one level up): **Raw papers | Build paper**.
- Raw mode = a filtered list of whole papers (reuse the school/year/type facets already in the left rail),
  each opening to view/print the full paper PDF + solutions.
- This is also the natural home for the **pre-2020 old-syllabus papers** (out of scope for segmentation):
  they can't be diced into questions, but they can be listed and printed whole here.
- Cross-refs: **FEATURE-7** (canonical papers structure), and the solutions pipeline (real + AI-filled
  solutions become the printable answer pages in raw mode).

_Not started — logged 2026-07-08._

---

_(Numbers below chosen to avoid the concurrent-session collisions above — two FEATURE-7s and a
FEATURE-8 already exist. Renumber when the branches are reconciled.)_

## FEATURE-9 — Sync must be automatic, not just on button-press

**Type:** sync / persistence. **Severity:** high (without it, cross-device sync is basically useless).
Right now cloud sync only happens when the user **manually taps the sync button**. It needs to push to
the cloud **automatically**: after every couple of minutes of playback, after each flashcard review,
and at the end of a session — so progress actually shows up on other devices without thinking about it.
As it stands the feature is trivial/pointless because you have to remember to press the button.

**Fix direction.** Add debounced/throttled auto-push triggers to the existing sync (`window.Sync`):
a periodic timer during playback (~2 min), a hook on flashcard grade/complete, and a flush on
`pause` / `visibilitychange` (session end / app backgrounded). Reuse the same push the button calls;
guard against overlapping pushes and no-op when nothing changed. Pair with pull-on-open so a device
picks up remote progress on launch.

## BUG-23 — TTS voices broken in the installed PWA but fine in the browser (recurring)

**Type:** audio / PWA. **Severity:** medium–high (recurring). The narration **voices break when the app
is run as an installed PWA**, yet work correctly in a normal browser tab. This keeps coming back.
**Why it likely recurs:** installed-PWA audio differs from a browser tab — a different service-worker
cache scope, stricter autoplay/audio-session handling, and (if any voice path uses the Web Speech
`speechSynthesis` API) the installed standalone context often has **no/limited system voices** where the
browser does. Investigate: is the broken path the SpeechSynthesis API or a fetched audio file? If the
former, it can't be relied on in a PWA — bake/serve the audio instead. If the latter, it's a
service-worker caching/range-request issue specific to standalone mode. Needs on-device (installed PWA)
repro to pin which. Related: BUG-15 (streaming), BUG-8 (SW caching).

## BUG-24 — Glossaries don't contain the recap acronyms

**Type:** content pipeline. **Severity:** medium. The subject glossaries are **missing the recap
acronyms/abbreviations** (the short forms introduced in episodes). The FEATURE-7 "Memorisation" deck
adds an **Acronyms & Abbreviations** MEM set, but the **glossary** itself still doesn't carry those
terms. Fix: fold acronyms/abbreviations into the per-episode glossary generation so they're defined in
the glossary too, not only in the flashcard deck. Same root cause as **BUG-17** (glossary built as a
separate manual step, so coverage drifts) — the durable fix is to generate glossary terms (incl.
acronyms) per episode as part of the pipeline.

## BUG-25 — Paper generator UI looks bad on iOS; back button hidden under the status-bar clock

**Type:** UI / iOS. **Severity:** medium. The **past-paper generator** (`generator.html`) renders poorly
on iOS: the layout is messy and the **back button is obscured by the iOS status-bar time** (the header
sits under the notch/status bar). Almost certainly a **safe-area-inset** problem — the generator's header
doesn't pad for `env(safe-area-inset-top)` (and the page may be missing `viewport-fit=cover` handling
that `index.html` has). Fix: apply `padding-top: env(safe-area-inset-top)` to the generator header/top
bar, verify `viewport-fit=cover` + `apple-mobile-web-app-status-bar-style` are set consistently with the
main app, and audit the generator's spacing/controls on a real iPhone. The main app's header already
handles this — port the same treatment to `generator.html`. Related: BUG-2 / BUG-5 (generator UI on iOS).

_Not started — logged 2026-07-08._
