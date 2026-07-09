# BUG-36 — Background audio resume: bug trace & post-mortem

**Status (2026-07-09):** unresolved. All fix attempts reverted. Live build `c6c61ca` is back to the
known-good native audio (`410a382` audio code + later non-audio features). Speed works, no loop, but
the original bug remains: **pause while the screen is off → can't resume from the lock screen.**

This doc exists because we've gone around this twice and kept regressing. It records what actually
happened, what the git history proves, and how to stop circling.

---

## 1. The symptom

- **Original bug (BUG-36):** Play an episode → lock the phone → pause from the lock screen → press play
  from the lock screen. It does **not** resume. The identical pause→resume works fine with the screen on.
- **What my attempts added on top (regressions):** at various points, audio **would not speed up** and
  **looped** (timer advances at high speed, pause→play does nothing useful, no sound). Those were
  *introduced by the fix attempts*, not the original bug.

---

## 2. Timeline of attempts (the history you asked me to record)

| # | Commit | Approach | Result |
|---|--------|----------|--------|
| — | `410a382` | **Baseline.** Retire Web Audio engine, always native `<audio>`+preservesPitch. | Speed good, streams, no loop. **Only background-*resume* broken.** This is the known-good floor. |
| 1 | `72a60ee` | Silent keepalive: play a silent data-URI to hold the iOS audio session across a screen-off pause. | "Doesn't work, but nothing broke." |
| 2 | `ad5b582` | Silent anchor runs continuously from play, held through pause. | Didn't fix; timer moved at high speed, no sound. |
| 3 | `10a7c1f` | Drop the hybrid wrapper, use the raw native element; re-apply `preservesPitch`. | "Doesn't work." Numbers move, no audio. |
| 4 | `1167c18` | Route native `<audio>` through an AudioContext (`createMediaElementSource`) + `crossOrigin`, resume the context on every gesture. | **Regression:** won't speed up **and** loops. |
| ↩ | `553670e`,`cfe79d8`,`d55ff50`,`c6c61ca` | **Reverted all four.** Back to `410a382` audio code. | Speed + no-loop restored. Original bug still present. |

**Every one of attempts 1–4 was code I newly wrote for BUG-36. None of them restored a prior mechanism.**

---

## 3. What the git history actually proves

I searched the entire history (`git log -S` across all branches). Three findings that change the plan:

1. **There was never a working "silent-loop" keepalive to restore.** The strings `SILENT` / `data:audio`
   appear in the repo *only* in my BUG-36 attempts (and their reverts). The belief "I got it to work in
   the past" does **not** correspond to any committed mechanism. So "browse the history and bring back
   the version that worked" has no target — I already looked; it isn't there.

2. **The only real AudioContext lived in `speed-engine.js`** (the retired WSOLA engine), and by every
   commit message and your own testing it did **not** play in the background — iOS suspends a background
   AudioContext (`48dd671` only auto-resumes it on *wake*, i.e. `visibilitychange`, not while still
   locked). Retiring it (`410a382`) was the right call; it isn't the thing to bring back.

3. **The "loop" is a known, separately-fixed bug — this is its second appearance.** Two prior fixes:
   - `aa011a6` — *orphaned countdown interval → 1 Hz replay loop.* `showAdvanceToast` overwrote
     `advanceTimer` without clearing the old interval; once its countdown passed 0 it re-ran
     `loadEpisode(autoplay)` every second, overriding pause. Fixed by `dismissAdvanceToast()` at the top
     of `showAdvanceToast`.
   - `65099bb` — *lock-screen replay cascade.* Auto-advancing to an episode saved near its end played a
     1–2 s tail, fired `ended`, advanced again — a runaway of short snippets. Fixed with a `fromStart`
     flag on all auto-advance paths **and a runaway guard** (`lastAutoAdvanceAt`: two `ended` within 2 s
     stops auto-advancing).

   **Both guards are still present in `c6c61ca`** (verified: `dismissAdvanceToast()` at
   `app.js:792`; `lastAutoAdvanceAt` at `app.js:47/889/890`; four `fromStart:true`; nothing sets
   `audio.loop`). So the loop is **not** a permanent regression in the current build — it was **re-armed
   by attempt 4**: routing through the AudioContext + `crossOrigin` made the element fail-fast (likely a
   silent/errored decode that reaches `ended` quickly), which re-fed the auto-advance cascade faster than
   the 2 s guard catches on a slow network. Reverting attempt 4 removes the trigger.

---

## 4. Why we kept circling (the real root cause)

Not the audio API — the **method**:

- **I can't reproduce the bug.** It only manifests on your installed iOS PWA with the screen physically
  off. The Chrome extension can't reach it; screenshots time out; localhost is unreachable. So every
  attempt was a *blind guess* validated only by you testing on your phone hours later.
- **I deployed each guess straight to production.** One test subject (you), a slow feedback loop, and
  each guess could — and attempt 4 did — regress speed/loop for real.
- **I chased a mechanism that never existed** ("bring back the silent loop"), so each attempt was a fresh
  invention dressed up as a restoration.

That's the circle: guess → deploy → you test → "doesn't work" → guess again, with no instrumentation and
no ground truth about what iOS is actually doing.

---

## 5. What is actually known about the iOS constraint

- A backgrounded/locked iOS PWA can **keep playing** native `<audio>` that was already playing.
- Resuming from **fully paused + locked** must come through a **Media Session** lock-screen/headphone
  control (an OS-accepted gesture). An in-page `audio.play()` from a timer/handler is rejected in the
  background.
- On lock/pause iOS may **deactivate the audio session**; the lock-screen transport can then go
  unresponsive, so the `play` control does nothing until a foreground gesture (waking the screen)
  reactivates the session — which is exactly the reported symptom.

So the fix space is narrow and genuinely device-specific: keep `navigator.mediaSession.playbackState`
accurate while paused, keep the transport live, and resume from the Media Session `play` handler. Whether
iOS *permits* reactivating a deactivated session purely from the lock-screen control (no wake) is the open
question — and it may simply not be permitted, in which case the honest answer is a product decision, not
a code fix.

---

## 6. How to stop circling — the exit

**Do not attempt another blind fix-and-deploy.** Next step is to get *ground truth* first:

1. **Instrument, then observe (one deploy, no behaviour change).** Add a tiny on-screen debug log
   (visible in Settings) that records, with timestamps: `audio.paused`, `audioCtx?.state`,
   `mediaSession.playbackState`, and which handler fired (media-session play vs button). Then you: play →
   lock → pause → play-from-lock, unlock, and read the log. That tells us *what iOS actually did* instead
   of guessing.
2. **Remote-debug over USB (best signal).** Connect the iPhone to a Mac, Safari → Develop → your PWA,
   and watch the console/events live through the lock/pause/resume cycle. This is the single highest-value
   thing and removes all guessing. (You run it; I can't reach the device.)
3. **Only after we can see the failure**, write **one** targeted fix, test it via the debug log, and
   *then* deploy.
4. **Decision to make (yours):** if remote-debug shows iOS refuses to reactivate a deactivated session
   from the lock screen without a wake, we stop trying to beat the OS and instead pick a product answer:
   e.g. don't fully pause on lock (use a low/zero-volume hold you can restore), or accept "wake to
   resume" and make the lock-screen play button just wake+resume.

**Guard rails going forward (so we don't regress again):**
- Never deploy an audio change to `main`/production without a revert commit ready and the exact test
  steps written down.
- Keep the `410a382` audio block as the known-good floor; any experiment branches from it and is one
  revert away.
- If an attempt "doesn't work," **revert immediately** rather than stacking the next attempt on top —
  attempts 1–4 stacked and that's how attempt 4 re-armed the loop.

---

## 8. GROUND TRUTH (2026-07-09) — the on-screen log finally showed the failure

Build `6f07703` added a no-behaviour-change diagnostics ring buffer (Settings → About → Audio log).
Fred captured a full play→lock→pause→resume cycle. The decisive evidence is `currentTime` (`t=`):

```
+15.8  vis:hidden      t=104.0    screen locked, still playing
+17.2  MS:pause        t=109.3    played 104.0→109.3 WHILE LOCKED  → background *playback* works
+17.9  MS:play handler t=109.5    press play from the lock screen
+18.0  evt:playing     t=109.5    element claims playing; promise resolves
+20.3  MS:pause        t=109.5    2.3s later t is UNCHANGED
+23.2  MS:pause        t=109.5    frozen the entire time in background
+23.7  vis:visible                unlock
+24.6  btn:play        t=109.5 → +26.0 t=113.4   foreground: advances again
```

**Failure mode (confirmed, not hypothesised):** after a **background pause**, the next play is a
**phantom** — `evt:play`+`evt:playing` fire, `paused=false`, `MS:play resolved` — but `currentTime` is
**frozen** and there is no sound. iOS deactivates the element's audio session on a backgrounded pause and
re-playing in the background does **not** reactivate the output. Recovery only happens on a **foreground
gesture** (wake the screen — see the `+24.6` line). So: background *playback* survives a lock; background
*pause→resume* does not.

**Why this kills the earlier theories:**
- It is **not** a rejected `play()` (BUG-36 entry's "likely cause" was wrong) — the promise resolves.
- The **silent-keepalive** attempts (1, 2) couldn't work: iOS gives the native `<audio>` element its own
  audio session, *separate* from an AudioContext's. Holding a separate silent session alive does nothing
  for the element's session. To share one session the **element itself must be routed through the
  context** (`createMediaElementSource`).
- Attempt 4 *did* route through a context but (a) had no continuous output to keep that context's session
  alive across the pause, and (b) `crossOrigin`/routing broke loading → the speed + loop regression.

**Implication for the fix:** the only mechanism that can work is routing the element through **one**
AudioContext that is kept alive across the pause (a continuous silent source in the same graph). That is
the correct-but-risky Web-Audio family that regressed before — so it must be done with the diagnostics on
and a revert ready. The safe alternative is a product decision: accept "wake to resume" and make the
lock-screen play button wake+resume (the log shows that already works). Decision pending with Fred.

---

## 9. Attempt 5 result (2026-07-09) — the fix and the requirement are mutually exclusive

Fred chose to try the real fix. Commit `4e5d542` did it properly this time — CORS verified for ranged
cross-origin GET (206, `access-control-allow-origin` echoed for both origins, so the media graph is not
tainted), `crossOrigin` set before any `src`, graph built lazily in the first gesture, silent keepalive
in the same graph, diagnostics on.

**Result on device: high-speed playback regressed.** Routing the native `<audio>` element through
`createMediaElementSource` breaks iOS's high-rate `preservesPitch` playback — the exact same symptom as
attempt 4, now confirmed to be caused by the WebAudio routing itself (not the `crossOrigin`/CORS loading,
which we'd verified was fine). Reverted in `6e93d29`.

**This is the decisive finding.** The *only* mechanism that can fix BUG-36 (share one audio session via
the WebAudio graph) is **fundamentally incompatible** with the app's **non-negotiable** requirement
(clean high-speed playback to 7–8×; see the "Audio speed priorities" memory). You cannot have both on
iOS today:

- Native `<audio>` → high speed works, background *pause→resume* is dead (iOS kills the element session).
- Element routed through WebAudio → background resume becomes possible, but high speed breaks.

So BUG-36 is **not solvable in code** without sacrificing the higher-priority feature. Attempts 1–5 have
now exhausted the WebAudio family. The remaining resolutions are product decisions, not bugs to fix:

1. **Accept "wake to resume"** (recommended): keep native high speed; the lock-screen/pocket case is
   "wake the screen, then resume" — which the §8 log shows already works instantly. Optionally make the
   lock-screen play button trigger a wake. Background *playback* (the common case — lock while playing)
   already works; only *pausing then resuming while still locked* needs a wake.
2. Ship a low-priority "background-pause mode" toggle that routes through WebAudio *only* at 1× for users
   who value lock-screen pause over high speed. High complexity for a narrow case — probably not worth it.

**Current state:** native audio restored (working high speed), BUG-36 accepted as an iOS platform limit.
The on-screen diagnostics + the controlled-update mechanism (swipe-up / 6h) stay, so any future retry is
cheap and safe to iterate.

---

## 10. The re-encode idea + the `ctx=interrupted` proof (2026-07-09)

Fred asked the sharp question: since real-time speed is what breaks WebAudio, could we **pre-render each
file at the target speed and play it at 1×**? Then no speed algorithm runs, WebAudio has nothing to
break, and (the hope) it holds the session for background resume. Great idea — it hinges on one premise:
**does a WebAudio context actually survive backgrounding at 1×?**

We tested it directly (build `4f9346d`: forced `bgPauseMode`, routed through `createMediaElementSource` +
silent keepalive, forced 1×, with a `ctx=` field added to the diagnostics). The log settled it:

```
+15.4  vis:hidden   t=8.0   ctx=running        lock while playing — context alive
+18.6  vis:visible  t=11.2  ctx=interrupted    iOS INTERRUPTED the context while backgrounded
```

**`ctx=interrupted`** is a WebKit-specific AudioContext state: **iOS suspends the WebAudio context the
instant a PWA is backgrounded, and the continuous silent keepalive does not prevent it.** So WebAudio
cannot hold the audio session in the background — the *same* wall as the native element, now proven from
the WebAudio side too. Therefore **the re-encode idea cannot clear BUG-36**: it removes the speed
algorithm, but the blocker is session/context suspension, which is speed-independent.

Worse, routing through WebAudio *degraded the one thing that worked* — native **background playback**
stopped on lock (the interrupt), plus a pause-time stutter (a MediaElementSource artifact). So WebAudio
is strictly worse than native for this app.

**Final verdict:** iOS suspends the audio session for a backgrounded PWA — native `<audio>` (session
deactivated on pause) and WebAudio (`ctx=interrupted`) alike — and won't let it be reclaimed without a
foreground gesture. No web-side mechanism (silent keepalive, reload, re-encode, WebAudio routing) can
change that. BUG-36 is a hard iOS platform limit. Ship clean native audio; background *playback* works
(the primary case); background *pause→resume while still locked* requires a screen wake ("wake to
resume"). Attempts exhausted: 1, 2, 3, 4, 5, 6/6b/6c/6d (reload+seek kicks), and WebAudio-at-1×.

## 11. "It worked in the git history" — full archaeology (2026-07-09)

Fred was sure a past version resumed from the lock screen. I searched **both** codebases end to end:
- **This unified repo** (157 commits): the `<audio>` tag, Media Session handlers, and play/pause code
  are unchanged since commit #1 (`95caf6d`). The raw-element original (`const audio = audioEl`) was even
  re-tested faithfully in attempt 3 (`10a7c1f`) — same failure.
- **Legacy physics app** `github.com/freddygaffey/hsc-phy-podcast` (98 commits, cloned + searched): **no**
  AudioContext, silent-loop, keepalive, or `playsinline` ever existed. Media Session was added in
  `5301e56` as the identical standard `set("play", () => audio.play())`. Its live audio-control lines
  diff **identical** to ours.

**Conclusion:** across ~255 commits in two repos, there has never been a background-resume mechanism to
restore — it's always been plain native `<audio>` + Media Session. So "it worked once" is almost
certainly (a) an **iOS version change** (same code, different OS behaviour over time — unfixable), or
(b) memory of background *playback* (lock while playing), which still works. Not a lost commit.

---

## 7. Verification of the current (reverted) state — `c6c61ca`

- `git diff 410a382 HEAD -- app.js` filtered to audio identifiers → **empty** (audio code == known-good).
- Loop guards present: `app.js:792`, `app.js:47/889/890`, 4×`fromStart:true`, no `audio.loop`.
- `node --check app.js` → OK. Deployed to production; `build.json` = `c6c61ca`.
