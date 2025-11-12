#!/bin/bash
# Enhanced Stash Management Tool with Interactive Conflict Resolution
# This script provides comprehensive stash management capabilities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo "Enhanced Stash Management Tool"
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
    echo "  help                    Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 show stash@{0}"
    echo "  $0 apply-interactive stash@{0}"
    echo "  $0 process-all"
}

# Function to list all stashes
list_stashes() {
    echo -e "${BLUE}Current stashes:${NC}"
    git stash list
}

# Function to show stash details
show_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        echo -e "${RED}Error: Stash reference required${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Stash details for $stash_ref:${NC}"
    git stash show -p "$stash_ref"
}

# Function to apply stash non-interactively
apply_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        echo -e "${RED}Error: Stash reference required${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Applying stash $stash_ref...${NC}"
    if git stash apply "$stash_ref"; then
        echo -e "${GREEN}Stash applied successfully${NC}"
        return 0
    else
        echo -e "${RED}Failed to apply stash (conflicts detected)${NC}"
        return 1
    fi
}

# Function to apply stash with interactive conflict resolution
apply_stash_interactive() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        echo -e "${RED}Error: Stash reference required${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Applying stash $stash_ref with interactive conflict resolution...${NC}"
    
    # Check if interactive resolver exists
    if [[ -f "/home/masum/github/EmailIntelligence/scripts/interactive_stash_resolver.sh" ]]; then
        /home/masum/github/EmailIntelligence/scripts/interactive_stash_resolver.sh "$stash_ref"
        return $?
    else
        echo -e "${YELLOW}Interactive resolver not found, falling back to standard apply...${NC}"
        apply_stash "$stash_ref"
        return $?
    fi
}

# Function to pop stash non-interactively
pop_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        echo -e "${RED}Error: Stash reference required${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Popping stash $stash_ref...${NC}"
    if git stash pop "$stash_ref"; then
        echo -e "${GREEN}Stash popped successfully${NC}"
        return 0
    else
        echo -e "${RED}Failed to pop stash (conflicts detected)${NC}"
        return 1
    fi
}

# Function to pop stash with interactive conflict resolution
pop_stash_interactive() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        echo -e "${RED}Error: Stash reference required${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Popping stash $stash_ref with interactive conflict resolution...${NC}"
    
    # Apply with interactive resolution
    if apply_stash_interactive "$stash_ref"; then
        # Drop the stash after successful application
        echo -e "${BLUE}Dropping stash $stash_ref...${NC}"
        git stash drop "$stash_ref"
        echo -e "${GREEN}Stash popped successfully${NC}"
        return 0
    else
        echo -e "${RED}Failed to apply stash, not dropping${NC}"
        return 1
    fi
}

# Function to save current changes to stash
save_stash() {
    local message="$1"
    if [[ -z "$message" ]]; then
        echo -e "${BLUE}Saving current changes to stash...${NC}"
        git stash save
    else
        echo -e "${BLUE}Saving current changes to stash with message: $message${NC}"
        git stash save "$message"
    fi
    
    echo -e "${GREEN}Changes saved to stash${NC}"
}

# Function to drop a stash
drop_stash() {
    local stash_ref="$1"
    if [[ -z "$stash_ref" ]]; then
        echo -e "${RED}Error: Stash reference required${NC}"
        return 1
    fi
    
    echo -e "${YELLOW}Are you sure you want to drop $stash_ref? (y/N)${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        git stash drop "$stash_ref"
        echo -e "${GREEN}Stash dropped${NC}"
    else
        echo -e "${BLUE}Operation cancelled${NC}"
    fi
}

# Function to clear all stashes
clear_stashes() {
    echo -e "${YELLOW}Are you sure you want to clear all stashes? (y/N)${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        git stash clear
        echo -e "${GREEN}All stashes cleared${NC}"
    else
        echo -e "${BLUE}Operation cancelled${NC}"
    fi
}

# Function to analyze stashes and suggest processing order
analyze_stashes() {
    echo -e "${BLUE}Analyzing stashes...${NC}"
    
    if [[ $(git stash list | wc -l) -eq 0 ]]; then
        echo -e "${GREEN}No stashes found${NC}"
        return 0
    fi
    
    echo -e "${BLUE}Stash Analysis:${NC}"
    git stash list | while read -r line; do
        stash_ref=$(echo "$line" | cut -d: -f1)
        branch_info=$(echo "$line" | cut -d: -f3-)
        echo "  $stash_ref: $branch_info"
    done
    
    echo ""
    echo -e "${YELLOW}Suggested processing order:${NC}"
    echo "  1. Stashes on main development branches (orchestration-tools, main)"
    echo "  2. Stashes on feature branches"
    echo "  3. Stashes on experimental or temporary branches"
    echo ""
    echo -e "${BLUE}Recommendation: Use 'apply-interactive' for each stash to handle conflicts properly${NC}"
}

# Function to process all stashes interactively
process_all_stashes() {
    echo -e "${BLUE}Processing all stashes with interactive conflict resolution...${NC}"
    
    if [[ $(git stash list | wc -l) -eq 0 ]]; then
        echo -e "${GREEN}No stashes found${NC}"
        return 0
    fi
    
    # Get list of stashes
    stashes=($(git stash list | cut -d: -f1))
    
    echo -e "${BLUE}Found ${#stashes[@]} stashes to process${NC}"
    
    for stash in "${stashes[@]}"; do
        echo -e "${BLUE}Processing $stash...${NC}"
        echo ""
        
        # Show stash details
        show_stash "$stash"
        echo ""
        
        # Ask user how to proceed
        echo -e "${YELLOW}How would you like to process this stash?${NC}"
        echo "1) Apply interactively (resolve conflicts)"
        echo "2) Skip this stash"
        echo "3) Stop processing"
        echo -n "Enter your choice (1-3): "
        
        read -r choice
        
        case $choice in
            1)
                if apply_stash_interactive "$stash"; then
                    echo -e "${GREEN}Stash applied successfully${NC}"
                    echo -e "${YELLOW}Drop this stash? (y/N)${NC}"
                    read -r drop_confirm
                    if [[ "$drop_confirm" =~ ^[Yy]$ ]]; then
                        git stash drop "$stash"
                        echo -e "${GREEN}Stash dropped${NC}"
                    fi
                else
                    echo -e "${RED}Failed to apply stash${NC}"
                fi
                ;;
            2)
                echo -e "${BLUE}Skipping $stash${NC}"
                ;;
            3)
                echo -e "${BLUE}Stopping stash processing${NC}"
                break
                ;;
            *)
                echo -e "${RED}Invalid choice, skipping $stash${NC}"
                ;;
        esac
        
        echo ""
    done
    
    echo -e "${GREEN}Stash processing complete${NC}"
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
        drop)
            drop_stash "$2"
            ;;
        clear)
            clear_stashes
            ;;
        analyze)
            analyze_stashes
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
            echo -e "${RED}Unknown command: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"