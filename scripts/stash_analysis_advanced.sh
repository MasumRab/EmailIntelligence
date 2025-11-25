#!/bin/bash

# Simple Advanced Stash Analysis Script
# Provides basic analysis of all stashes with recommendations

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

print_color "BLUE" "=== Advanced Stash Analysis ==="
echo

# Function to get stash statistics
get_detailed_stats() {
    print_color "BLUE" "Detailed Stash Statistics:"
    
    local stash_count
    stash_count=$(get_stash_count)
    echo "Total stashes: $stash_count"
    
    if [ "$stash_count" -eq 0 ]; then
        echo "No stashes to analyze."
        return
    fi
    
    # Analyze by branch
    echo
    print_color "BLUE" "Stashes by Branch:"
    declare -A branch_counts
    declare -A branch_stashes
    
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    for stash_ref in "${stash_list[@]}"; do
        if [[ -n "$stash_ref" ]]; then
            local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
            local branch_name=$(get_branch_from_stash "$stash_message")
            
            # Increment count for this branch
            if [[ -n "${branch_counts[$branch_name]}" ]]; then
                branch_counts["$branch_name"]=$((branch_counts["$branch_name"] + 1))
            else
                branch_counts["$branch_name"]=1
            fi
            
            # Store the stash reference
            if [[ -n "${branch_stashes[$branch_name]}" ]]; then
                branch_stashes["$branch_name"]="${branch_stashes[$branch_name]} $stash_ref"
            else
                branch_stashes["$branch_name"]="$stash_ref"
            fi
        fi
    done
    
    # Print branch statistics
    for branch in "${!branch_counts[@]}"; do
        printf "%-30s : %d stash(es)\n" "$branch" "${branch_counts[$branch]}"
    done
}

# Function to provide processing recommendations
get_recommendations() {
    echo
    print_color "BLUE" "Processing Recommendations:"
    echo
    
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    # Analyze branch priority
    declare -A priority_map
    priority_map["orchestration-tools"]=5
    priority_map["main"]=4
    priority_map["scientific"]=4
    priority_map["develop"]=3
    
    # Create priority-ordered list
    declare -A stash_priorities
    for stash_ref in "${stash_list[@]}"; do
        if [[ -n "$stash_ref" ]]; then
            local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
            local branch_name=$(get_branch_from_stash "$stash_message")
            
            if [[ -n "${priority_map[$branch_name]}" ]]; then
                stash_priorities["$stash_ref"]="${priority_map[$branch_name]}"
            else
                stash_priorities["$stash_ref"]=1  # Default low priority
            fi
        fi
    done
    
    # Sort by priority (higher first)
    echo "Recommended processing order (by priority):"
    for priority in 5 4 3 2 1; do
        for stash_ref in "${!stash_priorities[@]}"; do
            if [[ "${stash_priorities[$stash_ref]}" -eq $priority ]]; then
                local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
                local branch_name=$(get_branch_from_stash "$stash_message")
                printf "Priority %d: %s -> %s\n" "$priority" "$stash_ref" "$branch_name"
            fi
        done
    done
}

# Function to show stash content preview
show_content_preview() {
    echo
    print_color "BLUE" "Stash Content Preview:"
    
    local stash_list
    readarray -t stash_list < <(get_stash_list)
    
    for stash_ref in "${stash_list[@]}"; do
        if [[ -n "$stash_ref" ]]; then
            local stash_message=$(git stash list | grep "$stash_ref" | cut -d: -f2-)
            local branch_name=$(get_branch_from_stash "$stash_message")
            
            echo
            print_color "GREEN" "$stash_ref ($branch_name):"
            
            # Show changed files
            local files
            readarray -t files < <(git stash show --name-only "$stash_ref" 2>/dev/null | head -3)
            for file in "${files[@]}"; do
                if [[ -n "$file" ]]; then
                    echo "  - $file"
                fi
            done
            
            local total_files=$(git stash show --name-only "$stash_ref" 2>/dev/null | wc -l)
            if [[ $total_files -gt 3 ]]; then
                echo "  ... and $((total_files - 3)) more files"
            fi
        fi
    done
}

# Main execution
get_detailed_stats
get_recommendations
show_content_preview

echo
print_color "GREEN" "Advanced stash analysis complete!"
print_color "BLUE" "Use the recommendations above to prioritize your stash processing."