#!/usr/bin/env python3
"""
Script to remove duplicate tasks from non_alignment_tasks.json based on task ID.
"""
import json


def remove_duplicate_tasks(completed_tasks_file):
    """Remove duplicate tasks from the completed tasks file based on task ID."""
    # Read the completed tasks file
    with open(completed_tasks_file, encoding="utf-8") as f:
        data = json.load(f)

    # Extract the completed tasks list
    completed_tasks = data["completed_non_alignment_tasks"]

    # Remove duplicates based on task ID, keeping the first occurrence
    seen_ids = set()
    unique_tasks = []

    for task in completed_tasks:
        task_id = task["id"]
        if task_id not in seen_ids:
            seen_ids.add(task_id)
            unique_tasks.append(task)

    # Update the data with unique tasks
    data["completed_non_alignment_tasks"] = unique_tasks

    # Write back to file
    with open(completed_tasks_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Removed duplicates from {completed_tasks_file}")
    print(f"  - Original count: {len(completed_tasks)}")
    print(f"  - Unique count: {len(unique_tasks)}")
    print(f"  - Duplicates removed: {len(completed_tasks) - len(unique_tasks)}")


def main():
    completed_tasks_path = "../tasks/non_alignment_tasks.json"
    remove_duplicate_tasks(completed_tasks_path)


if __name__ == "__main__":
    main()
