#!/usr/bin/env python3
"""
Subtask Expansion Script

Reads a main task file with embedded subtask definitions and generates
individual subtask markdown files.

Usage:
    python scripts/expand_subtasks.py --task 002 --template task-002.md
    python scripts/expand_subtasks.py --task 075 --template task-075.md --output /path/to/output
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


TEMPLATE_HEADER = """# Task {id}: {title}

**Status:** {status}
**Priority:** {priority}
**Effort:** {effort}
**Complexity:** {complexity}
**Dependencies:** {dependencies}
**Created:** {created}
**Parent:** {parent}

---

## Purpose

{purpose}

---

## Details

{details}

---

## Success Criteria

{success_criteria}

---

## Test Strategy

{test_strategy}

---

## Implementation Notes

{notes}

---

## Progress Log

### {created_date}
- Subtask file created from main task template
- Ready for implementation

"""


def parse_subtasks(content: str) -> List[Dict]:
    """Extract subtask definitions from template content."""
    subtasks = []

    pattern = (
        r"### Subtask (\d+): ([^\n]+)\n\n(\| Field \| Value \|[\s\S]*?)(?=\n### Subtask |\n## |\Z)"
    )

    for match in re.finditer(pattern, content):
        subtask_num = match.group(1)
        section_title = match.group(2)
        table_and_body = match.group(3)

        table_match = re.search(
            r"\| \*\*ID\*\* \| ([^|]+) \|\n"
            r"\| \*\*Title\*\* \| ([^|]+) \|\n"
            r"\| \*\*Status\*\* \| ([^|]+) \|\n"
            r"\| \*\*Priority\*\* \| ([^|]+) \|\n"
            r"\| \*\*Effort\*\* \| ([^|]+) \|\n"
            r"\| \*\*Complexity\*\* \| ([^|]+) \|\n"
            r"\| \*\*Dependencies\*\* \| ([^|]+) \|\n"
            r"(?:\| \*\*Owner\*\* \| ([^|]+) \|\n)?",
            table_and_body,
        )

        if table_match:
            purpose = re.search(r"\*\*Purpose:\*\*\n(.+?)(?=\n\*\*|\Z)", table_and_body, re.DOTALL)
            details = re.search(r"\*\*Details:\*\*\n(.+?)(?=\n\*\*|\Z)", table_and_body, re.DOTALL)
            criteria = re.search(
                r"\*\*Success Criteria:\*\*\n([\s\S]+?)(?=\n\*\*|\Z)", table_and_body
            )
            test = re.search(r"\*\*Test Strategy:\*\*\n([\s\S]+?)(?=\n\*\*|\Z)", table_and_body)

            subtask: Dict[str, str] = {
                "subtask_id": subtask_num,
                "section_title": section_title.strip(),
                "id": table_match.group(1).strip(),
                "title": table_match.group(2).strip(),
                "status": table_match.group(3).strip(),
                "priority": table_match.group(4).strip(),
                "effort": table_match.group(5).strip(),
                "complexity": table_match.group(6).strip(),
                "dependencies": table_match.group(7).strip(),
                "owner": "",
                "purpose": "",
                "details": "",
                "success_criteria": "",
                "test_strategy": "",
            }

            if table_match.group(8):
                subtask["owner"] = table_match.group(8).strip()
            if purpose:
                subtask["purpose"] = purpose.group(1).strip()
            if details:
                subtask["details"] = details.group(1).strip()
            if criteria:
                subtask["success_criteria"] = criteria.group(1).strip()
            if test:
                subtask["test_strategy"] = test.group(1).strip()

            subtasks.append(subtask)

    return subtasks


def parse_main_task_info(content: str) -> Dict:
    """Extract main task information from template."""
    info: Dict[str, str] = {}

    title_match = re.search(r"^# Task (\d+): (.+?)$", content, re.MULTILINE)
    if title_match:
        info["task_number"] = title_match.group(1)
        info["title"] = title_match.group(2)

    return info


def format_success_criteria(criteria_text: str) -> str:
    """Convert criteria text to markdown checklist format."""
    lines = criteria_text.strip().split("\n")
    formatted: List[str] = []
    for line in lines:
        line = line.strip().rstrip(".")
        if line and not line.startswith("- [ ]"):
            formatted.append(f"- [ ] {line}")
        elif line.startswith("- [ ]"):
            formatted.append(line)
    return "\n".join(formatted) if formatted else "- [ ] TBD"


def generate_subtask_file(subtask: Dict, main_task: Dict, output_dir: Path) -> Path:
    """Generate a subtask markdown file from subtask data."""
    filename = f"task-{main_task['task_number']}-{subtask['subtask_id']}.md"
    filepath = output_dir / filename

    content = TEMPLATE_HEADER.format(
        id=subtask["id"],
        title=subtask["title"],
        status=subtask["status"],
        priority=subtask["priority"],
        effort=subtask["effort"],
        complexity=subtask["complexity"],
        dependencies=subtask["dependencies"],
        created=datetime.now().strftime("%Y-%m-%d"),
        parent=f"Task {main_task['task_number']}: {main_task['title']}",
        purpose=subtask["purpose"],
        details=subtask["details"],
        success_criteria=format_success_criteria(subtask["success_criteria"]),
        test_strategy=subtask["test_strategy"],
        notes="_Add implementation notes here as work progresses_",
        created_date=datetime.now().strftime("%Y-%m-%d"),
    )

    filepath.write_text(content)
    return filepath


def update_main_task_progress(template_path: Path, subtasks: List[Dict], main_task: Dict):
    """Update the progress tracking table in the main task file."""
    content = template_path.read_text()

    completed_count = sum(1 for s in subtasks if s["status"].lower() == "done")
    total = len(subtasks)
    progress_pct = int((completed_count / total) * 100) if total > 0 else 0

    table_lines = [
        "| Subtask | Status | Effort | Completed |",
        "|---------|--------|--------|-----------|",
    ]
    for subtask in subtasks:
        subtask_id = subtask["subtask_id"]
        table_lines.append(f"| {subtask_id} | {subtask['status']} | {subtask['effort']} | - |")

    total_effort = 0
    for s in subtasks:
        match = re.search(r"(\d+)", s["effort"])
        if match:
            total_effort += int(match.group(1))
    table_lines.extend(
        [
            "",
            f"**Total Progress:** {completed_count}/{total} subtasks ({progress_pct}%)",
            f"**Total Effort:** {total_effort}+ hours",
        ]
    )

    new_progress = "\n".join(table_lines)

    pattern = r"(## Progress Tracking\n\n\| Subtask.*?)(?=\n##|\n### |\Z)"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_progress + "\n", content, flags=re.DOTALL)

    template_path.write_text(content)


def expand_subtasks(template_path: Path, output_dir: Path, dry_run: bool = False) -> List[Path]:
    """Main function to expand subtasks from template."""
    template_content = template_path.read_text()
    main_task = parse_main_task_info(template_content)
    subtasks = parse_subtasks(template_content)

    if not subtasks:
        print("ERROR: No subtasks found in template!")
        print("Make sure subtasks follow the expected format.")
        sys.exit(1)

    print(f"Task {main_task['task_number']}: {main_task['title']}")
    print(f"Found {len(subtasks)} subtasks to expand\n")

    generated_files: List[Path] = []
    for subtask in subtasks:
        filepath = output_dir / f"task-{main_task['task_number']}-{subtask['subtask_id']}.md"
        if dry_run:
            print(f"  Would create: {filepath.name}")
        else:
            generate_subtask_file(subtask, main_task, output_dir)
            generated_files.append(filepath)
            print(f"  Created: {filepath.name}")

    if not dry_run:
        print(f"\nTotal: {len(generated_files)} subtask files generated")
        update_main_task_progress(template_path, subtasks, main_task)
        print(f"Updated progress tracking in: {template_path.name}")

    return generated_files


def main():
    parser = argparse.ArgumentParser(
        description="Expand subtask definitions from a main task template"
    )
    parser.add_argument("--task", "-t", required=True, help="Task number (e.g., 002)")
    parser.add_argument(
        "--template",
        "-f",
        default="task-{task}.md",
        help="Template file path (use {task} placeholder)",
    )
    parser.add_argument(
        "--output", "-o", default=None, help="Output directory (default: same as template)"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be created without creating files",
    )

    args = parser.parse_args()

    template_path = Path(args.template.format(task=args.task))
    if not template_path.is_absolute():
        template_path = Path.cwd() / template_path

    if not template_path.exists():
        print(f"ERROR: Template file not found: {template_path}")
        sys.exit(1)

    output_dir: Optional[Path]
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = template_path.parent

    expand_subtasks(template_path, output_dir, args.dry_run)


if __name__ == "__main__":
    main()
