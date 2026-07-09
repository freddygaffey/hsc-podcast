#!/bin/bash
# STOP (2026-07-09): Repo locked until 6 Nov 2026 (after the HSC). No work here without tangible study gain. See STOP-UNTIL-NOV-6.md. Go do past papers.
# =====================================================================
# HSC past-paper pipeline — RESUME / RESTART
# Lives outside the git repo so `git clean` can't delete it.
# Run:  bash ~/hsc-resume.sh
# Safe to run anytime; it only starts things that aren't already running.
# =====================================================================
SERVER="root@api.plane.pebnums.com"
SRVDIR="/root/hsc-papers"
LOCALDIR="/Users/fred/hsc-podcast/papers"
SYNC="/Users/fred/.hsc-sync.sh"
SSH="ssh -o BatchMode=yes -o ConnectTimeout=20"

echo "== 1. SERVER downloader (all THSC subjects) =="
$SSH "$SERVER" "cd $SRVDIR && pgrep -f 'python3 _downloader.py' >/dev/null \
  && echo '   already running' \
  || { setsid nohup python3 _downloader.py >> _download.log 2>&1 </dev/null & echo '   RESTARTED'; }" </dev/null

echo "== 2. SERVER NESA official papers (re-run to fill any gaps; skips existing) =="
$SSH "$SERVER" "cd $SRVDIR && pgrep -f 'python3 _nesa.py' >/dev/null \
  && echo '   already running' \
  || { setsid nohup python3 _nesa.py >> _nesa.log 2>&1 </dev/null & echo '   (re)launched'; }" </dev/null

echo "== 2b. SERVER acehsc.net papers (one-shot; resumable, skips existing) =="
$SSH "$SERVER" "cd $SRVDIR && grep -q '=== acehsc done' _acehsc.log 2>/dev/null && echo '   already complete' \
  || { pgrep -f 'python3 _acehsc.py' >/dev/null && echo '   already running' \
       || { setsid nohup python3 _acehsc.py --all-types >> _acehsc.log 2>&1 </dev/null & echo '   (re)launched'; }; }" </dev/null

echo "== 2c. SERVER textbook grabber (Drive -> /root/hsc-textbooks; resumable, skips existing) =="
$SSH "$SERVER" "grep -q '=== grab done' /root/hsc-textbooks/_grab.log 2>/dev/null && echo '   already complete' \
  || { ps -eo comm,args | awk '\$1 ~ /python/ && /_grab.py/' | grep -q . && echo '   already running' \
       || { cd /root && setsid nohup python3 _grab.py >> /root/hsc-textbooks/_grab.log 2>&1 </dev/null & echo '   (re)launched'; }; }" </dev/null

echo "== 2d. LOCAL textbook sync loop (server -> ~/hsc-textbooks every 3 min) =="
if pgrep -f ".hsc-textbook-sync.sh" >/dev/null; then echo "   already running"; else
  nohup /Users/fred/.hsc-textbook-sync.sh >> /Users/fred/.hsc-textbook-sync.log 2>&1 & disown; echo "   RESTARTED"; fi

echo "== 3. LOCAL sync loop (server -> $LOCALDIR every 5 min) =="
if pgrep -f ".hsc-sync.sh" >/dev/null; then
  echo "   already running"
else
  nohup "$SYNC" >> /Users/fred/.hsc-sync.log 2>&1 & disown
  echo "   RESTARTED"
fi

echo "== 4. force one sync now =="
rsync -az --exclude='_*' --exclude='.gitignore' -e "$SSH" "$SERVER:$SRVDIR/" "$LOCALDIR/" && echo "   sync ok"

echo "== 5. status =="
srv=$($SSH "$SERVER" "find $SRVDIR -name '*.pdf' | wc -l" </dev/null)
loc=$(find "$LOCALDIR" -name '*.pdf' | wc -l | tr -d ' ')
left=$($SSH "$SERVER" "grep -aoE 'left [0-9]+' $SRVDIR/_download.log | tail -1" </dev/null)
echo "   server PDFs: $srv | local PDFs: $loc | THSC $left"
