#!/bin/bash
# modules/branch.sh - Branch module (~200 lines)

# Import dependencies if needed
# Define constants for this module
readonly BRANCH_TYPES=("orchestration-tools" "taskmaster" "main" "scientific")

# Function to identify branch type
identify_branch_type() {
    local branch_name="$1"
    
    if [[ "$branch_name" == orchestration-tools* ]]; then
        echo "orchestration-tools"
    elif [[ "$branch_name" == taskmaster* ]]; then
        echo "taskmaster"
    elif [[ "$branch_name" == "main" ]] || [[ "$branch_name" == scientific* ]]; then
        echo "main-scientific"
    else
        echo "generic"
    fi
}

# Function to validate branch safety
validate_branch_safety() {
    local branch_name="$1"
    
    # Check if branch is a taskmaster branch (should not be modified by distribution)
    if [[ "$branch_name" == taskmaster* ]]; then
        echo "ERROR: Cannot modify taskmaster branches directly (worktree isolation required)"
        return 1
    fi
    
    # Check if branch exists
    if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo "ERROR: Branch $branch_name does not exist locally"
        return 1
    fi
    
    # Check if branch is up to date with remote (optional safety check)
    local remote_branch="origin/$branch_name"
    if git show-ref --verify --quiet "refs/remotes/$remote_branch"; then
        local local_hash=$(git rev-parse "$branch_name")
        local remote_hash=$(git rev-parse "$remote_branch")
        
        if [[ "$local_hash" != "$remote_hash" ]]; then
            echo "WARNING: Branch $branch_name is not up to date with remote"
        fi
    fi
    
    echo "Branch $branch_name is safe for operations"
    return 0
}

# Function to check if it's an orchestration branch
is_orchestration_branch() {
    local branch_name="$1"
    
    if [[ "$branch_name" == orchestration-tools* ]]; then
        return 0  # Yes, it's an orchestration branch
    else
        return 1  # No, it's not an orchestration branch
    fi
}

# Function to check if it's a taskmaster branch
is_taskmaster_branch() {
    local branch_name="$1"
    
    if [[ "$branch_name" == taskmaster* ]]; then
        return 0  # Yes, it's a taskmaster branch
        else
        return 1  # No, it's not a taskmaster branch
    fi
}

# Function to check if it's a valid target branch for distribution
is_valid_target_branch() {
    local branch_name="$1"
    
    # Taskmaster branches are not valid targets (due to worktree isolation)
    if is_taskmaster_branch "$branch_name"; then
        echo "INFO: Skipping taskmaster branch $branch_name (worktree isolation required)"
        return 1
    fi
    
    # Orchestration-tools branches are valid targets
    if is_orchestration_branch "$branch_name"; then
        return 0
    fi
    
    # Other branches are generally not valid targets for orchestration distribution
    echo "INFO: Skipping non-orchestration branch $branch_name"
    return 1
}

# Function to get all orchestration branches
get_orchestration_branches() {
    git branch -r | grep "origin/orchestration-tools-" | sed 's/origin\///' | xargs
}

# Function to get current branch
get_current_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
}

# Function to switch to a branch safely
switch_to_branch_safely() {
    local target_branch="$1"
    
    # Check if we have uncommitted changes that might be lost
    if ! git diff-index --quiet HEAD --; then
        echo "WARNING: You have uncommitted changes that might be lost when switching branches"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Branch switch cancelled by user"
            return 1
        fi
    fi
    
    # Switch to the target branch
    if git checkout "$target_branch" 2>/dev/null; then
        echo "Successfully switched to branch: $target_branch"
        return 0
    else
        echo "ERROR: Failed to switch to branch: $target_branch"
        return 1
    fi
}

# Function to validate branch before distribution
validate_branch_before_distribution() {
    local branch_name="$1"
    
    # Validate branch safety
    if ! validate_branch_safety "$branch_name"; then
        return 1
    fi
    
    # Check if it's a valid target for distribution
    if ! is_valid_target_branch "$branch_name"; then
        return 1
    fi
    
    # Additional validation based on branch type
    local branch_type=$(identify_branch_type "$branch_name")
    case "$branch_type" in
        "orchestration-tools")
            # Additional checks for orchestration branches
            echo "Performing orchestration branch validation for: $branch_name"
            ;;
        "taskmaster")
            # Taskmaster branches should not reach this point due to earlier check
            echo "ERROR: Attempting to validate taskmaster branch for distribution"
            return 1
            ;;
        *)
            # Generic validation for other branch types
            echo "Performing generic validation for: $branch_name"
            ;;
    esac
    
    return 0
}

# Function to get branch commit hash
get_branch_commit_hash() {
    local branch_name="$1"
    
    git rev-parse "$branch_name" 2>/dev/null || echo "unknown"
}

# Function to compare two branches
compare_branches() {
    local branch1="$1"
    local branch2="$2"
    
    local hash1=$(get_branch_commit_hash "$branch1")
    local hash2=$(get_branch_commit_hash "$branch2")
    
    if [[ "$hash1" == "$hash2" ]]; then
        echo "Branches $branch1 and $branch2 have the same commit hash: $hash1"
        return 0
    else
        local common_ancestor=$(git merge-base "$branch1" "$branch2")
        if [[ "$common_ancestor" == "$hash1" ]]; then
            echo "Branch $branch1 is an ancestor of $branch2"
            return 1
        elif [[ "$common_ancestor" == "$hash2" ]]; then
            echo "Branch $branch2 is an ancestor of $branch1"
            return 1
        else
            echo "Branches $branch1 and $branch2 have diverged from common ancestor $common_ancestor"
            return 1
        fi
    fi
}

# Function to check if branch is up to date with remote
is_branch_up_to_date_with_remote() {
    local branch_name="$1"
    local remote_name="${2:-origin}"
    
    # Fetch latest from remote
    git fetch "$remote_name" "$branch_name" 2>/dev/null || {
        echo "ERROR: Could not fetch from $remote_name/$branch_name"
        return 1
    }
    
    # Get local and remote hashes
    local local_hash=$(git rev-parse "$branch_name")
    local remote_hash=$(git rev-parse "$remote_name/$branch_name" 2>/dev/null)
    
    if [[ -z "$remote_hash" ]]; then
        echo "INFO: Remote branch $remote_name/$branch_name does not exist"
        return 1
    fi
    
    if [[ "$local_hash" == "$remote_hash" ]]; then
        echo "Branch $branch_name is up to date with $remote_name/$branch_name"
        return 0
    else
        local ahead_count=$(git rev-list --count "$remote_hash".."$local_hash")
        local behind_count=$(git rev-list --count "$local_hash".."$remote_hash")
        
        echo "Branch $branch_name is ahead by $ahead_count commits and behind by $behind_count commits compared to $remote_name/$branch_name"
        return 1
    fi
}

# Function to create a backup of current branch state
backup_branch_state() {
    local branch_name="$1"
    local backup_name="${branch_name}_backup_$(date +%Y%m%d_%H%M%S)"
    
    # Create a lightweight tag as a backup
    if git tag "$backup_name" "$branch_name" 2>/dev/null; then
        echo "Backup created: $backup_name for branch $branch_name"
        return 0
    else
        echo "ERROR: Failed to create backup for branch $branch_name"
        return 1
    fi
}

# Function to restore from backup
restore_from_backup() {
    local backup_name="$1"
    local target_branch="$2"
    
    if git show-ref --verify --quiet "refs/tags/$backup_name"; then
        if git checkout -b "$target_branch" "$backup_name" 2>/dev/null; then
            echo "Restored branch $target_branch from backup $backup_name"
            return 0
        else
            echo "ERROR: Failed to restore from backup $backup_name to branch $target_branch"
            return 1
        fi
    else
        echo "ERROR: Backup $backup_name does not exist"
        return 1
    fi
}

# Function to clean up old backups
cleanup_old_backups() {
    local days_to_keep="${1:-7}"
    local branch_prefix="${2:-}"
    
    # Find and delete backup tags older than specified days
    git tag -l | grep -E "_backup_[0-9]{8}_[0-9]{6}$" | while read -r tag; do
        # Skip if branch prefix is specified and tag doesn't match
        if [[ -n "$branch_prefix" ]] && [[ ! "$tag" =~ ^${branch_prefix}_backup_ ]]; then
            continue
        fi
        
        # Get taggerdate to check age
        local tag_date=$(git tag -l --format='%(taggerdate:unix)' "$tag" | head -1)
        local current_date=$(date +%s)
        local age_days=$(( (current_date - tag_date) / 86400 ))
        
        if [[ $age_days -gt $days_to_keep ]]; then
            git tag -d "$tag" 2>/dev/null && echo "Deleted old backup: $tag"
        fi
    done
}

# Export functions that should be available to other modules
export -f identify_branch_type
export -f validate_branch_safety
export -f is_orchestration_branch
export -f is_taskmaster_branch
export -f is_valid_target_branch
export -f get_orchestration_branches
export -f get_current_branch
export -f switch_to_branch_safely
export -f validate_branch_before_distribution
export -f get_branch_commit_hash
export -f compare_branches
export -f is_branch_up_to_date_with_remote
export -f backup_branch_state
export -f restore_from_backup
export -f cleanup_old_backups