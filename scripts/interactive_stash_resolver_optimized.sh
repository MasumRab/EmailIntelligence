#!/bin/bash
# Optimized Interactive stash resolution with line-by-line conflict resolution
# This script provides an interactive way to resolve stash conflicts with granular control

set -e

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

# Function to display conflicts and options
resolve_conflict() {
    local file="$1"
    print_color "YELLOW" "Conflict detected in: $file"
    echo "Showing conflict markers and available options:"
    echo ""
    
    # Show the conflict with line numbers
    local line_num=1
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" =~ ^<<<<<<< ]]; then
            print_color "RED" "<<<<<<< ${line#<<<<<<< }"
        elif [[ "$line" =~ ^======= ]]; then
            print_color "YELLOW" "======="
        elif [[ "$line" =~ ^>>>>>>> ]]; then
            print_color "RED" ">>>>>>> ${line#>>>>>>> }"
        else
            echo "$line_num: $line"
        fi
        ((line_num++))
    done < "$file"
    
    echo ""
    echo "Choose how to resolve this conflict:"
    echo "1) Accept all 'theirs' changes (stashed changes)"
    echo "2) Accept all 'ours' changes (current branch)"
    echo "3) Keep both versions"
    echo "4) Edit manually in default editor"
    echo "5) Skip this file for now"
    echo "6) Abort the entire stash application"
    echo -n "Enter your choice (1-6): "
    
    read -r choice
    
    case $choice in
        1)
            echo "Accepting all 'theirs' changes..."
            git checkout --theirs "$file"
            git add "$file"
            ;;
        2)
            echo "Accepting all 'ours' changes..."
            git checkout --ours "$file"
            git add "$file"
            ;;
        3)
            echo "Keeping both versions..."
            # Remove conflict markers while keeping both versions
            sed -i '/^<<<<<<< /d; /^=======/d; /^>>>>>>> /d' "$file"
            git add "$file"
            ;;
        4)
            echo "Opening file in editor for manual resolution..."
            ${EDITOR:-vi} "$file"
            echo "Please resolve the conflicts and press Enter when done..."
            read -r _
            git add "$file"
            ;;
        5)
            echo "Skipping file for now..."
            return 1
            ;;
        6)
            echo "Aborting stash application..."
            git reset --hard HEAD
            git stash apply --abort 2>/dev/null || true
            exit 1
            ;;
        *)
            echo "Invalid choice, defaulting to 'theirs'..."
            git checkout --theirs "$file"
            git add "$file"
            ;;
    esac
}

# Function to apply stash with interactive conflict resolution
apply_stash_interactive() {
    local stash_ref="$1"
    
    print_color "BLUE" "Starting interactive stash application: $stash_ref"
    
    # First, try to apply the stash
    if git stash apply "$stash_ref" 2>/dev/null; then
        print_color "GREEN" "Stash applied without conflicts!"
        
        # Add all changes
        git add -A
        return 0
    else
        print_color "RED" "Conflicts detected, starting interactive resolution..."
        
        # Get list of conflicted files
        local conflicted_files
        readarray -t conflicted_files < <(git diff --name-only --diff-filter=U)
        
        local file
        for file in "${conflicted_files[@]}"; do
            resolve_conflict "$file"
        done
        
        # Check for any remaining unmerged files
        local remaining_conflicts
        readarray -t remaining_conflicts < <(git diff --name-only --diff-filter=U)
        if [[ ${#remaining_conflicts[@]} -gt 0 ]]; then
            print_color "YELLOW" "Some conflicts remain unhandled:"
            for file in "${remaining_conflicts[@]}"; do
                echo "  - $file"
            done
        fi
        
        # Add any remaining modified files
        local modified_files
        readarray -t modified_files < <(git diff --name-only --diff-filter=AM)
        if [[ ${#modified_files[@]} -gt 0 ]]; then
            git add "${modified_files[@]}"
        fi
        
        return 0
    fi
}

# Function to show stash details before applying
show_stash_info() {
    local stash_ref="$1"
    print_color "BLUE" "Stash Information:"
    git stash show -p "$stash_ref" | head -20
    echo "..."
    echo ""
    
    print_color "BLUE" "Files in stash:"
    git stash show --name-only "$stash_ref"
    echo ""
}

# Main execution
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <stash_ref>"
    echo "Example: $0 stash@{0}"
    echo ""
    echo "This script provides interactive conflict resolution when applying git stashes."
    echo "It allows you to choose how to handle each conflict line-by-line."
    exit 1
fi

STASH_REF="$1"

# Show stash info
show_stash_info "$STASH_REF"

# Confirm before proceeding
print_color "YELLOW" "Apply this stash interactively? (y/N)"
read -r confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Apply stash with interactive resolution
apply_stash_interactive "$STASH_REF"

print_color "GREEN" "Stash resolution complete!"
echo "Please review changes with 'git status' and commit when ready."