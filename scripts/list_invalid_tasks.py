#!/usr/bin/env python3
"""
List tasks from tasks_invalid.json (completed or invalidated tasks)
Usage: python scripts/list_invalid_tasks.py [--status STATUS]
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_invalid_tasks(file_path):
    """
    Parse tasks_invalid.json which may be malformed JSON.
    Extracts top-level tasks (IDs 1-13) that are not nested in subtasks.
    """
    try:
        with open(file_path) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found", file=sys.stderr)
        return []

    # Try normal JSON parsing first
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "tasks" in data:
            return data["tasks"]
        return []
    except json.JSONDecodeError:
        # If JSON is malformed, use regex parsing
        pass

    # Fallback: regex-based parsing for malformed JSON
    tasks = []
    lines = content.split("\n")
    depth = 0
    in_subtasks = False

    for i, line in enumerate(lines):
        # Track nesting depth
        depth += line.count("{") - line.count("}")

        # Check if we're entering/exiting subtasks
        if '"subtasks"' in line and "[" in line:
            in_subtasks = True
        if in_subtasks and depth <= 1:
            in_subtasks = False

        # Look for root-level task IDs (id 1-13, not in subtasks)
        if not in_subtasks and depth == 1:
            id_match = re.search(r'"id":\s*(\d+)', line)
            if id_match:
                task_id = int(id_match.group(1))
                if 1 <= task_id <= 13:
                    # Find title and status in nearby lines
                    title = None
                    status = None
                    priority = None

                    for j in range(i, min(i + 30, len(lines))):
                        if title is None:
                            title_match = re.search(r'"title":\s*"([^"]+)"', lines[j])
                            if title_match:
                                title = title_match.group(1)
                        if status is None:
                            status_match = re.search(r'"status":\s*"([^"]+)"', lines[j])
                            if status_match:
                                status = status_match.group(1)
                        if priority is None:
                            priority_match = re.search(r'"priority":\s*"([^"]+)"', lines[j])
                            if priority_match:
                                priority = priority_match.group(1)
                        if title and status:
                            break

                    if title and status:
                        tasks.append(
                            {
                                "id": task_id,
                                "title": title,
                                "status": status,
                                "priority": priority or "N/A",
                            }
                        )

    # Remove duplicates, keep first occurrence
    seen = set()
    unique_tasks = []
    for task in tasks:
        if task["id"] not in seen:
            seen.add(task["id"])
            unique_tasks.append(task)

    return sorted(unique_tasks, key=lambda x: x["id"])


def main():
    parser = argparse.ArgumentParser(description="List tasks from tasks_invalid.json")
    parser.add_argument("--status", help="Filter by status")
    parser.add_argument(
        "--file", default="tasks/tasks_invalid.json", help="Path to tasks_invalid.json"
    )

    args = parser.parse_args()

    # Resolve file path relative to script location
    script_dir = Path(__file__).parent.parent
    invalid_file = script_dir / args.file

    tasks = parse_invalid_tasks(invalid_file)

    if not tasks:
        print("No tasks found.")
        return

    # Apply status filter
    if args.status:
        tasks = [t for t in tasks if t.get("status") == args.status]

    print("Tasks in tasks_invalid.json:\n")
    print(f"Total: {len(tasks)}\n")

    for task in tasks:
        print(f"Task {task['id']}: {task['title']}")
        print(f"  Status: {task['status']}")
        print(f"  Priority: {task.get('priority', 'N/A')}")
        print()


if __name__ == "__main__":
    main()
