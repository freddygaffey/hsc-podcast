#!/usr/bin/env bash
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
#
# generate_espeak_voice.sh — render each episode with the eSpeak NG formant
# synthesizer as extra high-speed "Eloquence" voices — one per accent, saved as
# content/<episode>/zz_eloquence_<accent>.m4a (e.g. zz_eloquence_british.m4a).
#
# Why a formant synth as well as the neural Kokoro voices:
#   Research on high-speed listening (see _research/) found that at extreme
#   playback speeds, old formant synthesizers (Eloquence/DECtalk/eSpeak class)
#   stay crisp and intelligible where natural neural voices smear — it's what
#   screen-reader power users run at 18-22 syllables/second. So this is the voice
#   for the high-speed / 16x track. The neural voices remain the natural default.
#
# It auto-appears in the player's voice picker: generate_manifest.py discovers any
# <episode>/*.m4a, and the app's cleanVoiceName() renders "zz_eloquence" as
# "Eloquence" (the prefix is dropped) and sorts it last.
#
# Usage:
#   ./generate_espeak_voice.sh                       # every episode in content/
#   ./generate_espeak_voice.sh SA-20-01-What-is-AI-vs-ML   # one episode (folder name)
#
# Optional environment variables:
#   ESPEAK_ACCENTS  space-separated label=code set; one .m4a per accent per episode
#                   (default: ALL distinct English accents — see the ACCENTS block below).
#                   NB: eSpeak NG has no Australian accent.
#   ESPEAK_WPM    words/minute at 1x (the player applies speed)  (default: 175)
#   ESPEAK_PITCH  pitch 0-99                                      (default: 50)
#   ESPEAK_BIN    path to the espeak-ng binary                    (default: espeak-ng)
#   JOBS          episodes rendered in parallel (each render ~30s, so this matters)
#                 (default: CPU cores minus 2)

set -uo pipefail   # NOT -e: one failed render must not abort the whole batch

ESPEAK_BIN="${ESPEAK_BIN:-espeak-ng}"
ESPEAK_WPM="${ESPEAK_WPM:-175}"
ESPEAK_PITCH="${ESPEAK_PITCH:-50}"
CORES="$(sysctl -n hw.ncpu 2>/dev/null || nproc 2>/dev/null || echo 4)"
JOBS="${JOBS:-$(( CORES > 2 ? CORES - 2 : 1 ))}"   # parallel episodes; leave 2 cores free

# ── ACCENT SET ──────────────────────────────────────────────────────────────
# Each entry is  label=espeak-voice-code.  Every episode gets ONE file per accent:
#   content/<episode>/zz_eloquence_<label>.m4a   →  picker shows "Eloquence <Label>"
# (the zz_ prefix keeps them grouped and sorted last; the app's cleanVoiceName drops
#  the prefix and title-cases the rest, so label "received" → "Eloquence Received").
# eSpeak NG English accents on this machine (see: espeak-ng --voices=en):
#   en-gb (British) · en-gb-x-rp (Received Pronunciation) · en-gb-scotland (Scottish)
#   en-gb-x-gbclan (Lancaster) · en-us (American) · en-us-nyc (New York) · en-029 (Caribbean)
#   NB: eSpeak NG has NO Australian accent.
# Default = ALL distinct English accents eSpeak NG provides (each adds one "Eloquence
# <Label>" row to the player's voice picker). Trim the set if the picker gets too long,
# either by editing this line or via the ESPEAK_ACCENTS env var, e.g.:
#   ESPEAK_ACCENTS="british=en-gb american=en-us" ./generate_espeak_voice.sh
# (eSpeak NG still has no Australian accent.)
ACCENTS=(
  american=en-us            # Eloquence American
  newyork=en-us-nyc         # Eloquence Newyork
  british=en-gb             # Eloquence British
  received=en-gb-x-rp       # Eloquence Received  (Received Pronunciation)
  scottish=en-gb-scotland   # Eloquence Scottish
  lancaster=en-gb-x-gbclan  # Eloquence Lancaster
  westmidlands=en-gb-x-gbcwmd  # Eloquence Westmidlands
  caribbean=en-029          # Eloquence Caribbean
)
if [[ -n "${ESPEAK_ACCENTS:-}" ]]; then read -r -a ACCENTS <<< "$ESPEAK_ACCENTS"; fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SELF="$HERE/$(basename "${BASH_SOURCE[0]}")"   # absolute path, for parallel worker re-invocation
CONTENT_DIR="$HERE/content"
STRIPPER="$HERE/strip_markdown.py"

if ! command -v "$ESPEAK_BIN" >/dev/null 2>&1; then
  cat >&2 <<EOF
Error: espeak-ng not found (ESPEAK_BIN=$ESPEAK_BIN).
Install it with:  brew install espeak-ng      (macOS)
                  sudo apt install espeak-ng   (Debian/Ubuntu)
EOF
  exit 1
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg not found (needed to encode .m4a)." >&2
  exit 1
fi

# --- One episode's work: strip the script once, then render every accent -----
render_episode() {
  local ep="$1"
  local name src tmp_txt pair label code out wav
  name="$(basename "$ep")"
  src="$ep/script.md"

  # Clean the script to prose ONCE per episode (it's accent-independent), then reuse it
  # for every accent. Drop NARRATOR:/QUESTION: speaker labels and [pause] markers
  # (Kokoro consumes those; eSpeak should not read them aloud).
  tmp_txt="$(mktemp -t espeak.XXXXXX).txt"
  python3 "$STRIPPER" "$src" | python3 -c '
import re, sys
t = sys.stdin.read()
t = re.sub(r"(?im)^\s*\**\s*(NARRATOR|QUESTION)\s*\**\s*:\s*", "", t)
t = re.sub(r"(?im)^\s*\[?\s*pause\s*\]?\s*$", "", t)
sys.stdout.write(t)
' > "$tmp_txt"

  if [[ ! -s "$tmp_txt" ]]; then
    echo "  ! $name/script.md produced no text, skipping"
    rm -f "$tmp_txt"
    return 0
  fi

  # One audio file per accent.
  for pair in "${ACCENTS[@]}"; do
    label="${pair%%=*}"
    code="${pair#*=}"
    out="$ep/zz_eloquence_${label}.m4a"

    # Skip if up to date, so re-runs only touch changed episodes/accents.
    if [[ -e "$out" && "$out" -nt "$src" ]]; then
      echo "  = $name/zz_eloquence_${label}.m4a up to date, skipping"
      continue
    fi

    wav="$(mktemp -t espeak.XXXXXX).wav"
    echo "  -> $name/zz_eloquence_${label}.m4a   ($code)"
    if "$ESPEAK_BIN" -v "$code" -s "$ESPEAK_WPM" -p "$ESPEAK_PITCH" -w "$wav" -f "$tmp_txt" \
       && ffmpeg -y -loglevel error -i "$wav" -c:a aac -b:a 96k \
            -metadata artist="eSpeak NG: $code" \
            -metadata album="Voice: Eloquence ${label} (formant, high-speed track)" \
            -metadata comment="engine=espeak-ng voice=$code wpm=$ESPEAK_WPM" \
            "$out"; then
      :
    else
      # Don't leave a truncated/unreadable .m4a behind (the manifest would warn on it).
      echo "  ! FAILED $name/zz_eloquence_${label}.m4a — removing partial file" >&2
      rm -f "$out"
    fi
    rm -f "$wav"
  done

  rm -f "$tmp_txt"
}

# --- WORKER MODE: render the episode(s) handed to us, then exit --------------
# The orchestrator re-invokes this script as  "$SELF" --worker <episode-dir>  via
# xargs -P, so JOBS episodes render at once (eSpeak does one file at a time, ~30s each —
# the win is running many episodes in parallel across the CPU cores).
if [[ "${1:-}" == "--worker" ]]; then
  shift
  for ep in "$@"; do render_episode "$ep"; done
  exit 0
fi

# --- Gather episodes (same selection rules as generate_audio.sh) -------------
shopt -s nullglob
EPISODES=()
if [[ $# -gt 0 ]]; then
  for arg in "$@"; do
    if   [[ -f "$arg" && "$(basename "$arg")" == "script.md" ]]; then EPISODES+=("$(dirname "$arg")")
    elif [[ -d "$arg" && -f "$arg/script.md" ]]; then EPISODES+=("$arg")
    elif [[ -f "$CONTENT_DIR/$arg/script.md" ]]; then EPISODES+=("$CONTENT_DIR/$arg")
    else echo "Skipping (no script.md found): $arg" >&2; fi
  done
else
  # script.md at ANY depth (flat content/<episode>/ AND unified content/<subject>/<episode>/),
  # skipping underscore-prefixed dirs (templates, _example-episode, _plans, …).
  while IFS= read -r dir; do
    EPISODES+=("$dir")
  done < <(find "$CONTENT_DIR" -type f -name script.md -not -path '*/_*' 2>/dev/null \
             | sed 's@/script\.md$@@' | sort)
fi

if [[ ${#EPISODES[@]} -eq 0 ]]; then
  echo "No episodes found in $CONTENT_DIR." >&2
  exit 0
fi

echo "Rendering ${#EPISODES[@]} episode(s) × ${#ACCENTS[@]} accent(s) @ ${ESPEAK_WPM} wpm, ${JOBS} episodes in parallel:"
for pair in "${ACCENTS[@]}"; do echo "    zz_eloquence_${pair%%=*}.m4a   (${pair#*=})"; done

# Run JOBS episodes at once. Null-delimited (-0) so paths with spaces are safe; one
# episode per worker (-n1). Each worker is a fresh --worker invocation of this script.
printf '%s\0' "${EPISODES[@]}" | xargs -0 -n1 -P "$JOBS" "$SELF" --worker

echo "Done. Run tools/generate_manifest.py to surface the new voices in the app."
