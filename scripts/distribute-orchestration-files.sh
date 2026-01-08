#!/bin/bash
# distribute-orchestration-files.sh - Main entry point (~50 lines)

set -euo pipefail

# Define project root and module directory
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly MODULE_DIR="$PROJECT_ROOT/modules"

# Load all modules
source "$MODULE_DIR/config.sh"
source "$MODULE_DIR/utils.sh"
source "$MODULE_DIR/branch.sh"
source "$MODULE_DIR/validate.sh"
source "$MODULE_DIR/distribute.sh"
source "$MODULE_DIR/logging.sh"
source "$MODULE_DIR/safety.sh"

# Default options
DRY_RUN=false
SYNC_FROM_REMOTE=false
WITH_VALIDATION=false
SETUP_ONLY=false
HOOKS_ONLY=false
CONFIG_ONLY=false
VERIFY_ONLY=false
INTERACTIVE=false

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --sync-from-remote)
                SYNC_FROM_REMOTE=true
                shift
                ;;
            --with-validation)
                WITH_VALIDATION=true
                shift
                ;;
            --setup-only)
                SETUP_ONLY=true
                shift
                ;;
            --hooks-only)
                HOOKS_ONLY=true
                shift
                ;;
            --config-only)
                CONFIG_ONLY=true
                shift
                ;;
            --verify)
                VERIFY_ONLY=true
                shift
                ;;
            --interactive)
                INTERACTIVE=true
                shift
                ;;
            *)
                echo "Unknown option: $1"
                echo "Usage: $0 [--dry-run] [--sync-from-remote] [--with-validation] [--setup-only] [--hooks-only] [--config-only] [--verify] [--interactive]"
                exit 1
                ;;
        esac
    done
}

# Initialize configuration
initialize_configuration() {
    load_distribution_config
}

# Execute requested action
execute_requested_action() {
    if [[ "$VERIFY_ONLY" == true ]]; then
        validate_distribution_targets
        return $?
    fi

    if [[ "$SYNC_FROM_REMOTE" == true ]]; then
        sync_from_remote "origin/orchestration-tools"
    fi

    if [[ "$DRY_RUN" == true ]]; then
        echo "DRY RUN: Would distribute orchestration files"
        return 0
    fi

    # Perform distribution based on options
    if [[ "$SETUP_ONLY" == true ]]; then
        distribute_setup_files
    elif [[ "$HOOKS_ONLY" == true ]]; then
        distribute_hooks
    elif [[ "$CONFIG_ONLY" == true ]]; then
        distribute_configs
    else
        distribute_all_files
    fi

    if [[ "$WITH_VALIDATION" == true ]]; then
        validate_distribution_targets
    fi

    log_distribution_completion
    provide_distribution_feedback
}

# Main execution function
main() {
    parse_arguments "$@"
    initialize_configuration
    execute_requested_action
}

# Execute main function
main "$@"