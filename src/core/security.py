"""
Security Framework for Email Intelligence Platform

Implements enterprise-grade security features for the node-based workflow system,
including access controls, data sanitization, execution sandboxing, and audit logging.

Also includes security utilities for path validation and sanitization.
"""

import hashlib
import hmac
import html
import json
import logging
import os
import pathlib
import re
import secrets
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

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

    def __init__(self, base_dir: Optional[Union[str, Path]] = None):
        self.base_dir = base_dir or os.getcwd()

    def validate_io(self, path: str, mode: str = "r") -> bool:
        """
        Validates an I/O operation.
        Returns True if the path is safe, False otherwise.
        """
        return validate_path_safety(path, self.base_dir)

    def sanitize(self, path: str) -> Optional[Path]:
        """Sanitizes a path."""
        return sanitize_path(path, self.base_dir)

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


class SecureFileSystemProxy:
    """
    Proxy Pattern Implementation for Gated I/O.
    Intercepts file system operations to enforce SecurityValidator rules.
    """

    def __init__(self, validator: SecurityValidator):
        self._validator = validator

    def secure_open(
        self,
        file,
        mode="r",
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None,
    ):
        """
        Gated wrapper for the built-in open() function.
        Raises PermissionError if the path is not validated by the SecurityValidator.
        """
        # Convert path-like objects to strings for the validator
        path_str = str(file)

        if not self._validator.validate_io(path_str, mode):
            logger.error(
                f"SECURITY VIOLATION: Unauthorized access attempt to '{path_str}' [mode: {mode}]"
            )
            raise PermissionError(
                f"Access to path '{path_str}' is denied by SecurityPolicy."
            )

        return open(file, mode, buffering, encoding, errors, newline, closefd, opener)


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
    if base_dir is None:
        # Without a base_dir, perform strict validation of the path structure
        str_path = str(path).replace("\\", "/")

        # Check for dangerous characters (cross-platform)
        if re.search(r'[<>"|?*]', str_path):
            return False

        # Reject UNC-like paths (starting with //)
        if str_path.startswith("//"):
            return False

        # Split path into components to check for traversal and dot segments
        parts = str_path.split("/")

        # Check for traversal components
        if ".." in parts:
            return False

        # Reject absolute paths containing '.' segments (e.g. /./etc/passwd)
        if str_path.startswith("/") and "." in parts:
            return False

        return True

    try:
        base_path = pathlib.Path(base_dir).resolve()
        requested_path = (base_path / path).resolve()
        return requested_path.is_relative_to(base_path)
    except (ValueError, TypeError):
        return False


def sanitize_path(
    path: Union[str, pathlib.Path], base_dir: Optional[Union[str, pathlib.Path]] = None
) -> Optional[pathlib.Path]:
    """
    Sanitize a path by resolving it and ensuring it's within a base directory.

    Args:
        path: The path to sanitize
        base_dir: The base directory to confine the path to. If None, the CWD is used.

    Returns:
        A resolved, safe Path object or None if the path is unsafe.
    """
    if not validate_path_safety(path, base_dir):
        return None

    base_path = (pathlib.Path(base_dir) if base_dir else pathlib.Path.cwd()).resolve()
    return (base_path / path).resolve()


class DataSanitizer:
    """Sanitizes data to prevent injection and other security issues"""

    @staticmethod
    def sanitize_input(data: Any) -> Any:
        """
        Sanitize input data to prevent injection attacks
        """
        if isinstance(data, str):
            # Use html.escape to prevent XSS
            return html.escape(data)
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
            sensitive_keys = ["password", "token", "key", "secret", "auth"]
            for key in sensitive_keys:
                pattern = (
                    rf'((?:["\']?[\w-]*{re.escape(key)}[\w-]*["\']?)\s*:\s*)'
                    r"(?:"
                    r'(?:"[^"]*")|'
                    r"(?:'[^']*')|"
                    r"[^,\s}]+"
                    r")"
                )
                data = re.sub(
                    pattern,
                    r"\1[REDACTED]",
                    data,
                    flags=re.IGNORECASE,
                )
            return data
        elif isinstance(data, dict):
            sanitized_dict = {}
            for key, value in data.items():
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


class ExecutionSandbox:
    """Provides a secure execution environment for nodes"""

    def __init__(self, context: SecurityContext):
        self.context = context
        self.audit_logger = AuditLogger()

    async def execute_with_security(self, execute_func, *args, **kwargs):
        """
        Execute a function with security checks and monitoring
        """
        if time.time() > self.context.expires_at:
            raise PermissionError("Session has expired")

        sanitized_args = [DataSanitizer.sanitize_input(arg) for arg in args]
        sanitized_kwargs = {
            k: DataSanitizer.sanitize_input(v) for k, v in kwargs.items()
        }

        try:
            result = await execute_func(*sanitized_args, **sanitized_kwargs)
            return DataSanitizer.sanitize_output(result)
        except Exception as e:
            logger.error(f"Error during secure execution: {e}")
            raise


class SecurityManager:
    """
    Centralized security manager for the Email Intelligence Platform
    """

    def __init__(self):
        self.validator = SecurityValidator()
        self.sanitizer = DataSanitizer()
        self.audit_logger = AuditLogger()
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.secret_key = secrets.token_urlsafe(32)

    def create_session(
        self,
        user_id: str,
        permissions: List[Permission],
        security_level: SecurityLevel,
        allowed_resources: Optional[List[str]] = None,
        duration_hours: float = 8.0,
        ip_address: Optional[str] = None,
        origin: Optional[str] = None,
    ) -> SecurityContext:
        """Create a new security session"""
        session_token = secrets.token_urlsafe(32)
        context = SecurityContext(
            user_id=user_id,
            permissions=permissions,
            security_level=security_level,
            session_token=session_token,
            created_at=time.time(),
            expires_at=time.time() + (duration_hours * 3600),
            allowed_resources=allowed_resources or [],
            ip_address=ip_address,
            origin=origin,
        )
        self.active_sessions[session_token] = context
        return context


class PathValidator:
    """Secure path validation to prevent directory traversal attacks"""

    @staticmethod
    def is_safe_path(
        base_path: Union[str, Path], requested_path: Union[str, Path]
    ) -> bool:
        """
        Check if a requested path is safe (doesn't escape the base directory)
        """
        try:
            base_path = Path(base_path).resolve()
            requested_path = Path(requested_path).resolve()
            return requested_path.is_relative_to(base_path)
        except ValueError:
            return False

    @staticmethod
    def validate_database_path(
        db_path: Union[str, Path], allowed_dir: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Validate and resolve a database path with security checks
        """
        if not db_path:
            raise ValueError("Database path cannot be empty")

        if str(db_path) == ":memory:":
            return Path(":memory:")

        path = Path(db_path)
        if not path.is_absolute() and len(path.parts) == 1:
            path = Path(PathValidator.sanitize_filename(str(path)))

        try:
            resolved_path = path.resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid path: {e}")

        if allowed_dir:
            allowed_dir = Path(allowed_dir).resolve()
            if not resolved_path.is_relative_to(allowed_dir):
                raise ValueError(
                    f"Database path escapes allowed directory: {allowed_dir}"
                )

        return resolved_path

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize a filename by removing dangerous characters"""
        sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
        if sanitized.upper() in ["CON", "PRN", "AUX", "NUL"] or sanitized.upper().startswith(("COM", "LPT")):
            sanitized = f"_{sanitized}"
        return sanitized


def secure_path_join(
    base_dir: Union[str, Path], *paths: Union[str, Path]
) -> Optional[Path]:
    """Securely join paths, preventing directory traversal attacks."""
    try:
        result_path = Path(base_dir).resolve()
        for path_component in paths:
            if not validate_path_safety(path_component, result_path):
                return None
            result_path = (result_path / path_component).resolve()
        return result_path
    except Exception as e:
        logger.error(f"Error joining paths: {e}")
        return None
