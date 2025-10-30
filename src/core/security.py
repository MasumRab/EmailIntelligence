"""
<<<<<<< HEAD
Security Framework for Email Intelligence Platform

Implements enterprise-grade security features for the node-based workflow system,
including access controls, data sanitization, execution sandboxing, and audit logging.

Also includes security utilities for path validation and sanitization.
"""

import pathlib
import hashlib
import hmac
import json
import logging
import re
import secrets
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4
from pathlib import Path
=======
Security utilities for path validation and sanitization.
"""

import os
import pathlib
from typing import Optional, Union
import logging
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)

logger = logging.getLogger(__name__)

# Security enums and classes
class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"

class SecurityLevel(Enum):
    UNTRUSTED = "untrusted"
    LIMITED = "limited"
    TRUSTED = "trusted"
    INTERNAL = "internal"
    SYSTEM = "system"

@dataclass
class SecurityContext:
    user_id: str
    permissions: List[Permission] = None
    security_level: SecurityLevel = SecurityLevel.TRUSTED
    allowed_resources: List[str] = None
    session_id: str = None

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []
        if self.allowed_resources is None:
            self.allowed_resources = []
        if self.session_id is None:
            self.session_id = str(uuid4())

class SecurityManager:
    """Manages security contexts and sessions."""

    def create_session(self, user_id: str, permissions: List[Permission],
                      security_level: SecurityLevel, allowed_resources: List[str]) -> SecurityContext:
        """Create a new security context/session."""
        return SecurityContext(
            user_id=user_id,
            permissions=permissions,
            security_level=security_level,
            allowed_resources=allowed_resources
        )

class DataSanitizer:
    """Sanitizes data to prevent injection and other security issues"""

    @staticmethod
    def sanitize_input(data: Any) -> Any:
        """
        Sanitize input data to prevent injection attacks
        """
        if isinstance(data, str):
            # Basic sanitization - in production, use a library like bleach
            sanitized = data.replace("<script", "&lt;script").replace("javascript:", "javascript-")
            return sanitized
        elif isinstance(data, dict):
            sanitized_dict = {}
            for key, value in data.items():
                sanitized_dict[DataSanitizer.sanitize_input(key)] = DataSanitizer.sanitize_input(
                    value
                )
            return sanitized_dict
        elif isinstance(data, list):
            return [DataSanitizer.sanitize_input(item) for item in data]
        else:
            return data

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
                    rf'(\b{re.escape(key)}\b\s*:\s*)[^\s,]+',
                    r'\1[REDACTED]',
                    data,
                    flags=re.IGNORECASE
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

    @staticmethod
    def sanitize_string(input_str: str) -> str:
        """Sanitize string input."""
        return DataSanitizer.sanitize_input(input_str)

    @staticmethod
    def sanitize_path(path: str) -> str:
        """Sanitize file path."""
        return sanitize_path(path)  # Use existing function

class SecurityValidator:
    """Validates security constraints."""

    @staticmethod
    def validate_operation(operation: str, context: SecurityContext) -> bool:
        """Validate if operation is allowed in given security context."""
        # Simple validation - check if operation requires permissions we have
        required_permissions = {
            'read': [Permission.READ],
            'write': [Permission.WRITE],
            'execute': [Permission.EXECUTE],
            'delete': [Permission.DELETE]
        }

        perms = required_permissions.get(operation.lower(), [])
        return all(perm in context.permissions for perm in perms)

# Global security manager instance
security_manager = SecurityManager()

# Import SecurityContext from node_base if available (override our fallback)
try:
    from backend.node_engine.node_base import SecurityContext as NodeSecurityContext
    SecurityContext = NodeSecurityContext  # Use the node version if available
except ImportError:
    pass  # Use our fallback


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
        traversal_patterns = ['..', '/../', '/..', '\\..\\', '..\\', '/./', '\\./']
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

<<<<<<< HEAD
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
    def validate_access(
        context: SecurityContext, resource: str, permission: Permission
    ) -> bool:
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
=======
        # Additional safety checks
        if any(char in path_str for char in ['<', '>', '|', '?', '*']):
            logger.warning(f"Potentially dangerous characters detected in path: {path}")
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
            return False

        return True

    except Exception as e:
        logger.error(f"Error validating path {path}: {e}")
        return False


<<<<<<< HEAD
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
                logger.warning(
                    f"Path {path} is outside allowed base directory {base_dir}"
                )
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


class DataSanitizer:
    """Sanitizes data to prevent injection and other security issues"""

    @staticmethod
    def sanitize_input(data: Any) -> Any:
        """
        Sanitize input data to prevent injection attacks
        """
        if isinstance(data, str):
            # Basic sanitization - in production, use a library like bleach
            sanitized = data.replace("<script", "&lt;script").replace(
                "javascript:", "javascript-"
            )
            return sanitized
        elif isinstance(data, dict):
            sanitized_dict = {}
            for key, value in data.items():
                sanitized_dict[DataSanitizer.sanitize_input(key)] = (
                    DataSanitizer.sanitize_input(value)
                )
            return sanitized_dict
        elif isinstance(data, list):
            return [DataSanitizer.sanitize_input(item) for item in data]
        else:
            return data

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
                    sensitive in key.lower()
                    for sensitive in ["password", "token", "key", "secret"]
                ):
                    sanitized_dict[key] = "[REDACTED]"
                else:
                    sanitized_dict[key] = DataSanitizer.sanitize_output(value)
            return sanitized_dict
        elif isinstance(data, list):
            return [DataSanitizer.sanitize_output(item) for item in data]
        else:
            return data


class AuditLogger:
    """Logs security-related events for audit purposes"""

    def __init__(self):
        self.logger = logging.getLogger("security.audit")

    def log_access_attempt(
        self,
        context: SecurityContext,
        resource: str,
        permission: Permission,
        success: bool,
        details: str = "",
    ):
        """Log an access attempt to a resource"""
        log_entry = {
            "timestamp": time.time(),
            "user_id": context.user_id,
            "session_token": context.session_token,
            "resource": resource,
            "permission": permission.value,
            "success": success,
            "ip_address": context.ip_address,
            "details": details,
        }
        self.logger.info(f"ACCESS_ATTEMPT: {json.dumps(log_entry)}")

    def log_execution(
        self,
        context: SecurityContext,
        node_type: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
    ):
        """Log a node execution for audit purposes"""
        log_entry = {
            "timestamp": time.time(),
            "user_id": context.user_id,
            "session_token": context.session_token,
            "node_type": node_type,
            "execution_id": str(uuid4()),
            "ip_address": context.ip_address,
            "input_keys": list(inputs.keys())
            if isinstance(inputs, dict)
            else "unknown",
        }
        self.logger.info(f"EXECUTION: {json.dumps(log_entry)}")

    def log_security_violation(
        self, context: SecurityContext, violation_type: str, details: str
    ):
        """Log a security violation"""
        log_entry = {
            "timestamp": time.time(),
            "user_id": context.user_id,
            "session_token": context.session_token,
            "violation_type": violation_type,
            "details": details,
            "ip_address": context.ip_address,
        }
        self.logger.warning(f"SECURITY_VIOLATION: {json.dumps(log_entry)}")


class ExecutionSandbox:
    """Provides a secure execution environment for nodes"""

    def __init__(self, context: SecurityContext):
        self.context = context
        self.audit_logger = AuditLogger()

    async def execute_with_security(self, execute_func, *args, **kwargs):
        """
        Execute a function with security checks and monitoring
        """
        # Log the execution attempt
        self.audit_logger.log_execution(
            context=self.context,
            node_type=execute_func.__name__
            if hasattr(execute_func, "__name__")
            else "unknown",
            inputs=kwargs,
            outputs={},
        )

        # Perform security checks
        if time.time() > self.context.expires_at:
            self.audit_logger.log_security_violation(
                self.context,
                "EXPIRED_SESSION",
                f"Attempted execution with expired session (expired at {self.context.expires_at})",
            )
            raise PermissionError("Session has expired")

        # Sanitize inputs
        sanitized_args = [DataSanitizer.sanitize_input(arg) for arg in args]
        sanitized_kwargs = {
            k: DataSanitizer.sanitize_input(v) for k, v in kwargs.items()
        }

        try:
            # Execute the function in a controlled environment
            result = await execute_func(*sanitized_args, **sanitized_kwargs)

            # Sanitize outputs
            sanitized_result = DataSanitizer.sanitize_output(result)

            return sanitized_result

        except Exception as e:
            self.audit_logger.log_security_violation(
                self.context, "EXECUTION_ERROR", f"Error during execution: {str(e)}"
            )
            raise


class SecurityManager:
=======
def sanitize_path(path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None) -> Optional[pathlib.Path]:
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
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

<<<<<<< HEAD
    def __init__(self):
        self.validator = SecurityValidator()
        self.sanitizer = DataSanitizer()
        self.audit_logger = AuditLogger()
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.secret_key = secrets.token_urlsafe(
            32
        )  # In production, load from secure storage
=======
    try:
        path_obj = pathlib.Path(path).resolve()
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)

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

<<<<<<< HEAD
<<<<<<< HEAD
=======
            # Check each component for traversal
            if not validate_path_safety(str(component_path)):
                return None

            # Only allow simple filenames/directories (no absolute paths or traversal)
            if component_path.is_absolute() or '..' in str(component_path):
                return None

            result_path = result_path / component_path

        # Validate final path is within base directory
        result_path = result_path.resolve()
        base_resolved = pathlib.Path(base_dir).resolve()

        if not str(result_path).startswith(str(base_resolved)):
            return None

        return result_path

    except Exception:
        return None

        return result_path

    except Exception:
        return None

>>>>>>> d1ac970f (feat: Complete task verification framework and fix security module)
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
    def is_safe_path(
        base_path: Union[str, Path], requested_path: Union[str, Path]
    ) -> bool:
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
    def validate_and_resolve_db_path(
        db_path: Union[str, Path], allowed_dir: Optional[Union[str, Path]] = None
    ) -> Path:
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
                raise ValueError(
                    f"Database path escapes allowed directory: {allowed_dir}"
                )

        # Additional security checks
        if any(part.startswith(".") for part in resolved_path.parts):
            raise ValueError("Database path contains hidden files/directories")

        return resolved_path
<<<<<<< HEAD

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
        sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)

        # Also avoid names that might be problematic on various systems
        if sanitized.upper() in [
            "CON",
            "PRN",
            "AUX",
            "NUL",
        ] or sanitized.upper().startswith(("COM", "LPT")):
            sanitized = f"_{sanitized}"

        return sanitized


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
                logger.warning(
                    f"Path {path} is outside allowed base directory {base_dir}"
                )
                return False

        # Additional safety checks
        if any(char in path_str for char in ["<", ">", "|", "?", "*"]):
            logger.warning(f"Potentially dangerous characters detected in path: {path}")
            return False

        return True
    except Exception as e:
        logger.error(f"Error validating path {path}: {e}")
        return False


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

        # Use pathlib's resolve and relative_to for more robust directory traversal prevention
        # instead of simple string replacement
        base_path = pathlib.Path(base_dir) if base_dir else pathlib.Path.cwd()
        input_path = pathlib.Path(path_str)

        # Resolve the path to handle relative paths and symbolic links
        resolved_path = input_path.resolve()

        # Verify that the resolved path is within the allowed base directory
        if base_dir and not resolved_path.is_relative_to(base_path):
            logger.warning(f"Path escapes base directory: {path_str}")
            return None

        # Normalize path separators
        normalized_path = str(resolved_path).replace("\\", "/")

        # Additional checks to ensure validity
        if any(char in normalized_path for char in ["<", ">", "|", "?", "*"]):
            logger.warning(
                f"Invalid characters in path after sanitization: {normalized_path}"
            )
            return None

        return normalized_path
    except Exception as e:
        logger.warning(f"Error during path sanitization: {e}")
        return None


def secure_path_join(
    base_dir: Union[str, pathlib.Path], *paths: Union[str, pathlib.Path]
) -> Optional[pathlib.Path]:
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

=======
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
            # Check each component for traversal
            if not validate_path_safety(component_path):
                return None

            # Only allow simple filenames/directories (no absolute paths or traversal)
<<<<<<< HEAD
            if component_path.is_absolute() or ".." in str(component_path):
=======
            if component_path.is_absolute() or '..' in str(component_path):
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
                logger.warning(f"Unsafe path component: {path_component}")
                return None

            result_path = result_path / component_path

        # Final validation
<<<<<<< HEAD
        return result_path if validate_path_safety(result_path, base_dir) else None
=======
        if validate_path_safety(result_path, base_dir):
            return result_path

        return None
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)

    except Exception as e:
        logger.error(f"Error joining paths: {e}")
        return None
=======
>>>>>>> d1ac970f (feat: Complete task verification framework and fix security module)
