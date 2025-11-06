#!/bin/bash

# Manual cleanup script for orchestration-tools branch specific files
# This script removes orchestration-related scripts and hooks when run manually

# Only run if explicitly called
if [ "$1" != "--force" ]; then
    echo "Manual cleanup script for orchestration files"
    echo "Usage: $0 --force"
    echo "This will remove orchestration-specific files from the working directory."
    echo "WARNING: This operation cannot be undone."
    exit 1
fi

echo "Manual orchestration cleanup initiated..."

# Remove disabled scripts folder from git and working directory
if [ -d "scripts/currently_disabled" ]; then
    git rm -r scripts/currently_disabled
    echo "Removed scripts/currently_disabled/ from git and working directory"
fi

# Remove all orchestration-managed hooks to prevent mixup
HOOKS_TO_REMOVE=("pre-commit" "post-commit" "post-merge" "post-checkout" "post-push")
for hook in "${HOOKS_TO_REMOVE[@]}"; do
    if [ -f ".git/hooks/$hook" ]; then
        rm ".git/hooks/$hook"
        echo "Removed .git/hooks/$hook"
    fi
done

echo "Manual cleanup completed."