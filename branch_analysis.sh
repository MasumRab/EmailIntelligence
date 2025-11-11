#!/bin/bash

# Script to collect branch metadata

echo "Branch Analysis Data"
echo "===================="

for branch in $(git branch --format='%(refname:short)'); do
  echo "Branch: $branch"

  # Last commit date
  last_date=$(git log -1 --format="%ci" $branch 2>/dev/null)
  echo "  Last commit date: $last_date"

  # First commit date (relative to main)
  first_date=$(git log --reverse --format="%ci" $branch | head -1)
  echo "  First commit date: $first_date"

  # Commit count
  commit_count=$(git rev-list --count $branch 2>/dev/null)
  echo "  Commit count: $commit_count"

  # Main changed files (diff with main, top 5)
  echo "  Main changed files:"
  git diff --name-only main..$branch 2>/dev/null | head -5 | sed 's/^/    /'
  echo ""
done