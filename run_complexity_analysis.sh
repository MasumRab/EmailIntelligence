#!/bin/bash
#
# Workflow for performing a Task Master complexity analysis for each task .md file
# individually without uploading all tasks into the main tasks.json at once.
# This script uses tasks.json as a temporary holding area for one task at a time.

set -e

# --- Configuration ---
TASK_SOURCE_DIR="new_task_plan/task_files/subtasks"
REPORTS_DIR="complexity_reports"
TEMP_PARENT_DIR=$(mktemp -d)
ORIGINAL_PWD=$(pwd)

# --- Main ---
echo "Starting complexity analysis workflow..."
echo "Reports will be saved to: $REPORTS_DIR"
echo "Temporary processing directory: $TEMP_PARENT_DIR"

mkdir -p "$REPORTS_DIR"

# Find and process each task markdown file
find "$TASK_SOURCE_DIR" -type f -name 'task-*.md' | while read -r task_file_path; do
    task_id=$(basename "$task_file_path" .md)
    echo "---------------------------------"
    echo "Processing: $task_id"

    # 1. Isolate the task file in a temporary directory
    SINGLE_TASK_TEMP_DIR="$TEMP_PARENT_DIR/$task_id"
    # Mimic the nested structure the script might expect
    mkdir -p "$SINGLE_TASK_TEMP_DIR/new_task_plan/task_files/subtasks"
    cp "$task_file_path" "$SINGLE_TASK_TEMP_DIR/new_task_plan/task_files/subtasks/"

    # 2. Generate a temporary, single-task tasks.json
    cd "$SINGLE_TASK_TEMP_DIR"
    TEMP_TASKMASTER_DIR=".taskmaster/tasks"
    mkdir -p "$TEMP_TASKMASTER_DIR"
    TEMP_TASKS_JSON="$TEMP_TASKMASTER_DIR/tasks.json"

    echo "  -> Generating temporary tasks.json..."
    # Assuming the script searches from the current dir and places tasks.json in a relative path
    python3 "$ORIGINAL_PWD/scripts/regenerate_tasks_from_plan.py" >/dev/null 2>&1

    if [ ! -s "$TEMP_TASKS_JSON" ]; then
        echo "  -> WARNING: Failed to generate temporary tasks.json for $task_id. Skipping."
        cd "$ORIGINAL_PWD"
        continue
    fi

    # 3. Run complexity analysis on the single-task tasks.json
    REPORT_FILE="$ORIGINAL_PWD/$REPORTS_DIR/${task_id}-complexity.json"
    echo "  -> Running analysis and generating report: $REPORT_FILE"

    # Using task_summary.py as the analysis tool.
    # This command reads the temporary tasks.json and writes a summary to the report file.
    python3 "$ORIGINAL_PWD/scripts/task_summary.py" --tasks-file "$TEMP_TASKS_JSON" --output-format json > "$REPORT_FILE"

    if [ -s "$REPORT_FILE" ]; then
        echo "  -> Analysis complete for $task_id."
    else
        echo "  -> WARNING: Analysis did not produce a report for $task_id."
        rm -f "$REPORT_FILE"
    fi

    cd "$ORIGINAL_PWD"
done

# --- Cleanup ---
echo "---------------------------------"
echo "Workflow finished. Cleaning up temporary files..."
rm -rf "$TEMP_PARENT_DIR"
echo "Done. Reports are in the '$REPORTS_DIR' directory."
