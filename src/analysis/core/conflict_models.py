"""Compatibility shim for :mod:`src.core.conflict_models`.

This module was a byte-for-byte copy of ``src/core/conflict_models.py``. Two
identical copies drift: a fix applied to one leaves the other stale, and which
behaviour you get depends on which import path a caller used. The canonical
module is ``src.core.conflict_models``; this path re-exports it so existing
imports keep working.
"""

from ...core.conflict_models import (  # noqa: F401
    AnalysisResult,
    Conflict,
    ConflictBlock,
    ConflictTypeExtended,
    ResolutionPlan,
    ResolutionStrategy,
    RiskLevel,
    ValidationResult,
)

__all__ = [
    "AnalysisResult",
    "Conflict",
    "ConflictBlock",
    "ConflictTypeExtended",
    "ResolutionPlan",
    "ResolutionStrategy",
    "RiskLevel",
    "ValidationResult",
]
