#!/bin/bash

# enable-hooks.sh - Re-enable Git hooks after independent development
#
# DESCRIPTION:
#   Re-enables all previously disabled orchestration hooks. Run this after you've
#   finished modifying setup files directly in your branch.
#
# USAGE:
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
    # Check if disabled hooks directory exists
    if [[ ! -d "$DISABLED_HOOKS_DIR" ]]; then
        log_warn "No disabled hooks found (.git/hooks.disabled directory not found)"
        log_info "Hooks may already be enabled or were never disabled"
        exit 0
    fi

    # Ensure .git/hooks exists
    mkdir -p "$HOOKS_DIR"

    # List of hooks to re-enable
    HOOKS=(
        "pre-commit"
        "post-commit"
        "post-merge"
        "post-checkout"
        "post-push"
    )

    local enabled_count=0

    # Re-enable each hook
    for hook in "${HOOKS[@]}"; do
        local disabled_path="$DISABLED_HOOKS_DIR/$hook"
        local hook_path="$HOOKS_DIR/$hook"

        if [[ -f "$disabled_path" ]]; then
            # Move hook back from disabled directory
            mv "$disabled_path" "$hook_path"
            chmod +x "$hook_path"
            log_info "Re-enabled hook: $hook"
            ((enabled_count++))
        fi
    done

    # Clean up disabled hooks directory if empty
    if [[ -z "$(ls -A "$DISABLED_HOOKS_DIR" 2>/dev/null)" ]]; then
        rmdir "$DISABLED_HOOKS_DIR"
        log_info "Cleaned up disabled hooks directory"
    fi

    if [[ $enabled_count -gt 0 ]]; then
        log_info "All $enabled_count Git hooks have been re-enabled"
        echo ""
        echo "Orchestration-tools synchronization is now active again."
        echo "Setup files will be synced from orchestration-tools on next checkout/merge."
        echo ""
    else
        log_warn "No hooks were found to re-enable"
        exit 1
    fi
}

main "$@"