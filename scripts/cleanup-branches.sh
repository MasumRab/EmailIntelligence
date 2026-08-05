#!/bin/bash
# Comprehensive branch cleanup script for EmailIntelligence repo
# Removes old feature branches, experiment branches, and merges remotes

set -e

echo "🧹 EmailIntelligence Branch Cleanup"
echo "===================================="
echo ""

# Branches to keep (protected)
KEEP_BRANCHES=(
    "main"
    "master"
    "scientific"
    "orchestration-tools"
    "develop"
)

# Count stats
TOTAL_BEFORE=$(git branch -a | grep -v "remotes/" | wc -l)
echo "Total local branches before cleanup: $TOTAL_BEFORE"
echo ""

# Get list of all branches except those we want to keep
BRANCHES_TO_DELETE=$(git branch | grep -v -E "^\s*\*|$(printf '|%s' "${KEEP_BRANCHES[@]}")" | sed 's/^ *//')

# Count branches to delete
DELETE_COUNT=$(echo "$BRANCHES_TO_DELETE" | wc -l)
echo "Branches to delete: $DELETE_COUNT"
echo ""

# Confirm before deletion
echo "⚠️  About to delete the following branches:"
echo "$BRANCHES_TO_DELETE" | head -20
if [ "$DELETE_COUNT" -gt 20 ]; then
    echo "... and $((DELETE_COUNT - 20)) more"
fi
echo ""

read -p "Continue with deletion? (yes/no) " -n 3 -r
echo
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "🗑️  Deleting branches..."

# Delete each branch
DELETED=0
FAILED=0

echo "$BRANCHES_TO_DELETE" | while read branch; do
    if [ -n "$branch" ]; then
        if git branch -D "$branch" 2>/dev/null; then
            ((DELETED++))
            echo "✓ Deleted: $branch"
        else
            ((FAILED++))
            echo "✗ Failed to delete: $branch"
        fi
    fi
done

echo ""

# Delete remote tracking branches for deleted branches
echo "🔄 Cleaning up remote tracking branches..."
git remote prune origin --dry-run 2>/dev/null || true

read -p "Prune remote tracking branches? (yes/no) " -n 3 -r
echo
if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    git remote prune origin
    echo "✓ Remote tracking branches pruned"
fi

# Force fetch to clean up stale references
echo ""
echo "🔗 Syncing with remote..."
git fetch --all --prune --prune-tags

# Final count
TOTAL_AFTER=$(git branch | wc -l)
echo ""
echo "===================================="
echo "✅ Cleanup Complete"
echo "===================================="
echo "Branches before: $TOTAL_BEFORE"
echo "Branches after: $TOTAL_AFTER"
echo "Branches deleted: $((TOTAL_BEFORE - TOTAL_AFTER))"
echo ""
echo "Remaining branches:"
git branch | grep -v "^[[:space:]]*$" | sort
