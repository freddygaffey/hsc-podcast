#!/bin/bash
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# Pull textbooks downloaded on the server into the local staging dir every 3 min.
while true; do
  rsync -a --exclude='_*' -e "ssh -o BatchMode=yes -o ConnectTimeout=20" \
    root@api.plane.pebnums.com:/root/hsc-textbooks/ /Users/fred/hsc-textbooks/ \
    >> /Users/fred/.hsc-textbook-sync.log 2>&1
  echo "$(date '+%H:%M:%S') textbooks local: $(find /Users/fred/hsc-textbooks -type f ! -name '_*'|wc -l|tr -d ' ')" >> /Users/fred/.hsc-textbook-sync.log
  sleep 180
done
