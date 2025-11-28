#!/usr/bin/env python3
"""
Find the next available task to work on (similar to 'task-master next')
Usage: python scripts/next_task.py [--tag TAG]
"""

import json
import os
import sys
import argparse
from pathlib import Path

# Add the task_scripts directory to the path to import shared utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'task_scripts'))
from taskmaster_common import SecurityValidator, FileValidator

def load_tasks(file_path, tag="master"):
    """Load tasks from tasks.json file using shared utilities"""
    # Validate path security first
    if not SecurityValidator.validate_path_security(file_path):
        print(f"Error: Invalid or unsafe file path: {file_path}", file=sys.stderr)
        return []

    try:
        data = FileValidator.load_json_secure(file_path)
        
        if tag in data:
            return data[tag].get('tasks', [])
        elif 'tasks' in data:
            return data['tasks']
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def find_next_task(tasks):
    """
    Find the next available task based on:
    1. Status is 'pending'
    2. No unmet dependencies
    3. Priority (high > medium > low)
    """
    # Get all task IDs for dependency checking
    all_task_ids = {task['id'] for task in tasks}
    
    # Filter pending tasks
    pending_tasks = [t for t in tasks if t.get('status') == 'pending']
    
    if not pending_tasks:
        return None
    
    # Filter tasks with no unmet dependencies
    available_tasks = []
    for task in pending_tasks:
        deps = task.get('dependencies', [])
        # Check if all dependencies are satisfied (exist in task list)
        # Note: We can't check if dependencies are 'done' without checking invalid tasks
        # So we'll just check if they exist
        if all(dep in all_task_ids for dep in deps):
            available_tasks.append(task)
    
    if not available_tasks:
        return None
    
    # Sort by priority (high > medium > low) and then by ID
    priority_order = {'high': 3, 'medium': 2, 'low': 1, 'N/A': 0}
    available_tasks.sort(
        key=lambda t: (-priority_order.get(t.get('priority', 'N/A'), 0), t['id'])
    )
    
    return available_tasks[0]

def format_task(task):
    """Format task for display"""
    lines = [
        f"Next Task: {task['id']}",
        f"Title: {task['title']}",
        f"Status: {task.get('status', 'N/A')}",
        f"Priority: {task.get('priority', 'N/A')}",
    ]
    
    if task.get('dependencies'):
        lines.append(f"Dependencies: {', '.join(map(str, task['dependencies']))}")
    
    if task.get('description'):
        desc = task['description']
        if len(desc) > 200:
            desc = desc[:200] + "..."
        lines.append(f"\nDescription:\n{desc}")
    
    subtasks = task.get('subtasks', [])
    if subtasks:
        lines.append(f"\nSubtasks ({len(subtasks)}):")
        for subtask in subtasks[:5]:  # Show first 5
            lines.append(f"  - {subtask['id']}: {subtask['title']} ({subtask.get('status', 'N/A')})")
        if len(subtasks) > 5:
            lines.append(f"  ... and {len(subtasks) - 5} more")
    
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='Find next available task')
    parser.add_argument('--tag', default='master', help='Task tag (default: master)')
    parser.add_argument('--file', default='tasks/tasks.json', help='Path to tasks.json file')
    
    args = parser.parse_args()
    
    # Resolve file path
    script_dir = Path(__file__).parent.parent
    tasks_file = script_dir / args.file
    
    tasks = load_tasks(tasks_file, args.tag)
    
    if not tasks:
        print("No tasks found.")
        return
    
    next_task = find_next_task(tasks)
    
    if not next_task:
        print("No available tasks found (all tasks may have unmet dependencies or be completed).")
        return
    
    print(format_task(next_task))

if __name__ == '__main__':
    main()
