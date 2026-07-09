#!/bin/bash
# Resilient sync: lives OUTSIDE the git repo so `git clean` in the repo can't
# delete it. Pulls the server's papers into the local (git-ignored) papers dir
# every 5 min. Merge-only (no --delete): never removes local files.
SERVER="root@api.plane.pebnums.com:/root/hsc-papers/"
DEST="/Users/fred/hsc-podcast/papers/"
LOG="/Users/fred/.hsc-sync.log"
while true; do
  mkdir -p "$DEST"
  echo "$(date '+%Y-%m-%d %H:%M:%S')  syncing..." >> "$LOG"
  rsync -az --exclude='_*' --exclude='.gitignore' \
    -e "ssh -o BatchMode=yes -o ConnectTimeout=20" \
    "$SERVER" "$DEST" >> "$LOG" 2>&1
  echo "$(date '+%Y-%m-%d %H:%M:%S')  done ($(find "$DEST" -name '*.pdf' 2>/dev/null | wc -l | tr -d ' ') local PDFs)" >> "$LOG"
  sleep 300
done
