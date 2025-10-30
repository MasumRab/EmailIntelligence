"""
Security Framework for Email Intelligence Platform

Implements enterprise-grade security features for the node-based workflow system,
including access controls, data sanitization, execution sandboxing, and audit logging.
"""

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
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
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
            "input_keys": list(inputs.keys()) if isinstance(inputs, dict) else "unknown",
        }
        self.logger.info(f"EXECUTION: {json.dumps(log_entry)}")

    def log_security_violation(self, context: SecurityContext, violation_type: str, details: str):
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
            node_type=execute_func.__name__ if hasattr(execute_func, "__name__") else "unknown",
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
        sanitized_kwargs = {k: DataSanitizer.sanitize_input(v) for k, v in kwargs.items()}

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
        self.secret_key = secrets.token_urlsafe(32)  # In production, load from secure storage

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
