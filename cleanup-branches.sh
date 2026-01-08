#!/bin/bash
# cleanup-branches.sh - Automated script for cleaning up stale Git branches

# Ensure script exits on error and uses strict variable handling
set -euo pipefail

# Function to display help information
show_help() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:
    -h, --help      Show this help message
    -d, --dry-run   Show what would be deleted without actually deleting
    -f, --force     Force delete branches (use with caution)"
    echo ""
    echo "This script identifies and cleans up local branches that no longer exist on the remote."
}

# Initialize variables
DRY_RUN=false
FORCE_DELETE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE_DELETE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

echo "=== Git Branch Cleanup Script ==="
echo ""

# Check if we're in a Git repository
test -d .git || {
    echo "Error: Not in a Git repository"
    exit 1
}

# Get current branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Fetch latest remote state
echo "Fetching latest remote state..."
git fetch --prune

echo ""
echo "Checking for stale branches..."
echo ""

# Find stale branches (local branches where remote is gone)
STALE_BRANCHES=$(git branch -vv | grep ': gone]' | awk '{print $1}' || true)

if [ -z "$STALE_BRANCHES" ]; then
    echo "✓ No stale branches found."
    exit 0
fi

echo "Found stale branches:"
echo "$STALE_BRANCHES"
echo ""

# Count branches
BRANCH_COUNT=$(echo "$STALE_BRANCHES" | wc -w)
echo "Total stale branches: $BRANCH_COUNT"
echo ""

# Detailed analysis of each stale branch
echo "=== Branch Analysis ==="
for branch in $STALE_BRANCHES; do
    echo ""
    echo "Branch: $branch"
    
    # Check if branch is currently checked out
    if [ "$branch" = "$CURRENT_BRANCH" ]; then
        echo "  Status: Currently checked out - SKIPPING"
        continue
    fi
    
    # Checkout branch to check status
    if git checkout -q "$branch" 2>/dev/null; then
        # Check for uncommitted changes
        if ! git diff --quiet 2>/dev/null; then
            echo "  Status: Has uncommitted changes"
        elif ! git diff --cached --quiet 2>/dev/null; then
            echo "  Status: Has staged changes"
        else
            echo "  Status: Clean working directory"
        fi
        
        # Check if merged to main
        if git branch --merged main 2>/dev/null | grep -q "^\*\?\s*$branch"; then
            echo "  Merge Status: Merged to main"
        else
            echo "  Merge Status: Not merged to main"
        fi
        
        # Get last commit info
        LAST_COMMIT=$(git log -1 --pretty=format:"%h - %s (%ar)" 2>/dev/null || echo "unknown")
        echo "  Last Commit: $LAST_COMMIT"
        
        # Return to original branch
        git checkout -q "$CURRENT_BRANCH" 2>/dev/null
    else
        echo "  Status: Could not checkout (may be corrupted)"
    fi
done

echo ""
echo "=== Cleanup Summary ==="
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "DRY RUN - No branches will be deleted"
    echo "The following branches would be deleted:"
    for branch in $STALE_BRANCHES; do
        if [ "$branch" != "$CURRENT_BRANCH" ]; then
            echo "  - $branch"
        fi
    done
    exit 0
fi

# Confirmation prompt
read -p "Delete these $BRANCH_COUNT stale branches? [y/N] " -n 1 -r
echo
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Proceeding with deletion..."
    echo ""
    
    DELETED_COUNT=0
    SKIPPED_COUNT=0
    
    for branch in $STALE_BRANCHES; do
        # Skip current branch
        if [ "$branch" = "$CURRENT_BRANCH" ]; then
            echo "Skipping current branch: $branch"
            ((SKIPPED_COUNT++))
            continue
        fi
        
        # Determine delete command based on force flag
        DELETE_CMD="git branch -d"
        if [ "$FORCE_DELETE" = true ]; then
            DELETE_CMD="git branch -D"
        fi
        
        echo "Deleting branch: $branch"
        if $DELETE_CMD "$branch"; then
            echo "  ✓ Successfully deleted"
            ((DELETED_COUNT++))
        else
            echo "  ✗ Failed to delete (may need force delete)"
            if [ "$FORCE_DELETE" = false ]; then
                echo "  Try using --force option"
            fi
        fi
    done
    
    echo ""
    echo "=== Cleanup Results ==="
    echo "Successfully deleted: $DELETED_COUNT branches"
    echo "Skipped: $SKIPPED_COUNT branches"
    echo "Total processed: $BRANCH_COUNT branches"
    
    # Final fetch to clean up
    echo ""
    echo "Running final cleanup..."
    git fetch --prune
    git remote prune origin
    
    echo ""
    echo "✓ Branch cleanup complete!"
else
    echo "Cleanup cancelled by user."
    exit 0
fi