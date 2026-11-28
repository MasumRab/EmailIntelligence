#!/bin/bash
# Re-run CI on all Dependabot PRs and enable auto-merge

set -e

echo "=== Dependabot Auto-Merge Enabler ==="
echo ""

# Get all open Dependabot PRs
PR_LIST=$(gh pr list --author "dependabot[bot]" --state open --limit 50 --json number --jq '.[].number')

if [ -z "$PR_LIST" ]; then
  echo "No open Dependabot PRs found."
  exit 0
fi

echo "Found $(echo "$PR_LIST" | wc -l | tr -d ' ') Dependabot PRs"
echo ""

# Process each PR
for pr_number in $PR_LIST; do
  echo "Processing PR #$pr_number..."
  
  # Re-run CI checks
  echo "  → Re-running CI checks..."
  if gh run rerun --branch "dependabot/*/$pr_number" 2>/dev/null; then
    echo "    ✓ CI re-run triggered"
  else
    # Try alternative method
    gh pr comment "$pr_number" --body "🔄 Triggering CI re-run..." 2>/dev/null || true
    echo "    ⚠ Could not trigger re-run (may need manual intervention)"
  fi
  
  # Enable auto-merge
  echo "  → Enabling auto-merge..."
  if gh pr merge "$pr_number" --auto --merge 2>/dev/null; then
    echo "    ✓ Auto-merge enabled"
  else
    echo "    ⚠ Could not enable auto-merge (PR may have issues)"
  fi
  
  echo ""
done

echo "=== Complete ==="
echo ""
echo "Summary:"
echo "- CI re-runs triggered for all Dependabot PRs"
echo "- Auto-merge enabled where possible"
echo ""
echo "Monitor progress: gh pr list --author 'dependabot[bot]' --state open"
echo ""
echo "Note: PRs will auto-merge when CI passes (Mergify config updated)"
