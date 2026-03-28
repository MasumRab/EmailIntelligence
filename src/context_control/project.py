"""Project configuration management for Agent Context Control."""

from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import os

from .models import ProjectConfig
from .logging import get_context_logger
from .exceptions import ConfigurationError
from .config import get_current_config


logger = get_context_logger()


class ProjectConfigLoader:
    """Loads and manages project-specific configurations."""

    def __init__(self, config=None):
        """Initialize the project config loader.

        Args:
            config: Optional configuration override
        """
        self.config = config or get_current_config()
        self._cache: Dict[str, ProjectConfig] = {}

    def load_project_config(
        self, project_path: Optional[Path] = None
    ) -> Optional[ProjectConfig]:
        """Load project configuration from the given path.

        Args:
            project_path: Path to the project directory. Defaults to current directory.

        Returns:
            ProjectConfig instance or None if not found
        """
        project_path = project_path or Path.cwd()

        # Check cache first
        cache_key = str(project_path)
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Try to load from various locations
        config = self._load_from_project_file(project_path)
        if config:
            self._cache[cache_key] = config
            return config

        config = self._load_from_config_directory(project_path)
        if config:
            self._cache[cache_key] = config
            return config

        # Return None if no config found
        logger.debug(f"No project configuration found for {project_path}")
        return None

    def _load_from_project_file(self, project_path: Path) -> Optional[ProjectConfig]:
        """Load config from a project-specific file.

        Args:
            project_path: Path to the project directory

        Returns:
            ProjectConfig or None
        """
        config_files = [
            project_path / ".context-control" / "project.json",
            project_path / ".project.json",
            project_path / "project.json",
        ]

        for config_file in config_files:
            if config_file.exists():
                try:
                    with open(config_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    config = ProjectConfig(**data)
                    logger.info(f"Loaded project config from {config_file}")
                    return config
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    logger.warning(f"Invalid project config file {config_file}: {e}")
                    continue

        return None

    def _load_from_config_directory(
        self, project_path: Path
    ) -> Optional[ProjectConfig]:
        """Load config from a configuration directory.

        Args:
            project_path: Path to the project directory

        Returns:
            ProjectConfig or None
        """
        config_dir = project_path / ".context-control"
        if not config_dir.exists():
            return None

        # Look for project config files
        project_files = list(config_dir.glob("project*.json"))
        if not project_files:
            return None

        # Use the first one found
        config_file = project_files[0]
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            config = ProjectConfig(**data)
            logger.info(f"Loaded project config from {config_file}")
            return config
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Invalid project config file {config_file}: {e}")
            return None

    def save_project_config(
        self, config: ProjectConfig, project_path: Optional[Path] = None
    ) -> bool:
        """Save project configuration to file.

        Args:
            config: ProjectConfig to save
            project_path: Path to save to. Defaults to current directory.

        Returns:
            True if saved successfully, False otherwise
        """
        project_path = project_path or Path.cwd()
        config_dir = project_path / ".context-control"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / "project.json"

        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config.dict(), f, indent=2, ensure_ascii=False)

            # Update cache
            cache_key = str(project_path)
            self._cache[cache_key] = config

            logger.info(f"Saved project config to {config_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save project config to {config_file}: {e}")
            return False

    def detect_project_type(self, project_path: Optional[Path] = None) -> str:
        """Auto-detect project type based on files present.

        Args:
            project_path: Path to the project directory

        Returns:
            Detected project type
        """
        project_path = project_path or Path.cwd()

        # Check for common project indicators
        indicators = {
            "python": ["setup.py", "pyproject.toml", "requirements.txt", "*.py"],
            "javascript": ["package.json", "*.js", "*.ts"],
            "web": ["index.html", "static/", "templates/"],
            "api": ["api/", "routes/", "controllers/"],
            "library": ["src/", "lib/", "include/"],
            "data": ["data/", "*.csv", "*.json", "notebooks/"],
        }

        scores = {}
        for project_type, patterns in indicators.items():
            score = 0
            for pattern in patterns:
                if "*" in pattern:
                    # Glob pattern
                    matches = list(project_path.glob(pattern))
                    score += len(matches)
                else:
                    # Exact file
                    if (project_path / pattern).exists():
                        score += 1
            scores[project_type] = score

        # Return the type with highest score
        best_type = max(scores, key=lambda k: scores[k])
        if scores[best_type] == 0:
            return "generic"

        return best_type

    def create_default_config(
        self, project_path: Optional[Path] = None
    ) -> ProjectConfig:
        """Create a default project configuration.

        Args:
            project_path: Path to the project directory

        Returns:
            Default ProjectConfig for the project
        """
        project_path = project_path or Path.cwd()
        project_name = project_path.name
        project_type = self.detect_project_type(project_path)

        # Set defaults based on project type
        defaults = {
            "python": {
                "enable_code_execution": True,
                "enable_file_writing": True,
                "preferred_models": ["gpt-4", "claude-3", "codellama"],
            },
            "javascript": {
                "enable_code_execution": True,
                "enable_file_writing": True,
                "preferred_models": ["gpt-4", "claude-3", "codellama"],
            },
            "web": {
                "enable_file_writing": True,
                "preferred_models": ["gpt-4", "claude-3"],
            },
            "api": {
                "enable_shell_commands": True,
                "preferred_models": ["gpt-4", "claude-3"],
            },
            "library": {
                "enable_code_execution": True,
                "preferred_models": ["gpt-4", "claude-3", "codellama"],
            },
            "data": {
                "max_context_length": 8192,
                "preferred_models": ["gpt-4", "claude-3"],
            },
        }

        config_data = {
            "project_name": project_name,
            "project_type": project_type,
            **defaults.get(project_type, {}),
        }

        return ProjectConfig(**config_data)

    def clear_cache(self):
        """Clear the project config cache."""
        self._cache.clear()
        logger.debug("Project config cache cleared")


# Global instance
_project_loader: Optional[ProjectConfigLoader] = None


def get_project_loader() -> ProjectConfigLoader:
    """Get the global project config loader instance.

    Returns:
        ProjectConfigLoader instance
    """
    global _project_loader
    if _project_loader is None:
        _project_loader = ProjectConfigLoader()
    return _project_loader


def load_project_config(project_path: Optional[Path] = None) -> Optional[ProjectConfig]:
    """Load project configuration for the given path.

    Args:
        project_path: Path to the project directory

    Returns:
        ProjectConfig or None
    """
    return get_project_loader().load_project_config(project_path)
