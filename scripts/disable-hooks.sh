#!/bin/bash

<<<<<<< HEAD
# Script to temporarily disable Git hooks for development work
# This helps avoid hook-related warnings when working on non-orchestration branches

set -e

echo "Disabling Git hooks..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a Git repository"
    exit 1
fi

# Backup existing hooks if they exist
HOOKS_DIR=".git/hooks"
BACKUP_DIR=".git/hooks_backup"

if [ -d "$HOOKS_DIR" ] && [ "$(ls -A $HOOKS_DIR)" ]; then
    echo "Backing up existing hooks..."
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
    fi
    
    # Move all hook files to backup directory
    for hook in "$HOOKS_DIR"/*; do
        if [ -f "$hook" ]; then
            hook_name=$(basename "$hook")
            echo "  Backing up $hook_name"
            mv "$hook" "$BACKUP_DIR/$hook_name"
        fi
    done
fi

# Create dummy hooks that simply exit successfully
echo "Creating dummy hooks..."

HOOK_NAMES=("pre-commit" "post-commit" "post-merge" "post-checkout" "post-push")

for hook_name in "${HOOK_NAMES[@]}"; do
    hook_path="$HOOKS_DIR/$hook_name"
    
    # Create the hook file with a simple exit 0
    cat > "$hook_path" << 'EOF'
#!/bin/bash
# Dummy hook - does nothing
exit 0
EOF
    
    # Make it executable
    chmod +x "$hook_path"
    echo "  Created dummy $hook_name hook"
done

echo "Git hooks have been disabled successfully!"
echo ""
echo "To restore the original hooks later, run:"
echo "  ./scripts/restore-hooks.sh"
=======
# disable-hooks.sh - Disable Git hooks for independent setup file development
#
# DESCRIPTION:
#   Temporarily disables all orchestration hooks to allow independent development
#   of setup files without automatic synchronization from orchestration-tools branch.
#
#   Use this when you need to modify setup files directly in your branch without
#   interference from the hook-based sync mechanism.
#
# USAGE:
#   ./scripts/disable-hooks.sh
#   DISABLE_ORCHESTRATION_CHECKS=1 git checkout <branch>  # Use hooks-disabled mode
#
# To re-enable:
#   ./scripts/enable-hooks.sh
#
# AUTHOR: Orchestration Team
# VERSION: 1.0.0

set -e

HOOKS_DIR=".git/hooks"
DISABLED_HOOKS_DIR=".git/hooks.disabled"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

main() {
    # Check if .git/hooks exists
    if [[ ! -d "$HOOKS_DIR" ]]; then
        log_error ".git/hooks directory not found"
        exit 1
    fi

    # Create disabled hooks directory if it doesn't exist
    mkdir -p "$DISABLED_HOOKS_DIR"

    # List of hooks to disable
    HOOKS=(
        "pre-commit"
        "post-commit"
        "post-merge"
        "post-checkout"
        "post-push"
    )

    local disabled_count=0

    # Disable each hook
    for hook in "${HOOKS[@]}"; do
        local hook_path="$HOOKS_DIR/$hook"
        local disabled_path="$DISABLED_HOOKS_DIR/$hook"

        if [[ -f "$hook_path" ]]; then
            # Move hook to disabled directory
            mv "$hook_path" "$disabled_path"
            log_info "Disabled hook: $hook"
            ((disabled_count++))
        fi
    done

    if [[ $disabled_count -gt 0 ]]; then
        log_warn "All $disabled_count Git hooks have been disabled"
        echo ""
        log_info "You can now modify setup files independently without orchestration-tools sync"
        echo ""
        echo "To re-enable hooks, run:"
        echo "  ./scripts/enable-hooks.sh"
        echo ""
        echo "Or use environment variable to bypass hooks on single operations:"
        echo "  DISABLE_ORCHESTRATION_CHECKS=1 git checkout <branch>"
        echo "  DISABLE_ORCHESTRATION_CHECKS=1 git merge <branch>"
        echo ""
    else
        log_warn "No hooks found to disable (already disabled?)"
        exit 1
    fi
}

main "$@"
>>>>>>> 85c264ece19bbfafb8a4e31da1c234d05e6884e3
