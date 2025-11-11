#!/bin/bash

# Script to handle stashes and apply them to the correct branches
# This script will systematically process each stash, identify the correct branch,
# and apply the stash to that branch.

set -e  # Exit on any error

# Source common library
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
source "$SCRIPT_DIR/lib/stash_common.sh"

print_color "BLUE" "=== Stash Resolution Procedure ==="
echo "This procedure will help you systematically resolve all stashes."
echo

# Function to display current stash status
show_stash_status() {
    print_color "BLUE" "Current stash status:"
    git stash list || echo "No stashes found."
    echo
}

# Function to check if a branch exists
branch_exists() {
    local branch_name=$1
    git show-ref --verify --quiet "refs/heads/$branch_name"
}

# Function to create a branch if it doesn't exist
create_branch_if_needed() {
    local branch_name=$1
    local base_branch=${2:-main}  # Default to main if not specified
    
    if ! branch_exists "$branch_name"; then
        print_color "YELLOW" "Branch $branch_name does not exist. Creating from $base_branch..."
        git checkout -b "$branch_name" "$base_branch" || {
            print_color "RED" "Failed to create branch $branch_name from $base_branch"
            return 1
        }
    fi
    return 0
}

# Function to process a single stash
process_stash() {
    local stash_index=$1
    local stash_message=$(git stash list | sed -n "$((stash_index+1))p" || echo "")
    
    if [ -z "$stash_message" ]; then
        print_color "YELLOW" "No stash found at index $stash_index"
        return 1
    fi
    
    print_color "BLUE" "Processing stash@$stash_index: $stash_message"
    
    # Extract branch name from the stash
    local target_branch=$(get_branch_from_stash "$stash_message")
    print_color "BLUE" "  -> Identified target branch: $target_branch"
    
    # Check if the branch exists, create if needed
    if ! branch_exists "$target_branch"; then
        print_color "YELLOW" "  -> Branch $target_branch does not exist. Attempting to find similar branches..."
        
        # Look for similar branch names
        local similar_branches=$(git branch --list | grep -o "$target_branch\|* $target_branch\|${target_branch%-*}" | grep -v "^\*" | head -5)
        
        if [ -n "$similar_branches" ]; then
            print_color "YELLOW" "  -> Found similar branches: $similar_branches"
            read -p "  -> Enter the correct branch name or 'create' to create $target_branch: " corrected_branch
            if [ "$corrected_branch" = "create" ]; then
                corrected_branch="$target_branch"
            fi
        else
            corrected_branch="$target_branch"
        fi
        
        if ! create_branch_if_needed "$corrected_branch" "main"; then
            print_color "RED" "  -> Could not create or find appropriate branch. Skipping stash@$stash_index"
            return 1
        fi
        target_branch="$corrected_branch"
    fi
    
    # Switch to the target branch
    print_color "BLUE" "  -> Switching to branch: $target_branch"
    git checkout "$target_branch" > /dev/null 2>&1 || {
        print_color "RED" "  -> Failed to switch to $target_branch"
        return 1
    }
    
    # Apply the stash
    print_color "BLUE" "  -> Applying stash@$stash_index to $target_branch"
    if git stash apply "stash@{$stash_index}" 2>/dev/null; then
        print_color "GREEN" "  -> Successfully applied stash@$stash_index to $target_branch"
        
        # Show what changes were applied
        local changed_files=$(git status --porcelain | wc -l)
        if [ "$changed_files" -gt 0 ]; then
            print_color "BLUE" "  -> Files changed in $target_branch after applying stash:"
            git status --porcelain | head -10
            if [ $(git status --porcelain | wc -l) -gt 10 ]; then
                echo "  ... and $((changed_files - 10)) more files"
            fi
        fi
    else
        print_color "RED" "  -> Failed to apply stash@$stash_index to $target_branch"
        print_color "YELLOW" "  -> Attempting to pop stash@$stash_index instead"
        if git stash pop "stash@{$stash_index}" 2>/dev/null; then
            print_color "GREEN" "  -> Successfully popped stash@$stash_index to $target_branch"
        else
            print_color "RED" "  -> Failed to pop stash@$stash_index to $target_branch"
            git checkout - > /dev/null 2>&1  # Go back to previous branch
            return 1
        fi
    fi
    
    print_color "GREEN" "  -> Completed processing stash@$stash_index"
    return 0
}

# Function to create a summary of stashes by branch
summarize_stashes() {
    print_color "BLUE" "Stash Summary by Branch:"
    for i in {0..16}; do  # Check up to stash@{16}
        local stash_message=$(git stash list | sed -n "$((i+1))p")
        if [ -n "$stash_message" ]; then
            local target_branch=$(get_branch_from_stash "$stash_message")
            echo "  stash@{$i} -> $target_branch"
        fi
    done
    echo
}

# Main execution
print_color "BLUE" "Initial stash status:"
show_stash_status
echo

summarize_stashes

print_color "YELLOW" "WARNING: This procedure will apply stashes to their corresponding branches."
print_color "YELLOW" "You may need to resolve conflicts and decide whether to commit or discard the changes afterwards."
echo

read -p "Do you want to proceed with processing all stashes? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    # Process each stash in order (starting from newest - index 0)
    local stash_count
    stash_count=$(get_stash_count)
    
    if [ "$stash_count" -eq 0 ]; then
        print_color "GREEN" "No stashes to process."
        exit 0
    fi
    
    print_color "BLUE" "Starting to process $stash_count stashes..."
    
    # Process each stash
    for i in $(seq 0 $((stash_count - 1))); do
        echo
        print_color "BLUE" "--- Processing stash $((i + 1))/$stash_count ---"
        if process_stash $i; then
            print_color "GREEN" "Successfully processed stash@$i"
        else
            print_color "RED" "Failed to process stash@$i"
        fi
    done
    
    echo
    print_color "GREEN" "All stashes have been processed."
    print_color "YELLOW" "Please review the changes on each branch and decide whether to commit or discard them."
    
    # Show final status
    echo
    print_color "BLUE" "Final stash status:"
    show_stash_status
    
    echo
    print_color "BLUE" "Branches with changes:"
    for branch in $(git branch --list | grep -v "\*" | awk '{print $1}'); do
        if [ -n "$(git status --branch --porcelain 2>/dev/null | grep '^##')" ] && [ -n "$(git status --porcelain 2>/dev/null)" ]; then
            git checkout "$branch" > /dev/null 2>&1
            if [ -n "$(git status --porcelain)" ]; then
                echo "  $branch has $(git status --porcelain | wc -l) uncommitted changes"
            fi
        fi
    done
    
    # Go back to original branch
    git checkout - > /dev/null 2>&1
    
else
    print_color "YELLOW" "Operation cancelled."
fi

echo
print_color "BLUE" "=== Stash Resolution Procedure Complete ==="