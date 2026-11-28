#!/bin/bash
# Error handling utility functions for orchestration scripts

# Error exit function
error_exit() {
    local code=$1
    local message=$2

    log_error "$message"
    cleanup_on_error
    exit $code
}

# Cleanup on error
cleanup_on_error() {
    # Clean up temporary files, reset state, etc.
    log_debug "Performing error cleanup"

    # Add specific cleanup logic here as needed
    # For example: remove temporary files, reset git state, etc.
}

# Setup error handling
setup_error_handling() {
    # Set up traps
    trap 'error_exit $ERROR_UNEXPECTED "Unexpected error occurred at line $LINENO"' ERR

    # Note: set -euo pipefail should be set in main script, not in sourced files
    # to avoid issues with sourcing

    log_debug "Error handling initialized"
}

# Validate exit code
check_exit_code() {
    local exit_code=$1
    local operation=$2

    if [[ $exit_code -ne 0 ]]; then
        log_error "Operation failed: $operation (exit code: $exit_code)"
        return 1
    fi

    return 0
}