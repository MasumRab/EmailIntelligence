"""
EmailIntelligence CLI Package

This package contains the modularized EmailIntelligence CLI implementation.
"""

# Version
__version__ = "1.0.0"

# Import main components for easy access
from cli.cli_class import EmailIntelligenceCLI

# Import exceptions
from cli.exceptions import (
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
from cli.models import (
    ConflictType,
    ConflictSeverity,
    ConflictRegion,
    ConflictFile,
    ConflictReport,
    BranchPairResult,
    ConflictMatrix,
)

# Import workspace managers
from cli.workspace import (
    GitWorkspaceManager,
    GitWorktreeManager,
    FallbackWorkspaceManager,
    RobustWorkspaceManager,
)

# Import conflict detector
from cli.conflict import ConflictDetector

# Import commands
from cli.commands import create_parser, execute_command

# Import main entry point
from cli.main import main

# Convenience alias for CLI entry point
__all__ = [
    # Package info
    '__version__',
    # Main class
    'EmailIntelligenceCLI',
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
    'create_parser',
    'execute_command',
    # Entry point
    'main',
]
