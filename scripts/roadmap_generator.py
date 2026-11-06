import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import sys

@dataclass
class TaskInfo:
    id: str
    title: str
    status: str
    priority: str

def parse_task_file(file_path: str) -> Optional[TaskInfo]:
    """Parses a task markdown file and extracts metadata."""
    try:
        if os.path.isdir(file_path):
            print(f"Warning: {file_path} is a directory, skipping.", file=sys.stderr)
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return None

    title_match = re.search(r'# Task (\d+): (.*)', content)
    status_match = re.search(r'\*\*Status:\*\*\s*(.*)', content, re.IGNORECASE)
    priority_match = re.search(r'\*\*Priority:\*\*\s*(.*)', content, re.IGNORECASE)

    task_id = title_match.group(1) if title_match else Path(file_path).stem.replace('task_', '')
    title = title_match.group(2).strip() if title_match else "Unknown"
    status = status_match.group(1).strip() if status_match else "Unknown"
    priority = priority_match.group(1).strip() if priority_match else "Unknown"

    return TaskInfo(id=task_id, title=title, status=status, priority=priority)

def generate_roadmap(tasks_dir: str) -> str:
    """Generates a markdown roadmap table from task files in the directory."""
    tasks: List[TaskInfo] = []

    if not os.path.exists(tasks_dir):
        return "# Project Roadmap\n\nNo tasks found."

    for file in os.listdir(tasks_dir):
        if file.startswith('task_') and file.endswith('.md'):
            # Only include main tasks, not subtasks like task_006.3.md
            if re.match(r'^task_\d+\.md$', file):
                task = parse_task_file(os.path.join(tasks_dir, file))
                if task:
                    tasks.append(task)

    # Sort tasks by ID numerically
    tasks.sort(key=lambda t: int(t.id) if t.id.isdigit() else float('inf'))

    # Generate markdown table
    roadmap = "# Project Roadmap\n\n"
    roadmap += "| Task ID | Title | Status | Priority |\n"
    roadmap += "|---------|-------|--------|----------|\n"

    for task in tasks:
        # Escape pipe characters to avoid breaking the markdown table
        title = task.title.replace('|', r'\|')
        status = task.status.replace('|', r'\|')
        priority = task.priority.replace('|', r'\|')
        
        roadmap += f"| {task.id} | {title} | {status} | {priority} |\n"

    return roadmap

if __name__ == '__main__':
    # Normal execution
    tasks_dir = '.taskmaster/tasks'
    roadmap_content = generate_roadmap(tasks_dir)
    output_file = 'ROADMAP.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(roadmap_content)
    print(f"Roadmap generated at {output_file}")
