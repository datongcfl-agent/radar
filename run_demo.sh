#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
python3 -m unittest discover -s tests -v
rm -rf runs/weak-current-demo runs/pet-hospital-demo
python3 -m radar run --pack packs/weak-current/pack.json --seeds seeds/weak-current.json \
  --title "弱电管理系统" --out runs/weak-current-demo
python3 -m radar run --pack packs/pet-hospital/pack.json --seeds seeds/pet-hospital.json \
  --title "宠物医院管理系统" --out runs/pet-hospital-demo
echo
echo "看：runs/weak-current-demo/toc.md、coverage.md、gaps.md、report.md"
