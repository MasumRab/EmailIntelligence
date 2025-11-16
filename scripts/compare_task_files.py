#!/usr/bin/env python3
"""
Compare tasks across different JSON files
Usage: python scripts/compare_task_files.py
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

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

def get_task_signature(task):
    """Get a unique signature for a task (id + title)"""
    return (task.get('id'), task.get('title', ''))

def parse_invalid_tasks(file_path):
    """Parse tasks_invalid.json"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        try:
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'tasks' in data:
                return data['tasks']
        except json.JSONDecodeError:
            pass
        
        # Fallback parsing
        import re
        tasks = []
        lines = content.split('\n')
        depth = 0
        in_subtasks = False
        
        for i, line in enumerate(lines):
            depth += line.count('{') - line.count('}')
            if '"subtasks"' in line and '[' in line:
                in_subtasks = True
            if in_subtasks and depth <= 1:
                in_subtasks = False
            
            if not in_subtasks and depth == 1:
                id_match = re.search(r'"id":\s*(\d+)', line)
                if id_match:
                    task_id = int(id_match.group(1))
                    if 1 <= task_id <= 13:
                        title = None
                        status = None
                        for j in range(i, min(i+30, len(lines))):
                            if title is None:
                                title_match = re.search(r'"title":\s*"([^"]+)"', lines[j])
                                if title_match:
                                    title = title_match.group(1)
                            if status is None:
                                status_match = re.search(r'"status":\s*"([^"]+)"', lines[j])
                                if status_match:
                                    status = status_match.group(1)
                            if title and status:
                                break
                        
                        if title and status:
                            tasks.append({
                                'id': task_id,
                                'title': title,
                                'status': status
                            })
        
        seen = set()
        return [t for t in tasks if t['id'] not in seen and not seen.add(t['id'])]
    except FileNotFoundError:
        return []

def main():
    script_dir = Path(__file__).parent.parent
    
    # Load all task files
    tasks_main = load_tasks(script_dir / 'tasks/tasks.json', 'master')
    tasks_expanded = load_tasks(script_dir / 'tasks/tasks_expanded.json', 'master')
    tasks_new = load_tasks(script_dir / 'tasks/tasks_new.json')
    tasks_invalid = parse_invalid_tasks(script_dir / 'tasks/tasks_invalid.json')
    
    print("=" * 70)
    print("TASK FILE COMPARISON")
    print("=" * 70)
    print()
    
    # Create signature sets
    main_sigs = {get_task_signature(t) for t in tasks_main}
    expanded_sigs = {get_task_signature(t) for t in tasks_expanded}
    invalid_sigs = {get_task_signature(t) for t in tasks_invalid}
    
    # Compare main vs expanded
    print("tasks.json vs tasks_expanded.json:")
    if main_sigs == expanded_sigs:
        print("  ✓ Files contain identical tasks")
    else:
        only_main = main_sigs - expanded_sigs
        only_expanded = expanded_sigs - main_sigs
        if only_main:
            print(f"  Tasks only in tasks.json: {len(only_main)}")
            for task_id, title in sorted(only_main):
                print(f"    - Task {task_id}: {title}")
        if only_expanded:
            print(f"  Tasks only in tasks_expanded.json: {len(only_expanded)}")
            for task_id, title in sorted(only_expanded):
                print(f"    - Task {task_id}: {title}")
    print()
    
    # Compare main vs invalid
    print("tasks.json vs tasks_invalid.json:")
    overlap = main_sigs & invalid_sigs
    only_main = main_sigs - invalid_sigs
    only_invalid = invalid_sigs - main_sigs
    
    if overlap:
        print(f"  Overlapping tasks: {len(overlap)}")
        for task_id, title in sorted(overlap):
            # Find status in invalid
            invalid_task = next((t for t in tasks_invalid if t.get('id') == task_id), None)
            status = invalid_task.get('status') if invalid_task else 'N/A'
            print(f"    - Task {task_id}: {title} (status in invalid: {status})")
    
    if only_main:
        print(f"  Tasks only in tasks.json: {len(only_main)}")
        for task_id, title in sorted(only_main):
            print(f"    - Task {task_id}: {title}")
    
    if only_invalid:
        print(f"  Tasks only in tasks_invalid.json: {len(only_invalid)}")
        for task_id, title in sorted(only_invalid):
            invalid_task = next((t for t in tasks_invalid if t.get('id') == task_id), None)
            status = invalid_task.get('status') if invalid_task else 'N/A'
            print(f"    - Task {task_id}: {title} (status: {status})")
    print()
    
    # Check tasks_new.json
    if tasks_new:
        print("tasks_new.json:")
        print(f"  Contains {len(tasks_new)} tasks")
        for task in tasks_new:
            print(f"    - Task {task.get('id')}: {task.get('title')}")
    else:
        print("tasks_new.json: Empty")
    print()
    
    # Summary
    print("Summary:")
    print(f"  Total unique tasks across all files: {len(main_sigs | expanded_sigs | invalid_sigs)}")
    print(f"  Active tasks (tasks.json): {len(tasks_main)}")
    print(f"  Invalid/completed tasks: {len(tasks_invalid)}")

if __name__ == '__main__':
    main()
