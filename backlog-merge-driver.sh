#!/bin/bash
#
# Backlog.md Git Merge Driver
# Automatically resolves merge conflicts in backlog task files
#
# This driver prioritizes:
# 1. Completion status (Done > In Progress > To Do)
# 2. Checked acceptance criteria
# 3. Detailed implementation notes
# 4. Assignee information

set -e

# Input files from git
ANCESTOR="$1"
CURRENT="$2"
OTHER="$3"

# Output file that will be written to working directory
OUTPUT="$4"

# Temporary files for processing
TEMP_CURRENT=$(mktemp)
TEMP_OTHER=$(mktemp)
TEMP_ANCESTOR=$(mktemp)

cp "$CURRENT" "$TEMP_CURRENT"
cp "$OTHER" "$TEMP_OTHER"
cp "$ANCESTOR" "$TEMP_ANCESTOR"

# Function to extract status from a task file
get_status() {
    local file="$1"
    grep "^status:" "$file" | head -1 | sed 's/status: *//' | tr -d '\n\r' || echo ""
}

# Function to get completion priority (higher number = higher priority)
get_status_priority() {
    local status="$1"
    case "$status" in
        "Done") echo "3" ;;
        "In Progress") echo "2" ;;
        "To Do") echo "1" ;;
        *) echo "0" ;;
    esac
}

# Function to count checked acceptance criteria
count_checked_ac() {
    local file="$1"
    grep -c "^- \[x\]" "$file" || echo "0"
}

# Function to check if implementation notes exist and are detailed
has_implementation_notes() {
    local file="$1"
    local notes_section=$(sed -n '/^## Implementation Notes/,/^## /{p}' "$file" | wc -l)
    if [ "$notes_section" -gt 3 ]; then
        echo "1"
    else
        echo "0"
    fi
}

# Extract status from all versions
STATUS_CURRENT=$(get_status "$TEMP_CURRENT")
STATUS_OTHER=$(get_status "$TEMP_OTHER")
STATUS_ANCESTOR=$(get_status "$TEMP_ANCESTOR")

PRIORITY_CURRENT=$(get_status_priority "$STATUS_CURRENT")
PRIORITY_OTHER=$(get_status_priority "$STATUS_OTHER")

# Count checked ACs
AC_CURRENT=$(count_checked_ac "$TEMP_CURRENT")
AC_OTHER=$(count_checked_ac "$TEMP_OTHER")

# Check for implementation notes
NOTES_CURRENT=$(has_implementation_notes "$TEMP_CURRENT")
NOTES_OTHER=$(has_implementation_notes "$TEMP_OTHER")

echo "Merge Driver Analysis:" >&2
echo "  Current: status='$STATUS_CURRENT' (priority=$PRIORITY_CURRENT), ACs=$AC_CURRENT, notes=$NOTES_CURRENT" >&2
echo "  Other:   status='$STATUS_OTHER' (priority=$PRIORITY_OTHER), ACs=$AC_OTHER, notes=$NOTES_OTHER" >&2

# Decision logic
if [ "$PRIORITY_CURRENT" -gt "$PRIORITY_OTHER" ]; then
    echo "Choosing CURRENT version (higher status priority)" >&2
    cp "$TEMP_CURRENT" "$OUTPUT"
elif [ "$PRIORITY_CURRENT" -lt "$PRIORITY_OTHER" ]; then
    echo "Choosing OTHER version (higher status priority)" >&2
    cp "$TEMP_OTHER" "$OUTPUT"
elif [ "$AC_CURRENT" -gt "$AC_OTHER" ]; then
    echo "Choosing CURRENT version (more checked ACs)" >&2
    cp "$TEMP_CURRENT" "$OUTPUT"
elif [ "$AC_CURRENT" -lt "$AC_OTHER" ]; then
    echo "Choosing OTHER version (more checked ACs)" >&2
    cp "$TEMP_OTHER" "$OUTPUT"
elif [ "$NOTES_CURRENT" -gt "$NOTES_OTHER" ]; then
    echo "Choosing CURRENT version (has implementation notes)" >&2
    cp "$TEMP_CURRENT" "$OUTPUT"
elif [ "$NOTES_CURRENT" -lt "$NOTES_OTHER" ]; then
    echo "Choosing OTHER version (has implementation notes)" >&2
    cp "$TEMP_OTHER" "$OUTPUT"
else
    # If all metrics are equal, prefer the current branch (working directory)
    echo "Choosing CURRENT version (equal metrics, preserving working directory)" >&2
    cp "$TEMP_CURRENT" "$OUTPUT"
fi

# Cleanup
rm -f "$TEMP_CURRENT" "$TEMP_OTHER" "$TEMP_ANCESTOR"

exit 0
