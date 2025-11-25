#!/bin/bash

# Cleanup script for orchestration-tools branch specific files
# This script removes orchestration-related scripts and hooks when not on the orchestration-tools branch

current_branch=$(git branch --show-current)

# Check for uncommitted files that might be lost
UNCOMMITTED_FILES=$(git status --porcelain --untracked-files=all 2>/dev/null | grep -v "^scripts/" | grep -v "^setup/" | grep -v "^\..*taskmaster/" | wc -l)
if [[ $UNCOMMITTED_FILES -gt 0 ]]; then
    echo "⚠️  WARNING: There are $UNCOMMITTED_FILES uncommitted files that may be affected:"
    git status --porcelain --untracked-files=all 2>/dev/null | grep -v "^scripts/" | grep -v "^setup/" | grep -v "^\..*taskmaster/" | head -10
    if [[ $UNCOMMITTED_FILES -gt 10 ]]; then
        echo "  ... and $((UNCOMMITTED_FILES - 10)) more files"
    fi
    echo ""
fi

if [[ "$current_branch" != *"orchestration-tools"* ]]; then
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
        # But preserve some core scripts that might be needed for other workflows
        HOOKS_TO_REMOVE=("pre-commit" "post-commit" "post-merge" "post-checkout" "post-push")
        for hook in "${HOOKS_TO_REMOVE[@]}"; do
            if [ -f ".git/hooks/$hook" ]; then
                rm ".git/hooks/$hook"
                echo "Removed .git/hooks/$hook"
            fi
        done

        # Preserve critical orchestration scripts that might be needed for other branches
        # Do NOT remove: scripts/install-hooks.sh, scripts/disable-hooks.sh, scripts/enable-hooks.sh
        # These might be needed for other workflows

        echo "Cleanup completed."
        echo "Preserved critical orchestration scripts in scripts/ directory"
        echo "Preserved setup/ directory with configuration files"
        echo "Preserved .taskmaster/ worktree (git handles isolation)"
    else
        echo "Cleanup cancelled."
    fi
else
    echo "On orchestration-tools branch. No cleanup needed."
    echo "All orchestration files preserved on orchestration-tools branch."
fi