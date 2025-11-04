#!/bin/bash

# Cleanup script for orchestration-tools branch specific files
# This script removes orchestration-related scripts and hooks when not on the orchestration-tools branch

current_branch=$(git branch --show-current)

if [ "$current_branch" != "orchestration-tools" ]; then
    echo "Not on orchestration-tools branch. Orchestration cleanup triggered."

    # Prompt user before making changes
    echo "This will remove orchestration-specific files from the working directory."
    read -p "Proceed with cleanup? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
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

        echo "Cleanup completed."
    else
        echo "Cleanup cancelled."
    fi
else
    echo "On orchestration-tools branch. No cleanup needed."
fi