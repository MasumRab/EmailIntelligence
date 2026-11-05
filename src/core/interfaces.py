"""
Core interfaces for EmailIntelligence CLI

This module defines the abstract base classes (contracts) for the core components
of the system. All implementations must adhere to these interfaces.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .conflict_models import (
    Conflict,
    AnalysisResult,
    ResolutionStrategy,
    ValidationResult,
    ResolutionPlan,
)


class IConflictDetector(ABC):
    """
    Interface for conflict detection components.
    Responsible for identifying conflicts between git branches or PRs.
    """

    @abstractmethod
    async def detect_conflicts(self, pr_id: str, target_branch: str) -> List[Conflict]:
        """
        Detect conflicts between a PR and a target branch.

        Args:
            pr_id: The pull request ID to analyze
            target_branch: The target branch to compare against

        Returns:
            List of detected conflicts
        """


class IConstitutionalAnalyzer(ABC):
    """
    Interface for constitutional analysis components.
    Responsible for checking code against constitutional rules.
    """

    @abstractmethod
    async def analyze_constitutional_compliance(
        self, code: str, context: Dict[str, Any]
    ) -> AnalysisResult:
        """
        Analyze code for constitutional compliance.

        Args:
            code: The code to analyze
            context: Additional context for the analysis

        Returns:
            Analysis result with compliance information
        """


class IResolutionStrategy(ABC):
    """
    Interface for resolution strategy components.
    Responsible for determining how to resolve conflicts.
    """

    @abstractmethod
    async def generate_resolution_strategy(
        self, conflicts: List[Conflict]
    ) -> ResolutionStrategy:
        """
        Generate a resolution strategy for the given conflicts.

        Args:
            conflicts: List of conflicts to resolve

        Returns:
            Resolution strategy
        """


class IValidator(ABC):
    """
    Interface for validation components.
    Responsible for validating code and configurations.
    """

    @abstractmethod
    async def validate(
        self, target: Any, context: Dict[str, Any] = None
    ) -> ValidationResult:
        """
        Validate the target object.

        Args:
            target: The object to validate
            context: Additional context for validation

        Returns:
            Validation result
        """


class IResolutionEngine(ABC):
    """
    Interface for resolution engine components.
    Orchestrates the entire conflict resolution process.
    """

    @abstractmethod
    async def execute_resolution(self, plan: ResolutionPlan) -> Dict[str, Any]:
        """
        Execute a resolution plan.

        Args:
            plan: The resolution plan to execute

        Returns:
            Execution results
        """


class MetadataStore(ABC):
    """
    Interface for metadata storage components.
    Responsible for storing and retrieving metadata.
    """

    @abstractmethod
    async def save_conflict(self, conflict: Conflict) -> str:
        """Save conflict metadata"""
        pass

    @abstractmethod
    async def get_conflict(self, conflict_id: str) -> Optional[Conflict]:
        """Retrieve conflict metadata"""
        pass

    @abstractmethod
    async def save_analysis(self, analysis: AnalysisResult) -> str:
        """Save analysis result"""
        pass

    @abstractmethod
    async def get_analysis(self, conflict_id: str) -> Optional[AnalysisResult]:
        """Retrieve analysis result"""
        pass
