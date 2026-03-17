#!/bin/bash
# Advanced Interactive stash resolution with line-by-line conflict resolution
# This script provides an enhanced interactive way to resolve stash conflicts with granular control

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

# Function to display conflicts and options in a detailed way
resolve_conflict() {
    local file="$1"
    print_color "YELLOW" "Conflict detected in: $file"
    echo "Showing conflict markers and available options:"
    echo ""
    
    # Show the conflict with line numbers (more detailed view)
    local line_num=1
    local in_ours_block=false
    local in_theirs_block=false
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        # FIXED: Use substring matching instead of regex to avoid bash syntax errors with conflict markers
        # ADDED: Length check to prevent errors when line is shorter than 7 characters
        if [[ ${#line} -ge 7 ]]; then
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
        else
            # Line is shorter than 7 characters, so it can't be a conflict marker
            echo "  $line_num: $line"
        fi
        ((line_num++))
    done < "$file"
    
    echo ""
    echo "Choose how to resolve this conflict:"
    echo "1) Accept all 'theirs' changes (stashed changes) - Use stashed version"
    echo "2) Accept all 'ours' changes (current branch) - Use current version"
    echo "3) Keep both versions - Merge both (remove conflict markers)"
    echo "4) Edit manually in default editor"
    echo "5) Skip this file for now"
    echo "6) Choose specific lines from each side (advanced)"
    echo "7) Show diff between versions"
    echo "8) Abort the entire stash application"
    echo -n "Enter your choice (1-8): "
    
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
            resolve_conflict_by_lines "$file"
            ;;
        7)
            echo "Showing diff between conflict versions..."
            git diff --no-index /dev/null "$file" 2>/dev/null | head -50 || true
            echo ""
            resolve_conflict "$file"  # Recursive call to choose again
            ;;
        8)
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

# Advanced function to resolve conflicts line by line
resolve_conflict_by_lines() {
    local file="$1"
    print_color "BLUE" "Line-by-line conflict resolution for $file"
    echo "Enter line ranges to keep from 'theirs' (stashed) version, or 'all' to keep everything:"
    echo "Format: start-end (e.g., 1-5, 10-15) or individual lines (e.g., 1,3,5)"
    echo "Or type 'exit' to return to main options"
    
    local temp_file="/tmp/stash_resolve_$$"
    cp "$file" "$temp_file"
    
    # Show the file with conflict markers
    local line_num=1
    while IFS= read -r line || [[ -n "$line" ]]; do
        # FIXED: Use substring matching instead of regex to avoid bash syntax errors with conflict markers
        # ADDED: Length check to prevent errors when line is shorter than 7 characters
        if [[ ${#line} -ge 7 ]] && ([[ "${line:0:7}" == "<<<<<<<" ]] || [[ "${line:0:7}" == "=======" ]] || [[ "${line:0:7}" == ">>>>>>> " ]]); then
            echo "  $line_num: $line"
        elif [[ ${#line} -lt 7 ]]; then
            echo "$line_num: $line"
        else
            echo "$line_num: $line"
        fi
        ((line_num++))
    done < "$temp_file"
    
    echo -n "Enter your selection: "
    read -r selection
    
    if [[ "$selection" == "exit" ]]; then
        rm -f "$temp_file"
        return 1
    fi
    
    if [[ "$selection" == "all" ]]; then
        git checkout --theirs "$file"
        git add "$file"
        rm -f "$temp_file"
        return 0
    fi
    
    # For simplicity, we'll remove conflict markers and let user edit
    sed -i '/^<<<<<<< /d; /^=======/d; /^>>>>>>> /d' "$temp_file"
    echo "Conflict markers removed. Opening file for manual selection..."
    ${EDITOR:-vi} "$temp_file"
    
    # Move the edited file back
    mv "$temp_file" "$file"
    git add "$file"
}

# Function to apply stash with interactive conflict resolution
apply_stash_interactive() {
    local stash_ref="$1"
    
    print_color "BLUE" "Starting advanced interactive stash application: $stash_ref"
    
    # First, try to apply the stash
    if git stash apply "$stash_ref" 2>/dev/null; then
        print_color "GREEN" "Stash applied without conflicts!"
        
        # Add all changes
        git add -A
        return 0
    else
        print_color "RED" "Conflicts detected, starting advanced interactive resolution..."
        
        # Get list of conflicted files
        local conflicted_files
        readarray -t conflicted_files < <(git diff --name-only --diff-filter=U)
        
        # Process each conflicted file
        local file
        for file in "${conflicted_files[@]}"; do
            if [[ -n "$file" ]]; then
                resolve_conflict "$file"
            fi
        done
        
        # Check for any remaining unmerged files
        local remaining_conflicts
        readarray -t remaining_conflicts < <(git diff --name-only --diff-filter=U)
        if [[ ${#remaining_conflicts[@]} -gt 0 ]]; then
            print_color "YELLOW" "Some conflicts remain unhandled:"
            for file in "${remaining_conflicts[@]}"; do
                if [[ -n "$file" ]]; then
                    echo "  - $file"
                fi
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
    git stash show -p "$stash_ref" 2>&1 | head -20
    echo "..."
    echo ""
    
    print_color "BLUE" "Files in stash:"
    git stash show --name-only "$stash_ref"
    echo ""
    
    # Show statistics
    print_color "BLUE" "Stash Statistics:"
    local file_count=$(git stash show --name-only "$stash_ref" | wc -l)
    local insertions=$(git stash show -p "$stash_ref" 2>/dev/null | grep -c '^+[^+]' || echo 0)
    local deletions=$(git stash show -p "$stash_ref" 2>/dev/null | grep -c '^-[^-]' || echo 0)
    echo "  Files: $file_count"
    echo "  Insertions: $insertions"
    echo "  Deletions: $deletions"
}

# Function to perform a trial application and show expected conflicts
trial_apply() {
    local stash_ref="$1"
    
    print_color "BLUE" "Trial application to preview conflicts..."
    
    # Create a temporary branch for the trial
    local temp_branch="temp-stash-trial-$$"
    git checkout -b "$temp_branch" >/dev/null 2>&1 || {
        print_color "RED" "Failed to create temporary branch for trial"
        return 1
    }
    
    # Try to apply the stash
    if git stash apply "$stash_ref" 2>/dev/null; then
        print_color "GREEN" "Trial application successful - no conflicts expected"
    else
        print_color "RED" "Trial application shows conflicts:"
        local conflicted_files
        readarray -t conflicted_files < <(git diff --name-only --diff-filter=U)
        for file in "${conflicted_files[@]}"; do
            if [[ -n "$file" ]]; then
                echo "  - $file"
            fi
        done
    fi
    
    # Return to original branch and clean up
    local original_branch=$(git rev-parse --abbrev-ref HEAD | sed "s/$temp_branch//g" | sed "s/^[^a-zA-Z0-9]*//" | cut -d' ' -f1)
    git checkout - >/dev/null 2>&1
    git branch -D "$temp_branch" >/dev/null 2>&1 || true
}

# Main execution
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <stash_ref> [options]"
    echo "Example: $0 stash@{0}"
    echo ""
    echo "Options:"
    echo "  --preview, -p    Show stash info and trial application before proceeding"
    echo ""
    echo "This script provides advanced interactive conflict resolution when applying git stashes."
    echo "It allows you to choose how to handle each conflict with multiple resolution strategies."
    exit 1
fi

STASH_REF="$1"
PREVIEW_MODE=false

# Check for preview option
if [[ "$2" == "--preview" ]] || [[ "$2" == "-p" ]]; then
    PREVIEW_MODE=true
fi

# Show stash info
show_stash_info "$STASH_REF"

if [[ "$PREVIEW_MODE" == true ]]; then
    trial_apply "$STASH_REF"
    print_color "YELLOW" "Preview completed. Would you like to proceed with interactive application? (y/N)"
    read -r confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Operation cancelled."
        exit 0
    fi
fi

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