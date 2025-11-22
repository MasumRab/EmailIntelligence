"""
Intelligent Conflict Resolution Engine for PR Resolution Automation System

This module provides conflict resolution capabilities including:
- Constitutional validation (ConstitutionalEngine)
- AI-powered strategy generation with OpenAI (StrategyGenerator)
- Prompt engineering for AI (PromptEngine)
- Data models for conflicts and resolutions (types)

Note: Some modules mentioned in original design are not yet implemented.
      See PHASE_0_SETUP.md for details on missing modules.
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

# ===== MISSING MODULES (not yet implemented) =====
# TODO: Implement these modules or remove from API
# from .engine import ResolutionEngine
# from .generation import CodeChangeGenerator
# from .validation import ValidationFramework  # Use src.validation instead
# from .execution import ExecutionEngine
# from .workflows import WorkflowOrchestrator
# from .metrics import QualityMetrics  # Model exists in types.py, implementation missing
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
