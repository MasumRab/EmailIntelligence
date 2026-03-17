#!/bin/bash

# This script finds dangling commits that contain changes to source code files.

# Get the list of dangling commits
dangling_commits=$(grep "dangling commit" /home/masum/.gemini/tmp/ecf9a8bc2dfe40868144eda095201fa9bea57f16fec6afc9397615d58ba49520/fsck_lost_found.txt | awk '{print $3}')

if [ -z "$dangling_commits" ]; then
    echo "No dangling commits found."
    exit 0
fi

echo "Searching for source code changes in dangling commits..."

for commit_sha in $dangling_commits; do
    # Check if the commit contains changes in src/, backend/, or client/
    if git show --name-only --format="" "$commit_sha" | grep -qE "^(src/|backend/|client/)"; then
        echo "========================================================================"
        echo "Found potential source code changes in dangling commit: $commit_sha"
        echo "Commit message:"
        git show --no-patch --format=%B "$commit_sha"
        echo "------------------------------------------------------------------------"
        echo "Files changed:"
        git show --name-only --format="" "$commit_sha"
        echo "========================================================================"
        echo ""
    fi
done

echo "Search complete."
