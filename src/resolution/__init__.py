"""
Intelligent Conflict Resolution Engine for PR Resolution Automation System

This module provides AI-powered conflict resolution capabilities including:
- Resolution strategy generation with OpenAI
- Code change generation and intelligent merging
- Validation and testing framework
- Human-in-the-loop validation
- Resolution execution with rollback mechanisms
- Workflow orchestration and queue management
"""

from .engine import ResolutionEngine
from .strategies import StrategyGenerator
from .generation import CodeChangeGenerator
from .validation import ValidationFramework
from .execution import ExecutionEngine
from .workflows import WorkflowOrchestrator
from .prompts import PromptEngine
from .metrics import QualityMetrics
from .constitutional_engine import ConstitutionalEngine
from .types import (
    MergeConflict,
    DependencyConflict,
    ArchitectureViolation,
    SemanticConflict,
    ResourceConflict,
    ResolutionPlan,
)
from .queue import ResolutionQueue

__all__ = [
    "ResolutionEngine",
    "StrategyGenerator",
    "CodeChangeGenerator",
    "ValidationFramework",
    "ExecutionEngine",
    "WorkflowOrchestrator",
    "PromptEngine",
    "QualityMetrics",
    "ConstitutionalEngine",
    "MergeConflict",
    "DependencyConflict",
    "ArchitectureViolation",
    "SemanticConflict",
    "ResourceConflict",
    "ResolutionPlan",
    "ResolutionQueue",
]
