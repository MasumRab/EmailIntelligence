"""Agent Context Control - Automatic context isolation for AI agents.

This package provides automatic detection of branch environments and
provides appropriate context isolation to prevent contamination between
different development contexts (scientific, main, orchestration-tools).
"""

from .core import ContextController
from .environment import detect_branch, get_current_branch, is_git_repository
from .validation import ContextValidator
from .models import ContextProfile, AgentContext, ContextValidationResult, ProjectConfig
from .config import get_current_config
from .exceptions import (
    ContextNotFoundError,
    ContextValidationError,
    EnvironmentDetectionError,
)

__version__ = "1.0.0"
__all__ = [
    "ContextController",
    "detect_branch",
    "get_current_branch",
    "is_git_repository",
    "ContextValidator",
    "ContextProfile",
    "AgentContext",
    "ContextValidationResult",
    "ProjectConfig",
    "get_current_config",
    "ContextNotFoundError",
    "ContextValidationError",
    "EnvironmentDetectionError",
]
