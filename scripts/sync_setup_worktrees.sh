#!/bin/bash
# Script to update all local worktrees with the latest orchestration tools and setup files.
# This script should be part of the 'orchestration-tools' branch.

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to print usage
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Update all local worktrees with the latest orchestration tools and setup files."
    echo ""
    echo "Options:"
    echo "  --help, -h     Show this help message"
    echo "  --dry-run      (Not fully implemented for git pull, but can show worktrees)"
    echo "  --verbose, -v  Enable verbose output"
}

# Function to update all local worktrees
update_all_worktrees() {
    local dry_run=false
    local verbose=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                print_usage
                exit 0
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --verbose|-v)
                verbose=true
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                print_usage
                exit 1
                ;;
        esac
    done
    
    local REPO_ROOT=$(git rev-parse --show-toplevel)
    if [[ -z "$REPO_ROOT" ]]; then
        echo -e "${RED}Error: Not in a git repository.${NC}"
        exit 1
    fi

    echo -e "${BLUE}Updating all local worktrees from remote 'orchestration-tools' branch...${NC}"
    
    local worktree_list=$(git worktree list --porcelain | grep 'worktree ' | cut -d' ' -f2)
    local updated_count=0
    local skipped_count=0

    if [[ -z "$worktree_list" ]]; then
        echo -e "${YELLOW}No additional worktrees found.${NC}"
        exit 0
    fi

    for worktree_path in $worktree_list;
    do
        local worktree_name=$(basename "$worktree_path")
        echo -e "${BLUE}Processing worktree: $worktree_name (${worktree_path})${NC}"

        if [[ "$dry_run" == true ]]; then
            echo -e "${BLUE}[DRY RUN] Would perform 'git pull' in $worktree_name${NC}"
            ((skipped_count++))
            continue
        fi

        # Navigate into the worktree and perform git pull
        (cd "$worktree_path" && git pull)
        local pull_status=$?

        if [[ $pull_status -eq 0 ]]; then
            echo -e "${GREEN}Successfully pulled in $worktree_name. Post-merge hook should have updated tools/setup files.${NC}"
            ((updated_count++))
        else
            echo -e "${RED}Failed to pull in $worktree_name. Please check for conflicts or uncommitted changes.${NC}"
            ((skipped_count++))
        fi

        if [[ "$verbose" == true ]]; then
            echo -e "${BLUE}--- End of processing for $worktree_name ---${NC}"
        fi
    done
    
    echo -e "${GREEN}Update process complete!${NC}"
    echo -e "${GREEN}Worktrees updated: $updated_count${NC}"
    echo -e "${BLUE}Worktrees skipped/failed: $skipped_count${NC}"
}

# Run the update function with all arguments
update_all_worktrees "$@"