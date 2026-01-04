#!/bin/bash
# Common library for stash management scripts
# Contains shared functions and constants to avoid duplication

# Colors for output - defined once for consistency across all scripts
declare -A COLORS=(
    ["RED"]='\033[0;31m'
    ["GREEN"]='\033[0;32m'
    ["YELLOW"]='\033[1;33m'
    ["BLUE"]='\033[0;34m'
    ["NC"]='\033[0m' # No Color
)

# Function to print colored output
print_color() {
    local color="$1"
    local message="$2"
    echo -e "${COLORS[$color]}$message${COLORS[NC]}"
}

# Function to get branch name from stash message
get_branch_from_stash() {
    local stash_message="$1"
    if [[ $stash_message =~ "WIP on "([^[:space:]]+)":" ]] || [[ $stash_message =~ "On "([^[:space:]]+)":" ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        echo "unknown_branch"
    fi
}

# Function to show stash details
show_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    print_color "BLUE" "Stash details for $stash_ref:"
    git stash show -p "$stash_ref"
}

# Function to apply stash with optional interactive resolution
apply_stash() {
    local stash_ref="$1"
    local interactive="${2:-false}"
    
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    print_color "BLUE" "Applying stash $stash_ref..."
    
    if [[ "$interactive" == "true" ]]; then
        # Use interactive resolver if available
        local script_dir="$(dirname "${BASH_SOURCE[0]}")"
        local interactive_script="$script_dir/interactive_stash_resolver.sh"
        
        if [[ -f "$interactive_script" ]]; then
            "$interactive_script" "$stash_ref"
            return $?
        else
            print_color "YELLOW" "Interactive resolver not found, falling back to standard apply..."
        fi
    fi
    
    if git stash apply "$stash_ref"; then
        print_color "GREEN" "Stash applied successfully"
        return 0
    else
        print_color "RED" "Failed to apply stash (conflicts detected)"
        return 1
    fi
}

# Function to check if a branch exists
branch_exists() {
    local branch_name="$1"
    git show-ref --verify --quiet "refs/heads/$branch_name"
}

# Function to get a list of stashes
get_stash_list() {
    git stash list | cut -d: -f1
}

# Function to get stash count
get_stash_count() {
    git stash list | wc -l
}

# Function to confirm user action
confirm_action() {
    local message="$1"
    print_color "YELLOW" "$message (y/N)"
    read -r confirm
    [[ "$confirm" =~ ^[Yy]$ ]]
}