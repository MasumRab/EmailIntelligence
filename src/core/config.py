"""
Centralized configuration management for EmailIntelligence CLI

This module provides a unified configuration system using pydantic-settings
for type-safe configuration with environment variable support.
It extends the existing API settings to ensure consistency.
"""

from pydantic import Field
from typing import Optional, Literal
from pathlib import Path
from ..config.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """
    Central configuration for EmailIntelligence CLI.
    Extends the base API settings with CLI-specific configuration.
    """

    # ===== Git Configuration =====
    git_worktree_base: str = Field(
        default=".worktrees", description="Base directory for git worktrees"
    )
    git_timeout_seconds: int = Field(
        default=300, description="Timeout for git operations in seconds"
    )
    git_max_concurrent_operations: int = Field(
        default=3, description="Maximum concurrent git operations"
    )

    # ===== Validation Configuration =====
    min_test_coverage: float = Field(
        default=0.7, description="Minimum required test coverage (0.0-1.0)"
    )
    max_complexity_score: int = Field(
        default=10, description="Maximum allowed cyclomatic complexity"
    )
    run_security_scans: bool = Field(
        default=True, description="Run security scans during validation"
    )
    run_quality_checks: bool = Field(
        default=True, description="Run code quality checks during validation"
    )

    # ===== Performance Configuration (CLI Extensions) =====
    max_concurrent_analyses: int = Field(
        default=5, description="Maximum concurrent conflict analyses"
    )
    cache_enabled: bool = Field(default=True, description="Enable caching for performance")
    cache_ttl_seconds: int = Field(
        default=3600, description="Cache time-to-live in seconds (1 hour)"
    )

    # ===== Logging Configuration =====
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    log_format: Literal["json", "text"] = Field(
        default="json", description="Log format (json or text)"
    )
    log_file: Optional[str] = Field(
        default=None, description="Log file path (None for console only)"
    )

    # ===== Storage Configuration =====
    metadata_storage_backend: str = Field(
        default="neo4j", description="Metadata storage backend (neo4j or file)"
    )
    file_storage_path: str = Field(
        default=".emailintelligence/metadata",
        description="Path for file-based metadata storage",
    )

    # ===== Analysis Configuration =====
    enable_ast_analysis: bool = Field(default=True, description="Enable AST-based code analysis")
    enable_semantic_analysis: bool = Field(
        default=True, description="Enable semantic conflict detection"
    )
    enable_constitutional_analysis: bool = Field(
        default=True, description="Enable constitutional rule checking"
    )
    constitutional_rules_path: str = Field(
        default="constitutions", description="Path to constitutional rules directory"
    )

    # ===== Resolution Configuration =====
    auto_resolve_simple_conflicts: bool = Field(
        default=True, description="Automatically resolve simple conflicts"
    )
    require_approval_for_high_risk: bool = Field(
        default=True, description="Require human approval for high-risk resolutions"
    )
    max_resolution_attempts: int = Field(
        default=3, description="Maximum resolution attempts per conflict"
    )

    # ===== Testing Configuration =====
    test_framework: str = Field(default="pytest", description="Testing framework to use")
    test_timeout_seconds: int = Field(
        default=300, description="Timeout for test execution in seconds"
    )

    # ===== AI Configuration (CLI Extensions) =====
    use_ai_strategies: bool = Field(
        default=False, description="Enable AI-powered strategy generation"
    )
    fallback_to_non_ai: bool = Field(
        default=True, description="Fall back to non-AI strategies if AI fails"
    )

    # ===== Environment =====
    environment: str = Field(
        default="development",
        description="Environment (development, staging, production)",
    )

    class Config:
        """Pydantic configuration"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Allow extra fields for forward compatibility
        extra = "ignore"

    def get_worktree_path(self, pr_id: str) -> Path:
        """Get worktree path for a PR"""
        return Path(self.git_worktree_base) / f"pr-{pr_id}"

    def get_metadata_path(self, key: str) -> Path:
        """Get metadata file path"""
        return Path(self.file_storage_path) / f"{key}.json"

    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"

    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
