#!/usr/bin/env bash
#
# generate_all_voices.sh — render every episode in every selectable narrator voice.
# Each voice lands inside the episode folder as content/<…>/<voice>.m4a, so the viewer
# can offer them as a voice picker. The question (second) voice is the same across all.
#
# Works on both layouts: flat content/<episode>/ and unified content/<subject>/<episode>/.
#
# Usage:
#   ./generate_all_voices.sh                      # render all episodes, all voices (once)
#   ./generate_all_voices.sh PF11-01-Intro        # render one episode (folder name or path)
#   ./generate_all_voices.sh --once               # render only episodes that NEED it, then exit
#   ./generate_all_voices.sh --daemon             # DAEMON: watch content/, render new/changed
#                                                 #   scripts in the background, forever
#   CONTENT_DIR=content/physics ./generate_all_voices.sh --daemon   # scope to one subject
#   POLL_INTERVAL=5 ./generate_all_voices.sh --daemon               # poll faster (default 10s)
#
# In --daemon mode this renders audio IN PARALLEL with episode authoring: leave it running
# and the AI can keep writing scripts while each finished one is turned into audio behind it.
# Stop the daemon with Ctrl-C. Per-voice "already up to date, skip" is handled downstream, so
# re-rendering is always cheap and safe.

# NOTE: deliberately NOT 'set -e'. The two render stages below must BOTH run even if the other
# has failures — otherwise one failed neural (Kokoro) render would abort before the Eloquence
# (eSpeak) stage, silently leaving episodes with every neural voice but no Eloquence track.
# Each stage is resumable (skips up-to-date files), so the next pass picks up any stragglers.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CONTENT_DIR="${CONTENT_DIR:-$HERE/content}"
POLL_INTERVAL="${POLL_INTERVAL:-10}"

# The canonical set of narrator voices the user can choose between.
NARRATORS=(af_heart am_onyx am_santa bf_isabella bm_daniel bm_george)
# Second voice used for QUESTION: lines in every version.
QUESTION_VOICE="bm_fable"

# --- Render one batch (episode args, or none = "all" per the helpers' own discovery) -------
render() {
  echo "═══ Rendering ${#NARRATORS[@]} narrator voices: ${NARRATORS[*]} ═══"
  KOKORO_VOICES="${NARRATORS[*]}" \
  KOKORO_VOICE2="$QUESTION_VOICE" \
    "$HERE/_generate_audio.sh" "$@" \
    || echo "WARN: some neural (Kokoro) renders failed — continuing to Eloquence anyway."

  # eSpeak NG formant "Eloquence" — the crisp-at-extreme-speed track for the high-speed
  # listener. ALWAYS runs, even if the neural stage failed, so Eloquence is never skipped.
  echo "═══ Rendering formant high-speed voice: Eloquence (eSpeak NG) ═══"
  "$HERE/generate_espeak_voice.sh" "$@" \
    || echo "WARN: some Eloquence (eSpeak) renders failed — see above."
}

# --- Daemon helpers ------------------------------------------------------------------------
# Every episode folder (script.md at any depth), skipping underscore-prefixed dirs.
list_episodes() {
  find "$CONTENT_DIR" -type f -name script.md -not -path '*/_*' 2>/dev/null \
    | sed 's@/script\.md$@@' | sort
}

# Needs rendering if it has a script.md and any expected NARRATOR voice is missing or older than
# the script. We check each narrator voice individually rather than "any .m4a newer than the
# script" — otherwise an episode that only got the Eloquence (zz_eloquence_*) tracks would look
# done forever and the neural voices would never be (re)rendered. The helpers still do per-voice
# skipping downstream, so this is just a cheap gate to avoid spinning up the renderer for nothing.
needs_render() {
  local ep="$1" v
  [[ -f "$ep/script.md" ]] || return 1
  for v in "${NARRATORS[@]}"; do
    [[ -f "$ep/$v.m4a" ]] || return 0          # narrator voice missing entirely
    [[ "$ep/script.md" -nt "$ep/$v.m4a" ]] && return 0   # script edited since this voice rendered
  done
  return 1
}

# Render only the episodes that currently need it. Returns 1 if there was nothing to do.
render_pending() {
  local pending=() ep
  while IFS= read -r ep; do
    [[ -n "$ep" ]] && needs_render "$ep" && pending+=("$ep")
  done < <(list_episodes)
  [[ ${#pending[@]} -eq 0 ]] && return 1
  echo "[$(date '+%H:%M:%S')] $((${#pending[@]})) episode(s) to render: ${pending[*]##*/}"
  render "${pending[@]}"
  return 0
}

# --- Parse flags ---------------------------------------------------------------------------
MODE="all"          # all | once | daemon
PASS=()             # passthrough episode args
for arg in "$@"; do
  case "$arg" in
    --daemon|--watch) MODE="daemon" ;;
    --once)           MODE="once" ;;
    -h|--help)        sed -n '2,30p' "$HERE/$(basename "$0")"; exit 0 ;;
    *)                PASS+=("$arg") ;;
  esac
done

[[ -d "$CONTENT_DIR" ]] || { echo "ERROR: content dir '$CONTENT_DIR' not found." >&2; exit 1; }

case "$MODE" in
  daemon)
    echo "Voice daemon watching '$CONTENT_DIR' (poll ${POLL_INTERVAL}s) — Ctrl-C to stop."
    trap 'echo; echo "Stopped."; exit 0' INT
    while true; do
      render_pending || true
      sleep "$POLL_INTERVAL"
    done
    ;;
  once)
    if render_pending; then
      echo "All voices done."
    else
      echo "Nothing to render — every episode is up to date."
    fi
    ;;
  all)
    render "${PASS[@]}"
    echo "All voices done. Each episode folder now holds one .m4a per voice (incl. Eloquence)."
    ;;
esac
