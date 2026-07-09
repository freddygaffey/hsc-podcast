> ⛔ STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# Bug-fix list

_Running list of concrete UI / behaviour bugs to fix later. Design-level quiz issues
(provenance labelling, flashcards-vs-HSC-drilling) live in [`quiz-issues.md`](quiz-issues.md).
Logged 2026-07-02._

> **Bugs that came back:** see [`regression-log.md`](regression-log.md) for the five bugs that were
> fixed, regressed, and re-resolved (the auto-advance loop, sideways scroll, the audio-engine saga,
> vanishing DT quizzes, parallel-session clobbering) — with the guard that should stop each recurring.
> The BUG-36 background-audio saga has its own trace: [`audio-background-resume.md`](audio-background-resume.md).

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

## BUG-25 — Paper generator UI looks bad on iOS; back button obscured under the status-bar clock and not clickable

**Type:** UI / iOS. **Severity:** medium. The **past-paper generator** (`generator.html`) renders poorly
on iOS: the layout is messy and the **back button is obscured by the iOS status-bar time** (the header
sits under the notch/status bar). Crucially, the back button **exists but is not accessible / clickable**
— it isn't missing; it's hidden under the status-bar region, which both covers it *and* intercepts the
tap, so you can't press it to leave the generator (you can get stuck). Almost certainly a
**safe-area-inset** problem — the generator's header doesn't pad for `env(safe-area-inset-top)` (and the
page may be missing `viewport-fit=cover` handling that `index.html` has).

**Fix.** Apply `padding-top: env(safe-area-inset-top)` to the generator header/top bar, verify
`viewport-fit=cover` + `apple-mobile-web-app-status-bar-style` are set consistently with the main app,
and audit the generator's spacing/controls on a real iPhone. The main app's header already handles
this — port the same treatment to `generator.html`. Then **confirm the back button both clears the notch
_and_ responds to a tap**; if it's still unclickable after the safe-area fix, check for an overlay /
`z-index` / `pointer-events` element covering it and intercepting taps. Related: BUG-2 / BUG-5 (generator
UI on iOS).

_(Merged in the former BUG-29 — "back button present but not clickable" — 2026-07-08; same root cause.)_

_Not started — logged 2026-07-08._

## FEATURE-10 — Drag to reorder subjects (persisted + synced)

**Type:** feature (subject hub UX). **Severity:** medium — with the onboarding picker landing (FEATURE-6)
and ~100 subjects incoming, users need control over which subjects sit at the top.

**Want.** Let the user **drag subjects to reorder them** in the subject UI (the hub / tile grid), so the
ones they care about sit where they want. The chosen order must be **saved** (persisted locally) **and
synced** to the cloud so it carries across devices.

**Fix direction.**
- Make the subject tiles in `renderSubjects()` drag-reorderable — HTML5 drag-and-drop (or pointer-based
  drag with a touch fallback, since the primary device is iOS and native DnD is flaky on touch). Add a
  clear drag affordance (handle) and reorder on drop.
- Persist the order to a `localStorage` key (e.g. `podcast-subject-order`) as an array of subject ids;
  `renderSubjects()` sorts the selected set by that order, with any unlisted/new subjects appended.
- **Sync it.** Fold `podcast-subject-order` into the same `window.Sync` payload as the other prefs so it
  pushes/pulls with progress — ties into **FEATURE-9** (make sync automatic) so a reorder on one device
  shows up on the others without a manual push.
- Compose with **FEATURE-6**: the onboarding subject picker chooses *which* subjects show; this chooses
  *what order* they show in. Editing the selection later shouldn't clobber an existing order.

_Not started — logged 2026-07-08._

---

## FEATURE-11 — Migrate paper assets to a dedicated `hsc-papers-and-resources` bucket

**Type:** infrastructure / migration. **Design:** parser agent; **implementation:** code-changes agent. **Severity:** high — unblocks clean paper hosting + raw-paper browsing (FEATURE-8).

**Decision (Fred):** separate *paper assets* from *audio*. Audio stays in `hsc-podcast-audio`; ALL paper assets move to a new dedicated bucket **`hsc-papers-and-resources`** (already created, empty). Cleaner lifecycle, and it hosts *every raw paper* — including ones never segmented ("I just want to have papers").

**Current state**
- App reads `assetBaseUrl = https://audio.hsc.pebnum.com` (= `hsc-podcast-audio`). Paper crops live at `hsc-podcast-audio/<subject>/papers/<slug>/` — old boundaries-pipeline output, patchy, with `-1` dedup cruft.
- Half-done `hsc-questions` bucket exists (`<subject>/<slug>/` layout, ~2.2k maths-adv files) — NOT wired to the app.
- New `hsc-papers-and-resources` exists, empty.

**Target layout** (`hsc-papers-and-resources`):
```
<subject>/papers/<slug>/
   paper.pdf          full raw paper — uploaded for EVERY paper, segmented or not
   q01.pdf q11.pdf …  question crops (with-lines variant)
   q01-c.pdf …        compact / no-lines variant
   a01.pdf …          solution crops (real) + AI-generated solutions (watermarked)
```
slug = `<year>-<school>-<type>` (e.g. `2024-barker-trial`); one consistent `paperId → slug` map across upload + manifest.

**Migration steps**
1. Bind a custom domain (e.g. `papers.hsc.pebnum.com`) → `hsc-papers-and-resources` (R2 custom domain + DNS).
2. Upload every paper's source PDF → `<subject>/papers/<slug>/paper.pdf` (all papers; unblocks raw-browse / FEATURE-8).
3. Copy existing crops `hsc-podcast-audio/<subject>/papers/` → new bucket; reconcile with `hsc-questions` (dedupe, prefer complete). `rclone copy` (additive).
4. Bake the 247 verified `split.json` → crops → new bucket (see bake fix below).
5. Repoint app: `content/*/subject.json` → `assetBaseUrl = https://papers.hsc.pebnum.com`; keep `audioBaseUrl` on audio.hsc.pebnum.com. Check `generator.html` / `app.js` build crop URLs from `assetBaseUrl`.
6. Point `upload_questions.py`, `sync_bucket.py` (+ deploy scripts) at `hsc-papers-and-resources` for papers; audio tooling unchanged.
7. Cleanup (after verify — sync-deletes authorized by Fred): remove old paper crops from `hsc-podcast-audio`; fold `hsc-questions` in, then delete it. Do NOT delete `hsc-podcast-audio` (audio). Inventory `hsc-podcast` (54 GB, unknown owner) before touching.

**BLOCKER — fix `bake_split.py` before any crop upload:**
- **Page off-by-one:** `split.json` `page` is 1-based, but the bake uses it as 0-based for both `fitz.show_pdf_page(...)` and `info["pages"][page]`. Change both to `page-1`. *Verified:* unit `q1` baked as Question 4; rendering `page-1` gives the correct Question 1. Without this, **every crop is one page off.**
- Only bakes `regions[0]` — must bake **all** regions (multi-page/continued questions lose content).
- Resolve the source PDF via `_index.json` (paperId→current path), not the frozen `info.json` path (Fred reworked `papers/`; frozen paths go stale).
- Add the two variants (with-lines / no-lines) from the `writingSpace` bands.

_Not started — logged 2026-07-08. Bucket created; app currently still serves from hsc-podcast-audio._

---

## BUG-26 — "Download all voices" toggle doesn't back-propagate + no large-download warning

**Type:** downloads / settings. **Severity:** medium. Two related gaps in the Settings →
**"Download all voices"** toggle (`DOWNLOAD_ALL_VOICES_KEY`, `app.js` ~1687):

1. **No back-propagation.** Ticking the box only sets the flag for *future* downloads
   (`chosenVoiceNames` returns all voices when set). Episodes already saved to disk keep just
   their single default voice — the extra voices are **never back-filled**. Expected: turning the
   toggle on should download the missing voices for episodes that are already downloaded (walk the
   saved-downloads records, fetch each episode's not-yet-cached voices, update its `voices` list).
2. **No size warning.** Back-filling every voice across all saved episodes can be many GB. It
   should **warn / confirm before downloading more than ~10 GB** of additional voice data
   (estimate the extra bytes for the missing voices — cf. `estEpisodeBytes` / `EST_BYTES_PER_SEC` —
   and gate on a confirm). If the user declines, revert the toggle so it reflects reality.

Should also respect the existing mobile-data guard (`mayDownload`). Cross-ref: BUG-14 (module
download state), BUG-15 (streaming vs download).

## BUG-27 — Speed picker (≤2× screen-off mode): speed options open off-screen / can't be changed

**Type:** UI / player. **Severity:** medium (you can't change speed at all in this mode). In the
**low-speed / screen-off** playback mode the large slider is replaced by the dropdown speed picker
(FEATURE-5, `#speed-picker-btn` / `buildSpeedPickerMenu`, presets 0.5·0.75·1·1.25·1.5·1.75·2). The
menu of speed options **opens upward / off the top of the screen**, so the options are unreachable
and the speed can't be changed. Fix direction: position the picker menu within the viewport (open
downward, or clamp/flip it so it stays on-screen and scrollable). _Needs a screenshot to confirm
which way it overflows._ Cross-ref: FEATURE-3 / FEATURE-5 (screen-off mode + dropdown picker).

_Not started — logged 2026-07-08._

---

## FEATURE-12 — Usage telemetry: log user activity to a database

**Type:** feature (analytics / instrumentation). **Severity:** medium — no visibility today into how
the app is actually used; every product decision (which subjects/episodes matter, whether high-speed
playback is used, where quizzes drop off) is currently guesswork.

**Want.** Client-side event logging that writes to a **server-side database** so you can see *how* and
*what* people use in the app — which subjects/episodes are opened, play/pause and completion, playback
speed actually used, downloads, quiz/flashcard starts + grades, onboarding subject choices, PWA vs
browser, install events, errors.

**Direction (Cloudflare-native — the app already deploys on Cloudflare Pages, `deploy.sh`).**
- **Ingest endpoint.** A small **Cloudflare Worker** (e.g. `/api/track` route, or a Pages Function) that
  accepts batched JSON events over `POST` and writes them. Keep it same-origin so no CORS/adblock hit.
- **Store.** Two sensible options — pick per query pattern:
  - **Workers Analytics Engine** — purpose-built for high-write, low-cost event telemetry; query with the
    GraphQL/SQL analytics API. Best if these are fire-and-forget metrics.
  - **D1** (SQLite) — if you want to run arbitrary SQL / joins over raw events and keep full rows.
  - (R2 for cheap raw-event archival is a third, if volume grows.)
- **Client.** A tiny `track(event, props)` helper in `app.js` that buffers events and flushes on a timer
  and on `visibilitychange`/`pagehide` via `navigator.sendBeacon` (survives backgrounding — matters on
  iOS). Attach a random, rotating **anonymous client id** (localStorage), session id, app build/commit
  (already surfaced via `_buildInfo`), and standalone-vs-browser. Instrument the existing choke points:
  `loadEpisode`, play/pause, completion, `setSpeed`, download start/complete, quiz start + grade,
  onboarding save, install prompt.
- **Reliability.** Never block the UI; swallow failures; cap the buffer; drop (don't retry forever) on
  repeated failure. Works alongside — not through — the sync path (`window.Sync`).

**Privacy / consent (do not skip — this is collecting data about real users).**
- Keep it **anonymous**: no names/emails, no free-text, no precise content — event names + coarse props
  only. Rotate the client id; don't join it to the sync account id.
- **Opt-out (decided by Fred):** telemetry is **ON by default**; add a **Settings toggle to opt out**
  ("Share anonymous usage data", checked by default) — logging runs unless the user unticks it. Persist
  the choice to a `localStorage` key and check it in `track()` before buffering/sending. Also honour
  Do-Not-Track / `navigator.connection.saveData` where present.
- Respect the mobile-data posture already in the app (BUG-15) — telemetry beacons are tiny, but don't
  fire chatty logging on a metered link.
- Note it in a short privacy blurb; if any non-anonymous field is ever added, that changes the consent
  requirement.

**Open calls for Fred.** (1) Analytics Engine vs D1 (metrics dashboards vs raw-SQL exploration).
(2) Event taxonomy — the specific list of events/props worth logging.
_(Decided: opt-out — telemetry on by default, Settings toggle to disable.)_

_Not started — logged 2026-07-08._

---

## FEATURE-13 — In-app feedback box (free text → database Fred can read)

**Type:** feature (feedback). **Severity:** medium — no way today for users to tell you what's broken or
what they want; pairs with FEATURE-12 (usage telemetry) but is **explicit, user-initiated** input.

**Want.** A **feedback box** somewhere in the app where a user can type **plain text** and send it; the
message lands in a **database Fred can read**.

**Direction.**
- **UI.** A "Send feedback" entry in **Settings** (simplest home) opening a small sheet: a `<textarea>`
  + Send button, with a short "thanks" confirmation and error/retry on failure. Keep it one field —
  free text only. (Optional later: a category chip — bug / idea / other.)
- **Backend.** Reuse the **same Cloudflare Worker / Pages Function** stood up for FEATURE-12, with a
  separate `/api/feedback` route writing to its own table/dataset. **D1** is the better fit here than
  Analytics Engine (you want to *read individual messages*, not aggregate metrics) — one `feedback`
  table: `id, created_at, message, app_build, standalone, anon_client_id, user_agent`. Reading = a
  simple `SELECT … ORDER BY created_at DESC` (via `wrangler d1 execute` or a tiny admin view).
- **Context to attach (no PII).** App build/commit (`_buildInfo`), standalone-vs-browser, the anonymous
  client id (so you can tie feedback to a session if the telemetry backend is on), locale/timezone.
  **No name/email** unless the user volunteers one in the text.
- **Abuse/robustness.** Cap length (e.g. ≤4 KB), trim empties, basic rate-limit on the Worker, and
  submit via `fetch` (this is a deliberate user action, so a spinner + success/fail is fine — no need
  for `sendBeacon`). Don't block the UI; swallow nothing silently — show the user if it failed.

**Open calls for Fred.** (1) Where the entry point lives (Settings vs a floating "Feedback" button).
(2) Whether to offer an optional contact field so you can reply. (3) Whether to add the category chip.

_Not started — logged 2026-07-08._

---

## FEATURE-14 — Generator toggles: view all past papers · in-syllabus only · build custom paper from multiple tests

**Type:** feature (past-paper generator UX). **Severity:** medium. **Overlaps FEATURE-8** (raw-browse vs
build-paper mode toggle) and **FEATURE-7 / FEATURE-11** (current-syllabus filtering via
`tools/syllabus_cutoffs.json` / the organized papers contract) — **build these together, not twice.**
This entry pins the exact toggles Fred asked for.

**Want — three controls in the generator (`generator.html`):**

1. **Mode toggle: "View all past papers" vs "Build custom paper".** (= FEATURE-8's top-level segmented
   control.) *View* = list every whole past paper as-is → open to view/print the full paper (+ solutions
   once that pipeline lands). *Build* = the existing custom-assembly flow.
2. **In-syllabus toggle.** Filter to **current-syllabus papers only** vs **all papers (incl. old
   syllabus)**. Drive it off the syllabus cutoffs (`tools/syllabus_cutoffs.json` /
   `papers_organized/_MANIFEST.json` buckets: `Papers/**` = current, `Archive-pre-<cutoff>` = old — see
   FEATURE-7). Default **in-syllabus on**. Applies in both modes: hides pre-cutoff papers from the browse
   list, and excludes their questions from custom-paper generation unless toggled off.
3. **Build custom practice paper from multiple tests.** In build mode, let the user assemble one practice
   paper drawing questions from **multiple source papers/tests at once** (mixed by topic/marks/recipe),
   not just one paper — the multi-paper question bank the generator already assembles.

**Direction.**
- Put the mode toggle at the top (segmented, like FEATURE-8: **All papers | Build paper**), and the
  in-syllabus toggle in the left-rail filters alongside school/year/type.
- The in-syllabus filter is one predicate over the paper's bucket/year; apply it to both the browse list
  and the question pool so the two modes stay consistent.
- Multi-test build is largely the existing basket/recipe flow — just make sure the source-paper facet
  allows selecting across papers rather than scoping to one.
- Cross-refs: **FEATURE-8** (mode toggle + home for old-syllabus whole papers), **FEATURE-7** (organized
  papers contract + cutoffs), **FEATURE-11** (paper-asset bucket / raw `paper.pdf` for whole-paper view),
  **BUG-25** (generator iOS layout).

**Open call for Fred.** Confirm whether FEATURE-14 simply *is* FEATURE-8 with the added in-syllabus
toggle (merge into one build) or should stay tracked separately.

_Not started — logged 2026-07-08._

---

## FEATURE-15 — Guided onboarding walkthrough (how to use the app)

**Type:** feature (onboarding / first-run). **Severity:** medium — new users land with no idea what the
app can do; a short guided tour raises activation. **Builds on FEATURE-6** (first-run subject picker) —
this is the *next* step after subjects are chosen, a walkthrough of the core features. Keep the two as
one onboarding flow, not two competing first-run experiences.

**Want.** A first-run guided walkthrough that shows the user, step by step, how to:

1. **Install the app** — how to download/install the PWA to the home screen (the platform-specific
   "Add to Home Screen" step; reuse the existing install prompt / `updateInstallUI`).
2. **Make an account / log in** — how to sign in so progress syncs across devices (ties to `window.Sync`
   / the sign-in flow).
3. **Download past papers** — where to find and save papers for offline use.
4. **Generate a custom paper** — how to build a practice paper in the generator (cf. FEATURE-8/FEATURE-14).
5. **Play audio** — how to start an episode, and the speed controls (incl. screen-off vs high-speed modes,
   FEATURE-3/FEATURE-5).
6. **How the quizzes work** — the flashcard/quiz + spaced-repetition review loop (recall vs MC, cf.
   BUG-21 / FEATURE-7 decks).
7. **Settings** — end by **taking them to the Settings tab** so they see where preferences live (default
   voice, screen-off mode, download-all-voices, feedback, opt-out telemetry, etc.).

**Direction.**
- A dismissible **step-through coach-mark / tooltip tour** (spotlight each target control with a short
  caption + Next/Skip), or a simple sequence of intro cards if per-element anchoring is too fragile on
  mobile. Ends by opening the Settings sheet.
- Trigger on first run (after FEATURE-6's subject pick) — gate on a `localStorage` flag (e.g.
  `podcast-toured`) so it shows once; add a **"Replay walkthrough"** entry in Settings to see it again.
- Each step should be **skippable** and the whole tour dismissible at any point; never block the app.
- Steps must degrade gracefully when a target isn't present (e.g. install step hidden if already
  installed / unsupported; account step reflects signed-in state).
- Cross-refs: **FEATURE-6** (first-run picker — sequence this right after it), **FEATURE-9** (auto-sync,
  for the login step's payoff), **FEATURE-3/5** (playback modes), **FEATURE-8/14** (generator),
  **FEATURE-12/13** (settings items the tour points at).

**Open calls for Fred.** (1) Coach-mark spotlight tour vs plain intro-card carousel (spotlight is nicer
but fiddlier on iOS). (2) Whether the login/account step is mandatory or skippable at onboarding.

_Not started — logged 2026-07-08._

---

## BUG-28 — High-speed engine makes audio unintelligible

**Type:** audio engine. **Severity:** medium–high (defeats the point of high-speed listening — you can't
make out the words). Turning on the **high-speed engine** in Settings (the Web Audio pitch-preserving
speed engine, `speed-engine.js`, intent key `podcast-hs-engine` — the "alt/ultra high-speed" option)
makes the narration sound **unintelligible / heavily distorted**, not just fast. The words smear rather
than staying crisp.

**Likely cause.** The WSOLA / time-stretch DSP in the worklet degrades at speed — frame/overlap or
window parameters produce artefacts (metallic/warbly smearing) that wreck intelligibility even at
moderate multipliers. Same subsystem as **BUG-22** (dropouts at ~7×) and **BUG-10** (Media Session vs
AudioContext), but this is a **quality/clarity** fault, not a dropout or control-routing one.

**Suggested resolution (Fred, 2026-07-08).** With the **high-speed-engine tick box _un_ticked**, fast
playback actually **sounds better** (native `<audio>.playbackRate` — crisp, just pitch-shifted). So the
preferred fix is to **stop routing normal high-speed listening through the special engine** — i.e.
default it **off** / de-emphasise it so the clear native path is what users get by default.
**Do NOT remove the high-speed engine entirely** — it's very good and must stay available (kept as an
opt-in for the very top speeds / pitch preservation where native can't reach). Net: keep the capability,
change the default so unticked (native) is the norm.

**Fix direction (needs on-device listening — can't be tuned blind).**
- **Default the high-speed engine OFF** and make native playback the standard high-speed path; leave the
  engine as an explicit opt-in tick box for users who want the extreme speeds it enables. (Mind the
  existing default/migration in FEATURE-3 so this doesn't fight the screen-off-mode default.)
- Separately, still worth profiling/tuning the engine's time-stretch params (analysis/synthesis frame
  size, overlap/hop, search window) for clarity when it *is* on — consider speed-dependent parameters, or
  a better time-stretch algorithm/library if WSOLA can't be made clean.
- Verify at 1.5×, 2×, 3×, 5× — clarity likely varies a lot across the range.

Cross-refs: **BUG-22** (dropouts/underruns at high tempo), **BUG-10** (headphone/lock-screen pause),
**FEATURE-3** (screen-off native vs high-speed engine toggle + its default/migration).

_Not started — logged 2026-07-08._

---

## FEATURE-16 — Settings: adjust visible subjects (units-aware, not enforced)

**Type:** feature (subject hub / settings). **Severity:** high (scaling blocker — the catalogue is
growing to **hundreds of subjects**, so a persistent way to curate which ones show is essential).
**Extends FEATURE-6** (first-run searchable subject picker, which already saves to `podcast-subjects` and
exposes an "Edit subjects" entry in Settings) — this makes that Settings control first-class and
**units-aware**. Build on FEATURE-6's picker; don't create a second one. Pairs with **FEATURE-10**
(drag-reorder the chosen subjects).

**Want.**
- An **active Settings control** to add/remove which subjects are visible on the hub — a searchable
  checklist over the full (hundreds-strong) catalogue, filtering the hub to the selected set (persisted
  to `podcast-subjects`, ideally synced — FEATURE-9).
- **Units awareness.** HSC subjects carry a **unit value** (most 2 units; Extension/1-unit courses = 1).
  A typical student takes **~12 units**, so show a **running units tally** of the current selection as
  gentle guidance (e.g. "10 / 12 units").
- **Do NOT enforce the 12-unit cap.** It's informational only — **some people take more**, so never block
  or hard-limit selection; at most a soft, dismissible hint if they go well over.

**Direction.**
- Add a `units` field per subject in `content/<subject>/subject.json` (default 2; 1 for Extension/1-unit
  courses) and surface it through `manifest.json`.
- In the picker/settings UI, sum `units` across selected subjects and display the tally live; keep it a
  label, not a gate — selection stays unrestricted.
- Reuse FEATURE-6's picker component for both first-run and the Settings edit path so there's one
  implementation; compose with FEATURE-10 (order) so editing the selection doesn't clobber the saved order.
- Cross-refs: **FEATURE-6** (searchable picker + `podcast-subjects`), **FEATURE-10** (reorder),
  **FEATURE-9** (sync the selection), **FEATURE-15** (onboarding walkthrough can point at this control).

**Open call for Fred.** Whether to show any soft over-12-units nudge at all, or omit the warning entirely
and just display the tally.

_Not started — logged 2026-07-08._

---

## BUG-29 — _(merged into BUG-25)_

Merged into **BUG-25** on 2026-07-08 — same root cause (the generator back button is obscured under the
iOS status-bar/notch and so isn't clickable). See BUG-25 for the description and fix. Number retained to
avoid renumbering / concurrent-session collisions.

## BUG-30 — Software Engineering: two revision-deck headings show as blank podcast episodes — remove from podcast list, keep flashcards

**Type:** content / UI. **Severity:** medium. In **Software Engineering** there are **two revision-deck
sections/headings** — **"Memorisation"** (`MEM-*`) and **"Episode Content"** (`EPC-*`) — that surface in
the **podcast/episode list** but have **no content in the podcast content area** (no audio, only a stub
`script.md`). So opening one shows a **blank podcast** — the cards live in the Quiz/flashcards tab, but
the episode itself is empty.

**Want (Fred).** **Remove the two headings from the podcast listing** so they no longer appear as blank,
audio-less episodes. **Keep the flashcards** — the MEM/EPC cards must stay available in the
flashcard/review system; only their appearance as empty *podcast* entries should go.

**So:** don't delete the deck content — just stop rendering these card-only decks as podcast episodes.

**Fix direction.**
- Stop the `MEM-*` / `EPC-*` (audio-less, card-only) modules from rendering as podcast sections/episodes
  in the Software hub — drop the two "Revision decks" headings from the episode/podcast browse view.
- Preserve the cards in the flashcard path: they must still feed the Quiz/review decks (cf. FEATURE-7's
  deck tagging / "Review deck" setting), just not appear as playable episodes.
- Likely touch points: the "Revision decks" grouping in `content/software/subject.json` (`groupNames` /
  year bucket that promotes MEM+EPC into two sections) and the render path that lists modules as
  episodes; or gate audio-less modules out of the podcast list while keeping them in the card pool.
- Cross-refs: **FEATURE-7** (MEM/EPC card-only deck design — keep the cards), **BUG-3** (hide play
  controls for non-audio entries — related rendering gap for card-only content).

_Not started — logged 2026-07-08._

---

## BUG-31 — Quiz progress bar: empty/unfilled track invisible (esp. light mode)

**Type:** UI / theming. **Severity:** low–medium (you can't gauge how far through the quiz you are — the
bar's full length isn't visible). In the quiz UI the **progress bar's unfilled track can't be seen**, so
the bar reads as "empty" / not there — most notably in **light mode**. The blue fill
(`.quiz-progress-fill`, `var(--accent)`) shows, but the **track behind it is too low-contrast** to see.

**Cause (confirmed in code).** `.quiz-progress-track` (`style.css:1405`) is only **3px tall** with
`background: var(--border)`. In light mode `--border` is `#d8d8dc` on a `#ffffff` page background — barely
distinguishable — so the empty portion of the bar is effectively invisible. (Dark mode `--border`
`#2c2c2e` on `#121212` is also low-contrast, but the report centres on light mode.)

**Fix direction.**
- Give the track a more visible background than `var(--border)` — e.g. a dedicated track token, or a
  translucent overlay (`rgba` of the text colour) that reads in both themes — and/or bump the height
  (3px → ~5–6px) so the unfilled portion is discernible.
- Verify the full bar length is visible in **both** light and dark before/at 0% progress.
- Check the sibling bars that share the pattern (`.module-progress-track` / `.ep-progress-track`, same
  `var(--border)` track) don't have the same low-contrast issue.

_Not started — logged 2026-07-08._

---

## BUG-32 — Flashcards panel can't be closed unless scrolled to the top; needs an always-reachable grab handle

**Type:** UI / gesture. **Severity:** medium (you can get stuck in the panel after scrolling). The
**flashcards panel** (sheet overlay) can **only be closed from the top** — the ✕ and the swipe-to-dismiss
both live in the header. Once you've **scrolled down** inside the panel, the header and ✕ are off-screen,
so there's **no way to close it without scrolling all the way back up**.

**Cause (confirmed in code).** `enableSheetDismiss()` (`app.js:183`) only starts the swipe-down-dismiss
drag when the touch begins on the header (`if (!e.target.closest(".q-head, .stats-header")) return;`) — it
deliberately excludes the scrollable list/body so a scroll gesture isn't hijacked. Correct for the body,
but it means the **only** dismiss affordances (✕ + header drag) scroll out of reach.

**Want (Fred).**
- Add an **always-reachable grab handle** — a grabber/pill **in the middle** (i.e. persistent, not only at
  the very top) that you can **grab and swipe down** to dismiss the panel from anywhere, without scrolling
  up. (A sticky handle that stays put as the content scrolls.)
- **Keep the ✕ close button** as well, **especially for iOS**.
- **iOS may warrant a different design** — Fred noted "iOS might have a different design with the
  toaster." _⚠️ "toaster" is ambiguous (transcription) — needs clarifying: likely a sticky bottom
  bar / distinct sheet chrome for iOS? Confirm before building the iOS variant._

**Fix direction.**
- Add a fixed/sticky **drag handle** element to the sheet (a small centred grabber pill) that stays
  visible as the body scrolls; wire the existing dismiss-drag (`touchstart/move/end`, `dy > 90` →
  `closeSheet`) to *that* handle so it works regardless of scroll position — without re-enabling
  drag-to-dismiss on the scrollable body (which would fight scrolling).
- Optionally also keep a compact ✕ pinned (sticky header) so a tap-close is always available too.
- Applies to the shared sheet component (`enableSheetDismiss` / `.stats-panel`), so verify the change
  doesn't regress the other sheets (Stats, Review, Queue, Settings). Cross-ref: **BUG-1** (sheet
  scroll-lock), and the Review-overlay Exit note in `quiz-issues.md` → Q3.

_Not started — logged 2026-07-08._

---

## BUG-33 — Papers browse shows (almost) only HSC/NESA papers; trial & other-source papers dropped or mis-typed — SYSTEMATIC across subjects

**Type:** content pipeline / data classification. **Severity:** high (whole categories of downloaded
papers are invisible in the app). **Reported (Fred):** for **English Standard**, the app looks like it
**only has HSC papers**, even though trial/other papers were **downloaded from various other websites**
(ACE / thsconline / school trials).

**What the data shows (investigated 2026-07-08).** Each subject's browse list comes from
`content/<subject>/papers-index.json` (loaded by `generator.html` ~L898, browse mode). Papers carry a
`type`: `nesa` (official HSC), `thsc` (trial HSC), `exam` (other exams/assessments), `notes`, `marking`.
- **`english-standard`**: `nesa: 50, exam: 165, notes: 26` — **zero `thsc` (trial) papers**, and its
  `exam` bucket is mostly **ACE _assessment_ tasks** (essays/speeches/creative writing, e.g.
  `ace-assessment-…`), **not** trial exam papers. So the only real *papers* are the 50 NESA/HSC ones →
  "only HSC".
- Real trial papers **do exist on disk** but don't surface: raw `papers/English Standard/ACE-Trial/`
  has school trials (2015 All Saints, Casino, Hurlstone, James Ruse, Ryde; 2019 Baulkham Hills, Sydney
  Grammar), yet `papers_organized/English Standard/Papers/Trial/` holds only **3** (the pre-2019 ones
  were archived to `Archive-pre-2019` by the syllabus cutoff).

**Two systematic causes (both need confirming):**
1. **Mis-classification.** Trial/other-source papers get typed `exam` (lumped with assessment essays) or
   not recognised as trials — no `thsc` type is assigned for the English subjects. School/source and
   year are also junk (derived from filenames — see the garbage `school` values in the index).
2. **Cutoff archiving hides trials.** The syllabus cutoff (`tools/syllabus_cutoffs.json`) archives
   pre-cutoff papers; English Standard's cutoff (2019) sends the bulk of the ACE trial set (2015) to
   `Archive-pre-*`, so the browsable trial set is nearly empty even though the files exist.

**Same error is systematic — cross-subject scan (do NOT treat as English-only):** subjects whose
`papers-index.json` is **all/only NESA-HSC with no trials** — **`english-eal-d`** (72, all `nesa`),
**`english-studies`** (14, all `nesa`) — plus the English family where trials collapse into `exam`:
**`english-advanced`** (`nesa:51, exam:619, notes:140` — **no `thsc`**) and **`english-standard`**
(above). Contrast the sciences/maths, which correctly carry big `thsc` trial buckets (physics 256,
chemistry 249, maths-ext1 1066). So the fault clusters in the **English subjects** (and the
`nesa`-only ones) where the classifier never emits `thsc`.

**Action (Fred's ask — audit every subject).** Have the papers/parser agent **audit all subjects** for
this: (a) trials mis-typed as `exam` or missing entirely; (b) subjects reduced to NESA-only; (c) whether
the cutoff is wrongly hiding still-relevant trials. Fix the classifier so trials → `thsc` and only true
assessments → `exam`, recover source/school/year from the organized layout (not filename guessing —
cf. FEATURE-7 / FEATURE-11 organized contract), and re-evaluate cutoffs for the English subjects.

**Fix touch points.** The index/classification stage that builds `content/<subject>/papers-index.json`
(the `type`/`school`/`year` assignment), `tools/organize_papers.py` + `tools/syllabus_cutoffs.json`
(bucketing/cutoffs), and confirm `generator.html` browse surfaces every non-`notes` type. Cross-refs:
**FEATURE-7** (organized papers contract — source of clean type/school/year), **FEATURE-11** (paper-asset
bucket + raw `paper.pdf`), **FEATURE-14** (in-syllabus toggle — depends on correct cutoff/type),
**BUG-11** (another content-classification/order fault).

_Not started — logged 2026-07-08._

---

## BUG-34 — Phantom generic "English" subject in the paper generator (should be split into the real courses)

**Type:** content pipeline / data. **Severity:** medium–high (a non-existent HSC course shows in the
generator, and it's hoarding the trials that belong to the real English courses). **Reported (Fred):**
there is **no "English" HSC course — only the typed courses** (Standard, Advanced, EAL/D, Extension 1,
Extension 2, Studies). Yet the generator lists a plain **"English"** subject.

**What it is (investigated 2026-07-08).** `content/paper-subjects.json` has an entry
`{id:"english", name:"English", papers:404, hasQuestions:true}` alongside the real
`english-standard` / `english-advanced` / etc. It's a **browse-only bucket** — `content/english/` has
only `papers-index.json` + `questions.json`, **no `subject.json`** — so it's not a real subject, just a
paper pile that leaks into the generator's subject dropdown.

**Why it exists / why it matters.** It's the scraper's **generic English catch-all**: `papers/English/`
is split `Y12-HSC`, `Y12-Trial-P1`, `Y12-Trial-P2-Adv`, `Y12-Trial-P2-Std`. **Paper 1 (Texts & Human
Experiences) is common to Standard _and_ Advanced**, so source sites (thsconline) file those trials under
plain "English" rather than a specific course. Result: **404 papers, 391 of them `thsc` trials**
(2001–2025) sit here — **almost certainly the missing trials from BUG-33** (why `english-standard` /
`english-advanced` have zero `thsc`).

**Fix direction.**
- **Reassign** the generic-English papers into the real courses: Paper 1 / common-module trials → both
  **English Standard** and **English Advanced** (shared); Paper 2 splits already labelled `-p2-std` /
  `-p2-adv` → the matching course; EAL/D / Extension where identifiable.
- Then **remove the phantom `english` subject** from `content/paper-subjects.json` (and its
  `content/english/` bucket) so only real courses appear.
- Where a Paper 1 genuinely can't be attributed to one course, decide a rule (surface under both, or a
  labelled "English (common Paper 1)" grouping) rather than a fake top-level subject.
- Fixes the root of **BUG-33** for the English family. Cross-refs: **BUG-33** (trials missing/mis-typed),
  **FEATURE-7 / FEATURE-11** (organized papers contract + correct subject attribution).

_Not started — logged 2026-07-08._

---

## BUG-35 — Paper generator layout is badly organized on phone (wasted space, sparse filters)

**Type:** UI / iOS. **Severity:** medium (looks unpolished and wastes the small screen; filters are hard
to use). **Reported (Fred) with screenshot (iPhone, "Build a paper" tab, English Standard).** The
generator (`generator.html`) is **poorly laid out on a phone** — a long, sparse vertical scroll.

**Concrete problems in the screenshot.**
- **Large wasted vertical whitespace** — a big empty gap between "Clear all filters" and the
  "111 questions match" results row; the filter column is mostly air.
- **Sparse single-item filter sections stacked tall** — SYLLABUS / SOURCE / YEARS / EXTRAS each show
  just one chip (e.g. SOURCE = a lone "HSC"), each taking a full row + heading. Wastes space and buries
  the results far down the page. Could be a compact filter bar / collapsible row / two-column layout on
  mobile.
- **Theme toggle (half-moon) floats awkwardly** next to the subject dropdown, unlabelled and cramped.
- **Question-row titles truncated** ("Unclass…") — the topic label is clipped so rows aren't
  distinguishable at a glance.

**Also surfaced by this screen (data, not layout — cross-refs):**
- SOURCE offers **only "HSC"** for English Standard → confirms **BUG-33** (no trial/other sources).
- SYLLABUS is **"Unclassified" ×111** → English Standard questions carry **no syllabus-outcome tags**, so
  the syllabus filter is useless here (worth its own look — question tagging gap; relates to BUG-33's
  classification theme).

**Fix direction.** Rework the generator's mobile layout: collapse the filter sections into a compact,
space-efficient control (sticky filter bar or accordion), remove the dead vertical space so results
appear without a long scroll, give the theme toggle a proper home, and let question titles wrap/ellipsis
sensibly (show enough to distinguish). Verify on a real iPhone. **Related: BUG-25** (generator iOS layout
messy + back button under status bar — same page, treat together), **BUG-2 / BUG-5** (generator UI /
dark mode on iOS).

_Not started — logged 2026-07-08._

---

## BUG-36 — Audio can't be resumed after pausing while the screen is off

**Type:** audio / playback. **Severity:** high (you can't restart playback without waking the phone —
breaks screen-off / pocket listening, the core use case). **Reported (Fred).** If you **pause** an
episode while the **screen is off** (phone locked / in pocket), you then **can't resume** it. The same
pause→resume works fine when the **screen is on**. So resume is specifically broken in the
locked/background state.

**Likely cause (needs on-device confirmation).** Resuming audio from a **backgrounded / locked** iOS
context has to come through the **Media Session** lock-screen/headphone control (a real user gesture the
OS accepts) — an in-page `audio.play()` fired from a background timer/handler is **rejected** because it
isn't a foreground user gesture, and the audio session may have been suspended by the OS on lock. If the
Media Session `play` handler isn't wired to the app's real resume path (or the lock-screen controls
aren't kept live while paused), pressing play with the screen off does nothing; waking the screen gives a
foreground gesture, so it works there. Same subsystem as **BUG-10** (Media Session play/pause routing)
and **BUG-22** (AudioContext suspends in background and doesn't resume — partially addressed by auto-
resume on `visibilitychange`, commit `48dd671`, but that fires on *wake*, not while still off).

**Fix direction (device-specific — can't verify blind).**
- Ensure the Media Session **`play` handler resumes through the same engine-aware toggle** the on-screen
  button uses, and keep `navigator.mediaSession.playbackState` accurate while paused so the lock-screen
  play button stays live and routable.
- Keep the audio session/element alive across a screen-off pause (don't fully tear down on lock) so a
  lock-screen play can restart it; resume any suspended AudioContext from the Media Session gesture, not
  only on `visibilitychange`.
- Verify on the **native** path specifically — playback is now always native (`<audio>`, commit
  `410a382`), so this is about the native element + Media Session in the locked state, not the retired
  Web Audio engine. Test: play → lock screen → pause from lock screen/headphones → press play from lock
  screen; must resume without waking.

Cross-refs: **BUG-10** (headphone/lock-screen pause not routed), **BUG-22** (AudioContext background
suspend/resume), **FEATURE-3** (screen-off native playback mode — this is that mode's core promise).

**⚠️ Full bug trace / post-mortem: [`docs/audio-background-resume.md`](audio-background-resume.md).**
Read this before touching the audio module again — it records why four fix attempts failed and why we
kept circling.

**Attempt log (all reverted — do not re-try blind):**
- `72a60ee` silent keepalive → didn't work. `ad5b582` continuous silent anchor → didn't work.
- `10a7c1f` raw native element → didn't work. `1167c18` AudioContext routing → **regressed** speed + re-armed the auto-advance loop.
- `4e5d542` attempt 5: proper WebAudio session-sharing (CORS verified, done right) → **regressed high speed** on device (reverted `6e93d29`).
- **On-device diagnostics (`6f07703`) pinned the exact failure** — see the trace doc §8/§9.

**CONCLUSION — accepted as an iOS platform limit, not a code bug.** The only mechanism that can fix
background pause→resume (routing `<audio>` through a WebAudio graph to share the audio session) is
**fundamentally incompatible** with the app's non-negotiable high-speed playback — routing through
`createMediaElementSource` breaks iOS's high-rate `preservesPitch`. You can have clean high speed *or*
lock-screen pause→resume, not both. Resolution is a product decision (recommended: accept "wake to
resume" — background *playback* already survives a lock; only pausing-then-resuming *while still locked*
needs a screen wake). Full analysis + the two product options in `audio-background-resume.md` §9.

**Key findings from the git-history trace:**
1. **No "silent-loop" mechanism ever existed** in committed history — nothing to "bring back." Every
   attempt was newly-invented code, not a restoration.
2. The **loop** is a re-appearance of the auto-advance cascade (prior fixes `aa011a6`, `65099bb`); its
   guards are intact in the current build, and attempt 4 re-triggered it. Fixed again by the revert.
3. Root cause of the circle is **method, not API**: the bug only repros on the installed iOS PWA with the
   screen off, which I can't reach, so every fix was a blind guess deployed to prod.

**Next step is NOT another fix** — it's ground truth first: add an on-screen debug log (or USB
Safari remote-debug) to see what iOS actually does through pause→lock→resume, *then* write one targeted
fix. May end in a product decision (don't fully pause on lock, or "wake to resume") if iOS won't
reactivate a deactivated session from the lock screen. See the trace doc §6.

_Unresolved — original bug still present; regressions reverted. Logged 2026-07-09._

---

## BUG-37 — Settings feedback box misaligned; "Send feedback" button should sit below the textarea

**Type:** UI / layout. **Severity:** low (cosmetic, but the feedback control looks broken). **Reported
(Fred).** The **feedback box in Settings** (FEATURE-13) is **not aligned correctly** — the **"Send
feedback" button should be below the textarea**, stacked underneath it, not beside/misplaced.

**Where.** `index.html:245–248` — Settings → Feedback section: `#feedback-text` (`textarea.setting-text`)
then `#btn-feedback-send` (`button.setting-btn`) then `#feedback-status` (`p.setting-hint`). The **DOM
order is already correct** (button follows the textarea), so this is a **CSS layout** issue — the button
isn't rendering as a full-width block below the box (likely the settings row/section container lays its
children out in a row, or `.setting-btn` is inline/auto-width and floats up next to the `width:100%`
textarea).

**Fix direction.**
- Make the Feedback controls a **vertical stack**: textarea full-width, then the **Send button on its own
  line below it**, then the status hint. E.g. wrap the three in a column flex container
  (`flex-direction: column; align-items: stretch`), or ensure `.setting-btn` here is `display:block` /
  full-width and clears the textarea.
- Check whether `.setting-btn` / `.setting-text` inherit a horizontal `.settings-*` row layout that needs
  overriding just for this section; verify the button spacing (a small `margin-top`) so it doesn't hug
  the box.
- Verify on iOS (installed PWA) as well as desktop — the settings sheet is the primary surface. Related:
  **FEATURE-13** (the feedback box itself), **BUG-2** (settings/dark-mode styling consistency).

_Not started — logged 2026-07-09._
