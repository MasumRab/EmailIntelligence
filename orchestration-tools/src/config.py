"""Configuration management for orchestration tools."""

import os
import json
from pathlib import Path
from typing import Any, Optional, Dict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # GitHub
    github_token: Optional[str] = None
    github_org: str = "MasumRab"
    github_repo: str = "EmailIntelligence"

    # Git Configuration
    git_user_name: str = "Orchestration Bot"
    git_user_email: str = "orchestration@example.com"

    # Verification Configuration
    verification_profile: str = "default"
    log_level: str = "INFO"
    log_format: str = "json"

    # Environment
    environment: str = "development"
    debug: bool = False

    # Formal Verification
    formal_verification_enabled: bool = True
    formal_verification_timeout: int = 3600
    formal_verification_coverage_target: float = 0.99

    # Token Optimization
    token_optimization_enabled: bool = True
    token_limit_per_request: int = 4000
    token_limit_per_day: int = 100000

    # Performance
    parallel_execution: bool = True
    max_parallel_tasks: int = 4
    cache_enabled: bool = True
    cache_ttl: int = 3600

    # Security
    enable_encryption: bool = True
    encryption_key_path: str = ".keys/encryption.key"
    auth_method: str = "token"

    # Logging
    log_file_path: str = "./logs/orchestration.log"
    structured_logging: bool = True
    correlation_id_prefix: str = "ORCH"

    class Config:
        """Pydantic settings configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_settings() -> Settings:
    """Load settings from environment."""
    load_dotenv()
    return Settings()


def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """Load YAML configuration file."""
    try:
        import yaml
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        raise ImportError("PyYAML is required to load YAML configuration files")
    except FileNotFoundError:
        return {}


def load_json_config(config_path: Path) -> Dict[str, Any]:
    """Load JSON configuration file."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_path}: {e}")


def get_config_path(profile: str = "default") -> Path:
    """Get configuration file path for a verification profile."""
    base_path = Path(__file__).parent.parent / "config"
    return base_path / f"{profile}.yaml"


def load_verification_profiles() -> Dict[str, Any]:
    """Load all verification profiles."""
    config_path = Path(__file__).parent.parent / "config" / "verification_profiles.yaml"
    return load_yaml_config(config_path)


# Global settings instance
settings = load_settings()
