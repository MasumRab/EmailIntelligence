#!/bin/bash

# force_sync_context.sh - Manually sync essential files from the orchestration-tools branch.

# --- Colors ---
COLOR_BOLD=$(tput bold)
COLOR_GREEN=$(tput setaf 2)
COLOR_YELLOW=$(tput setaf 3)
COLOR_RED=$(tput setaf 1)
COLOR_RESET=$(tput sgr0)

echo "${COLOR_BOLD}========================================="
echo "   Force Sync Context"
echo "=========================================${COLOR_RESET}"
echo

current_branch=$(git rev-parse --abbrev-ref HEAD)

# --- Check if on orchestration-tools branch ---
if [ "$current_branch" == "orchestration-tools" ]; then
    echo "${COLOR_YELLOW}Already on 'orchestration-tools' branch. No sync needed.${COLOR_RESET}"
    exit 0
fi

# --- Check if orchestration-tools branch exists ---
if ! git show-ref --verify --quiet refs/heads/orchestration-tools; then
    echo "${COLOR_RED}Error: 'orchestration-tools' branch not found.${COLOR_RESET}"
    echo "Cannot sync from a non-existent branch."
    exit 1
fi

# --- Files to Sync ---
source "$(dirname "$0")/orchestration.conf"

echo "The following files will be overwritten with the versions from 'orchestration-tools':"
for file in "${ORCHESTRATED_FILES[@]}"; do
    echo "  - $file"
done
echo

read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Sync cancelled."
    exit 1
fi

# --- Sync Files ---
echo "Syncing files..."
for file in "${ORCHESTRATED_FILES[@]}"; do
    git checkout orchestration-tools -- "$file"
    if [ $? -eq 0 ]; then
        echo "  - Synced $file"
    else
        echo "  - ${COLOR_YELLOW}Warning: Could not sync $file.${COLOR_RESET}"
    fi
done

echo
echo "${COLOR_GREEN}Force sync complete.${COLOR_RESET}"
echo "${COLOR_BOLD}=========================================${COLOR_RESET}"
