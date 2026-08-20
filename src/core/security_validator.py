"""
Security Validation for Workflows and Nodes

Provides comprehensive security validation for workflow execution, node operations,
and data processing with configurable security levels.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .audit_logger import AuditEventType, AuditSeverity, audit_logger

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for validation."""

    UNTRUSTED = "untrusted"
    LIMITED = "limited"
    TRUSTED = "trusted"
    SYSTEM = "system"


@dataclass
class ValidationResult:
    """Result of security validation."""

    is_valid: bool
    violations: List[str]
    warnings: List[str]
    recommendations: List[str]


class NodeSecurityValidator:
    """
    Validates security aspects of workflow nodes.
    """

    # Dangerous patterns to check for
    DANGEROUS_PATTERNS = [
        r"\bimport\s+os\b",
        r"\bimport\s+subprocess\b",
        r"\bimport\s+sys\b",
        r"\beval\s*\(",
        r"\bexec\s*\(",
        r"\bopen\s*\(",
        r"\b__import__\s*\(",
        r"\bgetattr\s*\(",
        r"\bsetattr\s*\(",
        r"\bdelattr\s*\(",
        r"\bglobals\s*\(",
        r"\blocals\s*\(",
        r"\bvars\s*\(",
        r"\bdir\s*\(",
        r"\bcompile\s*\(",
        r"\binput\s*\(",
        r"\braw_input\s*\(",
    ]

    # Allowed modules for different security levels
    ALLOWED_MODULES = {
        SecurityLevel.UNTRUSTED: {
            "math",
            "random",
            "datetime",
            "json",
            "re",
            "string",
            "collections",
        },
        SecurityLevel.LIMITED: {
            "math",
            "random",
            "datetime",
            "json",
            "re",
            "string",
            "collections",
            "urllib.parse",
            "base64",
            "hashlib",
            "hmac",
        },
        SecurityLevel.TRUSTED: {
            "math",
            "random",
            "datetime",
            "json",
            "re",
            "string",
            "collections",
            "urllib.parse",
            "base64",
            "hashlib",
            "hmac",
            "os.path",
            "pathlib",
        },
        SecurityLevel.SYSTEM: set(),  # No restrictions
    }

    def validate_node_code(
        self,
        code: str,
        security_level: SecurityLevel,
        node_name: str,
        user_id: Optional[str] = None,
    ) -> ValidationResult:
        """
        Validate node code for security violations.

        Args:
            code: Python code to validate
            security_level: Security level to validate against
            node_name: Name of the node for logging
            user_id: User ID for audit logging

        Returns:
            ValidationResult with findings
        """
        violations = []
        warnings = []
        recommendations = []

        # Check for dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code):
                violations.append(f"Dangerous pattern detected: {pattern}")

        # Check for allowed modules based on security level
        if security_level != SecurityLevel.SYSTEM:
            allowed_modules = self.ALLOWED_MODULES[security_level]

            # Extract import statements
            import_pattern = r"^\s*(?:from\s+(\w+(?:\.\w+)*)|import\s+(\w+(?:\.\w+)*))"
            imports = re.findall(import_pattern, code, re.MULTILINE)

            for from_import, import_stmt in imports:
                module_name = from_import or import_stmt
                if module_name and module_name not in allowed_modules:
                    violations.append(
                        f"Module '{module_name}' not allowed at {security_level.value} security level"
                    )

        # Check for network operations (warnings for untrusted/limited)
        if security_level in [SecurityLevel.UNTRUSTED, SecurityLevel.LIMITED]:
            network_patterns = [
                r"\brequests\b",
                r"\burllib\b",
                r"\bhttp\b",
                r"\bsocket\b",
            ]
            for pattern in network_patterns:
                if re.search(pattern, code):
                    warnings.append(f"Network operation detected: {pattern}")

        # Recommendations
        if violations:
            recommendations.append(
                "Review and sanitize node code to remove security violations"
            )
        if warnings:
            recommendations.append(
                "Consider code review for potential security implications"
            )

        result = ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            recommendations=recommendations,
        )

        # Audit log the validation
        if not result.is_valid:
            audit_logger.log_security_event(
                event_type=AuditEventType.SECURITY_VIOLATION,
                severity=AuditSeverity.HIGH,
                user_id=user_id,
                resource=f"node:{node_name}",
                action="code_validation",
                result="failure",
                details={
                    "violations": violations,
                    "warnings": warnings,
                    "security_level": security_level.value,
                },
            )

        return result

    def validate_node_config(
        self, config: Dict[str, Any], security_level: SecurityLevel, node_name: str
    ) -> ValidationResult:
        """
        Validate node configuration for security issues.
        """
        violations = []
        warnings = []
        recommendations = []

        # Check for dangerous configuration values
        dangerous_keys = ["password", "secret", "key", "token", "credential"]
        for key in config.keys():
            if any(dangerous_key in key.lower() for dangerous_key in dangerous_keys):
                warnings.append(f"Potentially sensitive configuration key: {key}")

        # Check for file paths
        if "file_path" in config or "path" in config:
            path_value = config.get("file_path") or config.get("path")
            if path_value and ".." in str(path_value):
                violations.append("Path traversal detected in configuration")

        # Size limits based on security level
        if security_level == SecurityLevel.UNTRUSTED:
            max_size = 1024 * 1024  # 1MB
        elif security_level == SecurityLevel.LIMITED:
            max_size = 10 * 1024 * 1024  # 10MB
        else:
            max_size = 100 * 1024 * 1024  # 100MB

        if "max_size" in config and config["max_size"] > max_size:
            violations.append(
                f"Size limit {config['max_size']} exceeds maximum for {security_level.value} level"
            )

        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            recommendations=recommendations,
        )


class WorkflowSecurityValidator:
    """
    Validates security aspects of workflows.
    """

    def validate_workflow_execution(
        self,
        workflow_config: Dict[str, Any],
        user_id: str,
        security_level: SecurityLevel,
    ) -> ValidationResult:
        """
        Validate workflow execution for security compliance.
        """
        violations = []
        warnings = []
        recommendations = []

        # Check workflow size limits
        node_count = len(workflow_config.get("nodes", []))
        if security_level == SecurityLevel.UNTRUSTED and node_count > 5:
            violations.append("Workflow too large for untrusted security level")
        elif security_level == SecurityLevel.LIMITED and node_count > 20:
            violations.append("Workflow too large for limited security level")

        # Check for circular dependencies (potential DoS)
        nodes = workflow_config.get("nodes", [])
        edges = workflow_config.get("edges", [])

        # Simple cycle detection
        if self._has_cycles(edges):
            violations.append("Workflow contains circular dependencies")

        # Check for resource-intensive operations
        resource_intensive_nodes = ["ai_model", "batch_processor", "external_api"]
        resource_count = sum(
            1 for node in nodes if node.get("type") in resource_intensive_nodes
        )

        if security_level == SecurityLevel.UNTRUSTED and resource_count > 0:
            violations.append(
                "Resource-intensive operations not allowed at untrusted level"
            )
        elif security_level == SecurityLevel.LIMITED and resource_count > 2:
            warnings.append("Multiple resource-intensive operations detected")

        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            recommendations=recommendations,
        )

    def _has_cycles(self, edges: List[Dict[str, Any]]) -> bool:
        """Simple cycle detection in workflow graph."""
        # Build adjacency list
        graph = {}
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            if source not in graph:
                graph[source] = []
            graph[source].append(target)

        # Simple DFS-based cycle detection
        visited = set()
        rec_stack = set()

        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True

        return False


# Global validators
node_validator = NodeSecurityValidator()
workflow_validator = WorkflowSecurityValidator()
