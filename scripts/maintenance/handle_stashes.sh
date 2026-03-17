#!/bin/bash

# Script to handle stashes and apply them to the correct branches
# This script will systematically process each stash, identify the correct branch,
# and apply the stash to that branch.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Stash Resolution Procedure ===${NC}"
echo "This procedure will help you systematically resolve all stashes."
echo

# Function to display current stash status
show_stash_status() {
    echo -e "${BLUE}Current stash status:${NC}"
    git stash list || echo "No stashes found."
    echo
}

# Function to get the branch name from a stash message
get_branch_from_stash() {
    local stash_index=$1
    local stash_message=$(git stash list | sed -n "$((stash_index+1))p" | cut -d: -f2-)
    
    # Extract branch name from stash message
    if [[ $stash_message =~ "WIP on "([^[:space:]]+)":" ]] || [[ $stash_message =~ "On "([^[:space:]]+)":" ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        echo "unknown_branch_$stash_index"
    fi
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
        echo -e "${YELLOW}Branch $branch_name does not exist. Creating from $base_branch...${NC}"
        git checkout -b "$branch_name" "$base_branch" || {
            echo -e "${RED}Failed to create branch $branch_name from $base_branch${NC}"
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
        echo -e "${YELLOW}No stash found at index $stash_index${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Processing stash@$stash_index: $stash_message${NC}"
    
    # Extract branch name from the stash
    local target_branch=$(get_branch_from_stash $stash_index)
    echo -e "${BLUE}  -> Identified target branch: $target_branch${NC}"
    
    # Check if the branch exists, create if needed
    if ! branch_exists "$target_branch"; then
        echo -e "${YELLOW}  -> Branch $target_branch does not exist. Attempting to find similar branches...${NC}"
        
        # Look for similar branch names
        local similar_branches=$(git branch --list | grep -o "$target_branch\|* $target_branch\|${target_branch%-*}" | grep -v "^\*" | head -5)
        
        if [ -n "$similar_branches" ]; then
            echo -e "${YELLOW}  -> Found similar branches: $similar_branches${NC}"
            read -p "  -> Enter the correct branch name or 'create' to create $target_branch: " corrected_branch
            if [ "$corrected_branch" = "create" ]; then
                corrected_branch="$target_branch"
            fi
        else
            corrected_branch="$target_branch"
        fi
        
        if ! create_branch_if_needed "$corrected_branch" "main"; then
            echo -e "${RED}  -> Could not create or find appropriate branch. Skipping stash@$stash_index${NC}"
            return 1
        fi
        target_branch="$corrected_branch"
    fi
    
    # Switch to the target branch
    echo -e "${BLUE}  -> Switching to branch: $target_branch${NC}"
    git checkout "$target_branch" > /dev/null 2>&1 || {
        echo -e "${RED}  -> Failed to switch to $target_branch${NC}"
        return 1
    }
    
    # Apply the stash
    echo -e "${BLUE}  -> Applying stash@$stash_index to $target_branch${NC}"
    if git stash apply "stash@{$stash_index}" 2>/dev/null; then
        echo -e "${GREEN}  -> Successfully applied stash@$stash_index to $target_branch${NC}"
        
        # Show what changes were applied
        local changed_files=$(git status --porcelain | wc -l)
        if [ "$changed_files" -gt 0 ]; then
            echo -e "${BLUE}  -> Files changed in $target_branch after applying stash:${NC}"
            git status --porcelain | head -10
            if [ $(git status --porcelain | wc -l) -gt 10 ]; then
                echo "  ... and $((changed_files - 10)) more files"
            fi
        fi
    else
        echo -e "${RED}  -> Failed to apply stash@$stash_index to $target_branch${NC}"
        echo -e "${YELLOW}  -> Attempting to pop stash@$stash_index instead${NC}"
        if git stash pop "stash@{$stash_index}" 2>/dev/null; then
            echo -e "${GREEN}  -> Successfully popped stash@$stash_index to $target_branch${NC}"
        else
            echo -e "${RED}  -> Failed to pop stash@$stash_index to $target_branch${NC}"
            git checkout - > /dev/null 2>&1  # Go back to previous branch
            return 1
        fi
    fi
    
    echo -e "${GREEN}  -> Completed processing stash@$stash_index${NC}"
    return 0
}

# Function to create a summary of stashes by branch
summarize_stashes() {
    echo -e "${BLUE}Stash Summary by Branch:${NC}"
    for i in {0..16}; do  # Check up to stash@{16}
        local stash_message=$(git stash list | sed -n "$((i+1))p")
        if [ -n "$stash_message" ]; then
            local target_branch=$(get_branch_from_stash $i)
            echo "  stash@{$i} -> $target_branch"
        fi
    done
    echo
}

# Main execution
echo -e "${BLUE}Initial stash status:${NC}"
show_stash_status
echo

summarize_stashes

echo -e "${YELLOW}WARNING: This procedure will apply stashes to their corresponding branches.${NC}"
echo -e "${YELLOW}You may need to resolve conflicts and decide whether to commit or discard the changes afterwards.${NC}"
echo

read -p "Do you want to proceed with processing all stashes? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    # Process each stash in order (starting from newest - index 0)
    local stash_count=$(git stash list | wc -l)
    
    if [ "$stash_count" -eq 0 ]; then
        echo -e "${GREEN}No stashes to process.${NC}"
        exit 0
    fi
    
    echo -e "${BLUE}Starting to process $stash_count stashes...${NC}"
    
    # Process each stash
    for i in $(seq 0 $((stash_count - 1))); do
        echo
        echo -e "${BLUE}--- Processing stash $((i + 1))/$stash_count ---${NC}"
        if process_stash $i; then
            echo -e "${GREEN}Successfully processed stash@$i${NC}"
        else
            echo -e "${RED}Failed to process stash@$i${NC}"
        fi
    done
    
    echo
    echo -e "${GREEN}All stashes have been processed.${NC}"
    echo -e "${YELLOW}Please review the changes on each branch and decide whether to commit or discard them.${NC}"
    
    # Show final status
    echo
    echo -e "${BLUE}Final stash status:${NC}"
    show_stash_status
    
    echo
    echo -e "${BLUE}Branches with changes:${NC}"
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
    echo -e "${YELLOW}Operation cancelled.${NC}"
fi

echo
echo -e "${BLUE}=== Stash Resolution Procedure Complete ===${NC}"