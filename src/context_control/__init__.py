"""Agent Context Control - Automatic context isolation for AI agents.

This package provides automatic detection of branch environments and
provides appropriate context isolation to prevent contamination between
different development contexts (scientific, main, orchestration-tools).
"""

from .config import get_current_config, init_config
from .core import ContextController
from .environment import detect_branch, get_current_branch, is_git_repository
from .exceptions import (ContextNotFoundError, ContextValidationError,
                         EnvironmentDetectionError)
from .models import (AgentContext, ContextProfile, ContextValidationResult,
                     ProjectConfig)
from .validation import ContextValidator

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
    "init_config",
    "ContextNotFoundError",
    "ContextValidationError",
    "EnvironmentDetectionError",
]
