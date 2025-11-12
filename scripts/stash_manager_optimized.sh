#!/bin/bash
# Enhanced Stash Management Tool with Interactive Conflict Resolution
# This script provides comprehensive stash management capabilities
# utilizing the common library for shared functions

set -e

# Source common library to avoid code duplication
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMON_LIB="$SCRIPT_DIR/lib/stash_common.sh"

if [[ -f "$COMMON_LIB" ]]; then
    source "$COMMON_LIB"
else
    echo "Error: Common library not found at $COMMON_LIB"
    exit 1
fi

# Function to display help
show_help() {
    print_color "BLUE" "Enhanced Stash Management Tool"
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  list                    List all stashes"
    echo "  show <stash>            Show details of a specific stash"
    echo "  apply <stash>           Apply a stash (non-interactive)"
    echo "  apply-interactive <stash> Apply a stash with interactive conflict resolution"
    echo "  pop <stash>             Apply and drop a stash (non-interactive)"
    echo "  pop-interactive <stash> Apply and drop a stash with interactive conflict resolution"
    echo "  save [message]          Save current changes to a new stash"
    echo "  drop <stash>            Drop a stash"
    echo "  clear                   Clear all stashes"
    echo "  analyze                 Analyze stashes and suggest processing order"
    echo "  process-all             Process all stashes with interactive resolution"
    echo "  branch-info             Show which branch each stash belongs to"
    echo "  search <pattern>        Search stashes for a specific pattern"
    echo "  save-with-branch <branch> [message] Save changes with branch info in message"
    echo "  help                    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 show stash@{0}"
    echo "  $0 apply-interactive stash@{0}"
    echo "  $0 process-all"
    echo "  $0 search 'fix'"
    echo "  $0 branch-info"
    echo "  $0 save-with-branch feature/new-feature 'WIP on feature/new-feature'"
}

# Function to list all stashes with branch information
list_stashes() {
    print_color "BLUE" "Current stashes:"
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    if [[ ${#stash_list[@]} -eq 0 ]]; then
        echo "No stashes found."
        return 0
    fi
    
    for stash_ref in "${stash_list[@]}"; do
        if [[ -n "$stash_ref" ]]; then
            local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
            local branch_name=$(get_branch_from_stash "$stash_message")
            printf "%-20s -> %s\n" "$stash_ref" "$branch_name"
        fi
    done
}

# Function to show stash details using common library function
show_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    show_stash "$stash_ref"  # Using function from common library
}

# Function to apply stash non-interactively using common library function
apply_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    apply_stash "$stash_ref" "false"  # Using function from common library
}

# Function to apply stash with interactive conflict resolution
apply_stash_interactive() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    print_color "BLUE" "Applying stash $stash_ref with interactive conflict resolution..."
    
    # Check if interactive resolver exists
    local script_path="$(dirname "$0")/interactive_stash_resolver_optimized.sh"
    if [[ -f "$script_path" ]]; then
        "$script_path" "$stash_ref"
        return $?
    else
        print_color "YELLOW" "Interactive resolver not found, falling back to standard apply..."
        apply_stash "$stash_ref" "false"
        return $?
    fi
}

# Function to pop stash non-interactively
pop_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    print_color "BLUE" "Popping stash $stash_ref..."
    if git stash pop "$stash_ref"; then
        print_color "GREEN" "Stash popped successfully"
        return 0
    else
        print_color "RED" "Failed to pop stash (conflicts detected)"
        return 1
    fi
}

# Function to pop stash with interactive conflict resolution
pop_stash_interactive() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    print_color "BLUE" "Popping stash $stash_ref with interactive conflict resolution..."
    
    # Apply with interactive resolution
    if apply_stash_interactive "$stash_ref"; then
        # Drop the stash after successful application
        print_color "BLUE" "Dropping stash $stash_ref..."
        git stash drop "$stash_ref"
        print_color "GREEN" "Stash popped successfully"
        return 0
    else
        print_color "RED" "Failed to apply stash, not dropping"
        return 1
    fi
}

# Function to save current changes to stash
save_stash() {
    local message="$1"
    if [[ -z "$message" ]]; then
        print_color "BLUE" "Saving current changes to stash..."
        if git stash save; then
            print_color "GREEN" "Changes saved to stash"
        else
            print_color "RED" "Failed to save changes to stash"
            return 1
        fi
    else
        print_color "BLUE" "Saving current changes to stash with message: $message"
        if git stash save "$message"; then
            print_color "GREEN" "Changes saved to stash"
        else
            print_color "RED" "Failed to save changes to stash"
            return 1
        fi
    fi
}

# Function to save current changes to stash with branch info
save_with_branch() {
    local branch_name="$1"
    local message="$2"
    
    if [[ -z "$branch_name" ]]; then
        branch_name=$(git branch --show-current)
        if [[ -z "$branch_name" || "$branch_name" == "HEAD" ]]; then
            print_color "RED" "Error: Could not determine current branch name"
            return 1
        fi
    fi
    
    local stash_message="WIP on $branch_name: $(git log -1 --format="%h %s")"
    if [[ -n "$message" ]]; then
        stash_message="$message"
    fi
    
    print_color "BLUE" "Saving changes with branch info: $stash_message"
    if git stash save "$stash_message"; then
        print_color "GREEN" "Changes saved to stash with branch info"
    else
        print_color "RED" "Failed to save changes to stash"
        return 1
    fi
}

# Function to drop a stash
drop_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        print_color "RED" "Error: Stash reference required"
        return 1
    fi
    
    if confirm_action "Are you sure you want to drop $stash_ref?"; then
        git stash drop "$stash_ref"
        print_color "GREEN" "Stash dropped"
    else
        print_color "BLUE" "Operation cancelled"
    fi
}

# Function to clear all stashes
clear_stashes() {
    if confirm_action "Are you sure you want to clear all stashes?"; then
        git stash clear
        print_color "GREEN" "All stashes cleared"
    else
        print_color "BLUE" "Operation cancelled"
    fi
}

# Function to analyze stashes and suggest processing order
analyze_stashes() {
    print_color "BLUE" "Analyzing stashes..."
    
    local stash_count
    stash_count=$(get_stash_count)
    if [[ "$stash_count" -eq 0 ]]; then
        print_color "GREEN" "No stashes found"
        return 0
    fi
    
    print_color "BLUE" "Stash Analysis:"
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    for stash_ref in "${stash_list[@]}"; do
        if [[ -n "$stash_ref" ]]; then
            local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
            local branch_name=$(get_branch_from_stash "$stash_message")
            printf "  %s -> %s\n" "$stash_ref" "$branch_name"
        fi
    done
    
    echo ""
    print_color "YELLOW" "Suggested processing order:"
    echo "  1. Stashes on main development branches (orchestration-tools, main)"
    echo "  2. Stashes on feature branches"
    echo "  3. Stashes on experimental or temporary branches"
    echo ""
    print_color "BLUE" "Recommendation: Use 'apply-interactive' for each stash to handle conflicts properly"
}

# Function to show branch info for each stash
show_branch_info() {
    print_color "BLUE" "Stash Branch Information:"
    
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    if [[ ${#stash_list[@]} -eq 0 ]]; then
        echo "No stashes found."
        return 0
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
        print_color "GREEN" "Branch: $branch"
        for stash in ${stashes_by_branch["$branch"]}; do
            echo "  - $stash"
        done
        echo ""
    done
}

# Function to search stashes for a pattern
search_stashes() {
    local pattern="$1"
    if [[ -z "$pattern" ]]; then
        print_color "RED" "Error: Search pattern required"
        return 1
    fi
    
    print_color "BLUE" "Searching for pattern '$pattern' in stashes..."
    
    local found=0
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    for stash_ref in "${stash_list[@]}"; do
        if [[ -n "$stash_ref" ]]; then
            local stash_diff=$(git stash show -p "$stash_ref" 2>/dev/null)
            local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
            
            if [[ "$stash_diff" == *"$pattern"* ]] || [[ "$stash_message" == *"$pattern"* ]]; then
                print_color "GREEN" "Found in $stash_ref:"
                echo "$stash_message"
                found=1
            fi
        fi
    done
    
    if [[ $found -eq 0 ]]; then
        print_color "YELLOW" "No stashes found containing pattern '$pattern'"
    fi
}

# Function to process all stashes interactively
process_all_stashes() {
    print_color "BLUE" "Processing all stashes with interactive conflict resolution..."
    
    local stash_count
    stash_count=$(get_stash_count)
    if [[ "$stash_count" -eq 0 ]]; then
        print_color "GREEN" "No stashes found"
        return 0
    fi
    
    print_color "BLUE" "Found $stash_count stashes to process"
    
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    for stash in "${stash_list[@]}"; do
        if [[ -n "$stash" ]]; then
            print_color "BLUE" "Processing $stash..."
            echo ""
            
            # Show stash details
            show_stash "$stash"
            echo ""
            
            # Ask user how to proceed
            print_color "YELLOW" "How would you like to process this stash?"
            echo "1) Apply interactively (resolve conflicts)"
            echo "2) Skip this stash"
            echo "3) Stop processing"
            echo -n "Enter your choice (1-3): "
            
            read -r choice
            
            case $choice in
                1)
                    if apply_stash_interactive "$stash"; then
                        print_color "GREEN" "Stash applied successfully"
                        if confirm_action "Drop this stash?"; then
                            git stash drop "$stash"
                            print_color "GREEN" "Stash dropped"
                        fi
                    else
                        print_color "RED" "Failed to apply stash"
                    fi
                    ;;
                2)
                    print_color "BLUE" "Skipping $stash"
                    ;;
                3)
                    print_color "BLUE" "Stopping stash processing"
                    break
                    ;;
                *)
                    print_color "RED" "Invalid choice, skipping $stash"
                    ;;
            esac
            
            echo ""
        fi
    done
    
    print_color "GREEN" "Stash processing complete"
}

# Main execution
main() {
    case "$1" in
        list)
            list_stashes
            ;;
        show)
            show_stash "$2"
            ;;
        apply)
            apply_stash "$2"
            ;;
        apply-interactive)
            apply_stash_interactive "$2"
            ;;
        pop)
            pop_stash "$2"
            ;;
        pop-interactive)
            pop_stash_interactive "$2"
            ;;
        save)
            save_stash "$2"
            ;;
        save-with-branch)
            save_with_branch "$2" "$3"
            ;;
        drop)
            drop_stash "$2"
            ;;
        clear)
            clear_stashes
            ;;
        analyze)
            analyze_stashes
            ;;
        branch-info)
            show_branch_info
            ;;
        search)
            search_stashes "$2"
            ;;
        process-all)
            process_all_stashes
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            show_help
            ;;
        *)
            print_color "RED" "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"