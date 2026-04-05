#!/bin/bash

# Script to restore Git hooks that were previously disabled
# This restores the original hooks from the backup directory

set -e

echo "Restoring Git hooks..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a Git repository"
    exit 1
fi

# Define directories
HOOKS_DIR=".git/hooks"
BACKUP_DIR=".git/hooks_backup"

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "No backup found. Hooks may not have been disabled previously."
    exit 1
fi

# Remove dummy hooks
echo "Removing dummy hooks..."
HOOK_NAMES=("pre-commit" "post-commit" "post-merge" "post-checkout" "post-push")

for hook_name in "${HOOK_NAMES[@]}"; do
    hook_path="$HOOKS_DIR/$hook_name"
    if [ -f "$hook_path" ]; then
        # Check if it's a dummy hook by looking for the comment
        if grep -q "Dummy hook - does nothing" "$hook_path" 2>/dev/null; then
            echo "  Removing dummy $hook_name hook"
            rm "$hook_path"
        fi
    fi
done

# Restore original hooks from backup
echo "Restoring original hooks from backup..."
for backup_hook in "$BACKUP_DIR"/*; do
    if [ -f "$backup_hook" ]; then
        hook_name=$(basename "$backup_hook")
        echo "  Restoring $hook_name"
        mv "$backup_hook" "$HOOKS_DIR/$hook_name"
    fi
done

# Remove backup directory if empty
if [ -d "$BACKUP_DIR" ] && [ ! "$(ls -A $BACKUP_DIR)" ]; then
    rmdir "$BACKUP_DIR"
fi

echo "Git hooks have been restored successfully!"