"""
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