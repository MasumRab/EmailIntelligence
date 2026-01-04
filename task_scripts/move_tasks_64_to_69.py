#!/usr/bin/env python3
"""
Script to move tasks 64-69 from tasks.json to non_alignment_tasks.json
"""
import json
import shutil
from datetime import datetime


def move_tasks_range(source_file, dest_file, task_ids_to_move):
    """
    Move specific tasks by ID range from source file to destination file.

    Args:
        source_file: Path to the source tasks.json file
        dest_file: Path to the destination non_alignment_tasks.json file
        task_ids_to_move: List of task IDs to move

    Returns:
        dict with statistics
    """
    # Make backup of source file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{source_file}.backup_move_range_{timestamp}"
    shutil.copy2(source_file, backup_path)
    print(f"Created backup: {backup_path}")

    # Read the source tasks file
    with open(source_file, encoding="utf-8") as f:
        source_data = json.load(f)

    # Get the source tasks array
    source_tasks = source_data["master"]["tasks"]

    # Separate tasks to move and remaining tasks
    tasks_to_move = []
    remaining_tasks = []

    for task in source_tasks:
        if task["id"] in task_ids_to_move:
            # Change status to 'done' when moving to completed tasks
            task_copy = task.copy()  # Make a copy to avoid modifying original
            task_copy["status"] = "done"  # Mark as completed when moved
            tasks_to_move.append(task_copy)
        else:
            remaining_tasks.append(task)

    # Update the source data with only remaining tasks
    source_data["master"]["tasks"] = remaining_tasks

    # Write the updated source tasks back to the file
    with open(source_file, "w", encoding="utf-8") as f:
        json.dump(source_data, f, indent=2, ensure_ascii=False)

    # Load existing completed tasks from destination file
    existing_completed = []
    if open(dest_file, encoding="utf-8"):
        try:
            with open(dest_file, encoding="utf-8") as f:
                dest_data = json.load(f)
                existing_completed = dest_data.get("completed_non_alignment_tasks", [])
        except FileNotFoundError:
            print(f"Destination file {dest_file} not found, creating new one")
            existing_completed = []

    # Create a map of existing task IDs to avoid duplicates
    existing_task_ids = {task["id"] for task in existing_completed}

    # Add only tasks that are not already in the completed tasks file
    new_tasks_to_move = []
    for task in tasks_to_move:
        if task["id"] not in existing_task_ids:
            new_tasks_to_move.append(task)

    # Combine existing completed tasks with new ones
    all_unique_completed = existing_completed + new_tasks_to_move

    # Write the completed tasks to the destination file
    with open(dest_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "completed_non_alignment_tasks": all_unique_completed,
                "metadata": {
                    "moved_from_file": source_file,
                    "moved_timestamp": datetime.now().isoformat(),
                    "task_ids_moved": task_ids_to_move,
                    "newly_moved_count": len(new_tasks_to_move),
                    "total_completed_tasks": len(all_unique_completed),
                },
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    return {
        "tasks_moved": len(new_tasks_to_move),
        "total_in_completed": len(all_unique_completed),
        "removed_from_source": len(tasks_to_move),
        "remaining_in_source": len(remaining_tasks),
        "duplicates_skipped": len(tasks_to_move) - len(new_tasks_to_move),
    }


def main():
    """Main function to run the move process for tasks 64-69."""
    # Define file paths
    source_tasks_path = "../tasks/tasks.json"
    completed_tasks_path = "../tasks/non_alignment_tasks.json"

    # Task IDs to move (64 to 69 inclusive)
    task_ids_to_move = list(range(64, 70))  # [64, 65, 66, 67, 68, 69]

    # Move tasks
    stats = move_tasks_range(source_tasks_path, completed_tasks_path, task_ids_to_move)

    print("Move operation completed!")
    print(f"  - Tasks identified for move: {task_ids_to_move}")
    print(f"  - Tasks actually moved: {stats['tasks_moved']}")
    print(f"  - Duplicates skipped: {stats['duplicates_skipped']}")
    print(f"  - Total tasks in completed file: {stats['total_in_completed']}")
    print(f"  - Tasks removed from main file: {stats['removed_from_source']}")
    print(f"  - Remaining tasks in main file: {stats['remaining_in_source']}")

    # Show what was moved
    if stats["tasks_moved"] > 0:
        print("\nMoved tasks:")
        for task_id in task_ids_to_move:
            print(f"  - Task {task_id}")
    else:
        print("\nNo new tasks were moved (they were already in the completed file).")


if __name__ == "__main__":
    main()
