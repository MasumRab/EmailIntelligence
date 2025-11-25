"""
Core module initialization
"""

from .interfaces import (
    IConflictDetector,
    IConstitutionalAnalyzer,
    IStrategyGenerator,
    IConflictResolver,
    IValidator,
    IMetadataStore,
)

from .models import (
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
)

__all__ = [
    # Interfaces
    "IConflictDetector",
    "IConstitutionalAnalyzer",
    "IStrategyGenerator",
    "IConflictResolver",
    "IValidator",
    "IMetadataStore",
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
]
