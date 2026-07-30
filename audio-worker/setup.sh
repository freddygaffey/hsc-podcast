#!/usr/bin/env bash
# setup.sh — provision the private audio bucket, PIN and Worker in ONE go.
#
# Run this yourself: it needs an interactive `wrangler login`, which an agent can't do.
#
#   cd audio-worker
#   ./setup.sh                 # DRY RUN — shows every command, changes nothing
#   ./setup.sh --go            # actually provision
#
# Afterwards, upload your own file:
#   wrangler r2 object put hsc-podcast-private/past-the-shallows/book.m4a \
#     --file /path/to/your.m4a --content-type audio/mp4

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

BUCKET="${BUCKET:-hsc-podcast-private}"
DB_NAME="${DB_NAME:-hsc-podcast-auth}"
PIN="${PIN:-}"
GO=0
[[ "${1:-}" == "--go" ]] && GO=1

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
run() {
  echo "  \$ $*"
  if [[ $GO == 1 ]]; then "$@" || { echo "  ^ FAILED" >&2; return 1; }; fi
}

command -v wrangler >/dev/null || { echo "ERROR: wrangler not installed (npm i -g wrangler)" >&2; exit 1; }
command -v python3  >/dev/null || { echo "ERROR: python3 required" >&2; exit 1; }

if [[ -z "$PIN" ]]; then
  echo "No PIN given. Set one explicitly, e.g.:  PIN=1234 ./setup.sh --go" >&2
  echo "(A PIN generated for you is in audio-worker/README.md.)" >&2
  exit 1
fi
[[ "$PIN" =~ ^[0-9]{4}$ ]] || { echo "ERROR: PIN must be exactly 4 digits." >&2; exit 1; }

bold "Private audio setup"
echo "  bucket : $BUCKET  (private — no custom domain, no r2.dev)"
echo "  db     : $DB_NAME"
echo "  mode   : $([[ $GO == 1 ]] && echo LIVE || echo 'DRY RUN (pass --go)')"
echo

# Salt + PBKDF2 hash computed locally; the bare PIN never leaves this machine.
read -r SALT HASH <<<"$(python3 - "$PIN" <<'PY'
import hashlib, secrets, sys
pin = sys.argv[1]
salt = secrets.token_hex(16)
h = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt.encode(), 600000, dklen=32).hex()
print(salt, h)
PY
)"

bold "1. Private bucket"
run wrangler r2 bucket create "$BUCKET"

bold "2. Schema (same DB as the auth worker)"
run wrangler d1 execute "$DB_NAME" --remote --file schema.sql

bold "3. Store the PIN hash"
SQL="INSERT INTO pin_auth (id, pin_hash, salt, created) VALUES (1, '$HASH', '$SALT', strftime('%s','now'))
     ON CONFLICT(id) DO UPDATE SET pin_hash=excluded.pin_hash, salt=excluded.salt, created=excluded.created;"
run wrangler d1 execute "$DB_NAME" --remote --command "$SQL"

bold "4. Session signing secret"
if [[ $GO == 1 ]]; then
  python3 -c "import secrets;print(secrets.token_hex(32))" | wrangler secret put SESSION_SECRET
else
  echo "  \$ python3 -c 'import secrets;print(secrets.token_hex(32))' | wrangler secret put SESSION_SECRET"
fi

bold "5. Deploy"
run wrangler deploy

echo
if [[ $GO == 0 ]]; then
  bold "DRY RUN — nothing changed. Re-run with --go."
  exit 0
fi

bold "Done. Verify it actually refuses anonymous reads:"
cat <<'EOF'
  curl -si https://<worker-url>/past-the-shallows/book.m4a | head -1        # expect 401
  curl -sX POST https://<worker-url>/session \
       -H 'Content-Type: application/json' -d '{"pin":"XXXX"}'              # expect {"token":...}
EOF
echo
echo "IMPORTANT: paste the database_id from 'wrangler d1 list' into wrangler.toml"
echo "before step 5 if you haven't already, or the deploy will fail."
