"""
Validation Module

Provides validation utilities for code and configurations.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    details: Dict[str, Any]


class Validator:
    """
    Validates code and configurations.
    """

    def __init__(self):
        self.rules = []

    async def validate(self, target: Any, context: Dict = None) -> ValidationResult:
        """Validate a target object."""
        errors = []
        warnings = []

        if isinstance(target, str):
            # Validate code string
            if "eval(" in target or "exec(" in target:
                warnings.append("Use of eval() or exec() detected")
            if "shell=True" in target:
                warnings.append("shell=True in subprocess detected")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            details={"target_type": type(target).__name__},
        )

    def add_rule(self, rule_func, description: str):
        """Add a custom validation rule."""
        self.rules.append((rule_func, description))
