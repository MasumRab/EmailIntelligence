#!/bin/bash
# Regression test for terminal escape sequence injection (OSC sequences)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cat "$PROJECT_ROOT/scripts/test_orchestration.sh" | sed -n '/^log_info() {/,/^}/p' > temp_log_info.sh
BLUE='\033[0;34m'
NC='\033[0m'
source temp_log_info.sh

var=$'\x1b]0;pwned\x07'
output=$(log_info "$var")

# Log info outputs: \033[0;34m[INFO]\033[0m ]0;pwned
# Let's verify that exactly:
expected=$'\033[0;34m[INFO]\033[0m ]0;pwned'

if [[ "$output" == "$expected" ]]; then
    echo "BRANCH: Pass: Escape sequence neutralized (printed as literal string/stripped)"
else
    echo "BRANCH: Fail: Escape sequence evaluated or missing!"
fi
rm temp_log_info.sh
