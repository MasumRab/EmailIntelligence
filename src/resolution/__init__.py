"""
Intelligent Conflict Resolution Engine for PR Resolution Automation System

Available modules:
- ConstitutionalEngine: Constitutional validation
- StrategyGenerator: AI-powered strategy generation (requires OpenAI)
- PromptEngine: Prompt engineering for AI
- Data models: MergeConflict, ResolutionStrategy, etc.
"""

# ===== EXISTING MODULES =====
from .strategies import StrategyGenerator
from .prompts import PromptEngine
from .constitutional_engine import ConstitutionalEngine
from .types import (
    # Enums
    ConflictTypeExtended,
    RiskLevel,
    ExecutionStatus,
    ValidationStatus,
    # Models
    CodeChange,
    ResolutionStep,
    ResolutionStrategy,
    ValidationResult,
    QualityMetrics,
    ResolutionPlan,
    # Conflict types (imported from models.graph_entities)
    MergeConflict,
    DependencyConflict,
    ArchitectureViolation,
    SemanticConflict,
    ResourceConflict,
)

# ===== MISSING MODULES (commented out) =====
# TODO: Implement these modules or remove from API
# from .engine import ResolutionEngine
# from .generation import CodeChangeGenerator
# from .validation import ValidationFramework
# from .execution import ExecutionEngine
# from .workflows import WorkflowOrchestrator
# from .metrics import QualityMetrics  # Note: Model exists in types.py
# from .queue import ResolutionQueue

__all__ = [
    # Available classes
    "StrategyGenerator",
    "PromptEngine",
    "ConstitutionalEngine",
    # Enums
    "ConflictTypeExtended",
    "RiskLevel",
    "ExecutionStatus",
    "ValidationStatus",
    # Models
    "CodeChange",
    "ResolutionStep",
    "ResolutionStrategy",
    "ValidationResult",
    "QualityMetrics",
    "ResolutionPlan",
    # Conflict types
    "MergeConflict",
    "DependencyConflict",
    "ArchitectureViolation",
    "SemanticConflict",
    "ResourceConflict",
]
