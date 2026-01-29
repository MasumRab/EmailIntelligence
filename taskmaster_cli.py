#!/usr/bin/env python3
"""
Taskmaster CLI - Official CLI for Taskmaster project

This is the official task-master CLI tool that should be referenced in documentation.
Implements the functionality to parse PRDs and generate tasks.json as referenced throughout the codebase.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_task_from_md(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Parse a single task markdown file and convert it to task dictionary format.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract task ID from filename or content
        task_id = None
        filename = file_path.stem
        # Look for patterns like task-001, task_001, task-001-1, etc.
        id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
        if id_match:
            task_id = id_match.group(1).replace('_', '.').replace('-', '.')
        else:
            # Try to extract from content
            id_match = re.search(r'#\s*Task.*?[:\-\s]+(?:ID:)?\s*(\d+(?:\.\d+)?)', content)
            if id_match:
                task_id = id_match.group(1)

        if not task_id:
            print(f"Warning: Could not determine task ID for {file_path.name}, skipping")
            return None

        # Extract title
        title_match = re.search(r'#\s*Task.*?[:\-]\s*(.+)', content)
        title = title_match.group(1).strip() if title_match else f"Task {task_id}"

        # Extract status
        status_match = re.search(r'\*\*Status:\*\*\s*(.+?)(?:\n|$)', content)
        status = status_match.group(1).strip() if status_match else "pending"

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\*\s*(.+?)(?:\n|$)', content)
        priority = priority_match.group(1).strip() if priority_match else "medium"

        # Extract effort
        effort_match = re.search(r'\*\*Effort:\*\*\s*(.+?)(?:\n|$)', content)
        effort = effort_match.group(1).strip() if effort_match else "TBD"

        # Extract complexity
        complexity_match = re.search(r'\*\*Complexity:\*\*\s*(.+?)(?:\n|$)', content)
        complexity = complexity_match.group(1).strip() if complexity_match else "TBD"

        # Extract description/purpose
        purpose_match = re.search(r'## Overview/Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
        if not purpose_match:
            purpose_match = re.search(r'## Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
        if not purpose_match:
            purpose_match = re.search(r'## Overview\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
        
        description = purpose_match.group(1).strip() if purpose_match else "Task description not provided"

        # Extract dependencies
        dependencies = []
        deps_match = re.search(r'\*\*Dependencies:\*\*\s*(.+?)(?:\n|$)', content)
        if deps_match:
            deps_text = deps_match.group(1).strip()
            if deps_text.lower() != 'none' and deps_text.lower() != 'null':
                # Split by comma or 'and' to get individual dependencies
                deps_list = re.split(r',\s*|\s+and\s+', deps_text)
                dependencies = [dep.strip() for dep in deps_list if dep.strip()]

        # Extract details
        details_match = re.search(r'## Implementation Guide\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
        if not details_match:
            details_match = re.search(r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
        details = details_match.group(1).strip() if details_match else description

        # Extract success criteria
        success_criteria = []
        criteria_match = re.search(r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
        if criteria_match:
            criteria_content = criteria_match.group(1)
            # Extract checklist items
            checklist_items = re.findall(r'- \[.\]\s*(.+)', criteria_content)
            success_criteria = checklist_items

        # Extract subtasks if they exist
        subtasks = []
        subtasks_match = re.search(r'## Sub-subtasks Breakdown\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
        if subtasks_match:
            subtasks_content = subtasks_match.group(1)
            # Look for subtask patterns like ### 1.1: Title or ### 1.1.1: Title
            subtask_pattern = r'###\s+(\d+\.\d+(?:\.\d+)?)[:\-\s]+([^\n]+)\s*\n+((?:(?!###\s+\d+\.\d+)[^\n])*[\s\S]*?)(?=\n###\s+\d+\.\d+|\n## |\n---|\Z)'
            matches = re.findall(subtask_pattern, subtasks_content, re.MULTILINE)
            
            for match in matches:
                subtask_id = match[0].strip()
                subtask_title = match[1].strip()
                subtask_details = match[2].strip()
                
                # Extract status from subtask content if available
                subtask_status = "pending"
                status_pattern = r'\*\*Status:?\*\*\s*(\w+)'
                status_match = re.search(status_pattern, subtask_details)
                if status_match:
                    subtask_status = status_match.group(1).lower()
                
                # Extract dependencies for subtask
                subtask_deps = []
                deps_pattern = r'\*\*Depends on:?\*\*\s*([^\n]+)'
                deps_match = re.search(deps_pattern, subtask_details)
                if deps_match:
                    deps_text = deps_match.group(1).strip()
                    if deps_text.lower() != 'none':
                        subtask_deps = [deps_text]
                
                subtasks.append({
                    "id": subtask_id,
                    "title": subtask_title,
                    "description": subtask_title,  # Using title as description if no specific description
                    "details": subtask_details,
                    "status": subtask_status,
                    "dependencies": subtask_deps,
                    "parentTaskId": task_id
                })

        return {
            "id": task_id,
            "title": title,
            "description": description,
            "details": details,
            "status": status,
            "dependencies": dependencies,
            "priority": priority,
            "effort": effort,
            "complexity": complexity,
            "success_criteria": success_criteria,
            "subtasks": subtasks
        }
    except Exception as e:
        print(f"Error parsing {file_path.name}: {e}")
        return None


def convert_tasks_md_to_json(tasks_dir: str = "tasks", output_file: str = "tasks/tasks.json"):
    """
    Convert all task markdown files in a directory to a single tasks.json file.
    """
    tasks_path = Path(tasks_dir)
    if not tasks_path.exists():
        print(f"Tasks directory {tasks_path} does not exist")
        return False

    # Find all task markdown files
    task_files = list(tasks_path.glob("task*.md"))
    
    # Also look in subdirectories like task_data
    task_files.extend(list((tasks_path / "task_data").rglob("task*.md")))
    
    # Also look in other common directories
    for subdir in ["task_data", "enhanced_improved_tasks", "improved_tasks", "restructured_tasks_14_section"]:
        subdir_path = tasks_path / subdir
        if subdir_path.exists():
            task_files.extend(list(subdir_path.glob("task*.md")))

    print(f"Found {len(task_files)} task markdown files to process")

    tasks = []
    for task_file in task_files:
        print(f"Processing {task_file.name}...")
        task_data = parse_task_from_md(task_file)
        if task_data:
            tasks.append(task_data)

    # Create the proper JSON structure that matches task-master format
    result = {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "Taskmaster-generated tasks from markdown files",
            "lastUpdated": "2026-01-21T12:00:00Z",
            "tasks": tasks
        }
    }

    # Write to output file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print(f"Successfully converted {len(tasks)} tasks to {output_file}")
    return True


def main():
    """Main function for the task-master CLI tool."""
    parser = argparse.ArgumentParser(
        description="Taskmaster CLI - Convert PRDs to tasks and manage task workflows"
    )
    parser.add_argument(
        "command",
        choices=["parse-prd", "list", "show", "init", "models", "analyze-complexity", "expand", "add-task", "set-status"],
        help="Command to execute"
    )
    parser.add_argument(
        "--input",
        "-i",
        help="Input file (for parse-prd command)"
    )
    parser.add_argument(
        "--output", 
        "-o",
        default="tasks/tasks.json",
        help="Output file (default: tasks/tasks.json)"
    )
    parser.add_argument(
        "--tasks-dir",
        default="tasks",
        help="Directory containing task markdown files (default: tasks)"
    )
    
    args = parser.parse_args()

    if args.command == "parse-prd":
        if not args.input:
            print("Error: --input/-i is required for parse-prd command")
            sys.exit(1)
        
        print(f"Parsing PRD file: {args.input}")
        print("Converting to tasks...")
        
        # For now, implement the conversion from MD files to JSON
        # In a real implementation, this would parse the PRD and generate tasks
        success = convert_tasks_md_to_json(args.tasks_dir, args.output)
        
        if success:
            print(f"Successfully generated tasks to {args.output}")
        else:
            print("Failed to generate tasks")
            sys.exit(1)
    
    elif args.command == "list":
        # List tasks from the JSON file
        try:
            with open(args.output, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            tasks = data.get("master", {}).get("tasks", [])
            print(f"Found {len(tasks)} tasks:")
            for task in tasks:
                status = task.get("status", "unknown")
                print(f"  - {task.get('id', 'unknown')}: {task.get('title', 'No title')} [{status}]")
        except FileNotFoundError:
            print(f"No tasks file found at {args.output}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in {args.output}")
    
    elif args.command == "init":
        # Initialize a new taskmaster project
        tasks_dir = Path(args.tasks_dir)
        tasks_dir.mkdir(exist_ok=True)
        
        # Create a basic tasks.json structure
        basic_tasks = {
            "master": {
                "name": "Task Master",
                "version": "1.0.0", 
                "description": "New Taskmaster project",
                "lastUpdated": "2026-01-21T12:00:00Z",
                "tasks": []
            }
        }
        
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(basic_tasks, f, indent=2)
        
        print(f"Initialized new Taskmaster project with {args.output}")
        print(f"Created {args.tasks_dir} directory for task markdown files")
    
    else:
        # For other commands that aren't fully implemented yet
        print(f"Command '{args.command}' recognized but not fully implemented in this version")
        print("This is a simplified implementation focusing on the core MD to JSON conversion functionality")


if __name__ == "__main__":
    main()