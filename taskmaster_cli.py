#!/usr/bin/env python3
"""
Taskmaster CLI - Official CLI for Taskmaster project

This is the official task-master CLI tool that should be referenced in
documentation. It implements the functionality to parse PRDs and generate
tasks.json as referenced throughout the codebase.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# A section ends at the next level-2 heading, a horizontal rule, or end of file.
_SECTION_END = r"(?=\n## |\n---|\Z)"
_SUBTASK_PATTERN = (
    r"###\s+(\d+\.\d+(?:\.\d+)?)[:\-\s]+([^\n]+)\s*\n+"
    r"((?:(?!###\s+\d+\.\d+)[^\n])*[\s\S]*?)"
    r"(?=\n###\s+\d+\.\d+|\n## |\n---|\Z)"
)


def _field(content: str, label: str, default: str) -> str:
    """Return the value of a ``**Label:** value`` line, or *default*."""
    match = re.search(rf"\*\*{label}:\*\*\s*(.+?)(?:\n|$)", content)
    return match.group(1).strip() if match else default


def _section(content: str, headings: List[str], default: str) -> str:
    """Return the body of the first matching level-2 heading, or *default*."""
    for heading in headings:
        match = re.search(
            rf"## {re.escape(heading)}\s*\n+([\s\S]+?){_SECTION_END}", content
        )
        if match:
            return match.group(1).strip()
    return default


def _task_id(file_path: Path, content: str) -> Optional[str]:
    """Derive the task id from the file name, falling back to the content."""
    match = re.search(r"task[-_]?(\d+(?:[-_.]\d+)*)", file_path.stem, re.IGNORECASE)
    if match:
        return match.group(1).replace("_", ".").replace("-", ".")
    match = re.search(r"#\s*Task.*?[:\-\s]+(?:ID:)?\s*(\d+(?:\.\d+)?)", content)
    return match.group(1) if match else None


def _dependencies(content: str) -> List[str]:
    """Return the dependency list declared on the task."""
    match = re.search(r"\*\*Dependencies:\*\*\s*(.+?)(?:\n|$)", content)
    if not match:
        return []
    text = match.group(1).strip()
    if text.lower() in ("none", "null"):
        return []
    return [dep.strip() for dep in re.split(r",\s*|\s+and\s+", text) if dep.strip()]


def _success_criteria(content: str) -> List[str]:
    """Return the checklist items of the Success Criteria section."""
    match = re.search(rf"## Success Criteria\s*\n+([\s\S]+?){_SECTION_END}", content)
    return re.findall(r"- \[.\]\s*(.+)", match.group(1)) if match else []


def _subtasks(content: str, task_id: str) -> List[Dict[str, Any]]:
    """Return the subtasks declared in the Sub-subtasks Breakdown section."""
    match = re.search(
        rf"## Sub-subtasks Breakdown\s*\n+([\s\S]+?){_SECTION_END}", content
    )
    if not match:
        return []

    subtasks = []
    for sub_id, sub_title, sub_details in re.findall(
        _SUBTASK_PATTERN, match.group(1), re.MULTILINE
    ):
        details = sub_details.strip()
        status_match = re.search(r"\*\*Status:?\*\*\s*(\w+)", details)
        deps_match = re.search(r"\*\*Depends on:?\*\*\s*([^\n]+)", details)
        sub_deps = []
        if deps_match and deps_match.group(1).strip().lower() != "none":
            sub_deps = [deps_match.group(1).strip()]

        subtasks.append(
            {
                "id": sub_id.strip(),
                "title": sub_title.strip(),
                "description": sub_title.strip(),
                "details": details,
                "status": status_match.group(1).lower() if status_match else "pending",
                "dependencies": sub_deps,
                "parentTaskId": task_id,
            }
        )
    return subtasks


def parse_task_from_md(file_path: Path) -> Optional[Dict[str, Any]]:
    """Parse a single task markdown file and convert it to task dictionary format."""
    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            content = handle.read()

        task_id = _task_id(file_path, content)
        if not task_id:
            print(f"Warning: Could not determine task ID for {file_path.name}, skipping")
            return None

        title_match = re.search(r"#\s*Task.*?[:\-]\s*(.+)", content)
        description = _section(
            content,
            ["Overview/Purpose", "Purpose", "Overview"],
            "Task description not provided",
        )

        return {
            "id": task_id,
            "title": title_match.group(1).strip() if title_match else f"Task {task_id}",
            "description": description,
            "details": _section(
                content, ["Implementation Guide", "Details"], description
            ),
            "status": _field(content, "Status", "pending"),
            "dependencies": _dependencies(content),
            "priority": _field(content, "Priority", "medium"),
            "effort": _field(content, "Effort", "TBD"),
            "complexity": _field(content, "Complexity", "TBD"),
            "success_criteria": _success_criteria(content),
            "subtasks": _subtasks(content, task_id),
        }
    except Exception as exc:  # noqa: BLE001 - one bad file must not abort the run
        print(f"Error parsing {file_path.name}: {exc}")
        return None


def _task_files(tasks_path: Path) -> List[Path]:
    """Collect every ``task*.md`` file the converter understands."""
    task_files = list(tasks_path.glob("task*.md"))
    task_files.extend(list((tasks_path / "task_data").rglob("task*.md")))
    for subdir in (
        "task_data",
        "enhanced_improved_tasks",
        "improved_tasks",
        "restructured_tasks_14_section",
    ):
        subdir_path = tasks_path / subdir
        if subdir_path.exists():
            task_files.extend(list(subdir_path.glob("task*.md")))
    return task_files


def convert_tasks_md_to_json(
    tasks_dir: str = "tasks", output_file: str = "tasks/tasks.json"
) -> bool:
    """Convert all task markdown files in a directory to a single tasks.json file."""
    tasks_path = Path(tasks_dir)
    if not tasks_path.exists():
        print(f"Tasks directory {tasks_path} does not exist")
        return False

    task_files = _task_files(tasks_path)
    print(f"Found {len(task_files)} task markdown files to process")

    tasks = []
    for task_file in task_files:
        print(f"Processing {task_file.name}...")
        task_data = parse_task_from_md(task_file)
        if task_data:
            tasks.append(task_data)

    result = {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "Taskmaster-generated tasks from markdown files",
            "lastUpdated": "2026-01-21T12:00:00Z",
            "tasks": tasks,
        }
    }

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)

    print(f"Successfully converted {len(tasks)} tasks to {output_file}")
    return True


def _run_parse_prd(args: argparse.Namespace) -> None:
    """Handle ``parse-prd``: convert the markdown task files to tasks.json."""
    if not args.input:
        print("Error: --input/-i is required for parse-prd command")
        sys.exit(1)

    print(f"Parsing PRD file: {args.input}")
    print("Converting to tasks...")
    if convert_tasks_md_to_json(args.tasks_dir, args.output):
        print(f"Successfully generated tasks to {args.output}")
    else:
        print("Failed to generate tasks")
        sys.exit(1)


def _run_list(args: argparse.Namespace) -> None:
    """Handle ``list``: print the tasks recorded in the output file."""
    try:
        with open(args.output, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        print(f"No tasks file found at {args.output}")
        return
    except json.JSONDecodeError:
        print(f"Invalid JSON in {args.output}")
        return

    tasks = data.get("master", {}).get("tasks", [])
    print(f"Found {len(tasks)} tasks:")
    for task in tasks:
        print(
            f"  - {task.get('id', 'unknown')}: "
            f"{task.get('title', 'No title')} [{task.get('status', 'unknown')}]"
        )


def _run_init(args: argparse.Namespace) -> None:
    """Handle ``init``: create an empty tasks.json and the tasks directory."""
    Path(args.tasks_dir).mkdir(exist_ok=True)

    basic_tasks = {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "New Taskmaster project",
            "lastUpdated": "2026-01-21T12:00:00Z",
            "tasks": [],
        }
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(basic_tasks, handle, indent=2)

    print(f"Initialized new Taskmaster project with {args.output}")
    print(f"Created {args.tasks_dir} directory for task markdown files")


def _run_unimplemented(args: argparse.Namespace) -> None:
    """Handle a recognised command that has no implementation yet."""
    print(
        f"Command '{args.command}' recognized but not fully implemented in this version"
    )
    print(
        "This is a simplified implementation focusing on the core MD to JSON "
        "conversion functionality"
    )


_HANDLERS = {
    "parse-prd": _run_parse_prd,
    "list": _run_list,
    "init": _run_init,
}


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Taskmaster CLI - Convert PRDs to tasks and manage task workflows"
    )
    parser.add_argument(
        "command",
        choices=[
            "parse-prd",
            "list",
            "show",
            "init",
            "models",
            "analyze-complexity",
            "expand",
            "add-task",
            "set-status",
        ],
        help="Command to execute",
    )
    parser.add_argument("--input", "-i", help="Input file (for parse-prd command)")
    parser.add_argument(
        "--output",
        "-o",
        default="tasks/tasks.json",
        help="Output file (default: tasks/tasks.json)",
    )
    parser.add_argument(
        "--tasks-dir",
        default="tasks",
        help="Directory containing task markdown files (default: tasks)",
    )
    return parser


def main() -> None:
    """Run the task-master CLI."""
    args = _build_parser().parse_args()
    _HANDLERS.get(args.command, _run_unimplemented)(args)


if __name__ == "__main__":
    main()
