#!/bin/bash
# enhanced-launch-system.sh - Enhanced launch system with SOLID principles

set -euo pipefail

# Define project root and module directory
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
readonly MODULE_DIR="$PROJECT_ROOT/modules"
readonly LAUNCH_LOG_FILE="$PROJECT_ROOT/logs/launch-system.log"

# Import all modules
source "$MODULE_DIR/config.sh"
source "$MODULE_DIR/utils.sh"
source "$MODULE_DIR/branch.sh"
source "$MODULE_DIR/validate.sh"
source "$MODULE_DIR/distribute.sh"
source "$MODULE_DIR/logging.sh"
source "$MODULE_DIR/safety.sh"

# Default options
ACTION="run"
DRY_RUN=false
SYNC_FROM_REMOTE=false
WITH_VALIDATION=false
SETUP_ONLY=false
HOOKS_ONLY=false
CONFIG_ONLY=false
VERIFY_ONLY=false
INTERACTIVE=false
VERBOSE=false

# Function to log launch system events
log_launch_event() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Create logs directory if it doesn't exist
    mkdir -p "$(dirname "$LAUNCH_LOG_FILE")"
    
    # Format log entry
    local log_entry="[$timestamp] [$level] [launch-system] $message"
    
    # Write to log file
    echo "$log_entry" >> "$LAUNCH_LOG_FILE"
    
    # Output to console if level is INFO or higher
    if [[ "$level" == "ERROR" ]] || [[ "$level" == "WARN" ]] || [[ "$level" == "INFO" ]]; then
        echo "$log_entry"
    fi
}

# Function to validate environment before launch
validate_launch_environment() {
    log_launch_event "INFO" "Validating launch environment..."
    
    # Check if git repository is in a good state
    if ! validate_git_repository_state; then
        log_launch_event "ERROR" "Git repository state validation failed"
        return 1
    fi
    
    # Check if we're in the right branch
    local current_branch=$(get_current_branch)
    if [[ "$current_branch" == taskmaster* ]]; then
        log_launch_event "WARN" "Currently on taskmaster branch: $current_branch"
    fi
    
    # Check disk space
    if ! check_disk_space 100; then  # Require at least 100MB
        log_launch_event "WARN" "Insufficient disk space detected"
    fi
    
    log_launch_event "INFO" "Launch environment validation passed"
    return 0
}

# Function to handle setup action
handle_setup_action() {
    log_launch_event "INFO" "Executing setup action..."
    
    # Create necessary directories
    mkdir -p "$PROJECT_ROOT/logs" "$PROJECT_ROOT/config" "$PROJECT_ROOT/backups"
    
    # Initialize configuration
    load_distribution_config
    
    # Validate environment
    validate_launch_environment
    
    log_launch_event "INFO" "Setup action completed successfully"
}

# Function to handle distribution action
handle_distribution_action() {
    log_launch_event "INFO" "Executing distribution action..."
    
    # Validate environment first
    if ! validate_launch_environment; then
        log_launch_event "ERROR" "Environment validation failed, aborting distribution"
        return 1
    fi
    
    # Check for uncommitted files
    if ! check_uncommitted_files "false"; then
        log_launch_event "ERROR" "Uncommitted files detected and user cancelled operation"
        return 1
    fi
    
    # Perform distribution based on options
    if [[ "$DRY_RUN" == true ]]; then
        log_launch_event "INFO" "DRY RUN: Would distribute orchestration files"
        return 0
    fi
    
    if [[ "$SYNC_FROM_REMOTE" == true ]]; then
        log_launch_event "INFO" "Syncing from remote orchestration-tools branch"
        sync_from_remote "origin/orchestration-tools"
    fi
    
    # Perform distribution based on selected options
    if [[ "$SETUP_ONLY" == true ]]; then
        distribute_setup_files
    elif [[ "$HOOKS_ONLY" == true ]]; then
        distribute_hooks
    elif [[ "$CONFIG_ONLY" == true ]]; then
        distribute_configs
    elif [[ "$VERIFY_ONLY" == true ]]; then
        validate_distribution_targets
        return $?
    else
        distribute_all_files
    fi
    
    if [[ "$WITH_VALIDATION" == true ]]; then
        validate_distribution_targets
    fi
    
    log_distribution_completion
    provide_distribution_feedback
    
    log_launch_event "INFO" "Distribution action completed successfully"
}

# Function to handle verification action
handle_verification_action() {
    log_launch_event "INFO" "Executing verification action..."
    
    # Run all validation checks
    validate_distribution_targets
    
    log_launch_event "INFO" "Verification action completed"
}

# Function to display help
show_help() {
    cat << EOF
Enhanced Orchestration Launch System

Usage: $0 [OPTIONS] [ACTION]

Actions:
  run          Run the orchestration distribution (default)
  setup        Set up the orchestration environment
  verify       Verify the orchestration setup
  help         Show this help message

Options:
  --dry-run           Preview distribution without making changes
  --sync-from-remote  Pull latest from remote before distribution
  --with-validation   Run validation after distribution
  --setup-only        Distribute only setup files
  --hooks-only        Distribute only git hooks
  --config-only       Distribute only configuration files
  --verify            Run validation without distribution
  --interactive       Prompt for confirmation on major actions
  --verbose           Enable verbose output
  --help              Show this help message

Examples:
  $0 setup                           # Set up the environment
  $0 run --sync-from-remote          # Run distribution with remote sync
  $0 run --dry-run                   # Preview distribution
  $0 verify                          # Verify orchestration setup
EOF
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            run|setup|verify|help)
                ACTION="$1"
                shift
                ;;
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
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option or action: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Main execution function
main() {
    log_launch_event "INFO" "Starting enhanced launch system"
    
    parse_arguments "$@"
    
    case "$ACTION" in
        setup)
            handle_setup_action
            ;;
        verify)
            handle_verification_action
            ;;
        run)
            handle_distribution_action
            ;;
        help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown action: $ACTION"
            show_help
            exit 1
            ;;
    esac
    
    log_launch_event "INFO" "Enhanced launch system completed successfully"
}

# Execute main function
main "$@"