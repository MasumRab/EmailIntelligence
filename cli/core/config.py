"""
Configuration Management Module
"""
import logging
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

class ConfigManager:
    """Configuration management"""
    
    def __init__(self, cli_base):
        self.cli = cli_base
        self.logger = getattr(cli_base, 'logger', None)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config file."""
        if self.cli.config_file.exists():
            with open(self.cli.config_file) as f:
                if yaml:
                    return yaml.safe_load(f) or {}
        return {}
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        pass
    
    def _check_git_repository(self) -> None:
        """Verify we're in a git repository."""
        if not (self.cli.repo_root / ".git").exists():
            self._error_exit("Not a git repository")
    
    def _setup_logger(self, name: str) -> logging.Logger:
        """Setup a logger with consistent formatting."""
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _info(self, message: str) -> None:
        """Log info message."""
        if self.logger:
            self.logger.info(message)

    def _warn(self, message: str) -> None:
        """Log warning message."""
        if self.logger:
            self.logger.warning(f"⚠️  {message}")

    def _error(self, message: str) -> None:
        """Log error message."""
        if self.logger:
            self.logger.error(f"❌ {message}")

    def _success(self, message: str) -> None:
        """Log success message."""
        if self.logger:
            self.logger.info(f"✅ {message}")

    def _error_exit(self, message: str) -> None:
        """Log error and exit."""
        self._error(message)
        sys.exit(1)
