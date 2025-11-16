#!/usr/bin/env python3
"""
Show detailed information about a specific task
Usage: python scripts/show_task.py <task_id> [--file FILE] [--tag TAG]
"""

import json
import sys
import argparse
from pathlib import Path

def find_task_by_id(tasks, task_id):
    """Find a task by ID, including in subtasks"""
    for task in tasks:
        if task['id'] == task_id:
            return task
        # Check subtasks
        for subtask in task.get('subtasks', []):
            if subtask['id'] == task_id:
                return subtask
    return None

def format_task_details(task, indent=0):
    """Format task with full details"""
    prefix = "  " * indent
    lines = [
        f"{prefix}Task {task['id']}: {task['title']}",
        f"{prefix}  Status: {task.get('status', 'N/A')}",
        f"{prefix}  Priority: {task.get('priority', 'N/A')}",
    ]
    
    if task.get('dependencies'):
        lines.append(f"{prefix}  Dependencies: {', '.join(map(str, task['dependencies']))}")
    
    if task.get('description'):
        desc = task['description'].replace('\n', ' ')
        if len(desc) > 100:
            desc = desc[:100] + "..."
        lines.append(f"{prefix}  Description: {desc}")
    
    if task.get('details'):
        lines.append(f"{prefix}  Details:")
        details = task['details'].split('\n')
        for detail in details[:5]:  # Show first 5 lines
            lines.append(f"{prefix}    - {detail}")
        if len(details) > 5:
            lines.append(f"{prefix}    ... ({len(details) - 5} more lines)")
    
    if task.get('testStrategy'):
        lines.append(f"{prefix}  Test Strategy: {task['testStrategy'][:100]}...")
    
    subtasks = task.get('subtasks', [])
    if subtasks:
        lines.append(f"{prefix}  Subtasks ({len(subtasks)}):")
        for subtask in subtasks:
            lines.append(f"{prefix}    - {subtask['id']}: {subtask['title']} ({subtask.get('status', 'N/A')})")
    
    return '\n'.join(lines)

def load_tasks(file_path, tag="master"):
    """Load tasks from JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if tag in data:
            return data[tag].get('tasks', [])
        elif 'tasks' in data:
            return data['tasks']
        elif isinstance(data, list):
            return data
        else:
            return []
    except FileNotFoundError:
        print(f"Error: {file_path} not found", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(description='Show detailed task information')
    parser.add_argument('task_id', type=int, help='Task ID to show')
    parser.add_argument('--file', default='tasks/tasks.json', help='Path to tasks JSON file')
    parser.add_argument('--tag', default='master', help='Task tag (default: master)')
    parser.add_argument('--invalid', action='store_true', help='Search in tasks_invalid.json instead')
    
    args = parser.parse_args()
    
    # Resolve file path
    script_dir = Path(__file__).parent.parent
    if args.invalid:
        tasks_file = script_dir / 'tasks/tasks_invalid.json'
    else:
        tasks_file = script_dir / args.file
    
    tasks = load_tasks(tasks_file, args.tag)
    
    if not tasks:
        print("No tasks found in file.")
        return
    
    # Handle invalid tasks file (may need special parsing)
    if args.invalid:
        # Try to find task using simple search
        import re
        with open(tasks_file, 'r') as f:
            content = f.read()
        
        # Search for task with matching ID
        pattern = rf'\{{[^}}]*"id":\s*{args.task_id}[^}}]*"title":\s*"([^"]+)"[^}}]*"status":\s*"([^"]+)"'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            print(f"Task {args.task_id}: {match.group(1)}")
            print(f"  Status: {match.group(2)}")
            print("\nNote: Full details not available from invalid tasks file.")
            return
    
    task = find_task_by_id(tasks, args.task_id)
    
    if not task:
        print(f"Task {args.task_id} not found.")
        return
    
    print(format_task_details(task))

if __name__ == '__main__':
    main()
