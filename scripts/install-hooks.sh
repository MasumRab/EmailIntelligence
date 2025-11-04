#!/bin/bash

# Install Git hooks from scripts/hooks/ to .git/hooks/
# This ensures all branches have the correct hook versions

set -e

HOOKS_DIR="scripts/hooks"
GIT_HOOKS_DIR=".git/hooks"

echo "Installing Git hooks..."

# Create .git/hooks directory if it doesn't exist
mkdir -p "$GIT_HOOKS_DIR"

# List of hooks to install
HOOKS=(
    "pre-commit"
    "post-commit"
    "post-merge"
    "post-checkout"
    "post-push"
)

# Install each hook
for hook in "${HOOKS[@]}"; do
    if [[ -f "$HOOKS_DIR/$hook" ]]; then
        echo "Installing $hook hook..."
        cp "$HOOKS_DIR/$hook" "$GIT_HOOKS_DIR/$hook"
        chmod +x "$GIT_HOOKS_DIR/$hook"
    else
        echo "Warning: $hook hook not found in $HOOKS_DIR/"
    fi
done

echo "Git hooks installed successfully."
echo "Current hooks in .git/hooks/:"
ls -la "$GIT_HOOKS_DIR" | grep -E '(pre-commit|post-commit|post-merge|post-checkout|post-push)$' || echo "No hooks found"