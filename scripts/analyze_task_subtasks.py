#!/usr/bin/env python3
"""
Task Subtask Analysis Tool
Identifies tasks that lack subtasks for complexity management
"""

import re
from pathlib import Path
import json
from typing import List, Dict, Any


def analyze_task_subtasks(task_file_path: str) -> Dict[str, Any]:
    """
    Analyze a task file to determine if it has subtasks defined.
    """
    with open(task_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    task_info = {
        'file_path': str(task_file_path),
        'file_name': task_file_path.name,
        'has_subtasks': False,
        'subtask_count': 0,
        'subtask_section_found': False,
        'subtask_section_type': None,
        'title': 'Unknown',
        'id': 'Unknown',
        'status': 'Unknown',
        'complexity': 'Unknown'
    }

    # Extract task ID and title from header
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['title'] = title_match.group(1).strip()

    # Extract ID from filename or content
    filename = task_file_path.stem
    id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
    if id_match:
        task_info['id'] = id_match.group(1).replace('_', '.').replace('-', '.')

    # Look for various subtask section headings
    subtask_patterns = [
        r'## Sub-subtasks Breakdown',
        r'## Subtasks',
        r'## Sub-subtasks',
        r'## Implementation Sub-steps',
        r'## Task Breakdown',
        r'### \d+\.\d+\.?\s+',  # Pattern for subtask headers like "### 1.1. ..."
    ]

    for pattern in subtask_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            task_info['subtask_section_found'] = True
            if 'Sub-subtasks' in pattern or 'Subtasks' in pattern:
                task_info['subtask_section_type'] = pattern.replace('## ', '').replace('### ', '')

    # Count actual subtasks if section is found
    if task_info['subtask_section_found']:
        # Look for subtask entries in various formats
        # Format 1: Table format with ID column
        table_matches = re.findall(r'\|\s*ID\s*\|\s*Subtask\s*\|[\s\S]*?\n((?:\|\s*[^\n]*\s*\|.*\n(?:\|\s*[^\n]*\s*\|.*\n)*)+)', content)
        if table_matches:
            for table in table_matches:
                rows = table.strip().split('\n')
                # Count rows that have actual content (not just header separators)
                actual_rows = [row for row in rows if '|' in row and not re.match(r'^\|\s*-+\s*\|\s*-+\s*\|', row)]
                task_info['subtask_count'] += len(actual_rows)

        # Format 2: List format with checkboxes
        checklist_matches = re.findall(r'- \[.\]\s*.*?(?=\n\s*-\s*\[)', content + '\n')  # Add newline to catch last item
        task_info['subtask_count'] += len(checklist_matches)

        # Format 3: Header format (### 1.1, ### 1.2, etc.)
        header_matches = re.findall(r'###\s+\d+\.\d+\.?\s+', content)
        task_info['subtask_count'] += len(header_matches)

    # Determine if task has meaningful subtasks (more than just section header)
    task_info['has_subtasks'] = task_info['subtask_count'] > 0

    # Extract additional metadata
    status_match = re.search(r'\*\*Status:?\*\*\s*(.+?)(?:\n|$)', content)
    if status_match:
        task_info['status'] = status_match.group(1).strip()

    complexity_match = re.search(r'\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)', content)
    if complexity_match:
        task_info['complexity'] = complexity_match.group(1).strip()

    return task_info


def main():
    tasks_dir = Path("/home/masum/github/PR/.taskmaster/tasks")
    task_files = list(tasks_dir.glob("task*.md"))

    print(f"Analyzing {len(task_files)} task files for subtask presence...")

    tasks_with_subtasks = []
    tasks_without_subtasks = []

    for task_file in task_files:
        analysis = analyze_task_subtasks(task_file)
        if analysis['has_subtasks']:
            tasks_with_subtasks.append(analysis)
        else:
            tasks_without_subtasks.append(analysis)

    print(f"\nAnalysis Results:")
    print(f"- Tasks WITH subtasks: {len(tasks_with_subtasks)}")
    print(f"- Tasks WITHOUT subtasks: {len(tasks_without_subtasks)}")
    print(f"- Total tasks analyzed: {len(task_files)}")

    if tasks_without_subtasks:
        print(f"\nTasks lacking subtasks for complexity management:")
        print("-" * 60)
        for i, task in enumerate(tasks_without_subtasks, 1):
            print(f"{i:2d}. {task['file_name']}")
            print(f"    Title: {task['title']}")
            print(f"    ID: {task['id']}")
            print(f"    Status: {task['status']}")
            print(f"    Complexity: {task['complexity']}")
            print(f"    Subtask count: {task['subtask_count']}")
            print()

    # Create detailed report
    report = {
        "summary": {
            "total_tasks": len(task_files),
            "tasks_with_subtasks": len(tasks_with_subtasks),
            "tasks_without_subtasks": len(tasks_without_subtasks),
            "percentage_without_subtasks": round((len(tasks_without_subtasks) / len(task_files)) * 100, 2)
        },
        "tasks_without_subtasks": tasks_without_subtasks,
        "tasks_with_subtasks": tasks_with_subtasks
    }

    # Save detailed report
    with open("task_subtask_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"Detailed analysis report saved to task_subtask_analysis_report.json")

    # Generate recommendations
    if tasks_without_subtasks:
        print(f"\nRECOMMENDATIONS:")
        print(f"Based on the analysis, {len(tasks_without_subtasks)} tasks lack subtasks which is important for complexity management.")
        print(f"For better complexity management, consider breaking down these tasks into smaller subtasks.")
        print(f"This will improve:")
        print(f"- Task tracking and progress monitoring")
        print(f"- Assignment of work to different team members")
        print(f"- Estimation accuracy")
        print(f"- Risk management")
        print(f"- Quality assurance")

    return 0


if __name__ == "__main__":
    exit(main())