#!/bin/bash

# Cleanup script for orchestration-tools branch specific files
# This script removes orchestration-related scripts and hooks when not on the orchestration-tools branch

current_branch=$(git branch --show-current)

if [ "$current_branch" != "orchestration-tools" ]; then
    echo "Not on orchestration-tools branch. Cleaning up orchestration-specific files..."

    # Remove disabled scripts folder from git and working directory
    if [ -d "scripts/currently_disabled" ]; then
        git rm -r scripts/currently_disabled
        echo "Removed scripts/currently_disabled/ from git and working directory"
    fi

    # Remove orchestration-specific hooks
    if [ -f ".git/hooks/post-commit-setup-sync" ]; then
        rm .git/hooks/post-commit-setup-sync
        echo "Removed .git/hooks/post-commit-setup-sync"
    fi

    echo "Cleanup completed."
else
    echo "On orchestration-tools branch. No cleanup needed."
fi