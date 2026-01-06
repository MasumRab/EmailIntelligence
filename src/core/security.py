"""
Security Framework for Email Intelligence Platform

Implements enterprise-grade security features for the node-based workflow system,
including access controls, data sanitization, execution sandboxing, and audit logging.

Also includes security utilities for path validation and sanitization.
"""

import pathlib
import hashlib
import html
import hmac
import json
import logging
import re
import secrets
import time
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4
from pathlib import Path

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
        str_path = str(path).replace('\\', '/')

        # Check for dangerous characters (cross-platform)
        if re.search(r'[<>"|?*]', str_path):
            return False

        # Reject UNC-like paths (starting with //)
        if str_path.startswith('//'):
             return False

        # Split path into components to check for traversal and dot segments
        parts = str_path.split('/')

        # Check for traversal components
        if '..' in parts:
            return False

        # Reject absolute paths containing '.' segments (e.g. /./etc/passwd)
        # This is often used for obfuscation.
        if str_path.startswith('/') and '.' in parts:
            return False

        return True

    try:
        base_path = pathlib.Path(base_dir).resolve()
        # Ensure we don't accidentally resolve relative paths against CWD implicitly if not intended,
        # but here we join with base_path, so relative paths are resolved against base_path.
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
            # Use html.escape to prevent XSS by escaping all HTML characters
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
            # Improved sanitization to redact sensitive key-value pairs
            # This regex looks for common sensitive keys followed by a colon and captures the value.
            sensitive_keys = ["password", "token", "key", "secret", "auth"]
            for key in sensitive_keys:
                # Improved regex:
                # 1. Key part: Matches optional quotes, then any word characters surrounding the sensitive key
                #    e.g. "api_key", 'auth_token', password
                # 2. Value part: Matches either quoted string (simple) or unquoted characters until separator
                pattern = (
                    rf'((?:["\']?[\w-]*{re.escape(key)}[\w-]*["\']?)\s*:\s*)'  # Capture group 1: Key + colon
                    r'(?:'
                    r'(?:"[^"]*")|'      # Double quoted value
                    r"(?:'[^']*')|"      # Single quoted value
                    r'[^,\s}]+'          # Unquoted value
                    r')'
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
    """
    Centralized security manager for the Email Intelligence Platform
    """

    def __init__(self):
        self.validator = SecurityValidator()
        self.sanitizer = DataSanitizer()
        self.audit_logger = AuditLogger()
        self.active_sessions: Dict[str, SecurityContext] = {}
        self.secret_key = secrets.token_urlsafe(
            32
        )  # In production, load from secure storage

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

    def validate_session(self, session_token: str) -> Optional[SecurityContext]:
        """Validate a session token and return the context"""
        if session_token not in self.active_sessions:
            return None

        context = self.active_sessions[session_token]

        if time.time() > context.expires_at:
            # Clean up expired session
            del self.active_sessions[session_token]
            return None

        return context

    def generate_signed_token(self, data: Dict[str, Any]) -> str:
        """Generate a signed token for secure data transmission"""
        json_data = json.dumps(data, sort_keys=True, separators=(",", ":"))
        signature = hmac.new(
            self.secret_key.encode(), json_data.encode(), hashlib.sha256
        ).hexdigest()
        return f"{json_data}.{signature}"

    def verify_signed_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a signed token and return the data"""
        if "." not in token:
            return None

        try:
            json_part, signature_part = token.rsplit(".", 1)
            expected_signature = hmac.new(
                self.secret_key.encode(), json_part.encode(), hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, signature_part):
                return None

            return json.loads(json_part)
        except (json.JSONDecodeError, ValueError):
            return None

    def cleanup_expired_sessions(self):
        """Remove expired sessions from memory"""
        current_time = time.time()
        expired_tokens = [
            token
            for token, context in self.active_sessions.items()
            if current_time > context.expires_at
        ]

        for token in expired_tokens:
            del self.active_sessions[token]

        if expired_tokens:
            logger.info(f"Cleaned up {len(expired_tokens)} expired sessions")

    async def secure_execute_node(
        self, session_token: str, node_type: str, inputs: Dict[str, Any], execute_func
    ) -> Dict[str, Any]:
        """Securely execute a node with full security checks"""
        context = self.validate_session(session_token)
        if not context:
            raise PermissionError("Invalid or expired session")

        # Validate access to execute this node type
        if not self.validator.validate_access(context, node_type, Permission.EXECUTE):
            self.audit_logger.log_access_attempt(
                context,
                node_type,
                Permission.EXECUTE,
                False,
                "Insufficient permissions to execute node",
            )
            raise PermissionError(f"Insufficient permissions to execute {node_type}")

        # Validate data access
        if not self.validator.validate_data_access(context, inputs):
            self.audit_logger.log_security_violation(
                context,
                "DATA_ACCESS_VIOLATION",
                f"Attempted to access sensitive data through {node_type}",
            )
            raise PermissionError("Attempted to access sensitive data")

        # Create sandbox and execute
        sandbox = ExecutionSandbox(context)
        return await sandbox.execute_with_security(execute_func, **inputs)


# Global security manager instance
security_manager = SecurityManager()


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
        result_path = pathlib.Path(base_dir).resolve()

        # Join each path component securely
        for path_component in paths:
            if not validate_path_safety(path_component, result_path):
                return None
            result_path = (result_path / path_component).resolve()

        return result_path

    except Exception as e:
        logger.error(f"Error joining paths: {e}")
        return None
