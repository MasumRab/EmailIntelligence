#!/bin/bash

# Install Git hooks from scripts/hooks/ to .git/hooks/
# This ensures all branches have the correct hook versions

set -e

HOOKS_DIR="scripts/hooks"
GIT_HOOKS_DIR=".git/hooks"

echo "Installing Git hooks..."

# Ensure we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    exit 1
fi

# Check if orchestration-tools branch exists
if ! git show-ref --verify --quiet refs/heads/orchestration-tools && ! git show-ref --verify --quiet refs/remotes/origin/orchestration-tools; then
    echo "Error: orchestration-tools branch not found"
    exit 1
fi

# Check if local install-hooks.sh is behind orchestration-tools version
if git ls-tree -r orchestration-tools --name-only 2>/dev/null | grep -q "^scripts/install-hooks.sh$"; then
    if ! git diff --quiet orchestration-tools:"scripts/install-hooks.sh" "scripts/install-hooks.sh" 2>/dev/null; then
        echo "Local install-hooks.sh differs from orchestration-tools version."
        read -p "Update install-hooks.sh from orchestration-tools? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git checkout orchestration-tools -- "scripts/install-hooks.sh" --quiet
            echo "Updated install-hooks.sh from orchestration-tools."
            # Re-run the script with updated version
            exec "$0" "$@"
        fi
    fi
fi

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