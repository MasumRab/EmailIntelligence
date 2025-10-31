"""
Security Framework for Email Intelligence Platform

Implements enterprise-grade security features for the node-based workflow system,
including access controls, data sanitization, execution sandboxing, and audit logging.

Also includes security utilities for path validation and sanitization.
"""

import os
import pathlib
import asyncio
import hashlib
import hmac
import json
import logging
import re
import secrets
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import uuid4
import pathlib

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for different operations and data access"""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class Permission(Enum):
    """Permission types for fine-grained access control"""

    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


@dataclass
class SecurityContext:
    """Holds security information for an execution context"""

    user_id: str
    permissions: List[Permission]
    security_level: SecurityLevel
    session_token: str
    created_at: float
    expires_at: float
    allowed_resources: List[str]
    ip_address: Optional[str] = None
    origin: Optional[str] = None


class SecurityValidator:
    """Validates security requirements for operations"""

    @staticmethod
    def validate_access(context: SecurityContext, resource: str, permission: Permission) -> bool:
        """
        Validate if a security context has permission to access a resource
        """
        if permission not in context.permissions:
            return False

        # Check if resource is in allowed resources
        if context.allowed_resources and resource not in context.allowed_resources:
            return False

        # Check expiration
        if time.time() > context.expires_at:
            return False

        return True

    @staticmethod
    def validate_data_access(context: SecurityContext, data: Dict[str, Any]) -> bool:
        """
        Validate if the security context can access the provided data
        """
        # Check for sensitive fields in the data
        sensitive_fields = ["password", "token", "key", "secret", "auth"]

        for key in data.keys():
            if any(sensitive in key.lower() for sensitive in sensitive_fields):
                # For sensitive data, check for elevated permissions
                if Permission.ADMIN not in context.permissions:
                    logger.warning(f"Access denied to sensitive field: {key}")
                    return False

        return True

def validate_path_safety(path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None) -> bool:
    """
    Validate that a path is safe and doesn't contain directory traversal attempts.

    Args:
        path: The path to validate
        base_dir: Optional base directory to resolve relative to

    Returns:
        True if path is safe, False otherwise
    """
    import pathlib
    
    try:
        path_obj = pathlib.Path(path)
        original_path = str(path)

        # If base_dir is provided and path is relative, resolve relative to base_dir
        if base_dir and not path_obj.is_absolute():
            path_obj = (pathlib.Path(base_dir) / path_obj).resolve()
        else:
            path_obj = path_obj.resolve()

        # Check for directory traversal patterns
        if ('../' in original_path or '..\\' in original_path or '/./' in original_path or '\\./' in original_path or original_path.startswith('\\\\') ):
            logger.warning(f"Directory traversal detected in path: {path}")
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
        resolved_str = str(path_obj)
        if any(char in resolved_str for char in ['<', '>', '|', '?', '*']):
            logger.warning(f"Potentially dangerous characters detected in path: {path}")
            return False

        return True
    except Exception as e:
        logger.error(f"Error validating path {path}: {e}")
        return False


def sanitize_path(path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None) -> Optional[pathlib.Path]:
    """
    Sanitize a path by validating it and returning the resolved path if safe.

    Args:
        path: The path to sanitize
        base_dir: Optional base directory for validation

    Returns:
        Resolved Path object if safe, None if unsafe
    """
    import pathlib

    try:
        path_obj = pathlib.Path(path)

        # First validate the path
        if not validate_path_safety(path, base_dir):
            return None

        # Return the resolved path
        return path_obj.resolve()

    except Exception as e:
        logger.warning(f"Error during path sanitization: {e}")
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
    import pathlib
    
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
