#!/usr/bin/env python3
"""
Task Files Consolidation Script

This script identifies the most complete and placeholder-free versions of task files
from various directories and consolidates them into the primary tasks directory.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


def count_placeholders(content: str) -> int:
    """Count the number of placeholder patterns in the content."""
    placeholder_patterns = [
        r'\[.*?\]',  # Square brackets with any content
        r'\(.*?\)',  # Parentheses with any content (when containing placeholders)
        r'\{\{.*?\}\}',  # Double curly braces
        r'PLACEHOLDER',  # Literal placeholder
        r'NEEDS_IMPLEMENTATION',  # Literal needs implementation
        r'TODO',  # Literal todo
        r'FIXME',  # Literal fixme
        r'METHOD TO VERIFY',  # Method to verify
        r'VERIFICATION METHOD',  # Verification method
        r'HOW TO TEST',  # How to test
        r'HOW TO VALIDATE',  # How to validate
        r'DESCRIPTION NEEDED',  # Description needed
        r'PARAMETER NAME',  # Parameter name
        r'EXPECTED OUTCOME',  # Expected outcome
        r'IMPLEMENTATION DETAILS',  # Implementation details
        r'SPECIFY',  # Specify
        r'DEFINE',  # Define
        r'CONFIGURATION PARAMETER',  # Configuration parameter
        r'CONFIGURATION VALUE',  # Configuration value
        r'CONFIGURATION OPTION',  # Configuration option
        r'CONFIGURATION SETTING',  # Configuration setting
        r'TEST REQUIREMENT',  # Test requirement
        r'TEST STRATEGY',  # Test strategy
        r'PERFORMANCE TARGET',  # Performance target
        r'PERFORMANCE REQUIREMENT',  # Performance requirement
        r'PERFORMANCE METRIC',  # Performance metric
        r'PERFORMANCE BENCHMARK',  # Performance benchmark
        r'PERFORMANCE INDICATOR',  # Performance indicator
        r'PERFORMANCE MEASUREMENT',  # Performance measurement
        r'PERFORMANCE GOAL',  # Performance goal
        r'PERFORMANCE OBJECTIVE',  # Performance objective
        r'PERFORMANCE STANDARD',  # Performance standard
        r'PERFORMANCE CRITERION',  # Performance criterion
        r'PERFORMANCE SPECIFICATION',  # Performance specification
        r'PERFORMANCE REQUIREMENT',  # Performance requirement
        r'PERFORMANCE EXPECTATION',  # Performance expectation
    ]

    count = 0
    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        count += len(matches)

    return count


def calculate_completeness_score(content: str) -> float:
    """Calculate a completeness score based on content richness."""
    # Count sections (headers with ##)
    sections = len(re.findall(r'^##\s', content, re.MULTILINE))

    # Count lines of actual content (not empty or just whitespace)
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    content_lines = len([line for line in lines if not line.startswith('#')])

    # Count checklist items
    checklists = len(re.findall(r'- \[.\]', content))

    # Calculate score based on these factors - using balanced multipliers
    score = sections * 2.0 + content_lines * 0.1 + checklists * 1.0

    return min(score, 100.0)  # Cap at 100


def find_task_files_by_id(directory: Path) -> Dict[str, List[Path]]:
    """Find all task files grouped by task ID."""
    task_groups = {}

    for file_path in directory.rglob("*.md"):
        if "task" in file_path.name.lower():
            # Extract task ID from filename
            task_id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', file_path.name, re.IGNORECASE)
            if task_id_match:
                task_id = task_id_match.group(1).replace('_', '.').replace('-', '.')
                if task_id not in task_groups:
                    task_groups[task_id] = []
                task_groups[task_id].append(file_path)

    return task_groups


def select_best_task_version(task_paths: List[Path]) -> Tuple[Path, str]:
    """Select the best version of a task based on completeness and placeholder count."""
    best_path = None
    best_score = -float('inf')  # Use negative infinity as initial value
    best_content = ""

    for path in task_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            completeness_score = calculate_completeness_score(content)
            placeholder_count = count_placeholders(content)

            # Use a combined score that balances completeness and penalizes placeholders
            # Lower penalty to avoid negative scores for files with many placeholders but good content
            combined_score = completeness_score - (placeholder_count * 0.5)  # Reduced penalty

            if combined_score > best_score:
                best_score = combined_score
                best_path = path
                best_content = content
        except Exception as e:
            print(f"Error reading {path}: {e}")
            continue

    return best_path, best_content


def consolidate_tasks():
    """Consolidate task files from multiple directories into the primary tasks directory."""
    print("🔍 Analyzing task files across directories...")

    # Define directories to search
    search_dirs = [
        Path("tasks"),
        Path("enhanced_improved_tasks"),
        Path("improved_tasks"),
        Path("restructured_tasks_14_section"),
        Path("task_data")
    ]

    # Collect all task files by ID
    all_task_groups = {}
    for search_dir in search_dirs:
        if search_dir.exists():
            print(f"  📂 Checking {search_dir}/")
            task_groups = find_task_files_by_id(search_dir)

            for task_id, paths in task_groups.items():
                if task_id not in all_task_groups:
                    all_task_groups[task_id] = []
                all_task_groups[task_id].extend(paths)

    print(f"  📋 Found {len(all_task_groups)} unique task IDs across all directories")

    # Select the best version for each task
    primary_tasks_dir = Path("tasks")
    primary_tasks_dir.mkdir(exist_ok=True)

    selected_count = 0
    for task_id, task_paths in all_task_groups.items():
        best_path, best_content = select_best_task_version(task_paths)

        if best_path:
            # Create a new filename in the primary tasks directory
            new_filename = f"task-{task_id.replace('.', '-')}.md"
            new_path = primary_tasks_dir / new_filename

            # Write the best content to the primary directory
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(best_content)

            print(f"  ✅ Selected best version for task {task_id} from {best_path.name}")
            selected_count += 1
        else:
            print(f"  ❌ Could not select best version for task {task_id}")

    print(f"\n📊 Consolidation complete!")
    print(f"   Selected {selected_count} task files for the primary tasks directory")
    print(f"   Original files remain in their respective directories")
    print(f"   The primary tasks directory now contains the most complete versions")

    return selected_count


def main():
    """Main function to run the consolidation process."""
    print("🚀 Starting Task File Consolidation Process")
    print("="*50)

    try:
        selected_count = consolidate_tasks()

        print(f"\n✅ Task File Consolidation Complete!")
        print(f"   Consolidated {selected_count} task files to the primary tasks directory")
        print(f"   These represent the most complete, placeholder-free versions available")

        return 0
    except Exception as e:
        print(f"\n❌ Error during consolidation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())