#!/bin/bash
# Git utility functions for orchestration scripts

# Get current branch name
get_current_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null
}

# Check if file exists in branch
file_exists_in_branch() {
    local file_path=$1
    local branch=${2:-orchestration-tools}

    git ls-tree -r "$branch" --name-only 2>/dev/null | grep -q "^${file_path}$"
}

# Safely checkout file from branch
checkout_file_from_branch() {
    local file_path=$1
    local branch=${2:-orchestration-tools}

    if file_exists_in_branch "$file_path" "$branch"; then
        if git diff --quiet "$branch":"$file_path" "$file_path" 2>/dev/null; then
            log_debug "File $file_path is already up to date"
            return $ERROR_NONE
        fi

        log_info "Updating $file_path from $branch"
        if git checkout --quiet "$branch" -- "$file_path" 2>/dev/null; then
            log_debug "Successfully updated $file_path"
            return $ERROR_NONE
        else
            log_error "Failed to checkout $file_path from $branch"
            return $ERROR_GIT
        fi
    else
        log_debug "File $file_path not found in $branch branch"
        return $ERROR_FILESYSTEM
    fi
}

# Check if current directory is a git worktree
is_git_worktree() {
    git rev-parse --is-inside-work-tree >/dev/null 2>&1
}

# Get git repository root
get_git_root() {
    git rev-parse --show-toplevel 2>/dev/null
}