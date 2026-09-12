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
    
    # Check if orchestration-tools branch exists
    if ! git show-ref --verify --quiet refs/heads/orchestration-tools; then
    echo -e "${YELLOW}Warning: orchestration-tools branch not found${NC}"
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

    # Shared configuration files to synchronize (excluding environment-specific ones)
    local config_files=(
    ".flake8"
    ".pylintrc"
    "tsconfig.json"
    "package.json"
    "tailwind.config.ts"
    "vite.config.ts"
    "drizzle.config.ts"
    "components.json"
    ".gitignore"
    ".gitattributes"
    )

    # Launch system architecture files (part of setup since launch.py depends on them)
    local launch_files=(
    "src/core/commands/command_factory.py"
    "src/core/commands/command_interface.py"
    "src/core/commands/setup_command.py"
    "src/core/commands/run_command.py"
    "src/core/commands/test_command.py"
    "src/core/commands/__init__.py"
    "src/core/container.py"
    )
    # Note: package-lock.json excluded as it's environment-specific
    
    # Counter for synchronized files
    local synced_count=0
    local skipped_count=0
    
    # Synchronize to other worktrees
    # Check for temporary worktrees only (no persistent worktrees)
    # Orchestration sync happens through post-merge hooks in worktrees
    # This script is for manual bulk operations when needed
    for worktree_dir in "/tmp"; do
    if [[ -d "$worktree_dir" ]]; then
    for worktree in "$worktree_dir"/*/; do
    # Only process temporary worktrees (not orchestration-tools)
    worktree_base=$(basename "$worktree")
    if [[ "$worktree_base" == orchestration-tools* ]] || [[ ! -d "$worktree/.git" ]]; then
                    continue
                fi
    # Skip if not a directory
    if [[ ! -d "$worktree" ]]; then
    continue
    fi

    local worktree_name="$(basename "$worktree")"

    # Skip docs worktrees (docs-main, docs-scientific) as they're for documentation only
    if [[ "$worktree_name" == "docs-main" ]] || [[ "$worktree_name" == "docs-scientific" ]]; then
    if [[ "$verbose" == true ]]; then
    echo -e "${BLUE}Skipping docs worktree: $worktree${NC}"
    fi
    continue
    fi

        # Skip template/config directories
        if [[ "$worktree_name" == "main" ]] || [[ "$worktree_name" == "scientific" ]]; then
            # Only skip if it's in the local worktrees/ directory (templates)
            if [[ "$worktree_dir" == "worktrees" ]]; then
                if [[ "$verbose" == true ]]; then
                    echo -e "${BLUE}Skipping template directory: $worktree${NC}"
                fi
                continue
            fi
        fi

    echo -e "${BLUE}Synchronizing to worktree: $worktree_name${NC}"

    # Change to worktree directory
    if [[ "$dry_run" == false ]]; then
        cd "$worktree" || continue
    fi

    # Synchronize setup files
    for file in "${setup_files[@]}"; do
        local source_path="setup/$file"

        # Check if source file exists in orchestration-tools
        if ! git cat-file -e "orchestration-tools:$source_path" 2>/dev/null; then
        if [[ "$verbose" == true ]]; then
        echo -e "${YELLOW}Skipping setup/$file (not found in orchestration-tools)${NC}"
            fi
            continue
            fi

            # Check if destination file exists and is different
            local should_sync=true
            if [[ -f "$source_path" ]]; then
                # Compare with orchestration-tools version
                if git cat-file -p "orchestration-tools:$source_path" | cmp -s - "$source_path"; then
            should_sync=false
            if [[ "$verbose" == true ]]; then
            echo -e "${BLUE}Skipping setup/$file (unchanged)${NC}"
            fi
            fi
            fi

            # Sync file if needed
            if [[ "$should_sync" == true ]]; then
                if [[ "$dry_run" == false ]]; then
                git checkout orchestration-tools -- "$source_path" 2>/dev/null || {
            echo -e "${YELLOW}Failed to checkout setup/$file${NC}"
            continue
            }
            echo -e "${GREEN}Updated setup/$file in $worktree${NC}"
                else
                    echo -e "${BLUE}[DRY RUN] Would update setup/$file in $worktree${NC}"
                fi
                ((synced_count++))
            else
                ((skipped_count++))
            fi
        done

        # Synchronize shared config files
        for file in "${config_files[@]}"; do
            # Check if source file exists in orchestration-tools
            if ! git cat-file -e "orchestration-tools:$file" 2>/dev/null; then
                if [[ "$verbose" == true ]]; then
                    echo -e "${YELLOW}Skipping $file (not found in orchestration-tools)${NC}"
                fi
                continue
            fi

            # Check if destination file exists and is different
            local should_sync=true
            if [[ -f "$file" ]]; then
                # Compare with orchestration-tools version
                if git cat-file -p "orchestration-tools:$file" | cmp -s - "$file"; then
                    should_sync=false
                    if [[ "$verbose" == true ]]; then
                        echo -e "${BLUE}Skipping $file (unchanged)${NC}"
                    fi
                fi
            fi

            # Sync file if needed
            if [[ "$should_sync" == true ]]; then
                if [[ "$dry_run" == false ]]; then
                    git checkout orchestration-tools -- "$file" 2>/dev/null || {
                        echo -e "${YELLOW}Failed to checkout $file${NC}"
                        continue
                    }
                    echo -e "${GREEN}Updated $file in $worktree${NC}"
                else
                    echo -e "${BLUE}[DRY RUN] Would update $file in $worktree${NC}"
                fi
                ((synced_count++))
            else
                ((skipped_count++))
            fi
        done

        # Synchronize launch system architecture files
        for file in "${launch_files[@]}"; do
            # Check if source file exists in orchestration-tools
            if ! git cat-file -e "orchestration-tools:$file" 2>/dev/null; then
                if [[ "$verbose" == true ]]; then
                    echo -e "${YELLOW}Skipping $file (not found in orchestration-tools)${NC}"
                fi
                continue
            fi

            # Check if destination file exists and is different
            local should_sync=true
            if [[ -f "$file" ]]; then
                # Compare with orchestration-tools version
                if git cat-file -p "orchestration-tools:$file" | cmp -s - "$file"; then
                    should_sync=false
                    if [[ "$verbose" == true ]]; then
                        echo -e "${BLUE}Skipping $file (unchanged)${NC}"
                    fi
                fi
            fi

            # Sync file if needed
            if [[ "$should_sync" == true ]]; then
                if [[ "$dry_run" == false ]]; then
                    git checkout orchestration-tools -- "$file" 2>/dev/null || {
                        echo -e "${YELLOW}Failed to checkout $file${NC}"
                        continue
                    }
                    echo -e "${GREEN}Updated $file in $worktree${NC}"
                else
                    echo -e "${BLUE}[DRY RUN] Would update $file in $worktree${NC}"
                fi
                ((synced_count++))
            else
                ((skipped_count++))
            fi
        done

    # Return to original directory
        if [[ "$dry_run" == false ]]; then
    cd - >/dev/null || continue
    fi
            done
        fi
    done
    
    echo -e "${GREEN}Synchronization complete!${NC}"
    echo -e "${GREEN}Files synchronized: $synced_count${NC}"
    echo -e "${BLUE}Files unchanged: $skipped_count${NC}"
}

# Run the sync function with all arguments
sync_setup_files "$@"