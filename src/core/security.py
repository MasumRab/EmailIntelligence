"""
Security utilities for path validation and sanitization.
"""

import os
import pathlib
from typing import Optional, Union
import logging
import re
import secrets
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import uuid4

logger = logging.getLogger(__name__)


def validate_path_safety(path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None) -> bool:
    """
    Validate that a path is safe and doesn't contain directory traversal attempts.

    Args:
        path: The path to validate
        base_dir: Optional base directory to resolve relative to

    Returns:
        True if path is safe, False otherwise
    """
    try:
        path_obj = pathlib.Path(path).resolve()

        # Check for directory traversal patterns
        path_str = str(path_obj)

        # Common directory traversal patterns
        traversal_patterns = ['..', '\\', '//', '/./', '\\./']
        for pattern in traversal_patterns:
            if pattern in str(path):
                logger.warning(f"Potential directory traversal detected in path: {path}")
                return False

        # If base_dir is specified, ensure path is within base_dir
        if base_dir:
            base_obj = pathlib.Path(base_dir).resolve()
            try:
                # Check if path is within base_dir
                path_obj.relative_to(base_obj)
            except ValueError:
                logger.warning(f"Path {path} is outside allowed base directory {base_dir}")
                return False

        # Additional safety checks
        if any(char in path_str for char in ['<', '>', '|', '?', '*']):
            logger.warning(f"Potentially dangerous characters detected in path: {path}")
            return False

        return True

    except Exception as e:
        logger.error(f"Error validating path {path}: {e}")
        return False


def sanitize_path(path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None) -> Optional[pathlib.Path]:
    """
    Sanitize a path by resolving it and ensuring it's safe.

    Args:
        path: The path to sanitize
        base_dir: Optional base directory to resolve relative to

    Returns:
        Sanitized Path object, or None if path is unsafe
    """
    if not validate_path_safety(path, base_dir):
        return None

    try:
        path_obj = pathlib.Path(path).resolve()

        # If base_dir is specified, ensure we return a path relative to base_dir
        if base_dir:
            base_obj = pathlib.Path(base_dir).resolve()
            try:
                relative_path = path_obj.relative_to(base_obj)
                return base_obj / relative_path
            except ValueError:
                # Path is not within base_dir, return None
                return None

        return path_obj

    except Exception as e:
        logger.error(f"Error sanitizing path {path}: {e}")
        return None


def secure_path_join(base_dir: Union[str, pathlib.Path], *paths: Union[str, pathlib.Path]) -> Optional[pathlib.Path]:
    """
    Securely join paths, preventing directory traversal attacks.

    Args:
        base_dir: Base directory
        *paths: Path components to join

    Returns:
        Joined path if safe, None otherwise
    """
    try:
        # Start with base directory
        result_path = pathlib.Path(base_dir)

        # Join each path component securely
        for path_component in paths:
            component_path = pathlib.Path(path_component)

def create_default_security_context() -> SecurityContext:
    """Create a default security context for internal operations"""
    return security_manager.create_session(
        user_id="system",
        permissions=[Permission.READ, Permission.WRITE, Permission.EXECUTE],
        security_level=SecurityLevel.INTERNAL,
        allowed_resources=["*"],
    )


class PathValidator:
    """Secure path validation to prevent directory traversal attacks"""

    @staticmethod
    def is_safe_path(base_path: Union[str, Path], requested_path: Union[str, Path]) -> bool:
        """
        Check if a requested path is safe (doesn't escape the base directory)

        Args:
            base_path: The base directory that should not be escaped
            requested_path: The path to validate

        Returns:
            True if the path is safe, False otherwise
        """
        try:
            base_path = Path(base_path).resolve()
            requested_path = Path(requested_path).resolve()

            # Check if the resolved path starts with the base path
            return requested_path.is_relative_to(base_path)
        except (ValueError, OSError):
            return False

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename to prevent path traversal and other attacks

        Args:
            filename: The filename to sanitize

        Returns:
            Sanitized filename safe for use
        """
        if not filename:
            return "default.db"

        # Remove any path separators and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', filename)

        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip(' .')

        # Ensure it's not empty and doesn't start with dangerous patterns
        if not sanitized or sanitized.startswith('.') or '..' in sanitized:
            return "default.db"

        # Limit length
        if len(sanitized) > 255:
            sanitized = sanitized[:255]

        return sanitized

    @staticmethod
    def validate_database_path(db_path: Union[str, Path], allowed_dir: Optional[Union[str, Path]] = None) -> Path:
        """
        Validate and sanitize a database path

        Args:
            db_path: The database path to validate
            allowed_dir: Optional base directory that the path must be within

        Returns:
            Validated and resolved Path object

        Raises:
            ValueError: If the path is not safe
        """
        if not db_path:
            raise ValueError("Database path cannot be empty")

        # Handle special in-memory database
        if str(db_path) == ":memory:":
            return Path(":memory:")

        path = Path(db_path)

        # Sanitize filename if it's just a filename
        if not path.is_absolute() and len(path.parts) == 1:
            path = Path(PathValidator.sanitize_filename(str(path)))

        # Resolve the path
        try:
            resolved_path = path.resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid path: {e}")

        # Check against allowed directory if specified
        if allowed_dir:
            allowed_dir = Path(allowed_dir).resolve()
            if not resolved_path.is_relative_to(allowed_dir):
                raise ValueError(f"Database path escapes allowed directory: {allowed_dir}")

        # Additional security checks
        if any(part.startswith('.') for part in resolved_path.parts):
            raise ValueError("Database path contains hidden files/directories")

        return resolved_path
=======
            # Check each component for traversal
            if not validate_path_safety(component_path):
                return None

            # Only allow simple filenames/directories (no absolute paths or traversal)
            if component_path.is_absolute() or '..' in str(component_path):
                logger.warning(f"Unsafe path component: {path_component}")
                return None

            result_path = result_path / component_path

        # Final validation
        if validate_path_safety(result_path, base_dir):
            return result_path

        return None

    except Exception as e:
        logger.error(f"Error joining paths: {e}")
        return None
