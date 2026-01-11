#!/usr/bin/env python3
"""
Converts a single task markdown file into a valid tasks.json structure.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

def parse_single_task_md(filepath: str) -> dict:
    """Parses a single task markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    task = {
        "subtasks": []
    }

    # Use regex to find key-value pairs like **Status:** pending
    metadata_patterns = {
        "title": r"^# Task ID: \d+\s*(.*)",
        "id": r"^# Task ID: (\d+)",
        "status": r"\*\*Status:\*\* (.*)",
        "priority": r"\*\*Priority:\*\* (.*)",
        "effort": r"\*\*Effort:\*\* (.*)",
        "complexity": r"\*\*Complexity:\*\* (.*)",
    }

    for key, pattern in metadata_patterns.items():
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            task[key] = match.group(1).strip()

    # Extract description from ## Purpose section
    purpose_match = re.search(r"## Purpose\n\n(.*?)\n\n---", content, re.DOTALL)
    if purpose_match:
        task["description"] = purpose_match.group(1).strip().replace('\n', ' ')
    else:
        task["description"] = task.get("title", "")


    # Extract subtasks from the markdown table
    subtask_table_match = re.search(r"## Subtask Status Summary\n\n\| ID\s*\| Subtask\s*\| Status\s*\| Effort\s*\| Dependencies\s*\|\n\|---*\|---*\|---*\|---*\|---*\|\n(.*?)(\n\n---|\Z)", content, re.DOTALL)
    if subtask_table_match:
        table_body = subtask_table_match.group(1)
        for line in table_body.strip().split('\n'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5:
                subtask_id_full = parts[1]
                # Extract the sub-id number
                subtask_id_num_match = re.search(r'(\d+\.\d+)', subtask_id_full)
                if not subtask_id_num_match:
                    continue
                
                subtask_id = subtask_id_num_match.group(1)

                subtask = {
                    "id": subtask_id,
                    "title": parts[2],
                    "status": parts[3],
                    "effort": parts[4],
                    "dependencies": [d.strip() for d in parts[5].split(',') if d.strip],
                    "description": "",
                    "details": "",
                    "testStrategy": "",
                    "parentId": task.get("id")
                }
                task["subtasks"].append(subtask)

    return task

def map_to_tasks_json_format(task: dict) -> dict:
    """Maps the parsed task to the final tasks.json structure."""
    
    # Map main task
    json_task = {
        "id": task.get("id"),
        "title": task.get("title", ""),
        "description": task.get("description", ""),
        "status": task.get("status", "pending"),
        "priority": task.get("priority", "medium"),
        "dependencies": [],
        "details": "",
        "subtasks": [],
        "testStrategy": "",
        "complexity": task.get("complexity", "0/10"),
        "effort": task.get("effort", "0 hours"),
        "updatedAt": datetime.now().isoformat(),
    }

    # Map subtasks
    for sub in task.get("subtasks", []):
        json_subtask = {
            "id": sub.get("id"),
            "title": sub.get("title"),
            "description": sub.get("description"),
            "dependencies": sub.get("dependencies", []),
            "details": sub.get("details", ""),

            "status": sub.get("status", "pending"),
            "parentId": sub.get("parentId"),
        }
        json_task["subtasks"].append(json_subtask)

    return {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "Generated from single task markdown.",
            "lastUpdated": datetime.now().isoformat(),
            "tasks": [json_task]
        }
    }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Converts a single task markdown file to a tasks.json structure.")
    parser.add_argument("markdown_file", help="Path to the task markdown file.")
    args = parser.parse_args()

    filepath = Path(args.markdown_file)
    if not filepath.is_file():
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)

    try:
        parsed_task = parse_single_task_md(str(filepath))
        tasks_json_structure = map_to_tasks_json_format(parsed_task)
        print(json.dumps(tasks_json_structure, indent=2))
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
