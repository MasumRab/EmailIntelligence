"""
<<<<<<< HEAD
Project Configuration System

This module provides a centralized configuration system for the EmailIntelligence project
structure, allowing paths and components to be defined dynamically rather than hardcoded.
This prevents issues during major refactors when file locations change.
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
        self.backend = self.root / "backend"
        self.client = self.root / "client"
        self.shared = self.root / "shared"
        self.tests = self.root / "tests"
        self.models = self.root / "models"
        self.setup = self.root / "setup"

        # Backend subdirectories
        self.python_backend = self.backend / "python_backend"
        self.python_nlp = self.backend / "python_nlp"
        self.server_ts = self.backend / "server-ts"


@dataclass
class ProjectComponents:
    """Configuration for project components and their locations."""

    # Required directories (must exist)
    required_dirs: Set[str] = field(default_factory=lambda: {
        "backend", "client", "shared", "tests"
    })

    # Required files (must exist in root)
    required_files: Set[str] = field(default_factory=lambda: {
        "pyproject.toml", "README.md", "requirements.txt"
    })

    # Critical files to check for merge conflicts (Python backend files)
    critical_backend_files: Set[str] = field(default_factory=lambda: {
        "main.py", "database.py", "email_routes.py", "category_routes.py",
        "gmail_routes.py", "filter_routes.py", "action_routes.py",
        "dashboard_routes.py", "workflow_routes.py", "performance_monitor.py"
    })

    # Critical NLP files
    critical_nlp_files: Set[str] = field(default_factory=lambda: {
        "nlp_engine.py", "gmail_integration.py", "gmail_service.py",
        "smart_filters.py", "smart_retrieval.py", "ai_training.py"
    })

    # Service configurations
    services: Dict[str, Dict] = field(default_factory=lambda: {
        "python_backend": {
            "path": "backend/python_backend",
            "main_file": "main.py",
            "port": 8000
        },
        "typescript_backend": {
            "path": "backend/server-ts",
            "package_json": "package.json",
            "port": 8001
        },
        "frontend": {
            "path": "client",
            "package_json": "package.json",
            "port": 3000
        },
        "gradio_ui": {
            "path": "backend/python_backend",
            "main_file": "main.py",
            "port": 7860
        }
    })


class ProjectConfig:
    """Main project configuration class."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or self._find_project_root()
        self.paths = ProjectPaths(self.root_dir)
        self.components = ProjectComponents()

    def _find_project_root(self) -> Path:
        """Find the project root directory by looking for key files."""
        # Start from the directory containing this config file
        current = Path(__file__).resolve().parent.parent

        # Look for project root markers (prioritize root-level files)
        root_markers = ["README.md", ".git"]

        # First check if we're already in the right place
        if all((current / marker).exists() for marker in root_markers):
            return current

        # Look upwards
        while current.parent != current:  # Stop at filesystem root
            if all((current / marker).exists() for marker in root_markers):
                return current
            current = current.parent

        # Fallback: look for pyproject.toml at root level
        current = Path(__file__).resolve().parent.parent
        if (current / "README.md").exists():
            return current

        # Final fallback
        return Path.cwd()

    def get_critical_files(self) -> List[str]:
        """Get the complete list of critical files to check for merge conflicts."""
        critical_files = []

        # Add required files
        critical_files.extend(self.components.required_files)

        # Add backend Python files
        for file in self.components.critical_backend_files:
            critical_files.append(f"backend/python_backend/{file}")

        # Add NLP files
        for file in self.components.critical_nlp_files:
            critical_files.append(f"backend/python_nlp/{file}")

        return critical_files

    def get_service_path(self, service_name: str) -> Optional[Path]:
        """Get the path for a specific service."""
        service_config = self.components.services.get(service_name)
        if service_config:
            return self.root_dir / service_config["path"]
        return None

    def get_service_config(self, service_name: str) -> Optional[Dict]:
        """Get the configuration for a specific service."""
        return self.components.services.get(service_name)

    def validate_structure(self) -> List[str]:
        """Validate that the project structure matches the configuration."""
        issues = []

        # Check required directories
        for dir_name in self.components.required_dirs:
            dir_path = self.root_dir / dir_name
            if not dir_path.exists():
                issues.append(f"Required directory '{dir_name}' is missing.")
            elif not dir_path.is_dir():
                issues.append(f"'{dir_name}' exists but is not a directory.")

        # Check required files
        for file_name in self.components.required_files:
            file_path = self.root_dir / file_name
            if not file_path.exists():
                issues.append(f"Required file '{file_name}' is missing.")
            elif not file_path.is_file():
                issues.append(f"'{file_name}' exists but is not a file.")

        # Check service paths
        for service_name, service_config in self.components.services.items():
            service_path = self.root_dir / service_config["path"]
            if not service_path.exists():
                issues.append(f"Service '{service_name}' path '{service_config['path']}' does not exist.")

        return issues

    def discover_services(self) -> Dict[str, Dict]:
        """Auto-discover available services based on directory structure."""
        discovered_services = {}

        # Check for Python backend
        if self.paths.python_backend.exists():
            discovered_services["python_backend"] = {
                "path": "backend/python_backend",
                "type": "python",
                "main_file": "main.py"
            }

        # Check for TypeScript backend
        if self.paths.server_ts.exists():
            discovered_services["typescript_backend"] = {
                "path": "backend/server-ts",
                "type": "typescript",
                "package_json": "package.json"
            }

        # Check for frontend
        if self.paths.client.exists():
            discovered_services["frontend"] = {
                "path": "client",
                "type": "javascript",
                "package_json": "package.json"
            }

        return discovered_services


# Global configuration instance
_project_config: Optional[ProjectConfig] = None


def get_project_config() -> ProjectConfig:
    """Get the global project configuration instance."""
    global _project_config
    if _project_config is None:
        _project_config = ProjectConfig()
    return _project_config


def reload_config() -> None:
    """Reload the project configuration."""
    global _project_config
    _project_config = ProjectConfig()
=======
Project configuration utilities
"""

from pathlib import Path

class ProjectConfig:
    """Project configuration container."""

    def __init__(self):
        self.root_dir = Path(__file__).parent.parent

# Global configuration instance
_project_config = None

def get_project_config():
    """Get the project configuration."""
    global _project_config
    if _project_config is None:
        _project_config = ProjectConfig()
    return _project_config
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
