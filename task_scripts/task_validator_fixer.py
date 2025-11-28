#!/usr/bin/env python3
"""
Comprehensive Task Master tasks.json validator and fixer.

This script provides robust validation and fixing capabilities for Task Master tasks.json files,
including:
- JSON structure validation and fixing
- Duplicate ID detection and resolution
- Dependency validation and fixing
- Subtask consistency checking
- Orphaned subtask detection
- Field consistency validation
- Backup creation and cleanup
- Priority weakness handling
- Flexible configuration and adaptation
"""

import json
import os
import sys
import re
import copy
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional, Union
import argparse
import logging


class TaskValidatorFixer:
    """Main class for validating and fixing tasks.json files."""

    def __init__(self, tasks_file: str = "tasks/tasks.json", backup_dir: str = ".taskmaster/backups"):
        """
        Initialize the validator/fixer.

        Args:
            tasks_file: Path to the tasks.json file
            backup_dir: Directory for backup files
        """
        self.tasks_file = Path(tasks_file)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Validation results
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
        self.all_task_ids = set()
        self.task_lookup = {}
        self.dependency_graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)

    @staticmethod
    def validate_path_security(filepath: str, base_dir: str = None) -> bool:
        """Validate that a path is safe and within allowed boundaries."""
        try:
            # Check for null bytes and other dangerous characters
            if '\x00' in filepath:
                return False

            # Use Path.resolve() to normalize the path
            path_obj = Path(filepath).resolve()
            normalized_path = str(path_obj)

            # Check for URL encoding and other bypass attempts
            path_lower = normalized_path.lower()
            if any(unsafe_pattern in path_lower for unsafe_pattern in ['%2e%2e', '%2f', '%5c']):
                return False

            # Check for directory traversal using multiple methods
            path_str = str(path_obj).replace('\\', '/')
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
                r'\.\./',  # Path traversal
                r'\.\.\\', # Path traversal (Windows)
                r'\$\(',   # Command substitution
                r'`.*`',   # Command substitution
                r';.*;',   # Multiple commands
                r'&&.*&&', # Multiple commands
                r'\|\|.*\|\|', # Multiple commands
                r'\.git',  # Git directory access
                r'\.ssh',  # SSH directory access
                r'/etc/',  # System config directory
                r'/root/', # Root directory
                r'C:\\Windows\\', # Windows system directory
                r'\x00',   # Null byte
            ]

            for pattern in suspicious_patterns:
                if re.search(pattern, normalized_path, re.IGNORECASE):
                    return False

            return True
        except Exception:
            return False

    def backup_tasks(self) -> Path:
        """Create a backup of the current tasks file."""
        # Validate path security for the original file
        if not self.validate_path_security(str(self.tasks_file)):
            raise ValueError(f"Invalid or unsafe file path: {self.tasks_file}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"tasks_backup_{timestamp}.json"

        # Validate path security for the backup file
        if not self.validate_path_security(str(backup_file)):
            raise ValueError(f"Invalid or unsafe backup file path: {backup_file}")

        with open(self.tasks_file, 'r', encoding='utf-8') as src:
            with open(backup_file, 'w', encoding='utf-8') as dst:
                dst.write(src.read())

        self.logger.info(f"Backup created: {backup_file}")
        return backup_file

    def load_tasks(self) -> Dict:
        """Load tasks from the JSON file with error handling."""
        # Validate path security first
        if not self.validate_path_security(str(self.tasks_file)):
            raise ValueError(f"Invalid or unsafe file path: {self.tasks_file}")

        try:
            # Check file size before loading to prevent memory issues
            max_file_size = 50 * 1024 * 1024  # 50 MB limit
            file_size = os.path.getsize(self.tasks_file)
            if file_size > max_file_size:
                raise ValueError(f"File size {file_size} bytes exceeds maximum allowed size of {max_file_size} bytes")

            # Read file in chunks to prevent memory issues with very large files
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                content = f.read(max_file_size)  # Limit read to max file size

            # Check if we read the entire file
            if len(content) == max_file_size:
                # Check if there's more content in the file
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    f.seek(max_file_size)
                    remaining = f.read(1)
                    if remaining:
                        raise ValueError(f"File size exceeds maximum allowed size of {max_file_size} bytes")

            # Parse JSON with size validation
            data = json.loads(content)
            return data
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON Decode Error: {e}")
            raise
        except FileNotFoundError:
            self.logger.error(f"File not found: {self.tasks_file}")
            raise
        except ValueError as e:
            self.logger.error(f"File size validation error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error reading file: {e}")
            raise

    def load_tasks_with_timeout(self, timeout: int = 30) -> Dict:
        """Load tasks from the JSON file with timeout protection.

        For cross-platform compatibility, this method uses file size limits
        and basic validation rather than signal-based timeouts.
        """
        # Check file size first to prevent loading huge files
        max_file_size = 50 * 1024 * 1024  # 50 MB limit
        file_size = os.path.getsize(self.tasks_file)
        if file_size > max_file_size:
            raise ValueError(f"File size {file_size} bytes exceeds maximum allowed size of {max_file_size} bytes")

        # Additional validation could be added here if needed
        return self.load_tasks()

    def save_tasks(self, data: Dict) -> None:
        """Save tasks back to the JSON file."""
        # Validate path security first
        if not self.validate_path_security(str(self.tasks_file)):
            raise ValueError(f"Invalid or unsafe file path: {self.tasks_file}")

        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def extract_tasks(self, data: Dict) -> List[Dict]:
        """Extract tasks from the nested structure."""
        if 'master' in data and 'tasks' in data['master']:
            return data['master']['tasks']
        else:
            return data.get('tasks', [])

    def collect_all_task_ids(self, tasks: List[Dict]) -> Tuple[Set, Dict, List]:
        """Collect all task IDs and build lookup dictionary."""
        all_ids = set()
        all_ids_list = []  # Keep original list to detect duplicates
        lookup = {}

        for task in tasks:
            task_id = task.get('id')
            if task_id is not None:
                task_id_str = str(task_id)
                all_ids.add(task_id_str)
                all_ids_list.append(task_id_str)
                lookup[task_id_str] = task

                # Process subtasks
                if 'subtasks' in task:
                    for subtask in task['subtasks']:
                        subtask_id = subtask.get('id')
                        if subtask_id is not None:
                            full_subtask_id = f"{task_id_str}.{subtask_id}"
                            all_ids.add(full_subtask_id)
                            all_ids_list.append(full_subtask_id)
                            lookup[full_subtask_id] = subtask

        return all_ids, lookup, all_ids_list

    def validate_json_structure(self, data: Dict) -> bool:
        """Validate basic JSON structure."""
        try:
            json.dumps(data)  # This will raise an exception if the structure is invalid
            return True
        except (TypeError, ValueError) as e:
            self.errors.append(f"Invalid JSON structure: {e}")
            return False

    def validate_duplicate_ids(self, all_ids_list: List[str]) -> bool:
        """Check for duplicate IDs."""
        original_count = len(all_ids_list)
        unique_count = len(set(all_ids_list))

        if original_count != unique_count:
            # Find actual duplicates
            seen = set()
            duplicates = []
            for item in all_ids_list:
                if item in seen and item not in duplicates:
                    duplicates.append(item)
                seen.add(item)

            self.errors.append(f"Duplicate IDs found: {duplicates}")
            return False
        return True

    def validate_task_structure(self, task: Dict, task_id: str, is_subtask: bool = False) -> None:
        """Validate individual task structure."""
        prefix = "Subtask" if is_subtask else "Task"
        
        # Check required fields
        if 'id' not in task:
            self.errors.append(f"{prefix} {task_id} missing 'id' field")
        
        if 'title' not in task:
            self.errors.append(f"{prefix} {task_id} missing 'title' field")
        
        if 'status' not in task:
            self.errors.append(f"{prefix} {task_id} missing 'status' field")
        elif task['status'] not in ['pending', 'in-progress', 'done', 'deferred', 'cancelled', 'review']:
            self.warnings.append(f"{prefix} {task_id} has invalid status: {task['status']}")

    def validate_dependencies(self, task: Dict, task_id: str, all_ids: Set[str], is_subtask: bool = False) -> None:
        """Validate task dependencies."""
        prefix = "Subtask" if is_subtask else "Task"
        dependencies = task.get('dependencies', [])
        
        for dep in dependencies:
            dep_str = str(dep)
            
            # Check if dependency exists in the task list
            if dep_str not in all_ids:
                # Check if it's a relative dependency within the same parent
                if '.' in dep_str and task_id and dep_str.startswith(f"{task_id}."):
                    continue  # This might be a valid relative dependency
                self.errors.append(f"{prefix} {task_id} has invalid dependency: {dep_str}")

    def build_dependency_graph(self, tasks: List[Dict], all_ids: Set[str]) -> None:
        """Build dependency graph for cycle detection."""
        self.dependency_graph.clear()
        self.reverse_graph.clear()

        for task in tasks:
            task_id = str(task.get('id'))
            
            # Process task dependencies
            deps = task.get('dependencies', [])
            for dep in deps:
                dep_str = str(dep)
                if dep_str in all_ids:
                    self.dependency_graph[task_id].append(dep_str)
                    self.reverse_graph[dep_str].append(task_id)

            # Process subtask dependencies
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    subtask_id = subtask.get('id')
                    if subtask_id is not None:
                        full_subtask_id = f"{task_id}.{subtask_id}"
                        
                        subtask_deps = subtask.get('dependencies', [])
                        for dep in subtask_deps:
                            dep_str = str(dep)
                            if dep_str in all_ids:
                                self.dependency_graph[full_subtask_id].append(dep_str)
                                self.reverse_graph[dep_str].append(full_subtask_id)

    def detect_circular_dependencies(self) -> bool:
        """Detect circular dependencies using Kahn's algorithm."""
        all_nodes = set(self.dependency_graph.keys()) | set(self.reverse_graph.keys())
        in_degree = defaultdict(int)

        # Calculate in-degrees
        for node in all_nodes:
            in_degree[node] = len(self.reverse_graph[node])

        # Find nodes with no incoming edges
        queue = deque([node for node in all_nodes if in_degree[node] == 0])
        visited = set()

        while queue:
            current = queue.popleft()
            visited.add(current)

            # Process all nodes that depend on current
            for dependent in self.dependency_graph[current]:
                if dependent in in_degree:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        # Check if all nodes were visited (no cycles)
        unvisited = all_nodes - visited
        if unvisited:
            self.errors.append(f"Circular dependencies detected! Unvisited nodes: {unvisited}")
            return False
        return True

    def validate_orphaned_subtasks(self, tasks: List[Dict]) -> None:
        """Detect orphaned subtasks (subtasks without proper parent task)."""
        for task in tasks:
            task_id = str(task.get('id'))
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    subtask_id = subtask.get('id')
                    if subtask_id is not None:
                        full_subtask_id = f"{task_id}.{subtask_id}"
                        # Verify the subtask exists in our lookup
                        if full_subtask_id not in self.task_lookup:
                            self.errors.append(f"Orphaned subtask reference: {full_subtask_id}")

    def validate_priority_consistency(self, tasks: List[Dict]) -> None:
        """Validate priority field consistency."""
        for task in tasks:
            if 'priority' in task:
                priority = task['priority']
                if priority not in ['low', 'medium', 'high']:
                    self.warnings.append(f"Task {task.get('id')} has invalid priority: {priority}")

    def fix_duplicate_ids(self, data: Dict) -> int:
        """Fix duplicate IDs by adding suffixes."""
        tasks = self.extract_tasks(data)
        id_counter = defaultdict(int)
        fixed_count = 0

        # First pass: identify duplicates
        all_ids = []
        for task in tasks:
            task_id = str(task.get('id'))
            all_ids.append((task, task_id, False))  # (task_obj, id, is_subtask)
            
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    subtask_id = str(subtask.get('id'))
                    all_ids.append((subtask, f"{task_id}.{subtask_id}", True))

        # Second pass: fix duplicates
        used_ids = set()
        for task_obj, original_id, is_subtask in all_ids:
            current_id = original_id
            counter = 1
            
            while current_id in used_ids:
                if is_subtask:
                    # For subtasks, modify the subtask ID part
                    parts = original_id.split('.')
                    if len(parts) == 2:
                        base_task_id, subtask_part = parts
                        current_id = f"{base_task_id}.{subtask_part}_{counter}"
                        counter += 1
                else:
                    # For main tasks, add suffix
                    current_id = f"{original_id}_{counter}"
                    counter += 1

            if current_id != original_id:
                task_obj['id'] = current_id.split('.')[-1] if is_subtask else current_id
                self.fixes_applied.append(f"Fixed duplicate ID: {original_id} -> {current_id}")
                fixed_count += 1
            
            used_ids.add(current_id)

        return fixed_count

    def fix_invalid_dependencies(self, data: Dict) -> int:
        """Fix invalid dependencies by removing them or converting relative references."""
        tasks = self.extract_tasks(data)
        fixed_count = 0

        for task in tasks:
            task_id = str(task.get('id'))
            
            # Fix task dependencies
            if 'dependencies' in task:
                original_deps = task['dependencies'][:]
                new_deps = []
                
                for dep in original_deps:
                    dep_str = str(dep)
                    if dep_str in self.all_task_ids:
                        new_deps.append(dep)
                    else:
                        self.fixes_applied.append(f"Removed invalid dependency {dep} from task {task_id}")
                        fixed_count += 1
                
                if new_deps != original_deps:
                    task['dependencies'] = new_deps

            # Fix subtask dependencies
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    subtask_id = str(subtask.get('id'))
                    full_subtask_id = f"{task_id}.{subtask_id}"
                    
                    if 'dependencies' in subtask:
                        original_deps = subtask['dependencies'][:]
                        new_deps = []
                        
                        for dep in original_deps:
                            dep_str = str(dep)
                            if dep_str in self.all_task_ids:
                                new_deps.append(dep)
                            elif '.' in dep_str and dep_str.startswith(f"{task_id}."):
                                # This might be a valid relative dependency
                                new_deps.append(dep)
                            else:
                                self.fixes_applied.append(f"Removed invalid dependency {dep} from subtask {full_subtask_id}")
                                fixed_count += 1
                        
                        if new_deps != original_deps:
                            subtask['dependencies'] = new_deps

        return fixed_count

    def fix_missing_fields(self, data: Dict) -> int:
        """Fix missing required fields with default values."""
        tasks = self.extract_tasks(data)
        fixed_count = 0

        for task in tasks:
            task_id = str(task.get('id'))

            # Add missing id
            if 'id' not in task:
                # Find next available ID that doesn't conflict
                existing_ids = {str(t.get('id')) for t in tasks if 'id' in t}
                new_id = 1
                while str(new_id) in existing_ids:
                    new_id += 1
                task['id'] = new_id
                self.fixes_applied.append(f"Added missing ID to task: {task['id']}")
                fixed_count += 1
            
            # Add missing title
            if 'title' not in task:
                task['title'] = f"Untitled Task {task.get('id')}"
                self.fixes_applied.append(f"Added missing title to task {task.get('id')}")
                fixed_count += 1
            
            # Add missing status
            if 'status' not in task:
                task['status'] = 'pending'
                self.fixes_applied.append(f"Added default status 'pending' to task {task.get('id')}")
                fixed_count += 1
            
            # Process subtasks
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    subtask_id = str(subtask.get('id'))

                    if 'id' not in subtask:
                        # Find next available subtask ID that doesn't conflict
                        existing_subtask_ids = {str(st.get('id')) for st in task['subtasks'] if 'id' in st}
                        new_subtask_id = 1
                        while str(new_subtask_id) in existing_subtask_ids:
                            new_subtask_id += 1
                        subtask['id'] = new_subtask_id
                        self.fixes_applied.append(f"Added missing ID to subtask in task {task_id}")
                        fixed_count += 1
                    
                    if 'title' not in subtask:
                        subtask['title'] = f"Untitled Subtask {subtask.get('id')} in task {task_id}"
                        self.fixes_applied.append(f"Added missing title to subtask {subtask.get('id')} in task {task_id}")
                        fixed_count += 1
                    
                    if 'status' not in subtask:
                        subtask['status'] = 'pending'
                        self.fixes_applied.append(f"Added default status 'pending' to subtask {subtask.get('id')} in task {task_id}")
                        fixed_count += 1

        return fixed_count

    def fix_priority_weaknesses(self, data: Dict) -> int:
        """Fix priority weaknesses by setting default priorities."""
        tasks = self.extract_tasks(data)
        fixed_count = 0

        for task in tasks:
            if 'priority' not in task or task['priority'] not in ['low', 'medium', 'high']:
                task['priority'] = 'medium'  # Default priority
                self.fixes_applied.append(f"Set default priority 'medium' to task {task.get('id')}")
                fixed_count += 1
            
            # Process subtasks
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    if 'priority' not in subtask or subtask['priority'] not in ['low', 'medium', 'high']:
                        subtask['priority'] = 'medium'  # Default priority
                        self.fixes_applied.append(f"Set default priority 'medium' to subtask {subtask.get('id')}")
                        fixed_count += 1

        return fixed_count

    def validate_and_fix(self, fix_issues: bool = True, create_backup: bool = True) -> bool:
        """
        Main validation and fixing method.

        Args:
            fix_issues: Whether to automatically fix detected issues
            create_backup: Whether to create a backup before fixing

        Returns:
            True if validation passes (or passes after fixing), False otherwise
        """
        self.errors = []
        self.warnings = []
        self.fixes_applied = []

        try:
            # Load the tasks file
            data = self.load_tasks()
            
            # Create backup if requested
            backup_file = None
            if fix_issues and create_backup:
                backup_file = self.backup_tasks()

            # Extract tasks
            tasks = self.extract_tasks(data)

            # Validate JSON structure
            if not self.validate_json_structure(data):
                if fix_issues:
                    self.logger.error("Cannot fix invalid JSON structure. Please correct manually.")
                    return False

            # Collect all task IDs
            self.all_task_ids, self.task_lookup, all_ids_list = self.collect_all_task_ids(tasks)

            # Validate for duplicates
            self.validate_duplicate_ids(all_ids_list)

            # Build dependency graph
            self.build_dependency_graph(tasks, self.all_task_ids)

            # Validate each task and subtask
            for task in tasks:
                task_id = str(task.get('id'))
                
                # Validate task structure
                self.validate_task_structure(task, task_id)
                
                # Validate dependencies
                self.validate_dependencies(task, task_id, self.all_task_ids)
                
                # Validate subtasks
                if 'subtasks' in task:
                    for subtask in task['subtasks']:
                        subtask_id = subtask.get('id')
                        full_subtask_id = f"{task_id}.{subtask_id}" if subtask_id is not None else task_id
                        
                        self.validate_task_structure(subtask, full_subtask_id, is_subtask=True)
                        self.validate_dependencies(subtask, full_subtask_id, self.all_task_ids, is_subtask=True)

            # Detect circular dependencies
            self.detect_circular_dependencies()

            # Validate orphaned subtasks
            self.validate_orphaned_subtasks(tasks)

            # Validate priority consistency
            self.validate_priority_consistency(tasks)

            # Print results before fixing
            if fix_issues and (self.errors or self.warnings):
                self.print_results()

            # Apply fixes if requested
            if fix_issues and (self.errors or self.warnings):
                fixed_duplicate_ids = 0
                fixed_invalid_deps = 0
                fixed_missing_fields = 0
                fixed_priority = 0

                if any("Duplicate" in error for error in self.errors):
                    fixed_duplicate_ids = self.fix_duplicate_ids(data)
                    # Recalculate IDs after fixing duplicates
                    self.all_task_ids, self.task_lookup, _ = self.collect_all_task_ids(self.extract_tasks(data))

                if any("invalid dependency" in error for error in self.errors):
                    fixed_invalid_deps = self.fix_invalid_dependencies(data)

                if any("missing" in error for error in self.errors):
                    fixed_missing_fields = self.fix_missing_fields(data)
                    # Recalculate IDs after adding missing IDs
                    self.all_task_ids, self.task_lookup, _ = self.collect_all_task_ids(self.extract_tasks(data))

                if any("priority" in warning for warning in self.warnings):
                    fixed_priority = self.fix_priority_weaknesses(data)

                # Save the fixed data
                self.save_tasks(data)

                # Log fixes applied
                total_fixed = fixed_duplicate_ids + fixed_invalid_deps + fixed_missing_fields + fixed_priority
                if total_fixed > 0:
                    self.logger.info(f"Applied {total_fixed} fixes:")
                    for fix in self.fixes_applied[-10:]:  # Show last 10 fixes
                        self.logger.info(f"  - {fix}")
                    if len(self.fixes_applied) > 10:
                        self.logger.info(f"  ... and {len(self.fixes_applied) - 10} more fixes")

                # Re-validate after fixes to see if all issues are resolved
                # Reload the fixed data for validation
                data_after_fix = self.load_tasks()
                tasks_after_fix = self.extract_tasks(data_after_fix)
                all_ids_after_fix, lookup_after_fix, all_ids_list_after_fix = self.collect_all_task_ids(tasks_after_fix)

                # Re-initialize for validation
                self.errors = []
                self.warnings = []

                # Re-validate the fixed data
                self.validate_duplicate_ids(all_ids_list_after_fix)
                self.build_dependency_graph(tasks_after_fix, all_ids_after_fix)

                for task in tasks_after_fix:
                    task_id = str(task.get('id'))
                    self.validate_task_structure(task, task_id)
                    self.validate_dependencies(task, task_id, all_ids_after_fix)

                    if 'subtasks' in task:
                        for subtask in task['subtasks']:
                            subtask_id = subtask.get('id')
                            full_subtask_id = f"{task_id}.{subtask_id}" if subtask_id is not None else task_id
                            self.validate_task_structure(subtask, full_subtask_id, is_subtask=True)
                            self.validate_dependencies(subtask, full_subtask_id, all_ids_after_fix, is_subtask=True)

                self.detect_circular_dependencies()
                self.validate_orphaned_subtasks(tasks_after_fix)
                self.validate_priority_consistency(tasks_after_fix)

            # Print results
            self.print_results()

            # Return True if no errors remain (or if we fixed them)
            if fix_issues:
                # Return result based on validation after fixes
                return len(self.errors) == 0
            else:
                return len(self.errors) == 0

        except Exception as e:
            self.logger.error(f"Error during validation: {e}")
            return False

    def print_results(self) -> None:
        """Print validation results."""
        print(f"\nValidation Results:")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Fixes Applied: {len(self.fixes_applied)}")

        if self.errors:
            print("\n❌ Errors found:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        if self.warnings:
            print("\n⚠️  Warnings found:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        if self.fixes_applied:
            print(f"\n🔧 Fixes applied:")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"  {i}. {fix}")

    def cleanup_backups(self, keep_last_n: int = 5) -> int:
        """
        Clean up old backup files, keeping only the most recent N backups.

        Args:
            keep_last_n: Number of recent backups to keep

        Returns:
            Number of files deleted
        """
        backup_files = list(self.backup_dir.glob("tasks_backup_*.json"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        files_to_delete = backup_files[keep_last_n:]
        deleted_count = 0
        
        for file in files_to_delete:
            try:
                file.unlink()
                deleted_count += 1
                self.logger.info(f"Deleted old backup: {file}")
            except Exception as e:
                self.logger.error(f"Failed to delete backup {file}: {e}")
        
        if deleted_count > 0:
            self.logger.info(f"Cleaned up {deleted_count} old backup files")
        
        return deleted_count

    def get_statistics(self, data: Optional[Dict] = None) -> Dict:
        """Get statistics about the tasks file."""
        if data is None:
            data = self.load_tasks()
        
        tasks = self.extract_tasks(data)
        
        stats = {
            'total_tasks': len(tasks),
            'total_subtasks': 0,
            'statuses': defaultdict(int),
            'priorities': defaultdict(int),
            'dependencies_count': 0,
            'tasks_with_subtasks': 0
        }
        
        for task in tasks:
            # Count subtasks
            if 'subtasks' in task:
                stats['total_subtasks'] += len(task['subtasks'])
                stats['tasks_with_subtasks'] += 1
                
                for subtask in task['subtasks']:
                    if 'status' in subtask:
                        stats['statuses'][subtask['status']] += 1
                    if 'priority' in subtask:
                        stats['priorities'][subtask['priority']] += 1
                    if 'dependencies' in subtask:
                        stats['dependencies_count'] += len(subtask['dependencies'])
            
            # Count main task stats
            if 'status' in task:
                stats['statuses'][task['status']] += 1
            if 'priority' in task:
                stats['priorities'][task['priority']] += 1
            if 'dependencies' in task:
                stats['dependencies_count'] += len(task['dependencies'])
        
        return dict(stats)


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Validate and fix Task Master tasks.json files")
    parser.add_argument("--file", "-f", default="tasks/tasks.json", help="Path to tasks.json file")
    parser.add_argument("--validate", "-v", action="store_true", help="Validate only (no fixes)")
    parser.add_argument("--fix", "-x", action="store_true", help="Validate and fix issues")
    parser.add_argument("--backup", "-b", action="store_true", help="Create backup before fixing")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    parser.add_argument("--cleanup", "-c", action="store_true", help="Clean up old backup files")
    parser.add_argument("--stats", "-s", action="store_true", help="Show statistics only")
    parser.add_argument("--keep-backups", type=int, default=5, help="Number of backup files to keep (for cleanup)")
    
    args = parser.parse_args()

    # Validate path security before creating validator
    if not TaskValidatorFixer.validate_path_security(args.file):
        print(f"Error: Invalid or unsafe file path: {args.file}")
        sys.exit(1)

    validator = TaskValidatorFixer(args.file)

    if args.stats:
        try:
            data = validator.load_tasks()
            stats = validator.get_statistics(data)
            print("Tasks Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"Error getting statistics: {e}")
            sys.exit(1)
        return

    if args.cleanup:
        deleted = validator.cleanup_backups(args.keep_backups)
        print(f"Cleaned up {deleted} old backup files")
        return

    # Determine backup behavior
    create_backup = args.backup or (not args.no_backup and args.fix)
    
    if args.validate:
        success = validator.validate_and_fix(fix_issues=False, create_backup=False)
        sys.exit(0 if success else 1)
    elif args.fix:
        success = validator.validate_and_fix(fix_issues=True, create_backup=create_backup)
        sys.exit(0 if success else 1)
    else:
        # Default: validate only
        success = validator.validate_and_fix(fix_issues=False, create_backup=False)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()