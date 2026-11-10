"""
Project Configuration System

This module provides a centralized configuration system for the EmailIntelligence project
structure, allowing paths and components to be defined dynamically rather than hardcoded.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class ProjectPaths:
    """Configuration for project directory structure."""
    root: Path

    # Core directories
    backend: Path = field(init=False)
    client: Path = field(init=False)
    shared: Path = field(init=False)
    tests: Path = field(init=False)
    models: Path = field(init=False)
    setup: Path = field(init=False)

    # Backend subdirectories
    python_backend: Path = field(init=False)
    python_nlp: Path = field(init=False)
    server_ts: Path = field(init=False)

    def __post_init__(self):
        """Initialize derived paths."""
        self.backend = self.root / "src" / "backend"
        self.client = self.root / "src" / "client"
        self.shared = self.root / "src" / "shared"
        self.tests = self.root / "tests"
        self.models = self.root / "models"
        self.setup = self.root / "scripts" / "automation" / "setup"

        # Backend subdirectories
        self.python_backend = self.backend / "python_backend"
        self.python_nlp = self.backend / "python_nlp"
        self.server_ts = self.backend / "server-ts"


class ProjectConfig:
    """Main project configuration class."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or self._find_project_root()
        self.paths = ProjectPaths(self.root_dir)

    def _find_project_root(self) -> Path:
        """Find the project root directory."""
        current = Path(__file__).resolve().parent
        while current.parent != current:
            if (current / "README.md").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()

# Global configuration instance
_project_config = None

def get_project_config():
    """Get the project configuration."""
    global _project_config
    if _project_config is None:
        _project_config = ProjectConfig()
    return _project_config
