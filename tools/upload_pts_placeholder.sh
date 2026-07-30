#!/usr/bin/env bash
# upload_pts_placeholder.sh — publish the Past the Shallows PLACEHOLDER audio to R2.
#
# The English Standard player ships with a placeholder track instead of a narration
# of the novel (which is in copyright and is not distributed). The placeholder tells
# the listener to load their own audiobook file; once they pick one, the app plays
# that local file instead and the placeholder is never heard again.
#
# You run this yourself — it is not run automatically.
#
#   ./tools/upload_pts_placeholder.sh                 # DRY RUN (default): shows what would happen
#   ./tools/upload_pts_placeholder.sh --go            # actually generate + upload
#   SRC_DIR=~/my-dummies ./tools/upload_pts_placeholder.sh --go   # use YOUR files instead
#
# PREREQ: an rclone remote named "r2" (same one tools/migrate-audio.sh uses).
#   rclone listremotes | grep r2:
# Also needs espeak-ng + ffmpeg, but ONLY when generating (not when SRC_DIR is set).

set -uo pipefail

REMOTE="${REMOTE:-r2}"
BUCKET="${R2_BUCKET:-hsc-podcast-audio}"
DEST="english-standard/past-the-shallows"
SRC_DIR="${SRC_DIR:-}"                      # set this to use your own dummy files
BUILD="${BUILD:-$(mktemp -d)}"
GO=0
[[ "${1:-}" == "--go" ]] && GO=1

# The placeholder script. Keep it short — it plays once, before the user loads a file.
read -r -d '' MSG <<'EOF'
Past the Shallows is not available here. This book is in copyright, so no recording of it
is included with this app. To listen, tap the button on screen and choose your own audiobook
file. It stays on your device, and the scene map will follow along with it automatically.
EOF

say_what() { printf '\033[1m%s\033[0m\n' "$*"; }

say_what "Past the Shallows — placeholder audio"
echo "  remote : ${REMOTE}:${BUCKET}/${DEST}"
echo "  source : ${SRC_DIR:-<generate with espeak-ng>}"
echo "  mode   : $([[ $GO == 1 ]] && echo LIVE || echo 'DRY RUN (pass --go to actually do it)')"
echo

command -v rclone >/dev/null || { echo "ERROR: rclone not installed." >&2; exit 1; }
rclone listremotes | grep -qx "${REMOTE}:" || {
  echo "ERROR: rclone remote '${REMOTE}:' not found. See tools/migrate-audio.sh header." >&2; exit 1; }

if [[ -n "$SRC_DIR" ]]; then
  [[ -d "$SRC_DIR" ]] || { echo "ERROR: SRC_DIR '$SRC_DIR' not found." >&2; exit 1; }
  STAGE="$SRC_DIR"
  echo "Using your files from $STAGE:"
  ls -1 "$STAGE" | sed 's/^/  /'
else
  command -v espeak-ng >/dev/null || { echo "ERROR: espeak-ng not installed (brew install espeak-ng)." >&2; exit 1; }
  command -v ffmpeg    >/dev/null || { echo "ERROR: ffmpeg not installed (brew install ffmpeg)." >&2; exit 1; }
  STAGE="$BUILD"
  echo "Would generate into $STAGE:"
  # One file per voice slot the player might ask for, so the picker never 404s.
  for v in placeholder zz_eloquence_british zz_eloquence_received; do
    echo "  ${v}.m4a"
    if [[ $GO == 1 ]]; then
      printf '%s\n' "$MSG" > "$STAGE/msg.txt"
      espeak-ng -v en-gb -s 165 -p 50 -w "$STAGE/${v}.wav" -f "$STAGE/msg.txt" 2>/dev/null
      ffmpeg -y -loglevel error -i "$STAGE/${v}.wav" -c:a aac -b:a 48k "$STAGE/${v}.m4a"
      rm -f "$STAGE/${v}.wav"
    fi
  done
  [[ $GO == 1 ]] && rm -f "$STAGE/msg.txt"
fi

echo
if [[ $GO == 0 ]]; then
  say_what "DRY RUN — nothing generated, nothing uploaded."
  echo "Re-run with --go when you're happy:"
  echo "  ./tools/upload_pts_placeholder.sh --go"
  exit 0
fi

say_what "Uploading to ${REMOTE}:${BUCKET}/${DEST} ..."
rclone copy "$STAGE" "${REMOTE}:${BUCKET}/${DEST}" \
  --include '*.m4a' --progress --transfers 4 --checkers 8 || {
    echo "ERROR: rclone copy failed." >&2; exit 1; }

echo
say_what "Done. Now on R2:"
rclone ls "${REMOTE}:${BUCKET}/${DEST}" | sed 's/^/  /'
echo
echo "Public URLs will be:"
rclone lsf "${REMOTE}:${BUCKET}/${DEST}" | sed "s|^|  https://audio.hsc.pebnum.com/${DEST}/|"
