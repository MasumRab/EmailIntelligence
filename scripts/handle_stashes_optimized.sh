#!/bin/bash

# Advanced Script to handle stashes and apply them to the correct branches
# This script will systematically process each stash, identify the correct branch,
# and apply the stash to that branch with enhanced features.

set -e  # Exit on any error

# Source common library to avoid code duplication
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMON_LIB="$SCRIPT_DIR/lib/stash_common.sh"

if [[ -f "$COMMON_LIB" ]]; then
    source "$COMMON_LIB"
else
    echo "Error: Common library not found at $COMMON_LIB"
    exit 1
fi

print_color "BLUE" "=== Advanced Stash Resolution Procedure ==="
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
        if git checkout -b "$branch_name" "$base_branch" 2>/dev/null; then
            print_color "GREEN" "Successfully created branch $branch_name from $base_branch"
        else
            print_color "RED" "Failed to create branch $branch_name from $base_branch"
            return 1
        fi
    fi
    return 0
}

# Function to get all remote branches
get_remote_branches() {
    git branch -r | grep -v '\->' | sed 's/origin\///' | grep -v "HEAD"
}

# Function to find the best matching branch
find_best_matching_branch() {
    local target_branch_candidate=$1
    
    # First, check if the exact branch exists
    if branch_exists "$target_branch_candidate"; then
        echo "$target_branch_candidate"
        return
    fi
    
    # Check for similar branch names (partial match)
    local similar_branches=$(git branch --list | grep -v "\*" | grep "$target_branch_candidate" | sed 's/^[[:space:]]*//')
    if [[ -n "$similar_branches" ]]; then
        echo "$similar_branches" | head -n 1
        return
    fi
    
    # Check remote branches for matches
    local remote_matches=$(get_remote_branches | grep "$target_branch_candidate" | head -n 1)
    if [[ -n "$remote_matches" ]]; then
        echo "$remote_matches"
        return
    fi
    
    # If nothing found, return the original candidate
    echo "$target_branch_candidate"
}

# Function to process a single stash with more options
process_stash() {
    local stash_index=$1
    local stash_message=$(git stash list | sed -n "$((stash_index+1))p" || echo "")
    
    if [ -z "$stash_message" ]; then
        print_color "YELLOW" "No stash found at index $stash_index"
        return 1
    fi
    
    print_color "BLUE" "Processing stash@$stash_index: $stash_message"
    
    # Extract branch name from the stash
    local target_branch_candidate=$(get_branch_from_stash "$stash_message")
    print_color "BLUE" "  -> Identified target branch candidate: $target_branch_candidate"
    
    # Find the best matching branch
    local target_branch=$(find_best_matching_branch "$target_branch_candidate")
    print_color "BLUE" "  -> Using target branch: $target_branch"
    
    # Check if the branch exists, create if needed
    if ! branch_exists "$target_branch"; then
        print_color "YELLOW" "  -> Branch $target_branch does not exist."
        
        # Look for similar branch names
        local all_branches=$(git branch --list | grep -v "\*" | awk '{print $1}' | head -10)
        if [ -n "$all_branches" ]; then
            print_color "YELLOW" "  -> Available branches:"
            for branch in $all_branches; do
                echo "    - $branch"
            done
            echo "  -> Enter a branch name to use, or 'create' to create $target_branch, or 'skip' to skip this stash: "
            read -r user_choice
            case "$user_choice" in
                "create")
                    if ! create_branch_if_needed "$target_branch" "main"; then
                        print_color "RED" "  -> Could not create branch. Skipping stash@$stash_index"
                        return 1
                    fi
                    ;;
                "skip")
                    print_color "YELLOW" "  -> Skipping stash@$stash_index as requested"
                    return 1
                    ;;
                "")
                    print_color "YELLOW" "  -> No branch specified. Skipping stash@$stash_index"
                    return 1
                    ;;
                *)
                    if branch_exists "$user_choice"; then
                        target_branch="$user_choice"
                        print_color "BLUE" "  -> Using user-specified branch: $target_branch"
                    else
                        print_color "RED" "  -> Branch $user_choice does not exist. Skipping stash@$stash_index"
                        return 1
                    fi
                    ;;
            esac
        else
            if confirm_action "Branch $target_branch does not exist. Create from main?"; then
                if ! create_branch_if_needed "$target_branch" "main"; then
                    print_color "RED" "  -> Could not create branch. Skipping stash@$stash_index"
                    return 1
                fi
            else
                print_color "YELLOW" "  -> Skipping stash@$stash_index as creation was declined"
                return 1
            fi
        fi
    fi
    
    # Switch to the target branch
    print_color "BLUE" "  -> Switching to branch: $target_branch"
    if ! git checkout "$target_branch" > /dev/null 2>&1; then
        print_color "RED" "  -> Failed to switch to $target_branch"
        return 1
    fi
    
    # Check if there are uncommitted changes on the target branch
    if [[ -n "$(git status --porcelain)" ]]; then
        print_color "YELLOW" "  -> WARNING: $target_branch has uncommitted changes!"
        echo "Current changes on $target_branch:"
        git status --porcelain | head -5
        if [[ $(git status --porcelain | wc -l) -gt 5 ]]; then
            echo "  ... and $(( $(git status --porcelain | wc -l) - 5 )) more files"
        fi
        
        echo "How do you want to proceed?"
        echo "1) Stash current changes and proceed (recommended)"
        echo "2) Apply stash anyway (may cause conflicts)"
        echo "3) Skip this stash and return to previous branch"
        echo -n "Enter your choice (1-3): "
        read -r choice
        
        case $choice in
            1)
                print_color "BLUE" "  -> Stashing current changes on $target_branch..."
                git stash push -m "Auto-stashed before applying other stash" || {
                    print_color "YELLOW" "  -> No changes to stash or stash failed"
                }
                ;;
            2)
                print_color "YELLOW" "  -> Proceeding with potential conflicts..."
                ;;
            3)
                print_color "BLUE" "  -> Returning to previous branch and skipping stash@$stash_index..."
                git checkout - > /dev/null 2>&1
                return 1
                ;;
            *)
                print_color "YELLOW" "  -> Invalid choice, proceeding anyway..."
                ;;
        esac
    fi
    
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
        print_color "YELLOW" "  -> Conflicts detected, would you like to resolve interactively?"
        
        if confirm_action "Resolve conflicts interactively?"; then
            # Use the interactive resolver
            local interactive_script="$SCRIPT_DIR/interactive_stash_resolver_optimized.sh"
            if [[ -f "$interactive_script" ]]; then
                if "$interactive_script" "stash@{$stash_index}"; then
                    print_color "GREEN" "Stash applied successfully with interactive resolution"
                else
                    print_color "YELLOW" "Interactive resolution cancelled or failed"
                    # Return to previous state
                    git checkout . > /dev/null 2>&1
                    git clean -fd > /dev/null 2>&1
                    return 1
                fi
            else
                print_color "RED" "Interactive resolver not found, skipping stash@$stash_index"
                git checkout . > /dev/null 2>&1
                git clean -fd > /dev/null 2>&1
                return 1
            fi
        else
            print_color "YELLOW" "Skipping stash@$stash_index due to conflicts"
            # Return to previous state
            git checkout . > /dev/null 2>&1
            git clean -fd > /dev/null 2>&1
            return 1
        fi
    fi
    
    print_color "GREEN" "  -> Completed processing stash@$stash_index"
    return 0
}

# Function to create a summary of stashes by branch
summarize_stashes() {
    print_color "BLUE" "Advanced Stash Summary by Branch:"
    
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    if [[ ${#stash_list[@]} -eq 0 ]]; then
        echo "No stashes found."
        return
    fi
    
    # Group stashes by branch
    declare -A stashes_by_branch
    
    for stash_ref in "${stash_list[@]}"; do
        if [[ -n "$stash_ref" ]]; then
            local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
            local branch_name=$(get_branch_from_stash "$stash_message")
            stashes_by_branch["$branch_name"]+="$stash_ref "
        fi
    done
    
    # Print grouped stashes
    for branch in "${!stashes_by_branch[@]}"; do
        local count=0
        for stash in ${stashes_by_branch["$branch"]}; do
            ((count++))
        done
        printf "%-30s : %d stash(es)\n" "$branch" "$count"
        
        # List the actual stashes
        for stash in ${stashes_by_branch["$branch"]}; do
            local message=$(git stash list | grep "$stash" | cut -d: -f2-)
            echo "    - $stash: $message"
        done
        echo ""
    done
}

# Function to get stash statistics
get_stash_stats() {
    local stash_count
    stash_count=$(get_stash_count)
    
    if [ "$stash_count" -eq 0 ]; then
        print_color "GREEN" "No stashes to process."
        return 0
    fi
    
    print_color "BLUE" "Stash Statistics:"
    echo "Total stashes: $stash_count"
    
    # Count by type
    local orchestration_count=$(git stash list | grep -c "orchestration-tools" || echo 0)
    local main_count=$(git stash list | grep -c "main" || echo 0) 
    local feature_count=$(git stash list | grep -c "feature/" || echo 0)
    local other_count=$((stash_count - orchestration_count - main_count - feature_count))
    
    echo "  - orchestration-tools: $orchestration_count"
    echo "  - main: $main_count" 
    echo "  - feature/*: $feature_count"
    echo "  - other: $other_count"
    
    # Show oldest and newest
    if [ "$stash_count" -gt 0 ]; then
        local newest=$(git stash list | head -n1)
        local oldest=$(git stash list | tail -n1)
        echo ""
        echo "Newest stash: $newest"
        echo "Oldest stash: $oldest"
    fi
}

# Main execution
print_color "BLUE" "Initial stash status:"
show_stash_status
echo

summarize_stashes
echo

get_stash_stats
echo

print_color "YELLOW" "WARNING: This procedure will apply stashes to their corresponding branches."
print_color "YELLOW" "You may need to resolve conflicts and decide whether to commit or discard the changes afterwards."
echo

read -p "Do you want to proceed with processing all stashes? (yes/no/analyze-only): " confirm

if [ "$confirm" = "analyze-only" ]; then
    print_color "BLUE" "Analysis completed. No stashes were processed."
    exit 0
elif [ "$confirm" = "yes" ]; then
    # Process each stash in order (starting from newest - index 0)
    local stash_count
    stash_count=$(get_stash_count)
    
    if [ "$stash_count" -eq 0 ]; then
        print_color "GREEN" "No stashes to process."
        exit 0
    fi
    
    print_color "BLUE" "Starting to process $stash_count stashes..."
    
    local successful=0
    local failed=0
    
    # Process each stash
    for i in $(seq 0 $((stash_count - 1))); do
        echo
        print_color "BLUE" "--- Processing stash $((i + 1))/$stash_count ---"
        if process_stash $i; then
            print_color "GREEN" "Successfully processed stash@$i"
            ((successful++))
        else
            print_color "RED" "Failed to process stash@$i"
            ((failed++))
        fi
    done
    
    echo
    print_color "GREEN" "Stash processing completed!"
    print_color "GREEN" "Successful: $successful | Failed: $failed"
    print_color "YELLOW" "Please review the changes on each branch and decide whether to commit or discard them."
    
    # Show final status
    echo
    print_color "BLUE" "Final stash status:"
    show_stash_status
    
    echo
    print_color "BLUE" "Branches with changes:"
    for branch in $(git branch --list | grep -v "\*" | awk '{print $1}'); do
        # Switch to branch to check status
        if git checkout "$branch" > /dev/null 2>&1; then
            if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
                echo "  $branch has $(git status --porcelain | wc -l) uncommitted changes"
            fi
        fi
    done
    
    # Return to original branch
    git checkout - > /dev/null 2>&1
    
else
    print_color "YELLOW" "Operation cancelled."
fi

echo
print_color "BLUE" "=== Advanced Stash Resolution Procedure Complete ==="