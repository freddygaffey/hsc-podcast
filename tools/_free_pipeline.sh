#!/bin/bash
# Free full-corpus baseline: render -> OCR-segment -> bake, zero LLM tokens. Maths first.
cd "$(dirname "$0")/.."
LOG=papers/_work/_free.log; : > "$LOG"
n=0; ok=0
while IFS= read -r path; do
  [ -z "$path" ] && continue
  n=$((n+1))
  # render prints "paperId: <pid>"
  pid=$(python3 tools/render_paper.py "$path" 2>>"$LOG" | grep -oE 'paperId: [^ ]+' | head -1 | cut -d' ' -f2)
  [ -z "$pid" ] && { echo "[$n] RENDER-FAIL $path" >>"$LOG"; continue; }
  python3 tools/locate_ocr.py "$pid" >>"$LOG" 2>&1 && \
  python3 tools/bake_questions.py "$pid" >>"$LOG" 2>&1 && ok=$((ok+1)) || echo "[$n] FAIL $pid" >>"$LOG"
  # free disk: drop page PNGs after baking (keep ocr.json cache + baked/)
  rm -f "papers/_work/$pid"/p*.png 2>/dev/null
  [ $((n % 10)) -eq 0 ] && echo "PROGRESS: $ok/$n baked" >>"$LOG"
done < papers/_work/_free_paths.txt
echo "FREE PIPELINE DONE: $ok/$n baked" >>"$LOG"
