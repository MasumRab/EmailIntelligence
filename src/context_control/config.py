"""Configuration management system for Agent Context Control library."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator


class ContextControlConfig(BaseModel):
    """Main configuration for the Agent Context Control library."""

    # Storage configuration
    config_dir: Path = Field(
        default=Path(".context-control"),
        description="Directory for configuration files",
    )
    profiles_dir: Path = Field(
        default=Path(".context-control/profiles"),
        description="Directory for context profile files",
    )

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[Path] = Field(default=None, description="Optional log file path")

    # Git configuration
    git_repo_path: Path = Field(
        default=Path("."), description="Path to the Git repository"
    )

    # Security configuration
    enable_isolation: bool = Field(
        default=True, description="Enable context isolation mechanisms"
    )
    strict_validation: bool = Field(
        default=True, description="Enable strict context validation"
    )

    # Performance configuration
    cache_enabled: bool = Field(
        default=True, description="Enable caching for performance"
    )
    cache_ttl_seconds: int = Field(
        default=300, description="Cache time-to-live in seconds"
    )

    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v.upper()

    @validator("cache_ttl_seconds")
    def validate_cache_ttl(cls, v):
        """Validate cache TTL is positive."""
        if v <= 0:
            raise ValueError("Cache TTL must be positive")
        return v

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


class ConfigurationLoader:
    """Handles loading configuration from various sources with dependency injection support."""
    
    def __init__(self):
        """Initialize the configuration loader."""
        self._config_cache: Dict[str, ContextControlConfig] = {}
    
    def load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables.

        Returns:
            Dictionary of configuration values from environment
        """
        config = {}

        # Path configurations
        if config_dir := os.getenv("CONTEXT_CONTROL_CONFIG_DIR"):
            config["config_dir"] = Path(config_dir)
        if profiles_dir := os.getenv("CONTEXT_CONTROL_PROFILES_DIR"):
            config["profiles_dir"] = Path(profiles_dir)
        if git_repo_path := os.getenv("CONTEXT_CONTROL_GIT_REPO_PATH"):
            config["git_repo_path"] = Path(git_repo_path)
        if log_file := os.getenv("CONTEXT_CONTROL_LOG_FILE"):
            config["log_file"] = Path(log_file)

        # String configurations
        if log_level := os.getenv("CONTEXT_CONTROL_LOG_LEVEL"):
            config["log_level"] = log_level

        # Boolean configurations
        if enable_isolation := os.getenv("CONTEXT_CONTROL_ENABLE_ISOLATION"):
            config["enable_isolation"] = enable_isolation.lower() in ("true", "1", "yes")
        if strict_validation := os.getenv("CONTEXT_CONTROL_STRICT_VALIDATION"):
            config["strict_validation"] = strict_validation.lower() in ("true", "1", "yes")
        if cache_enabled := os.getenv("CONTEXT_CONTROL_CACHE_ENABLED"):
            config["cache_enabled"] = cache_enabled.lower() in ("true", "1", "yes")

        # Integer configurations
        if cache_ttl := os.getenv("CONTEXT_CONTROL_CACHE_TTL_SECONDS"):
            try:
                config["cache_ttl_seconds"] = int(cache_ttl)
            except ValueError:
                pass  # Use default if invalid

        return config

    def load_from_file(self, config_file: Path) -> Dict[str, Any]:
        """Load configuration from a JSON file.

        Args:
            config_file: Path to the configuration file

        Returns:
            Dictionary of configuration values from file
        """
        import json

        if not config_file.exists():
            return {}

        try:
            with open(config_file, "r") as f:
                data = json.load(f)

            # Convert string paths to Path objects
            for key in ["config_dir", "profiles_dir", "git_repo_path", "log_file"]:
                if key in data and isinstance(data[key], str):
                    data[key] = Path(data[key])

            return data
        except (json.JSONDecodeError, IOError):
            return {}
    
    def load_config(
        self, 
        config_file: Optional[Path] = None, 
        override_config: Optional[Dict[str, Any]] = None,
        cache_key: Optional[str] = None
    ) -> ContextControlConfig:
        """Load the complete configuration, merging defaults, file, env, and overrides.

        Args:
            config_file: Optional path to configuration file
            override_config: Optional configuration overrides
            cache_key: Optional cache key for caching (if None, caching is disabled)

        Returns:
            Complete ContextControlConfig instance
        """
        # Check cache first if cache key provided
        if cache_key and cache_key in self._config_cache:
            return self._config_cache[cache_key]
        
        config = {}

        # Load from file if specified
        if config_file:
            config.update(self.load_from_file(config_file))

        # Load from environment (overrides file)
        config.update(self.load_from_env())

        # Apply overrides (highest priority)
        if override_config:
            config.update(override_config)

        # Create and optionally cache the configuration
        final_config = ContextControlConfig(**config)
        
        if cache_key:
            self._config_cache[cache_key] = final_config
            
        return final_config
    
    def clear_cache(self):
        """Clear all cached configurations."""
        self._config_cache.clear()


# Global configuration instance for legacy support
_global_config: Optional[ContextControlConfig] = None


def get_current_config() -> ContextControlConfig:
    """Get the current global configuration (legacy function).
    
    Returns:
        Current configuration instance
    """
    global _global_config
    if _global_config is None:
        _global_config = get_config()
    return _global_config


def reset_global_config():
    """Reset the global configuration (for testing/legacy support)."""
    global _global_config
    _global_config = None


# Global configuration loader instance for backward compatibility
_default_loader = ConfigurationLoader()


def get_config(
    config_file: Optional[Path] = None, override_config: Optional[Dict[str, Any]] = None
) -> ContextControlConfig:
    """Get the complete configuration, merging defaults, file, env, and overrides.

    Args:
        config_file: Optional path to configuration file
        override_config: Optional configuration overrides

    Returns:
        Complete ContextControlConfig instance
    """
    return _default_loader.load_config(config_file, override_config)


def init_config(
    config_file: Optional[Path] = None, override_config: Optional[Dict[str, Any]] = None
) -> ContextControlConfig:
    """Initialize configuration (deprecated - kept for backward compatibility).

    Args:
        config_file: Optional path to configuration file
        override_config: Optional configuration overrides

    Returns:
        The initialized configuration
    """
    return get_config(config_file, override_config)


def load_config_with_cache(
    config_file: Optional[Path] = None, 
    override_config: Optional[Dict[str, Any]] = None,
    cache_key: str = "default"
) -> ContextControlConfig:
    """Load configuration with caching support.

    Args:
        config_file: Optional path to configuration file
        override_config: Optional configuration overrides
        cache_key: Cache key for the configuration

    Returns:
        Complete ContextControlConfig instance
    """
    return _default_loader.load_config(config_file, override_config, cache_key)


def clear_config_cache():
    """Clear all cached configurations."""
    _default_loader.clear_cache()
    reset_global_config()
