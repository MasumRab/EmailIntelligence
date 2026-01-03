#!/usr/bin/env python3
"""
Final script to complete the task of moving completed tasks from tasks.json to non_alignment_tasks.json.
"""
import json
import os
import shutil
from datetime import datetime

def finalize_task_move():
    """Final move of completed tasks from main tasks.json to non_alignment_tasks.json file."""
    # File paths
    main_tasks_path = '../tasks/tasks.json'
    completed_tasks_path = '../tasks/non_alignment_tasks.json'
    
    # Make backup of original file
    backup_path = f"{main_tasks_path}.backup_finalize_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(main_tasks_path, backup_path)
    print(f"Created backup: {backup_path}")

    # Read the main tasks.json file
    with open(main_tasks_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get the original tasks array
    all_tasks = data['master']['tasks']
    
    # Separate completed and non-completed tasks
    completed_tasks = []
    non_completed_tasks = []
    
    for task in all_tasks:
        if task.get('status') == 'done':
            completed_tasks.append(task)
        else:
            non_completed_tasks.append(task)

    print(f"Found {len(completed_tasks)} completed tasks to move")
    print(f"Keeping {len(non_completed_tasks)} non-completed tasks in main file")

    # Update the main file with only non-completed tasks
    data['master']['tasks'] = non_completed_tasks

    # Write the filtered tasks back to the main file
    with open(main_tasks_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Load existing completed tasks from the separate file (if it exists)
    existing_completed_tasks = []
    if os.path.exists(completed_tasks_path):
        with open(completed_tasks_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            existing_completed_tasks = existing_data.get('completed_non_alignment_tasks', [])
    
    # Build a map of existing task IDs to avoid duplicates
    existing_task_ids = {task['id'] for task in existing_completed_tasks}
    
    # Add only newly completed tasks that aren't already in the completed file
    new_completed_tasks = [task for task in completed_tasks if task['id'] not in existing_task_ids]
    
    # Combine existing and new completed tasks
    all_completed_tasks = existing_completed_tasks + new_completed_tasks

    # Write the completed tasks to the separate file
    with open(completed_tasks_path, 'w', encoding='utf-8') as f:
        json.dump({
            "completed_non_alignment_tasks": all_completed_tasks,
            "metadata": {
                "moved_from_original_file": os.path.basename(main_tasks_path),
                "moved_timestamp": datetime.now().isoformat(),
                "newly_moved_tasks": len(new_completed_tasks),
                "total_accumulated_completed_tasks": len(all_completed_tasks),
                "note": "These tasks were completed and moved out of the main tasks list"
            }
        }, f, indent=2, ensure_ascii=False)

    print(f"\nSUMMARY:")
    print(f"  - Moved {len(new_completed_tasks)} new completed tasks to {completed_tasks_path}")
    print(f"  - Total completed tasks in completed file: {len(all_completed_tasks)}")
    print(f"  - Non-completed tasks remaining in main file: {len(non_completed_tasks)}")
    print(f"  - Completed tasks remaining in main file: {len([t for t in non_completed_tasks if t.get('status') == 'done'])}")
    
    return {
        "newly_moved": len(new_completed_tasks),
        "total_completed": len(all_completed_tasks),
        "remaining_in_main": len(non_completed_tasks),
        "completed_in_main_still": len([t for t in non_completed_tasks if t.get('status') == 'done'])
    }

def main():
    """Main function."""
    stats = finalize_task_move()
    print("\nFinalization completed successfully!")

if __name__ == "__main__":
    main()