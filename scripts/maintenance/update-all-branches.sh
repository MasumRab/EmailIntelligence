#!/bin/bash

# Update all branches with essential infrastructure scripts from orchestration-tools
# This script propagates install-hooks.sh, validation scripts, and other utilities
# while maintaining branch integrity (no application code or hooks committed)

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load common libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Configuration
DRY_RUN=false
INTERACTIVE=true
SKIP_BRANCHES=()
TARGET_BRANCHES=()
VERBOSE=false

# Scripts to propagate to all branches
SCRIPTS_TO_PROPAGATE=(
    "install-hooks.sh"
    "enable-hooks.sh"
    "disable-hooks.sh"
    "validate-orchestration-context.sh"
    "validate-branch-propagation.sh"
    "extract-orchestration-changes.sh"
    "sync_setup_worktrees.sh"
    "reverse_sync_orchestration.sh"
    "cleanup_orchestration.sh"
    "context-control"
)

# Lib directory to propagate
LIB_DIR="lib"

# Directories to propagate to all branches
DIRS_TO_PROPAGATE=(
    "setup"
    "deployment"
    ".specify"
)

# Documentation files to propagate
DOCS_TO_PROPAGATE=(
    "docs/orchestration-workflow.md"
    "docs/orchestration_summary.md"
    "docs/env_management.md"
    "docs/git_workflow_plan.md"
    "docs/critical_files_check.md"
    "docs/guides/branch_switching_guide.md"
    "docs/guides/workflow_and_review_process.md"
)

# Config files to propagate
CONFIG_FILES_TO_PROPAGATE=(
    "pyproject.toml"
    "requirements.txt"
    "requirements-dev.txt"
    "uv.lock"
    ".gitignore"
    ".gitattributes"
    "launch.py"
)

# Branches to skip (these manage their own versions)
DEFAULT_SKIP_BRANCHES=(
    "HEAD"
    "taskmaster"
)

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --no-interactive)
                INTERACTIVE=false
                shift
                ;;
            --skip)
                IFS=',' read -ra SKIP_BRANCHES <<< "$2"
                shift 2
                ;;
            --branches)
                IFS=',' read -ra TARGET_BRANCHES <<< "$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat << 'HELP'
Usage: update-all-branches.sh [OPTIONS]

Update all branches with essential infrastructure scripts from orchestration-tools

Options:
  --dry-run              Show what would be done without making changes
  --no-interactive       Don't prompt for confirmation
  --skip BRANCH1,BRANCH2 Skip specific branches (comma-separated)
  --branches BRANCH1,BRANCH2 Update only specific branches (comma-separated)
  --verbose              Show detailed output
  --help                 Show this help message

Scripts propagated:
   - install-hooks.sh
   - enable-hooks.sh
   - disable-hooks.sh
   - validate-orchestration-context.sh
   - validate-branch-propagation.sh
   - extract-orchestration-changes.sh
   - sync_setup_worktrees.sh
   - reverse_sync_orchestration.sh
   - cleanup_orchestration.sh
   - context-control
   - scripts/lib/ (all helper libraries)
   - setup/ (launch scripts and environment setup)
   - deployment/ (Docker and deployment configurations)
   - .specify/ (constitution and templates)
   - docs/orchestration*.md (orchestration documentation)
   - pyproject.toml, requirements*.txt, uv.lock (Python configuration)
   - .gitignore, .gitattributes (Git configuration)
   - launch.py (main application launcher)

Branch integrity maintained:
  - No application code changes committed
  - No .git/hooks/ files committed
  - Only infrastructure scripts and lib files
  - Branch policies enforced via pre-commit hook

Examples:
  # Dry run to see what would happen
  ./scripts/update-all-branches.sh --dry-run

  # Update only main and scientific branches
  ./scripts/update-all-branches.sh --branches main,scientific

  # Update all except specific branches
  ./scripts/update-all-branches.sh --skip feature/wip,experimental

  # Auto-confirm all updates (CI/CD use)
  ./scripts/update-all-branches.sh --no-interactive

HELP
}

# Get list of branches to update
get_branches_to_update() {
    local branches
    
    # If specific branches provided, use those
    if [[ ${#TARGET_BRANCHES[@]} -gt 0 ]]; then
        branches=("${TARGET_BRANCHES[@]}")
    else
        # Otherwise get all branches
        branches=($(git branch -r | grep -v HEAD | sed 's|origin/||' | sort -u))
    fi
    
    # Filter out skip list
    local filtered_branches=()
    for branch in "${branches[@]}"; do
        local skip=false
        for skip_branch in "${DEFAULT_SKIP_BRANCHES[@]}" "${SKIP_BRANCHES[@]}"; do
            if [[ "$branch" == "$skip_branch" ]]; then
                skip=true
                break
            fi
        done
        if [[ "$skip" == false ]]; then
            filtered_branches+=("$branch")
        fi
    done
    
    echo "${filtered_branches[@]}"
}

# Verify orchestration-tools has the scripts
verify_source_branch() {
    echo -e "${BLUE}Verifying source branch has all scripts...${NC}"
    
    for script in "${SCRIPTS_TO_PROPAGATE[@]}"; do
        if ! git show "orchestration-tools:scripts/$script" > /dev/null 2>&1; then
            echo -e "${RED}✗ Missing script in orchestration-tools: $script${NC}"
            return 1
        fi
    done
    
    if ! git show "orchestration-tools:scripts/$LIB_DIR/" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Warning: lib/ directory not found in orchestration-tools${NC}"
    fi

    # Verify directories
    for dir in "${DIRS_TO_PROPAGATE[@]}"; do
        if ! git show "orchestration-tools:$dir/" > /dev/null 2>&1; then
            echo -e "${YELLOW}⚠ Warning: $dir/ directory not found in orchestration-tools${NC}"
        fi
    done

    # Verify documentation files
    for doc in "${DOCS_TO_PROPAGATE[@]}"; do
        if ! git show "orchestration-tools:$doc" > /dev/null 2>&1; then
            echo -e "${YELLOW}⚠ Warning: $doc not found in orchestration-tools${NC}"
        fi
    done

    # Verify config files
    for config in "${CONFIG_FILES_TO_PROPAGATE[@]}"; do
        if ! git show "orchestration-tools:$config" > /dev/null 2>&1; then
            echo -e "${YELLOW}⚠ Warning: $config not found in orchestration-tools${NC}"
        fi
    done

    echo -e "${GREEN}✓ All source files verified${NC}"
    return 0
}

# Update a single branch with scripts
update_branch() {
    local branch=$1
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    
    echo -e "${BLUE}Updating branch: $branch${NC}"
    
    # Skip if branch doesn't exist remotely
    if ! git rev-parse --verify "origin/$branch" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Branch not found on remote: $branch${NC}"
        return 0
    fi
    
    # Check out branch
    if [[ "$VERBOSE" == true ]]; then
        echo "  git fetch origin $branch"
        echo "  git checkout $branch"
    fi
    
    if [[ "$DRY_RUN" == false ]]; then
        git fetch origin "$branch" 2>/dev/null || {
            echo -e "${YELLOW}⚠ Failed to fetch $branch${NC}"
            return 0
        }
        git checkout "$branch" 2>/dev/null || {
            echo -e "${YELLOW}⚠ Failed to checkout $branch${NC}"
            return 0
        }
    fi
    
    # Copy scripts from orchestration-tools
    local scripts_updated=0
    for script in "${SCRIPTS_TO_PROPAGATE[@]}"; do
        if [[ "$VERBOSE" == true ]]; then
            echo "  Checking script: $script"
        fi
        
        # Check if script exists on orchestration-tools
        if ! git show "orchestration-tools:scripts/$script" > /dev/null 2>&1; then
            if [[ "$VERBOSE" == true ]]; then
                echo "    Script not in orchestration-tools, skipping"
            fi
            continue
        fi
        
        if [[ "$VERBOSE" == true ]]; then
            echo "  Copying script: $script"
        fi
        
        if [[ "$DRY_RUN" == false ]]; then
            git show "orchestration-tools:scripts/$script" > "scripts/$script"
            chmod +x "scripts/$script"
            git add "scripts/$script"
            scripts_updated=$((scripts_updated + 1))
        else
            echo "    [DRY-RUN] Would update: scripts/$script"
            scripts_updated=$((scripts_updated + 1))
        fi
    done
    
    # Copy lib directory
    if git show "orchestration-tools:scripts/$LIB_DIR/" > /dev/null 2>&1; then
        if [[ "$VERBOSE" == true ]]; then
            echo "  Syncing lib/ directory"
        fi

        if [[ "$DRY_RUN" == false ]]; then
            # Get list of files in lib from orchestration-tools
            local lib_files=$(git ls-tree -r --name-only "orchestration-tools:scripts/$LIB_DIR" 2>/dev/null || echo "")

            for lib_file in $lib_files; do
                local relative_file="${lib_file#scripts/}"
                git show "orchestration-tools:$lib_file" > "$relative_file"
                chmod +x "$relative_file"
                git add "$relative_file"
                scripts_updated=$((scripts_updated + 1))
            done
        fi
    fi

    # Copy directories
    for dir in "${DIRS_TO_PROPAGATE[@]}"; do
        if git show "orchestration-tools:$dir/" > /dev/null 2>&1; then
            if [[ "$VERBOSE" == true ]]; then
                echo "  Syncing $dir/ directory"
            fi

            if [[ "$DRY_RUN" == false ]]; then
                # Get list of files in directory from orchestration-tools
                local dir_files=$(git ls-tree -r --name-only "orchestration-tools:$dir" 2>/dev/null || echo "")

                for dir_file in $dir_files; do
                    git show "orchestration-tools:$dir_file" > "$dir_file"
                    # Make scripts executable if they are in scripts/
                    if [[ "$dir_file" == scripts/* ]]; then
                        chmod +x "$dir_file"
                    fi
                    git add "$dir_file"
                    scripts_updated=$((scripts_updated + 1))
                done
            else
                echo "    [DRY-RUN] Would sync: $dir/"
            fi
        fi
    done

    # Copy documentation files
    for doc in "${DOCS_TO_PROPAGATE[@]}"; do
        if git show "orchestration-tools:$doc" > /dev/null 2>&1; then
            if [[ "$VERBOSE" == true ]]; then
                echo "  Syncing doc: $doc"
            fi

            if [[ "$DRY_RUN" == false ]]; then
                git show "orchestration-tools:$doc" > "$doc"
                git add "$doc"
                scripts_updated=$((scripts_updated + 1))
            else
                echo "    [DRY-RUN] Would update: $doc"
            fi
        fi
    done

    # Copy config files
    for config in "${CONFIG_FILES_TO_PROPAGATE[@]}"; do
        if git show "orchestration-tools:$config" > /dev/null 2>&1; then
            if [[ "$VERBOSE" == true ]]; then
                echo "  Syncing config: $config"
            fi

            if [[ "$DRY_RUN" == false ]]; then
                git show "orchestration-tools:$config" > "$config"
                # Make executable if it's a script
                if [[ "$config" == *.py ]] || [[ "$config" == *.sh ]]; then
                    chmod +x "$config"
                fi
                git add "$config"
                scripts_updated=$((scripts_updated + 1))
            else
                echo "    [DRY-RUN] Would update: $config"
            fi
        fi
    done
    
    # Check if anything was updated
    if [[ $scripts_updated -eq 0 ]]; then
        echo -e "${YELLOW}  ⚠ No scripts to update on $branch${NC}"
        return 0
    fi
    
    # Commit changes
    if [[ "$DRY_RUN" == false ]]; then
        # Check if there are staged changes
        if git diff --cached --quiet; then
            echo -e "${YELLOW}  ⚠ No changes to commit on $branch${NC}"
            return 0
        fi
        
        echo "  Committing changes..."
        git commit -m "chore: sync infrastructure scripts from orchestration-tools

- Update install-hooks.sh, enable-hooks.sh, disable-hooks.sh
- Update validate-orchestration-context.sh
- Update validate-branch-propagation.sh
- Update extract-orchestration-changes.sh
- Sync scripts/lib/ helper libraries
- Maintain branch propagation integrity" 2>/dev/null || {
            echo -e "${YELLOW}  ⚠ Commit failed (may be no changes): $branch${NC}"
            return 0
        }
        
        # Push changes
        echo "  Pushing to origin/$branch..."
        git push origin "$branch" 2>/dev/null || {
            echo -e "${RED}✗ Failed to push $branch${NC}"
            return 1
        }
        
        echo -e "${GREEN}✓ Updated: $branch${NC}"
    else
        echo -e "${GREEN}✓ [DRY-RUN] Would update: $branch ($scripts_updated files)${NC}"
    fi
    
    return 0
}

# Main update process
main() {
    parse_args "$@"
    
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         Updating All Branches with Infrastructure Scripts    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Verify we're in a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    fi
    
    # Verify source branch
    if ! verify_source_branch; then
        echo -e "${RED}Error: Cannot proceed without source scripts${NC}"
        exit 1
    fi
    echo ""
    
    # Get branches to update
    local branches_to_update=($(get_branches_to_update))
    
    if [[ ${#branches_to_update[@]} -eq 0 ]]; then
        echo -e "${YELLOW}No branches to update${NC}"
        exit 0
    fi
    
    echo -e "${BLUE}Branches to update (${#branches_to_update[@]}):${NC}"
    printf '  %s\n' "${branches_to_update[@]}"
    echo ""
    
    # Show scripts that will be propagated
    echo -e "${BLUE}Scripts to propagate:${NC}"
    printf '  - %s\n' "${SCRIPTS_TO_PROPAGATE[@]}"
    echo "  - scripts/lib/ (all files)"
    echo ""
    
    # Show dry-run notice
    if [[ "$DRY_RUN" == true ]]; then
        echo -e "${YELLOW}DRY-RUN MODE: No changes will be made${NC}"
        echo ""
    fi
    
    # Prompt for confirmation
    if [[ "$INTERACTIVE" == true && "$DRY_RUN" == false ]]; then
        read -p "Proceed with updating branches? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Cancelled${NC}"
            exit 0
        fi
    fi
    
    echo -e "${BLUE}Starting update process...${NC}"
    echo ""
    
    # Update each branch
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    local failed_branches=()
    local updated_branches=()
    
    for branch in "${branches_to_update[@]}"; do
        if update_branch "$branch"; then
            updated_branches+=("$branch")
        else
            failed_branches+=("$branch")
        fi
    done
    
    # Return to original branch
    echo ""
    echo "Returning to original branch: $current_branch"
    git checkout "$current_branch" 2>/dev/null || git checkout main 2>/dev/null
    
    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Update Summary${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    
    if [[ "$DRY_RUN" == true ]]; then
        echo -e "${YELLOW}DRY-RUN: No actual changes were made${NC}"
    fi
    
    echo "Updated branches: ${#updated_branches[@]}"
    if [[ ${#updated_branches[@]} -gt 0 ]]; then
        printf '  ✓ %s\n' "${updated_branches[@]}"
    fi
    
    if [[ ${#failed_branches[@]} -gt 0 ]]; then
        echo "Failed branches: ${#failed_branches[@]}"
        printf '  ✗ %s\n' "${failed_branches[@]}"
    fi
    
    echo ""
    
    if [[ ${#failed_branches[@]} -eq 0 ]]; then
        echo -e "${GREEN}✓ All branches updated successfully${NC}"
        exit 0
    else
        echo -e "${RED}✗ Some branches failed to update${NC}"
        exit 1
    fi
}

# Run main function
main "$@"
