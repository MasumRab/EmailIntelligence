#!/bin/bash
# Script to synchronize setup files between worktrees

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to print usage
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Synchronize setup files between worktrees"
    echo ""
    echo "Options:"
    echo "  --help, -h     Show this help message"
    echo "  --dry-run      Show what would be synchronized without making changes"
    echo "  --verbose, -v  Enable verbose output"
    echo ""
    echo "Examples:"
    echo "  $0                 # Synchronize setup files"
    echo "  $0 --dry-run       # Show what would be synchronized"
    echo "  $0 --verbose       # Synchronize with verbose output"
}

# Function to sync setup files from launch-setup-fixes to other worktrees
sync_setup_files() {
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
    
    # Check if we're in the right directory
    if [[ ! -d ".git" ]]; then
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    fi
    
    # Check if worktrees directory exists
    if [[ ! -d "worktrees" ]]; then
        echo -e "${YELLOW}Warning: No worktrees directory found${NC}"
        exit 0
    fi
    
    # Check if launch-setup-fixes worktree exists
    if [[ ! -d "worktrees/launch-setup-fixes" ]]; then
        echo -e "${YELLOW}Warning: launch-setup-fixes worktree not found${NC}"
        exit 0
    fi
    
    # Check if setup directory exists in launch-setup-fixes worktree
    if [[ ! -d "worktrees/launch-setup-fixes/setup" ]]; then
        echo -e "${YELLOW}Warning: setup directory not found in launch-setup-fixes worktree${NC}"
        exit 0
    fi
    
    echo -e "${BLUE}Synchronizing setup files...${NC}"
    
    # List of files to synchronize
    local setup_files=(
        ".env.example"
        "launch.bat"
        "launch.py"
        "launch.sh"
        "pyproject.toml"
        "README.md"
        "requirements-dev.txt"
        "requirements.txt"
        "setup_environment_system.sh"
        "setup_environment_wsl.sh"
        "setup_python.sh"
    )
    
    # Counter for synchronized files
    local synced_count=0
    local skipped_count=0
    
    # Synchronize to other worktrees
    for worktree in worktrees/*/; do
        # Skip launch-setup-fixes worktree (source)
        if [[ "$(basename "$worktree")" == "launch-setup-fixes" ]]; then
            continue
        fi
        
        # Skip docs worktrees (docs-main, docs-scientific) as they're for documentation only
        if [[ "$(basename "$worktree")" == "docs-main" ]] || [[ "$(basename "$worktree")" == "docs-scientific" ]]; then
            if [[ "$verbose" == true ]]; then
                echo -e "${BLUE}Skipping docs worktree: $worktree${NC}"
            fi
            continue
        fi
        
        # Skip if not a directory
        if [[ ! -d "$worktree" ]]; then
            continue
        fi
        
        # Create setup directory if it doesn't exist
        if [[ ! -d "$worktree/setup" ]]; then
            if [[ "$dry_run" == false ]]; then
                mkdir -p "$worktree/setup"
                echo -e "${GREEN}Created setup directory in $worktree${NC}"
            else
                echo -e "${BLUE}[DRY RUN] Would create setup directory in $worktree${NC}"
            fi
        fi
        
        # Synchronize each setup file
        for file in "${setup_files[@]}"; do
            local source_file="worktrees/launch-setup-fixes/setup/$file"
            local dest_file="$worktree/setup/$file"
            
            # Check if source file exists
            if [[ ! -f "$source_file" ]]; then
                if [[ "$verbose" == true ]]; then
                    echo -e "${YELLOW}Skipping $file (not found in source)${NC}"
                fi
                continue
            fi
            
            # Check if destination file exists and is different
            local should_copy=true
            if [[ -f "$dest_file" ]]; then
                if cmp -s "$source_file" "$dest_file"; then
                    should_copy=false
                    if [[ "$verbose" == true ]]; then
                        echo -e "${BLUE}Skipping $file (unchanged)${NC}"
                    fi
                fi
            fi
            
            # Copy file if needed
            if [[ "$should_copy" == true ]]; then
                if [[ "$dry_run" == false ]]; then
                    cp "$source_file" "$dest_file"
                    echo -e "${GREEN}Copied $file to $worktree${NC}"
                else
                    echo -e "${BLUE}[DRY RUN] Would copy $file to $worktree${NC}"
                fi
                ((synced_count++))
            else
                ((skipped_count++))
            fi
        done
    done
    
    echo -e "${GREEN}Synchronization complete!${NC}"
    echo -e "${GREEN}Files synchronized: $synced_count${NC}"
    echo -e "${BLUE}Files unchanged: $skipped_count${NC}"
}

# Run the sync function with all arguments
sync_setup_files "$@"