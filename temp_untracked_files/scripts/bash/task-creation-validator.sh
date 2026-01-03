#!/bin/bash

################################################################################
# Task Creation Validator
# 
# Purpose: Systematically check all task files before creating a new task
# Usage: ./scripts/bash/task-creation-validator.sh "Your Task Title" [keywords...]
# Example: ./scripts/bash/task-creation-validator.sh "Systematic Branch Analysis" branch analyze documentation
#
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
TASK_TITLE="${1:-}"
KEYWORDS="${@:2}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# File paths
TASKS_JSON="${REPO_ROOT}/.taskmaster/tasks/tasks.json"
TASKS_DIR="${REPO_ROOT}/.taskmaster/tasks"
BACKLOG_DIR="${REPO_ROOT}/backlog"
SPECS_DIR="${REPO_ROOT}/specs"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}\n"
}

print_section() {
    echo -e "\n${YELLOW}→ $1${NC}"
}

print_result() {
    local status=$1
    local message=$2
    
    if [ "$status" = "pass" ]; then
        echo -e "${GREEN}✓${NC} $message"
    elif [ "$status" = "warn" ]; then
        echo -e "${YELLOW}⚠${NC} $message"
    else
        echo -e "${RED}✗${NC} $message"
    fi
}

check_file_exists() {
    if [ ! -f "$1" ]; then
        print_result "fail" "Required file not found: $1"
        exit 1
    fi
}

################################################################################
# Validation Functions
################################################################################

validate_inputs() {
    print_header "1. Input Validation"
    
    if [ -z "$TASK_TITLE" ]; then
        print_result "fail" "Task title is required"
        echo "Usage: $0 \"Task Title\" [keyword1] [keyword2] ..."
        exit 1
    fi
    
    print_result "pass" "Task title provided: '$TASK_TITLE'"
    
    if [ -n "$KEYWORDS" ]; then
        print_result "pass" "Search keywords: $KEYWORDS"
    else
        print_result "warn" "No additional keywords provided (optional)"
    fi
}

check_files_exist() {
    print_header "2. Repository File Check"
    
    check_file_exists "$TASKS_JSON"
    print_result "pass" "Task database found: .taskmaster/tasks/tasks.json"
    
    if [ -d "$TASKS_DIR" ]; then
        local count=$(find "$TASKS_DIR" -name "*.md" 2>/dev/null | wc -l)
        print_result "pass" "Task markdown files found: $count files"
    fi
}

search_task_database() {
    print_section "Searching Task Database"
    
    # Extract first few words from task title for search
    local search_term=$(echo "$TASK_TITLE" | awk '{print $1}' | tr '[:upper:]' '[:lower:]')
    
    echo "Searching for tasks related to: '$search_term'"
    echo ""
    
    # Get all tasks
    python3 << PYTHON_EOF
import json
import sys
import re

search_term = "$search_term"
with open("$TASKS_JSON", 'r') as f:
    data = json.load(f)
    tasks = data['master']['tasks']
    
    print("Current Tasks in Database:")
    print("-" * 80)
    
    for task in tasks:
        task_id = task['id']
        title = task['title']
        status = task['status']
        
        # Highlight if search term appears in title
        if search_term.lower() in title.lower():
            print(f"  ⚠ Task {task_id}: {title}")
            print(f"     Status: {status}")
            print(f"     Priority: {task.get('priority', 'N/A')}")
        else:
            print(f"  • Task {task_id}: {title}")
    
    print("\n" + "-" * 80)
    print(f"Total tasks: {len(tasks)}")
PYTHON_EOF
}

search_markdown_files() {
    print_section "Searching Markdown Files"
    
    local search_term=$(echo "$TASK_TITLE" | awk '{print tolower($1)}')
    
    echo "Searching .taskmaster/tasks/ for markdown files..."
    if [ -d "$TASKS_DIR" ]; then
        local matches=$(grep -ri "$search_term" "$TASKS_DIR" 2>/dev/null | wc -l)
        if [ "$matches" -gt 0 ]; then
            print_result "warn" "Found $matches matching lines in task markdown files"
            echo ""
            grep -rn "$search_term" "$TASKS_DIR" 2>/dev/null | head -5
            echo "(showing first 5 matches)"
        else
            print_result "pass" "No matching task markdown files found"
        fi
    fi
}

search_backlog() {
    print_section "Searching Backlog Directory"
    
    if [ -d "$BACKLOG_DIR" ]; then
        local matches=$(grep -ri "$TASK_TITLE" "$BACKLOG_DIR" 2>/dev/null | wc -l)
        if [ "$matches" -gt 0 ]; then
            print_result "warn" "Found $matches matches in backlog/"
            echo ""
            grep -rn "$TASK_TITLE" "$BACKLOG_DIR" 2>/dev/null | head -3
        else
            print_result "pass" "No matches in backlog/"
        fi
    else
        print_result "pass" "No backlog/ directory found (not required)"
    fi
}

search_specs() {
    print_section "Searching Specifications"
    
    if [ -d "$SPECS_DIR" ]; then
        local matches=$(grep -ri "$TASK_TITLE" "$SPECS_DIR" 2>/dev/null | wc -l)
        if [ "$matches" -gt 0 ]; then
            print_result "warn" "Found $matches matches in specs/"
        else
            print_result "pass" "No matches in specs/"
        fi
    else
        print_result "pass" "No specs/ directory found (not required)"
    fi
}

search_root_markdown() {
    print_section "Searching Root-Level Markdown"
    
    local search_term=$(echo "$TASK_TITLE" | awk '{print tolower($1)}')
    local matches=$(grep -ri "$search_term" "$REPO_ROOT" --include="*.md" \
                   --exclude-dir=.taskmaster --exclude-dir=backlog \
                   --exclude-dir=specs --exclude-dir=.git --exclude-dir=node_modules \
                   2>/dev/null | wc -l)
    
    if [ "$matches" -gt 0 ]; then
        print_result "warn" "Found $matches matches in root .md files"
        echo ""
        grep -rn "$search_term" "$REPO_ROOT" --include="*.md" \
             --exclude-dir=.taskmaster --exclude-dir=backlog \
             --exclude-dir=specs --exclude-dir=.git --exclude-dir=node_modules \
             2>/dev/null | head -3
    else
        print_result "pass" "No matches in root-level markdown files"
    fi
}

analyze_dependencies() {
    print_section "Analyzing Task Dependencies"
    
    echo "Extracting task dependency graph..."
    echo ""
    
    python3 << PYTHON_EOF
import json

with open("$TASKS_JSON", 'r') as f:
    data = json.load(f)
    tasks = data['master']['tasks']
    
    print("Task Dependencies:")
    print("-" * 60)
    
    for task in tasks:
        deps = task.get('dependencies', [])
        if deps:
            print(f"Task {task['id']}: depends on {deps}")
    
    print("\n" + "-" * 60)
    print("\nHighest Priority Tasks (high):")
    for task in tasks:
        if task.get('priority') == 'high':
            print(f"  • Task {task['id']}: {task['title']}")
PYTHON_EOF
}

check_in_progress_tasks() {
    print_section "Checking In-Progress Tasks"
    
    python3 << PYTHON_EOF
import json

with open("$TASKS_JSON", 'r') as f:
    data = json.load(f)
    tasks = data['master']['tasks']
    
    in_progress = [t for t in tasks if t['status'] in ['in-progress', 'in_progress']]
    
    if in_progress:
        print("Currently In-Progress Tasks:")
        print("-" * 60)
        for task in in_progress:
            print(f"Task {task['id']}: {task['title']}")
            print(f"  Status: {task['status']}")
    else:
        print("No tasks currently in progress.")
PYTHON_EOF
}

get_next_task_id() {
    print_section "Next Available Task ID"
    
    python3 << PYTHON_EOF
import json

with open("$TASKS_JSON", 'r') as f:
    data = json.load(f)
    tasks = data['master']['tasks']
    
    task_ids = [t['id'] for t in tasks]
    
    if task_ids:
        max_id = max(task_ids) if isinstance(task_ids[0], int) else max([int(str(t).split('.')[0]) for t in task_ids])
        next_id = max_id + 1
        print(f"Current task IDs: {sorted(task_ids)}")
        print(f"Next available ID: {next_id}")
    else:
        print("No tasks found. Next ID: 1")
PYTHON_EOF
}

check_keywords() {
    print_section "Keyword Search"
    
    if [ -n "$KEYWORDS" ]; then
        echo "Searching for additional keywords..."
        echo ""
        
        for keyword in $KEYWORDS; do
            echo "Searching for: '$keyword'"
            local matches=$(grep -ri "$keyword" "$TASKS_JSON" "$TASKS_DIR" 2>/dev/null | wc -l)
            if [ "$matches" -gt 0 ]; then
                print_result "warn" "Found $matches matches for '$keyword'"
            else
                print_result "pass" "No matches for '$keyword'"
            fi
        done
    else
        print_result "warn" "No additional keywords provided"
    fi
}

generate_summary() {
    print_header "Summary"
    
    echo -e "${YELLOW}Task Creation Readiness:${NC}"
    echo ""
    echo "Task Title: $TASK_TITLE"
    echo "Search Keywords: ${KEYWORDS:-none}"
    echo ""
    echo "Next Steps:"
    echo "1. Review all search results above"
    echo "2. If no duplicates found → proceed with task creation"
    echo "3. If duplicates found → enhance existing task OR clarify scope difference"
    echo "4. Run: task-master add-task --prompt=\"....\""
    echo "5. Run: task-master expand --id=<new-id> to create subtasks"
    echo ""
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header "Task Creation Validator"
    echo "Task Title: $TASK_TITLE"
    echo "Repository: $REPO_ROOT"
    
    # Run validation sequence
    validate_inputs
    check_files_exist
    search_task_database
    search_markdown_files
    search_backlog
    search_specs
    search_root_markdown
    analyze_dependencies
    check_in_progress_tasks
    get_next_task_id
    check_keywords
    generate_summary
}

# Execute main
main "$@"
