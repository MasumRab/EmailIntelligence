#!/bin/bash

# Script to analyze stashes and provide recommendations on processing order
# This helps prioritize which stashes to handle first based on branch importance

echo "=== Stash Analysis and Processing Recommendations ==="
echo

# Show all stashes with their branches
echo "All Stashes with Target Branches:"
echo "--------------------------------"
git stash list | nl

echo
echo "Stash Processing Recommendations:"
echo "-------------------------------"

# Count stashes by branch
echo "Stashes by branch:"
git stash list | sed 's/:.*//' | sed 's/.*On //; s/.*WIP on //' | sort | uniq -c | sort -nr

echo
echo "Priority Order for Processing:"
echo "1. orchestration-tools (multiple stashes, critical branch)"
echo "2. scientific (ahead of remote, important work)"
echo "3. 002-validate-orchestration-tools (orchestration related)"
echo "4. feature/backend-to-src-migration (migration work)"
echo "5. Other branches in order of appearance"

echo
echo "Important Notes:"
echo "- The orchestration-tools branch has 6 stashes and is 61 commits behind remote"
echo "- The scientific branch has 3 stashes and is 2 commits ahead of remote"
echo "- Many stashes appear to be related to orchestration tools work"
echo "- Consider pulling latest changes before applying stashes to avoid conflicts"