#!/bin/bash
# detailed_reporter.sh - Detailed reporting for orchestration distribution system

set -euo pipefail

# Configuration
readonly REPORTS_DIR="${REPORTS_DIR:-./reports}"
readonly LOG_DIR="${LOG_DIR:-./logs}"
readonly PERFORMANCE_LOG="${LOG_DIR}/performance.log"
readonly METRICS_LOG="${LOG_DIR}/metrics.jsonl"
readonly DETAILED_REPORT="${REPORTS_DIR}/detailed_report_$(date +%Y%m%d_%H%M%S).txt"

# Create directories if they don't exist
mkdir -p "$REPORTS_DIR" "$LOG_DIR"

# Function to generate detailed distribution report
generate_distribution_report() {
    local report_file="$1"
    
    {
        echo "=== DETAILED DISTRIBUTION REPORT ==="
        echo "Generated: $(date)"
        echo "Hostname: $(hostname)"
        echo "User: $(whoami)"
        echo ""

        # System information
        echo "SYSTEM INFORMATION:"
        echo "  OS: $(uname -s)"
        echo "  Kernel: $(uname -r)"
        echo "  Architecture: $(uname -m)"
        echo "  Uptime: $(uptime)"
        echo ""

        # Git information
        echo "GIT INFORMATION:"
        if command -v git >/dev/null 2>&1; then
            echo "  Git version: $(git --version)"
            echo "  Current branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'N/A')"
            echo "  Git status: $(git status --porcelain 2>/dev/null | wc -l) files modified"
        else
            echo "  Git: Not installed"
        fi
        echo ""

        # Disk usage
        echo "DISK USAGE:"
        df -h . | tail -1
        echo ""

        # Distribution statistics
        echo "DISTRIBUTION STATISTICS:"
        if [[ -f "$METRICS_LOG" ]]; then
            local total_ops=$(wc -l < "$METRICS_LOG")
            local successes=$(grep '"status": "success"' "$METRICS_LOG" | wc -l)
            local failures=$(grep '"status": "failure"' "$METRICS_LOG" | wc -l)
            local success_rate=$(echo "scale=2; $successes * 100 / $total_ops" | bc -l)
            
            echo "  Total operations: $total_ops"
            echo "  Successful operations: $successes"
            echo "  Failed operations: $failures"
            echo "  Success rate: ${success_rate}%"
            
            # Average duration
            local total_duration=$(awk -F'"duration_seconds": ' '{sum += $2} END {print sum}' "$METRICS_LOG" | cut -d',' -f1)
            local avg_duration=$(echo "scale=3; $total_duration / $total_ops" | bc -l)
            echo "  Average duration: $avg_duration seconds"
            
            # Slowest operation
            local slowest=$(awk -F'"duration_seconds": ' '{if($2 > max) {max=$2}} END {print max}' "$METRICS_LOG")
            echo "  Slowest operation: $slowest seconds"
        else
            echo "  No performance data available"
        fi
        echo ""

        # Operation breakdown
        echo "OPERATION BREAKDOWN:"
        if [[ -f "$METRICS_LOG" ]]; then
            for op_type in "distribution" "validation" "command"; do
                if grep -q "\"operation\": \"$op_type\"" "$METRICS_LOG"; then
                    local count=$(grep "\"operation\": \"$op_type\"" "$METRICS_LOG" | wc -l)
                    local avg_dur=$(grep "\"operation\": \"$op_type\"" "$METRICS_LOG" | awk -F'"duration_seconds": ' '{sum += $2} END {print sum/NR}' | cut -d',' -f1)
                    local success_rate_op=$(grep "\"operation\": \"$op_type\"" "$METRICS_LOG" | grep '"status": "success"' | wc -l)
                    local total_op=$(grep "\"operation\": \"$op_type\"" "$METRICS_LOG" | wc -l)
                    local rate_op=$(echo "scale=2; $success_rate_op * 100 / $total_op" | bc -l)
                    
                    echo "  $op_type:"
                    echo "    Count: $count"
                    echo "    Average duration: $avg_dur s"
                    echo "    Success rate: ${rate_op}%"
                fi
            done
        fi
        echo ""

        # Recent operations
        echo "RECENT OPERATIONS (last 10):"
        if [[ -f "$METRICS_LOG" ]]; then
            tail -10 "$METRICS_LOG" | while read -r line; do
                local timestamp=$(echo "$line" | grep -o '"timestamp": "[^"]*"' | cut -d'"' -f4)
                local operation=$(echo "$line" | grep -o '"operation": "[^"]*"' | cut -d'"' -f4)
                local duration=$(echo "$line" | grep -o '"duration_seconds": [0-9.]*' | cut -d' ' -f2 | cut -d',' -f1)
                local status=$(echo "$line" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)
                local details=$(echo "$line" | grep -o '"details": "[^"]*"' | cut -d'"' -f4)
                
                printf "  [%s] %s | %.3fs | %s | %s\n" "$timestamp" "$operation" "$duration" "$status" "$details"
            done
        else
            echo "  No recent operations"
        fi
        echo ""

        # Configuration information
        echo "CONFIGURATION INFORMATION:"
        echo "  Reports directory: $REPORTS_DIR"
        echo "  Logs directory: $LOG_DIR"
        echo "  Performance log: $PERFORMANCE_LOG"
        echo "  Metrics log: $METRICS_LOG"
        echo ""

        # File counts
        echo "FILE COUNTS:"
        echo "  Scripts directory: $(find ./scripts -type f | wc -l) files"
        echo "  Modules directory: $(find ./modules -type f | wc -l) files"
        echo "  Config directory: $(find ./config -type f | wc -l) files"
        echo "  Setup directory: $(find ./setup -type f | wc -l) files"
        echo ""

        # Module information
        echo "MODULE INFORMATION:"
        if [[ -d "./modules" ]]; then
            for module in ./modules/*.sh; do
                if [[ -f "$module" ]]; then
                    local module_name=$(basename "$module")
                    local line_count=$(wc -l < "$module")
                    echo "  $module_name: $line_count lines"
                fi
            done
        fi
        echo ""

        # Safety checks performed
        echo "SAFETY CHECKS SUMMARY:"
        echo "  Uncommitted file checks: $(grep -c 'uncommitted' "$PERFORMANCE_LOG" 2>/dev/null || echo 0)"
        echo "  Taskmaster isolation checks: $(grep -c 'taskmaster' "$PERFORMANCE_LOG" 2>/dev/null || echo 0)"
        echo "  Permission validations: $(grep -c 'permission' "$PERFORMANCE_LOG" 2>/dev/null || echo 0)"
        echo ""

        # Validation checks performed
        echo "VALIDATION CHECKS SUMMARY:"
        echo "  Branch validation: $(grep -c 'branch' "$PERFORMANCE_LOG" 2>/dev/null || echo 0)"
        echo "  File integrity checks: $(grep -c 'integrity' "$PERFORMANCE_LOG" 2>/dev/null || echo 0)"
        echo "  Large file detection: $(grep -c 'large' "$PERFORMANCE_LOG" 2>/dev/null || echo 0)"
        echo "  Sensitive data scans: $(grep -c 'sensitive' "$PERFORMANCE_LOG" 2>/dev/null || echo 0)"
        echo ""

        # Recommendations
        echo "RECOMMENDATIONS:"
        if [[ -f "$METRICS_LOG" ]]; then
            local avg_duration=$(echo "scale=3; $total_duration / $total_ops" | bc -l)
            if (( $(echo "$avg_duration > 5.0" | bc -l) )); then
                echo "  - Average operation time is high ($avg_duration s), consider optimization"
            fi
            
            if (( $(echo "$success_rate < 95.0" | bc -l) )); then
                echo "  - Success rate is low ($success_rate%), investigate failures"
            fi
        fi
        
        echo "  - Review recent operations for anomalies"
        echo "  - Monitor disk space usage"
        echo "  - Ensure configuration files are up to date"
        echo ""

        echo "Report generated by: $(basename "$0")"
        echo "Report location: $report_file"
    } > "$report_file"
}

# Function to generate summary report
generate_summary_report() {
    local report_file="$1"
    
    {
        echo "=== DAILY SUMMARY REPORT ==="
        echo "Date: $(date)"
        echo ""

        if [[ -f "$METRICS_LOG" ]]; then
            local total_ops=$(wc -l < "$METRICS_LOG")
            local successes=$(grep '"status": "success"' "$METRICS_LOG" | wc -l)
            local failures=$(grep '"status": "failure"' "$METRICS_LOG" | wc -l)
            local success_rate=$(echo "scale=2; $successes * 100 / $total_ops" | bc -l)
            
            echo "OPERATION SUMMARY:"
            echo "  Total: $total_ops"
            echo "  Success: $successes"
            echo "  Failures: $failures"
            echo "  Success Rate: ${success_rate}%"
            
            local avg_duration=$(awk -F'"duration_seconds": ' '{sum += $2} END {print sum/NR}' "$METRICS_LOG" | cut -d',' -f1)
            echo "  Avg Duration: $avg_duration s"
        else
            echo "OPERATION SUMMARY:"
            echo "  No operations recorded today"
        fi
        echo ""

        echo "SYSTEM HEALTH:"
        local disk_usage=$(df . | awk 'NR==2 {print $5}' | sed 's/%//')
        echo "  Disk Usage: ${disk_usage}%"
        
        if [[ $disk_usage -gt 80 ]]; then
            echo "  ⚠️  High disk usage - consider cleanup"
        else
            echo "  ✅ Disk usage acceptable"
        fi
        echo ""

        echo "CONFIGURATION:"
        echo "  Modules: $(find ./modules -maxdepth 1 -name '*.sh' | wc -l) files"
        echo "  Scripts: $(find ./scripts -maxdepth 1 -name '*.sh' | wc -l) files"
        echo "  Configs: $(find ./config -maxdepth 1 -name '*.json' | wc -l) files"
        echo ""

        echo "NEXT ACTIONS:"
        echo "  - Review any failed operations"
        echo "  - Check for system maintenance needs"
        echo "  - Verify backup status"
    } > "$report_file"
}

# Function to generate weekly report
generate_weekly_report() {
    local report_file="$1"
    
    {
        echo "=== WEEKLY PERFORMANCE REPORT ==="
        echo "Week: $(date +%Y-W%U)"
        echo "Generated: $(date)"
        echo ""

        if [[ -f "$METRICS_LOG" ]]; then
            local total_ops=$(wc -l < "$METRICS_LOG")
            local successes=$(grep '"status": "success"' "$METRICS_LOG" | wc -l)
            local failures=$(grep '"status": "failure"' "$METRICS_LOG" | wc -l)
            local success_rate=$(echo "scale=2; $successes * 100 / $total_ops" | bc -l)
            
            echo "WEEKLY STATISTICS:"
            echo "  Total Operations: $total_ops"
            echo "  Success Rate: ${success_rate}%"
            
            local avg_duration=$(awk -F'"duration_seconds": ' '{sum += $2} END {print sum/NR}' "$METRICS_LOG" | cut -d',' -f1)
            echo "  Average Duration: $avg_duration s"
            
            # Find peak usage times
            echo "  Peak Usage Day: $(cut -d'T' -f1 "$METRICS_LOG" | cut -d'"' -f4 | sort | uniq -c | sort -nr | head -1 | awk '{print $2}')"
        else
            echo "WEEKLY STATISTICS:"
            echo "  No data available for this week"
        fi
        echo ""

        echo "TRENDS:"
        echo "  - Performance stability: TBD"
        echo "  - Success rate trend: TBD"
        echo "  - Operation volume: TBD"
        echo ""

        echo "IMPROVEMENT AREAS:"
        echo "  - Optimize slow operations"
        echo "  - Investigate failure patterns"
        echo "  - Review configuration efficiency"
    } > "$report_file"
}

# Function to send report via email (placeholder)
send_report_email() {
    local report_file="$1"
    local recipient="${2:-admin@localhost}"
    
    echo "EMAIL REPORT FUNCTION:"
    echo "Would send report to: $recipient"
    echo "Report file: $report_file"
    echo "Subject: Orchestration Distribution Report - $(date)"
    echo ""
    echo "This is a placeholder function. In a real implementation, this would:"
    echo "1. Format the report for email"
    echo "2. Send using mail command or SMTP"
    echo "3. Log the sending activity"
}

# Function to archive old reports
archive_reports() {
    local days_to_keep="${1:-30}"
    
    find "$REPORTS_DIR" -name "detailed_report_*" -mtime +$days_to_keep -delete
    find "$REPORTS_DIR" -name "summary_report_*" -mtime +$days_to_keep -delete
    find "$REPORTS_DIR" -name "weekly_report_*" -mtime +$days_to_keep -delete
    
    echo "Archived reports older than $days_to_keep days"
}

# Main function
main() {
    local action="${1:-detailed}"
    local output_file="${2:-$DETAILED_REPORT}"
    local recipient="${3:-}"

    case "$action" in
        "detailed")
            generate_distribution_report "$output_file"
            echo "Detailed report generated: $output_file"
            ;;
        "summary")
            local summary_file="${REPORTS_DIR}/summary_report_$(date +%Y%m%d).txt"
            generate_summary_report "$summary_file"
            echo "Summary report generated: $summary_file"
            ;;
        "weekly")
            local weekly_file="${REPORTS_DIR}/weekly_report_$(date +%Y%m%d).txt"
            generate_weekly_report "$weekly_file"
            echo "Weekly report generated: $weekly_file"
            ;;
        "email")
            if [[ -z "$recipient" ]]; then
                echo "Usage: $0 email <report_type> <email_address>"
                return 1
            fi
            local report_type="${2:-detailed}"
            local temp_report="/tmp/orchestration_report_$(date +%s).txt"
            
            case "$report_type" in
                "detailed") generate_distribution_report "$temp_report" ;;
                "summary") 
                    temp_report="${REPORTS_DIR}/summary_report_$(date +%Y%m%d).txt"
                    generate_summary_report "$temp_report"
                    ;;
                "weekly")
                    temp_report="${REPORTS_DIR}/weekly_report_$(date +%Y%m%d).txt"
                    generate_weekly_report "$temp_report"
                    ;;
                *)
                    echo "Invalid report type: $report_type"
                    return 1
                    ;;
            esac
            
            send_report_email "$temp_report" "$recipient"
            ;;
        "archive")
            local days="${2:-30}"
            archive_reports "$days"
            ;;
        "help")
            echo "Detailed Reporter Usage:"
            echo "  $0 detailed [output_file]          - Generate detailed report"
            echo "  $0 summary                         - Generate daily summary"
            echo "  $0 weekly                          - Generate weekly report"
            echo "  $0 email <type> <email>            - Send report via email"
            echo "  $0 archive [days]                  - Archive old reports"
            echo "  $0 help                            - Show this help"
            ;;
        *)
            echo "Unknown action: $action"
            echo "Use 'help' for usage information"
            return 1
            ;;
    esac
}

# Export functions for use by other scripts
export -f generate_distribution_report
export -f generate_summary_report
export -f generate_weekly_report
export -f send_report_email
export -f archive_reports

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi