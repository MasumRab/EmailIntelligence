#!/bin/bash
# Regression test for terminal escape sequence injection

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# We must extract the log_info function from test_orchestration.sh
# and source it here to verify it works in place!
cat "$PROJECT_ROOT/scripts/test_orchestration.sh" | sed -n '/^log_info() {/,/^}/p' > temp_log_info.sh
BLUE='\033[0;34m'
NC='\033[0m'
source temp_log_info.sh

var=$'\x1b[31mRedText\x1b[0m'
output=$(log_info "$var")

if [[ "$output" == $'\033[0;34m[INFO]\033[0m RedText' ]]; then
    echo "Pass: Escape sequence neutralized (printed as literal string)"
else
    echo "Fail: Escape sequence evaluated or missing!"
fi
rm temp_log_info.sh
