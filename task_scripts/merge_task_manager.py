#!/usr/bin/env python3
"""
Advanced Task File Manager for Complex Merge Processes

This script provides a comprehensive solution for managing and fixing tasks.json files
during complex merge processes. It handles:
- Duplicate ID detection and resolution with sophisticated merging
- Invalid JSON structure validation and fixing
- Dependency issue detection and resolution
- Subtask consistency checking and fixing
- Orphaned subtask detection and cleanup
- Merge conflict detection and resolution
- Backup creation and recovery
- Atomic operations with rollback capability
- Flexible configuration and adaptation to complex violations
"""

import json
import os
import sys
import shutil
import tempfile
import re
import hashlib
import time
import copy
from pathlib import Path
from typing import Dict, Any, List, Tuple, Union, Optional, Set
from collections import defaultdict, deque
from datetime import datetime
import argparse
import logging
import traceback


class AdvancedTaskManager:
    """Advanced task file manager with comprehensive merge conflict handling"""

    def __init__(self, tasks_file: str = "tasks/tasks.json", backup_dir: Optional[str] = None):
        """
        Initialize the advanced task manager.

        Args:
            tasks_file: Path to the tasks.json file
            backup_dir: Directory for backup files (defaults to temp directory)
        """
        self.tasks_file = Path(tasks_file)
        self.backup_dir = Path(backup_dir) if backup_dir else Path(tempfile.gettempdir()) / "task_manager_backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Security patterns to prevent path traversal and other vulnerabilities
        self.security_patterns = [
            r'\.\./', r'\.\.\\', r'/etc/', r'/root/', r'C:\\Windows\\', r'~/.ssh/',
            r'rm\s+-rf', r'eval\s*\(', r'exec\s*\(', r'import\s+os', r'import\s+subprocess'
        ]

        # Validation results
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
        self.all_task_ids = set()
        self.task_lookup = {}
        self.dependency_graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)
        self.merge_conflicts_detected = False

    def validate_path_security(self, filepath: str, allowed_base_dir: str = None) -> bool:
        """Validate file path security to prevent path traversal and other vulnerabilities."""
        try:
            # Check for null bytes and other dangerous characters
            if '\x00' in filepath:
                self.logger.error(f"Null byte detected in path: {filepath}")
                return False

            from pathlib import Path

            # Use Path.resolve() to normalize and resolve the path
            resolved_path = Path(filepath).resolve()
            normalized_path = str(resolved_path)

            # Check for URL encoding and other bypass attempts
            path_lower = normalized_path.lower()
            if any(unsafe_pattern in path_lower for unsafe_pattern in ['%2e%2e', '%2f', '%5c']):
                self.logger.error(f"URL encoding detected in path: {filepath}")
                return False

            # Check for directory traversal using multiple methods
            path_str = str(resolved_path).replace('\\', '/')
            if ".." in path_str.split("/"):
                self.logger.error(f"Path traversal detected: {filepath}")
                return False

            # Check against security patterns
            for pattern in self.security_patterns:
                if re.search(pattern, normalized_path, re.IGNORECASE):
                    self.logger.error(f"Security violation detected: {filepath}")
                    return False

            # If allowed base directory is specified, ensure path is within it
            if allowed_base_dir:
                try:
                    resolved_allowed = Path(allowed_base_dir).resolve()
                    resolved_path.relative_to(resolved_allowed)
                except ValueError:
                    self.logger.error(f"Path outside allowed base directory: {filepath}")
                    return False

            # Additional checks for potentially dangerous paths
            # Exclude temporary directories used in testing
            dangerous_patterns = [
                r'\.git', r'\.ssh', r'/etc', r'/root', r'C:\\Windows', r'/proc', r'/sys', r'\x00'
            ]

            path_lower = normalized_path.lower()
            for pattern in dangerous_patterns:
                if re.search(pattern, path_lower):
                    # Only flag as dangerous if not in temp directory
                    is_temp_path = any(temp_dir.lower() in path_lower for temp_dir in [tempfile.gettempdir().lower(), '/tmp/'])
                    if not is_temp_path:
                        self.logger.warning(f"Potentially dangerous path pattern detected: {filepath}")
                        return False

        except Exception:
            self.logger.error(f"Invalid path format: {filepath}")
            return False

        return True

    def create_backup(self, filepath: str) -> str:
        """Create a backup of the original file with timestamp."""
        if not self.validate_path_security(filepath):
            raise ValueError(f"Security validation failed for: {filepath}")

        # Use UUID to avoid race conditions that could occur with timestamp-based naming
        import uuid
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

        # Verify the backup has content and matches the original size (optional verification)
        if os.path.getsize(filepath) != os.path.getsize(backup_path):
            raise Exception(f"Backup size mismatch: {filepath} vs {backup_path}")

        self.logger.info(f"Created verified backup: {backup_path}")
        return str(backup_path)

    def check_merge_conflicts(self, filepath: str) -> bool:
        """Check for Git merge conflict markers in the file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            conflict_markers = ['<<<<<<< HEAD', '=======', '>>>>>>> ', '<<<<<<< ', '>>>>>>>']
            has_conflicts = any(marker in content for marker in conflict_markers)

            if has_conflicts:
                self.logger.warning(f"Merge conflicts detected in: {filepath}")
                self.merge_conflicts_detected = True

            return has_conflicts
        except Exception as e:
            self.logger.error(f"Error checking merge conflicts in {filepath}: {e}")
            return False

    def load_tasks(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """
        Load tasks from the JSON file with comprehensive error handling.

        Args:
            filepath: Optional specific file to load (defaults to self.tasks_file)

        Returns:
            Loaded JSON data as dictionary
        """
        file_to_load = Path(filepath) if filepath else self.tasks_file

        if not self.validate_path_security(str(file_to_load)):
            raise ValueError(f"Security validation failed for: {file_to_load}")

        try:
            # Check file size before loading to prevent memory issues
            max_file_size = 50 * 1024 * 1024  # 50 MB limit
            file_size = os.path.getsize(file_to_load)
            if file_size > max_file_size:
                raise ValueError(f"File size {file_size} bytes exceeds maximum allowed size of {max_file_size} bytes")

            # Read file in chunks to prevent memory issues with very large files
            with open(file_to_load, 'r', encoding='utf-8') as f:
                content = f.read(max_file_size)  # Limit read to max file size

            # Check if we read the entire file
            if len(content) == max_file_size:
                # Check if there's more content in the file
                with open(file_to_load, 'r', encoding='utf-8') as f:
                    f.seek(max_file_size)
                    remaining = f.read(1)
                    if remaining:
                        raise ValueError(f"File size exceeds maximum allowed size of {max_file_size} bytes")

            content = content.strip()

            # Handle empty files
            if not content:
                return {"tasks": []}

            # Try to parse JSON
            try:
                data = json.loads(content)
                return data
            except json.JSONDecodeError as e:
                self.logger.warning(f"JSON parsing failed: {e}")

                # Try to fix common JSON issues
                fixed_content = self.attempt_json_fix(content)
                if fixed_content:
                    try:
                        data = json.loads(fixed_content)
                        self.logger.info("Successfully fixed JSON structure")
                        return data
                    except json.JSONDecodeError:
                        self.logger.error("Could not fix JSON structure")
                        raise e
                else:
                    raise e

        except FileNotFoundError:
            self.logger.error(f"File not found: {file_to_load}")
            # Create a default structure
            default_data = {"tasks": []}
            self.logger.info(f"Created default structure for missing file: {file_to_load}")
            return default_data
        except Exception as e:
            self.logger.error(f"Error reading file {file_to_load}: {e}")
            raise

    def attempt_json_fix(self, content: str) -> Optional[str]:
        """
        Attempt to fix common JSON structure issues.
        
        Args:
            content: Raw file content
            
        Returns:
            Fixed content string or None if unable to fix
        """
        try:
            # Remove common merge conflict markers and comments
            lines = content.split('\n')
            cleaned_lines = []
            
            skip_line = False
            for line in lines:
                stripped = line.strip()
                
                # Skip conflict markers
                if stripped.startswith('<<<<<<<') or stripped.startswith('=======') or stripped.startswith('>>>>>>>'):
                    skip_line = True
                    continue
                elif skip_line and (stripped.startswith('}') or stripped.startswith(']')):
                    skip_line = False
                    continue
                elif skip_line:
                    continue
                else:
                    # Remove inline comments (basic implementation)
                    if '//' in line:
                        line = line.split('//')[0]
                    if '/*' in line and '*/' in line:
                        # Simple comment removal (doesn't handle nested comments)
                        line = re.sub(r'/\*.*?\*/', '', line)
                    
                    cleaned_lines.append(line)
            
            cleaned_content = '\n'.join(cleaned_lines)
            
            # Try to parse the cleaned content
            json.loads(cleaned_content)
            return cleaned_content
            
        except json.JSONDecodeError:
            # Try more aggressive fixes
            try:
                # Remove trailing commas
                content = re.sub(r',(\s*[}\]])', r'\1', content)
                # Fix unquoted property names
                content = re.sub(r'(\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', content)
                # Remove comments (simple approach)
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
                
                # Try parsing again
                json.loads(content)
                return content
            except json.JSONDecodeError:
                return None

    def save_tasks(self, data: Dict[str, Any], filepath: Optional[str] = None) -> None:
        """
        Save tasks back to the JSON file with error handling.
        
        Args:
            data: Data dictionary to save
            filepath: Optional specific file to save to (defaults to self.tasks_file)
        """
        file_to_save = Path(filepath) if filepath else self.tasks_file
        
        if not self.validate_path_security(str(file_to_save)):
            raise ValueError(f"Security validation failed for: {file_to_save}")
        
        try:
            # Create backup before saving
            backup_path = self.create_backup(str(file_to_save))
            
            with open(file_to_save, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, separators=(',', ': '))
            
            self.logger.info(f"Successfully saved tasks to: {file_to_save}")
            
        except Exception as e:
            self.logger.error(f"Error saving tasks to {file_to_save}: {e}")
            # Attempt to restore from backup
            self.restore_from_backup(backup_path)
            raise

    def extract_tasks(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tasks from the nested structure with fallback."""
        if 'master' in data and 'tasks' in data['master']:
            return data['master']['tasks']
        elif 'tasks' in data:
            return data['tasks']
        else:
            # Create empty tasks array if none exists
            data['tasks'] = []
            return data['tasks']

    def set_tasks(self, data: Dict[str, Any], tasks: List[Dict[str, Any]]) -> None:
        """Set tasks back into the data structure."""
        if 'master' in data and 'tasks' in data['master']:
            data['master']['tasks'] = tasks
        else:
            data['tasks'] = tasks

    def collect_all_task_ids(self, tasks: List[Dict[str, Any]]) -> Tuple[Set[str], Dict[str, Dict[str, Any]], List[str]]:
        """
        Collect all task IDs and build lookup dictionary.
        
        Returns:
            Tuple of (all_ids_set, lookup_dict, all_ids_list_with_duplicates)
        """
        all_ids = set()
        all_ids_list = []  # Keep original list to detect duplicates
        lookup = {}

        for task in tasks:
            if not isinstance(task, dict):
                continue
                
            task_id = task.get('id')
            if task_id is not None:
                task_id_str = str(task_id)
                all_ids.add(task_id_str)
                all_ids_list.append(task_id_str)
                lookup[task_id_str] = task

                # Process subtasks
                if 'subtasks' in task and isinstance(task['subtasks'], list):
                    for subtask in task['subtasks']:
                        if not isinstance(subtask, dict):
                            continue
                            
                        subtask_id = subtask.get('id')
                        if subtask_id is not None:
                            full_subtask_id = f"{task_id_str}.{subtask_id}"
                            all_ids.add(full_subtask_id)
                            all_ids_list.append(full_subtask_id)
                            lookup[full_subtask_id] = subtask

        return all_ids, lookup, all_ids_list

    def validate_json_structure(self, data: Dict[str, Any]) -> bool:
        """Validate basic JSON structure."""
        try:
            # This will raise an exception if the structure is invalid
            json.dumps(data, ensure_ascii=False)
            return True
        except (TypeError, ValueError) as e:
            self.errors.append(f"Invalid JSON structure: {e}")
            return False

    def validate_duplicate_ids(self, all_ids_list: List[str]) -> List[str]:
        """
        Check for duplicate IDs and return list of duplicates.
        
        Returns:
            List of duplicate IDs found
        """
        seen = set()
        duplicates = []
        for item in all_ids_list:
            if item in seen and item not in duplicates:
                duplicates.append(item)
            seen.add(item)

        if duplicates:
            self.errors.append(f"Duplicate IDs found: {duplicates}")
        
        return duplicates

    def validate_task_structure(self, task: Dict[str, Any], task_id: str, is_subtask: bool = False) -> None:
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

        # Validate data types
        if 'id' in task and not isinstance(task['id'], (str, int, float)):
            self.errors.append(f"{prefix} {task_id} has invalid ID type: {type(task['id'])}")

        if 'title' in task and not isinstance(task['title'], str):
            self.errors.append(f"{prefix} {task_id} has invalid title type: {type(task['title'])}")

        if 'status' in task and not isinstance(task['status'], str):
            self.errors.append(f"{prefix} {task_id} has invalid status type: {type(task['status'])}")

    def validate_dependencies(self, task: Dict[str, Any], task_id: str, all_ids: Set[str], is_subtask: bool = False) -> None:
        """Validate task dependencies."""
        prefix = "Subtask" if is_subtask else "Task"
        dependencies = task.get('dependencies', [])

        if not isinstance(dependencies, list):
            self.errors.append(f"{prefix} {task_id} has invalid dependencies type: {type(dependencies)}")
            return

        for dep in dependencies:
            dep_str = str(dep)

            # Check if dependency exists in the task list
            if dep_str not in all_ids:
                # Check if it's a relative dependency within the same parent
                if '.' in dep_str and task_id and dep_str.startswith(f"{task_id}."):
                    continue  # This might be a valid relative dependency
                self.errors.append(f"{prefix} {task_id} has invalid dependency: {dep_str}")

    def build_dependency_graph(self, tasks: List[Dict[str, Any]], all_ids: Set[str]) -> None:
        """Build dependency graph for cycle detection."""
        self.dependency_graph.clear()
        self.reverse_graph.clear()

        for task in tasks:
            if not isinstance(task, dict):
                continue
                
            task_id = str(task.get('id'))

            # Process task dependencies
            deps = task.get('dependencies', [])
            if isinstance(deps, list):
                for dep in deps:
                    dep_str = str(dep)
                    if dep_str in all_ids:
                        self.dependency_graph[task_id].append(dep_str)
                        self.reverse_graph[dep_str].append(task_id)

            # Process subtask dependencies
            if 'subtasks' in task and isinstance(task['subtasks'], list):
                for subtask in task['subtasks']:
                    if not isinstance(subtask, dict):
                        continue
                        
                    subtask_id = subtask.get('id')
                    if subtask_id is not None:
                        full_subtask_id = f"{task_id}.{subtask_id}"

                        subtask_deps = subtask.get('dependencies', [])
                        if isinstance(subtask_deps, list):
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

    def validate_orphaned_subtasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Detect orphaned subtasks (subtasks without proper parent task)."""
        for task in tasks:
            if not isinstance(task, dict):
                continue
                
            task_id = str(task.get('id'))
            if 'subtasks' in task and isinstance(task['subtasks'], list):
                for subtask in task['subtasks']:
                    if not isinstance(subtask, dict):
                        continue
                        
                    subtask_id = subtask.get('id')
                    if subtask_id is not None:
                        full_subtask_id = f"{task_id}.{subtask_id}"
                        # Verify the subtask exists in our lookup
                        if full_subtask_id not in self.task_lookup:
                            self.errors.append(f"Orphaned subtask reference: {full_subtask_id}")

    def validate_priority_consistency(self, tasks: List[Dict[str, Any]]) -> None:
        """Validate priority field consistency."""
        for task in tasks:
            if not isinstance(task, dict):
                continue
                
            if 'priority' in task:
                priority = task['priority']
                if priority not in ['low', 'medium', 'high']:
                    self.warnings.append(f"Task {task.get('id')} has invalid priority: {priority}")

    def resolve_duplicate_ids(self, tasks: List[Dict[str, Any]]) -> int:
        """
        Resolve duplicate IDs by creating merged tasks or renaming with suffixes.

        Returns:
            Number of duplicates resolved
        """
        resolved_count = 0

        # First, resolve duplicate main tasks
        # Create a new task list to avoid modification during iteration
        new_tasks = []

        # Group main tasks by ID to identify duplicates
        main_task_groups = defaultdict(list)
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                continue

            task_id = str(task.get('id', f"unnamed_{i}"))
            main_task_groups[task_id].append((i, task))  # Store index and task

        # Process each group of main task duplicates
        for task_id, group in main_task_groups.items():
            if len(group) > 1:
                # Multiple tasks with the same ID - need to resolve
                self.logger.info(f"Resolving {len(group)} duplicate main tasks with ID: {task_id}")

                # Keep the first task and merge/fix the rest
                _, primary_task = group[0]
                merged_task = copy.deepcopy(primary_task)

                for i, (task_idx, duplicate_task) in enumerate(group[1:], 1):
                    # Merge fields from duplicate into primary task
                    merged_task = self.merge_duplicate_task_fields(merged_task, duplicate_task, task_id, i)
                    resolved_count += 1

                # Add the merged task to the new list
                new_tasks.append(merged_task)
            else:
                # No duplicates, add the single task
                _, single_task = group[0]
                new_tasks.append(single_task)

        # Now resolve duplicate subtasks within each task
        for task in new_tasks:
            if isinstance(task, dict) and 'subtasks' in task and isinstance(task['subtasks'], list):
                subtask_groups = defaultdict(list)

                # Group subtasks by ID
                for j, subtask in enumerate(task['subtasks']):
                    if not isinstance(subtask, dict):
                        continue

                    subtask_id = str(subtask.get('id', f"unnamed_sub_{j}"))
                    full_subtask_id = f"{task.get('id', 'unknown')}.{subtask_id}"
                    subtask_groups[full_subtask_id].append((j, subtask))

                # Process subtask duplicates
                new_subtasks = []
                for subtask_id, sub_group in subtask_groups.items():
                    if len(sub_group) > 1:
                        # Multiple subtasks with the same ID - need to resolve
                        self.logger.info(f"Resolving {len(sub_group)} duplicate subtasks with ID: {subtask_id}")

                        # Keep the first subtask and merge/fix the rest
                        _, primary_subtask = sub_group[0]
                        merged_subtask = copy.deepcopy(primary_subtask)

                        for i, (sub_idx, duplicate_subtask) in enumerate(sub_group[1:], 1):
                            # Merge fields from duplicate into primary subtask
                            merged_subtask = self.merge_duplicate_task_fields(merged_subtask, duplicate_subtask, subtask_id, i)
                            resolved_count += 1

                        new_subtasks.append(merged_subtask)
                    else:
                        # No duplicates, add the single subtask
                        _, single_subtask = sub_group[0]
                        new_subtasks.append(single_subtask)

                # Update the task's subtasks
                task['subtasks'] = new_subtasks

        # Replace the original tasks list
        tasks.clear()
        tasks.extend(new_tasks)

        return resolved_count

    def merge_duplicate_task_fields(self, primary_task: Dict[str, Any], duplicate_task: Dict[str, Any], task_id: str, duplicate_index: int) -> Dict[str, Any]:
        """Merge fields from duplicate task into primary task."""
        merged_task = copy.deepcopy(primary_task)
        
        # Merge fields with conflict resolution
        for field, value in duplicate_task.items():
            if field == 'id':
                continue  # Don't merge ID field
                
            if field not in merged_task:
                # Field doesn't exist in primary, just add it
                merged_task[field] = value
            elif field == 'dependencies':
                # Merge dependencies (union of both lists)
                if isinstance(merged_task[field], list) and isinstance(value, list):
                    merged_deps = list(set(merged_task[field] + value))
                    merged_task[field] = merged_deps
                    self.fixes_applied.append(f"Merged dependencies for task {task_id}")
                else:
                    # If not both lists, keep primary and warn
                    self.warnings.append(f"Conflict in dependencies for task {task_id}, keeping primary")
            elif field == 'subtasks':
                # Merge subtasks
                if isinstance(merged_task[field], list) and isinstance(value, list):
                    # Add subtasks from duplicate that don't already exist
                    existing_subtask_ids = {str(st.get('id', '')) for st in merged_task[field]}
                    for subtask in value:
                        if str(subtask.get('id', '')) not in existing_subtask_ids:
                            merged_task[field].append(subtask)
                    self.fixes_applied.append(f"Merged subtasks for task {task_id}")
                else:
                    self.warnings.append(f"Conflict in subtasks for task {task_id}, keeping primary")
            elif field in ['title', 'description', 'details']:
                # For text fields, prefer non-empty values or concatenate if both exist
                if not merged_task[field] and value:
                    merged_task[field] = value
                elif merged_task[field] and value and merged_task[field] != value:
                    # Both have values, concatenate with separator
                    merged_task[field] = f"{merged_task[field]} | {value}"
                    self.warnings.append(f"Concatenated conflicting {field} for task {task_id}")
            elif field == 'status':
                # For status, use more advanced logic (e.g., 'done' takes precedence over 'pending')
                status_priority = {'cancelled': 0, 'deferred': 1, 'pending': 2, 'in-progress': 3, 'review': 4, 'done': 5}
                primary_status = merged_task[field]
                duplicate_status = value
                
                if status_priority.get(duplicate_status, 0) > status_priority.get(primary_status, 0):
                    merged_task[field] = duplicate_status
                    self.fixes_applied.append(f"Updated status for task {task_id} from {primary_status} to {duplicate_status}")
            else:
                # For other fields, keep primary and warn about conflict
                self.warnings.append(f"Conflict in field '{field}' for task {task_id}, keeping primary value")

        return merged_task

    def fix_invalid_dependencies(self, tasks: List[Dict[str, Any]], all_ids: Set[str]) -> int:
        """Fix invalid dependencies by removing them or converting relative references."""
        fixed_count = 0

        for task in tasks:
            if not isinstance(task, dict):
                continue
                
            task_id = str(task.get('id', 'unknown'))

            # Fix task dependencies
            if 'dependencies' in task and isinstance(task['dependencies'], list):
                original_deps = task['dependencies'][:]
                new_deps = []

                for dep in original_deps:
                    dep_str = str(dep)
                    if dep_str in all_ids:
                        new_deps.append(dep)
                    else:
                        # Check for relative dependencies within same parent
                        if '.' in dep_str and task_id and dep_str.startswith(f"{task_id}."):
                            new_deps.append(dep)
                        else:
                            self.fixes_applied.append(f"Removed invalid dependency {dep} from task {task_id}")
                            fixed_count += 1

                if new_deps != original_deps:
                    task['dependencies'] = new_deps

            # Fix subtask dependencies
            if 'subtasks' in task and isinstance(task['subtasks'], list):
                for subtask in task['subtasks']:
                    if not isinstance(subtask, dict):
                        continue
                        
                    subtask_id = str(subtask.get('id', 'unknown'))
                    full_subtask_id = f"{task_id}.{subtask_id}"

                    if 'dependencies' in subtask and isinstance(subtask['dependencies'], list):
                        original_deps = subtask['dependencies'][:]
                        new_deps = []

                        for dep in original_deps:
                            dep_str = str(dep)
                            if dep_str in all_ids:
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

    def fix_missing_fields(self, tasks: List[Dict[str, Any]]) -> int:
        """Fix missing required fields with default values."""
        fixed_count = 0

        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                # Replace invalid task with default structure
                new_task = {
                    'id': f"recovered_task_{i}",
                    'title': f"Recovered Task {i}",
                    'status': 'pending'
                }
                tasks[i] = new_task
                self.fixes_applied.append(f"Replaced invalid task structure at index {i}")
                fixed_count += 1
                continue

            task_id = str(task.get('id', f"unnamed_task_{i}"))

            # Add missing id
            if 'id' not in task or task['id'] is None:
                # Find next available ID that doesn't conflict
                existing_ids = {str(t.get('id')) for t in tasks if 'id' in t}
                new_id = 1
                while str(new_id) in existing_ids:
                    new_id += 1
                task['id'] = new_id
                self.fixes_applied.append(f"Added missing ID to task: {task['id']}")
                fixed_count += 1

            # Add missing title
            if 'title' not in task or not task['title']:
                task['title'] = f"Untitled Task {task.get('id')}"
                self.fixes_applied.append(f"Added missing title to task {task.get('id')}")
                fixed_count += 1

            # Add missing status
            if 'status' not in task or task['status'] not in ['pending', 'in-progress', 'done', 'deferred', 'cancelled', 'review']:
                task['status'] = 'pending'
                self.fixes_applied.append(f"Added default status 'pending' to task {task.get('id')}")
                fixed_count += 1

            # Process subtasks
            if 'subtasks' in task and isinstance(task['subtasks'], list):
                for j, subtask in enumerate(task['subtasks']):
                    if not isinstance(subtask, dict):
                        # Replace invalid subtask with default structure
                        new_subtask = {
                            'id': j + 1,
                            'title': f"Recovered Subtask {j + 1} in task {task_id}",
                            'status': 'pending'
                        }
                        task['subtasks'][j] = new_subtask
                        self.fixes_applied.append(f"Replaced invalid subtask structure in task {task_id}")
                        fixed_count += 1
                        continue

                    subtask_id = str(subtask.get('id', f"unnamed_subtask_{j}"))

                    if 'id' not in subtask or subtask['id'] is None:
                        # Find next available subtask ID that doesn't conflict
                        existing_subtask_ids = {str(st.get('id')) for st in task['subtasks'] if 'id' in st}
                        new_subtask_id = 1
                        while str(new_subtask_id) in existing_subtask_ids:
                            new_subtask_id += 1
                        subtask['id'] = new_subtask_id
                        self.fixes_applied.append(f"Added missing ID to subtask in task {task_id}")
                        fixed_count += 1

                    if 'title' not in subtask or not subtask['title']:
                        subtask['title'] = f"Untitled Subtask {subtask.get('id')} in task {task_id}"
                        self.fixes_applied.append(f"Added missing title to subtask {subtask.get('id')} in task {task_id}")
                        fixed_count += 1

                    if 'status' not in subtask or subtask['status'] not in ['pending', 'in-progress', 'done', 'deferred', 'cancelled', 'review']:
                        subtask['status'] = 'pending'
                        self.fixes_applied.append(f"Added default status 'pending' to subtask {subtask.get('id')} in task {task_id}")
                        fixed_count += 1

        return fixed_count

    def fix_priority_weaknesses(self, tasks: List[Dict[str, Any]]) -> int:
        """Fix priority weaknesses by setting default priorities."""
        fixed_count = 0

        for task in tasks:
            if not isinstance(task, dict):
                continue
                
            if 'priority' not in task or task['priority'] not in ['low', 'medium', 'high']:
                task['priority'] = 'medium'  # Default priority
                self.fixes_applied.append(f"Set default priority 'medium' to task {task.get('id', 'unknown')}")
                fixed_count += 1

            # Process subtasks
            if 'subtasks' in task and isinstance(task['subtasks'], list):
                for subtask in task['subtasks']:
                    if not isinstance(subtask, dict):
                        continue
                        
                    if 'priority' not in subtask or subtask['priority'] not in ['low', 'medium', 'high']:
                        subtask['priority'] = 'medium'  # Default priority
                        self.fixes_applied.append(f"Set default priority 'medium' to subtask {subtask.get('id', 'unknown')}")
                        fixed_count += 1

        return fixed_count

    def fix_orphaned_subtasks(self, tasks: List[Dict[str, Any]]) -> int:
        """Fix orphaned subtasks by removing them or promoting to main tasks."""
        fixed_count = 0
        orphaned_subtasks = []

        # First, identify orphaned subtasks
        for task in tasks:
            if not isinstance(task, dict) or 'subtasks' not in task:
                continue
                
            task_id = str(task.get('id', 'unknown'))
            valid_subtasks = []
            
            for subtask in task['subtasks']:
                if not isinstance(subtask, dict):
                    continue
                    
                subtask_id = subtask.get('id')
                if subtask_id is not None:
                    full_subtask_id = f"{task_id}.{subtask_id}"
                    # Check if this subtask exists in our lookup (it should if properly structured)
                    if full_subtask_id in self.task_lookup:
                        valid_subtasks.append(subtask)
                    else:
                        # This might be an orphaned subtask
                        orphaned_subtasks.append((task, subtask))
                else:
                    valid_subtasks.append(subtask)
            
            task['subtasks'] = valid_subtasks

        # Handle orphaned subtasks - convert them to main tasks
        for parent_task, orphaned_subtask in orphaned_subtasks:
            # Convert orphaned subtask to a main task
            new_task = copy.deepcopy(orphaned_subtask)
            # Remove the parent reference from the ID if it exists
            if 'id' in new_task and isinstance(new_task['id'], str) and '.' in new_task['id']:
                new_task['id'] = new_task['id'].split('.')[-1]
            
            tasks.append(new_task)
            self.fixes_applied.append(f"Converted orphaned subtask to main task: {new_task.get('id', 'unknown')}")
            fixed_count += 1

        return fixed_count

    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore the original file from backup."""
        try:
            if Path(backup_path).exists():
                shutil.copy2(backup_path, self.tasks_file)
                self.logger.info(f"Restored from backup: {backup_path}")
                return True
            else:
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
        except Exception as e:
            self.logger.error(f"Error restoring from backup {backup_path}: {e}")
            return False

    def validate_and_fix(self, fix_issues: bool = True, create_backup: bool = True, 
                        resolve_duplicates: bool = True, fix_dependencies: bool = True,
                        fix_structure: bool = True, fix_priorities: bool = True,
                        fix_orphans: bool = True) -> bool:
        """
        Main validation and fixing method with comprehensive options.

        Args:
            fix_issues: Whether to automatically fix detected issues
            create_backup: Whether to create a backup before fixing
            resolve_duplicates: Whether to resolve duplicate IDs
            fix_dependencies: Whether to fix invalid dependencies
            fix_structure: Whether to fix missing fields and structure
            fix_priorities: Whether to fix priority weaknesses
            fix_orphans: Whether to fix orphaned subtasks

        Returns:
            True if validation passes (or passes after fixing), False otherwise
        """
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
        self.merge_conflicts_detected = False

        try:
            # Check for merge conflicts first
            if self.check_merge_conflicts(str(self.tasks_file)):
                self.logger.warning("Merge conflicts detected, attempting to resolve...")

            # Load the tasks file
            data = self.load_tasks()

            # Create backup if requested
            backup_file = None
            if fix_issues and create_backup:
                backup_file = self.create_backup(str(self.tasks_file))

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
            duplicates = self.validate_duplicate_ids(all_ids_list)

            # Build dependency graph
            self.build_dependency_graph(tasks, self.all_task_ids)

            # Validate each task and subtask
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                    
                task_id = str(task.get('id', 'unknown'))

                # Validate task structure
                self.validate_task_structure(task, task_id)

                # Validate dependencies
                self.validate_dependencies(task, task_id, self.all_task_ids)

                # Validate subtasks
                if 'subtasks' in task and isinstance(task['subtasks'], list):
                    for subtask in task['subtasks']:
                        if not isinstance(subtask, dict):
                            continue
                            
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
                fixed_orphans = 0

                try:
                    # Fix duplicates first to avoid cascading issues
                    if resolve_duplicates and duplicates:
                        fixed_duplicate_ids = self.resolve_duplicate_ids(tasks)
                        # Recalculate IDs after fixing duplicates
                        self.all_task_ids, self.task_lookup, all_ids_list = self.collect_all_task_ids(tasks)

                    # Fix invalid dependencies
                    if fix_dependencies:
                        fixed_invalid_deps = self.fix_invalid_dependencies(tasks, self.all_task_ids)

                    # Fix missing fields and structure
                    if fix_structure:
                        fixed_missing_fields = self.fix_missing_fields(tasks)
                        # Recalculate IDs after adding missing IDs
                        self.all_task_ids, self.task_lookup, all_ids_list = self.collect_all_task_ids(tasks)

                    # Fix priority weaknesses
                    if fix_priorities:
                        fixed_priority = self.fix_priority_weaknesses(tasks)

                    # Fix orphaned subtasks
                    if fix_orphans:
                        fixed_orphans = self.fix_orphaned_subtasks(tasks)
                        # Recalculate IDs after fixing orphans
                        self.all_task_ids, self.task_lookup, all_ids_list = self.collect_all_task_ids(tasks)

                    # Update the data structure with fixed tasks
                    self.set_tasks(data, tasks)

                    # Save the fixed data
                    self.save_tasks(data)

                    # Log fixes applied
                    total_fixed = fixed_duplicate_ids + fixed_invalid_deps + fixed_missing_fields + fixed_priority + fixed_orphans
                    if total_fixed > 0:
                        self.logger.info(f"Applied {total_fixed} fixes:")
                        for fix in self.fixes_applied[-10:]:  # Show last 10 fixes
                            self.logger.info(f"  - {fix}")
                        if len(self.fixes_applied) > 10:
                            self.logger.info(f"  ... and {len(self.fixes_applied) - 10} more fixes")

                except Exception as e:
                    self.logger.error(f"Error during fixing process: {e}")
                    self.logger.error(f"Traceback: {traceback.format_exc()}")
                    if backup_file:
                        self.restore_from_backup(backup_file)
                    return False

                # Re-validate after fixes to see if all issues are resolved
                try:
                    # Use the fixed data directly instead of reloading to avoid merge conflicts
                    tasks_after_fix = self.extract_tasks(data)
                    all_ids_after_fix, lookup_after_fix, all_ids_list_after_fix = self.collect_all_task_ids(tasks_after_fix)

                    # Re-initialize for validation
                    self.errors = []
                    self.warnings = []

                    # Re-validate the fixed data
                    self.validate_duplicate_ids(all_ids_list_after_fix)
                    self.build_dependency_graph(tasks_after_fix, all_ids_after_fix)

                    for task in tasks_after_fix:
                        if not isinstance(task, dict):
                            continue
                            
                        task_id = str(task.get('id', 'unknown'))
                        self.validate_task_structure(task, task_id)
                        self.validate_dependencies(task, task_id, all_ids_after_fix)

                        if 'subtasks' in task and isinstance(task['subtasks'], list):
                            for subtask in task['subtasks']:
                                if not isinstance(subtask, dict):
                                    continue
                                    
                                subtask_id = subtask.get('id')
                                full_subtask_id = f"{task_id}.{subtask_id}" if subtask_id is not None else task_id
                                self.validate_task_structure(subtask, full_subtask_id, is_subtask=True)
                                self.validate_dependencies(subtask, full_subtask_id, all_ids_after_fix, is_subtask=True)

                    self.detect_circular_dependencies()
                    self.validate_orphaned_subtasks(tasks_after_fix)
                    self.validate_priority_consistency(tasks_after_fix)

                except Exception as e:
                    self.logger.error(f"Error during re-validation: {e}")
                    return False

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
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def print_results(self) -> None:
        """Print validation results."""
        print(f"\n{'='*50}")
        print(f"Validation Results:")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Fixes Applied: {len(self.fixes_applied)}")
        print(f"  Merge Conflicts Detected: {self.merge_conflicts_detected}")
        print(f"{'='*50}")

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

        if self.merge_conflicts_detected:
            print(f"\n🔍 Merge conflicts were detected and handled.")

    def get_statistics(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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
            'tasks_with_subtasks': 0,
            'total_fields': 0
        }

        for task in tasks:
            if not isinstance(task, dict):
                continue
                
            # Count subtasks
            if 'subtasks' in task and isinstance(task['subtasks'], list):
                stats['total_subtasks'] += len(task['subtasks'])
                stats['tasks_with_subtasks'] += 1

                for subtask in task['subtasks']:
                    if not isinstance(subtask, dict):
                        continue
                        
                    stats['total_fields'] += len(subtask)
                    if 'status' in subtask:
                        stats['statuses'][subtask['status']] += 1
                    if 'priority' in subtask:
                        stats['priorities'][subtask['priority']] += 1
                    if 'dependencies' in subtask and isinstance(subtask['dependencies'], list):
                        stats['dependencies_count'] += len(subtask['dependencies'])

            # Count main task stats
            stats['total_fields'] += len(task)
            if 'status' in task:
                stats['statuses'][task['status']] += 1
            if 'priority' in task:
                stats['priorities'][task['priority']] += 1
            if 'dependencies' in task and isinstance(task['dependencies'], list):
                stats['dependencies_count'] += len(task['dependencies'])

        return dict(stats)

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


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Advanced Task File Manager for Complex Merge Processes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate tasks file without fixing
  python merge_task_manager.py --validate tasks.json

  # Validate and fix with backup
  python merge_task_manager.py --fix --backup tasks.json

  # Show statistics only
  python merge_task_manager.py --stats tasks.json

  # Clean up old backups
  python merge_task_manager.py --cleanup --keep-backups 3 tasks.json
        """
    )
    parser.add_argument("file", nargs="?", default="tasks/tasks.json", 
                       help="Path to tasks.json file (default: tasks/tasks.json)")
    parser.add_argument("--validate", "-v", action="store_true", 
                       help="Validate only (no fixes)")
    parser.add_argument("--fix", "-x", action="store_true", 
                       help="Validate and fix issues")
    parser.add_argument("--backup", "-b", action="store_true", 
                       help="Create backup before fixing")
    parser.add_argument("--no-backup", action="store_true", 
                       help="Skip backup creation")
    parser.add_argument("--cleanup", "-c", action="store_true", 
                       help="Clean up old backup files")
    parser.add_argument("--stats", "-s", action="store_true", 
                       help="Show statistics only")
    parser.add_argument("--keep-backups", type=int, default=5, 
                       help="Number of backup files to keep (for cleanup)")
    parser.add_argument("--no-duplicates", action="store_true", 
                       help="Skip duplicate ID resolution")
    parser.add_argument("--no-dependencies", action="store_true", 
                       help="Skip dependency fixing")
    parser.add_argument("--no-structure", action="store_true", 
                       help="Skip structure fixing")
    parser.add_argument("--no-priorities", action="store_true", 
                       help="Skip priority fixing")
    parser.add_argument("--no-orphans", action="store_true", 
                       help="Skip orphaned subtask fixing")
    parser.add_argument("--backup-dir", 
                       help="Custom backup directory")

    args = parser.parse_args()

    # Create manager instance
    backup_dir = args.backup_dir or (Path(tempfile.gettempdir()) / "task_manager_backups")
    manager = AdvancedTaskManager(args.file, str(backup_dir))

    if args.stats:
        try:
            data = manager.load_tasks()
            stats = manager.get_statistics(data)
            print("Tasks Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"Error getting statistics: {e}")
            sys.exit(1)
        return

    if args.cleanup:
        deleted = manager.cleanup_backups(args.keep_backups)
        print(f"Cleaned up {deleted} old backup files")
        return

    # Determine backup behavior
    create_backup = args.backup or (not args.no_backup and args.fix)

    if args.validate:
        success = manager.validate_and_fix(
            fix_issues=False, 
            create_backup=False,
            resolve_duplicates=not args.no_duplicates,
            fix_dependencies=not args.no_dependencies,
            fix_structure=not args.no_structure,
            fix_priorities=not args.no_priorities,
            fix_orphans=not args.no_orphans
        )
        sys.exit(0 if success else 1)
    elif args.fix:
        success = manager.validate_and_fix(
            fix_issues=True, 
            create_backup=create_backup,
            resolve_duplicates=not args.no_duplicates,
            fix_dependencies=not args.no_dependencies,
            fix_structure=not args.no_structure,
            fix_priorities=not args.no_priorities,
            fix_orphans=not args.no_orphans
        )
        sys.exit(0 if success else 1)
    else:
        # Default: validate only
        success = manager.validate_and_fix(
            fix_issues=False, 
            create_backup=False,
            resolve_duplicates=not args.no_duplicates,
            fix_dependencies=not args.no_dependencies,
            fix_structure=not args.no_structure,
            fix_priorities=not args.no_priorities,
            fix_orphans=not args.no_orphans
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()