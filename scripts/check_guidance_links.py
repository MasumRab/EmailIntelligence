#!/usr/bin/env python3
"""
Verify that guidance links in task files point to existing files.
"""

import os
import re
from pathlib import Path

def check_links():
    tasks_dir = Path("tasks")
    guidance_dir = Path("guidance")
    
    if not tasks_dir.exists():
        print(f"Error: {tasks_dir} directory not found.")
        return 1
        
    task_files = list(tasks_dir.glob("task-*.md"))
    if not task_files:
        print("No task files found.")
        return 0
        
    print(f"Checking {len(task_files)} task files for guidance links...")
    
    errors = []
    checked_count = 0
    link_count = 0
    
    # Regex to find markdown links: [text](path)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    for task_file in task_files:
        checked_count += 1
        content = task_file.read_text()
        
        links = link_pattern.findall(content)
        for text, path in links:
            if "../guidance/" in path:
                link_count += 1
                # Resolve path relative to the task file
                # task_file is in 'tasks/', path is '../guidance/file.md'
                # resolved_path should be 'guidance/file.md'
                resolved_path = (task_file.parent / path).resolve()
                
                # Check if it's within the project root
                project_root = Path.cwd()
                if not resolved_path.exists():
                    errors.append(f"{task_file}: Broken link [{text}]({path}) - File not found")
                elif not str(resolved_path).startswith(str(project_root)):
                     errors.append(f"{task_file}: Link [{text}]({path}) points outside project root")

    if errors:
        print(f"\nFound {len(errors)} broken guidance links:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print(f"\n✅ All {link_count} guidance links in {checked_count} task files are valid.")
        return 0

if __name__ == "__main__":
    exit(check_links())
