#!/bin/bash
# Common utilities for orchestration scripts

# Source all utility libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$(dirname "${BASH_SOURCE[0]}")"

# Source utilities if they exist
[[ -f "$LIB_DIR/logging.sh" ]] && source "$LIB_DIR/logging.sh"
[[ -f "$LIB_DIR/validation.sh" ]] && source "$LIB_DIR/validation.sh"
[[ -f "$LIB_DIR/git_utils.sh" ]] && source "$LIB_DIR/git_utils.sh"
[[ -f "$LIB_DIR/error_handling.sh" ]] && source "$LIB_DIR/error_handling.sh"

# Global configuration
HOOKS_DIR="${HOOKS_DIR:-scripts/hooks}"
GIT_HOOKS_DIR="${GIT_HOOKS_DIR:-.git/hooks}"
ORCHESTRATION_BRANCH="${ORCHESTRATION_BRANCH:-orchestration-tools}"

# Initialize common setup
common_init() {
    setup_logging
    setup_error_handling
    log_debug "Common utilities initialized"
}