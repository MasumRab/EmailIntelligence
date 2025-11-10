#!/bin/bash

# propose_orchestration_change.sh - Streamline the process of proposing a change to an orchestrated file.

# --- Colors ---
COLOR_BOLD=$(tput bold)
COLOR_GREEN=$(tput setaf 2)
COLOR_YELLOW=$(tput setaf 3)
COLOR_RED=$(tput setaf 1)
COLOR_RESET=$(tput sgr0)

# --- Check for file argument ---
if [ -z "$1" ]; then
    echo "${COLOR_RED}Error: No file specified.${COLOR_RESET}"
    echo "Usage: $0 <path_to_orchestrated_file>"
    exit 1
fi

file_to_propose="$1"
current_branch=$(git rev-parse --abbrev-ref HEAD)
user_name=$(git config user.name)
user_name_sanitized=$(echo "$user_name" | tr -cd '[:alnum:]_-')
new_branch_name="proposal/${user_name_sanitized}_$(basename "$file_to_propose")_$(date +%s)"

echo "${COLOR_BOLD}========================================="
echo "   Propose Orchestration Change"
echo "=========================================${COLOR_RESET}"
echo

# --- Check if on orchestration-tools branch ---
if [ "$current_branch" == "orchestration-tools" ]; then
    echo "${COLOR_YELLOW}Already on 'orchestration-tools' branch.${COLOR_RESET}"
    echo "Please commit and push your changes directly."
    exit 0
fi

# --- Check if the file has changes ---
if [ -z "$(git status --porcelain "$file_to_propose")" ]; then
    echo "${COLOR_RED}Error: No changes detected in '$file_to_propose'.${COLOR_RESET}"
    exit 1
fi

# --- Create and switch to new branch ---
echo "Creating new proposal branch: $new_branch_name"
git checkout -b "$new_branch_name" orchestration-tools
if [ $? -ne 0 ]; then
    echo "${COLOR_RED}Error: Failed to create new branch from 'orchestration-tools'.${COLOR_RESET}"
    exit 1
fi

# --- Apply the change ---
echo "Applying changes from '$current_branch'..."
git checkout "$current_branch" -- "$file_to_propose"
if [ $? -ne 0 ]; then
    echo "${COLOR_RED}Error: Failed to apply changes to '$file_to_propose'.${COLOR_RESET}"
    git checkout "$current_branch"
    git branch -D "$new_branch_name"
    exit 1
fi

# --- Commit and Push ---
echo "Committing changes..."
git add "$file_to_propose"
git commit -m "feat(orchestration): Propose change to $(basename "$file_to_propose")" -m "Proposed change from branch '$current_branch' by '$user_name'."

echo
echo "${COLOR_GREEN}Change has been committed to branch '$new_branch_name'.${COLOR_RESET}"
echo "Please push this branch and create a pull request to 'orchestration-tools'."
echo
echo "git push origin $new_branch_name"
echo
echo "${COLOR_BOLD}=========================================${COLOR_RESET}"
