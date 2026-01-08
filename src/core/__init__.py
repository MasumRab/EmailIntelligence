"""
Core module initialization
"""

from .interfaces import (
    IConflictDetector,
    IConstitutionalAnalyzer,
    IResolutionStrategy,
    IValidator,
    IResolutionEngine,
)

from .conflict_models import (
    Conflict,
    ConflictBlock,
    AnalysisResult,
)

from .config import settings, Settings
from .exceptions import (
    EmailIntelligenceError,
    ConflictDetectionError,
    AnalysisError,
    StrategyGenerationError,
    ResolutionError,
    ValidationError,
    DatabaseError,
    GitOperationError,
    StorageError,
)

__all__ = [
    # Interfaces
    "IConflictDetector",
    "IConstitutionalAnalyzer",
    "IResolutionStrategy",
    "IValidator",
    "IResolutionEngine",
    # Models
    "Conflict",
    "ConflictBlock",
    "AnalysisResult",
    # Config
    "settings",
    "Settings",
    # Exceptions
    "EmailIntelligenceError",
    "ConflictDetectionError",
    "AnalysisError",
    "StrategyGenerationError",
    "ResolutionError",
    "ValidationError",
    "DatabaseError",
    "GitOperationError",
    "StorageError",
]
