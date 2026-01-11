#!/usr/bin/env python3
"""
Generate a comprehensive summary of all tasks across all JSON files
Usage: python scripts/task_summary.py
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_tasks(file_path, tag="master"):
    """Load tasks from tasks.json file"""
    try:
        with open(file_path) as f:
            data = json.load(f)

        if tag in data:
            return data[tag].get("tasks", [])
        elif "tasks" in data:
            return data["tasks"]
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def parse_invalid_tasks(file_path):
    """Parse tasks_invalid.json (may be malformed)"""
    try:
        with open(file_path) as f:
            content = f.read()

        # Try normal JSON parsing
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "tasks" in data:
                return data["tasks"]
        except json.JSONDecodeError:
            pass

        # Fallback: extract top-level tasks
        import re

        tasks = []
        lines = content.split("\n")
        depth = 0
        in_subtasks = False

        for i, line in enumerate(lines):
            depth += line.count("{") - line.count("}")
            if '"subtasks"' in line and "[" in line:
                in_subtasks = True
            if in_subtasks and depth <= 1:
                in_subtasks = False

            if not in_subtasks and depth == 1:
                id_match = re.search(r'"id":\s*(\d+)', line)
                if id_match:
                    task_id = int(id_match.group(1))
                    if 1 <= task_id <= 13:
                        title = None
                        status = None
                        for j in range(i, min(i + 30, len(lines))):
                            if title is None:
                                title_match = re.search(r'"title":\s*"([^"]+)"', lines[j])
                                if title_match:
                                    title = title_match.group(1)
                            if status is None:
                                status_match = re.search(r'"status":\s*"([^"]+)"', lines[j])
                                if status_match:
                                    status = status_match.group(1)
                            if title and status:
                                break

                        if title and status:
                            tasks.append({"id": task_id, "title": title, "status": status})

        seen = set()
        return [t for t in tasks if t["id"] not in seen and not seen.add(t["id"])]
    except FileNotFoundError:
        return []


def count_subtasks(task):
    """Count total subtasks recursively"""
    count = len(task.get("subtasks", []))
    for subtask in task.get("subtasks", []):
        count += count_subtasks(subtask)
    return count


def print_summary(tasks_json, source_name="tasks.json"):
    """Prints a summary for a given list of tasks."""
    print("=" * 70)
    print(f"TASK SUMMARY REPORT FOR: {source_name}")
    print("=" * 70)
    print()

    if not tasks_json:
        print("No tasks found.")
        return

    status_count = defaultdict(int)
    priority_count = defaultdict(int)
    total_subtasks = 0

    for task in tasks_json:
        status_count[task.get("status", "unknown")] += 1
        priority_count[task.get("priority", "unknown")] += 1
        total_subtasks += count_subtasks(task)

    print(f"Main Tasks ({source_name}) Breakdown:")
    print(f"  Total tasks: {len(tasks_json)}")
    print(f"  Total subtasks: {total_subtasks}")
    print()
    print("  By Status:")
    for status, count in sorted(status_count.items()):
        print(f"    {status:15} {count:3} tasks")
    print()
    print("  By Priority:")
    for priority, count in sorted(priority_count.items()):
        print(f"    {priority:15} {count:3} tasks")
    print()

    task_ids = [t.get("id") for t in tasks_json if t.get("id") is not None]
    if task_ids:
        try:
            numeric_ids = [int(i) for i in task_ids]
            print(f"Task ID Range: {min(numeric_ids)} - {max(numeric_ids)}")
            missing = [i for i in range(min(numeric_ids), max(numeric_ids) + 1) if i not in numeric_ids]
            if missing:
                print(f"Missing IDs: {missing}")
        except (ValueError, TypeError):
            print(f"Task IDs are not all numeric: {task_ids}")
        print()

    print(f"All Tasks ({source_name}):")
    # Sort by numeric part of ID if possible
    try:
        sorted_tasks = sorted(tasks_json, key=lambda x: int(str(x.get("id", "0")).split('.')[0]))
    except (ValueError, TypeError):
        sorted_tasks = sorted(tasks_json, key=lambda x: str(x.get("id", "")))

    for task in sorted_tasks:
        subtask_count = count_subtasks(task)
        task_id_str = str(task.get('id', 'N/A'))
        print(
            f"  {task_id_str:5} [{task.get('status', 'N/A'):12}] [{task.get('priority', 'N/A'):8}] "
            f"({subtask_count:2} subtasks) {task.get('title', 'No Title')}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(description="Generate a comprehensive summary of all tasks across all JSON files")
    parser.add_argument("--tasks-file", help="Path to a single tasks JSON file to summarize.")
    args = parser.parse_args()

    if args.tasks_file:
        tasks = load_tasks(args.tasks_file)
        print_summary(tasks, source_name=args.tasks_file)
    else:
        script_dir = Path(__file__).parent.parent
        tasks_json = load_tasks(script_dir / "tasks/tasks.json", "master")
        tasks_expanded = load_tasks(script_dir / "tasks/tasks_expanded.json", "master")
        tasks_new = load_tasks(script_dir / "tasks/tasks_new.json")
        tasks_invalid = parse_invalid_tasks(script_dir / "tasks/tasks_invalid.json")

        print("=" * 70)
        print("TASK SUMMARY REPORT")
        print("=" * 70)
        print()
        
        print("Tasks by File:")
        print(f"  tasks.json:           {len(tasks_json)} tasks")
        print(f"  tasks_expanded.json:  {len(tasks_expanded)} tasks")
        print(f"  tasks_new.json:       {len(tasks_new)} tasks")
        print(f"  tasks_invalid.json:   {len(tasks_invalid)} tasks")
        print()

        if tasks_json:
            print_summary(tasks_json, "tasks.json")

        if tasks_invalid:
            print("Invalid/Completed Tasks (tasks_invalid.json):")
            invalid_status_count = defaultdict(int)
            for task in tasks_invalid:
                invalid_status_count[task.get("status", "unknown")] += 1
            print(f"  Total: {len(tasks_invalid)}")
            print("  By Status:")
            for status, count in sorted(invalid_status_count.items()):
                print(f"    {status:15} {count:3} tasks")
            print()


if __name__ == "__main__":
    main()
