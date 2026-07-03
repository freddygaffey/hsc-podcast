#!/bin/bash
# Overnight free batch: OCR-segment + bake every rendered paper (no LLM tokens).
cd "$(dirname "$0")/.."
LOG=papers/_work/_batch.log
: > "$LOG"
n=0; ok=0
for wd in papers/_work/*/; do
  [ -f "$wd/info.json" ] || continue
  pid=$(basename "$wd")
  n=$((n+1))
  echo "[$n] $pid" >> "$LOG"
  python3 tools/locate_ocr.py "$pid"      >> "$LOG" 2>&1 && \
  python3 tools/bake_questions.py "$pid"   >> "$LOG" 2>&1 && ok=$((ok+1)) || echo "  FAILED $pid" >> "$LOG"
done
echo "BATCH DONE: $ok/$n papers baked" >> "$LOG"
