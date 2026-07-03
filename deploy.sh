#!/usr/bin/env bash
#
# deploy.sh — build a clean dist/ and deploy the unified app to Cloudflare Pages.
#
# Ships the app shell + per-episode markdown/quiz + the manifest. Audio is NOT shipped
# (it streams from R2 via each subject's audioBaseUrl). Run from the repo root.
#
#   ./deploy.sh                                   # deploy to $PAGES_PROJECT (default below)
#   PAGES_PROJECT=hsc-podcast-unified ./deploy.sh
#
# Prereqs: wrangler (logged in), rsync, git.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PAGES_PROJECT="${PAGES_PROJECT:-hsc-podcast-unified}"
DIST="${DIST:-dist}"
BUILD="$(git rev-parse --short HEAD 2>/dev/null || date +%s)"

echo "==> Assembling $DIST/ (build $BUILD)"
rm -rf "$DIST"; mkdir -p "$DIST"

# App shell.
cp index.html generator.html paper-export.js app.js auth.js style.css speed-engine.js app.webmanifest _headers "$DIST/"
# Service worker — stamp the build version so each deploy gets a fresh APP_SHELL cache.
sed "s/__BUILD__/$BUILD/" service-worker.js > "$DIST/service-worker.js"
# Manifest + vendored libs + icons.
cp manifest.json "$DIST/"
cp -r vendor "$DIST/"
cp -r icons "$DIST/"

# Per-episode text the app fetches at runtime (script/supplementary/quiz only). Skip
# underscore dirs (the _template-subject scaffold) and never ship audio or voices.json.
rsync -a --prune-empty-dirs \
  --exclude='_*' \
  --exclude='resources' \
  --include='*/' \
  --include='script.md' --include='supplementary.md' --include='quiz.json' \
  --include='questions.json' --include='subject.json' \
  --include='*.png' --include='*.jpg' --include='*.jpeg' --include='*.webp' --include='*.svg' \
  --include='paper.pdf' --include='mg.pdf' \
  --exclude='*' \
  content/ "$DIST/content/"

# Safety net: no audio in the Pages bundle.
if find "$DIST" \( -name '*.m4a' -o -name '*.wav' \) | grep -q .; then
  echo "ERROR: audio found in $DIST — aborting (audio belongs in R2)." >&2; exit 1
fi

echo "==> dist: $(du -sh "$DIST" | cut -f1), $(find "$DIST" -type f | wc -l | tr -d ' ') files"
echo "==> Deploying to Pages project: $PAGES_PROJECT"
DEPLOY_ARGS=(--project-name "$PAGES_PROJECT" --commit-dirty=true)
# PAGES_BRANCH=main forces a production deploy even from a feature git branch.
[ -n "${PAGES_BRANCH:-}" ] && DEPLOY_ARGS+=(--branch "$PAGES_BRANCH")
wrangler pages deploy "$DIST" "${DEPLOY_ARGS[@]}"
echo "==> Done."
