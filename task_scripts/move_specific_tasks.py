#!/usr/bin/env python3
"""
Script to move specific tasks (by ID) and completed tasks to non_alignment_tasks.json.
Moves tasks with specific IDs (3, 4, 6) plus any tasks with status 'done'.
"""
import json
import os
import shutil
from datetime import datetime


def move_specific_and_completed_tasks(original_file_path, completed_tasks_file, specific_task_ids):
    """
    Move specific tasks by ID and completed tasks from original to completed tasks file.

    Args:
        original_file_path: Path to the original tasks.json file
        completed_tasks_file: Path where tasks should be stored
        specific_task_ids: List of task IDs to move regardless of status

    Returns:
        dict with statistics
    """
    # Make backup of original file
    backup_path = (
        f"{original_file_path}.backup_specific_move_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    shutil.copy2(original_file_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read the original tasks.json file
    with open(original_file_path, encoding="utf-8") as f:
        data = json.load(f)

    # Get the original tasks array
    original_tasks = data["master"]["tasks"]

    # Separate tasks to move (specific IDs + completed) and remaining tasks
    tasks_to_move = []
    remaining_tasks = []

    for task in original_tasks:
        if task["id"] in specific_task_ids or task.get("status") == "done":
            tasks_to_move.append(task)
        else:
            remaining_tasks.append(task)

    # Update the data with only remaining tasks
    data["master"]["tasks"] = remaining_tasks

    # Write the updated tasks back to the original file
    with open(original_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Load existing completed tasks
    existing_completed = []
    if os.path.exists(completed_tasks_file):
        with open(completed_tasks_file, encoding="utf-8") as f:
            existing_data = json.load(f)
            existing_completed = existing_data.get("completed_non_alignment_tasks", [])

    # Create a map of existing task IDs to avoid duplicates
    existing_ids = {task["id"] for task in existing_completed}

    # Add only tasks that are not already in the completed tasks file
    new_tasks_to_move = [task for task in tasks_to_move if task["id"] not in existing_ids]

    # Combine existing completed tasks with new ones
    all_unique_completed = existing_completed + new_tasks_to_move

    # Write the completed tasks to the separate file
    with open(completed_tasks_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "completed_non_alignment_tasks": all_unique_completed,
                "metadata": {
                    "moved_from_original_file": os.path.basename(original_file_path),
                    "moved_timestamp": datetime.now().isoformat(),
                    "specific_ids_requested": specific_task_ids,
                    "newly_moved_tasks": len(new_tasks_to_move),
                    "total_accumulated_completed_tasks": len(all_unique_completed),
                },
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    return {
        "specific_tasks_found": [t for t in tasks_to_move if t["id"] in specific_task_ids],
        "completed_tasks_found": [
            t
            for t in tasks_to_move
            if t.get("status") == "done" and t["id"] not in specific_task_ids
        ],
        "newly_moved": len(new_tasks_to_move),
        "total_in_completed": len(all_unique_completed),
        "removed_from_main": len(tasks_to_move),
        "remaining_in_main": len(remaining_tasks),
    }


def main():
    """Main function to run the specific move process."""
    # Define file paths (relative to project root)
    original_tasks_path = "../tasks/tasks.json"
    completed_tasks_path = "../tasks/non_alignment_tasks.json"

    # Specific task IDs to move regardless of status
    specific_task_ids = [1, 3, 4, 6]  # Including 1 as well since it was mentioned originally

    # Move tasks
    stats = move_specific_and_completed_tasks(
        original_tasks_path, completed_tasks_path, specific_task_ids
    )

    print("Specific move completed!")
    print(
        f"  - Specific tasks requested ({specific_task_ids}): {[t['id'] for t in stats['specific_tasks_found']]}"
    )
    print(f"  - Completed tasks found: {[t['id'] for t in stats['completed_tasks_found']]}")
    print(f"  - Newly moved tasks: {stats['newly_moved']}")
    print(f"  - Total tasks in completed file: {stats['total_in_completed']}")
    print(f"  - Tasks removed from main file: {stats['removed_from_main']}")
    print(f"  - Remaining tasks in main file: {stats['remaining_in_main']}")

    # Show what was moved
    if stats["newly_moved"] > 0:
        print("\nMoved tasks:")
        for task in stats["specific_tasks_found"] + stats["completed_tasks_found"]:
            print(f"  - Task {task['id']}: {task['title']} (Status: {task['status']})")
    else:
        print("\nNo new tasks were moved (they were already in the completed file).")

    print(f"\nTasks are now in: {completed_tasks_path}")
    print(f"Remaining tasks in: {original_tasks_path}")


if __name__ == "__main__":
    main()
