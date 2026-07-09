> ⛔ STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# Audio-playback bug hunt — HSC podcast PWA

You are an expert web-audio / PWA engineer doing an adversarial bug hunt on the **audio
playback subsystem** of this app. Your job is to find real, reproducible defects that cause
wrong or annoying playback behaviour — not to refactor or restyle.

## Context you must load first

This is a vanilla static PWA (no framework, no build step). Audio is a single native
`<audio id="audio">` element (the Web Audio speed engine in `speed-engine.js` is **disabled**
— see the comment near `const audio = audioEl` in `app.js`; speed is just
`audio.playbackRate`). Audio `.m4a` files stream cross-origin from R2 via HTTP Range
requests. The app is installed as a PWA on **iOS Safari**, so lock-screen / background /
audio-session-interruption behaviour matters a lot.

Read these before reporting anything:
- `app.js` — the whole player. Focus on: the `audio` event handlers (`play`, `pause`,
  `ended`, `timeupdate`, `loadedmetadata`), `loadEpisode`, `setAudioSource`, `switchVoice`,
  `playTitleIntro`, `showAdvanceToast` / `dismissAdvanceToast` / auto-advance, `getNextEpisode`,
  `getLastPlayedEpisode`, `startModule`, the queue logic, `persistProgress` /
  `saveEpisodeProgress` / `getEpisodeProgress`, the Media Session handlers (`setupMediaSession`,
  `setPositionState`), the sleep timer, the transcript-tap seek, and the service-worker
  registration / update-reload block.
- `service-worker.js` — audio caching, `rangeFromCache` (206 slicing), `cacheFirst`,
  `staleWhileRevalidate`, `networkFirst`, and the install/activate/skipWaiting/claim lifecycle.
- `index.html` — the `<audio>` element and script load order.

## Recently fixed — do NOT re-report these, but DO look for siblings/regressions

1. `showAdvanceToast` overwrote `advanceTimer` without clearing it → orphaned `setInterval`
   re-fired `loadEpisode(autoplay)` every second (1 Hz replay loop that overrode pause).
2. Auto-advance resumed the next episode at its **saved position**; a next episode saved near
   its end played a ~1–2 s tail, fired `ended`, advanced again → runaway cascade of snippets.
   Fixed with a `fromStart` flag on the auto-advance/next paths + a 2 s runaway guard in `ended`.
3. `getNextEpisode` didn't skip completed episodes → auto-advance replayed finished episodes.
4. Installed PWA kept running stale cached `app.js`; added a guarded `controllerchange` reload.

## Hunt these categories (be specific and exhaustive)

**A. Event feedback loops & runaways.** Any handler that can re-trigger its own event or
another player action in a cycle: `ended`→load→`ended`, `pause`→…→`play`, `timeupdate`→seek→
`timeupdate`, seek→play. Check every `.play()` / `audio.pause()` / `audio.currentTime =` /
`audio.load()` call site and ask "what fires this again?". Check timers (`setInterval`/
`setTimeout`) for orphaning, double-scheduling, and missing clears.

**B. Auto-advance, queue & "next".** Off-by-one / wrap-around in `getNextEpisode`; advancing
to an episode with no audio; the queue and sequential-advance interacting; `document.hidden`
(background) path vs the foreground countdown-toast path diverging; navigating away mid-toast;
rapid `ended` (e.g. scrubbing to the very end sets `currentTime = duration` and fires `ended`).

**C. Resume / progress state.** `progressPct` rounding at the 0.999 completion boundary;
`completed` set from position vs from a real `ended`; resuming at ≈end and instantly
re-advancing; stale `lastVoice` / voice index (`findIndex` returning -1); progress saved for
the wrong episode after a fast switch; `subject:epId` id namespacing mismatches.

**D. `loadToken` / async races.** Rapid src changes, voice switches, and auto-advance racing
the `loadedmetadata` handler; the title-intro (`playTitleIntro`) firing its delayed
`audio.play()` after the user paused or loaded a different episode; a stale token applying a
seek/rate to the wrong track.

**E. iOS PWA / background / Media Session.** Audio-session interruption (call, notification,
route change) firing spurious `pause`/`play`/`ended`; lock-screen `play`/`pause`/`seek`/
`nexttrack` handlers vs app state; `setPositionState` reporting `position`/`duration`/
`playbackRate` inconsistently at non-1× speed; background auto-advance keeping the session warm;
`playbackRate` reset after backgrounding.

**F. Service worker & audio delivery.** `rangeFromCache` byte-range math (suffix `bytes=-N`,
open-ended, `start>end`, off-by-one on `end`, `Content-Range`/`Content-Length`); a partially
downloaded file served as if complete; cache-first serving stale audio; `.m4a` matching by
extension colliding with anything; SW update leaving a mismatched shell; offline behaviour.

**G. Speed / sleep-timer / misc controls.** Speed changes mid-playback; the sleep timer
pausing/interacting with auto-advance; rewind/forward clamping at 0 and `duration`; the
progress-bar `isSeeking` flag getting stuck; transcript-tap seek when `duration` is 0/NaN.

## Method

- Trace concrete failing scenarios: give exact inputs/state → the wrong output. A finding
  without a plausible trigger is not a finding.
- Prioritise anything that (a) loops/won't-pause, (b) plays/skips the wrong episode,
  (c) loses or corrupts progress, or (d) breaks background/lock-screen playback on iOS.
- Adversarially verify each candidate against the code before reporting — try to disprove it.
- Distinguish CONFIRMED (you traced the exact code path) from PLAUSIBLE (needs a device to
  confirm, e.g. an iOS-only timing issue).

## Output

For each bug: **file:line**, one-line summary, the concrete failure scenario (inputs/state →
wrong behaviour), confirmed vs plausible, and a minimal suggested fix. Rank most-severe first.
Do not make code changes — report only.
