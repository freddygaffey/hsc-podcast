#!/usr/bin/env bash
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
#
# deploy-legacy.sh — repoint a legacy single-subject app at the unified audio bucket
# (audio.hsc.pebnum.com/<subject>/...) and redeploy it to its existing Pages project.
# The legacy apps keep their own app code; only their manifest's audio URLs change.
#
#   tools/deploy-legacy.sh hsc-phy-podcast physics  hsc-phy-podcast
#   tools/deploy-legacy.sh hsc-sdd-podcast software hsc-podcast
#
# Env: AUDIO_BASE_URL (default https://audio.hsc.pebnum.com)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"

SRC="${1:?legacy dir}"; SUBJECT="${2:?subject}"; PROJECT="${3:?pages project}"
AUDIO="${AUDIO_BASE_URL:-https://audio.hsc.pebnum.com}"
DIST="dist-legacy-$SUBJECT"
[ -d "$SRC" ] || { echo "ERROR: $SRC not found" >&2; exit 1; }

echo "==> Assembling $DIST/ from $SRC (audio -> $AUDIO/$SUBJECT/...)"
rm -rf "$DIST"; mkdir -p "$DIST"

# App shell (copy whatever the legacy app has).
for f in index.html app.js auth.js style.css speed-engine.js app.webmanifest _headers; do
  [ -f "$SRC/$f" ] && cp "$SRC/$f" "$DIST/"
done
# Stamp the SW build version if it uses the __BUILD__ placeholder.
if [ -f "$SRC/service-worker.js" ]; then
  sed "s/__BUILD__/$(date +%s)/" "$SRC/service-worker.js" > "$DIST/service-worker.js"
fi
[ -d "$SRC/vendor" ] && cp -r "$SRC/vendor" "$DIST/"
[ -d "$SRC/icons" ]  && cp -r "$SRC/icons"  "$DIST/"

# Per-episode text only (no audio).
rsync -a --prune-empty-dirs \
  --include='*/' --include='script.md' --include='supplementary.md' --include='quiz.json' \
  --exclude='*' "$SRC/content/" "$DIST/content/"

# Rewrite the manifest's audio URLs to the unified bucket, subject-prefixed.
python3 - "$SRC/manifest.json" "$SUBJECT" "$AUDIO" "$DIST/manifest.json" <<'PY'
import json, sys
src, subject, audio, out = sys.argv[1:5]
m = json.load(open(src))
n = 0
for mod in m.get("modules", []):
    for ep in mod.get("episodes", []):
        for v in ep.get("voices", []):
            v["file"] = f"{audio.rstrip('/')}/{subject}/{ep['id']}/{v['name']}.m4a"
            n += 1
json.dump(m, open(out, "w"), indent=2)
print(f"    rewrote {n} audio URLs")
PY

# Safety: never ship audio.
if find "$DIST" \( -name '*.m4a' -o -name '*.wav' \) | grep -q .; then
  echo "ERROR: audio found in $DIST" >&2; exit 1
fi
echo "==> dist: $(du -sh "$DIST" | cut -f1)"
echo "==> Deploying to Pages project: $PROJECT"
wrangler pages deploy "$DIST" --project-name "$PROJECT" --commit-dirty=true
echo "==> Done. $SRC now streams audio from $AUDIO/$SUBJECT/"
