#!/usr/bin/env python3
"""
Script to consolidate completed tasks by removing them from tasks.json and keeping them in non_alignment_tasks.json
without creating duplicates.
"""
import json
import os
import shutil
from datetime import datetime

def consolidate_completed_tasks(original_file_path, completed_tasks_file):
    """
    Move completed tasks from original tasks file to completed tasks file without duplicating existing entries.
    
    Args:
        original_file_path: Path to the original tasks.json file
        completed_tasks_file: Path where completed tasks should be stored
    
    Returns:
        dict with number of tasks moved and other statistics
    """
    # Make backup of original file
    backup_path = f"{original_file_path}.backup_consolidate_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(original_file_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read the original tasks.json file
    with open(original_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get the original tasks array
    original_tasks = data['master']['tasks']
    
    # Separate completed and remaining tasks
    completed_tasks = []
    remaining_tasks = []
    
    for task in original_tasks:
        if task.get('status') == 'done':
            completed_tasks.append(task)
        else:
            remaining_tasks.append(task)

    # Update the data with only remaining (non-completed) tasks
    data['master']['tasks'] = remaining_tasks

    # Write the updated tasks back to the original file
    with open(original_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Load existing completed tasks or create new structure
    existing_completed = []
    if os.path.exists(completed_tasks_file):
        with open(completed_tasks_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_completed = existing_data.get('completed_non_alignment_tasks', [])

    # Create a set of IDs that are already in the completed tasks file to avoid duplicates
    existing_ids = {task['id'] for task in existing_completed}
    
    # Add only tasks that are not already in the completed tasks file
    new_completed_tasks = [task for task in completed_tasks if task['id'] not in existing_ids]
    
    # Combine existing completed tasks with new ones
    all_unique_completed = existing_completed + new_completed_tasks

    # Write the completed tasks to the separate file
    with open(completed_tasks_file, 'w', encoding='utf-8') as f:
        json.dump({
            "completed_non_alignment_tasks": all_unique_completed,
            "metadata": {
                "moved_from_original_file": os.path.basename(original_file_path),
                "moved_timestamp": datetime.now().isoformat(),
                "newly_moved_tasks": len(new_completed_tasks),
                "total_accumulated_completed_tasks": len(all_unique_completed)
            }
        }, f, indent=2, ensure_ascii=False)

    return {
        "newly_moved": len(new_completed_tasks),
        "total_in_completed": len(all_unique_completed),
        "removed_from_main": len(completed_tasks),
        "remaining_in_main": len(remaining_tasks)
    }

def main():
    """Main function to run the consolidation process."""
    # Define file paths (relative to project root)
    original_tasks_path = '../tasks/tasks.json'
    completed_tasks_path = '../tasks/non_alignment_tasks.json'
    
    # Consolidate completed tasks
    stats = consolidate_completed_tasks(original_tasks_path, completed_tasks_path)
    
    print(f"Consolidation completed!")
    print(f"  - Newly moved tasks: {stats['newly_moved']}")
    print(f"  - Total tasks in completed file: {stats['total_in_completed']}")
    print(f"  - Tasks removed from main file: {stats['removed_from_main']}")
    print(f"  - Remaining tasks in main file: {stats['remaining_in_main']}")
    
    # Show what was newly moved (if any)
    if stats['newly_moved'] > 0:
        with open(completed_tasks_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("\nNewly moved tasks:")
            # Show only the newly moved tasks from the updated file
            all_completed = data['completed_non_alignment_tasks']
            # Just show a sample since we already consolidated based on IDs
            for task in all_completed[-stats['newly_moved']:]:  # Show last N which are the new ones
                print(f"  - Task {task['id']}: {task['title']} (Status: {task['status']})")
    else:
        print("\nNo new tasks were moved (they were already in the completed file).")
    
    print(f"\nCompleted tasks are now in: {completed_tasks_path}")
    print(f"Active tasks remain in: {original_tasks_path}")

if __name__ == "__main__":
    main()