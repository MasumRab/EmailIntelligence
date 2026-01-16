#!/usr/bin/env python3
"""
Task Metadata Manager for Task Master AI

This script addresses the limitation that Task Master's TaskEntity.toJSON() 
strips custom fields during serialization. It provides:

1. EMBED: Parse markdown task files and embed extended metadata into the 
   'details' field using a structured YAML-like format that survives 
   task-master operations.

2. BACKUP: Maintain backup markdown files for all tasks in case details 
   are lost during task-master operations (expand, update-task, etc.).

3. RESTORE: Restore task content from backups when needed.

4. SYNC: Synchronize metadata between markdown backups and tasks.json.

FIELDS NOT CAPTURED BY TASK-MASTER SCHEMA:
- effort (e.g., "2-3h")
- complexity (e.g., "7/10")  
- owner (e.g., "developer-name")
- successCriteria (checklist items)
- testStrategy (for subtasks - only tasks have this)
- initiative (grouping identifier)
- blocks (downstream dependencies)
- scope, focus (descriptive metadata)
- progressLog (timestamped notes)

Usage:
    python task_metadata_manager.py embed --task 001
    python task_metadata_manager.py backup --all
    python task_metadata_manager.py restore --task 001
    python task_metadata_manager.py sync --task 001
    python task_metadata_manager.py report

GitHub Issue Reference: https://github.com/eyaltoledano/claude-task-master/issues/1555
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Add task_scripts to path for shared utilities
sys.path.insert(0, str(Path(__file__).parent.parent / "task_scripts"))

try:
    from taskmaster_common import SecurityValidator, BackupManager, FileValidator
    HAS_COMMON = True
except ImportError:
    HAS_COMMON = False


# Configuration
TASKMASTER_ROOT = Path(__file__).parent.parent
TASKS_DIR = TASKMASTER_ROOT / "tasks"
TASKS_JSON = TASKS_DIR / "tasks.json"
BACKUP_DIR = TASKMASTER_ROOT / "backups" / "task_markdown_backups"
REPORTS_DIR = TASKMASTER_ROOT / "reports"

# Metadata delimiter used in details field
METADATA_START = "<!-- EXTENDED_METADATA"
METADATA_END = "END_EXTENDED_METADATA -->"


class TaskMetadataManager:
    """Manages extended metadata for Task Master tasks."""

    def __init__(self):
        self.tasks_json_path = TASKS_JSON
        self.tasks_dir = TASKS_DIR
        self.backup_dir = BACKUP_DIR
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Use shared BackupManager if available
        if HAS_COMMON:
            self.backup_manager = BackupManager(self.backup_dir)
        else:
            self.backup_manager = None

    def validate_path(self, filepath: str) -> bool:
        """Validate file path for security."""
        if HAS_COMMON:
            return SecurityValidator.validate_path_security(filepath, str(TASKMASTER_ROOT))
        return True  # Fallback: allow if no security module

    def load_tasks_json(self) -> dict:
        """Load tasks.json file."""
        if not self.tasks_json_path.exists():
            return {"master": {"tasks": []}}
        with open(self.tasks_json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_tasks_json(self, data: dict) -> None:
        """Save tasks.json file."""
        with open(self.tasks_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def parse_markdown_task(self, filepath: Path) -> dict:
        """
        Parse a markdown task file and extract extended metadata.
        
        Returns dict with:
        - id, title, status, priority, dependencies (standard fields)
        - effort, complexity, owner, initiative, etc. (extended fields)
        - successCriteria, testStrategy (extended fields)
        - subtasks (if present)
        - rawContent (full file content for backup)
        """
        if not filepath.exists():
            return {}

        content = filepath.read_text(encoding="utf-8")
        metadata = {"rawContent": content, "filepath": str(filepath)}

        # Extract title from first heading
        title_match = re.search(r"^#\s+(?:Task\s+(?:ID:?\s*)?)?(\d+[.\d]*)\s*[:\-]?\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
        if title_match:
            metadata["id"] = title_match.group(1).strip()
            metadata["title"] = title_match.group(2).strip()

        # Extract standard fields
        field_patterns = {
            "status": r"\*\*Status:?\*\*\s*(.+?)(?:\n|$)",
            "priority": r"\*\*Priority:?\*\*\s*(.+?)(?:\n|$)",
            "effort": r"\*\*Effort:?\*\*\s*(.+?)(?:\n|$)",
            "complexity": r"\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)",
            "owner": r"\*\*Owner:?\*\*\s*(.+?)(?:\n|$)",
            "initiative": r"\*\*Initiative:?\*\*\s*(.+?)(?:\n|$)",
            "dependencies": r"\*\*Dependencies:?\*\*\s*(.+?)(?:\n|$)",
            "blocks": r"\*\*Blocks:?\*\*\s*(.+?)(?:\n|$)",
            "scope": r"\*\*Scope:?\*\*\s*(.+?)(?:\n|$)",
            "focus": r"\*\*Focus:?\*\*\s*(.+?)(?:\n|$)",
        }

        for field, pattern in field_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metadata[field] = match.group(1).strip()

        # Extract Purpose/Description section
        purpose_match = re.search(r"##\s*Purpose\s*\n+([\s\S]+?)(?=\n##|\n---|\Z)", content)
        if purpose_match:
            metadata["purpose"] = purpose_match.group(1).strip()

        # Extract Success Criteria
        criteria_match = re.search(r"##\s*Success Criteria\s*\n+([\s\S]+?)(?=\n##|\n---|\Z)", content)
        if criteria_match:
            criteria_text = criteria_match.group(1)
            criteria = re.findall(r"-\s*\[[ x]\]\s*(.+)", criteria_text)
            if criteria:
                metadata["successCriteria"] = criteria

        # Extract Test Strategy
        test_match = re.search(r"(?:\*\*Test Strategy:?\*\*|##\s*Test Strategy)\s*\n*([\s\S]+?)(?=\n##|\n---|\n\*\*|\Z)", content)
        if test_match:
            metadata["testStrategy"] = test_match.group(1).strip()

        # Extract Details section
        details_match = re.search(r"(?:\*\*Details:?\*\*|##\s*Details)\s*\n*([\s\S]+?)(?=\n##|\n---|\n\*\*Success|\Z)", content)
        if details_match:
            metadata["details"] = details_match.group(1).strip()

        # Extract Progress Log
        log_match = re.search(r"##\s*Progress Log\s*\n+([\s\S]+?)(?=\n##|\Z)", content)
        if log_match:
            metadata["progressLog"] = log_match.group(1).strip()

        # Extract subtasks from table
        subtask_pattern = r"\|\s*(\d+\.\d+)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|"
        subtasks = []
        for match in re.finditer(subtask_pattern, content):
            subtasks.append({
                "id": match.group(1).strip(),
                "title": match.group(2).strip(),
                "status": match.group(3).strip(),
                "effort": match.group(4).strip(),
                "dependencies": match.group(5).strip(),
            })
        if subtasks:
            metadata["subtasks"] = subtasks

        return metadata

    def format_extended_metadata(self, metadata: dict) -> str:
        """
        Format extended metadata as a structured block to embed in details field.
        Uses HTML comments to preserve through task-master operations.
        """
        extended_fields = [
            "effort", "complexity", "owner", "initiative", "blocks",
            "scope", "focus", "successCriteria", "progressLog"
        ]

        lines = [METADATA_START]
        for field in extended_fields:
            if field in metadata and metadata[field]:
                value = metadata[field]
                if isinstance(value, list):
                    lines.append(f"{field}:")
                    for item in value:
                        lines.append(f"  - {item}")
                else:
                    lines.append(f"{field}: {value}")
        lines.append(METADATA_END)

        return "\n".join(lines)

    def extract_extended_metadata(self, details: str) -> tuple[str, dict]:
        """
        Extract extended metadata from details field.
        Returns (clean_details, metadata_dict).
        """
        if not details or METADATA_START not in details:
            return details or "", {}

        pattern = re.compile(
            rf"{re.escape(METADATA_START)}\s*([\s\S]*?)\s*{re.escape(METADATA_END)}",
            re.MULTILINE
        )
        match = pattern.search(details)
        if not match:
            return details, {}

        metadata_block = match.group(1)
        clean_details = pattern.sub("", details).strip()

        # Parse the metadata block
        metadata = {}
        current_key = None
        current_list = []

        for line in metadata_block.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("- ") and current_key:
                current_list.append(line[2:].strip())
            elif ":" in line:
                if current_key and current_list:
                    metadata[current_key] = current_list
                    current_list = []

                key, _, value = line.partition(":")
                current_key = key.strip()
                value = value.strip()
                if value:
                    metadata[current_key] = value
                    current_key = None

        if current_key and current_list:
            metadata[current_key] = current_list

        return clean_details, metadata

    def embed_metadata_in_task(self, task_id: str) -> bool:
        """
        Read markdown file for task and embed extended metadata into tasks.json.
        """
        # Find markdown file
        md_pattern = f"task-{task_id.zfill(3)}*.md" if "." not in task_id else f"task-{task_id.replace('.', '-')}.md"
        md_files = list(self.tasks_dir.glob(f"task-{task_id.zfill(3)}.md"))
        
        if not md_files:
            # Try without zero-padding
            md_files = list(self.tasks_dir.glob(f"task-{task_id}.md"))
        
        if not md_files:
            print(f"No markdown file found for task {task_id}")
            return False

        md_file = md_files[0]
        parsed = self.parse_markdown_task(md_file)

        if not parsed:
            print(f"Failed to parse {md_file}")
            return False

        # Load tasks.json
        data = self.load_tasks_json()
        tasks = data.get("master", {}).get("tasks", [])

        # Find matching task
        task_num = int(task_id.split(".")[0]) if "." in task_id else int(task_id)
        target_task = None
        for task in tasks:
            if task.get("id") == task_num:
                target_task = task
                break

        if not target_task:
            print(f"Task {task_id} not found in tasks.json")
            return False

        # Get existing details and remove old metadata block
        existing_details = target_task.get("details", "")
        clean_details, _ = self.extract_extended_metadata(existing_details)

        # Format new metadata block
        metadata_block = self.format_extended_metadata(parsed)

        # Combine: original details + metadata block
        if clean_details:
            new_details = f"{clean_details}\n\n{metadata_block}"
        else:
            new_details = metadata_block

        target_task["details"] = new_details

        # Save updated tasks.json
        self.save_tasks_json(data)
        print(f"Embedded metadata for task {task_id}")
        return True

    def backup_task(self, task_id: str) -> bool:
        """
        Create a timestamped backup of the task markdown file.
        """
        md_files = list(self.tasks_dir.glob(f"task-{task_id.zfill(3)}*.md"))
        if not md_files:
            md_files = list(self.tasks_dir.glob(f"task-{task_id}*.md"))

        if not md_files:
            print(f"No markdown files found for task {task_id}")
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_backup_dir = self.backup_dir / f"task-{task_id.zfill(3)}"
        task_backup_dir.mkdir(parents=True, exist_ok=True)

        for md_file in md_files:
            backup_name = f"{md_file.stem}_{timestamp}{md_file.suffix}"
            backup_path = task_backup_dir / backup_name
            shutil.copy2(md_file, backup_path)
            print(f"Backed up: {md_file.name} -> {backup_path}")

        # Also save current tasks.json entry
        data = self.load_tasks_json()
        task_num = int(task_id.split(".")[0])
        for task in data.get("master", {}).get("tasks", []):
            if task.get("id") == task_num:
                json_backup = task_backup_dir / f"task-{task_id.zfill(3)}_json_{timestamp}.json"
                with open(json_backup, "w", encoding="utf-8") as f:
                    json.dump(task, f, indent=2, ensure_ascii=False)
                print(f"Backed up JSON: {json_backup}")
                break

        return True

    def backup_all_tasks(self) -> int:
        """Backup all task markdown files."""
        md_files = list(self.tasks_dir.glob("task-*.md"))
        backed_up = set()

        for md_file in md_files:
            # Extract task ID from filename
            match = re.match(r"task-(\d+)", md_file.stem)
            if match:
                task_id = match.group(1)
                if task_id not in backed_up:
                    self.backup_task(task_id)
                    backed_up.add(task_id)

        print(f"\nBacked up {len(backed_up)} tasks")
        return len(backed_up)

    def list_backups(self, task_id: str) -> list[Path]:
        """List available backups for a task."""
        task_backup_dir = self.backup_dir / f"task-{task_id.zfill(3)}"
        if not task_backup_dir.exists():
            return []
        return sorted(task_backup_dir.glob("*.md"), reverse=True)

    def restore_from_backup(self, task_id: str, backup_index: int = 0) -> bool:
        """
        Restore task markdown from backup.
        backup_index: 0 = most recent, 1 = second most recent, etc.
        """
        backups = self.list_backups(task_id)
        if not backups:
            print(f"No backups found for task {task_id}")
            return False

        if backup_index >= len(backups):
            print(f"Backup index {backup_index} out of range (max: {len(backups) - 1})")
            return False

        backup_file = backups[backup_index]

        # Determine original filename
        original_name = re.sub(r"_\d{8}_\d{6}\.md$", ".md", backup_file.name)
        original_path = self.tasks_dir / original_name

        # Create backup of current before restoring
        if original_path.exists():
            self.backup_task(task_id)

        shutil.copy2(backup_file, original_path)
        print(f"Restored: {backup_file} -> {original_path}")
        return True

    def generate_report(self) -> dict:
        """
        Generate a report on metadata coverage across all tasks.
        """
        report = {
            "generated": datetime.now().isoformat(),
            "tasks_analyzed": 0,
            "tasks_with_extended_metadata": 0,
            "fields_coverage": {},
            "tasks": []
        }

        extended_fields = [
            "effort", "complexity", "owner", "initiative", "blocks",
            "scope", "focus", "successCriteria", "testStrategy", "progressLog"
        ]

        for field in extended_fields:
            report["fields_coverage"][field] = 0

        md_files = sorted(self.tasks_dir.glob("task-[0-9][0-9][0-9].md"))

        for md_file in md_files:
            report["tasks_analyzed"] += 1
            parsed = self.parse_markdown_task(md_file)

            task_info = {
                "id": parsed.get("id", md_file.stem),
                "title": parsed.get("title", "Unknown"),
                "has_extended_metadata": False,
                "fields_present": []
            }

            for field in extended_fields:
                if field in parsed and parsed[field]:
                    task_info["fields_present"].append(field)
                    report["fields_coverage"][field] += 1

            if task_info["fields_present"]:
                task_info["has_extended_metadata"] = True
                report["tasks_with_extended_metadata"] += 1

            report["tasks"].append(task_info)

        # Save report
        report_path = REPORTS_DIR / "metadata_coverage_report.json"
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\nMetadata Coverage Report")
        print(f"========================")
        print(f"Tasks analyzed: {report['tasks_analyzed']}")
        print(f"Tasks with extended metadata: {report['tasks_with_extended_metadata']}")
        print(f"\nField coverage:")
        for field, count in report["fields_coverage"].items():
            pct = (count / report["tasks_analyzed"] * 100) if report["tasks_analyzed"] > 0 else 0
            print(f"  {field}: {count} ({pct:.1f}%)")

        print(f"\nReport saved to: {report_path}")
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Task Metadata Manager - Preserve extended metadata for Task Master AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python task_metadata_manager.py embed --task 001
  python task_metadata_manager.py backup --all
  python task_metadata_manager.py backup --task 001
  python task_metadata_manager.py restore --task 001 --index 0
  python task_metadata_manager.py list-backups --task 001
  python task_metadata_manager.py report
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Embed command
    embed_parser = subparsers.add_parser("embed", help="Embed extended metadata into tasks.json")
    embed_parser.add_argument("--task", required=True, help="Task ID (e.g., 001)")
    embed_parser.add_argument("--all", action="store_true", help="Embed for all tasks")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Backup task markdown files")
    backup_parser.add_argument("--task", help="Task ID to backup")
    backup_parser.add_argument("--all", action="store_true", help="Backup all tasks")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("--task", required=True, help="Task ID to restore")
    restore_parser.add_argument("--index", type=int, default=0, help="Backup index (0=most recent)")

    # List backups command
    list_parser = subparsers.add_parser("list-backups", help="List available backups")
    list_parser.add_argument("--task", required=True, help="Task ID")

    # Report command
    subparsers.add_parser("report", help="Generate metadata coverage report")

    args = parser.parse_args()
    manager = TaskMetadataManager()

    if args.command == "embed":
        if args.all:
            md_files = sorted(manager.tasks_dir.glob("task-[0-9][0-9][0-9].md"))
            for md_file in md_files:
                match = re.match(r"task-(\d+)", md_file.stem)
                if match:
                    manager.embed_metadata_in_task(match.group(1))
        else:
            manager.embed_metadata_in_task(args.task)

    elif args.command == "backup":
        if args.all:
            manager.backup_all_tasks()
        elif args.task:
            manager.backup_task(args.task)
        else:
            parser.error("Specify --task or --all")

    elif args.command == "restore":
        manager.restore_from_backup(args.task, args.index)

    elif args.command == "list-backups":
        backups = manager.list_backups(args.task)
        if backups:
            print(f"Backups for task {args.task}:")
            for i, backup in enumerate(backups):
                print(f"  [{i}] {backup.name}")
        else:
            print(f"No backups found for task {args.task}")

    elif args.command == "report":
        manager.generate_report()


if __name__ == "__main__":
    main()
