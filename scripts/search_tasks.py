#!/usr/bin/env python3
"""
Search tasks by keyword in title, description, or details
Usage: python scripts/search_tasks.py <keyword> [--file FILE] [--tag TAG]
"""

import argparse
import os
import sys
from pathlib import Path

# Add the task_scripts directory to the path to import shared utilities
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "task_scripts"))
from taskmaster_common import FileValidator, SecurityValidator, TaskValidator


def format_task_match(task, keyword, show_context=False):
    """Format a matching task for display"""
    lines = [
        f"Task {task['id']}: {task['title']}",
        f"  Status: {task.get('status', 'N/A')}",
        f"  Priority: {task.get('priority', 'N/A')}",
    ]

    # Highlight matches
    if show_context:
        title = task.get("title", "")
        desc = task.get("description", "")

        # Find and highlight keyword in title
        if keyword.lower() in title.lower():
            lines.append(f"  Title match: {title[:100]}")

        # Find and highlight keyword in description
        if desc and keyword.lower() in desc.lower():
            # Extract context around match
            idx = desc.lower().find(keyword.lower())
            if idx != -1:
                start = max(0, idx - 50)
                end = min(len(desc), idx + len(keyword) + 50)
                context = desc[start:end]
                lines.append(f"  Description match: ...{context}...")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search tasks by keyword")
    parser.add_argument("keyword", help="Keyword to search for")
    parser.add_argument("--file", default="tasks/tasks.json", help="Path to tasks JSON file")
    parser.add_argument("--tag", default="master", help="Task tag (default: master)")
    parser.add_argument("--case-sensitive", action="store_true", help="Case-sensitive search")
    parser.add_argument("--show-context", action="store_true", help="Show context around matches")
    parser.add_argument("--invalid", action="store_true", help="Search in tasks_invalid.json")

    args = parser.parse_args()

    # Resolve file path
    script_dir = Path(__file__).parent.parent
    tasks_file = script_dir / "tasks/tasks_invalid.json" if args.invalid else script_dir / args.file

    # Validate path security first
    if not SecurityValidator.validate_path_security(str(tasks_file)):
        print(f"Error: Invalid or unsafe file path: {tasks_file}", file=sys.stderr)
        sys.exit(1)

    # Load tasks using secure loading
    try:
        data = FileValidator.load_json_secure(str(tasks_file))
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract tasks from data
    if args.tag in data:
        tasks = data[args.tag].get("tasks", [])
    elif "tasks" in data:
        tasks = data["tasks"]
    elif isinstance(data, list):
        tasks = data
    else:
        tasks = []

    if not tasks:
        print("No tasks found in file.")
        return

    # Use the consolidated search functionality
    matches = TaskValidator.search_tasks(tasks, args.keyword, args.case_sensitive)

    if not matches:
        print(f"No tasks found matching '{args.keyword}'")
        return

    print(f"Found {len(matches)} task(s) matching '{args.keyword}':\n")

    for task in matches:
        print(format_task_match(task, args.keyword, args.show_context))
        print()


if __name__ == "__main__":
    main()
