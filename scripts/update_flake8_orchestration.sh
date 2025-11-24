#!/bin/bash
# Update only .flake8 file in orchestration-tools branch
# This script safely updates just the .flake8 file without affecting other files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "=" | head -c 70 && echo ""
echo "Updating .flake8 in orchestration-tools branch"
echo "=" | head -c 70 && echo ""
echo ""

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"

# Stash any uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "Stashing uncommitted changes..."
    git stash push -m "Stash before updating .flake8 in orchestration-tools"
    STASHED=true
else
    STASHED=false
fi

# Switch to orchestration-tools branch
echo "Switching to orchestration-tools branch..."
git checkout orchestration-tools

# Pull latest changes
echo "Pulling latest orchestration-tools changes..."
git pull origin orchestration-tools || echo "Note: Could not pull (may be up to date)"

# Checkout .flake8 from taskmaster branch
echo "Updating .flake8 from taskmaster branch..."
git checkout taskmaster -- .flake8

# Show what changed
echo ""
echo "Changes to .flake8:"
git diff HEAD -- .flake8 || echo "No changes (file already matches)"

# Ask for confirmation (or use --yes flag to skip)
if [ "$1" != "--yes" ]; then
    echo ""
    read -p "Commit and push these changes? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted. Restoring original .flake8..."
        git checkout HEAD -- .flake8
        git checkout "$CURRENT_BRANCH"
        if [ "$STASHED" = true ]; then
            git stash pop
        fi
        exit 1
    fi
fi

# Commit the change
echo "Committing .flake8 update..."
git add .flake8
git commit -m "Update .flake8 from taskmaster branch

- Sync .flake8 configuration from taskmaster branch
- Only .flake8 file updated, no other changes"

# Push to remote
echo "Pushing to origin/orchestration-tools..."
git push origin orchestration-tools

# Switch back to original branch
echo "Switching back to $CURRENT_BRANCH..."
git checkout "$CURRENT_BRANCH"

# Restore stashed changes if any
if [ "$STASHED" = true ]; then
    echo "Restoring stashed changes..."
    git stash pop || echo "Note: Stash restore had conflicts (manual resolution needed)"
fi

echo ""
echo "✅ .flake8 successfully updated in orchestration-tools branch"
echo "=" | head -c 70 && echo ""
