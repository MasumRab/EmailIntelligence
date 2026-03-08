"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Security and Resource Management for the Node-Based Email Intelligence Platform.

This module implements security measures and resource management for the node-based
workflow system.
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Optional

# Import bleach for proper HTML sanitization
try:
    import bleach
except ImportError:
    bleach = None
    import warnings

    warnings.warn(
        "bleach library not found. Install it using 'pip install bleach' for proper HTML sanitization."
    )


class SecurityLevel(Enum):
    """Security levels for nodes and workflows."""

    UNTRUSTED = "untrusted"
    LIMITED = "limited"
    TRUSTED = "trusted"
    SYSTEM = "system"


@dataclass
class ResourceLimits:
    """Resource limits for node execution."""

    max_memory_mb: int = 100
    max_execution_time_seconds: int = 30
    max_api_calls: int = 10
    max_file_size_bytes: int = 10 * 1024 * 1024  # 10MB


class SecurityManager:
    """Manages security and permissions for the node system."""

    def __init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.trusted_node_types = set()
        self.security_policies = {}
        self._api_call_counts = {}

    # TODO(P1, 3h): Implement comprehensive security policies with RBAC support
    # Pseudo code for RBAC security policies:
    # - Create Role-Based Access Control system
    # - Define roles: admin, user, guest with different permissions
    # - Implement permission checking for node execution
    # - Add user context to security validation
    # - Support role hierarchies and permission inheritance

    # TODO(P1, 4h): Add rate limiting for different user roles and node types
    # Pseudo code for rate limiting:
    # - Implement token bucket or sliding window algorithms
    # - Different limits for different user roles (admin: 1000/min, user: 100/min)
    # - Per-node-type rate limiting (expensive nodes: lower limits)
    # - Add rate limit headers to responses
    # - Implement rate limit bypass for trusted operations

    def register_trusted_node_type(self, node_type: str):
        """Register a node type as trusted."""
        self.trusted_node_types.add(node_type)
        self.logger.info(f"Registered trusted node type: {node_type}")

    def is_trusted_node(self, node_type: str) -> bool:
        """Check if a node type is trusted."""
        return node_type in self.trusted_node_types

    def validate_node_execution(self, node_type: str, config: Dict[str, Any]) -> bool:
        """Validate if a node can be executed based on security policies."""
        # Basic validation for potentially dangerous operations
        if node_type not in self.trusted_node_types:
            # Check for potentially unsafe configurations
            if config.get("code", "") or config.get("script", ""):
                self.logger.warning(
                    f"Untrusted node {node_type} has code configuration - access denied"
                )
                return False

        return True

    # TODO(P1, 5h): Implement comprehensive node validation with static analysis of config parameters
    # Pseudo code for static analysis validation:
    # - Parse config parameters for potentially dangerous patterns
    # - Check for SQL injection, XSS, command injection vulnerabilities
    # - Validate URLs, file paths, and external service calls
    # - Implement AST analysis for code/script parameters
    # - Add whitelist/blacklist validation for allowed operations

    # TODO(P2, 3h): Add support for dynamic security policies based on user context
    # Pseudo code for dynamic security policies:
    # - Load security policies based on user identity and context
    # - Support time-based policies (different rules during business hours)
    # - Implement location-based restrictions
    # - Add session-based security levels
    # - Support emergency override policies for critical operations

    def check_api_call_limit(self, workflow_id: str, node_id: str) -> bool:
        """Check if API call limits are exceeded."""
        key = f"{workflow_id}:{node_id}"
        count = self._api_call_counts.get(key, 0)

        # If we don't have a policy, use default limits
        limits = self.get_resource_limits(workflow_id, node_id)

        if count >= limits.max_api_calls:
            self.logger.warning(f"API call limit exceeded for {key}")
            return False

        self._api_call_counts[key] = count + 1
        return True

    def get_resource_limits(self, workflow_id: str, node_id: str) -> ResourceLimits:
        """Get resource limits for a specific workflow/node."""
        # In a real implementation, this would load from config
        return ResourceLimits()

    def reset_api_call_count(self, workflow_id: str, node_id: str):
        """Reset API call count for a workflow/node."""
        key = f"{workflow_id}:{node_id}"
        self._api_call_counts[key] = 0


class InputSanitizer:
    """Sanitizes inputs to prevent injection attacks."""

    @staticmethod
    def sanitize_string(value: str) -> str:
        """Sanitize a string input using proper HTML sanitization."""
        if not isinstance(value, str):
            raise ValueError("Expected string input")

        # If bleach is available, use it for proper HTML sanitization
        if bleach is not None:
            # Allow only safe HTML tags and attributes
            allowed_tags = [
                "p",
                "br",
                "strong",
                "em",
                "u",
                "ol",
                "ul",
                "li",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
            ]
            allowed_attributes = {
                "a": ["href", "title"],
                "img": ["src", "alt", "title"],
                "*": ["class", "id"],
            }
            # Clean HTML and strip malicious content
            sanitized = bleach.clean(
                value, tags=allowed_tags, attributes=allowed_attributes, strip=True
            )
        else:
            # Fallback to basic implementation if bleach is not available
            # Remove potentially dangerous characters/patterns
            sanitized = value.replace("<script", "&lt;script").replace(
                "javascript:", "javascript&#58;"
            )
            sanitized = sanitized.replace("onerror", "onerror&#58;").replace(
                "onload", "onload&#58;"
            )
            sanitized = sanitized.replace("<iframe", "&lt;iframe").replace("<object", "&lt;object")
            sanitized = sanitized.replace("<embed", "&lt;embed").replace("<form", "&lt;form")

        return sanitized

    # TODO(P1, 4h): Enhance sanitization to support additional content types (Markdown, etc.)
    # Pseudo code for additional content type sanitization:
    # - Add Markdown sanitization with allowed elements (headers, links, lists)
    # - Implement CSV sanitization to prevent formula injection
    # - Add XML sanitization with schema validation
    # - Support YAML sanitization with type safety checks
    # - Implement binary data sanitization for file uploads

    # TODO(P2, 2h): Add configurable sanitization policies based on security levels
    # Pseudo code for configurable sanitization policies:
    # - Create SanitizationPolicy class with different security levels
    # - Level 1 (Strict): Minimal allowed content, maximum security
    # - Level 2 (Standard): Balanced security and functionality
    # - Level 3 (Permissive): Maximum functionality, reduced security
    # - Allow per-user or per-operation policy selection

    @staticmethod
    def sanitize_json(value: str) -> Dict[str, Any]:
        """Sanitize and parse JSON input."""
        try:
            parsed = json.loads(value)
            return InputSanitizer._sanitize_dict(parsed)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input")

    @staticmethod
    def _sanitize_dict(obj: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitize a dictionary."""
        if not isinstance(obj, dict):
            return obj

        sanitized = {}
        for key, value in obj.items():
            if isinstance(value, str):
                sanitized[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = InputSanitizer._sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [InputSanitizer._sanitize_item(item) for item in value]
            else:
                sanitized[key] = value

        return sanitized

    @staticmethod
    def _sanitize_item(item: Any) -> Any:
        """Sanitize an item in a list."""
        if isinstance(item, str):
            return InputSanitizer.sanitize_string(item)
        elif isinstance(item, dict):
            return InputSanitizer._sanitize_dict(item)
        elif isinstance(item, list):
            return [InputSanitizer._sanitize_item(i) for i in item]
        return item


class ExecutionSandbox:
    """Provides a sandboxed environment for node execution."""

    def __init__(self, security_manager: SecurityManager):
        self.security_manager = security_manager
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    # TODO(P1, 8h): Implement comprehensive execution sandboxing with resource isolation
    # TODO(P2, 4h): Add support for custom execution environments based on node security levels

    async def execute_with_timeout(self, coro: Callable, timeout: int, *args, **kwargs) -> Any:
        """Execute a coroutine with a timeout."""
        try:
            result = await asyncio.wait_for(coro(*args, **kwargs), timeout=timeout)
            return result
        except asyncio.TimeoutError:
            raise RuntimeError(f"Execution timed out after {timeout} seconds")

    def validate_input_types(self, inputs: Dict[str, Any], expected_types: Dict[str, type]) -> bool:
        """Validate input types against expected types."""
        for port_name, expected_type in expected_types.items():
            if port_name in inputs:
                if not isinstance(inputs[port_name], expected_type):
                    self.logger.error(
                    f"Input validation failed: {port_name} expected "
                    f"{expected_type}, got {type(inputs[port_name])}"
                    )
                    return False
        return True


class AuditLogger:
    """Logs execution events for audit and debugging."""

    def __init__(self, log_file: str = "logs/workflow_audit.log"):
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        import os

        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Create file handler
        from logging.handlers import RotatingFileHandler

        handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_workflow_start(self, workflow_id: str, workflow_name: str, user_id: str = None):
        """Log workflow execution start."""
        self.logger.info(f"WORKFLOW_START: id={workflow_id}, name={workflow_name}, user={user_id}")

    def log_workflow_end(self, workflow_id: str, status: str, duration: float, user_id: str = None):
        """Log workflow execution end."""
        self.logger.info(
        f"WORKFLOW_END: id={workflow_id}, status={status}, "
        f"duration={duration}s, user={user_id}"
        )

    def log_node_execution(
        self, workflow_id: str, node_id: str, node_name: str, status: str, duration: float
    ):
        """Log node execution."""
        self.logger.info(
            f"NODE_EXEC: workflow={workflow_id}, node_id={node_id}, name={
                         node_name}, status={status}, duration={duration}s"
        )

    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related events."""
        self.logger.warning(f"SECURITY_EVENT: type={event_type}, details={details}")


class ResourceManager:
    """Manages resources for scalable node execution."""

    def __init__(self, max_concurrent_workflows: int = 10):
        self.max_concurrent_workflows = max_concurrent_workflows
        self.current_workflows = 0
        self.workflow_queue = asyncio.Queue()
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._resource_usage = {}

    async def acquire_resources(self, workflow_id: str, required_resources: ResourceLimits) -> bool:
        """Acquire resources for a workflow."""
        if self.current_workflows >= self.max_concurrent_workflows:
            self.logger.info(f"Max concurrent workflows reached. Workflow {workflow_id} queued.")
            await self.workflow_queue.put(workflow_id)
            return False

        self.current_workflows += 1
        self._resource_usage[workflow_id] = {
            "acquired_at": datetime.now(),
            "limits": required_resources,
        }

        self.logger.info(
            f"Resources acquired for workflow {workflow_id}. Current: {
                         self.current_workflows}/{self.max_concurrent_workflows}"
        )
        return True

    def release_resources(self, workflow_id: str):
        """Release resources for a workflow."""
        if workflow_id in self._resource_usage:
            del self._resource_usage[workflow_id]

        if self.current_workflows > 0:
            self.current_workflows -= 1

        self.logger.info(
            f"Resources released for workflow {workflow_id}. Current: {
                         self.current_workflows}/{self.max_concurrent_workflows}"
        )

    async def get_next_queued_workflow(self) -> Optional[str]:
        """Get the next workflow from the queue."""
        try:
            return await asyncio.wait_for(self.workflow_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None


# Global instances
security_manager = SecurityManager()

# Register trusted node types
for node_type in [
    "EmailSourceNode",
    "PreprocessingNode",
    "AIAnalysisNode",
    "FilterNode",
    "ActionNode",
]:
    security_manager.register_trusted_node_type(node_type)

audit_logger = AuditLogger()
resource_manager = ResourceManager()
