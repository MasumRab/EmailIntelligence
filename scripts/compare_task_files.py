#!/usr/bin/env python3
"""
Compare tasks across different JSON files
Usage: python scripts/compare_task_files.py
"""

import os
import sys
from pathlib import Path

# Add the task_scripts directory to the path to import shared utilities
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "task_scripts"))
from taskmaster_common import FileValidator, SecurityValidator, TaskComparison


def main():
    script_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("TASK FILE COMPARISON")
    print("=" * 70)
    print()

    # Define file paths
    tasks_main_path = script_dir / "tasks/tasks.json"
    tasks_expanded_path = script_dir / "tasks/tasks_expanded.json"
    tasks_new_path = script_dir / "tasks/tasks_new.json"
    tasks_invalid_path = script_dir / "tasks/tasks_invalid.json"

    # Validate file paths
    files_to_check = [tasks_main_path, tasks_expanded_path, tasks_new_path, tasks_invalid_path]
    valid_files = []

    for file_path in files_to_check:
        if SecurityValidator.validate_path_security(str(file_path)):
            valid_files.append(str(file_path))
        else:
            print(f"Warning: Skipping invalid file path: {file_path}")

    # Compare main vs expanded if both exist
    if tasks_main_path.exists() and tasks_expanded_path.exists():
        print("tasks.json vs tasks_expanded.json:")
        try:
            comparison = TaskComparison.compare_task_files(
                str(tasks_main_path), str(tasks_expanded_path)
            )
            if comparison["added"] or comparison["removed"] or comparison["modified"]:
                print(f"  Added: {len(comparison['added'])}")
                print(f"  Removed: {len(comparison['removed'])}")
                print(f"  Modified: {len(comparison['modified'])}")
            else:
                print("  ✓ Files contain identical tasks")
        except Exception as e:
            print(f"  Error comparing files: {e}")
    print()

    # Compare main vs invalid if both exist
    if tasks_main_path.exists() and tasks_invalid_path.exists():
        print("tasks.json vs tasks_invalid.json:")
        try:
            comparison = TaskComparison.compare_task_files(
                str(tasks_main_path), str(tasks_invalid_path)
            )
            print(f"  Added: {len(comparison['added'])}")
            print(f"  Removed: {len(comparison['removed'])}")
            print(f"  Modified: {len(comparison['modified'])}")
            print(f"  Common: {comparison['common_count']}")
        except Exception as e:
            print(f"  Error comparing files: {e}")
    print()

    # Check tasks_new.json
    if tasks_new_path.exists():
        try:
            data = FileValidator.load_json_secure(str(tasks_new_path))
            if isinstance(data, dict) and "tasks" in data:
                tasks_new_count = len(data["tasks"])
            elif isinstance(data, list):
                tasks_new_count = len(data)
            else:
                tasks_new_count = 0

            print(f"tasks_new.json: Contains {tasks_new_count} tasks")
        except Exception as e:
            print(f"tasks_new.json: Error reading file: {e}")
    else:
        print("tasks_new.json: File not found")
    print()

    # Summary
    total_tasks = 0
    if tasks_main_path.exists():
        try:
            main_data = FileValidator.load_json_secure(str(tasks_main_path))
            main_tasks = TaskComparison.extract_tasks_from_data(main_data, "master")
            total_tasks += len(main_tasks)
            print("Summary:")
            print(f"  Active tasks (tasks.json): {len(main_tasks)}")
        except Exception:
            print("Summary: Could not read tasks.json")
    print()


if __name__ == "__main__":
    main()
