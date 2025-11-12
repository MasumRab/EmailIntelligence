#!/bin/bash
# Interactive stash resolution with line-by-line conflict resolution
# This script provides an interactive way to resolve stash conflicts with granular control

# Note: NOT using set -e to allow proper error handling and user choices
set +e  # Explicitly disable exit-on-error for this script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display conflicts and options
resolve_conflict() {
    local file="$1"
    echo -e "${YELLOW}Conflict detected in: $file${NC}"
    echo "Showing conflict markers and available options:"
    echo ""
    
    # Show the conflict with line numbers
    while IFS= read -r line || [[ -n "$line" ]]; do
        # FIXED: Use substring matching instead of regex to avoid bash syntax errors with conflict markers
        if [[ "${line:0:7}" == "<<<<<<<" ]]; then
            print_color "RED" "<<<<<<< ${line#<<<<<<< } (THEIRS - from stash)"
            in_theirs_block=true
        elif [[ "${line:0:7}" == "=======" ]]; then
            print_color "YELLOW" "======= (SEPARATOR)"
            in_theirs_block=false
            in_ours_block=true
        elif [[ "${line:0:7}" == ">>>>>>> " ]]; then
            print_color "RED" ">>>>>>> ${line#>>>>>>> } (OURS - from working directory)"
            in_ours_block=false
        elif [[ "$in_theirs_block" == true ]]; then
            print_color "RED" "  $line_num: $line"
        elif [[ "$in_ours_block" == true ]]; then
            print_color "GREEN" "  $line_num: $line"
        else
            echo "  $line_num: $line"
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
            echo "Accepting all 'ours' changes (current working tree)..."
            git checkout --ours "$file"
            git add "$file"
            ;;
        3)
            echo "Keeping both versions..."
            # Remove conflict markers while keeping both versions
            # This keeps all content, just removes the markers
            sed -i '/^<<<<<<< /,/^>>>>>>> /{ /^<<<<<<< /d; /^=======/d; /^>>>>>>> /d; }' "$file"
            git add "$file"
            ;;
        4)
            echo "Opening file in editor for manual resolution..."
            ${EDITOR:-vi} "$file"
            if [[ $? -ne 0 ]]; then
                echo -e "${RED}Editor exited with error${NC}"
                return 1
            fi
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
    
    echo -e "${BLUE}Starting interactive stash application: $stash_ref${NC}"
    
    # First, try to apply the stash
    if git stash apply "$stash_ref" 2>/dev/null; then
        echo -e "${GREEN}Stash applied without conflicts!${NC}"
        
        # Add all changes
        git add -A
        return 0
    else
        echo -e "${RED}Conflicts detected, starting interactive resolution...${NC}"
        
        # Get list of conflicted files
        conflicted_files=$(git diff --name-only --diff-filter=U)
        
        for file in $conflicted_files; do
            resolve_conflict "$file"
        done
        
        # Check for any remaining unmerged files
        remaining_conflicts=$(git diff --name-only --diff-filter=U)
        if [[ -n "$remaining_conflicts" ]]; then
            echo -e "${YELLOW}Some conflicts remain unhandled:${NC}"
            for file in $remaining_conflicts; do
                echo "  - $file"
            done
        fi
        
        # Add any remaining modified files
        modified_files=$(git diff --name-only --diff-filter=AM)
        if [[ -n "$modified_files" ]]; then
            echo "$modified_files" | xargs -I {} git add "{}"
        fi
        
        return 0
    fi
}

# Function to show stash details before applying
show_stash_info() {
    local stash_ref="$1"
    echo -e "${BLUE}Stash Information:${NC}"
    git stash show -p "$stash_ref" | head -20
    echo "..."
    echo ""
    
    echo -e "${BLUE}Files in stash:${NC}"
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

# Validate stash exists
if ! git rev-parse "$STASH_REF" > /dev/null 2>&1; then
    echo -e "${RED}Error: Stash '$STASH_REF' not found${NC}"
    echo "Available stashes:"
    git stash list
    exit 1
fi

# Show stash info
show_stash_info "$STASH_REF"

# Confirm before proceeding
echo -e "${YELLOW}Apply this stash interactively? (y/N)${NC}"
read -r confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

# Apply stash with interactive resolution
apply_stash_interactive "$STASH_REF"

echo -e "${GREEN}Stash resolution complete!${NC}"
echo "Please review changes with 'git status' and commit when ready."