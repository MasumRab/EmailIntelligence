#!/bin/bash

# Worktree Documentation Inheritance Sync Script
# Synchronizes common documentation across worktrees

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the project root
if [[ ! -d "$PROJECT_ROOT/worktrees" ]]; then
    print_error "Worktrees directory not found. Run this script from the project root."
    exit 1
fi

# Function to sync common docs from source to target worktree
sync_common_docs() {
    local source_worktree="$1"
    local target_worktree="$2"

    print_status "Syncing common docs from $source_worktree to $target_worktree"

    # Check if source worktree exists
    if [[ ! -d "$PROJECT_ROOT/worktrees/$source_worktree" ]]; then
        print_error "Source worktree $source_worktree does not exist"
        return 1
    fi

    # Check if target worktree exists
    if [[ ! -d "$PROJECT_ROOT/worktrees/$target_worktree" ]]; then
        print_error "Target worktree $target_worktree does not exist"
        return 1
    fi

    local source_common="$PROJECT_ROOT/worktrees/$source_worktree/docs/common/docs"
    local target_common="$PROJECT_ROOT/worktrees/$target_worktree/docs/common/docs"

    # Check if source common docs exist
    if [[ ! -d "$source_common" ]]; then
        print_error "Source common docs directory not found: $source_common"
        return 1
    fi

    # Create target common docs directory if it doesn't exist
    mkdir -p "$target_common"

    # Use rsync to sync files, preserving timestamps and permissions
    if command -v rsync &> /dev/null; then
        rsync -av --delete "$source_common/" "$target_common/"
    else
        # Fallback to cp if rsync is not available
        print_warning "rsync not available, using cp (may not preserve all metadata)"
        cp -r "$source_common"/* "$target_common/" 2>/dev/null || true
    fi

    print_success "Synced common docs from $source_worktree to $target_worktree"
}

# Function to sync from inheritance base to all worktrees
sync_from_inheritance_base() {
    print_status "Syncing from inheritance base to all worktrees"

    # Check if inheritance base exists
    if [[ ! -d "$PROJECT_ROOT/docs" ]]; then
        print_error "Inheritance base docs directory not found: $PROJECT_ROOT/docs"
        return 1
    fi

    # Sync to main worktree
    if [[ -d "$PROJECT_ROOT/worktrees/docs-main" ]]; then
        print_status "Syncing to docs-main worktree"
        mkdir -p "$PROJECT_ROOT/worktrees/docs-main/docs/common"
        if command -v rsync &> /dev/null; then
            rsync -av --delete "$PROJECT_ROOT/docs/" "$PROJECT_ROOT/worktrees/docs-main/docs/common/docs/"
        else
            cp -r "$PROJECT_ROOT/docs"/* "$PROJECT_ROOT/worktrees/docs-main/docs/common/docs/" 2>/dev/null || true
        fi
        print_success "Synced to docs-main worktree"
    else
        print_warning "docs-main worktree not found, skipping"
    fi

    # Sync to scientific worktree
    if [[ -d "$PROJECT_ROOT/worktrees/docs-scientific" ]]; then
        print_status "Syncing to docs-scientific worktree"
        mkdir -p "$PROJECT_ROOT/worktrees/docs-scientific/docs/common"
        if command -v rsync &> /dev/null; then
            rsync -av --delete "$PROJECT_ROOT/docs/" "$PROJECT_ROOT/worktrees/docs-scientific/docs/common/docs/"
        else
            cp -r "$PROJECT_ROOT/docs"/* "$PROJECT_ROOT/worktrees/docs-scientific/docs/common/docs/" 2>/dev/null || true
        fi
        print_success "Synced to docs-scientific worktree"
    else
        print_warning "docs-scientific worktree not found, skipping"
    fi
}

# Function to sync between worktrees
sync_between_worktrees() {
    local source="$1"
    local target="$2"

    if [[ -z "$source" || -z "$target" ]]; then
        print_error "Source and target worktrees must be specified"
        echo "Usage: $0 --sync-between <source> <target>"
        exit 1
    fi

    sync_common_docs "$source" "$target"
}

# Function to check worktree status
check_worktree_status() {
    print_status "Checking worktree status"

    echo "Worktrees found:"
    git worktree list

    echo -e "\nWorktree documentation status:"

    # Check main worktree
    if [[ -d "$PROJECT_ROOT/worktrees/docs-main" ]]; then
        local main_common_count=$(find "$PROJECT_ROOT/worktrees/docs-main/docs/common" -name "*.md" 2>/dev/null | wc -l)
        local main_branch_count=$(find "$PROJECT_ROOT/worktrees/docs-main/docs/main" -name "*.md" 2>/dev/null | wc -l)
        echo "docs-main: $main_common_count common docs, $main_branch_count branch-specific docs"
    else
        echo "docs-main: NOT FOUND"
    fi

    # Check scientific worktree
    if [[ -d "$PROJECT_ROOT/worktrees/docs-scientific" ]]; then
        local scientific_common_count=$(find "$PROJECT_ROOT/worktrees/docs-scientific/docs/common" -name "*.md" 2>/dev/null | wc -l)
        local scientific_branch_count=$(find "$PROJECT_ROOT/worktrees/docs-scientific/docs/scientific" -name "*.md" 2>/dev/null | wc -l)
        echo "docs-scientific: $scientific_common_count common docs, $scientific_branch_count branch-specific docs"
    else
        echo "docs-scientific: NOT FOUND"
    fi
}

# Main script logic
case "${1:-}" in
    "--sync-from-base"|"-b")
        print_status "Syncing common docs from inheritance base to all worktrees"
        sync_from_inheritance_base
        ;;
    "--sync-between"|"-s")
        sync_between_worktrees "$2" "$3"
        ;;
    "--status"|"-t")
        check_worktree_status
        ;;
    "--help"|"-h"|"")
echo "Worktree Documentation Inheritance Sync Script"
echo ""
echo "Usage:"
echo "  $0 --sync-from-base          Sync from inheritance base to all worktrees"
echo "  $0 --sync-between <src> <dst> Sync common docs between specific worktrees"
echo "  $0 --status                  Check worktree documentation status"
echo "  $0 --help                    Show this help message"
echo ""
echo "Note: For advanced conflict resolution, use the Python version:"
echo "  python scripts/sync_common_docs.py --conflict-strategy backup"
echo "  Strategies: overwrite (default), backup, skip, newer"
echo ""
echo "Examples:"
echo "  $0 --sync-from-base"
echo "  $0 --sync-between docs-main docs-scientific"
echo "  $0 --status"
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use '$0 --help' for usage information"
        exit 1
        ;;
esac

print_success "Sync operation completed"