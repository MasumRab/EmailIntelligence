#!/bin/bash
# modules/logging.sh - Logging module (~200 lines)

# Import dependencies if needed
# Define constants for this module
readonly LOG_FILE_PATH="${LOG_FILE_PATH:-${PROJECT_ROOT:-.}/logs/orchestration-distribution.log}"
readonly LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Function to log distribution event
log_distribution_event() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local script_name=$(basename "$0")
    
    # Create logs directory if it doesn't exist
    mkdir -p "$(dirname "$LOG_FILE_PATH")"
    
    # Format log entry
    local log_entry="[$timestamp] [$level] [$script_name] $message"
    
    # Write to log file
    echo "$log_entry" >> "$LOG_FILE_PATH"
    
    # Output to console if level is INFO or higher
    if [[ "$level" == "ERROR" ]] || [[ "$level" == "WARN" ]] || [[ "$level" == "INFO" ]]; then
        echo "$log_entry"
    fi
}

# Function to log validation results
log_validation_results() {
    local validation_type="$1"
    local result="$2"
    local details="${3:-N/A}"
    
    if [[ "$result" == "SUCCESS" ]]; then
        log_distribution_event "INFO" "Validation '$validation_type': $result - $details"
    elif [[ "$result" == "WARNING" ]]; then
        log_distribution_event "WARN" "Validation '$validation_type': $result - $details"
    else
        log_distribution_event "ERROR" "Validation '$validation_type': $result - $details"
    fi
}

# Function to create distribution report
create_distribution_report() {
    local report_file="$1"
    local start_time="$2"
    local end_time="$3"
    local status="$4"
    
    # Calculate duration
    local duration=$((end_time - start_time))
    
    # Create report content
    local report_content="# Distribution Report\n\n"
    report_content+="**Status**: $status\n"
    report_content+="**Start Time**: $(date -d "@$start_time" '+%Y-%m-%d %H:%M:%S')\n"
    report_content+="**End Time**: $(date -d "@$end_time" '+%Y-%m-%d %H:%M:%S')\n"
    report_content+="**Duration**: ${duration}s\n\n"
    
    # Add validation results
    report_content+="## Validation Results\n"
    report_content+="- Branch validation: $(get_validation_status "branch")\n"
    report_content+="- File integrity: $(get_validation_status "integrity")\n"
    report_content+="- Permissions: $(get_validation_status "permissions")\n\n"
    
    # Add distribution summary
    report_content+="## Distribution Summary\n"
    report_content+="- Source branch: $(get_current_branch)\n"
    report_content+="- Target branches: $(get_target_branches_summary)\n"
    report_content+="- Files distributed: $(get_distributed_files_count)\n\n"
    
    # Add next steps
    report_content+="## Next Steps\n"
    report_content+="- Verify distribution: scripts/validate-orchestration-context.sh\n"
    report_content+="- Test hooks: scripts/install-hooks.sh --verify\n"
    report_content+="- Check branch consistency: scripts/validate-branch-propagation.sh\n\n"
    
    # Add related documentation
    report_content+="## Related Documentation\n"
    report_content+="- ORCHESTRATION_PROCESS_GUIDE.md (Strategy 5/7 workflows)\n"
    report_content+="- TASKMASTER_BRANCH_CONVENTIONS.md (branch isolation)\n"
    report_content+="- AGENTS.md (Task Master integration)\n"
    
    # Write report to file
    echo -e "$report_content" > "$report_file"
    
    log_distribution_event "INFO" "Distribution report created: $report_file"
}

# Function to log commit information
log_commit() {
    local commit_hash="$1"
    local branch_name="$2"
    local message="$3"
    
    log_distribution_event "INFO" "Commit $commit_hash on branch $branch_name: $message"
}

# Function to log error
log_error() {
    local error_message="$1"
    local error_code="${2:-UNKNOWN}"
    
    log_distribution_event "ERROR" "[$error_code] $error_message"
    
    # Also log to stderr
    echo "ERROR [$error_code]: $error_message" >&2
}

# Function to format log message with consistent structure
format_log_message() {
    local category="$1"
    local action="$2"
    local details="$3"
    
    echo "[$category] $action - $details"
}

# Function to get validation status (helper for report)
get_validation_status() {
    local validation_type="$1"
    # This would normally check actual validation results
    # For now, returning placeholder
    echo "PENDING"
}

# Function to get current branch (helper for report)
get_current_branch() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
}

# Function to get target branches summary (helper for report)
get_target_branches_summary() {
    git branch -r | grep "origin/orchestration-tools-" | sed 's/origin\///' | tr '\n' ' ' | sed 's/ $//'
}

# Function to get distributed files count (helper for report)
get_distributed_files_count() {
    # This would normally track actual distributed files
    # For now, returning placeholder
    echo "N/A"
}

# Function to log distribution start
log_distribution_start() {
    local distribution_type="$1"
    local targets="$2"
    
    log_distribution_event "INFO" "Starting $distribution_type distribution to targets: $targets"
}

# Function to log distribution completion
log_distribution_completion() {
    local distribution_type="${1:-full}"
    local success_count="${2:-0}"
    local failure_count="${3:-0}"
    
    if [[ $failure_count -eq 0 ]]; then
        log_distribution_event "INFO" "$distribution_type distribution completed successfully ($success_count targets)"
    else
        log_distribution_event "WARN" "$distribution_type distribution completed with $failure_count failures ($success_count successes)"
    fi
}

# Function to log safety check results
log_safety_check() {
    local check_name="$1"
    local result="$2"
    local details="${3:-N/A}"
    
    if [[ "$result" == "PASS" ]]; then
        log_distribution_event "INFO" "Safety check '$check_name': PASS - $details"
    else
        log_distribution_event "WARN" "Safety check '$check_name': FAIL - $details"
    fi
}

# Function to log configuration changes
log_config_change() {
    local config_key="$1"
    local old_value="$2"
    local new_value="$3"
    
    log_distribution_event "INFO" "Configuration change: $config_key changed from '$old_value' to '$new_value'"
}

# Function to log remote sync operations
log_remote_sync() {
    local operation="$1"
    local source="$2"
    local result="$3"
    
    log_distribution_event "INFO" "Remote sync: $operation from $source - $result"
}

# Function to provide distribution feedback to user
provide_distribution_feedback() {
    echo ""
    echo "✅ Distribution completed successfully!"
    echo ""
    echo "📝 Next recommended steps:"
    echo "  1. Verify distribution: scripts/validate-orchestration-context.sh"
    echo "  2. Test hooks: scripts/install-hooks.sh --verify"
    echo "  3. Check branch consistency: scripts/validate-branch-propagation.sh"
    echo ""
    echo "🔗 Related documentation:"
    echo "  - ORCHESTRATION_PROCESS_GUIDE.md (Strategy 5/7 workflows)"
    echo "  - TASKMASTER_BRANCH_CONVENTIONS.md (branch isolation)"
    echo "  - AGENTS.md (Task Master integration)"
    
    log_distribution_event "INFO" "Provided user feedback and next steps"
}

# Export functions that should be available to other modules
export -f log_distribution_event
export -f log_validation_results
export -f create_distribution_report
export -f log_commit
export -f log_error
export -f format_log_message
export -f log_distribution_start
export -f log_distribution_completion
export -f log_safety_check
export -f log_config_change
export -f log_remote_sync
export -f provide_distribution_feedback