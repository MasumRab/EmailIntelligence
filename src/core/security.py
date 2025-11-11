"""
<<<<<<< HEAD
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
=======
Core security functionalities for the Email Intelligence Platform.
This module includes input validation, data sanitization, and other
security-related utilities to protect against common vulnerabilities.
"""

>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
import logging
import os
import re
<<<<<<< HEAD
import secrets
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import uuid4
from pathlib import Path
=======
from typing import Any, Dict, List
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d

logger = logging.getLogger(__name__)

# --- Constants for Sanitization ---
# Stricter regex for path validation to disallow '..'
SAFE_PATH_REGEX = re.compile(r"^[a-zA-Z0-9._-]+$")

# Regex to detect potentially sensitive key-value pairs in strings
# Looks for common key names followed by variations of separators and the value.
SENSITIVE_KEY_REGEX = re.compile(
    r"""
    (['"]?
    (password|secret|token|api_key|access_key|private_key|key|credentials|auth)
    ['"]?
    \s*[:=]\s*)
    (['"]?
    [^'"\s,}\]]+
    ['"]?)
    """,
    re.IGNORECASE | re.VERBOSE,
)
REDACTED_MESSAGE = "[REDACTED]"


<<<<<<< HEAD
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


def validate_path_safety(
    path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None
) -> bool:
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
        path_obj = pathlib.Path(path).resolve()

        # Check for directory traversal patterns
        path_str = str(path_obj)

        # Common directory traversal patterns
        # Check for directory traversal attempts by looking for '..' as a path segment
        if any(part == ".." for part in path_obj.parts):
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
        if any(char in path_str for char in ["<", ">", "|", "?", "*"]):
            logger.warning(f"Potentially dangerous characters detected in path: {path}")
            return False

        return True
    except Exception as e:
        logger.warning(f"Error during path validation: {e}")
        return False


def sanitize_path(path: Union[str, pathlib.Path]) -> Optional[str]:
    """
    Sanitize a path by removing or encoding potentially dangerous characters.

    Args:
        path: The path to sanitize

    Returns:
        Sanitized path string or None if path is invalid
    """
    import pathlib

    try:
        # Convert to string if it's a Path object
        path_str = str(path)

        # Basic sanitization - remove dangerous sequences
        path_str = path_str.replace("../", "").replace("..\\", "")

        # Normalize path separators
        path_str = path_str.replace("\\", "/")

        # Additional checks to ensure validity
        if any(char in path_str for char in ["<", ">", "|", "?", "*"]):
            logger.warning(f"Invalid characters in path after sanitization: {path_str}")
            return None

        return path_str
    except Exception as e:
        logger.warning(f"Error during path sanitization: {e}")
        return None

=======
# --- Data Sanitization ---
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d

class DataSanitizer:
    """A class to handle redaction of sensitive data from logs and outputs."""

    def __init__(self, sensitive_keys: List[str] = None, redaction_string: str = REDACTED_MESSAGE):
        """
        Initializes the DataSanitizer with a list of sensitive keys.
        """
        if sensitive_keys is None:
            sensitive_keys = [
                "password", "secret", "token", "api_key",
                "access_key", "private_key", "credentials", "auth"
            ]

<<<<<<< HEAD
    @staticmethod
    def sanitize_output(data: Any) -> Any:
        """
        Sanitize output data to prevent information disclosure
        """
        if isinstance(data, str):
            # Improved sanitization to redact sensitive key-value pairs
            # This regex looks for common sensitive keys followed by a colon and captures the value.
            sensitive_keys = ["password", "token", "key", "secret", "auth"]
            for key in sensitive_keys:
                # This regex will find 'key: value' and replace it with 'key: [REDACTED]'
                # It handles optional whitespace and stops at the next comma or end of string.
                data = re.sub(
                    rf"(\b{re.escape(key)}\b\s*:\s*)[^\s,]+",
                    r"\1[REDACTED]",
                    data,
                    flags=re.IGNORECASE,
                )
            return data
        elif isinstance(data, dict):
            sanitized_dict = {}
            for key, value in data.items():
                # Redact sensitive fields
                if any(
                    sensitive in key.lower() for sensitive in ["password", "token", "key", "secret"]
                ):
                    sanitized_dict[key] = "[REDACTED]"
                else:
                    sanitized_dict[key] = DataSanitizer.sanitize_output(value)
            return sanitized_dict
        elif isinstance(data, list):
            return [DataSanitizer.sanitize_output(item) for item in data]
        else:
            return data
=======
        self.sensitive_keys = sensitive_keys
        self.redaction_string = redaction_string
        self.sensitive_key_pattern = self._build_sensitive_key_regex(self.sensitive_keys)
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d

    def _build_sensitive_key_regex(self, keys: List[str]) -> re.Pattern:
        """Builds a regex to find sensitive key-value pairs from a list of keys."""
        key_pattern = "|".join(re.escape(key) for key in keys)

        # Group 1: The entire key part, including separator and opening quote for the value.
        # Group 2: The opening quote for the value, which should be matched at the end.
        return re.compile(
            r"""
            ( # Group 1: Key part up to the value's opening quote
                ['"]?                  # Optional opening quote for the key
                (?:{key_pattern})      # The sensitive key itself
                ['"]?                  # Optional closing quote for the key
                \s*[:=]\s*              # Separator
                (['"]?)                # Group 2: Optional opening quote for the value
            )
            (?:[^\s,'"{{}}]+)          # The value itself (non-capturing group)
            \2                         # Match the same quote as Group 2
            """.format(key_pattern=key_pattern),
            re.IGNORECASE | re.VERBOSE
        )

    def redact(self, data: Any) -> Any:
        """
        Recursively redacts sensitive information from various data structures.
        """
        if isinstance(data, dict):
            return {key: self.redact(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.redact(item) for item in data]
        elif isinstance(data, str):
            return self.redact_string(data)
        return data

    def redact_string(self, text: str) -> str:
        """
        Redacts sensitive key-value pairs from a string.
        """
        def repl(m):
            # m.group(1) is the key part (e.g., 'password": "')
            # m.group(2) is the quote character
            # We replace the whole match with key part + redacted string + closing quote
            return f"{m.group(1)}{self.redaction_string}{m.group(2)}"

        return self.sensitive_key_pattern.sub(repl, text)

# Default instance for convenience
default_sanitizer = DataSanitizer()

def sanitize_data(data: Any) -> Any:
    """
    Sanitizes data by redacting sensitive information using the default sanitizer.
    """
    return default_sanitizer.redact(data)


# --- Input Validation ---

<<<<<<< HEAD

def get_security_manager() -> SecurityManager:
    """Get the global security manager instance"""
    return security_manager


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
        except ValueError:
            # If the path is not relative to base (or other path resolution issues)
            return False

    @staticmethod
    def validate_and_resolve_db_path(db_path: Union[str, Path], 
                                   allowed_dir: Optional[Union[str, Path]] = None) -> Path:
        """
        Validate and resolve a database path with security checks

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

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename by removing dangerous characters

        Args:
            filename: The filename to sanitize

        Returns:
            Sanitized filename
        """
        # Remove any path traversal attempts and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Also avoid names that might be problematic on various systems
        if sanitized.upper() in ['CON', 'PRN', 'AUX', 'NUL'] or \
           sanitized.upper().startswith(('COM', 'LPT')):
            sanitized = f"_{sanitized}"
            
        return sanitized


def validate_path_safety(
    path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None
) -> bool:
=======
def validate_path_safety(path: str, base_dir: str = None) -> bool:
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
    """
    Validates a path to prevent directory traversal attacks.
    Ensures the path is within the intended directory and contains no malicious components.

    - Disallows absolute paths.
    - Prevents ".." components to stop directory traversal.
    - If base_dir is provided, ensures the resolved path is within base_dir.
    """
<<<<<<< HEAD
    import pathlib

    try:
        path_obj = pathlib.Path(path).resolve()

        # Check for directory traversal patterns
        path_str = str(path_obj)

        # Check for directory traversal attempts by looking for '..' as a path segment
        if any(part == ".." for part in path_obj.parts):
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
        if any(char in path_str for char in ["<", ">", "|", "?", "*"]):
            logger.warning(f"Potentially dangerous characters detected in path: {path}")
            return False

        return True
    except Exception as e:
        logger.error(f"Error validating path {path}: {e}")
=======
    if not isinstance(path, str) or not path:
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
        return False

    # 1. Disallow absolute paths
    if os.path.isabs(path):
        logger.warning(f"Path validation failed: Absolute path detected '{path}'")
        return False

<<<<<<< HEAD
def sanitize_path(
    path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None
) -> Optional[str]:
    """
    Sanitize a path by removing or encoding potentially dangerous characters.

    Args:
        path: The path to sanitize

    Returns:
        Sanitized path string or None if path is invalid
    """
    import pathlib

    try:
        # Convert to string if it's a Path object
        path_str = str(path)

        # Basic sanitization - remove dangerous sequences
        path_str = path_str.replace("../", "").replace("..\\", "")
        path_str = path_str.replace("<!--", "").replace("-->", "")  # Prevent comment injection
        path_str = path_str.replace("<script", "").replace(
            "script>", ""
        )  # Prevent script injection

        # Normalize path separators
        path_str = path_str.replace("\\", "/")

        # Additional checks to ensure validity
        if any(char in path_str for char in ["<", ">", "|", "?", "*"]):
            logger.warning(f"Invalid characters in path after sanitization: {path_str}")
            return None

        return path_str
    except Exception as e:
        logger.warning(f"Error during path sanitization: {e}")
        return None
=======
    # 2. Check for directory traversal attempts
    if ".." in path.split(os.path.sep):
        logger.warning(f"Path validation failed: Directory traversal attempt in '{path}'")
        return False

    # 3. Normalize the path to resolve any redundant separators
    normalized_path = os.path.normpath(path)

    # 4. If a base directory is provided, check that the path is contained within it
    if base_dir:
        # Ensure base_dir is an absolute path for reliable comparison
        abs_base_dir = os.path.abspath(base_dir)

        # Resolve the full path of the user-provided path relative to the base directory
        full_path = os.path.abspath(os.path.join(abs_base_dir, normalized_path))

        # Check if the resolved path is a subdirectory of the base directory
        if not full_path.startswith(abs_base_dir):
            logger.warning(
                f"Path validation failed: Path '{full_path}' is outside of base directory '{abs_base_dir}'"
            )
            return False

    return True

def sanitize_path(path: str) -> str:
    """
    Sanitizes a path by removing potentially malicious characters and components.
    This is a stronger measure than validation alone, intended to produce a safe
    version of a given path.
    """
    if not isinstance(path, str) or not path:
        return ""
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d

    # Split the path into components
    parts = path.split(os.path.sep)

<<<<<<< HEAD
def secure_path_join(
    base_dir: Union[str, pathlib.Path], *paths: Union[str, pathlib.Path]
) -> Optional[pathlib.Path]:
=======
    # Filter out any dangerous components ('..', '.', etc.)
    safe_parts = [part for part in parts if part and part not in ('.', '..')]

    # Further sanitize each part to remove unsafe characters
    sanitized_parts = [SAFE_PATH_REGEX.sub('', part) for part in safe_parts]

    # Rejoin the sanitized parts
    return os.path.join(*sanitized_parts)

def validate_email_format(email: str) -> bool:
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
    """
    Validates if a string is a correctly formatted email address.
    """
<<<<<<< HEAD
    import pathlib

    try:
        # Start with base directory
        result_path = pathlib.Path(base_dir)
=======
    # A simple but effective regex for email validation
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return email_regex.match(email) is not None
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d

def validate_user_input(
    data: Dict[str, Any],
    required_fields: List[str],
    field_validators: Dict[str, callable] = None
) -> List[str]:
    """
    A generic utility to validate user-provided data dictionaries.

    - Checks for the presence of all required fields.
    - Applies specific validation functions to fields if provided.

<<<<<<< HEAD
            # Only allow simple filenames/directories (no absolute paths or traversal)
            if component_path.is_absolute() or ".." in str(component_path):
                logger.warning(f"Unsafe path component: {path_component}")
                return None
=======
    Returns a list of validation error messages. An empty list means success.
    """
    errors = []
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d

    # 1. Check for missing required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: '{field}'")

<<<<<<< HEAD
        # Final validation
        return result_path if validate_path_safety(result_path, base_dir) else None

    except Exception as e:
        logger.error(f"Error joining paths: {e}")
        return None
=======
    if errors:
        return errors  # Return early if required fields are missing

    # 2. Apply custom validators for specific fields
    if field_validators:
        for field, validator in field_validators.items():
            if field in data:
                if not validator(data[field]):
                    errors.append(f"Invalid format for field: '{field}'")

    return errors
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
