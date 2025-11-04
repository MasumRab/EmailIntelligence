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

# Install each hook by pulling from orchestration-tools branch
for hook in "${HOOKS[@]}"; do
    hook_path="scripts/hooks/$hook"
    if git ls-tree -r orchestration-tools --name-only 2>/dev/null | grep -q "^$hook_path$"; then
        echo "Installing $hook hook from orchestration-tools..."
        git checkout orchestration-tools -- "$hook_path" --quiet
        cp "$hook_path" "$GIT_HOOKS_DIR/$hook"
        chmod +x "$GIT_HOOKS_DIR/$hook"
    else
        echo "Warning: $hook not found in orchestration-tools branch"
    fi
done

echo "Git hooks installed successfully from orchestration-tools branch."
echo "Current hooks in .git/hooks/:"
ls -la "$GIT_HOOKS_DIR" | grep -E '(pre-commit|post-commit|post-merge|post-checkout|post-push)$' || echo "No hooks found"