#!/bin/bash
# collect_feedback.sh - Collect user feedback for orchestration distribution system

set -euo pipefail

readonly FEEDBACK_DIR="${FEEDBACK_DIR:-./feedback}"
readonly FEEDBACK_FILE="${FEEDBACK_DIR}/feedback.jsonl"
readonly LOG_FILE="${FEEDBACK_DIR}/feedback.log"

# Create feedback directory if it doesn't exist
mkdir -p "$FEEDBACK_DIR"

# Function to log feedback collection activity
log_activity() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

# Function to collect user feedback
collect_user_feedback() {
    local feedback_type=""
    local severity=""
    local description=""
    local title=""
    
    echo "=== Orchestration Distribution System - User Feedback ==="
    echo ""
    
    # Get feedback title
    echo "Please provide a brief title for your feedback:"
    read -r title
    title="${title//\"/\\\"}"  # Escape quotes
    
    echo ""
    echo "Select feedback type:"
    echo "1) Bug Report"
    echo "2) Feature Request" 
    echo "3) Suggestion"
    echo "4) Praise"
    echo "5) Other"
    
    local type_choice
    read -p "Enter choice (1-5): " type_choice
    
    case "$type_choice" in
        1) feedback_type="bug" ;;
        2) feedback_type="feature" ;;
        3) feedback_type="suggestion" ;;
        4) feedback_type="praise" ;;
        5) feedback_type="other" ;;
        *) 
            echo "Invalid choice. Defaulting to suggestion."
            feedback_type="suggestion"
            ;;
    esac
    
    # Get severity for bugs
    if [[ "$feedback_type" == "bug" ]]; then
        echo ""
        echo "How severe is this issue?"
        echo "1) Critical - System unusable"
        echo "2) High - Major functionality impacted" 
        echo "3) Medium - Minor functionality impacted"
        echo "4) Low - Cosmetic or minor issue"
        local severity_choice
        read -p "Enter choice (1-4): " severity_choice
        
        case "$severity_choice" in
            1) severity="critical" ;;
            2) severity="high" ;;
            3) severity="medium" ;;
            4) severity="low" ;;
            *) severity="medium" ;;
        esac
    else
        severity="medium"
    fi
    
    # Get description
    echo ""
    case "$feedback_type" in
        "bug")
            echo "Please describe the bug in detail:"
            echo "- What were you trying to do?"
            echo "- What happened?"
            echo "- What did you expect to happen?"
            echo "- Any error messages?"
            ;;
        "feature")
            echo "Please describe the feature you'd like to see:"
            echo "- What would this feature do?"
            echo "- Why would it be useful?"
            echo "- Any specific requirements?"
            ;;
        *)
            echo "Please provide your feedback in detail:"
            ;;
    esac
    
    local input_desc
    read -r input_desc
    description="${input_desc//\"/\\\"}"  # Escape quotes
    
    # Get user information
    local user_id="$(whoami)@$(hostname)"
    local timestamp=$(date -Iseconds)
    
    # Create feedback entry
    local feedback_entry=$(printf '{
  "timestamp": "%s",
  "user_id": "%s",
  "title": "%s",
  "type": "%s",
  "severity": "%s",
  "description": "%s",
  "status": "received",
  "assigned_to": "unassigned",
  "version": "1.0"
}' "$timestamp" "$user_id" "$title" "$feedback_type" "$severity" "$description")
    
    # Write to feedback file
    echo "$feedback_entry" >> "$FEEDBACK_FILE"
    
    # Log the activity
    log_activity "INFO" "Feedback collected - Type: $feedback_type, Title: $title"
    
    echo ""
    echo "Thank you for your feedback! It has been recorded."
    echo "Feedback ID: $(wc -l < "$FEEDBACK_FILE")"
    echo "We will review your feedback and respond as appropriate."
    echo ""
    echo "Feedback submitted at: $timestamp"
}

# Function to show feedback status
show_feedback_status() {
    if [[ ! -f "$FEEDBACK_FILE" ]]; then
        echo "No feedback data available"
        return 1
    fi
    
    local total_feedback=$(wc -l < "$FEEDBACK_FILE")
    echo "Feedback Collection Status:"
    echo "  Total feedback items: $total_feedback"
    echo "  Feedback file: $FEEDBACK_FILE"
    echo "  Log file: $LOG_FILE"
    echo ""
    
    # Show breakdown by type
    echo "Breakdown by type:"
    for type in "bug" "feature" "suggestion" "praise" "other"; do
        local count=$(grep -c "\"type\": \"$type\"" "$FEEDBACK_FILE" 2>/dev/null || echo 0)
        if [[ $count -gt 0 ]]; then
            echo "  $type: $count"
        fi
    done
}

# Function to show recent feedback
show_recent_feedback() {
    local count="${1:-5}"
    
    if [[ ! -f "$FEEDBACK_FILE" ]]; then
        echo "No feedback data available"
        return 1
    fi
    
    echo "Recent feedback (last $count):"
    echo ""
    
    tail -n "$count" "$FEEDBACK_FILE" | while read -r line; do
        local timestamp=$(echo "$line" | grep -o '"timestamp": "[^"]*"' | cut -d'"' -f4)
        local title=$(echo "$line" | grep -o '"title": "[^"]*"' | cut -d'"' -f4)
        local type=$(echo "$line" | grep -o '"type": "[^"]*"' | cut -d'"' -f4)
        local severity=$(echo "$line" | grep -o '"severity": "[^"]*"' | cut -d'"' -f4)
        
        printf "  [%s] %s (%s - %s)\n" "$timestamp" "$title" "$type" "$severity"
    done
}

# Main function
main() {
    local action="${1:-collect}"
    
    case "$action" in
        "collect"|"submit")
            collect_user_feedback
            ;;
        "status")
            show_feedback_status
            ;;
        "recent")
            local num="${2:-5}"
            show_recent_feedback "$num"
            ;;
        "help")
            echo "Orchestration Distribution System - Feedback Collection"
            echo "Usage:"
            echo "  $0 collect|submit    - Collect user feedback"
            echo "  $0 status            - Show feedback collection status"
            echo "  $0 recent [count]    - Show recent feedback items (default: 5)"
            echo "  $0 help              - Show this help"
            echo ""
            echo "Environment Variables:"
            echo "  FEEDBACK_DIR         - Directory for feedback storage (default: ./feedback)"
            ;;
        *)
            echo "Unknown action: $action"
            echo "Use 'help' for usage information"
            return 1
            ;;
    esac
}

# Run main function if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi