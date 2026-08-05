#!/bin/bash
# Validate orchestration-tools branch purity
# Exit 0 = clean, 1 = contaminated

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== Validating Orchestration Context ==="

# Check if on orchestration-tools branch
CURRENT_BRANCH=$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "orchestration-tools" ]]; then
  echo "⚠ Warning: Not on orchestration-tools branch (current: $CURRENT_BRANCH)"
fi

ISSUES_FOUND=0

# Critical: Application code should NOT be on orchestration-tools
CRITICAL_PATHS=(
  "src/"
  "client/"
  "plugins/"
  "backend/"
  "modules/"
)

echo ""
echo "Checking for application code contamination..."
for path in "${CRITICAL_PATHS[@]}"; do
  if [[ -d "$REPO_ROOT/$path" ]]; then
    echo "✗ CRITICAL: Found '$path' (should not exist on orchestration-tools)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi
done

# Critical: Agent/context guidance files should NOT be on orchestration-tools
GUIDANCE_FILES=(
  "AGENTS.md"
  "CRUSH.md"
  "GEMINI.md"
  "IFLOW.md"
  "LLXPRT.md"
)

echo ""
echo "Checking for agent guidance contamination..."
for file in "${GUIDANCE_FILES[@]}"; do
  if [[ -f "$REPO_ROOT/$file" ]]; then
    echo "✗ CRITICAL: Found '$file' (should be on main, not orchestration-tools)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  fi
done

# Setup files: Check for recursion in launch.sh
echo ""
echo "Checking setup files for corruption..."
if [[ -f "$REPO_ROOT/setup/launch.sh" ]]; then
  if grep -q '\$SCRIPT_DIR/setup/launch\.sh' "$REPO_ROOT/setup/launch.sh"; then
    echo "✗ CRITICAL: launch.sh has recursive reference (corrupted)"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
  else
    echo "✓ launch.sh looks OK"
  fi
fi

# Check setup/launch.py exists and is valid
if [[ -f "$REPO_ROOT/setup/launch.py" ]]; then
  echo "✓ setup/launch.py exists"
else
  echo "⚠ Warning: setup/launch.py missing"
fi

# Summarize
echo ""
if [[ $ISSUES_FOUND -eq 0 ]]; then
  echo "✓ Context validation PASSED (0 issues)"
  exit 0
else
  echo "✗ Context validation FAILED ($ISSUES_FOUND critical issues)"
  exit 1
fi
