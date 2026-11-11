"""
EmailIntelligence CLI Package

This package contains the modularized EmailIntelligence CLI implementation.
"""

# Version
__version__ = "1.0.0"

# Import main components from new modular structure
from .core import (
    EmailIntelligenceCLIBase,
    WorkflowOrchestrator,
    ConflictResolver,
    BranchManager,
    WorkspaceManager,
    GitOperations,
    ConfigManager,
    ConstitutionalAnalyzer,
    StrategyGenerator,
    ContentAligner,
    Validator,
    ResolutionManager,
)

# Import exceptions
from .exceptions import (
    EmailIntelligenceError,
    GitOperationError,
    MergeTreeError,
    BranchNotFoundError,
    WorktreeUnavailableError,
    ConflictDetectionError,
    WorkspaceCreationError,
    ResolutionNotReadyError,
    PushOperationError,
    BranchEnumerationError,
    ScanExecutionError,
)

# Import models
from .models import (
    ConflictType,
    ConflictSeverity,
    ConflictRegion,
    ConflictFile,
    ConflictReport,
    BranchPairResult,
    ConflictMatrix,
)

# Import workspace managers
from .workspace import (
    GitWorkspaceManager,
    GitWorktreeManager,
    FallbackWorkspaceManager,
    RobustWorkspaceManager,
)

# Import conflict detector
from .conflict import ConflictDetector

# Import commands
from .commands import (
    BaseCommand,
    ConflictCommands,
    BranchCommands,
    WorkspaceCommands,
    AnalysisCommands,
    AlignmentCommands,
    ValidationCommands,
    ResolutionCommands,
    ConstitutionalCommands,
    StrategyCommands,
)

# Import main entry point
from .main import main

# Convenience alias for CLI entry point
__all__ = [
    # Package info
    '__version__',
    # Core classes
    'EmailIntelligenceCLIBase',
    'WorkflowOrchestrator',
    'ConflictResolver',
    'BranchManager',
    'WorkspaceManager',
    'GitOperations',
    'ConfigManager',
    'ConstitutionalAnalyzer',
    'StrategyGenerator',
    'ContentAligner',
    'Validator',
    'ResolutionManager',
    # Exceptions
    'EmailIntelligenceError',
    'GitOperationError',
    'MergeTreeError',
    'BranchNotFoundError',
    'WorktreeUnavailableError',
    'ConflictDetectionError',
    'WorkspaceCreationError',
    'ResolutionNotReadyError',
    'PushOperationError',
    'BranchEnumerationError',
    'ScanExecutionError',
    # Models
    'ConflictType',
    'ConflictSeverity',
    'ConflictRegion',
    'ConflictFile',
    'ConflictReport',
    'BranchPairResult',
    'ConflictMatrix',
    # Workspace
    'GitWorkspaceManager',
    'GitWorktreeManager',
    'FallbackWorkspaceManager',
    'RobustWorkspaceManager',
    # Conflict detection
    'ConflictDetector',
    # Commands
    'BaseCommand',
    'ConflictCommands',
    'BranchCommands',
    'WorkspaceCommands',
    'AnalysisCommands',
    'AlignmentCommands',
    'ValidationCommands',
    'ResolutionCommands',
    'ConstitutionalCommands',
    'StrategyCommands',
    # Entry point
    'main',
]
