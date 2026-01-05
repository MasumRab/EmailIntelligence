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
            pr_id: ID of the Pull Request
            target_branch: Name of the target branch (e.g., 'main')

        Returns:
            List of detected Conflict objects
        """
        pass

    @abstractmethod
    async def detect_conflicts_between_branches(
        self, source_branch: str, target_branch: str
    ) -> List[Conflict]:
        """
        Detect conflicts between two specific branches.

        Args:
            source_branch: Name of the source branch
            target_branch: Name of the target branch

        Returns:
            List of detected Conflict objects
        """
        pass


class IConstitutionalAnalyzer(ABC):
    """
    Interface for constitutional analysis components.
    Responsible for checking code against constitutional rules and requirements.
    """

    @abstractmethod
    async def analyze(self, conflict: Conflict, context: Dict[str, Any] = None) -> AnalysisResult:
        """
        Analyze a conflict against constitutional rules.

        Args:
            conflict: The conflict to analyze
            context: Optional additional context

        Returns:
            AnalysisResult containing findings and metrics
        """
        pass

    @abstractmethod
    async def validate_code_change(self, code: str, rules: List[str] = None) -> Dict[str, Any]:
        """
        Validate a specific code snippet against rules.

        Args:
            code: The code content to validate
            rules: Optional list of specific rules to check

        Returns:
            Dictionary of validation results
        """
        pass


class IStrategyGenerator(ABC):
    """
    Interface for strategy generation components.
    Responsible for generating resolution strategies for conflicts.
    """

    @abstractmethod
    async def generate_strategies(
        self,
        conflict: Conflict,
        analysis: AnalysisResult,
        context: Dict[str, Any] = None,
    ) -> List[ResolutionStrategy]:
        """
        Generate potential resolution strategies for a conflict.

        Args:
            conflict: The conflict to resolve
            analysis: The analysis result for the conflict
            context: Optional additional context

        Returns:
            List of proposed ResolutionStrategy objects
        """
        pass


class IConflictResolver(ABC):
    """
    Interface for conflict resolution components.
    Responsible for executing resolution strategies.
    """

    @abstractmethod
    async def resolve(self, conflict: Conflict, strategy: ResolutionStrategy) -> ResolutionPlan:
        """
        Create a resolution plan based on a strategy.

        Args:
            conflict: The conflict to resolve
            strategy: The selected resolution strategy

        Returns:
            ResolutionPlan containing specific steps and code changes
        """
        pass

    @abstractmethod
    async def execute_plan(self, plan: ResolutionPlan) -> bool:
        """
        Execute a resolution plan.

        Args:
            plan: The plan to execute

        Returns:
            True if execution was successful, False otherwise
        """
        pass


class IValidator(ABC):
    """
    Interface for validation components.
    Responsible for validating resolutions (tests, linting, security).
    """

    @abstractmethod
    async def validate(self, context: Dict[str, Any]) -> ValidationResult:
        """
        Perform validation on the current state.

        Args:
            context: Context containing paths, IDs, etc.

        Returns:
            ValidationResult containing status and details
        """
        pass


class IMetadataStore(ABC):
    """
    Interface for metadata storage components.
    Responsible for persisting analysis and resolution data.
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
