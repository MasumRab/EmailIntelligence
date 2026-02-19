#!/usr/bin/env python3
from __future__ import annotations

from collections import OrderedDict
from datetime import date
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = ROOT / "tasks"
MAP_PATH = ROOT / "OPTION_C_VISUAL_MAP.md"

TASK_FILE_RE = re.compile(r"^task_(\d{3})\.md$")
TITLE_RE = re.compile(r"^#\s+Task\s+\d+\s*[:\-]?\s*(.+)$")
DEPENDENCY_PATTERNS = [
    re.compile(r"^\*\*Dependencies:\*\*\s*(.+)$", re.I),
    re.compile(r"^\*\*Dependencies\*\*:\s*(.+)$", re.I),
    re.compile(r"^Dependencies:\s*(.+)$", re.I),
]
ARTIFACT_RE = re.compile(r"`([^`]+\.(?:json|md|yaml|yml|csv|txt))`")


def normalize_dependency(value: str) -> str:
    cleaned = value.strip()
    # Remove any leading/trailing asterisks that might be part of markdown formatting
    cleaned = re.sub(r"^\*+|\*+$", "", cleaned).strip()
    
    # Check for "None" specifically after stripping asterisks
    if cleaned.lower() == "none":
        return "None"
    
    # Otherwise, perform general cleanup, removing non-alphanumeric characters (except commas, parentheses, hyphens, periods).
    cleaned = re.sub(r"[^\w\s,().-]", "", cleaned).strip()
    return cleaned or "None"


def extract_task_info(path: Path) -> dict:
    title = None
    dependencies = None
    artifacts = []
    seen_artifacts = OrderedDict()

    for line in path.read_text().splitlines():
        if title is None:
            title_match = TITLE_RE.match(line)
            if title_match:
                title = title_match.group(1).strip()

        if dependencies is None:
            stripped = line.strip()
            for pattern in DEPENDENCY_PATTERNS:
                match = pattern.match(stripped)
                if match:
                    dependencies = normalize_dependency(match.group(1))
                    break

        for match in ARTIFACT_RE.finditer(line):
            artifact = match.group(1)
            if artifact not in seen_artifacts:
                seen_artifacts[artifact] = None
        if seen_artifacts:
            artifacts = list(seen_artifacts.keys())

    if dependencies is None:
        dependencies = "None"

    return {
        "title": title or "Untitled Task",
        "dependencies": dependencies,
        "artifacts": artifacts,
    }


def format_artifacts(artifacts: list[str]) -> str:
    if not artifacts:
        return "None listed"
    shown = artifacts[:5]
    suffix = ""
    if len(artifacts) > 5:
        suffix = f" (+{len(artifacts) - 5} more)"
    rendered = ", ".join(f"`{artifact}`" for artifact in shown)
    return f"{rendered}{suffix}"


def build_inventory() -> tuple[list[str], list[str], int]:
    task_rows = []
    missing_titles = []
    missing_outputs = 0

    task_files = sorted(
        [path for path in TASKS_ROOT.glob("task_*.md") if TASK_FILE_RE.match(path.name)],
        key=lambda p: int(TASK_FILE_RE.match(p.name).group(1)),
    )

    for path in task_files:
        match = TASK_FILE_RE.match(path.name)
        if not match:
            continue
        task_id = match.group(1)
        if int(task_id) > 28:
            continue

        info = extract_task_info(path)
        if info["title"] == "Untitled Task":
            missing_titles.append(task_id)
        outputs = format_artifacts(info["artifacts"])
        if outputs == "None listed":
            missing_outputs += 1
        task_rows.append(
            f"| {task_id} | {info['title']} | {info['dependencies']} | {outputs} |"
        )

    return task_rows, missing_titles, missing_outputs


def build_section() -> str:
    task_rows, missing_titles, missing_outputs = build_inventory()
    missing_titles_text = ", ".join(missing_titles) if missing_titles else "None"

    section_lines = [
        f"## Current Task Framework Map ({date.today().isoformat()})",
        "",
        "This section reflects the current task files (001-028) as they exist now. "
        "It is added above the legacy Option C map to preserve historical reference.",
        "",
        "### Task Inventory",
        "| Task ID | Title | Dependencies (Normalized) | Outputs |",
        "| --- | --- | --- | --- |",
        *task_rows,
        "",
        "### Drift Summary",
        f"- Tasks with missing titles: {missing_titles_text}.",
        f"- Output artifacts remain unevenly specified; {missing_outputs} tasks list none while Task 002 references extensive legacy artifacts.",
        "",
        "### Notes",
        "- Dependency values are taken from the task headers and may be stale where tasks still reference older IDs.",
        "- Output values list the first few named artifacts or note when an output section exists; many tasks still lack explicit output definitions.",
        "- Use the dependency/output audit to identify missing or inconsistent references before aligning the map.",
        "",
    ]

    return "\n".join(section_lines)


def main() -> None:
    content = MAP_PATH.read_text()
    start_marker = "## Current Task Framework Map"
    end_marker = "## 1. ASCII Dependency Map"

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    if end_index == -1:
        raise RuntimeError("Could not locate ASCII map section marker in OPTION_C_VISUAL_MAP.md")
    if start_index != -1 and end_index <= start_index:
        raise RuntimeError("Could not locate map section markers in OPTION_C_VISUAL_MAP.md")

    new_section = build_section()
    if start_index == -1:
        updated = f"{content[:end_index]}{new_section}\n\n{content[end_index:]}"
    else:
        updated = f"{content[:start_index]}{new_section}\n{content[end_index:]}"
    MAP_PATH.write_text(updated)


if __name__ == "__main__":
    main()
