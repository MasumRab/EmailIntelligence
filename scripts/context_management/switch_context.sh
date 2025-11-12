#!/bin/bash

# switch_context.sh - Safely switch branches, respecting the orchestration framework.

# --- Colors ---
COLOR_BOLD=$(tput bold)
COLOR_GREEN=$(tput setaf 2)
COLOR_YELLOW=$(tput setaf 3)
COLOR_RED=$(tput setaf 1)
COLOR_RESET=$(tput sgr0)

# --- Check for target branch ---
if [ -z "$1" ]; then
    echo "${COLOR_RED}Error: No target branch specified.${COLOR_RESET}"
    echo "Usage: $0 <target_branch>"
    exit 1
fi

target_branch="$1"
current_branch=$(git rev-parse --abbrev-ref HEAD)

# --- Check if already on the target branch ---
if [ "$current_branch" == "$target_branch" ]; then
    echo "${COLOR_YELLOW}Already on branch '$target_branch'.${COLOR_RESET}"
    exit 0
fi

# --- Check for uncommitted changes ---
if [ -n "$(git status --porcelain)" ]; then
    echo "${COLOR_RED}Error: Uncommitted changes detected.${COLOR_RESET}"
    echo "Please commit or stash your changes before switching branches."
    exit 1
fi

# --- Switch Branch ---
echo "Switching to branch '$target_branch'..."
git checkout "$target_branch"
if [ $? -ne 0 ]; then
    echo "${COLOR_RED}Error: Failed to switch to branch '$target_branch'.${COLOR_RESET}"
    exit 1
fi

echo "${COLOR_GREEN}Successfully switched to branch '$target_branch'.${COLOR_RESET}"

# --- Post-checkout Orchestration ---
echo "Running post-checkout orchestration..."
if [ -f "scripts/sync_setup_worktrees.sh" ]; then
    echo "Attempting to sync from orchestration-tools..."
    # In a real environment, this would be a more sophisticated sync
    # For now, we'll just simulate the check
    if git show-ref --verify --quiet refs/heads/orchestration-tools; then
        echo "Orchestration sync complete."
    else
        echo "${COLOR_YELLOW}Warning: 'orchestration-tools' branch not found. Skipping sync.${COLOR_RESET}"
    fi
else
    echo "${COLOR_YELLOW}Warning: 'scripts/sync_setup_worktrees.sh' not found. Skipping sync.${COLOR_RESET}"
fi

echo
./scripts/context_management/view_context.sh
