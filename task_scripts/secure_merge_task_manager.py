#!/usr/bin/env python3
"""
Secure Merge Task Manager - Production-Ready Script

This script provides a robust, secure, and production-ready solution for managing
complex merge processes with comprehensive validation, security checks, and audit trails.
"""

import os
import sys
import json
import logging
import subprocess
import tempfile
import shutil
import hashlib
import time
import argparse
import re
import secrets
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import yaml
from contextlib import contextmanager
import threading
import queue
import importlib.util


class LogLevel(Enum):
    """Log levels for the application."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class TaskStatus(Enum):
    """Status of a merge task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    VALIDATION_FAILED = "validation_failed"


@dataclass
class TaskResult:
    """Result of a merge task operation."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None


class SecurityValidator:
    """Security validation utilities for file paths and commands."""
    
    @staticmethod
    def validate_path(path: str, base_dir: str = None) -> bool:
        """Validate that a path is safe and within allowed boundaries."""
        try:
            path_obj = Path(path).resolve()
            
            # Check for path traversal attempts
            if ".." in path.split("/") or ".." in path.split("\\"):
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
                r'\|\|.*\|\|' # Multiple commands
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, path, re.IGNORECASE):
                    return False
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def sanitize_command(cmd: List[str]) -> List[str]:
        """Sanitize command arguments to prevent command injection."""
        sanitized = []
        for arg in cmd:
            # Remove potentially dangerous characters
            if isinstance(arg, str):
                # Basic sanitization - in production, you might want more sophisticated validation
                if not re.match(r'^[a-zA-Z0-9._/-]+$', arg):
                    raise ValueError(f"Invalid command argument: {arg}")
            sanitized.append(arg)
        return sanitized


class AuditLogger:
    """Enhanced audit trail logger for tracking all merge operations."""

    def __init__(self, log_file: str = None):
        self.log_file = log_file or "merge_audit.log"
        self.logger = logging.getLogger("merge_audit")
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Create rotating file handler for better log management
            from logging.handlers import RotatingFileHandler
            handler = RotatingFileHandler(
                self.log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_operation(self, operation: str, details: Dict[str, Any], user_id: str = None):
        """Log a merge operation with details and optional user identification."""
        log_entry = {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "user_id": user_id,
            "session_id": getattr(self, '_session_id', secrets.token_hex(16))
        }
        self.logger.info(json.dumps(log_entry))

    def log_error(self, error_msg: str, context: Dict[str, Any] = None, user_id: str = None):
        """Log an error with context and optional user identification."""
        log_entry = {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": error_msg,
            "context": context or {},
            "user_id": user_id,
            "session_id": getattr(self, '_session_id', secrets.token_hex(16))
        }
        self.logger.error(json.dumps(log_entry))

    def log_security_event(self, event_type: str, details: Dict[str, Any], severity: str = "INFO"):
        """Log a security-related event with severity level."""
        log_entry = {
            "operation": "security_event",
            "event_type": event_type,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "session_id": getattr(self, '_session_id', secrets.token_hex(16))
        }

        if severity.upper() == "ERROR":
            self.logger.error(json.dumps(log_entry))
        elif severity.upper() == "WARNING":
            self.logger.warning(json.dumps(log_entry))
        else:
            self.logger.info(json.dumps(log_entry))

    def log_validation_result(self, validator_type: str, target: str, result: bool, details: str = ""):
        """Log the result of a validation."""
        self.log_operation(
            'validation_result',
            {
                'validator': validator_type,
                'target': target,
                'result': result,
                'details': details
            }
        )


class ConfigurationManager:
    """Enhanced configuration manager with validation and security."""

    def __init__(self, config_file: str = "merge_config.yaml"):
        self.config_file = config_file
        # Try to import our config validation module
        try:
            spec = importlib.util.spec_from_file_location("config_validation",
                                                         os.path.join(os.path.dirname(__file__), "config_validation.py"))
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            self.config_validator_class = config_module.ConfigManager
            self.input_validator_class = config_module.InputValidator
        except ImportError:
            print("Warning: config_validation module not found, using basic config manager")
            self.config_validator_class = None
            self.input_validator_class = None

        if self.config_validator_class:
            self.config_manager = self.config_validator_class(config_file)
            self.config = self.config_manager.config
        else:
            self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "security": {
                "max_file_size_mb": 100,
                "allowed_extensions": [".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml", ".txt", ".md"],
                "forbidden_patterns": ["eval\\(", "exec\\(", "importlib\\.", "subprocess\\."],
                "enable_security_scan": True,
                "enable_syntax_check": True,
                "max_diff_lines": 10000
            },
            "logging": {
                "level": "INFO",
                "audit_file": "merge_audit.log",
                "max_log_size_mb": 10,
                "backup_count": 5,
                "console_output": False
            },
            "validation": {
                "enable_syntax_check": True,
                "enable_security_scan": True,
                "max_diff_lines": 10000,
                "validate_file_integrity": True
            },
            "backup": {
                "create_backup": True,
                "backup_suffix": ".backup",
                "max_backups": 5,
                "backup_on_validation_error": False
            },
            "general": {
                "session_timeout_minutes": 60,
                "max_concurrent_operations": 5,
                "enable_audit_trail": True
            }
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                # Merge user config with defaults
                config = self._deep_merge(default_config, user_config)
                return config
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
                return default_config

        return default_config

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation)."""
        if self.config_validator_class:
            return self.config_manager.get(key, default)

        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def validate_config(self, task_config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate task configuration using input validator."""
        if self.input_validator_class:
            validator = self.input_validator_class(self)
            result = validator.validate_task_config(task_config)
            all_errors = result["errors"] + result["warnings"]  # Include warnings as well
            return len(result["errors"]) == 0, all_errors
        else:
            # Basic validation if module not available
            required_fields = ["source_branch", "target_branch"]
            errors = []
            for field in required_fields:
                if field not in task_config or not task_config[field]:
                    errors.append(f"Missing required field: {field}")
            return len(errors) == 0, errors


class FileValidator:
    """Validate files for security and integrity."""
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
    
    def validate_file(self, file_path: str) -> TaskResult:
        """Validate a file for security and integrity."""
        try:
            # Check file exists
            if not os.path.exists(file_path):
                return TaskResult(False, f"File does not exist: {file_path}")
            
            # Check file size
            max_size = self.config.get("security.max_file_size_mb", 100) * 1024 * 1024
            if os.path.getsize(file_path) > max_size:
                return TaskResult(False, f"File too large: {file_path}")
            
            # Check file extension
            allowed_extensions = self.config.get("security.allowed_extensions", [])
            file_ext = Path(file_path).suffix.lower()
            if file_ext not in allowed_extensions:
                return TaskResult(False, f"File extension not allowed: {file_ext}")
            
            # Check for forbidden patterns (security scan)
            if self.config.get("validation.enable_security_scan", True):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                forbidden_patterns = self.config.get("security.forbidden_patterns", [])
                for pattern in forbidden_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        return TaskResult(False, f"Forbidden pattern found in {file_path}: {pattern}")
            
            return TaskResult(True, "File validation passed")
        
        except Exception as e:
            return TaskResult(False, f"File validation error: {str(e)}", error_details=str(e))
    
    def validate_diff_size(self, diff_content: str) -> TaskResult:
        """Validate that diff content is not too large."""
        max_lines = self.config.get("validation.max_diff_lines", 10000)
        line_count = len(diff_content.split('\n'))
        
        if line_count > max_lines:
            return TaskResult(False, f"Diff too large: {line_count} lines (max: {max_lines})")
        
        return TaskResult(True, "Diff size validation passed")


class BackupManager:
    """Manage file backups during merge operations."""
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
    
    def create_backup(self, file_path: str) -> Optional[str]:
        """Create a backup of the specified file."""
        if not self.config.get("backup.create_backup", True):
            return None
        
        try:
            backup_suffix = self.config.get("backup.backup_suffix", ".backup")
            backup_path = f"{file_path}{backup_suffix}_{int(time.time())}"
            
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Warning: Could not create backup for {file_path}: {e}")
            return None
    
    def cleanup_old_backups(self, file_path: str):
        """Clean up old backups for a file."""
        max_backups = self.config.get("backup.max_backups", 5)
        backup_suffix = self.config.get("backup.backup_suffix", ".backup")
        
        # Find all backups for this file
        dir_path = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        
        backups = []
        for item in os.listdir(dir_path):
            if item.startswith(f"{base_name}{backup_suffix}"):
                backup_path = os.path.join(dir_path, item)
                backups.append((backup_path, os.path.getctime(backup_path)))
        
        # Sort by creation time (oldest first) and remove excess
        backups.sort(key=lambda x: x[1])
        for backup_path, _ in backups[:-max_backups]:
            try:
                os.remove(backup_path)
            except Exception as e:
                print(f"Warning: Could not remove old backup {backup_path}: {e}")


class GitManager:
    """Manage Git operations safely."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.validator = SecurityValidator()
    
    def _execute_git_command(self, cmd: List[str]) -> Tuple[bool, str, str]:
        """Execute a git command safely."""
        try:
            # Validate command arguments
            cmd = self.validator.sanitize_command(cmd)
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            
            return success, stdout, stderr
        except subprocess.TimeoutExpired:
            return False, "", "Git command timed out"
        except Exception as e:
            return False, "", f"Git command error: {str(e)}"
    
    def get_current_branch(self) -> TaskResult:
        """Get the current Git branch."""
        success, stdout, stderr = self._execute_git_command(["git", "branch", "--show-current"])
        if success:
            return TaskResult(True, "Current branch retrieved", data={"branch": stdout})
        else:
            return TaskResult(False, f"Could not get current branch: {stderr}")
    
    def check_merge_conflicts(self, branch: str) -> TaskResult:
        """Check if merging the specified branch would create conflicts."""
        # Create a temporary branch to test the merge
        temp_branch = f"merge_test_{int(time.time())}"
        
        # Create and switch to temp branch
        success, _, stderr = self._execute_git_command(["git", "checkout", "-b", temp_branch])
        if not success:
            return TaskResult(False, f"Could not create temp branch: {stderr}")
        
        try:
            # Attempt to merge
            success, stdout, stderr = self._execute_git_command(["git", "merge", branch])
            
            if success:
                # Check if merge was fast-forward or if there are conflicts
                if "CONFLICT" in stdout or "conflict" in stderr.lower():
                    return TaskResult(False, "Merge conflicts detected", data={"conflicts": True})
                else:
                    return TaskResult(True, "No merge conflicts detected", data={"conflicts": False})
            else:
                if "CONFLICT" in stderr or "conflict" in stderr.lower():
                    return TaskResult(False, "Merge conflicts detected", data={"conflicts": True})
                else:
                    return TaskResult(False, f"Merge failed: {stderr}")
        finally:
            # Clean up temp branch
            self._execute_git_command(["git", "checkout", "-"])
            self._execute_git_command(["git", "branch", "-D", temp_branch])


class MergeTaskManager:
    """Main merge task manager with comprehensive security and validation."""
    
    def __init__(self, config_file: str = "merge_config.yaml"):
        self.config = ConfigurationManager(config_file)
        self.validator = FileValidator(self.config)
        self.backup_manager = BackupManager(self.config)
        self.git_manager = GitManager()
        self.audit_logger = AuditLogger(self.config.get("logging.audit_file", "merge_audit.log"))
        self.lock = threading.Lock()
        
        # Setup logging
        log_level = getattr(logging, self.config.get("logging.level", "INFO"))
        logging.basicConfig(level=log_level)
    
    def execute_merge_task(self, task_config: Dict[str, Any]) -> TaskResult:
        """Execute a merge task with full validation and security checks."""
        with self.lock:
            try:
                # Validate task configuration
                validation_result = self._validate_task_config(task_config)
                if not validation_result.success:
                    self.audit_logger.log_error(
                        "Task configuration validation failed",
                        {"task_config": task_config, "error": validation_result.message}
                    )
                    return validation_result
                
                # Log the start of the merge operation
                self.audit_logger.log_operation("merge_task_start", {
                    "task_id": task_config.get("task_id"),
                    "source_branch": task_config.get("source_branch"),
                    "target_branch": task_config.get("target_branch"),
                    "files": task_config.get("files", []),
                    "timestamp": datetime.now().isoformat()
                })
                
                # Perform syntax checking if enabled
                if self.config.get("validation.enable_syntax_check", True):
                    syntax_result = self._check_syntax(task_config.get("files", []))
                    if not syntax_result.success:
                        self.audit_logger.log_error(
                            "Syntax check failed",
                            {"files": task_config.get("files", []), "error": syntax_result.message}
                        )
                        return syntax_result
                
                # Perform the merge operation
                merge_result = self._perform_merge(task_config)
                
                # Log the result
                self.audit_logger.log_operation("merge_task_complete", {
                    "task_id": task_config.get("task_id"),
                    "success": merge_result.success,
                    "message": merge_result.message,
                    "timestamp": datetime.now().isoformat()
                })
                
                return merge_result
                
            except Exception as e:
                error_msg = f"Merge task execution failed: {str(e)}"
                self.audit_logger.log_error(error_msg, {"task_config": task_config})
                return TaskResult(False, error_msg, error_details=str(e))
    
    def _validate_task_config(self, config: Dict[str, Any]) -> TaskResult:
        """Validate the task configuration using enhanced validation."""
        # Use the configuration manager's validation
        is_valid, errors = self.config.validate_config(config)

        if not is_valid:
            return TaskResult(False, f"Task configuration validation failed: {'; '.join(errors)}")

        # Additional security validation
        required_fields = ["source_branch", "target_branch"]
        for field in required_fields:
            if field not in config or not config[field]:
                return TaskResult(False, f"Missing required field: {field}")

        # Validate file paths if provided
        files = config.get("files", [])
        for file_path in files:
            if not SecurityValidator.validate_path(file_path):
                return TaskResult(False, f"Invalid file path: {file_path}")

            validation_result = self.validator.validate_file(file_path)
            if not validation_result.success:
                return validation_result

        return TaskResult(True, "Task configuration validated")
    
    def _check_syntax(self, files: List[str]) -> TaskResult:
        """Check syntax of Python files."""
        for file_path in files:
            if file_path.endswith('.py'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    compile(content, file_path, 'exec')
                except SyntaxError as e:
                    return TaskResult(False, f"Syntax error in {file_path}: {str(e)}")
                except Exception as e:
                    return TaskResult(False, f"Could not check syntax for {file_path}: {str(e)}")
        
        return TaskResult(True, "Syntax check passed")
    
    def _perform_merge(self, task_config: Dict[str, Any]) -> TaskResult:
        """Perform the actual merge operation."""
        source_branch = task_config["source_branch"]
        target_branch = task_config["target_branch"]
        
        try:
            # Check for merge conflicts first
            conflict_check = self.git_manager.check_merge_conflicts(source_branch)
            if not conflict_check.success and conflict_check.data.get("conflicts"):
                return TaskResult(False, "Merge conflicts detected, aborting merge")
            
            # Switch to target branch
            success, _, stderr = self.git_manager._execute_git_command(["git", "checkout", target_branch])
            if not success:
                return TaskResult(False, f"Could not switch to target branch {target_branch}: {stderr}")
            
            # Perform merge
            success, stdout, stderr = self.git_manager._execute_git_command(["git", "merge", source_branch])
            if not success:
                # Rollback to previous state
                self.git_manager._execute_git_command(["git", "merge", "--abort"])
                return TaskResult(False, f"Merge failed: {stderr}")
            
            # Create backups for modified files
            files = task_config.get("files", [])
            for file_path in files:
                if os.path.exists(file_path):
                    backup_path = self.backup_manager.create_backup(file_path)
                    if backup_path:
                        print(f"Created backup: {backup_path}")
            
            return TaskResult(True, f"Successfully merged {source_branch} into {target_branch}", 
                            data={"merged_branch": source_branch, "target_branch": target_branch})
        
        except Exception as e:
            return TaskResult(False, f"Merge operation failed: {str(e)}", error_details=str(e))
    
    def rollback_merge(self, task_config: Dict[str, Any]) -> TaskResult:
        """Rollback a merge operation."""
        try:
            target_branch = task_config["target_branch"]
            
            # Reset to previous state (one commit before the merge)
            success, stdout, stderr = self.git_manager._execute_git_command([
                "git", "reset", "--hard", "HEAD~1"
            ])
            
            if success:
                return TaskResult(True, f"Successfully rolled back merge on {target_branch}")
            else:
                return TaskResult(False, f"Rollback failed: {stderr}")
        
        except Exception as e:
            return TaskResult(False, f"Rollback operation failed: {str(e)}", error_details=str(e))


def main():
    """Main function to run the merge task manager."""
    parser = argparse.ArgumentParser(description="Secure Merge Task Manager")
    parser.add_argument("--config", default="merge_config.yaml", help="Configuration file path")
    parser.add_argument("--task-file", required=True, help="Task configuration file")
    parser.add_argument("--rollback", action="store_true", help="Rollback the merge operation")
    
    args = parser.parse_args()
    
    # Initialize the merge task manager
    manager = MergeTaskManager(args.config)
    
    # Load task configuration
    try:
        with open(args.task_file, 'r') as f:
            task_config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading task configuration: {e}")
        sys.exit(1)
    
    # Execute the task
    if args.rollback:
        result = manager.rollback_merge(task_config)
    else:
        result = manager.execute_merge_task(task_config)
    
    # Print result
    print(f"Task Result: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Message: {result.message}")
    
    if result.error_details:
        print(f"Error Details: {result.error_details}")
    
    if result.data:
        print(f"Data: {json.dumps(result.data, indent=2)}")
    
    # Exit with appropriate code
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()