#!/usr/bin/env python3
"""Round-trip test: verify markdown tasks ↔ tasks.json data consistency.

Parses all tasks/task_*.md files and .taskmaster/tasks/tasks.json,
compares shared fields, and reports mismatches and orphans.

Usage:
    python scripts/roundtrip_test.py
"""

import json
import os
import re
import sys
from pathlib import Path

# Resolve project root (one level up from scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TASKS_MD_DIR = PROJECT_ROOT / "tasks"
TASKS_JSON_PATH = PROJECT_ROOT / ".taskmaster" / "tasks" / "tasks.json"

# ---------------------------------------------------------------------------
# Phase 1: Parse markdown files
# ---------------------------------------------------------------------------

# Matches filenames like task_001.md, task_001.2.md, task_075.md
TASK_FILE_RE = re.compile(r"^task_(\d+(?:\.\d+)?)\.md$")


def _normalize_id(raw_id: str) -> str:
    """Normalize a task ID to its canonical form (strip leading zeros per segment).

    '001'   -> '1'
    '001.2' -> '1.2'
    '012.3' -> '12.3'
    """
    parts = raw_id.split(".")
    return ".".join(str(int(p)) for p in parts)


def _extract_meta_field(text: str, field: str) -> str | None:
    """Extract a **Field:** value from markdown text."""
    pattern = re.compile(rf"^\*\*{re.escape(field)}:\*\*\s*(.+)$", re.MULTILINE)
    m = pattern.search(text)
    if m:
        return m.group(1).strip()
    return None


def _extract_title(text: str) -> str | None:
    """Extract title from '# Task NNN: Title' header."""
    m = re.search(r"^#\s+Task\s+[\d.]+:\s*(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


def parse_markdown_tasks() -> dict[str, dict]:
    """Return {normalized_id: {title, status, priority, dependencies, effort, complexity}}."""
    tasks: dict[str, dict] = {}
    if not TASKS_MD_DIR.is_dir():
        print(f"WARNING: markdown tasks directory not found: {TASKS_MD_DIR}")
        return tasks

    for fname in sorted(os.listdir(TASKS_MD_DIR)):
        m = TASK_FILE_RE.match(fname)
        if not m:
            continue
        raw_id = m.group(1)
        norm_id = _normalize_id(raw_id)
        filepath = TASKS_MD_DIR / fname
        try:
            text = filepath.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"WARNING: could not read {filepath}: {exc}")
            continue

        deps_raw = _extract_meta_field(text, "Dependencies")
        if deps_raw and deps_raw.lower() not in ("none", "n/a", "-", ""):
            # Extract all numeric IDs (e.g. 001, 002.3) from freeform text
            dep_ids = sorted(
                {_normalize_id(d) for d in re.findall(r"\b(\d+(?:\.\d+)?)\b", deps_raw)}
            )
        else:
            dep_ids = []

        tasks[norm_id] = {
            "title": _extract_title(text),
            "status": (_extract_meta_field(text, "Status") or "").lower() or None,
            "priority": (_extract_meta_field(text, "Priority") or "").lower() or None,
            "dependencies": dep_ids,
            "effort": _extract_meta_field(text, "Effort"),
            "complexity": _extract_meta_field(text, "Complexity"),
        }
    return tasks


# ---------------------------------------------------------------------------
# Phase 2: Parse tasks.json
# ---------------------------------------------------------------------------


def _flatten_json_tasks(tasks_list: list[dict]) -> dict[str, dict]:
    """Flatten tasks (and nested subtasks) from tasks.json into {id_str: fields}."""
    result: dict[str, dict] = {}
    for t in tasks_list:
        tid = str(t.get("id", ""))
        deps = t.get("dependencies", []) or []
        dep_ids = sorted(str(d) for d in deps)
        result[tid] = {
            "title": t.get("title"),
            "status": (t.get("status") or "").lower() or None,
            "priority": (t.get("priority") or "").lower() or None,
            "dependencies": dep_ids,
        }
        for st in t.get("subtasks", []):
            stid = str(st.get("id", ""))
            sdeps = st.get("dependencies", []) or []
            sdep_ids = sorted(str(d) for d in sdeps)
            result[stid] = {
                "title": st.get("title"),
                "status": (st.get("status") or "").lower() or None,
                "priority": (st.get("priority") or "").lower() or None,
                "dependencies": sdep_ids,
            }
    return result


def parse_json_tasks() -> dict[str, dict]:
    """Return {id_str: {title, status, priority, dependencies}} from tasks.json."""
    if not TASKS_JSON_PATH.is_file():
        print(f"WARNING: tasks.json not found: {TASKS_JSON_PATH}")
        return {}
    try:
        data = json.loads(TASKS_JSON_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"WARNING: could not parse tasks.json: {exc}")
        return {}

    # Handle both flat list and wrapped {"master": {"tasks": [...]}} formats
    if isinstance(data, list):
        tasks_list = data
    elif isinstance(data, dict):
        if "tasks" in data:
            tasks_list = data["tasks"]
        elif "master" in data and isinstance(data["master"], dict):
            tasks_list = data["master"].get("tasks", [])
        else:
            tasks_list = []
    else:
        tasks_list = []

    return _flatten_json_tasks(tasks_list)


# ---------------------------------------------------------------------------
# Phase 3 & 4: Compare and report
# ---------------------------------------------------------------------------

COMPARE_FIELDS = ["title", "status", "priority", "dependencies"]


def compare_and_report(md_tasks: dict, json_tasks: dict) -> int:
    """Compare tasks and print a report. Returns exit code (0=ok, 1=mismatches)."""
    md_ids = set(md_tasks.keys())
    json_ids = set(json_tasks.keys())

    common = sorted(md_ids & json_ids, key=lambda x: [int(p) for p in x.split(".")])
    only_md = sorted(md_ids - json_ids, key=lambda x: [int(p) for p in x.split(".")])
    only_json = sorted(json_ids - md_ids, key=lambda x: [int(p) for p in x.split(".")])

    mismatches: list[tuple[str, str, object, object]] = []

    for tid in common:
        md = md_tasks[tid]
        js = json_tasks[tid]
        for field in COMPARE_FIELDS:
            mv = md.get(field)
            jv = js.get(field)
            if mv != jv:
                mismatches.append((tid, field, mv, jv))

    # ---- Report ----
    sep = "=" * 68
    print(sep)
    print("  ROUND-TRIP TEST: Markdown ↔ JSON Consistency Report")
    print(sep)
    print()
    print(f"  Markdown task files : {len(md_ids)}")
    print(f"  JSON tasks          : {len(json_ids)}")
    print(f"  Matched (both)      : {len(common)}")
    print(f"  Only in Markdown    : {len(only_md)}")
    print(f"  Only in JSON        : {len(only_json)}")
    print(f"  Field mismatches    : {len(mismatches)}")
    print()

    if only_md:
        print(f"  Orphaned in Markdown ({len(only_md)}):")
        for tid in only_md:
            title = md_tasks[tid].get("title") or "(no title)"
            print(f"    - Task {tid}: {title}")
        print()

    if only_json:
        print(f"  Orphaned in JSON ({len(only_json)}):")
        for tid in only_json:
            title = json_tasks[tid].get("title") or "(no title)"
            print(f"    - Task {tid}: {title}")
        print()

    if mismatches:
        print(f"  Mismatches ({len(mismatches)}):")
        for tid, field, mv, jv in mismatches:
            print(f"    Task {tid} / {field}:")
            print(f"      markdown : {mv}")
            print(f"      json     : {jv}")
        print()

    if common and not mismatches:
        print("  ✅ All matched tasks are consistent across both sources.")
        print()

    print("  ⚠  Known limitation: TaskEntity.toJSON() strips custom fields")
    print("     (effort, complexity, owner, successCriteria).")
    print("     See: https://github.com/eyaltoledano/claude-task-master/issues/1555")
    print()
    print(sep)

    return 1 if mismatches else 0


def main() -> int:
    md_tasks = parse_markdown_tasks()
    json_tasks = parse_json_tasks()
    return compare_and_report(md_tasks, json_tasks)


if __name__ == "__main__":
    sys.exit(main())
