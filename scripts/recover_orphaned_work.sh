#!/bin/bash

# Recover Orphaned Work Script
# ============================
# This script helps recover work that was lost when switching branches with uncommitted
# orchestration-managed file changes. It provides several recovery mechanisms:
#
# 1. Stash Recovery: Find and recover git stashes
# 2. Git Reflog: Recover uncommitted changes from recent commits
# 3. Orphaned Branches: List branches that may contain orphaned work
# 4. WIP Detection: Find WIP branches or commits with uncommitted changes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ORCHESTRATION_MANAGED_FILES=(
    "setup/"
    "deployment/"
    "scripts/"
    ".flake8"
    ".pylintrc"
    ".gitignore"
    ".gitattributes"
    "pyproject.toml"
    "requirements.txt"
    "launch.py"
    "launch.sh"
)

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================================================
# FUNCTION: Show stashes
# ============================================================================
show_stashes() {
    local count
    count=$(git stash list 2>/dev/null | wc -l)
    
    if [[ $count -eq 0 ]]; then
        log_info "No stashes found"
        return 0
    fi
    
    log_warn "Found $count stash(es):"
    git stash list
    echo ""
}

# ============================================================================
# FUNCTION: Recover from stash
# ============================================================================
recover_from_stash() {
    local stash_index=$1
    
    if [[ -z "$stash_index" ]]; then
        log_error "Stash index required (e.g., 0 for stash@{0})"
        return 1
    fi
    
    log_info "Recovering from stash@{$stash_index}..."
    
    if ! git stash show "stash@{$stash_index}" > /dev/null 2>&1; then
        log_error "Stash stash@{$stash_index} not found"
        return 1
    fi
    
    # Show what will be recovered
    log_info "Files in this stash:"
    git stash show -p "stash@{$stash_index}" | grep "^diff --git" | sed 's/diff --git a\//  - /; s/ b.*//'
    
    read -p "Apply this stash? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if git stash apply "stash@{$stash_index}"; then
            log_success "Stash recovered. You may want to commit or continue editing."
            return 0
        else
            log_error "Failed to apply stash"
            return 1
        fi
    else
        log_warn "Recovery cancelled"
        return 1
    fi
}

# ============================================================================
# FUNCTION: Check reflog for uncommitted changes
# ============================================================================
check_reflog() {
    local branch=${1:-HEAD}
    
    log_info "Checking reflog for recent changes on $branch..."
    echo ""
    
    git reflog show "$branch" --pretty=format:"%h %gd: %gs" -n 20 | while read -r line; do
        echo "  $line"
    done
    
    echo ""
}

# ============================================================================
# FUNCTION: Find orphaned branches
# ============================================================================
find_orphaned_branches() {
    log_info "Searching for orphaned or stale branches..."
    echo ""
    
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD)
    
    # Find branches modified recently but not on main
    git branch -a --sort=-committerdate --format="%(refname:short) %(committerdate:short) %(subject)" | while read -r branch date subject; do
        # Skip current branch and remote tracking branches
        [[ "$branch" == "$current_branch" ]] && continue
        [[ "$branch" == *"/HEAD"* ]] && continue
        
        # Check if branch contains orchestration-managed file changes
        if git diff main..."$branch" --name-only 2>/dev/null | grep -q -E "$(IFS=|; echo "${ORCHESTRATION_MANAGED_FILES[*]}")"; then
            echo "  $branch ($date): $subject"
        fi
    done | head -20
    
    echo ""
}

# ============================================================================
# FUNCTION: Create patch from uncommitted changes
# ============================================================================
create_patch_from_changes() {
    local output_file=${1:-"orphaned_changes.patch"}
    
    if ! git diff --quiet 2>/dev/null && ! git diff --cached --quiet 2>/dev/null; then
        log_info "Creating patch of uncommitted changes..."
        
        # Stage all changes
        git diff --binary > "$output_file"
        
        if [[ -s "$output_file" ]]; then
            log_success "Patch created: $output_file"
            log_info "To apply this patch: git apply $output_file"
            return 0
        else
            log_warn "No changes to patch"
            rm "$output_file"
            return 1
        fi
    else
        log_info "No uncommitted changes to patch"
        return 0
    fi
}

# ============================================================================
# FUNCTION: Find work-in-progress commits
# ============================================================================
find_wip_commits() {
    log_info "Searching for WIP (Work In Progress) commits..."
    echo ""
    
    git log --oneline --grep="WIP\|TODO\|FIXME\|Draft" -n 20 2>/dev/null | while read -r commit message; do
        echo "  $commit: $message"
    done
    
    echo ""
}

# ============================================================================
# FUNCTION: Detect uncommitted changes by checking current status
# ============================================================================
check_uncommitted_changes() {
    log_info "Checking current working directory for uncommitted changes..."
    echo ""
    
    if git diff --quiet && git diff --cached --quiet; then
        log_success "Working directory is clean"
        return 0
    fi
    
    if ! git diff --quiet; then
        log_warn "Unstaged changes:"
        git diff --name-only | sed 's/^/  - /'
        echo ""
    fi
    
    if ! git diff --cached --quiet; then
        log_warn "Staged changes:"
        git diff --cached --name-only | sed 's/^/  + /'
        echo ""
    fi
    
    return 0
}

# ============================================================================
# FUNCTION: Restore from specific commit
# ============================================================================
restore_from_commit() {
    local commit_hash=$1
    local file_pattern=${2:-""}
    
    if [[ -z "$commit_hash" ]]; then
        log_error "Commit hash required"
        return 1
    fi
    
    log_info "Restoring from commit: $commit_hash"
    
    # Show what will be restored
    if [[ -n "$file_pattern" ]]; then
        log_info "Files matching pattern '$file_pattern':"
        git diff "$commit_hash"^.."$commit_hash" --name-only | grep "$file_pattern" | sed 's/^/  - /'
    else
        log_info "Files in this commit:"
        git diff "$commit_hash"^.."$commit_hash" --name-only | sed 's/^/  - /'
    fi
    
    echo ""
    read -p "Restore these files? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ -n "$file_pattern" ]]; then
            git checkout "$commit_hash"^ -- $(git diff "$commit_hash"^.."$commit_hash" --name-only | grep "$file_pattern")
        else
            git checkout "$commit_hash"^ -- $(git diff "$commit_hash"^.."$commit_hash" --name-only)
        fi
        log_success "Files restored"
        return 0
    else
        log_warn "Restore cancelled"
        return 1
    fi
}

# ============================================================================
# FUNCTION: Full recovery scan
# ============================================================================
full_recovery_scan() {
    log_info "========================================="
    log_info "FULL ORPHANED WORK RECOVERY SCAN"
    log_info "========================================="
    echo ""
    
    log_info "1. Checking current status..."
    check_uncommitted_changes
    echo ""
    
    log_info "2. Checking for stashes..."
    show_stashes
    echo ""
    
    log_info "3. Checking reflog..."
    check_reflog
    echo ""
    
    log_info "4. Finding WIP commits..."
    find_wip_commits
    echo ""
    
    log_info "5. Finding branches with orchestration changes..."
    find_orphaned_branches
    echo ""
    
    log_success "Recovery scan complete"
}

# ============================================================================
# FUNCTION: Print usage
# ============================================================================
print_usage() {
    cat << EOF
Usage: recover_orphaned_work.sh [COMMAND] [OPTIONS]

COMMANDS:
    scan              Full recovery scan (default)
    stashes           List all stashes
    recover-stash N   Recover from stash@{N}
    reflog [BRANCH]   Check reflog for branch
    branches          Find branches with orchestration changes
    patch [FILE]      Create patch from current changes
    wip               Find WIP commits
    status            Check uncommitted changes
    restore HASH      Restore files from specific commit
    help              Show this help message

EXAMPLES:
    # Full scan to find orphaned work
    ./recover_orphaned_work.sh scan
    
    # List stashes and recover from one
    ./recover_orphaned_work.sh stashes
    ./recover_orphaned_work.sh recover-stash 0
    
    # Check what was lost in recent commits
    ./recover_orphaned_work.sh reflog main
    
    # Find branches with your work
    ./recover_orphaned_work.sh branches
    
    # Create backup patch before switching branches
    ./recover_orphaned_work.sh patch my_changes.patch

EOF
}

# ============================================================================
# Main script
# ============================================================================

# Default command
COMMAND=${1:-scan}

case "$COMMAND" in
    scan)
        full_recovery_scan
        ;;
    stashes)
        show_stashes
        ;;
    recover-stash)
        recover_from_stash "$2"
        ;;
    reflog)
        check_reflog "$2"
        ;;
    branches)
        find_orphaned_branches
        ;;
    patch)
        create_patch_from_changes "$2"
        ;;
    wip)
        find_wip_commits
        ;;
    status)
        check_uncommitted_changes
        ;;
    restore)
        restore_from_commit "$2" "$3"
        ;;
    help|--help|-h)
        print_usage
        ;;
    *)
        log_error "Unknown command: $COMMAND"
        print_usage
        exit 1
        ;;
esac
