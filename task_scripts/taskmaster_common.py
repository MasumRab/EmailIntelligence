"""
Shared utilities for Task Master scripts to eliminate code duplication
"""

import json
import os
import re
import shutil
import tempfile
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union


class SecurityValidator:
    """Centralized security validation for all scripts"""

    @staticmethod
    def validate_path_security(filepath: str, base_dir: str = None) -> bool:
        """Validate that a path is safe and within allowed boundaries."""
        try:
            # Check for null bytes and other dangerous characters
            if "\x00" in filepath:
                return False

            # Use Path.resolve() to normalize the path
            path_obj = Path(filepath).resolve()
            normalized_path = str(path_obj)

            # Check for URL encoding and other bypass attempts
            path_lower = normalized_path.lower()
            if any(unsafe_pattern in path_lower for unsafe_pattern in ["%2e%2e", "%2f", "%5c"]):
                return False

            # Check for directory traversal using multiple methods
            path_str = str(path_obj).replace("\\", "/")
            if ".." in path_str.split("/"):
                return False

            # If base directory is specified, ensure path is within it
            if base_dir:
                base_path = Path(base_dir).resolve()
                try:
                    path_obj.relative_to(base_path)
                except ValueError:
                    return False

            # Additional safety checks
            suspicious_patterns = [
                r"\.\./",  # Path traversal
                r"\.\.\\",  # Path traversal (Windows)
                r"\$\(",  # Command substitution
                r"`.*`",  # Command substitution
                r";.*;",  # Multiple commands
                r"&&.*&&",  # Multiple commands
                r"\|\|.*\|\|",  # Multiple commands
                r"\.git",  # Git directory access
                r"\.ssh",  # SSH directory access
                r"/etc/",  # System config directory
                r"/root/",  # Root directory
                r"C:\\Windows\\",  # Windows system directory
                r"\x00",  # Null byte
            ]

            for pattern in suspicious_patterns:
                if re.search(pattern, normalized_path, re.IGNORECASE):
                    return False

            return True
        except Exception:
            return False


class BackupManager:
    """Centralized backup management"""

    def __init__(self, backup_dir: Optional[Path] = None):
        self.backup_dir = backup_dir or Path(tempfile.gettempdir()) / "taskmaster_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, filepath: str) -> str:
        """Create a backup of the original file with security validation."""
        # Validate path security first
        if not SecurityValidator.validate_path_security(filepath):
            raise ValueError(f"Security validation failed for: {filepath}")

        # Use UUID to avoid race conditions that could occur with timestamp-based naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        original_path = Path(filepath)
        backup_name = f"{original_path.stem}_{timestamp}_{unique_id}{original_path.suffix}"
        backup_path = self.backup_dir / backup_name

        # Copy the file and verify it was created successfully
        shutil.copy2(filepath, backup_path)

        # Verify backup was created successfully
        if not backup_path.exists():
            raise Exception(f"Failed to create backup file: {backup_path}")

        # Verify the backup has content and matches the original size
        if os.path.getsize(filepath) != os.path.getsize(backup_path):
            raise Exception(f"Backup size mismatch: {filepath} vs {backup_path}")

        return str(backup_path)


class FileValidator:
    """Centralized file validation utilities"""

    @staticmethod
    def validate_file_size(filepath: str, max_size: int = 50 * 1024 * 1024) -> bool:
        """Validate file size before processing to prevent memory issues."""
        try:
            file_size = os.path.getsize(filepath)
            return file_size <= max_size
        except OSError:
            return False

    @staticmethod
    def load_json_secure(filepath: str) -> Dict[str, Any]:
        """Securely load JSON with size validation and security checks."""
        if not SecurityValidator.validate_path_security(filepath):
            raise ValueError(f"Invalid or unsafe file path: {filepath}")

        max_size = 50 * 1024 * 1024  # Define max_size here
        if not FileValidator.validate_file_size(filepath, max_size):
            raise ValueError(f"File size exceeds maximum allowed size of {max_size} bytes")

        with open(filepath, encoding="utf-8") as f:
            content = f.read(max_size)

        # Check if file is larger than read content
        if len(content) == max_size:
            with open(filepath, encoding="utf-8") as f:
                f.seek(max_size)
                if f.read(1):  # If there's more content
                    raise ValueError("File size exceeds maximum allowed size")

        return json.loads(content)


class TaskValidator:
    """Centralized task validation utilities"""

    @staticmethod
    def collect_all_task_ids(
        tasks: List[Dict[str, Any]]
    ) -> tuple[Set[str], Dict[str, Any], List[str]]:
        """Collect all task IDs for dependency validation."""
        all_ids = set()
        all_ids_list = []
        lookup = {}

        for task in tasks:
            if not isinstance(task, dict):
                continue

            task_id = task.get("id")
            if task_id is not None:
                task_id_str = str(task_id)
                all_ids.add(task_id_str)
                all_ids_list.append(task_id_str)
                lookup[task_id_str] = task

                # Process subtasks
                if "subtasks" in task and isinstance(task["subtasks"], list):
                    for subtask in task["subtasks"]:
                        if not isinstance(subtask, dict):
                            continue

                        subtask_id = subtask.get("id")
                        if subtask_id is not None:
                            full_subtask_id = f"{task_id_str}.{subtask_id}"
                            all_ids.add(full_subtask_id)
                            all_ids_list.append(full_subtask_id)
                            lookup[full_subtask_id] = subtask

        return all_ids, lookup, all_ids_list

    @staticmethod
    def search_tasks(
        tasks: List[Dict[str, Any]], keyword: str, case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """Search for tasks by keyword in title, description, details, or status."""
        matches = []
        search_keyword = keyword if case_sensitive else keyword.lower()

        for task in tasks:
            if not isinstance(task, dict):
                continue

            # Prepare search fields
            search_fields = []
            for field in ["title", "description", "details", "status"]:
                if field in task and task[field] is not None:
                    field_value = str(task[field])
                    search_fields.append(field_value if case_sensitive else field_value.lower())

            # Check if keyword matches any field
            if any(search_keyword in field for field in search_fields):
                matches.append(task)

            # Search in subtasks as well
            if "subtasks" in task and isinstance(task["subtasks"], list):
                for subtask in task["subtasks"]:
                    if not isinstance(subtask, dict):
                        continue

                    subtask_fields = []
                    for field in ["title", "description", "details", "status"]:
                        if field in subtask and subtask[field] is not None:
                            field_value = str(subtask[field])
                            subtask_fields.append(
                                field_value if case_sensitive else field_value.lower()
                            )

                    if any(search_keyword in field for field in subtask_fields):
                        matches.append(subtask)

        return matches

    @staticmethod
    def find_tasks_by_status(tasks: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
        """Find tasks with a specific status."""
        matches = []

        for task in tasks:
            if not isinstance(task, dict):
                continue

            if task.get("status") == status:
                matches.append(task)

            # Check subtasks as well
            if "subtasks" in task and isinstance(task["subtasks"], list):
                for subtask in task["subtasks"]:
                    if isinstance(subtask, dict) and subtask.get("status") == status:
                        matches.append(subtask)

        return matches

    @staticmethod
    def find_task_by_id(
        tasks: List[Dict[str, Any]], task_id: Union[str, int]
    ) -> Optional[Dict[str, Any]]:
        """Find a task by ID, including in subtasks."""
        task_id_str = str(task_id)

        for task in tasks:
            if not isinstance(task, dict):
                continue

            if str(task.get("id")) == task_id_str:
                return task

            # Check subtasks
            if "subtasks" in task and isinstance(task["subtasks"], list):
                for subtask in task["subtasks"]:
                    if isinstance(subtask, dict) and str(subtask.get("id")) == task_id_str:
                        return subtask

        return None


class TaskComparison:
    """Utilities for comparing tasks across different files or datasets."""

    @staticmethod
    def compare_task_files(file_path1: str, file_path2: str, tag: str = "master") -> Dict[str, Any]:
        """Compare tasks between two JSON files."""
        # Validate file paths
        if not SecurityValidator.validate_path_security(file_path1):
            raise ValueError(f"Invalid or unsafe file path: {file_path1}")
        if not SecurityValidator.validate_path_security(file_path2):
            raise ValueError(f"Invalid or unsafe file path: {file_path2}")

        # Load both files
        data1 = FileValidator.load_json_secure(file_path1)
        data2 = FileValidator.load_json_secure(file_path2)

        # Extract tasks from both files
        tasks1 = TaskValidator.extract_tasks_from_data(data1, tag)
        tasks2 = TaskValidator.extract_tasks_from_data(data2, tag)

        # Compare the tasks
        return TaskComparison.compare_task_lists(tasks1, tasks2)

    @staticmethod
    def extract_tasks_from_data(data: Dict[str, Any], tag: str = "master") -> List[Dict[str, Any]]:
        """Extract tasks from data structure with proper tag handling."""
        if tag in data:
            return data[tag].get("tasks", [])
        elif "tasks" in data:
            return data["tasks"]
        elif isinstance(data, list):
            return data
        else:
            return []

    @staticmethod
    def compare_task_lists(
        tasks1: List[Dict[str, Any]], tasks2: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare two lists of tasks and return differences."""
        # Create lookup dictionaries by ID
        lookup1 = {str(task.get("id", f"temp_{i}")): task for i, task in enumerate(tasks1)}
        lookup2 = {str(task.get("id", f"temp_{i}")): task for i, task in enumerate(tasks2)}

        # Find added, removed, and modified tasks
        ids1 = set(lookup1.keys())
        ids2 = set(lookup2.keys())

        added = [lookup2[id] for id in ids2 - ids1]
        removed = [lookup1[id] for id in ids1 - ids2]
        common = ids1 & ids2

        modified = []
        for id in common:
            if TaskComparison.tasks_are_different(lookup1[id], lookup2[id]):
                modified.append({"id": id, "old": lookup1[id], "new": lookup2[id]})

        return {
            "added": added,
            "removed": removed,
            "modified": modified,
            "total_in_file1": len(tasks1),
            "total_in_file2": len(tasks2),
            "common_count": len(common),
        }

    @staticmethod
    def tasks_are_different(task1: Dict[str, Any], task2: Dict[str, Any]) -> bool:
        """Check if two tasks are different (excluding metadata like timestamps)."""
        # Create copies without temporary/metadata fields for comparison
        t1 = {k: v for k, v in task1.items() if k not in ["_created", "_modified", "_temp_id"]}
        t2 = {k: v for k, v in task2.items() if k not in ["_created", "_modified", "_temp_id"]}

        return t1 != t2


class TaskSummary:
    """Utilities for generating task summaries and statistics."""

    @staticmethod
    def generate_summary(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a comprehensive summary of tasks."""
        summary = {
            "total_tasks": 0,
            "status_counts": defaultdict(int),
            "priority_counts": defaultdict(int),
            "tasks_by_status": defaultdict(list),
            "tasks_by_priority": defaultdict(list),
            "has_dependencies": 0,
            "has_subtasks": 0,
            "subtasks_count": 0,
        }

        for task in tasks:
            if not isinstance(task, dict):
                continue

            summary["total_tasks"] += 1

            # Count by status
            status = task.get("status", "unknown")
            summary["status_counts"][status] += 1
            summary["tasks_by_status"][status].append(task.get("id"))

            # Count by priority
            priority = task.get("priority", "unknown")
            summary["priority_counts"][priority] += 1
            summary["tasks_by_priority"][priority].append(task.get("id"))

            # Check for dependencies
            if "dependencies" in task and task["dependencies"]:
                summary["has_dependencies"] += 1

            # Check for subtasks
            if "subtasks" in task and isinstance(task["subtasks"], list):
                summary["has_subtasks"] += 1
                summary["subtasks_count"] += len(task["subtasks"])

        # Convert defaultdicts to regular dicts for JSON serialization
        summary["status_counts"] = dict(summary["status_counts"])
        summary["priority_counts"] = dict(summary["priority_counts"])

        return summary
