"""
Security utilities for path validation and sanitization.
"""

import os
import pathlib
from typing import Optional, Union
import logging

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
