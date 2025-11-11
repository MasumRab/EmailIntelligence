#!/bin/bash

# Stash management tools for orchestration workflow
# Provides utilities for managing git stashes during branch switching

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

# Source common utilities
source "$SCRIPT_DIR/lib/common.sh" 2>/dev/null || {
    # If common.sh doesn't exist yet, define basic functions
    log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
    log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
    log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
}

# Configuration
STASH_MESSAGE="auto-stash-$(date +%Y%m%d-%H%M%S)"

show_help() {
    cat << 'HELP'
Usage: stash_tools.sh [COMMAND] [OPTIONS]

Stash management tools for orchestration workflow

Commands:
  save, push     Create a stash of current changes (tracked and untracked files)
  pop            Apply and remove the latest stash
  apply          Apply the latest stash without removing it
  list           Show all stashes
  clear          Remove all stashes
  branch-switch  Stash changes, switch to branch, then pop stash
  clean          Clean untracked files (like git clean -fd)

Examples:
  # Stash all changes with a timestamp
  ./scripts/stash_tools.sh save

  # Apply latest stash
  ./scripts/stash_tools.sh pop

  # Stash changes and switch to main branch
  ./scripts/stash_tools.sh branch-switch main

  # Clean untracked files
  ./scripts/stash_tools.sh clean

HELP
}

# Check if there's anything to stash
check_working_directory() {
    local has_changes=false
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        has_changes=true
    fi
    
    # Check for untracked files
    if [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
        has_changes=true
    fi
    
    echo "$has_changes"
}

# Save/backup current changes
stash_save() {
    local include_untracked=false
    local message="$STASH_MESSAGE"
    
    # Parse options
    while [[ $# -gt 0 ]]; do
        case $1 in
            --include-untracked)
                include_untracked=true
                shift
                ;;
            --message)
                message="$2"
                shift 2
                ;;
            --help)
                echo "Usage: stash_tools.sh save [--include-untracked] [--message MESSAGE]"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    local has_changes=$(check_working_directory)
    
    if [[ "$has_changes" == "false" ]]; then
        log_info "No changes to stash"
        return 0
    fi
    
    if [[ "$include_untracked" == true ]]; then
        log_info "Stashing changes (including untracked files)..."
        git stash push --include-untracked -m "$message"
    else
        log_info "Stashing changes (tracked files only)..."
        git stash push -m "$message"
    fi
    
    log_info "Changes stashed successfully"
}

# Pop latest stash
stash_pop() {
    if [[ -z "$(git stash list)" ]]; then
        log_warn "No stashes available to pop"
        return 0
    fi
    
    log_info "Popping latest stash..."
    git stash pop
    
    if [[ $? -ne 0 ]]; then
        log_error "Conflict occurred during stash pop. Please resolve manually."
        log_info "Current stashes:"
        git stash list
        exit 1
    fi
    
    log_info "Latest stash applied and removed"
}

# Apply latest stash without removing it
stash_apply() {
    if [[ -z "$(git stash list)" ]]; then
        log_warn "No stashes available to apply"
        return 0
    fi
    
    log_info "Applying latest stash..."
    git stash apply
    
    if [[ $? -ne 0 ]]; then
        log_error "Conflict occurred during stash apply. Please resolve manually."
        log_info "Current stashes:"
        git stash list
        exit 1
    fi
    
    log_info "Latest stash applied"
}

# List all stashes
stash_list() {
    if [[ -z "$(git stash list)" ]]; then
        log_info "No stashes found"
        return 0
    fi
    
    log_info "Stash list:"
    git stash list
}

# Clear all stashes
stash_clear() {
    if [[ -z "$(git stash list)" ]]; then
        log_info "No stashes to clear"
        return 0
    fi
    
    log_info "Current stashes:"
    git stash list
    echo ""
    
    read -p "Clear all stashes? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cancelled"
        return 0
    fi
    
    git stash clear
    log_info "All stashes cleared"
}

# Branch switch with stash
stash_branch_switch() {
    local target_branch="$1"
    
    if [[ -z "$target_branch" ]]; then
        log_error "Target branch not specified"
        echo "Usage: stash_tools.sh branch-switch BRANCH_NAME"
        exit 1
    fi
    
    local has_changes=$(check_working_directory)
    
    if [[ "$has_changes" == "true" ]]; then
        log_info "Stashing changes before branch switch..."
        git stash push --include-untracked -m "auto-stash-before-switch-$target_branch-$(date +%Y%m%d-%H%M%S)"
    else
        log_info "No changes to stash"
    fi
    
    log_info "Switching to branch: $target_branch"
    git checkout "$target_branch"
    
    # Check if stash exists before trying to pop
    if [[ -n "$(git stash list | head -n1)" && "$has_changes" == "true" ]]; then
        log_info "Applying stashed changes..."
        git stash pop
    fi
    
    log_info "Successfully switched to branch: $target_branch"
}

# Clean untracked files
clean_untracked() {
    log_info "Untracked files and directories:"
    git ls-files --others --exclude-standard
    git clean -nd
    
    echo ""
    read -p "Clean untracked files and directories? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cancelled"
        return 0
    fi
    
    git clean -fd
    log_info "Untracked files and directories cleaned"
}

# Main execution
main() {
    local command="${1:-help}"
    
    case "$command" in
        save|push)
            shift
            stash_save "$@"
            ;;
        pop)
            stash_pop
            ;;
        apply)
            stash_apply
            ;;
        list)
            stash_list
            ;;
        clear)
            stash_clear
            ;;
        branch-switch)
            shift
            stash_branch_switch "$1"
            ;;
        clean)
            clean_untracked
            ;;
        help|--help)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"