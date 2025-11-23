#!/usr/bin/env python3
"""
Fix Duplicate Task IDs Script

This script fixes the duplicate task IDs that weren't properly handled
in the deduplication phase.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

def fix_duplicate_ids():
    """Fix duplicate task IDs by merging tasks with the same ID"""
    deduplicated_file = Path("backlog/deduplication/deduplicated_tasks.json")

    with open(deduplicated_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tasks = data['tasks']
    print(f"Original task count: {len(tasks)}")

    # Group tasks by ID
    tasks_by_id = defaultdict(list)
    for task in tasks:
        task_id = task.get('id')
        if task_id:
            tasks_by_id[task_id].append(task)

    # Merge duplicates
    merged_tasks = []
    for task_id, task_list in tasks_by_id.items():
        if len(task_list) == 1:
            merged_tasks.append(task_list[0])
        else:
            # Merge multiple tasks with same ID
            print(f"Merging {len(task_list)} tasks with ID {task_id}")
            merged = merge_task_duplicates(task_list)
            merged_tasks.append(merged)

    print(f"After merging: {len(merged_tasks)} tasks")

    # Update the data
    data['tasks'] = merged_tasks
    data['metadata']['deduplicated_tasks'] = len(merged_tasks)

    # Save back
    with open(deduplicated_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ Fixed duplicate task IDs")

def merge_task_duplicates(tasks: List[Dict]) -> Dict:
    """Merge multiple tasks with the same ID"""
    if not tasks:
        return {}

    # Start with the first task
    merged = dict(tasks[0])

    # Merge information from other tasks
    for task in tasks[1:]:
        # Combine descriptions
        if task.get('description') and task['description'] not in merged.get('description', ''):
            merged['description'] = (merged.get('description', '') + '\n\n' + task['description']).strip()

        # Combine acceptance criteria
        if task.get('acceptance_criteria') and task['acceptance_criteria'] not in merged.get('acceptance_criteria', ''):
            merged['acceptance_criteria'] = (merged.get('acceptance_criteria', '') + '\n\n' + task['acceptance_criteria']).strip()

        # Combine assignees
        if task.get('assignees'):
            existing = set(merged.get('assignees', []))
            new_assignees = task['assignees']
            if isinstance(new_assignees, list):
                existing.update(new_assignees)
            else:
                existing.add(new_assignees)
            merged['assignees'] = list(existing)

        # Combine labels
        if task.get('labels'):
            existing = set(merged.get('labels', []))
            new_labels = task['labels']
            if isinstance(new_labels, list):
                existing.update(new_labels)
            else:
                existing.add(new_labels)
            merged['labels'] = list(existing)

        # Keep the most recent dates
        for date_field in ['created_date', 'updated_date']:
            if task.get(date_field) and task[date_field] > merged.get(date_field, ''):
                merged[date_field] = task[date_field]

        # Add source files
        merged_sources = set(merged.get('merged_from', []))
        merged_sources.add(task.get('source_file', ''))
        merged['merged_from'] = list(merged_sources)

    return merged

def regenerate_consolidated_files():
    """Regenerate all consolidated files after fixing duplicates"""
    print("Regenerating consolidated files...")

    # Run the reorganization script
    import subprocess
    scripts = [
        "backlog/reorganization/reorganize_tasks.py",
        "backlog/relationships/build_relationships.py",
        "backlog/consolidated/generate_consolidated_files.py"
    ]

    for script in scripts:
        print(f"Running {script}...")
        result = subprocess.run(["python3", script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running {script}: {result.stderr}")
        else:
            print(f"✅ {script} completed")

def main():
    print("Fixing duplicate task IDs...")
    fix_duplicate_ids()
    regenerate_consolidated_files()
    print("✅ All fixes applied and files regenerated")

if __name__ == "__main__":
    main()