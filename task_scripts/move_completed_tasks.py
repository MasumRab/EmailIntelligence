#!/usr/bin/env python3
"""
Script to move completed tasks from tasks.json to non_alignment_tasks.json.
This separates completed non-alignment tasks from active tasks.
"""
import json
import os
import shutil
from datetime import datetime


def move_completed_tasks(original_file_path, completed_tasks_file):
    """
    Move tasks with status 'done' from original tasks file to completed tasks file.

    Args:
        original_file_path: Path to the original tasks.json file
        completed_tasks_file: Path where completed tasks should be stored

    Returns:
        Number of completed tasks moved
    """
    # Make backup of original file
    backup_path = f"{original_file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(original_file_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read the original tasks.json file
    with open(original_file_path, encoding="utf-8") as f:
        data = json.load(f)

    # Get the original tasks array
    original_tasks = data["master"]["tasks"]

    # Separate completed and remaining tasks
    completed_tasks = []
    remaining_tasks = []

    for task in original_tasks:
        if task.get("status") == "done":
            completed_tasks.append(task)
        else:
            remaining_tasks.append(task)

    # Update the data with only remaining (non-completed) tasks
    data["master"]["tasks"] = remaining_tasks

    # Write the updated tasks back to the original file
    with open(original_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Load existing completed tasks or create new structure
    if os.path.exists(completed_tasks_file):
        with open(completed_tasks_file, encoding="utf-8") as f:
            existing_data = json.load(f)
        # Append new completed tasks to existing ones
        existing_completed = existing_data.get("completed_non_alignment_tasks", [])
    else:
        existing_completed = []

    # Combine existing completed tasks with new ones
    all_completed = existing_completed + completed_tasks

    # Write the completed tasks to the separate file
    with open(completed_tasks_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "completed_non_alignment_tasks": all_completed,
                "metadata": {
                    "moved_from_original_file": os.path.basename(original_file_path),
                    "moved_timestamp": datetime.now().isoformat(),
                    "total_moved_tasks": len(completed_tasks),
                    "total_accumulated_completed_tasks": len(all_completed),
                },
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    return len(completed_tasks)


def main():
    """Main function to run the move process."""
    # Define file paths (relative to project root)
    original_tasks_path = "../tasks/tasks.json"
    completed_tasks_path = "../tasks/non_alignment_tasks.json"

    # Move completed tasks
    count = move_completed_tasks(original_tasks_path, completed_tasks_path)

    print(
        f"Successfully moved {count} completed tasks from {original_tasks_path} to {completed_tasks_path}"
    )

    # Show what was moved
    with open(completed_tasks_path, encoding="utf-8") as f:
        data = json.load(f)
        print("Moved tasks:")
        for task in data["completed_non_alignment_tasks"]:
            print(f"  - Task {task['id']}: {task['title']} (Status: {task['status']})")

    # Show remaining tasks in main file
    with open(original_tasks_path, encoding="utf-8") as f:
        data = json.load(f)
        remaining_count = len(data["master"]["tasks"])
        print(f"\nRemaining {remaining_count} tasks in main tasks.json")


if __name__ == "__main__":
    main()
