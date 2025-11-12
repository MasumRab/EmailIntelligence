#!/bin/bash

# new_feature_branch.sh - Create a new feature branch from a specified base.

# --- Colors ---
COLOR_BOLD=$(tput bold)
COLOR_GREEN=$(tput setaf 2)
COLOR_YELLOW=$(tput setaf 3)
COLOR_RED=$(tput setaf 1)
COLOR_RESET=$(tput sgr0)

# --- Usage ---
if [ -z "$1" ]; then
    echo "${COLOR_RED}Error: No branch name specified.${COLOR_RESET}"
    echo "Usage: $0 <new_branch_name> [base_branch]"
    echo "  base_branch defaults to 'main'."
    exit 1
fi

new_branch_name="$1"
base_branch="${2:-main}"

echo "${COLOR_BOLD}========================================="
echo "   Create New Feature Branch"
echo "=========================================${COLOR_RESET}"
echo

# --- Validate base branch ---
if [ "$base_branch" != "main" ] && [ "$base_branch" != "scientific" ]; then
    echo "${COLOR_RED}Error: Invalid base branch '$base_branch'.${COLOR_RESET}"
    echo "Base branch must be 'main' or 'scientific'."
    exit 1
fi

# --- Check for uncommitted changes ---
if [ -n "$(git status --porcelain)" ]; then
    echo "${COLOR_RED}Error: Uncommitted changes detected.${COLOR_RESET}"
    echo "Please commit or stash your changes before creating a new branch."
    exit 1
fi

# --- Create Branch ---
echo "Creating new branch '$new_branch_name' from '$base_branch'..."
git checkout "$base_branch"
git pull origin "$base_branch" --rebase
git checkout -b "$new_branch_name"

if [ $? -ne 0 ]; then
    echo "${COLOR_RED}Error: Failed to create new branch.${COLOR_RESET}"
    exit 1
fi

echo
echo "${COLOR_GREEN}Successfully created and switched to branch '$new_branch_name'.${COLOR_RESET}"
echo

# --- Display Context ---
"$(dirname "$0")/../context_management/view_context.sh"

echo "${COLOR_BOLD}=========================================${COLOR_RESET}"
