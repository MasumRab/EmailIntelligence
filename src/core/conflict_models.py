from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class ValidationStatus(Enum):
    """Validation status levels"""
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    ERROR = "error"

@dataclass
class ValidationResult:
    """Result of security validation."""
    is_valid: bool
    violations: List[str]
    warnings: List[str]
    recommendations: List[str]
