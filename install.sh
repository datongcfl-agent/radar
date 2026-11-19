#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:?用法: bash install.sh <target-workspace>}"
mkdir -p "$TARGET/.dsh/skills"
rm -rf "$TARGET/.dsh/skills/radar"
cp -r "$HERE/.dsh/skills/radar" "$TARGET/.dsh/skills/radar"
echo "已安装到 $TARGET/.dsh/skills/radar"
