#!/usr/bin/env python3
"""
Generate a comprehensive summary of all tasks across all JSON files
Usage: python scripts/task_summary.py
"""

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


def main():
    script_dir = Path(__file__).parent.parent

    # Load tasks from different files
    tasks_json = load_tasks(script_dir / "tasks/tasks.json", "master")
    tasks_expanded = load_tasks(script_dir / "tasks/tasks_expanded.json", "master")
    tasks_new = load_tasks(script_dir / "tasks/tasks_new.json")
    tasks_invalid = parse_invalid_tasks(script_dir / "tasks/tasks_invalid.json")

    print("=" * 70)
    print("TASK SUMMARY REPORT")
    print("=" * 70)
    print()

    # Summary by file
    print("Tasks by File:")
    print(f"  tasks.json:           {len(tasks_json)} tasks")
    print(f"  tasks_expanded.json:  {len(tasks_expanded)} tasks")
    print(f"  tasks_new.json:       {len(tasks_new)} tasks")
    print(f"  tasks_invalid.json:   {len(tasks_invalid)} tasks")
    print()

    # Status breakdown for main tasks
    if tasks_json:
        status_count = defaultdict(int)
        priority_count = defaultdict(int)
        total_subtasks = 0

        for task in tasks_json:
            status_count[task.get("status", "unknown")] += 1
            priority_count[task.get("priority", "unknown")] += 1
            total_subtasks += count_subtasks(task)

        print("Main Tasks (tasks.json) Breakdown:")
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

    # Invalid tasks summary
    if tasks_invalid:
        invalid_status_count = defaultdict(int)
        for task in tasks_invalid:
            invalid_status_count[task.get("status", "unknown")] += 1

        print("Invalid/Completed Tasks (tasks_invalid.json):")
        print(f"  Total: {len(tasks_invalid)}")
        print("  By Status:")
        for status, count in sorted(invalid_status_count.items()):
            print(f"    {status:15} {count:3} tasks")
        print()

    # Task ID ranges
    if tasks_json:
        task_ids = [t["id"] for t in tasks_json]
        print(f"Task ID Range: {min(task_ids)} - {max(task_ids)}")
        missing = [i for i in range(min(task_ids), max(task_ids) + 1) if i not in task_ids]
        if missing:
            print(f"Missing IDs: {missing}")
        print()

    # List all task IDs and titles
    if tasks_json:
        print("All Tasks (tasks.json):")
        for task in sorted(tasks_json, key=lambda x: x["id"]):
            subtask_count = count_subtasks(task)
            print(
                f"  {task['id']:3} [{task.get('status', 'N/A'):12}] [{task.get('priority', 'N/A'):8}] "
                f"({subtask_count:2} subtasks) {task['title']}"
            )
        print()


if __name__ == "__main__":
    main()
