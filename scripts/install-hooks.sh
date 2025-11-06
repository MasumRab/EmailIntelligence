#!/bin/bash
# install-hooks.sh - Install Git hooks from orchestration-tools branch
#
# DESCRIPTION:
#   Installs Git hooks from the canonical orchestration-tools branch to ensure
#   consistent hook versions across all branches and worktrees.
#
# BEHAVIOR:
#   - Pulls hooks from remote orchestration-tools branch (source of truth)
#   - Installs to local .git/hooks/ directory
#   - Ensures all branches use identical hook versions
#
# USAGE:
#   ./scripts/install-hooks.sh [--force] [--verbose]
#
# OPTIONS:
#   --force    Force reinstallation of all hooks
#   --verbose  Enable verbose logging
#
# AUTHOR: Orchestration Team
# VERSION: 2.1.0
# 
# NOTE: When orchestration files are updated, run this script to ensure
# all hooks are properly installed. See docs/orchestration_hook_management.md
# for complete update procedures.

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

# Configuration
ORCHESTRATION_BRANCH="${ORCHESTRATION_BRANCH:-orchestration-tools}"
HOOKS_DIR="scripts/hooks"
REQUIRED_HOOKS=(
    "pre-commit"
    "post-commit"
    "post-merge"
    "post-checkout"
    "post-push"
)

# Parse command line arguments
parse_install_args() {
    FORCE=false
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --force|-f)
                FORCE=true
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                LOG_LEVEL="DEBUG"
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [--force] [--verbose]"
                echo "Install Git hooks from orchestration-tools branch"
                return 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

# Install a single hook from orchestration-tools branch
install_hook_from_remote() {
    local hook_name=$1
    local hook_path="$HOOKS_DIR/$hook_name"
    local git_hook_path=".git/hooks/$hook_name"

    log_info "Installing hook: $hook_name"

    # Check if hook exists in remote orchestration-tools
    if ! git ls-remote --exit-code --heads origin "$ORCHESTRATION_BRANCH" >/dev/null 2>&1; then
        log_error "Remote branch $ORCHESTRATION_BRANCH not found"
        return 1
    fi

    # Fetch latest from remote
    if ! git fetch origin "$ORCHESTRATION_BRANCH" --quiet 2>/dev/null; then
        log_warn "Failed to fetch from remote $ORCHESTRATION_BRANCH"
    fi

    # Check if hook exists in remote branch
    if ! git ls-tree -r "origin/$ORCHESTRATION_BRANCH" --name-only | grep -q "^$hook_path$"; then
        log_debug "Hook $hook_name not found in remote $ORCHESTRATION_BRANCH"
        return 1
    fi

    # Check if update is needed
    local needs_update=true
    if [[ -f "$git_hook_path" ]] && ! $FORCE; then
        # Compare local installed hook with remote version
        if git diff --quiet "origin/$ORCHESTRATION_BRANCH:$hook_path" "$git_hook_path" 2>/dev/null; then
            log_debug "Hook $hook_name is already up to date"
            needs_update=false
        fi
    fi

    if $needs_update; then
        log_info "Updating hook: $hook_name"

        # Checkout from remote branch
        if git show "origin/$ORCHESTRATION_BRANCH:$hook_path" > "$git_hook_path" 2>/dev/null; then
            chmod +x "$git_hook_path"
            log_info "Successfully installed hook: $hook_name"
            return 0
        else
            log_error "Failed to install hook: $hook_name"
            return 1
        fi
    else
        log_debug "Skipping hook (up to date): $hook_name"
        return 0
    fi
}

# Main installation function
main() {
    # Initialize logging manually to avoid common.sh issues
    LOG_LEVEL=${LOG_LEVEL:-INFO}
    CURRENT_LOG_LEVEL=${LOG_LEVEL}

    parse_install_args "$@"

    log_info "Installing Git hooks from remote $ORCHESTRATION_BRANCH branch..."

    # Validate environment
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        log_error "Not in a git repository"
        exit 1
    fi

    local installed=0
    local failed=0

    # Install each required hook
    for hook_name in "${REQUIRED_HOOKS[@]}"; do
        if install_hook_from_remote "$hook_name"; then
            ((installed++))
        else
            ((failed++))
        fi
    done

    log_info "Hook installation completed: $installed installed, $failed failed"

    if [[ $failed -gt 0 ]]; then
        log_warn "Some hooks failed to install. Check logs above."
        exit 1
    fi

    log_info "All hooks installed successfully from $ORCHESTRATION_BRANCH"
}

# Run main function
main "$@"
