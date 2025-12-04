#!/bin/bash

# Git Utility Functions for EmailIntelligence

# Function to check if a branch exists
branch_exists() {
    git show-ref --verify --quiet refs/heads/"$1"
}

# Function to get current branch name
current_branch() {
    git rev-parse --abbrev-ref HEAD
}

# Function to safely checkout a branch
safe_checkout() {
    if branch_exists "$1"; then
        git checkout "$1"
    else
        echo "Error: Branch '$1' does not exist."
        return 1
    fi
}

# Function to sync with remote
sync_remote() {
    local branch=${1:-$(current_branch)}
    echo "Syncing $branch with origin..."
    if ! git fetch origin "$branch"; then
        echo "Error: Failed to fetch origin/$branch" >&2
        return 1
    fi
    git pull origin "$branch"
}

# Function to list conflicts
list_conflicts() {
    git diff --name-only --diff-filter=U
}

# Function to show commit count ahead/behind
branch_status() {
    local upstream=${1:-"origin/$(current_branch)"}
    if ! git rev-parse --verify "$upstream" > /dev/null 2>&1; then
        echo "Error: Upstream '$upstream' does not exist."
        return 1
    fi
    local ahead=$(git rev-list --count HEAD ^"$upstream")
    local behind=$(git rev-list --count "$upstream" ^HEAD)
    echo "Ahead: $ahead, Behind: $behind"
}
