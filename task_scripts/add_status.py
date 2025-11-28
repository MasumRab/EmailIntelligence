#!/usr/bin/env python3
"""
Add Status to Task Files

This script adds status information to task files that may be missing it,
using the centralized shared utilities to avoid duplication.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Import shared utilities
from taskmaster_common import SecurityValidator, BackupManager, FileValidator

def add_status_to_task(task: Dict[str, Any]) -> Dict[str, Any]:
    """Add status field to a task if it's missing"""
    if 'status' not in task:
        task['status'] = 'pending'
        print(f"  - Added 'pending' status to task {task.get('id', 'unknown')}")
    elif task['status'] not in ['pending', 'in-progress', 'completed', 'cancelled', 'deferred']:
        print(f"  - Invalid status '{task['status']}' for task {task.get('id', 'unknown')}, setting to 'pending'")
        task['status'] = 'pending'
    return task

def add_status_to_task_file(filepath: str) -> bool:
    """Add status to all tasks in a task file using shared utilities."""
    # Validate path security using shared utility
    if not SecurityValidator.validate_path_security(filepath):
        print(f"Error: Invalid or unsafe file path: {filepath}")
        return False

    # Use centralized backup manager
    backup_mgr = BackupManager()
    backup_path = backup_mgr.create_backup(filepath)
    print(f"  - Created backup: {backup_path}")

    # Use centralized file validator
    try:
        data = FileValidator.load_json_secure(filepath)

        if not isinstance(data, dict) or 'tasks' not in data:
            print(f"Warning: {filepath} does not have a valid tasks structure")
            return False

        tasks = data['tasks']
        if not isinstance(tasks, list):
            print(f"Warning: {filepath} tasks is not an array")
            return False

        modified = False
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                print(f"Warning: Task at index {i} is not an object, skipping")
                continue

            original_task = task.copy()
            updated_task = add_status_to_task(task)

            if updated_task != original_task:
                tasks[i] = updated_task
                modified = True

        if modified:
            # Write updated file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  - Updated: {filepath}")
        else:
            print(f"  - No changes needed: {filepath}")

        return True

    except Exception as e:
        print(f"Error loading file: {e}")
        return False

def process_directory(directory: str, pattern: str = "**/tasks.json"):
    """Process all task files in a directory"""
    # Validate directory path security using shared utility
    if not SecurityValidator.validate_path_security(directory):
        print(f"Error: Invalid or unsafe directory path: {directory}")
        return 0

    dir_path = Path(directory)
    task_files = list(dir_path.glob(pattern))

    print(f"Found {len(task_files)} task files to process")

    success_count = 0
    for task_file in task_files:
        # Validate each task file path using shared utility
        task_file_str = str(task_file)
        if SecurityValidator.validate_path_security(task_file_str):
            print(f"Processing: {task_file}")
            if add_status_to_task_file(task_file_str):
                success_count += 1
        else:
            print(f"Skipping unsafe file: {task_file}")

    print(f"\nProcessed {success_count}/{len(task_files)} files successfully")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Add status field to task files')
    parser.add_argument('path', nargs='?', default='.', help='Path to process (file or directory)')
    parser.add_argument('--pattern', default='**/tasks.json', help='File pattern to match (for directories)')
    parser.add_argument('--file', help='Specific file to process (alternative to path)')

    args = parser.parse_args()

    path_to_process = args.file or args.path

    # Validate path security before processing using shared utility
    if not SecurityValidator.validate_path_security(path_to_process):
        print(f"Error: Invalid or unsafe path: {path_to_process}")
        sys.exit(1)

    if os.path.isfile(path_to_process):
        print(f"Processing single file: {path_to_process}")
        success = add_status_to_task_file(path_to_process)
        if success:
            print("File processed successfully")
        else:
            print("Failed to process file")
            sys.exit(1)
    elif os.path.isdir(path_to_process):
        print(f"Processing directory: {path_to_process}")
        process_directory(path_to_process, args.pattern)
    else:
        print(f"Error: Path does not exist: {path_to_process}")
        sys.exit(1)

if __name__ == "__main__":
    main()