#!/usr/bin/env bash
# run.sh — launch one phase prompt in a fresh amp thread.
# Usage: bash docs/handoff/prompts/run.sh <phase-number>
#        bash docs/handoff/prompts/run.sh 01
#        bash docs/handoff/prompts/run.sh 14
#
# Auto-resolves mode (rush/deep/smart) by matching the phase file name.

set -euo pipefail
phase="${1:-}"
[ -z "$phase" ] && { echo "usage: $0 <phase>"; exit 1; }

dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
file="$(ls "$dir"/phase-"$phase"-*.txt 2>/dev/null | head -1)"
[ -z "$file" ] && { echo "ERROR: no prompt for phase $phase in $dir"; exit 1; }

# mode is the third token in the filename: phase-NN-<mode>.txt
mode="$(basename "$file" .txt | awk -F- '{print $3}')"
echo "→ phase=$phase mode=$mode file=$file"

if ! command -v amp >/dev/null 2>&1; then
  echo "ERROR: amp CLI not found in PATH"; exit 1
fi

exec amp threads new --mode "$mode" --execute "$(cat "$file")"
