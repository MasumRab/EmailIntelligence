"""Compatibility shim for :mod:`src.core.interfaces`.

This module was a byte-for-byte copy of ``src/core/interfaces.py``. The
canonical module is ``src.core.interfaces``; this path re-exports it so the
existing ``from src.analysis.core.interfaces import ...`` import keeps working
without carrying a second definition that can drift.
"""

from ...core.interfaces import (  # noqa: F401
    IConflictDetector,
    IConstitutionalAnalyzer,
    IResolutionEngine,
    IResolutionStrategy,
    IValidator,
)

__all__ = [
    "IConflictDetector",
    "IConstitutionalAnalyzer",
    "IResolutionEngine",
    "IResolutionStrategy",
    "IValidator",
]
