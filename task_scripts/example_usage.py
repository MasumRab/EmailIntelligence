#!/usr/bin/env python3
"""
Example usage of the Advanced Task File Manager
"""

import json
import tempfile
from pathlib import Path

from merge_task_manager import AdvancedTaskManager


def create_example_task_file():
    """Create an example tasks.json file with various issues."""
    example_data = {
        "tasks": [
            {
                "id": 1,
                "title": "Task 1 - Valid",
                "status": "pending",
                "priority": "high",
                "dependencies": [],
            },
            {
                "id": 1,  # Duplicate ID!
                "title": "Task 1 - Duplicate",
                "status": "in-progress",  # Different status
                "description": "This is a duplicate task that should be merged",
            },
            {
                "id": 2,
                "title": "Task 2 - Missing Status",
                # Missing status field
                "priority": "medium",
            },
            {
                "id": 3,
                "title": "Task 3 - Invalid Dependency",
                "status": "pending",
                "dependencies": [999, 1000],  # Invalid dependencies
            },
            {
                "id": 4,
                "title": "Task 4 - With Subtasks",
                "status": "pending",
                "subtasks": [
                    {"id": 1, "title": "Subtask 1", "status": "pending"},
                    {
                        "id": 1,  # Duplicate subtask ID!
                        "title": "Subtask 1 Duplicate",
                        "status": "in-progress",
                    },
                    {
                        "id": 2
                        # Missing title and status
                    },
                ],
            },
        ]
    }

    # Write to a temporary file
    temp_file = Path(tempfile.mktemp(suffix=".json"))
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(example_data, f, indent=2)

    return temp_file


def main():
    print("Advanced Task File Manager - Example Usage")
    print("=" * 50)

    # Create example file with issues
    example_file = create_example_task_file()
    print(f"Created example file: {example_file}")

    # Show original content
    print("\nOriginal file content:")
    print("-" * 30)
    with open(example_file, encoding="utf-8") as f:
        print(f.read())

    # Create manager instance
    manager = AdvancedTaskManager(str(example_file))

    print("\nAnalyzing file with AdvancedTaskManager...")
    print("-" * 50)

    # Get initial statistics
    initial_stats = manager.get_statistics()
    print(f"Initial statistics: {initial_stats}")

    # Validate without fixing first
    print("\nValidating file (no fixes)...")
    success_before = manager.validate_and_fix(fix_issues=False, create_backup=False)
    print(f"Validation passed: {success_before}")

    # Now fix the issues
    print("\nFixing issues with backup...")
    success_after = manager.validate_and_fix(
        fix_issues=True,
        create_backup=True,
        resolve_duplicates=True,
        fix_dependencies=True,
        fix_structure=True,
        fix_priorities=True,
        fix_orphans=True,
    )
    print(f"Fixing completed successfully: {success_after}")

    # Show final content
    print("\nFixed file content:")
    print("-" * 30)
    with open(example_file, encoding="utf-8") as f:
        print(f.read())

    # Get final statistics
    final_stats = manager.get_statistics()
    print(f"\nFinal statistics: {final_stats}")

    # Show backup files
    backup_files = list(manager.backup_dir.glob("tasks_backup_*.json"))
    print(f"\nCreated {len(backup_files)} backup file(s)")
    for backup in backup_files[-3:]:  # Show last 3 backups
        print(f"  - {backup}")

    # Clean up
    example_file.unlink()
    print(f"\nCleaned up example file: {example_file}")


if __name__ == "__main__":
    main()
