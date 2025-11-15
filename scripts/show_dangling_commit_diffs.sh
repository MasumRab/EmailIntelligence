#!/bin/bash

# This script shows the diff of dangling commits.

# Get the list of dangling commits
dangling_commits=$(grep "dangling commit" /home/masum/.gemini/tmp/ecf9a8bc2dfe40868144eda095201fa9bea57f16fec6afc9397615d58ba49520/fsck_lost_found.txt | awk '{print $3}')

if [ -z "$dangling_commits" ]; then
    echo "No dangling commits found."
    exit 0
fi

echo "Showing diffs for dangling commits..."

for commit_sha in $dangling_commits; do
    echo "========================================================================"
    echo "Diff for dangling commit: $commit_sha"
    echo "========================================================================"
    git show "$commit_sha"
    echo ""
done

echo "Search complete."
