#!/usr/bin/env bash
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
#
# migrate-audio.sh — server-side R2→R2 copy of the legacy per-subject audio buckets into
# the single unified bucket, one folder per subject:
#
#   r2:hsc-phy-podcast/<ep>/<voice>.m4a  ->  r2:hsc-podcast-audio/physics/<ep>/<voice>.m4a
#   r2:hsc-sdd-podcast/<ep>/<voice>.m4a  ->  r2:hsc-podcast-audio/software/<ep>/<voice>.m4a
#
# Because source and dest are the same rclone remote (same R2 account/endpoint), rclone uses
# S3 server-side copy — no 42 GB flows through this machine, and R2↔R2 has no egress fee.
#
# PREREQ: an rclone remote named "r2" pointing at R2. Create it ONCE in your own terminal
# (keeps the secret out of this chat):
#
#   rclone config create r2 s3 \
#     provider=Cloudflare \
#     access_key_id=<R2_ACCESS_KEY_ID> \
#     secret_access_key=<R2_SECRET_ACCESS_KEY> \
#     endpoint=https://ac128818b294f0f51e44cb7082804bca.r2.cloudflarestorage.com \
#     acl=private
#
# (Get the keys from: Cloudflare dashboard → R2 → Manage API Tokens → Create API Token →
#  permission "Object Read & Write". The account id is already in the endpoint above.)
set -euo pipefail

REMOTE="${REMOTE:-r2}"
DEST="${DEST:-hsc-podcast-audio}"
FLAGS=(--transfers 32 --checkers 32 --fast-list --include '*.m4a' --progress --stats 10s)

command -v rclone >/dev/null || { echo "ERROR: rclone not installed." >&2; exit 1; }
rclone listremotes | grep -qx "${REMOTE}:" || {
  echo "ERROR: rclone remote '${REMOTE}:' not found. Create it first (see header)." >&2; exit 1; }

copy_subject() {
  local src_bucket="$1" subject="$2"
  echo "═══ ${src_bucket}  ->  ${DEST}/${subject}  (server-side) ═══"
  rclone copy "${REMOTE}:${src_bucket}" "${REMOTE}:${DEST}/${subject}" "${FLAGS[@]}"
}

copy_subject hsc-phy-podcast physics
copy_subject hsc-sdd-podcast software

echo ""
echo "═══ Verify object counts in ${DEST} ═══"
for subject in physics software; do
  n="$(rclone size "${REMOTE}:${DEST}/${subject}" --json 2>/dev/null | python3 -c 'import json,sys;print(json.load(sys.stdin)["count"])')"
  echo "  ${subject}: ${n} objects"
done
echo "Expected: physics 609, software 2198 (total 2807)."
echo "Done. Next: connect the custom domain audio.hsc.pebnum.com to ${DEST} (public access)."
