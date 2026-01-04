#!/usr/bin/env python3
"""
Split the enhanced task plan into individual task files.

Usage:
    python scripts/split_enhanced_plan.py [--input FILE] [--output-dir DIR]

Options:
    --input FILE     Input markdown file (default: ../new_task_plan/complete_new_task_outline_ENHANCED.md)
    --output-dir DIR Output directory for task files (default: ../new_task_plan/task_files)
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict

# Task mapping for filenames
ORIGINAL_TASK_MAP = {
    0: 7,  # I1.T0 -> Task 7
    1: 9,  # I1.T1 -> Task 9
    2: 19,  # I1.T2 -> Task 19
    3: 54,  # I2.T1 -> Task 54
    4: 55,  # I2.T2 -> Task 55
    5: 56,  # I2.T3 -> Task 56
    6: 57,  # I2.T4 -> Task 57
    7: 58,  # I2.TX -> Task 58
    8: 59,  # I2.T5 -> Task 59
    9: 60,  # I2.T6 -> Task 60
    10: 61,  # I2.T7 -> Task 61
    11: 62,  # I2.T8 -> Task 62
    12: 63,  # I2.T9 -> Task 63
    13: 63,  # I2.T10 -> Task 63
    14: 23,  # I3.T1 -> Task 23
    15: 101,  # I3.T2 -> Task 101
    16: 27,  # I4.T1 -> Task 27
    17: 31,  # I4.T2 -> Task 31
    18: 40,  # I4.T3 -> Task 40
    19: 100,  # I5.T1 -> Task 100
}

INITIATIVE_NAMES = {
    0: "Initiative 1: Foundational CI/CD & Validation Framework",
    1: "Initiative 1: Foundational CI/CD & Validation Framework",
    2: "Initiative 1: Foundational CI/CD & Validation Framework",
    3: "Initiative 2: Build Core Alignment Framework",
    4: "Initiative 2: Build Core Alignment Framework",
    5: "Initiative 2: Build Core Alignment Framework",
    6: "Initiative 2: Build Core Alignment Framework",
    7: "Initiative 2: Build Core Alignment Framework",
    8: "Initiative 2: Build Core Alignment Framework",
    9: "Initiative 2: Build Core Alignment Framework",
    10: "Initiative 2: Build Core Alignment Framework",
    11: "Initiative 2: Build Core Alignment Framework",
    12: "Initiative 2: Build Core Alignment Framework",
    13: "Initiative 2: Build Core Alignment Framework",
    14: "Initiative 3: Alignment Execution",
    15: "Initiative 3: Alignment Execution",
    16: "Initiative 4: Codebase Stability & Maintenance",
    17: "Initiative 4: Codebase Stability & Maintenance",
    18: "Initiative 4: Codebase Stability & Maintenance",
    19: "Initiative 5: Post-Alignment Cleanup",
}


def parse_enhanced_plan(filepath: str):
    """Parse the enhanced plan markdown file."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    tasks = []
    current_task = None
    current_section_lines = []

    for line in lines:
        stripped = line.strip()

        # Check for task header
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


def parse_task_from_lines(task_data: Dict):
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

    # Extract status and priority
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

    # Collect description
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

    task["description"] = " ".join(desc_parts)

    # Extract subtasks
    subtask_pattern = r"#### (I[0-9]+\.T[X0-9]+\.[0-9]+): (.+?) \(ID: ([0-9]+)\)"
    subtask_matches = re.findall(subtask_pattern, text, re.DOTALL)

    for subtask_id, subtask_title, subtask_num in subtask_matches:
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

            purpose_match = re.search(r"\*\*Purpose:\*\*\s*(.+?)(?=\n|$)", subtask_text)
            if purpose_match:
                subtask["description"] = purpose_match.group(1).strip()

            desc_match = re.search(r"\*\*Description:\*\*\s*(.+?)(?=\n\*\*|$)", subtask_text)
            if desc_match and not subtask["description"]:
                subtask["description"] = desc_match.group(1).strip()

            steps_match = re.search(
                r"\*\*Steps:\*\*(.+?)(?=\*\*Success|\*\*Effort|\*\*Depends|\n####|\n##)",
                subtask_text,
                re.DOTALL,
            )
            if steps_match:
                subtask["details"] = "Steps:" + steps_match.group(1).strip()

            deps_match = re.search(r"\*\*Depends on:\*\*\s*(.+)", subtask_text)
            if deps_match and deps_match.group(1).strip():
                deps = deps_match.group(1).split(",")
                subtask["dependencies"] = [
                    d.strip() for d in deps if d.strip() and d.strip() != "None"
                ]

            task["subtasks"].append(subtask)

    return task


def generate_task_markdown(task: Dict, seq_id: int, initiative_name: str) -> str:
    """Generate a markdown file for a single task."""
    original_id = ORIGINAL_TASK_MAP.get(seq_id, seq_id)

    md = f"""# Task {original_id}: {task["title"]}

**Original ID:** {task["id"]}
**Status:** {task["status"]}
**Priority:** {task["priority"]}
**Sequential ID:** {seq_id}
**Initiative:** {initiative_name}

---

## Purpose

{task["description"]}

---

## Success Criteria

"""
    # Add success criteria based on subtasks
    for _i, subtask in enumerate(task.get("subtasks", []), 1):
        md += f"- [ ] {subtask['title']}\n"

    if not task.get("subtasks"):
        md += "- [ ] Task implementation complete\n"

    md += """
---

## Subtasks

"""

    for subtask in task.get("subtasks", []):
        md += f"### {subtask['id']}: {subtask['title']}\n\n"
        md += f"**Purpose:** {subtask['description']}\n\n"

        if subtask.get("details"):
            md += f"{subtask['details']}\n\n"

        if subtask.get("dependencies"):
            md += f"**Depends on:** {', '.join(subtask['dependencies'])}\n\n"

        md += "---\n\n"

    md += f"""---

## Implementation Notes

**Generated:** {datetime.now().isoformat()}
**Source:** complete_new_task_outline_ENHANCED.md
**Original Task ID:** {original_id}

"""

    return md


def main():
    parser = argparse.ArgumentParser(description="Split enhanced plan into individual task files")
    parser.add_argument(
        "--input",
        "-i",
        default="../new_task_plan/complete_new_task_outline_ENHANCED.md",
        help="Input markdown file",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="../new_task_plan/task_files",
        help="Output directory for task files",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    input_path = script_dir / args.input
    output_dir = script_dir / args.output_dir

    print(f"Parsing enhanced plan: {input_path}")

    tasks = parse_enhanced_plan(str(input_path))
    print(f"Found {len(tasks)} tasks\n")

    # Create output directory
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Track which task IDs have been created
    created_ids = {}

    # Generate task files
    for i, task in enumerate(tasks):
        original_id = ORIGINAL_TASK_MAP.get(i, i)
        initiative = INITIATIVE_NAMES.get(i, "Unknown Initiative")

        # Handle duplicate task IDs by using suffix
        if original_id in created_ids:
            filename = f"task-{original_id}-{created_ids[original_id] + 1}.md"
            created_ids[original_id] += 1
        else:
            filename = f"task-{original_id}.md"
            created_ids[original_id] = 1

        filepath = output_dir / filename

        md_content = generate_task_markdown(task, i, initiative)

        if args.dry_run:
            print(f"[DRY RUN] Would create: {filepath}")
            print(f"  Task {original_id}: {task['title'][:50]}...")
            print(f"  Subtasks: {len(task.get('subtasks', []))}\n")
        else:
            with open(filepath, "w") as f:
                f.write(md_content)
            print(f"Created: {filepath}")
            print(f"  Task {original_id}: {task['title'][:50]}...")
            print(f"  Subtasks: {len(task.get('subtasks', []))}\n")

    if not args.dry_run:
        # List all generated files
        files = sorted(output_dir.glob("task-*.md"))
        print(f"\nGenerated {len(files)} task files in: {output_dir}")
        for f in files:
            print(f"  - {f.name}")


if __name__ == "__main__":
    main()
