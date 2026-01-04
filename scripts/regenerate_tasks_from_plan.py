#!/usr/bin/env python3
"""
Regenerate tasks.json from the enhanced plan document.

This script parses complete_new_task_outline_ENHANCED.md and generates
a new tasks.json file that preserves all task details while adopting
the new initiative structure.

Usage:
    python regenerate_tasks_from_plan.py [--input FILE] [--output FILE] [--dry-run]

Options:
    --input FILE     Input markdown file (default: ../new_task_plan/complete_new_task_outline_ENHANCED.md)
    --output FILE    Output JSON file (default: tasks/tasks.json)
    --dry-run        Preview changes without writing files
    --validate       Validate only, don't generate output
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Original task IDs that map to new initiative tasks
ORIGINAL_TASK_MAP = {
    0: 7,  # I1.T0 -> Task 7
    1: 9,  # I1.T1 -> Task 9
    2: 19,  # I1.T2 -> Task 19
    3: 54,  # I2.T1 -> Task 54
    4: 55,  # I2.T2 -> Task 55
    5: 56,  # I2.T3 -> Task 56
    6: 57,  # I2.T4 -> Task 57
    7: 58,  # I2.TX -> Task 58 (RESTORED)
    8: 59,  # I2.T5 -> Task 59
    9: 60,  # I2.T6 -> Task 60
    10: 61,  # I2.T7 -> Task 61
    11: 62,  # I2.T8 -> Task 62
    12: 63,  # I2.T9 -> Task 63
    13: 63,  # I2.T10 -> Task 63 (merged)
    14: 23,  # I3.T1 -> Task 23
    15: 101,  # I3.T2 -> Task 101
    16: 27,  # I4.T1 -> Task 27
    17: 31,  # I4.T2 -> Task 31
    18: 40,  # I4.T3 -> Task 40
    19: 100,  # I5.T1 -> Task 100
}


def parse_enhanced_plan(filepath: str) -> List[Dict]:
    """Parse the enhanced plan markdown file."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    tasks = []
    current_task = None
    current_section_lines = []

    for line in lines:
        stripped = line.strip()

        # Check for task header (using [0-9] instead of \d for compatibility)
        header_match = re.match(r"## (I[0-9]+\.T[X0-9]+): (.+)", stripped)
        if header_match:
            # Save previous task if exists
            if current_task:
                current_task["lines"] = current_section_lines.copy()
                tasks.append(parse_task_from_lines(current_task))

            # Start new task
            current_task = {
                "id": header_match.group(1),
                "title": header_match.group(2),
                "lines": [],
            }
            current_section_lines = [line]
        elif current_task is not None:
            current_section_lines.append(line)

    # Don't forget last task
    if current_task:
        current_task["lines"] = current_section_lines
        tasks.append(parse_task_from_lines(current_task))

    return tasks


def parse_task_from_lines(task_data: Dict) -> Dict:
    """Parse a task from its lines."""
    lines = task_data.get("lines", [])
    text = "".join(lines)

    task = {
        "id": task_data.get("id", ""),
        "title": task_data.get("title", ""),
        "description": "",
        "status": "pending",
        "priority": "medium",
        "dependencies": [],
        "details": "",
        "subtasks": [],
        "testStrategy": "",
    }

    # Extract status and priority from metadata lines
    for line in lines:
        stripped = line.strip()
        if "**Status:**" in stripped:
            status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", stripped)
            if status_match:
                task["status"] = status_match.group(1)
        if "**Priority:**" in stripped:
            priority_match = re.search(r"\*\*Priority:\*\*\s*(\w+)", stripped)
            if priority_match:
                task["priority"] = priority_match.group(1)

    # Collect description from Purpose and Description sections
    desc_parts = []
    in_purpose = False
    in_desc = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### Purpose"):
            in_purpose = True
            in_desc = False
            continue
        if stripped.startswith("### Description"):
            in_purpose = False
            in_desc = True
            continue
        if stripped.startswith("### Success Criteria") or stripped.startswith("##"):
            in_purpose = False
            in_desc = False

        if (in_purpose or in_desc) and stripped and not stripped.startswith("**"):
            desc_parts.append(stripped)
        elif (in_purpose or in_desc) and stripped.startswith("**"):
            # Check for inline status/priority
            if "**Status:**" not in stripped and "**Priority:**" not in stripped:
                desc_parts.append(stripped)

    task["description"] = " ".join(desc_parts)

    # Extract subtasks (#### I2.TX.1 patterns - using [0-9] for compatibility)
    subtask_pattern = r"#### (I[0-9]+\.T[X0-9]+\.[0-9]+): (.+?) \(ID: ([0-9]+)\)"
    subtask_matches = re.findall(subtask_pattern, text, re.DOTALL)

    for subtask_id, subtask_title, subtask_num in subtask_matches:
        # Find the full subtask section
        subtask_text_match = re.search(
            rf"{re.escape(subtask_id)}.*?(?=\n####|\n##|\Z)", text, re.DOTALL
        )
        if subtask_text_match:
            subtask_text = subtask_text_match.group(0)

            subtask = {
                "id": subtask_num,
                "title": subtask_title,
                "description": "",
                "dependencies": [],
                "details": "",
                "status": "pending",
                "testStrategy": "",
            }

            # Extract purpose
            purpose_match = re.search(r"\*\*Purpose:\*\*\s*(.+?)(?=\n|$)", subtask_text)
            if purpose_match:
                subtask["description"] = purpose_match.group(1).strip()

            # Extract description
            desc_match = re.search(r"\*\*Description:\*\*\s*(.+?)(?=\n\*\*|$)", subtask_text)
            if desc_match and not subtask["description"]:
                subtask["description"] = desc_match.group(1).strip()

            # Extract steps
            steps_match = re.search(
                r"\*\*Steps:\*\*(.+?)(?=\*\*Success|\*\*Effort|\*\*Depends|\n####|\n##)",
                subtask_text,
                re.DOTALL,
            )
            if steps_match:
                subtask["details"] = "Steps:" + steps_match.group(1).strip()

            # Extract dependencies (only if match exists and has content)
            deps_match = re.search(r"\*\*Depends on:\*\*\s*(.+)", subtask_text)
            if deps_match and deps_match.group(1).strip():
                deps = deps_match.group(1).split(",")
                subtask["dependencies"] = [
                    d.strip() for d in deps if d.strip() and d.strip() != "None"
                ]
            else:
                subtask["dependencies"] = []

            task["subtasks"].append(subtask)

    return task


def map_task_to_json(task: Dict, sequential_id: int) -> Dict:
    """Map a parsed task to tasks.json format."""
    original_id = ORIGINAL_TASK_MAP.get(sequential_id, sequential_id)

    json_task = {
        "id": str(original_id),
        "title": task.get("title", ""),
        "description": task.get("description", ""),
        "status": task.get("status", "pending"),
        "priority": task.get("priority", "medium"),
        "dependencies": [],
        "details": task.get("details", ""),
        "subtasks": [],
        "testStrategy": task.get("testStrategy", ""),
        "complexity": len(task.get("subtasks", [])),
        "recommendedSubtasks": len(task.get("subtasks", [])),
        "expansionPrompt": "N/A - subtasks already defined.",
        "updatedAt": datetime.now().isoformat(),
    }

    for subtask in task.get("subtasks", []):
        json_subtask = {
            "id": int(subtask.get("id", 1)),
            "title": subtask.get("title", ""),
            "description": subtask.get("description", ""),
            "dependencies": subtask.get("dependencies", []),
            "details": subtask.get("details", ""),
            "testStrategy": subtask.get("testStrategy", ""),
            "status": subtask.get("status", "pending"),
            "parentId": str(original_id),
        }
        json_task["subtasks"].append(json_subtask)

    return json_task


def generate_tasks_json(tasks: List[Dict]) -> Dict:
    """Generate the full tasks.json structure."""
    json_tasks = []

    for i, task in enumerate(tasks):
        json_task = map_task_to_json(task, i)
        json_tasks.append(json_task)

    result = {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "Enhanced task plan for branch alignment",
            "lastUpdated": datetime.now().isoformat(),
            "tasks": json_tasks,
        }
    }

    return result


def validate_tasks(tasks: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate parsed tasks for consistency."""
    errors = []

    # Check for duplicate IDs
    ids = [t.get("id") for t in tasks if t.get("id")]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate task IDs found")

    # Check for required fields
    for i, task in enumerate(tasks):
        if not task.get("id"):
            errors.append(f"Task {i} missing ID")
        if not task.get("title"):
            errors.append(f"Task {task.get('id', i)} missing title")

    # Check subtask dependencies
    for task in tasks:
        for subtask in task.get("subtasks", []):
            dep = subtask.get("dependencies", [])
            if dep and not all(d.startswith("I") for d in dep):
                errors.append(f"Subtask {subtask.get('id')} has invalid dependencies: {dep}")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="Regenerate tasks.json from enhanced plan")
    parser.add_argument(
        "--input",
        "-i",
        default="../new_task_plan/complete_new_task_outline_ENHANCED.md",
        help="Input markdown file",
    )
    parser.add_argument("--output", "-o", default="tasks/tasks.json", help="Output JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--validate", action="store_true", help="Validate input only")

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    input_path = script_dir / args.input
    output_path = script_dir / args.output

    print(f"Parsing enhanced plan: {input_path}")

    tasks = parse_enhanced_plan(str(input_path))
    print(f"Found {len(tasks)} tasks")

    # Show found tasks
    for task in tasks:
        print(f"  - {task['id']}: {task['title'][:50]}...")
        print(f"    Subtasks: {len(task.get('subtasks', []))}")

    valid, errors = validate_tasks(tasks)
    if not valid:
        print("\nValidation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("\nValidation passed!")

    if args.validate:
        print("Validation complete. Exiting.")
        sys.exit(0)

    # Generate JSON
    tasks_json = generate_tasks_json(tasks)

    # Output
    if args.dry_run:
        print("\n=== Dry Run - Would generate ===")
        print(json.dumps(tasks_json, indent=2)[:3000])
        print("\n... (truncated)")
    else:
        if output_path.exists():
            backup_path = output_path.with_suffix(
                f".json.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            output_path.rename(backup_path)
            print(f"\nBacked up existing file to: {backup_path}")

        with open(output_path, "w") as f:
            json.dump(tasks_json, f, indent=2)
        print(f"\nGenerated new tasks.json: {output_path}")
        print(f"Total tasks: {len(tasks_json['master']['tasks'])}")
        print(f"Total subtasks: {sum(len(t['subtasks']) for t in tasks_json['master']['tasks'])}")


if __name__ == "__main__":
    main()
