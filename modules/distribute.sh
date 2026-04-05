#!/bin/bash
# modules/distribute.sh - Distribution module (~200 lines)

# Import dependencies if needed
# Define constants for this module
readonly DISTRIBUTION_CONFIG_PATH="$PROJECT_ROOT/config/distribution.json"

# Function to distribute setup files only
distribute_setup_files() {
    echo "Distributing setup files..."
    
    # Get source and target branches from configuration
    local source_branch=$(get_source_branch)
    local target_branches=($(get_target_branches))
    
    for target_branch in "${target_branches[@]}"; do
        if is_valid_target_branch "$target_branch"; then
            echo "Distributing setup files to: $target_branch"
            distribute_from_to "$source_branch" "$target_branch" "setup/"
        fi
    done
}

# Function to distribute git hooks only
distribute_hooks() {
    echo "Distributing git hooks..."
    
    local source_branch=$(get_source_branch)
    local target_branches=($(get_target_branches))
    
    for target_branch in "${target_branches[@]}"; do
        if is_valid_target_branch "$target_branch"; then
            echo "Distributing hooks to: $target_branch"
            distribute_from_to "$source_branch" "$target_branch" "scripts/hooks/"
        fi
    done
}

# Function to distribute configuration files only
distribute_configs() {
    echo "Distributing configuration files..."
    
    local source_branch=$(get_source_branch)
    local target_branches=($(get_target_branches))
    
    for target_branch in "${target_branches[@]}"; do
        if is_valid_target_branch "$target_branch"; then
            echo "Distributing configs to: $target_branch"
            distribute_from_to "$source_branch" "$target_branch" ".flake8" ".pylintrc" ".gitignore" "launch.py"
        fi
    done
}

# Function to distribute all orchestration files
distribute_all_files() {
    echo "Distributing all orchestration files..."
    
    # Distribute in order: setup, hooks, configs, scripts
    distribute_setup_files
    distribute_hooks
    distribute_configs
    
    # Also distribute other orchestration scripts
    local source_branch=$(get_source_branch)
    local target_branches=($(get_target_branches))
    
    for target_branch in "${target_branches[@]}"; do
        if is_valid_target_branch "$target_branch"; then
            echo "Distributing scripts to: $target_branch"
            distribute_from_to "$source_branch" "$target_branch" "scripts/lib/"
        fi
    done
}

# Function to synchronize from remote orchestration-tools branch
sync_from_remote() {
    local source_branch="$1"
    echo "Pulling latest from $source_branch..."
    
    git fetch origin "$source_branch" || { echo "ERROR: Could not fetch from $source_branch"; return 1; }

    # Verify this is the latest commit
    local remote_hash=$(git rev-parse "origin/$source_branch")
    local local_hash=$(git rev-parse HEAD)

    if [[ "$remote_hash" != "$local_hash" ]]; then
        echo "INFO: Local branch is not at latest commit"
        echo "Remote: $remote_hash"
        echo "Local:  $local_hash"
        read -p "Update to latest remote commit? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git reset --hard "$remote_hash"
            echo "Updated to latest remote commit"
        else
            echo "WARNING: Using outdated local version for distribution"
        fi
    fi
}

# Helper function to distribute files from source to target branch
distribute_from_to() {
    local source_branch="$1"
    local target_branch="$2"
    shift 2
    
    # Save current branch
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    
    # Switch to target branch
    git checkout "$target_branch" || { echo "ERROR: Could not switch to $target_branch"; return 1; }
    
    # Copy files from source branch
    for item in "$@"; do
        if [[ -e "$item" ]]; then
            # Use git to copy the file from source branch
            git checkout "$source_branch" -- "$item" || { echo "ERROR: Could not copy $item from $source_branch"; }
        fi
    done
    
    # Switch back to original branch
    git checkout "$current_branch" || { echo "ERROR: Could not return to original branch"; return 1; }
    
    echo "Distribution to $target_branch completed"
}

# Function to get source branch from configuration
get_source_branch() {
    # Default to orchestration-tools
    echo "orchestration-tools"
}

# Function to get target branches from configuration
get_target_branches() {
    # Get all orchestration-tools-* branches
    git branch -r | grep "origin/orchestration-tools-" | sed 's/origin\///' | xargs
}

# Function to check if branch is valid for distribution
is_valid_target_branch() {
    local branch="$1"
    
    # Check if branch is a taskmaster branch (should not be distributed to)
    if [[ "$branch" == taskmaster* ]]; then
        echo "INFO: Skipping taskmaster branch $branch (worktree isolation required)"
        return 1
    fi
    
    # Check if branch is orchestration-tools-* (valid for distribution)
    if [[ "$branch" == orchestration-tools* ]]; then
        return 0
    fi
    
    # For other branches, check configuration
    return 0
}

# Function to fix permissions after distribution
fix_distribution_permissions() {
    local target_branch="$1"
    
    # Make sure scripts are executable
    find "scripts/" -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
    find "scripts/hooks/" -type f -exec chmod +x {} \; 2>/dev/null || true
}

# Function to validate distribution after completion
validate_distribution() {
    local target_branch="$1"
    
    # Run validation script if it exists
    if [[ -f "scripts/validate-orchestration-context.sh" ]]; then
        echo "Running validation for $target_branch..."
        # This would be run on the target branch after switching
    fi
}

# Export functions that should be available to other modules
export -f distribute_setup_files
export -f distribute_hooks
export -f distribute_configs
export -f distribute_all_files
export -f sync_from_remote
export -f distribute_from_to
export -f get_source_branch
export -f get_target_branches
export -f is_valid_target_branch
export -f fix_distribution_permissions
export -f validate_distribution