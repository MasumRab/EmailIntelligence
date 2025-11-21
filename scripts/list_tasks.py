#!/usr/bin/env python3
"""
List all tasks from tasks.json
Usage: python scripts/list_tasks.py [--status STATUS] [--priority PRIORITY] [--tag TAG]
"""

import json
import sys
import argparse
from pathlib import Path

def load_tasks(file_path, tag="master"):
    """Load tasks from tasks.json file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if tag in data:
            return data[tag].get('tasks', [])
        elif 'tasks' in data:
            return data['tasks']
        else:
            return []
    except FileNotFoundError:
        print(f"Error: {file_path} not found", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return []

def format_task(task, show_subtasks=False):
    """Format a task for display"""
    lines = [
        f"Task {task['id']}: {task['title']}",
        f"  Status: {task.get('status', 'N/A')}",
        f"  Priority: {task.get('priority', 'N/A')}",
    ]
    
    if task.get('dependencies'):
        lines.append(f"  Dependencies: {', '.join(map(str, task['dependencies']))}")
    
    subtasks = task.get('subtasks', [])
    if subtasks:
        lines.append(f"  Subtasks: {len(subtasks)}")
        if show_subtasks:
            for subtask in subtasks:
                lines.append(f"    - {subtask['id']}: {subtask['title']} ({subtask.get('status', 'N/A')})")
    
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='List tasks from tasks.json')
    parser.add_argument('--status', help='Filter by status (pending, in-progress, done, etc.)')
    parser.add_argument('--priority', help='Filter by priority (high, medium, low)')
    parser.add_argument('--tag', default='master', help='Task tag (default: master)')
    parser.add_argument('--show-subtasks', action='store_true', help='Show subtask details')
    parser.add_argument('--file', default='tasks/tasks.json', help='Path to tasks.json file')
    
    args = parser.parse_args()
    
    # Resolve file path relative to script location
    script_dir = Path(__file__).parent.parent
    tasks_file = script_dir / args.file
    
    tasks = load_tasks(tasks_file, args.tag)
    
    if not tasks:
        print("No tasks found.")
        return
    
    # Apply filters
    filtered_tasks = tasks
    if args.status:
        filtered_tasks = [t for t in filtered_tasks if t.get('status') == args.status]
    if args.priority:
        filtered_tasks = [t for t in filtered_tasks if t.get('priority') == args.priority]
    
    print(f"Total tasks: {len(filtered_tasks)} (filtered from {len(tasks)})\n")
    
    for task in filtered_tasks:
        print(format_task(task, args.show_subtasks))
        print()

if __name__ == '__main__':
    main()
