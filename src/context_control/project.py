"""Project configuration loader for Agent Context Control."""
from pathlib import Path
from typing import Optional
from .config import get_current_config
from .logging import get_context_logger
from .models import ProjectConfig
logger = get_context_logger()
class ProjectConfigLoader:
    """Loads project-specific configuration settings."""
    def __init__(self, config=None):
        """Initialize the project config loader.
        Args:
            config: Optional configuration override
        """
        self.config = config or get_current_config()
    def load_project_config(self) -> ProjectConfig:
        """Load project configuration from various sources.
        Returns:
            ProjectConfig instance with merged settings
        # For now, return a default configuration
        # In a real implementation, this would load from project files
        return ProjectConfig(
            project_name="default",
            project_type="generic",
            max_context_length=4096,
            enable_code_execution=False,
            enable_file_writing=False,
            enable_shell_commands=False,
            preferred_models=["gpt-4", "claude-3"],
        )
