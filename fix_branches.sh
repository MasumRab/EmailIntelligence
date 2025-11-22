#!/bin/bash

# List of branches that need the fix
branches=(
    "docs-cleanup"
    "docs/comprehensive-documentation"
    "feature-dashboard-stats-endpoint"
    "feature/backlog-ac-updates"
    "feature/work-in-progress-extensions"
    "scientific-consolidated"
    "scientific-minimal-rebased"
)

for branch in "${branches[@]}"; do
    echo "Processing branch: $branch"
    
    # Checkout the branch
    git checkout "$branch"
    
    # Merge the fix branch
    git merge fix-gitignore-version-files --no-edit
    
    # Push the changes
    git push origin "$branch"
    
    echo "Completed branch: $branch"
    echo "------------------------"
done

echo "All branches processed!"
