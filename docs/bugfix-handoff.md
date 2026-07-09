> ⛔ STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# Bug-fix handoff — HSC Study PWA

You are picking up a batch of bug fixes for a multi-subject HSC study PWA (podcasts + quizzes +
past papers). Read this whole file, then `docs/bugs.md` and `docs/quiz-issues.md`, before doing
anything.

## Mission
Work through the bugs in `docs/bugs.md`, fixing the ones that can be done safely and verified from
the repo. Keep the doc updated (status per bug). Do NOT blind-fix things you can't verify.

## Critical context — read before touching git

- **`main` is the deploy branch.** Production is Cloudflare Pages `hsc-podcast-unified.pages.dev`.
- **The shared working tree is on branch `glossary-content` and is being used by ANOTHER agent
  (building past papers). Do NOT switch it, stash it, reset it, or edit its tracked files.** It has
  uncommitted WIP that must stay intact.
- **`main` and `glossary-content` have diverged** and deploys have gone out from both — this is the
  root cause of a lot of instability (see BUG-9). Reconciling them is a user decision; don't do it
  unprompted.
- Rollback ref if a change goes wrong: **`backup/main-pre-dailyquiz`**.

## Workflow rules (follow exactly)

1. **All `main` work happens in a throwaway git worktree**, never in the shared tree:
   ```
   WT=/tmp/wt-main; rm -rf "$WT"; git worktree add "$WT" main
   # edit files under $WT, then:
   git -C "$WT" add <files>; git -C "$WT" commit -m "..."
   git worktree remove --force "$WT"   # commits persist on main
   ```
2. **Verify before committing:** `node --check "$WT/app.js"` (and any JS you touch). Add small
   Node logic tests where you can. There is **no browser/phone available** — the Chrome tool can't
   reach localhost, so you CANNOT visually verify UI or test on a device.
3. **One commit per bug**, message prefixed with the bug id (e.g. `BUG-14: ...`). End commit
   messages with: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
4. **Deploy only when the user explicitly says so.** Deploy = run `PAGES_BRANCH=main ./deploy.sh`
   from inside a `main` worktree (it builds from the working tree, so it must be a main checkout).
   Don't deploy unprompted.
5. Keep `docs/bugs.md` current and copy it to a backup after each change.

## What's already done
- **Fixed & deployed (live on `main`):** BUG-1 (scroll-lock), BUG-3 (no play button on papers),
  BUG-4 (dropped "HSC" prefix), BUG-7 (wide-equation sideways scroll).
- **Fixed, committed, NOT deployed:** BUG-22 partial (`48dd671`, AudioContext auto-resume on
  orientation/backgrounding). The 7× DSP dropout half is NOT done.

## The bugs — triage (full detail in `docs/bugs.md`)

**Do now — app-code, verifiable from repo:**
- **BUG-11** — Software Automation episode order: `SA-20-01-What-is-AI-vs-ML` must sort first. Fix
  the sort in `tools/generate_manifest.py`, regenerate `manifest.json`, verify episode order.
- **BUG-14** — module download icon should show ✓ when all its episodes are downloaded
  (`syncModuleDlBtn`, `app.js` ~1375). Ensure it's called after each episode download.
- **BUG-20** — quiz reveals the correct answer (blue) before you answer. The `opt-correct` reveal
  (`app.js` ~2519/2681) must only run after submission. HIGH impact.
- **BUG-19** — progress not saved when advancing to next episode offline: `persistProgress()` must
  run before the src changes (auto-advance path ~888).
- **BUG-18** — starting the title/quiz voice doesn't pause the playing episode (`playTitleIntro`).

**Attempt with care — app-code but hard to verify blind:**
- **BUG-15** — mobile-data streaming (check `guardPlayable`/`loadEpisode` aren't blocking streams).
- **BUG-12** — page still scrolls sideways somewhere (need to know which screen; find the wide el).

**Do NOT blind-fix (device / risk):**
- **BUG-22** 7× DSP dropout (WSOLA in `speed-engine.js` — needs on-device profiling).
- **BUG-10** headphone/lock-screen pause (iOS Media Session + Web Audio — needs an iPhone).
- **BUG-8** manifest-load resilience (load-critical path).

**Needs user input / out of scope for blind fixing:**
- **BUG-2** dark mode on generate tab (need a screenshot of the bad element — in-app CSS is already
  theme-aware).
- **BUG-5** custom-materials generate UI (NOT in this repo — separate tool).

**Content-generation pipeline (likely the other instance, not app code):**
- **BUG-13** episodes too verbose / over-linked, **BUG-16** ~3s inter-question breaks,
  **BUG-17** per-episode glossaries (currently one subject-wide `GLOSSARY.md`), **CONTENT-1** soften
  "no big data, no ML" line.

**Design / features (scope separately, don't just start):**
- **BUG-21 / quiz-issues.md Q2** — split MC "quizzes" from open-ended recall flashcards.
- **BUG-6** flashcard graphics/features, **FEATURE-1** in-app Python runner.

## Suggested order
BUG-20 → BUG-11 → BUG-14 → BUG-19 → BUG-18, committing and verifying each. Then report and ask
the user which to deploy, and hand the content-pipeline / device / design items back to them.
