"""
Shared utilities for Task Master scripts to eliminate code duplication
"""

import json
import os
import re
import shutil
import sys
import tempfile
import time
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Union

class SecurityValidator:
    """Centralized security validation for all scripts"""
    
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

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(max_size)

        # Check if file is larger than read content
        if len(content) == max_size:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.seek(max_size)
                if f.read(1):  # If there's more content
                    raise ValueError("File size exceeds maximum allowed size")

        return json.loads(content)

class TaskValidator:
    """Centralized task validation utilities"""
    
    @staticmethod
    def collect_all_task_ids(tasks: List[Dict[str, Any]]) -> tuple[Set[str], Dict[str, Any], List[str]]:
        """Collect all task IDs for dependency validation."""
        all_ids = set()
        all_ids_list = []
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