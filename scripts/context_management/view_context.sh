#!/bin/bash

# view_context.sh - Display the current development context.

# --- Colors ---
COLOR_BOLD=$(tput bold)
COLOR_GREEN=$(tput setaf 2)
COLOR_YELLOW=$(tput setaf 3)
COLOR_BLUE=$(tput setaf 4)
COLOR_RESET=$(tput sgr0)

# --- Get Current Branch ---
current_branch=$(git rev-parse --abbrev-ref HEAD)

# --- Check Orchestration Status ---
orchestration_status="<unknown>"
if [ "$current_branch" == "orchestration-tools" ]; then
    orchestration_status="${COLOR_GREEN}ACTIVE (Source of Truth)${COLOR_RESET}"
elif git show-ref --verify --quiet refs/heads/orchestration-tools; then
    orchestration_status="${COLOR_YELLOW}INACTIVE (Managed Branch)${COLOR_RESET}"
else
    orchestration_status="${COLOR_YELLOW}INACTIVE (Orchestration branch not found)${COLOR_RESET}"
fi

# --- Check for Uncommitted Changes ---
git_status=$(git status --porcelain)

# --- Display Context ---
echo "${COLOR_BOLD}========================================="
echo "   Development Context Overview"
echo "=========================================${COLOR_RESET}"
echo
echo "${COLOR_BLUE}Current Branch:${COLOR_RESET} $current_branch"
echo "${COLOR_BLUE}Orchestration Status:${COLOR_RESET} $orchestration_status"
echo
echo "${COLOR_BLUE}Uncommitted Changes:${COLOR_RESET}"
if [ -z "$git_status" ]; then
    echo "  ${COLOR_GREEN}No uncommitted changes.${COLOR_RESET}"
else
    echo "${COLOR_YELLOW}$git_status${COLOR_RESET}"
fi
echo
echo "${COLOR_BOLD}=========================================${COLOR_RESET}"
