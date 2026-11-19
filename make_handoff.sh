#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ "$#" -ge 1 ]; then
  OUT="$1"
else
  OUT="/tmp/radar-handoff-$(date +%Y%m%d).tar.gz"
fi
tar --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' \
    -czf "$OUT" -C "$HERE" .
echo "handoff: $OUT"
tar -tzf "$OUT" | head -20
