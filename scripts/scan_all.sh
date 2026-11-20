#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE"
STAMP="$(date +%Y%m%d-%H%M%S)"
BASE_ROOT="${BASE_ROOT:-runs}"
CODE=0
for name in weak-current video-kb pet-hospital; do
  pack="packs/${name}/pack.json"
  seeds="seeds/${name}.json"
  [ -f "$pack" ] || continue
  base="${BASE_ROOT}/${name}-last"
  if [ ! -e "$base" ]; then base="${BASE_ROOT}/${name}-demo"; fi
  out="${BASE_ROOT}/${name}-scan-${STAMP}"
  echo "== $name -> $out (base $base)"
  set +e
  python3 -m radar scan --pack "$pack" --seeds "$seeds" \
    --title "$name scan" --out "$out" --base "$base" \
    --verify-quotes --require-web-verify --fail-on-change
  rc=$?
  set -e
  if [ "$rc" -eq 0 ] || [ "$rc" -eq 2 ]; then
    ln -sfn "$(basename "$out")" "$base"
  fi
  [ "$rc" -eq 1 ] && CODE=1
  [ "$rc" -eq 2 ] && CODE=2
done
exit "$CODE"
