#!/bin/bash

# Script to show detailed information about each stash
# This helps understand what changes are in each stash before applying them

echo "=== Detailed Stash Information ==="
echo

# Get the number of stashes
stash_count=$(git stash list | wc -l)

if [ "$stash_count" -eq 0 ]; then
    echo "No stashes found."
    exit 0
fi

echo "Found $stash_count stashes:"
echo

# Process each stash
for i in $(seq 0 $((stash_count - 1))); do
    echo "=== Stash $((i + 1))/$stash_count ==="
    
    # Show stash reference and message
    stash_ref=$(git stash list | sed -n "$((i+1))p" | cut -d: -f1)
    stash_message=$(git stash list | sed -n "$((i+1))p" | cut -d: -f2-)
    
    echo "Reference: $stash_ref"
    echo "Message: $stash_message"
    
    # Extract branch name
    if [[ $stash_message =~ "WIP on "([^[:space:]]+)":" ]] || [[ $stash_message =~ "On "([^[:space:]]+)":" ]]; then
        branch_name="${BASH_REMATCH[1]}"
        echo "Target branch: $branch_name"
    else
        echo "Target branch: Could not determine"
    fi
    
    # Show files changed in the stash
    echo "Files changed:"
    git stash show "$stash_ref" --name-only | head -10 || echo "  Could not determine changed files"
    
    changed_files_count=$(git stash show "$stash_ref" --name-only 2>/dev/null | wc -l)
    if [ "$changed_files_count" -gt 10 ]; then
        echo "  ... and $((changed_files_count - 10)) more files"
    fi
    
    echo
    
    # Show a summary of changes (first few lines)
    echo "Changes summary (first 15 lines):"
    git stash show -p "$stash_ref" | head -15 | sed 's/^/  /' || echo "  Could not show changes"
    
    if [ $i -lt $((stash_count - 1)) ]; then
        echo "---"
        echo
    fi
done

echo "=== End of Stash Information ==="