#!/bin/bash

# This script finds files in dangling commits.

# Get the list of dangling commits
dangling_commits=$(grep "dangling commit" /home/masum/.gemini/tmp/ecf9a8bc2dfe40868144eda095201fa9bea57f16fec6afc9397615d58ba49520/fsck_lost_found.txt | awk '{print $3}')

if [ -z "$dangling_commits" ]; then
    echo "No dangling commits found."
    exit 0
fi

echo "Searching for files in dangling commits..."

for commit_sha in $dangling_commits; do
    echo "========================================================================"
    echo "Files in dangling commit: $commit_sha"
    echo "Commit message:"
    git show --no-patch --format=%B "$commit_sha"
    echo "------------------------------------------------------------------------"
    echo "Files:"
    git ls-tree -r --name-only "$commit_sha"
    echo "========================================================================"
    echo ""
done

echo "Search complete."
