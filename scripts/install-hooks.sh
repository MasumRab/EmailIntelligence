#!/bin/bash

# Install Git hooks from scripts/hooks/ to .git/hooks/

HOOKS_DIR="$(dirname "$0")/hooks"
GIT_HOOKS_DIR=".git/hooks"

echo "Installing Git hooks..."

for hook in "$HOOKS_DIR"/*; do
    if [[ -f "$hook" ]]; then
        hook_name=$(basename "$hook")
        cp "$hook" "$GIT_HOOKS_DIR/$hook_name"
        chmod +x "$GIT_HOOKS_DIR/$hook_name"
        echo "Installed: $hook_name"
    fi
done

echo "Git hooks installed successfully."
echo "Run this script after cloning to enable hooks."
