#!/usr/bin/env python3
"""
EmailIntelligence CLI - AI-powered git worktree-based conflict resolution tool

This module is now a backward-compatible wrapper around the new modular cli package.
For new code, import directly from cli:
    from cli import EmailIntelligenceCLI

This file maintains backward compatibility for existing scripts.
"""

# Backward compatibility imports - import from new modular structure
from cli import (
    # Main class
    EmailIntelligenceCLI,
    # Exceptions
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
    # Models
    ConflictType,
    ConflictSeverity,
    ConflictRegion,
    ConflictFile,
    ConflictReport,
    BranchPairResult,
    ConflictMatrix,
    # Workspace managers
    GitWorkspaceManager,
    GitWorktreeManager,
    FallbackWorkspaceManager,
    RobustWorkspaceManager,
    # Conflict detector
    ConflictDetector,
    # Entry point
    main,
)


# For backward compatibility, provide a simple main() that works with the new structure
def main():
    """Main CLI entry point - now delegates to cli.main.main()"""
    from cli.main import main as cli_main
    cli_main()


if __name__ == "__main__":
    main()
