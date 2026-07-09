> ⛔ STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# FEATURE-11 — Paper-assets migration runbook

Move **all paper assets** off the audio bucket into a dedicated bucket
**`hsc-papers-and-resources`** (public via `papers.hsc.pebnum.com`). Audio stays in
`hsc-podcast-audio` (`audio.hsc.pebnum.com`). See `docs/bugs.md` → FEATURE-11 for the decision.

_Logged 2026-07-08. Ground truth verified this session; re-check counts before running._

---

## 0. Current state (verified this session)

| Thing | State |
|---|---|
| Target bucket `hsc-papers-and-resources` | exists, **empty** |
| Custom domain `papers.hsc.pebnum.com` | **bound by Fred** — DNS live (Cloudflare IPs); TLS cert provisioning at time of writing |
| Audio bucket `hsc-podcast-audio` (`audio.hsc.pebnum.com`) | live; also holds old patchy paper crops under `<subject>/papers/…` |
| `hsc-questions` | half-done (`<subject>/<slug>/`, ~maths-adv), NOT wired to app |
| `hsc-podcast` | 54 GB, unknown owner — **inventory before touching** |
| Legacy `hsc-phy-podcast`, `hsc-sdd-podcast` | pre-unification per-subject buckets |
| `papers/_index.json` | **10,184** papers indexed (all HSC subjects) |
| Source PDFs under `papers/` | **12,214** files |
| Verified `papers/_work/*/split.json` (segmented) | **247** |
| rclone | installed; remote **`r2:`** = Cloudflare S3 endpoint (account `ac128818…`) |
| `subject.json` with `assetBaseUrl` to repoint | 7: dt, physics, maths-advanced, maths-extension-1, maths-extension-2, maths-standard-2, maths-accelerated |
| App crop-URL construction | `generator.html`: `${assetBaseUrl}/${subject}/papers/${slug}/${key}` — repoint = change `assetBaseUrl` only |
| Tooling | `upload_questions.py [bucket]` and `sync_bucket.py [bucket]` both take a bucket arg (default `hsc-podcast-audio`) and already write `<subject>/papers/<slug>/…` |

**Risk posture (Fred, 2026-07-08):** few users, **breaking the app in production is acceptable** →
the app repoint (Step 5) can ship without a maintenance window. **Data deletion (Step 7) is still
gated** — irreversible, done only after verification and with explicit per-command go-ahead.

---

## Decisions needed before executing

1. **Scope of raw-paper upload.** Only the app's active subjects (dt, physics, maths-*, software ≈
   a few hundred papers), or **all 10,184** ("I just want to have papers")? Recommend: **active
   subjects first** (prove the pipeline end-to-end), then a bulk pass for the rest.
2. **Slug strategy.** Target layout keys folders by `slug = <year>-<school>-<type>`, but many
   `_index.json` entries have null `year`/`type` (e.g. resource PDFs). `upload_questions.py` already
   has a slug derivation — **make that the single source of truth** and define a deterministic
   fallback for slug-less papers (e.g. `paperId`). Nothing uploads until one `paperId→slug` map is
   agreed and reused by upload **and** manifest.
3. **`hsc-questions` fate.** Fold its complete crops into the new bucket, then delete it (Step 7)?

---

## Steps

Each step: **what → commands → check → rollback → [who]**. Run from repo root. `--dry-run`/`echo`
first on anything that writes to a bucket.

### Step 1 — Custom domain → bucket  ✅ (done by Fred)
- **Check:** `curl -sSI https://papers.hsc.pebnum.com/anything` returns an R2 404 (not a TLS error).
  If still a TLS handshake error, the cert is provisioning — wait ~15 min.
- **Rollback:** n/a (additive).
- **[Fred]** done.

### Step 2 — Upload every raw `paper.pdf`
Upload each paper's source PDF → `<subject>/papers/<slug>/paper.pdf` (unblocks raw-paper browsing /
FEATURE-8, independent of segmentation).
- **Prep:** resolve `paperId → (subject, slug, source path)` from `papers/_index.json` (reuse the
  slug fn from `upload_questions.py`). Scope per decision #1.
- **Command (staged, add-only):**
  ```bash
  # dry run first — prints the planned <subject>/papers/<slug>/paper.pdf keys
  python3 tools/upload_questions.py hsc-papers-and-resources --subject physics --limit 5 --dry-run
  # then for real, per subject, widening scope
  python3 tools/upload_questions.py hsc-papers-and-resources --subject physics
  ```
  (If `upload_questions.py` only handles baked crops, add a `--papers-only` path or a small
  `upload_raw_papers.py` that rclones the source PDFs; keep the same slug fn.)
- **Check:** `rclone ls r2:hsc-papers-and-resources/physics/papers/ | grep paper.pdf | wc -l`
  vs expected count; open one via `https://papers.hsc.pebnum.com/physics/papers/<slug>/paper.pdf`.
- **Rollback:** `rclone delete r2:hsc-papers-and-resources/<subject>/papers/ --include 'paper.pdf'`.
- **[Claude]** with Fred confirming scope; bulk 10k pass is large — run subject-by-subject.

### Step 3 — Copy existing crops over + reconcile `hsc-questions`
- **Commands (add-only copy, per subject):**
  ```bash
  rclone copy r2:hsc-podcast-audio/physics/papers/ r2:hsc-papers-and-resources/physics/papers/ -P
  # reconcile the half-done questions bucket, preferring complete sets:
  rclone copy r2:hsc-questions/maths-advanced/ r2:hsc-papers-and-resources/maths-advanced/papers/ -P
  ```
- **Watch:** old crops have `-1` dedup cruft — exclude with `--exclude '*-1.pdf'` after confirming
  the un-suffixed one is complete.
- **Check:** spot-diff counts; open a few crop URLs on the new domain.
- **Rollback:** delete the copied prefixes (paths are additive, nothing overwritten in the old bucket).
- **[Claude]**.

### Step 4 — Bake the 247 verified `split.json` → crops → upload
`bake_split.py` blockers (page-1, all-regions, `_index.json` resolution) are **already fixed** on
disk. Remaining: the with-lines / no-lines **variants** live in the mask/generator stage (parse-papers
session) — confirm the generator emits `q01.pdf` + `q01-c.pdf` before bulk-baking.
- **Commands:**
  ```bash
  for pid in $(ls papers/_work); do python3 tools/bake_split.py "$pid"; done   # → baked_v3/
  python3 tools/upload_questions.py hsc-papers-and-resources --subject <s>      # push crops
  ```
- **Check:** open a baked crop URL; confirm page-correct (regression: unit q1 must render Question 1,
  not Q4).
- **Rollback:** re-bake / re-upload (deterministic cache).
- **[Claude + parse-papers session]** — coordinate on the variant emitter.

### Step 5 — Repoint the app  ← the only app-code change
In the 7 `subject.json`, change `assetBaseUrl` `https://audio.hsc.pebnum.com` →
`https://papers.hsc.pebnum.com`. Keep `audioBaseUrl` on `audio.hsc.pebnum.com`.
- **Command:**
  ```bash
  # after Steps 2–4 have populated the bucket for those subjects
  grep -rl '"assetBaseUrl": "https://audio.hsc.pebnum.com"' content/*/subject.json \
    | xargs sed -i '' 's#"assetBaseUrl": "https://audio.hsc.pebnum.com"#"assetBaseUrl": "https://papers.hsc.pebnum.com"#'
  python3 tools/generate_manifest.py        # assetBaseUrl is baked into manifest.json
  PAGES_BRANCH=main ./deploy.sh             # ship it (breaking prod is acceptable per Fred)
  ```
- **Check:** on prod, open a paper/generator crop and confirm it loads from `papers.hsc.pebnum.com`
  (DevTools network). Verify a subject whose crops are NOT yet migrated still works or is knowingly
  broken.
- **Rollback:** revert the sed + regenerate manifest + redeploy (≈2 min).
- **[Claude]**.

### Step 6 — Repoint tooling defaults
Point paper tooling at the new bucket so future uploads don't regress.
- Change `upload_questions.py` default bucket `hsc-podcast-audio` → `hsc-papers-and-resources`
  (or always pass it explicitly). Ensure `sync_bucket.py --delete` is **never** run against a bucket
  that mixes audio + papers — papers now have their own bucket, so a papers-only sync is safe there;
  audio sync stays on `hsc-podcast-audio`.
- **Check:** `--dry-run` a sync of each bucket; confirm no cross-contamination.
- **[Claude]**.

### Step 7 — Cleanup  ⚠️ DESTRUCTIVE — gated, do last, per-command go-ahead
Only after Steps 2–6 verified in production.
- Remove old paper crops from the audio bucket:
  `rclone delete r2:hsc-podcast-audio/<subject>/papers/ --dry-run` (review) → then without `--dry-run`.
- Fold `hsc-questions` in (Step 3), then delete the bucket.
- **Do NOT** delete `hsc-podcast-audio` (audio) or `hsc-podcast` (54 GB) — **inventory `hsc-podcast`
  first** (`rclone size r2:hsc-podcast`, `rclone lsd r2:hsc-podcast`) and identify the owner.
- **Rollback:** none (deletion is irreversible) → why it's gated and dry-run-first.
- **[Fred authorizes each delete].**

---

## Global rollback
The app depends only on `assetBaseUrl` (Step 5). To fully revert: `git revert` the subject.json
repoint, `generate_manifest.py`, redeploy — app is back on `audio.hsc.pebnum.com` in ~2 min. Bucket
uploads (Steps 2–4) are additive and harmless if left. Nothing is destructive until Step 7.

## Suggested execution order
1 (done) → **agree decisions #1–3** → 2 & 3 for **physics only** (proof) → 4 (physics) →
5 (physics-only repoint + deploy, verify on prod) → widen 2–4 to remaining active subjects →
optional bulk raw-paper pass for all subjects → 6 → 7 (gated).
