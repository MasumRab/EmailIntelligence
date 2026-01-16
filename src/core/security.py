"""
Security and validation module for EmailIntelligence CLI
Separated from main CLI to follow Single Responsibility Principle
"""
from pathlib import Path
from typing import Union
import re


class SecurityValidator:
    """Handles security validation and path safety checks"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def is_safe_path(self, path: Union[str, Path]) -> bool:
        """Validate that a path is safe and within the repository"""
        try:
            path_obj = Path(path)
            # Resolve the path to its absolute form
            resolved_path = path_obj.resolve()
            # Ensure the path is within the repository root
            resolved_path.relative_to(self.repo_root)
            return True
        except ValueError:
            # Path is outside the repository root
            return False

    def is_valid_pr_number(self, pr_number: int) -> bool:
        """Validate that the PR number is reasonable"""
        return isinstance(pr_number, int) and 1 <= pr_number <= 99999

    def is_valid_git_reference(self, ref: str) -> bool:
        """Validate git reference (branch name) to prevent command injection"""
        # Git reference naming rules: alphanumeric, hyphens, underscores, slashes
        # Cannot start/end with slash, no consecutive slashes, no special characters
        if not ref or len(ref) > 1024:  # Reasonable length limit
            return False
        # Check for valid characters and patterns
        if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._/-]*[a-zA-Z0-9]$', ref) or ref in ['HEAD', 'main', 'master']:
            # Additional check for dangerous patterns
            if '..' in ref or '@{' in ref or '\\' in ref:
                return False
            return True
        return False

    def sanitize_input(self, input_str: str) -> str:
        """Sanitize input string to prevent injection attacks"""
        # Remove potentially dangerous characters
        sanitized = input_str.replace(';', '').replace('|', '').replace('&', '').replace('`', '')
        sanitized = sanitized.replace('$(', '').replace('${', '').replace('<', '').replace('>', '')
        return sanitized

    def validate_file_path(self, file_path: Union[str, Path]) -> bool:
        """Validate file path to prevent directory traversal and other attacks"""
        path_obj = Path(file_path)
        
        # Check for directory traversal attempts
        if '..' in str(path_obj):
            return False
            
        # Check if path is absolute (which could be dangerous)
        if path_obj.is_absolute():
            # If absolute, ensure it's within repo root
            return self.is_safe_path(path_obj)
        else:
            # If relative, resolve it and check safety
            resolved = (self.repo_root / path_obj).resolve()
            return self.is_safe_path(resolved)