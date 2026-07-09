> ⛔ STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# Regression log — bugs introduced, fixed, reintroduced, and re-resolved

A record of the bugs in this project that did **not** stay fixed the first time. The point isn't blame —
it's to see the *pattern* behind each recurrence and the guard that should stop it coming back a third
time. Compiled from git history 2026-07-09.

Legend: **Intro** = introduced/first seen · **Fix** = first resolved · **Regress** = came back ·
**Re-fix** = resolved again.

---

## 1. Auto-advance replay loop (audio loops ~1 Hz, overrides pause) — 3 rounds

The single most-recurring functional bug. Audio keeps restarting itself, ignores the pause button.

| Phase | Commit | Date | What happened |
|-------|--------|------|----------------|
| Intro | `803b549` | 06-30 | Auto-advance feature ("skip completed, land on next due") — latent loop risk. |
| Fix 1 | `aa011a6` | 06-30 | Orphaned countdown interval: `showAdvanceToast` overwrote `advanceTimer` without clearing it; once its countdown passed 0 it re-ran `loadEpisode(autoplay)` every second forever. Fixed with `dismissAdvanceToast()` at the top. |
| Fix 2 | `65099bb` | 06-30 | Lock-screen cascade: auto-advancing to an episode saved near its end played a 1–2 s tail → `ended` → advance again. Fixed with a `fromStart` flag on all auto-advance paths **+ runaway guard** (`lastAutoAdvanceAt`: two `ended` within 2 s stops advancing). |
| Regress | `1167c18` | 07-08 | BUG-36 audio attempt 4 (AudioContext routing) made the element fail-fast to `ended`, **re-feeding the cascade** faster than the 2 s guard catches on a slow network. |
| Re-fix | `c6c61ca` | 07-09 | Reverted attempt 4. Guards intact in current build. |

**Root cause of recurrence:** the loop is an *emergent* property of the auto-advance state machine — any
change that makes an episode reach `ended` unexpectedly fast re-triggers it. The guards defend the state
machine; they don't defend against a *broken audio element* upstream.
**Guard going forward:** never let an audio experiment ship without checking it can't produce an instant
`ended` (empty/errored/zero-duration media). The runaway guard is the backstop, not the fix.

---

## 2. Page pans sideways / left edge clipped on phones — 3 rounds

Same visible symptom (the whole app scrolls horizontally, content clipped) surfaced by three different
culprits, each fix catching only the case in front of it.

| Phase | Commit | Date | Culprit fixed |
|-------|--------|------|----------------|
| Intro/Fix 1 | `109ea84` (BUG-7) | 07-03 | Wide KaTeX **display equations** widened the page → contain in `overflow-x:auto` box. |
| Fix 2 | `35a833e` (BUG-12) | 07-03 | Still panned from other wide elements → `html{overflow-x:clip}` + block/scroll **tables**. |
| Re-fix | `5321cca` (BUG-12) | 07-08 | On **iOS** wide equations still panned the page → also clip `<body>` + `max-width:100vw`. |

**Root cause of recurrence:** each fix targeted a *specific* wide element instead of guaranteeing the
viewport can never pan. `html{overflow-x:clip}` alone doesn't hold on iOS; it needed `body` too.
**Guard going forward:** the containment now lives at both `html` and `body` — treat any new
"pans sideways" report as *a new wide child that escaped its box*, and fix it by containing that child,
since the viewport-level guard is already as strong as CSS allows.

---

## 3. High-speed audio engine → lock-screen/streaming/background saga (BUG-10, BUG-15, BUG-22, BUG-36)

The longest arc. A fix for one thing (pitch-preserved high speed) *introduced* several regressions, whose
fix was ultimately to **remove the thing that was added** — and one symptom (BUG-36) still isn't solved.

| Phase | Commit | Date | What happened |
|-------|--------|------|----------------|
| Intro | `583cc87` | 07-03 | **Hybrid Web Audio engine** added for pitch-preserved speed to 16× (BUG-22/BUG-10). But its AudioContext is suspended by iOS in the background. |
| Patch | `48dd671` | 07-03 | BUG-22 *partial*: auto-resume the AudioContext on `visibilitychange` — but that fires on *wake*, not while still locked. |
| Shift | `d660e69`,`d56a15c` | 07-08 | Default to native `<audio>`; add a screen-off vs high-speed **mode toggle**. |
| Resolve (mostly) | `410a382` | 07-08 | **Retire the engine entirely** — always native. This is what actually fixed BUG-10 (streaming) + BUG-15 (lock-screen) + BUG-28 (clarity). The added complexity was the bug. |
| Still open | `72a60ee`→`1167c18` → reverted | 07-08/09 | **BUG-36** (resume from lock after a screen-off pause) — four attempts, all failed/reverted. See [`audio-background-resume.md`](audio-background-resume.md). |

**Root cause of recurrence:** a heavyweight abstraction (the WSOLA engine) was introduced to solve a
narrow need and brought a cluster of platform regressions with it; net progress came from *deleting* it.
**Guard going forward:** the native `<audio>` path (`410a382`) is the known-good floor for everything
except BUG-36. Don't reintroduce a Web Audio engine to chase BUG-36 — that's the exact move that caused
BUG-10/15/22 and re-armed the loop (cycle 1).

---

## 4. DT quizzes vanish from the app (manifest `quizPaths` dropped) — 2 rounds, same day

| Phase | Commit | Date | What happened |
|-------|--------|------|----------------|
| Fix 1 | `ca045bf` | 07-02 | Stale manifest missing DT + physics `quizPaths` → quizzes didn't show. Wired them up. |
| Re-fix | `770eb04` | 07-02 | Quizzes gone again → re-wire `quizPaths` **+ commit `dt/subject.json`** so the source, not just the generated manifest, carried them. |

**Root cause of recurrence:** `manifest.json` is a **generated file**. Hand-fixing the generated output
doesn't survive the next regeneration — the fix has to live in the *source* (`subject.json`) and be
re-generated. See also the "regenerate canonically" merges (`980f5c5`, `6217b45`).
**Guard going forward:** never edit generated artifacts (`manifest.json`) directly; change the source and
regenerate. Treat a line-merge of a generated file as untrustworthy — regenerate instead.

---

## 5. Home screen / edits clobbered by parallel sessions — recurring meta-pattern

Not one bug but a class: multiple agents/sessions editing `app.js`, `style.css`, and `manifest.json`
concurrently, silently reverting each other's work.

| Commit | Date | What happened |
|--------|------|----------------|
| `ae34111` | 07-02 | **Restore** subject hub + daily-quiz home screen + exit button after they were clobbered. |
| `05d9c1f` | — | Isolated `main-wip-contamination` (app.js/style.css/papers/tools) from parallel edits. |
| `d1edfe6`,`b923dc0`,`57144ac` | — | `reconcile-main` merge dance to untangle in-flight changes from parallel sessions. |
| `980f5c5`,`6217b45` | — | Regenerate `manifest.json` canonically after merge — *don't trust the line-merge* of a generated file. |

**Root cause of recurrence:** concurrent writers with no locking; generated files that don't survive
line-merges.
**Guard going forward:** commit/verify audio + core-shell edits frequently; after any merge that touches a
generated file, regenerate it rather than trusting the merge. When another agent is active, stay in your
lane (this is why BUG-36 work was confined to `app.js`).

---

## Meta-patterns (why fixes don't stick here)

1. **Emergent-state bugs** (cycle 1): the loop isn't in one place — it's a property of the auto-advance
   machine, re-triggerable by any upstream change. Guards mitigate; they don't immunise.
2. **Symptom-level fixes** (cycle 2): fixing the specific wide element, not the viewport invariant, leaves
   the next wide element to re-open it.
3. **Added complexity as the bug** (cycle 3): the Web Audio engine created more regressions than it solved;
   removal was the fix. Prefer the platform-native path.
4. **Editing generated output** (cycles 4–5): fixes to `manifest.json` don't survive regeneration/merge —
   fix the source.
5. **Blind fixes on an unreproducible target** (BUG-36): guess → deploy → user tests → repeat. The exit is
   instrumentation/ground-truth first (see `audio-background-resume.md` §6).

**The recurring prevention rule across all five:** fix the *invariant or the source*, not the *symptom or
the generated artifact* — and for anything you can't reproduce locally, get ground truth before deploying.
