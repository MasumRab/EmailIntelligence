#!/bin/bash
# performance_monitor.sh - Performance monitoring for orchestration distribution system

set -euo pipefail

# Configuration
readonly LOG_DIR="${PERFORMANCE_LOG_DIR:-./logs}"
readonly PERFORMANCE_LOG="${LOG_DIR}/performance.log"
readonly METRICS_LOG="${LOG_DIR}/metrics.jsonl"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Function to log performance metrics
log_performance_metric() {
    local operation="$1"
    local duration="$2"  # in seconds
    local status="$3"    # success/failure
    local details="${4:-""}"

    local timestamp=$(date -Iseconds)
    local hostname=$(hostname)
    local pid=$$

    # Create JSON log entry
    local log_entry=$(printf '{
  "timestamp": "%s",
  "hostname": "%s",
  "pid": %d,
  "operation": "%s",
  "duration_seconds": %.3f,
  "status": "%s",
  "details": "%s"
}' "$timestamp" "$hostname" "$pid" "$operation" "$duration" "$status" "$details")

    # Write to metrics log
    echo "$log_entry" >> "$METRICS_LOG"

    # Write to performance log in human-readable format
    printf "[%s] OPERATION: %s | DURATION: %.3fs | STATUS: %s | DETAILS: %s\n" \
        "$timestamp" "$operation" "$duration" "$status" "$details" >> "$PERFORMANCE_LOG"
}

# Function to measure execution time of a command
measure_command() {
    local operation="$1"
    shift
    local command=("$@")

    local start_time=$(date +%s.%N)
    local status="success"

    # Execute the command and capture exit status
    if ! "${command[@]}" 2>/dev/null; then
        status="failure"
    fi

    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l)

    # Log the performance metric
    log_performance_metric "$operation" "$duration" "$status"

    return 0
}

# Function to measure file distribution performance
measure_distribution() {
    local source_branch="$1"
    local target_branch="$2"
    local file_count="$3"

    local start_time=$(date +%s.%N)
    local status="success"

    # Simulate distribution measurement (in real implementation, this would measure actual distribution)
    # For now, we'll just log the metrics
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l)

    local details="files:$file_count,source:$source_branch,target:$target_branch"

    log_performance_metric "distribution" "$duration" "$status" "$details"
}

# Function to measure validation performance
measure_validation() {
    local validation_type="$1"
    local item_count="$2"

    local start_time=$(date +%s.%N)
    local status="success"

    # Simulate validation measurement
    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l)

    local details="type:$validation_type,count:$item_count"

    log_performance_metric "validation" "$duration" "$status" "$details"
}

# Function to generate performance report
generate_performance_report() {
    local report_format="${1:-text}"  # text or json

    if [[ ! -f "$METRICS_LOG" ]]; then
        echo "No performance data available"
        return 1
    fi

    case "$report_format" in
        "json")
            generate_json_report
            ;;
        "detailed")
            generate_detailed_report
            ;;
        *)
            generate_text_report
            ;;
    esac
}

# Function to generate text report
generate_text_report() {
    echo "=== PERFORMANCE REPORT ==="
    echo "Generated: $(date)"
    echo ""

    # Overall statistics
    echo "OVERALL STATISTICS:"
    echo "Total operations: $(wc -l < "$METRICS_LOG")"
    echo "Success rate: $(calculate_success_rate)%"
    echo "Average duration: $(calculate_average_duration)s"
    echo "Slowest operation: $(find_slowest_operation)"
    echo ""

    # Operation breakdown
    echo "OPERATION BREAKDOWN:"
    echo "Distribution operations:"
    grep '"operation": "distribution"' "$METRICS_LOG" | wc -l
    echo "Validation operations:"
    grep '"operation": "validation"' "$METRICS_LOG" | wc -l
    echo "Command operations:"
    grep '"operation": "command"' "$METRICS_LOG" | wc -l
    echo ""
}

# Function to calculate success rate
calculate_success_rate() {
    local total=$(wc -l < "$METRICS_LOG")
    local successes=$(grep '"status": "success"' "$METRICS_LOG" | wc -l)
    local rate=$(echo "scale=2; $successes * 100 / $total" | bc -l)
    echo "$rate"
}

# Function to calculate average duration
calculate_average_duration() {
    local total_duration=$(awk -F'"duration_seconds": ' '{sum += $2} END {print sum}' "$METRICS_LOG" | cut -d',' -f1)
    local count=$(wc -l < "$METRICS_LOG")
    local avg=$(echo "scale=3; $total_duration / $count" | bc -l)
    echo "$avg"
}

# Function to find slowest operation
find_slowest_operation() {
    local slowest=$(awk -F'"duration_seconds": ' '{if($2 > max) {max=$2; line=$0}} END {print max}' "$METRICS_LOG")
    echo "$slowest s"
}

# Function to generate detailed report
generate_detailed_report() {
    echo "=== DETAILED PERFORMANCE REPORT ==="
    echo "Generated: $(date)"
    echo ""

    # Detailed breakdown by operation type
    for op_type in "distribution" "validation" "command"; do
        if grep -q "\"operation\": \"$op_type\"" "$METRICS_LOG"; then
            echo "=== $op_type OPERATIONS ==="
            grep "\"operation\": \"$op_type\"" "$METRICS_LOG" | while read -r line; do
                local duration=$(echo "$line" | grep -o '"duration_seconds": [0-9.]*' | cut -d' ' -f2)
                local status=$(echo "$line" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)
                local details=$(echo "$line" | grep -o '"details": "[^"]*"' | cut -d'"' -f4)
                echo "  Duration: $duration s | Status: $status | Details: $details"
            done
            echo ""
        fi
    done
}

# Function to generate JSON report
generate_json_report() {
    local total_ops=$(wc -l < "$METRICS_LOG")
    local successes=$(grep '"status": "success"' "$METRICS_LOG" | wc -l)
    local failures=$(grep '"status": "failure"' "$METRICS_LOG" | wc -l)
    local avg_duration=$(calculate_average_duration)
    local success_rate=$(calculate_success_rate)

    printf '{
  "generated_at": "%s",
  "total_operations": %d,
  "successful_operations": %d,
  "failed_operations": %d,
  "success_rate_percent": %.2f,
  "average_duration_seconds": %.3f,
  "metrics_file": "%s"
}' "$(date -Iseconds)" "$total_ops" "$successes" "$failures" "$success_rate" "$avg_duration" "$METRICS_LOG"
}

# Function to clean old performance logs
clean_old_logs() {
    local days_to_keep="${1:-30}"  # Default: keep 30 days of logs

    find "$LOG_DIR" -name "performance.log*" -mtime +$days_to_keep -delete
    find "$LOG_DIR" -name "metrics.jsonl" -mtime +$days_to_keep -delete

    echo "Cleaned performance logs older than $days_to_keep days"
}

# Function to get performance summary
get_performance_summary() {
    if [[ ! -f "$METRICS_LOG" ]]; then
        echo "No performance data available"
        return 1
    fi

    local total_ops=$(wc -l < "$METRICS_LOG")
    local avg_duration=$(calculate_average_duration)
    local success_rate=$(calculate_success_rate)

    echo "Performance Summary:"
    echo "  Total operations: $total_ops"
    echo "  Avg duration: $avg_duration s"
    echo "  Success rate: $success_rate%"
}

# Main function to demonstrate usage
main() {
    local action="${1:-help}"

    case "$action" in
        "measure")
            shift
            measure_command "$@"
            ;;
        "log")
            local operation="$2"
            local duration="$3"
            local status="$4"
            local details="$5"
            log_performance_metric "$operation" "$duration" "$status" "$details"
            ;;
        "report")
            local format="${2:-text}"
            generate_performance_report "$format"
            ;;
        "summary")
            get_performance_summary
            ;;
        "clean")
            local days="${2:-30}"
            clean_old_logs "$days"
            ;;
        "help")
            echo "Performance Monitor Usage:"
            echo "  $0 measure <operation> <command...>     - Measure command execution"
            echo "  $0 log <operation> <duration> <status> [details] - Log performance metric"
            echo "  $0 report [text|json|detailed]         - Generate performance report"
            echo "  $0 summary                             - Get performance summary"
            echo "  $0 clean [days]                        - Clean old logs (default: 30 days)"
            echo "  $0 help                                - Show this help"
            ;;
        *)
            echo "Unknown action: $action"
            echo "Use 'help' for usage information"
            return 1
            ;;
    esac
}

# Export functions for use by other scripts
export -f log_performance_metric
export -f measure_command
export -f measure_distribution
export -f measure_validation
export -f generate_performance_report
export -f get_performance_summary

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi