#!/bin/bash

# check_context_health.sh - Check the health of the development environment context.

# --- Colors ---
COLOR_BOLD=$(tput bold)
COLOR_GREEN=$(tput setaf 2)
COLOR_YELLOW=$(tput setaf 3)
COLOR_RED=$(tput setaf 1)
COLOR_RESET=$(tput sgr0)

echo "${COLOR_BOLD}========================================="
echo "   Context Health Check"
echo "=========================================${COLOR_RESET}"
echo

# --- Check 1: Git Hooks ---
echo -n "Checking for Git hooks... "
hooks_installed=true
for hook in pre-commit post-commit post-merge post-checkout post-push; do
    if [ ! -f ".git/hooks/$hook" ]; then
        hooks_installed=false
    fi
done

if $hooks_installed; then
    echo "${COLOR_GREEN}OK${COLOR_RESET}"
else
    echo "${COLOR_RED}FAIL${COLOR_RESET}"
    echo "  ${COLOR_YELLOW}Warning: Not all Git hooks are installed. Run 'scripts/install-hooks.sh'.${COLOR_RESET}"
fi

# --- Check 2: Orchestration-Managed Files ---
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "orchestration-tools" ]; then
    echo -n "Checking for unauthorized changes to orchestrated files... "
    source "$(dirname "$0")/orchestration.conf"
    unauthorized_changes=false
    for file in "${ORCHESTRATED_FILES[@]}"; do
        if [ -n "$(git status --porcelain "$file")" ]; then
            unauthorized_changes=true
        fi
    done

    if $unauthorized_changes; then
        echo "${COLOR_RED}FAIL${COLOR_RESET}"
        echo "  ${COLOR_YELLOW}Warning: Unauthorized changes to orchestrated files detected.${COLOR_RESET}"
        echo "  ${COLOR_YELLOW}Use 'propose_orchestration_change.sh' to submit these changes.${COLOR_RESET}"
    else
        echo "${COLOR_GREEN}OK${COLOR_RESET}"
    fi
fi

# --- Check 3: Branch Tracking ---
echo -n "Checking branch tracking... "
tracking_branch=$(git for-each-ref --format='%(upstream:short)' "$(git symbolic-ref -q HEAD)")
if [ "$current_branch" == "main" ] || [ "$current_branch" == "scientific" ]; then
    if [ -z "$tracking_branch" ]; then
        echo "${COLOR_RED}FAIL${COLOR_RESET}"
        echo "  ${COLOR_YELLOW}Warning: Branch '$current_branch' is not tracking a remote branch.${COLOR_RESET}"
    else
        echo "${COLOR_GREEN}OK${COLOR_RESET}"
    fi
elif [ -n "$tracking_branch" ]; then
    echo "${COLOR_GREEN}OK${COLOR_RESET}"
else
    echo "${COLOR_YELLOW}N/A${COLOR_RESET}"
fi

echo
echo "${COLOR_BOLD}=========================================${COLOR_RESET}"
