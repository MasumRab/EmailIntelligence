# API Contracts: Agent Context Control

**Date**: 2025-11-10 | **Spec**: specs/001-agent-context-control/spec.md | **Data Models**: specs/001-agent-context-control/data-model.md

## Overview

This document defines the API contracts and interfaces for the Agent Context Control system. All interfaces follow Python type hints and protocol patterns for clear contracts and testability.

## Core Interfaces

### ContextController Protocol

The main interface for context control operations.

```python
from typing import Protocol, Optional, Dict, Any
from pathlib import Path
from .data_model import ContextProfile, AgentContext, BranchDetectionResult

class ContextController(Protocol):
    """Protocol for context controller implementations."""

    def get_context(self) -> AgentContext:
        """
        Get the current agent context based on branch/environment detection.

        Returns:
            AgentContext: Current context for the agent

        Raises:
            BranchDetectionError: If branch detection fails
            ContextValidationError: If context validation fails
            ContextIsolationError: If context isolation fails
        """
        ...

    def get_context_for_branch(self, branch: str) -> AgentContext:
        """
        Get context for a specific branch (for testing/debugging).

        Args:
            branch: Branch name to get context for

        Returns:
            AgentContext: Context for the specified branch
        """
        ...

    def validate_context(self, context_id: str) -> bool:
        """
        Validate a context profile.

        Args:
            context_id: Context identifier to validate

        Returns:
            bool: True if context is valid

        Raises:
            ContextValidationError: If validation fails
        """
        ...

    def list_contexts(self) -> Dict[str, ContextProfile]:
        """
        List all available context profiles.

        Returns:
            Dict[str, ContextProfile]: Mapping of context IDs to profiles
        """
        ...

    def reload_contexts(self) -> None:
        """
        Reload all context profiles from disk (clears cache).
        """
        ...

    @property
    def current_branch(self) -> Optional[str]:
        """Get the currently detected branch name."""
        ...

    @property
    def context_dir(self) -> Path:
        """Get the context directory path."""
        ...
```

### BranchDetector Protocol

Interface for branch detection implementations.

```python
class BranchDetector(Protocol):
    """Protocol for branch detection implementations."""

    def detect_branch(self, repo_path: str) -> BranchDetectionResult:
        """
        Detect the current branch and context information.

        Args:
            repo_path: Path to the git repository

        Returns:
            BranchDetectionResult: Detection results

        Raises:
            BranchDetectionError: If detection fails
        """
        ...

    def is_git_repository(self, path: str) -> bool:
        """
        Check if a path is a git repository.

        Args:
            path: Path to check

        Returns:
            bool: True if path is a git repository
        """
        ...
```

### ContextStorage Protocol

Interface for context profile storage.

```python
class ContextStorage(Protocol):
    """Protocol for context storage implementations."""

    def load_context(self, context_id: str) -> ContextProfile:
        """
        Load a context profile by ID.

        Args:
            context_id: Context identifier

        Returns:
            ContextProfile: Loaded context profile

        Raises:
            FileNotFoundError: If context file doesn't exist
            ContextValidationError: If context is invalid
        """
        ...

    def save_context(self, profile: ContextProfile) -> None:
        """
        Save a context profile.

        Args:
            profile: Context profile to save

        Raises:
            ContextIsolationError: If save operation fails
        """
        ...

    def list_contexts(self) -> Dict[str, ContextProfile]:
        """
        List all available context profiles.

        Returns:
            Dict[str, ContextProfile]: Context ID to profile mapping
        """
        ...

    def delete_context(self, context_id: str) -> None:
        """
        Delete a context profile.

        Args:
            context_id: Context identifier to delete

        Raises:
            FileNotFoundError: If context doesn't exist
            ContextIsolationError: If deletion fails
        """
        ...
```

### ContextValidator Protocol

Interface for context validation.

```python
from .data_model import ContextValidationResult

class ContextValidator(Protocol):
    """Protocol for context validation implementations."""

    def validate_profile(self, profile: ContextProfile) -> ContextValidationResult:
        """
        Validate a context profile.

        Args:
            profile: Profile to validate

        Returns:
            ContextValidationResult: Validation results
        """
        ...

    def validate_context_id(self, context_id: str) -> bool:
        """
        Validate a context ID format.

        Args:
            context_id: Context ID to validate

        Returns:
            bool: True if valid
        """
        ...

    def validate_branch_name(self, branch: str) -> bool:
        """
        Validate a branch name format.

        Args:
            branch: Branch name to validate

        Returns:
            bool: True if valid
        """
        ...
```

## Implementation Classes

### DefaultContextController

Reference implementation of the ContextController protocol.

```python
from typing import Optional, Dict
from pathlib import Path
import logging

from .data_model import ContextProfile, AgentContext, ContextControlConfig
from .interfaces import ContextController, BranchDetector, ContextStorage, ContextValidator

logger = logging.getLogger(__name__)

class DefaultContextController(ContextController):
    """Default implementation of ContextController."""

    def __init__(
        self,
        config: Optional[ContextControlConfig] = None,
        branch_detector: Optional[BranchDetector] = None,
        storage: Optional[ContextStorage] = None,
        validator: Optional[ContextValidator] = None
    ):
        """
        Initialize the context controller.

        Args:
            config: Configuration object
            branch_detector: Branch detection implementation
            storage: Context storage implementation
            validator: Context validation implementation
        """
        self.config = config or ContextControlConfig()
        self.branch_detector = branch_detector or GitBranchDetector()
        self.storage = storage or FileContextStorage(self.config.context_dir)
        self.validator = validator or SchemaContextValidator()

        # Initialize cache
        self._context_cache: Dict[str, AgentContext] = {}
        self._branch_cache: Optional[str] = None

    def get_context(self) -> AgentContext:
        """Get current context based on branch detection."""
        # Check cache first
        if self.config.cache_enabled and self._branch_cache:
            cached = self._context_cache.get(self._branch_cache)
            if cached:
                return cached

        # Detect current branch
        detection_result = self.branch_detector.detect_branch(".")

        # Load and validate context
        profile = self.storage.load_context(detection_result.context_id)
        validation = self.validator.validate_profile(profile)

        if not validation.is_valid:
            errors = [e.message for e in validation.errors]
            raise ContextValidationError(
                f"Context validation failed: {', '.join(errors)}",
                "VALIDATION_FAILED",
                {"errors": validation.errors}
            )

        # Create agent context
        context = self._create_agent_context(profile, detection_result)

        # Cache result
        if self.config.cache_enabled:
            self._context_cache[detection_result.context_id] = context
            self._branch_cache = detection_result.context_id

        logger.info(f"Loaded context: {context.context_id}")
        return context

    def get_context_for_branch(self, branch: str) -> AgentContext:
        """Get context for specific branch."""
        # Create mock detection result
        detection_result = BranchDetectionResult(
            branch_name=branch,
            commit_hash=None,
            is_detached=False,
            context_id=branch,
            detection_method="manual",
            detection_timestamp=datetime.now().isoformat(),
            repository_path="."
        )

        # Load context
        profile = self.storage.load_context(branch)
        context = self._create_agent_context(profile, detection_result)

        return context

    def validate_context(self, context_id: str) -> bool:
        """Validate a context profile."""
        try:
            profile = self.storage.load_context(context_id)
            validation = self.validator.validate_profile(profile)
            return validation.is_valid
        except Exception:
            return False

    def list_contexts(self) -> Dict[str, ContextProfile]:
        """List all available contexts."""
        return self.storage.list_contexts()

    def reload_contexts(self) -> None:
        """Reload contexts from disk."""
        self._context_cache.clear()
        self._branch_cache = None
        self.storage.reload()

    @property
    def current_branch(self) -> Optional[str]:
        """Get current branch."""
        if not self._branch_cache:
            try:
                result = self.branch_detector.detect_branch(".")
                self._branch_cache = result.branch_name
            except Exception:
                return None
        return self._branch_cache

    @property
    def context_dir(self) -> Path:
        """Get context directory."""
        return self.config.context_dir

    def _create_agent_context(
        self,
        profile: ContextProfile,
        detection: BranchDetectionResult
    ) -> AgentContext:
        """Create AgentContext from profile and detection result."""
        # Extract agent config with defaults
        agent_config = profile.agent_config or {}

        context = AgentContext(
            context_id=profile.context_id,
            environment=profile.environment,
            max_concurrent_tasks=agent_config.get("max_concurrent_tasks", 5),
            timeout_seconds=agent_config.get("timeout_seconds", 300),
            memory_limit_mb=agent_config.get("memory_limit_mb", 1024),
            feature_flags=profile.feature_flags or {},
            env_vars={},  # Populated separately for security
            branch_info={
                "branch_name": detection.branch_name,
                "commit_hash": detection.commit_hash,
                "is_detached": detection.is_detached,
                "detection_method": detection.detection_method
            },
            created_at=datetime.now().isoformat()
        )

        return context
```

### GitBranchDetector

Git-based branch detection implementation.

```python
import os
from pathlib import Path
from git import Repo, GitCommandError
from datetime import datetime

from .data_model import BranchDetectionResult
from .interfaces import BranchDetector

class GitBranchDetector(BranchDetector):
    """Git-based branch detection implementation."""

    def detect_branch(self, repo_path: str) -> BranchDetectionResult:
        """Detect branch using GitPython."""
        repo_path = Path(repo_path).resolve()

        try:
            repo = Repo(repo_path)
        except Exception as e:
            raise BranchDetectionError(
                f"Failed to open git repository at {repo_path}: {e}",
                "REPO_OPEN_FAILED",
                {"repo_path": str(repo_path)}
            )

        # Get current branch/commit info
        is_detached = repo.head.is_detached
        commit_hash = repo.head.commit.hexsha

        if is_detached:
            branch_name = None
            context_id = f"detached-{commit_hash[:8]}"
        else:
            branch_name = repo.active_branch.name
            context_id = branch_name

        # Check for CI/CD environment variables
        ci_branch = self._get_ci_branch()
        if ci_branch:
            branch_name = ci_branch
            context_id = f"ci-{ci_branch}"

        return BranchDetectionResult(
            branch_name=branch_name,
            commit_hash=commit_hash,
            is_detached=is_detached,
            context_id=context_id,
            detection_method="git" if not ci_branch else "ci",
            detection_timestamp=datetime.now().isoformat(),
            repository_path=str(repo_path)
        )

    def is_git_repository(self, path: str) -> bool:
        """Check if path is a git repository."""
        git_dir = Path(path) / ".git"
        return git_dir.exists() and git_dir.is_dir()

    def _get_ci_branch(self) -> Optional[str]:
        """Get branch name from CI/CD environment variables."""
        # Common CI/CD environment variables
        ci_vars = [
            "CI_COMMIT_REF_NAME",  # GitLab
            "GITHUB_HEAD_REF",     # GitHub Actions
            "CIRCLE_BRANCH",       # CircleCI
            "TRAVIS_BRANCH",       # Travis CI
            "BUILDKITE_BRANCH",    # Buildkite
            "CI_BRANCH",           # Generic
        ]

        for var in ci_vars:
            branch = os.environ.get(var)
            if branch:
                return branch

        return None
```

### FileContextStorage

File-based context storage implementation.

```python
import json
import hashlib
from pathlib import Path
from typing import Dict

from .data_model import ContextProfile, ContextFile
from .interfaces import ContextStorage

class FileContextStorage(ContextStorage):
    """File-based context storage implementation."""

    def __init__(self, context_dir: Path):
        """
        Initialize file storage.

        Args:
            context_dir: Directory containing context files
        """
        self.context_dir = Path(context_dir)
        self.context_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, ContextFile] = {}

    def load_context(self, context_id: str) -> ContextProfile:
        """Load context from JSON file."""
        if context_id in self._cache:
            return self._cache[context_id].profile

        file_path = self.context_dir / f"{context_id}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Context file not found: {file_path}")

        context_file = ContextFile.from_file(file_path)
        self._cache[context_id] = context_file

        return context_file.profile

    def save_context(self, profile: ContextProfile) -> None:
        """Save context to JSON file."""
        file_path = self.context_dir / f"{profile.context_id}.json"

        # Create backup if file exists
        if file_path.exists():
            backup_path = file_path.with_suffix('.json.backup')
            file_path.rename(backup_path)

        try:
            # Write new file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(profile.dict(), f, indent=2, ensure_ascii=False)

            # Remove backup on success
            if backup_path.exists():
                backup_path.unlink()

            # Invalidate cache
            self._cache.pop(profile.context_id, None)

        except Exception as e:
            # Restore backup on failure
            if backup_path.exists():
                backup_path.rename(file_path)
            raise ContextIsolationError(
                f"Failed to save context {profile.context_id}: {e}",
                "SAVE_FAILED",
                {"context_id": profile.context_id}
            )

    def list_contexts(self) -> Dict[str, ContextProfile]:
        """List all context files."""
        contexts = {}

        for file_path in self.context_dir.glob("*.json"):
            if file_path.name.endswith('.backup'):
                continue

            try:
                context_id = file_path.stem
                profile = self.load_context(context_id)
                contexts[context_id] = profile
            except Exception:
                # Skip invalid files
                continue

        return contexts

    def delete_context(self, context_id: str) -> None:
        """Delete context file."""
        file_path = self.context_dir / f"{context_id}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Context file not found: {file_path}")

        file_path.unlink()
        self._cache.pop(context_id, None)

    def reload(self) -> None:
        """Reload cache from disk."""
        self._cache.clear()
```

## CLI Interface Contract

### Command Line Interface

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class CLICommand(ABC):
    """Base class for CLI commands."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Command name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Command description."""
        ...

    @abstractmethod
    def execute(self, args: List[str]) -> int:
        """
        Execute the command.

        Args:
            args: Command arguments

        Returns:
            int: Exit code (0 for success)
        """
        ...

class ContextControlCLI:
    """Main CLI interface."""

    def __init__(self, controller: ContextController):
        """Initialize CLI with context controller."""
        self.controller = controller
        self.commands: Dict[str, CLICommand] = {}

    def register_command(self, command: CLICommand) -> None:
        """Register a CLI command."""
        self.commands[command.name] = command

    def execute(self, args: List[str]) -> int:
        """Execute CLI command."""
        if not args:
            self._show_help()
            return 0

        command_name = args[0]
        command_args = args[1:]

        if command_name in ['help', '-h', '--help']:
            self._show_help()
            return 0

        command = self.commands.get(command_name)
        if not command:
            print(f"Unknown command: {command_name}")
            self._show_help()
            return 1

        try:
            return command.execute(command_args)
        except Exception as e:
            print(f"Error executing command {command_name}: {e}")
            return 1

    def _show_help(self) -> None:
        """Show help information."""
        print("Agent Context Control CLI")
        print()
        print("Available commands:")
        for name, command in self.commands.items():
            print(f"  {name:<15} {command.description}")
        print()
        print("Use 'command --help' for command-specific help.")
```

## Error Handling Contracts

### Exception Hierarchy

```python
class ContextControlException(Exception):
    """Base exception for context control operations."""

    def __init__(self, message: str, error_code: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}

class BranchDetectionException(ContextControlException):
    """Branch detection related errors."""
    pass

class ContextValidationException(ContextControlException):
    """Context validation related errors."""
    pass

class ContextIsolationException(ContextControlException):
    """Context isolation related errors."""
    pass

class ConfigurationException(ContextControlException):
    """Configuration related errors."""
    pass
```

## Testing Contracts

### Mock Implementations

```python
from .interfaces import ContextController, BranchDetector, ContextStorage

class MockBranchDetector(BranchDetector):
    """Mock branch detector for testing."""

    def __init__(self, branch_name: str = "main"):
        self.branch_name = branch_name

    def detect_branch(self, repo_path: str) -> BranchDetectionResult:
        return BranchDetectionResult(
            branch_name=self.branch_name,
            commit_hash="abc123",
            is_detached=False,
            context_id=self.branch_name,
            detection_method="mock",
            detection_timestamp="2023-01-01T00:00:00Z",
            repository_path=repo_path
        )

    def is_git_repository(self, path: str) -> bool:
        return True

class MockContextStorage(ContextStorage):
    """Mock context storage for testing."""

    def __init__(self, contexts: Optional[Dict[str, ContextProfile]] = None):
        self.contexts = contexts or {}

    def load_context(self, context_id: str) -> ContextProfile:
        if context_id not in self.contexts:
            raise FileNotFoundError(f"Mock context not found: {context_id}")
        return self.contexts[context_id]

    def save_context(self, profile: ContextProfile) -> None:
        self.contexts[profile.context_id] = profile

    def list_contexts(self) -> Dict[str, ContextProfile]:
        return self.contexts.copy()

    def delete_context(self, context_id: str) -> None:
        if context_id not in self.contexts:
            raise FileNotFoundError(f"Mock context not found: {context_id}")
        del self.contexts[context_id]

    def reload(self) -> None:
        pass  # No-op for mock
```

## Performance Contracts

### Performance Requirements

```python
from typing import Callable
import time

def measure_performance(func: Callable, iterations: int = 100) -> Dict[str, float]:
    """
    Measure function performance.

    Args:
        func: Function to measure
        iterations: Number of iterations to run

    Returns:
        Dict with performance metrics
    """
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds

    return {
        "avg_ms": sum(times) / len(times),
        "min_ms": min(times),
        "max_ms": max(times),
        "p95_ms": sorted(times)[int(len(times) * 0.95)]
    }

# Performance contracts
CONTEXT_LOAD_TIME_MS = 500  # Maximum context load time
BRANCH_DETECTION_TIME_MS = 100  # Maximum branch detection time
CONTEXT_VALIDATION_TIME_MS = 50  # Maximum validation time
```

## Security Contracts

### Security Requirements

```python
class SecurityValidator:
    """Security validation for context operations."""

    @staticmethod
    def validate_file_access(file_path: Path, operation: str) -> None:
        """
        Validate file access permissions.

        Args:
            file_path: Path to validate
            operation: Operation being performed

        Raises:
            SecurityException: If access is not allowed
        """
        # Implementation would check file permissions,
        # ownership, and path traversal attacks
        pass

    @staticmethod
    def validate_context_isolation(
        context_id: str,
        requesting_agent: str,
        allowed_contexts: List[str]
    ) -> None:
        """
        Validate context isolation.

        Args:
            context_id: Context being accessed
            requesting_agent: Agent requesting access
            allowed_contexts: Contexts agent is allowed to access

        Raises:
            SecurityException: If access is not allowed
        """
        if context_id not in allowed_contexts:
            raise SecurityException(
                f"Agent {requesting_agent} not allowed to access context {context_id}",
                "ACCESS_DENIED"
            )
```

This completes the API contracts specification. The interfaces provide clear contracts for implementation while allowing flexibility in the underlying implementations.