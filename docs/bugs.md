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

## Related (logged elsewhere)
- **Redundant / unstyled Exit in the Review overlay** — see `quiz-issues.md` → Q3.

_None started — parked for a later session._
