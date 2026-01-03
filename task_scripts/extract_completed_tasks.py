#!/usr/bin/env python3
"""
Script to extract completed tasks from tasks.json and create a separate file for them.
This helps separate completed non-alignment tasks from active tasks.
"""
import json
import os

def extract_completed_tasks(tasks_file_path, output_file_path):
    """
    Extract tasks with status 'done' from tasks.json and write them to output file.
    
    Args:
        tasks_file_path: Path to the original tasks.json file
        output_file_path: Path where completed tasks should be written
    
    Returns:
        Number of completed tasks found and extracted
    """
    # Read the original tasks.json file
    with open(tasks_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Navigate to the tasks array (assuming the structure is data['master']['tasks'])
    tasks = data['master']['tasks']

    # Find all tasks with status 'done' - only main tasks, not based on subtasks
    completed_tasks = []
    for task in tasks:
        if task.get('status') == 'done':
            completed_tasks.append(task)

    # Write the completed tasks to the output file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump({
            "completed_non_alignment_tasks": completed_tasks,
            "extraction_info": {
                "total_completed_tasks": len(completed_tasks),
                "extraction_timestamp": __import__('datetime').datetime.now().isoformat(),
                "source_file": os.path.basename(tasks_file_path)
            }
        }, f, indent=2, ensure_ascii=False)

    return len(completed_tasks)

def main():
    """Main function to run the extraction process."""
    # Define file paths
    tasks_json_path = '../tasks/tasks.json'  # Relative to this script's location
    output_path = '../tasks/non_alignment_tasks.json'
    
    # Extract completed tasks
    count = extract_completed_tasks(tasks_json_path, output_path)
    
    print(f"Successfully extracted {count} completed tasks to {output_path}")
    print("Completed tasks include:")
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for task in data['completed_non_alignment_tasks']:
            print(f"  - Task {task['id']}: {task['title']} (Status: {task['status']})")

if __name__ == "__main__":
    main()