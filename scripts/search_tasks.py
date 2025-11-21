#!/usr/bin/env python3
"""
Search tasks by keyword in title, description, or details
Usage: python scripts/search_tasks.py <keyword> [--file FILE] [--tag TAG]
"""

import json
import sys
import argparse
import re
from pathlib import Path

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
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def search_in_task(task, keyword, case_sensitive=False):
    """Check if keyword appears in task fields"""
    flags = 0 if case_sensitive else re.IGNORECASE
    
    fields_to_search = [
        task.get('title', ''),
        task.get('description', ''),
        task.get('details', ''),
    ]
    
    for field in fields_to_search:
        if re.search(keyword, field, flags):
            return True
    
    # Also search in subtasks
    for subtask in task.get('subtasks', []):
        if search_in_task(subtask, keyword, case_sensitive):
            return True
    
    return False

def format_task_match(task, keyword, show_context=False):
    """Format a matching task for display"""
    lines = [
        f"Task {task['id']}: {task['title']}",
        f"  Status: {task.get('status', 'N/A')}",
        f"  Priority: {task.get('priority', 'N/A')}",
    ]
    
    # Highlight matches
    if show_context:
        title = task.get('title', '')
        desc = task.get('description', '')
        
        # Find and highlight keyword in title
        if re.search(keyword, title, re.IGNORECASE):
            lines.append(f"  Title match: {title[:100]}")
        
        # Find and highlight keyword in description
        if desc and re.search(keyword, desc, re.IGNORECASE):
            # Extract context around match
            match = re.search(keyword, desc, re.IGNORECASE)
            if match:
                start = max(0, match.start() - 50)
                end = min(len(desc), match.end() + 50)
                context = desc[start:end]
                lines.append(f"  Description match: ...{context}...")
    
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='Search tasks by keyword')
    parser.add_argument('keyword', help='Keyword to search for')
    parser.add_argument('--file', default='tasks/tasks.json', help='Path to tasks JSON file')
    parser.add_argument('--tag', default='master', help='Task tag (default: master)')
    parser.add_argument('--case-sensitive', action='store_true', help='Case-sensitive search')
    parser.add_argument('--show-context', action='store_true', help='Show context around matches')
    parser.add_argument('--invalid', action='store_true', help='Search in tasks_invalid.json')
    
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
    
    # Search tasks
    matches = []
    for task in tasks:
        if search_in_task(task, args.keyword, args.case_sensitive):
            matches.append(task)
    
    if not matches:
        print(f"No tasks found matching '{args.keyword}'")
        return
    
    print(f"Found {len(matches)} task(s) matching '{args.keyword}':\n")
    
    for task in matches:
        print(format_task_match(task, args.keyword, args.show_context))
        print()

if __name__ == '__main__':
    main()
