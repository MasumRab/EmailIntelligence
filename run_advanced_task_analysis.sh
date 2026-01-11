#!/bin/bash
#
# Advanced workflow for performing analysis on each task .md file individually.
# This workflow adds Markdown linting and task validity checks, and it ensures
# the temporary tasks.json is cleared after each task is analyzed.
#
# Usage:
#   ./run_advanced_task_analysis.sh              (Analyzes all tasks)
#   ./run_advanced_task_analysis.sh task-001   (Analyzes a specific task)
#   ./run_advanced_task_analysis.sh task-002-1 task-002-3 (Analyzes multiple specific tasks)

set -e

# --- Configuration ---
TASK_SOURCE_DIR="new_task_plan"
REPORTS_DIR="complexity_reports"
TEMP_PARENT_DIR=$(mktemp -d)
ORIGINAL_PWD=$(pwd)

# --- Argument Parsing ---
TASKS_TO_PROCESS=()
if [ "$#" -gt 0 ]; then
    echo "Processing specific tasks provided as arguments: $@"
    # Use arguments directly. The loop will construct the path.
    TASKS_TO_PROCESS=("$@")
else
    echo "No specific tasks provided. Processing all tasks found in '$TASK_SOURCE_DIR'..."
    # Find all task files and store their full paths in the array.
    while IFS= read -r line; do
        TASKS_TO_PROCESS+=("$line")
    done < <(find "$TASK_SOURCE_DIR" -maxdepth 1 -type f -name 'task-*.md')
fi

if [ ${#TASKS_TO_PROCESS[@]} -eq 0 ]; then
    echo "No tasks to process. Exiting."
    exit 0
fi


# --- Main ---
echo "Starting advanced task analysis workflow..."
echo "Reports will be saved to: $REPORTS_DIR"
echo "Temporary processing directory: $TEMP_PARENT_DIR"

mkdir -p "$REPORTS_DIR"

# --- Processing Loop ---
for task_input in "${TASKS_TO_PROCESS[@]}"; do
    
    # Determine if input is a file path or just an ID
    if [[ -f "$task_input" ]]; then
        task_file_path="$task_input"
        task_id=$(basename "$task_file_path" .md)
    else
        task_id="$task_input"
        task_file_path="$ORIGINAL_PWD/$TASK_SOURCE_DIR/${task_id}.md"
    fi

    if [ ! -f "$task_file_path" ]; then
        echo "---------------------------------"
        echo "ERROR: Task file not found for '$task_id' at path '$task_file_path'. Skipping."
        continue
    fi
    
    echo "---------------------------------"
    echo "Processing: $task_id"

    # 1. Markdown Linting
    echo "  1. Linting Markdown file with mdl..."
    LINT_REPORT_FILE="$ORIGINAL_PWD/$REPORTS_DIR/${task_id}-linting-errors.txt"
    if ! mdl "$task_file_path" > "$LINT_REPORT_FILE" 2>&1; then
        echo "  -> ERROR: Markdown linting failed for $task_id. See report: $LINT_REPORT_FILE"
        # If linting fails, we don't proceed with this task
        continue
    fi
    # If linting passed, delete the empty report file
    if [ ! -s "$LINT_REPORT_FILE" ]; then
        rm -f "$LINT_REPORT_FILE"
    fi
    echo "  -> Markdown OK."

    # 2. Generate a temporary, single-task tasks.json using the new converter
    echo "  2. Generating single-task tasks.json from markdown..."
    SINGLE_TASK_TEMP_TASKS_JSON="$TEMP_PARENT_DIR/${task_id}-single.json"
    
    if ! python3 "$ORIGINAL_PWD/scripts/convert_md_to_task_json.py" "$task_file_path" > "$SINGLE_TASK_TEMP_TASKS_JSON"; then
        echo "  -> ERROR: Failed to convert markdown to JSON for $task_id. Skipping."
        rm -f "$SINGLE_TASK_TEMP_TASKS_JSON" # Clean up potentially partial file
        continue
    fi
    
    if [ ! -s "$SINGLE_TASK_TEMP_TASKS_JSON" ]; then
        echo "  -> WARNING: Markdown to JSON conversion produced an empty file for $task_id. Skipping."
        continue
    fi
    echo "  -> Single-task tasks.json generated successfully."

    # 3. Run Complexity Analysis on the single-task tasks.json
    REPORT_FILE="$ORIGINAL_PWD/$REPORTS_DIR/${task_id}-complexity.json"
    echo "  3. Running complexity analysis..."
    python3 "$ORIGINAL_PWD/scripts/task_summary.py" --tasks-file "$SINGLE_TASK_TEMP_TASKS_JSON" --output-format json > "$REPORT_FILE"

    if [ -s "$REPORT_FILE" ]; then
        echo "  -> Complexity analysis complete."
    else
        echo "  -> WARNING: Complexity analysis did not produce a report for $task_id."
        rm -f "$REPORT_FILE"
    fi
    
    # 4. Run Task Validity Check on the single-task tasks.json
    VALIDITY_REPORT_FILE="$ORIGINAL_PWD/$REPORTS_DIR/${task_id}-validity-errors.txt"
    echo "  4. Checking for task validation errors..."
    python3 "$ORIGINAL_PWD/scripts/list_invalid_tasks.py" --tasks-file "$SINGLE_TASK_TEMP_TASKS_JSON" > "$VALIDITY_REPORT_FILE"

    if [ -s "$VALIDITY_REPORT_FILE" ]; then
        echo "  -> WARNING: Task $task_id has validation issues. See report: ${VALIDITY_REPORT_FILE}"
    else
        echo "  -> Task validity OK."
        rm -f "$VALIDITY_REPORT_FILE"
    fi

    # 5. Explicitly clean up the single-task temporary JSON file
    rm -f "$SINGLE_TASK_TEMP_TASKS_JSON"
    echo "  -> Cleanup for $task_id complete."

done

# --- Final Cleanup ---
echo "---------------------------------"
echo "Workflow finished. Cleaning up parent temporary directory..."
rm -rf "$TEMP_PARENT_DIR"
echo "Done. Reports are in the '$REPORTS_DIR' directory."

