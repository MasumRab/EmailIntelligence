"""
Taskmaster Command Module

Implements the core Taskmaster logic for parsing PRDs and generating tasks.json.
Ported from .taskmaster/taskmaster_cli.py.
"""

import json
import re
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..interface import Command


class TaskmasterCommand(Command):
    """
    Command for parsing task markdown files and generating a unified tasks.json.
    
    This command implements the official Taskmaster workflow for converting
    specification-driven task definitions into machine-readable JSON.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "taskmaster"

    @property
    def description(self) -> str:
        return "Parse PRD markdown files and generate tasks.json"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--tasks-dir", 
            default="tasks",
            help="Directory containing task markdown files"
        )
        parser.add_argument(
            "--output", 
            default="tasks/tasks.json",
            help="Path to the output tasks.json file"
        )
        parser.add_argument(
            "--validate-only", 
            action="store_true", 
            help="Validate markdown files without writing JSON"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the taskmaster command."""
        tasks_dir = Path(args.tasks_dir)
        output_file = Path(args.output)

        # Security validation
        if self._security_validator:
            for path in [tasks_dir, output_file.parent]:
                is_safe, error = self._security_validator.validate_path_security(str(path.absolute()))
                if not is_safe:
                    print(f"Error: Security violation for path '{path}': {error}")
                    return 1

        if not tasks_dir.exists():
            print(f"Error: Tasks directory '{tasks_dir}' does not exist")
            return 1

        print(f"🔍 Scanning for task markdown files in '{tasks_dir}'...")
        
        task_files = self._find_task_files(tasks_dir)
        print(f"Found {len(task_files)} task markdown files.")

        tasks = []
        for task_file in task_files:
            task_data = self._parse_task_from_md(task_file)
            if task_data:
                tasks.append(task_data)

        if args.validate_only:
            print(f"✅ Validation complete. {len(tasks)} tasks are valid.")
            return 0

        # Create Taskmaster JSON structure
        result = {
            "master": {
                "name": "Task Master",
                "version": "2.0.0 (Modular)",
                "description": "Taskmaster-generated tasks from modular CLI",
                "tasks": tasks
            }
        }

        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"🚀 Successfully generated '{output_file}' with {len(tasks)} tasks.")
            return 0
        except Exception as e:
            print(f"Error writing output file: {e}")
            return 1

    def _find_task_files(self, tasks_path: Path) -> List[Path]:
        """Find all task markdown files in common directories."""
        files = list(tasks_path.glob("task*.md"))
        
        # Look in known subdirectories
        subdirs = ["task_data", "enhanced_improved_tasks", "improved_tasks", "restructured_tasks_14_section"]
        for subdir in subdirs:
            subdir_path = tasks_path / subdir
            if subdir_path.exists():
                files.extend(list(subdir_path.glob("task*.md")))
        
        return files

    def _parse_task_from_md(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse a single task markdown file. (Ported regex logic)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # ID Extraction
            id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', file_path.stem, re.IGNORECASE)
            task_id = id_match.group(1).replace('_', '.').replace('-', '.') if id_match else None
            
            if not task_id:
                return None

            # Content Extraction
            title_match = re.search(r'#\s*Task.*?[:\-]\s*(.+)', content)
            status_match = re.search(r'\*\*Status:\*\*\s*(.+?)(?:\n|$)', content)
            priority_match = re.search(r'\*\*Priority:\*\*\s*(.+?)(?:\n|$)', content)
            
            return {
                "id": task_id,
                "title": title_match.group(1).strip() if title_match else f"Task {task_id}",
                "status": status_match.group(1).strip() if status_match else "pending",
                "priority": priority_match.group(1).strip() if priority_match else "medium",
                "source_file": str(file_path)
            }
        except Exception as e:
            print(f"Warning: Failed to parse {file_path.name}: {e}")
            return None
