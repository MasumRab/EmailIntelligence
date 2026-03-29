#!/bin/bash
# Custom merge driver for backlog task files
# Prioritizes completion status: Done > In Progress > To Do

set -e

# Arguments: %O %A %B
ANCESTOR="$1"
OURS="$2"
THEIRS="$3"

# Function to extract status from frontmatter
get_status() {
    local file="$1"
    grep "^status:" "$file" | head -1 | sed 's/status: *//' | tr -d '"' || echo "To Do"
}

# Function to count checked acceptance criteria
count_checked_ac() {
    local file="$1"
    local count
    # Use command substitution which captures output regardless of exit code
    count=$(grep -c "\[x\]" "$file" 2>/dev/null)
    echo "$count"
}

# Function to check if file has implementation notes
has_notes() {
    local file="$1"
    grep -q "SECTION:NOTES:BEGIN" "$file" && echo "yes" || echo "no"
}

# Get status for each version
ancestor_status=$(get_status "$ANCESTOR")
ours_status=$(get_status "$OURS")
theirs_status=$(get_status "$THEIRS")

# Status priority: Done > Completed > In Progress > To Do > Empty/Unknown
get_priority() {
    case "$1" in
        "Done"|"Completed") echo 4 ;;
        "In Progress") echo 3 ;;
        "To Do") echo 2 ;;
        "") echo 1 ;;  # Empty status gets lowest priority
        "Not Started") echo 1 ;;  # Explicitly handle Not Started as low priority 
        *) echo 1 ;;  # Any other unrecognized status gets low priority
    esac
}

ours_priority=$(get_priority "$ours_status")
theirs_priority=$(get_priority "$theirs_status")

# Compare priorities
if [ "$ours_priority" -gt "$theirs_priority" ]; then
    # Our version has higher priority, use ours
    cat "$OURS" > "$2"
    exit 0
elif [ "$theirs_priority" -gt "$ours_priority" ]; then
    # Their version has higher priority, use theirs
    cat "$THEIRS" > "$2"
    exit 0
else
    # Same priority, compare other factors
    ours_checked=$(count_checked_ac "$OURS")
    theirs_checked=$(count_checked_ac "$THEIRS")

    if [ "$ours_checked" -gt "$theirs_checked" ]; then
        cat "$OURS" > "$2"
        exit 0
    elif [ "$theirs_checked" -gt "$ours_checked" ]; then
        cat "$THEIRS" > "$2"
        exit 0
    fi

    # If still tied, prefer the version with implementation notes
    ours_has_notes=$(has_notes "$OURS")
    theirs_has_notes=$(has_notes "$THEIRS")

    if [ "$ours_has_notes" = "yes" ] && [ "$theirs_has_notes" = "no" ]; then
        cat "$OURS" > "$2"
        exit 0
    elif [ "$theirs_has_notes" = "yes" ] && [ "$ours_has_notes" = "no" ]; then
        cat "$THEIRS" > "$2"
        exit 0
    fi

    # Final fallback: use our version
    cat "$OURS" > "$2"
    exit 0
fi