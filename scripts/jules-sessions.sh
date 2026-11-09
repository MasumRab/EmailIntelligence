#!/bin/bash
# Jules Sessions Helper Script

JULES_API_KEY="${JULES_API_KEY:-}"
BASE_URL="https://jules.googleapis.com/v1alpha"

if [ -z "$JULES_API_KEY" ]; then
    echo "Error: JULES_API_KEY not set"
    echo "Get your API key from: https://jules.google.com/settings#api"
    exit 1
fi

list_sessions() {
    curl -s "${BASE_URL}/sessions?pageSize=50" \
        -H "X-Goog-Api-Key: $JULES_API_KEY" | \
        jq '.sessions[] | {id: .id, title: .title, status: .status, requirePlanApproval: .requirePlanApproval, hasActivity: (.activitiesCount // 0)}'
}

list_sessions_needing_feedback() {
    echo "=== Sessions Requiring Feedback ==="
    curl -s "${BASE_URL}/sessions?pageSize=50" \
        -H "X-Goog-Api-Key: $JULES_API_KEY" | \
        jq -r '.sessions[] | select(.requirePlanApproval == true or .status == "PENDING_APPROVAL") | "\(.id) - \(.title) (status: \(.status))"' 2>/dev/null || \
    echo "No sessions requiring explicit feedback found"
}

get_session_details() {
    local session_id="$1"
    curl -s "${BASE_URL}/sessions/$session_id" \
        -H "X-Goog-Api-Key: $JULES_API_KEY"
}

list_activities() {
    local session_id="$1"
    curl -s "${BASE_URL}/sessions/$session_id/activities?pageSize=20" \
        -H "X-Goog-Api-Key: $JULES_API_KEY" | \
        jq '.activities[] | {id: .id, originator: .originator, type: (keys | first)}'
}

case "${1:-}" in
    list)
        list_sessions
        ;;
    feedback)
        list_sessions_needing_feedback
        ;;
    get)
        get_session_details "${2:-}"
        ;;
    activities)
        list_activities "${2:-}"
        ;;
    *)
        echo "Usage: $0 {list|feedback|get <id>|activities <id>}"
        echo ""
        echo "Commands:"
        echo "  list               - List all sessions"
        echo "  feedback           - List sessions needing feedback/approval"
        echo "  get <id>           - Get details of a specific session"
        echo "  activities <id>    - List activities for a session"
        ;;
esac
