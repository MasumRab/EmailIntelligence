"""
Fictionality Analysis Configuration for EmailIntelligence

Extends the main settings with fictionality-specific configuration
options following the existing settings patterns.
"""

from pydantic import BaseSettings, Field


class FictionalitySettings(BaseSettings):
    """
    Fictionality analysis specific settings

    Provides configuration for fictionality detection rate limits,
    caching, thresholds, and analysis parameters.
    """

    # Rate limiting for fictionality analysis
    fictionality_rate_limit_rpm: int = Field(
        default=3, description="Fictionality analysis requests per minute"
    )

    # Circuit breaker settings
    fictionality_circuit_breaker_threshold: int = Field(
        default=5,
        description="Circuit breaker failure threshold for fictionality analysis",
    )
    fictionality_circuit_breaker_timeout: int = Field(
        default=300, description="Circuit breaker timeout in seconds"
    )

    # Caching configuration
    fictionality_cache_ttl: int = Field(
        default=3600, description="Fictionality analysis cache TTL in seconds"  # 1 hour
    )
    fictionality_cache_enabled: bool = Field(
        default=True, description="Enable fictionality analysis caching"
    )

    # Analysis thresholds
    fictionality_default_threshold: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Default threshold for fictionality classification",
    )
    fictionality_high_threshold: float = Field(
        default=0.8, ge=0.0, le=1.0, description="High fictionality threshold"
    )
    fictionality_uncertain_threshold: float = Field(
        default=0.4, ge=0.0, le=1.0, description="Uncertain fictionality threshold"
    )

    # Analysis parameters
    fictionality_analysis_depth: str = Field(
        default="standard", description="Default analysis depth: quick, standard, deep"
    )
    fictionality_max_tokens: int = Field(
        default=1500, description="Maximum tokens for fictionality analysis"
    )
    fictionality_temperature: float = Field(
        default=0.1,
        ge=0.0,
        le=1.0,
        description="Temperature for fictionality analysis (low for consistency)",
    )

    # Batch processing
    fictionality_batch_size: int = Field(
        default=10, description="Default batch size for fictionality analysis"
    )
    fictionality_max_concurrent: int = Field(
        default=3, description="Maximum concurrent fictionality analyses"
    )

    # Content hashing
    fictionality_content_hash_algorithm: str = Field(
        default="sha256", description="Hash algorithm for content deduplication"
    )
    fictionality_content_hash_length: int = Field(
        default=16, description="Length of content hash for caching"
    )

    # Confidence scoring
    fictionality_confidence_weights: dict = Field(
        default_factory=lambda: {
            "technical_consistency": 0.3,
            "realism_of_requirements": 0.25,
            "complexity_appropriateness": 0.25,
            "detail_specificity": 0.2,
        },
        description="Weights for different confidence factors",
    )

    # Strategy adjustment factors
    fictionality_strategy_reduction_factors: dict = Field(
        default_factory=lambda: {
            "high_fictionality": 0.2,  # 20% reduction for high fictionality
            "probable_fictionality": 0.1,  # 10% reduction for probable fictionality
            "uncertain": 0.05,  # 5% reduction for uncertain
            "probable_real": 0.0,  # No reduction for probable real
            "highly_real": 0.0,  # No reduction for highly real
        },
        description="Confidence reduction factors for different fictionality levels",
    )

    # Error handling
    fictionality_fallback_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Fallback fictionality score when analysis fails",
    )
    fictionality_max_retries: int = Field(
        default=3, description="Maximum retries for fictionality analysis"
    )
    fictionality_retry_delay: float = Field(default=1.0, description="Retry delay in seconds")

    # Performance monitoring
    fictionality_performance_tracking: bool = Field(
        default=True,
        description="Enable performance tracking for fictionality analysis",
    )
    fictionality_metrics_retention_hours: int = Field(
        default=168,
        description="Retention period for fictionality metrics in hours",  # 7 days
    )

    # Feature flags
    fictionality_enabled: bool = Field(
        default=True, description="Enable fictionality analysis feature"
    )
    fictionality_batch_enabled: bool = Field(
        default=True, description="Enable batch fictionality analysis"
    )
    fictionality_caching_enabled: bool = Field(
        default=True, description="Enable fictionality analysis caching"
    )
    fictionality_monitoring_enabled: bool = Field(
        default=True, description="Enable fictionality analysis monitoring"
    )

    # Integration settings
    fictionality_integration_mode: str = Field(
        default="auto", description="Integration mode: auto, manual, disabled"
    )
    fictionality_strategy_integration: bool = Field(
        default=True, description="Integrate fictionality with strategy generation"
    )
    fictionality_conflict_integration: bool = Field(
        default=True, description="Integrate fictionality with conflict analysis"
    )

    # API configuration
    fictionality_api_timeout: int = Field(
        default=60, description="API timeout for fictionality analysis in seconds"
    )
    fictionality_api_version: str = Field(
        default="v1", description="API version for fictionality analysis"
    )

    class Config:
        env_prefix = "FICTIONALITY_"
        case_sensitive = False


# Global fictionality settings instance
fictionality_settings = FictionalitySettings()


class FictionalityAnalysisConfig:
    """
    Configuration helper for fictionality analysis operations
    """

    @staticmethod
    def get_analysis_timeout() -> int:
        """Get analysis timeout based on depth"""
        depth = fictionality_settings.fictionality_analysis_depth
        timeouts = {"quick": 30, "standard": 60, "deep": 120}
        return timeouts.get(depth, 60)

    @staticmethod
    def get_max_tokens_for_depth(depth: str) -> int:
        """Get max tokens based on analysis depth"""
        tokens = {"quick": 800, "standard": 1500, "deep": 2500}
        return tokens.get(depth, 1500)

    @staticmethod
    def get_cache_ttl_for_analysis(analysis_type: str) -> int:
        """Get cache TTL based on analysis type"""
        ttl_map = {
            "quick": 1800,
            "standard": 3600,
            "deep": 7200,
        }  # 30 minutes  # 1 hour  # 2 hours
        return ttl_map.get(analysis_type, 3600)

    @staticmethod
    def should_enable_caching() -> bool:
        """Check if caching should be enabled"""
        return (
            fictionality_settings.fictionality_cache_enabled
            and fictionality_settings.fictionality_caching_enabled
        )

    @staticmethod
    def get_rate_limit() -> int:
        """Get rate limit for fictionality analysis"""
        return fictionality_settings.fictionality_rate_limit_rpm

    @staticmethod
    def get_batch_config() -> dict:
        """Get batch processing configuration"""
        return {
            "max_size": fictionality_settings.fictionality_batch_size,
            "max_concurrent": fictionality_settings.fictionality_max_concurrent,
            "enabled": fictionality_settings.fictionality_batch_enabled,
        }

    @staticmethod
    def get_confidence_threshold(level: str) -> float:
        """Get confidence threshold for specific level"""
        thresholds = {
            "default": fictionality_settings.fictionality_default_threshold,
            "high": fictionality_settings.fictionality_high_threshold,
            "uncertain": fictionality_settings.fictionality_uncertain_threshold,
        }
        return thresholds.get(level, fictionality_settings.fictionality_default_threshold)

    @staticmethod
    def get_strategy_adjustment(fictionality_level: str) -> float:
        """Get strategy adjustment factor for fictionality level"""
        return fictionality_settings.fictionality_strategy_reduction_factors.get(
            fictionality_level, 0.0
        )

    @staticmethod
    def is_feature_enabled() -> bool:
        """Check if fictionality analysis is enabled"""
        return fictionality_settings.fictionality_enabled

    @staticmethod
    def get_integration_config() -> dict:
        """Get integration configuration"""
        return {
            "mode": fictionality_settings.fictionality_integration_mode,
            "strategy": fictionality_settings.fictionality_strategy_integration,
            "conflict": fictionality_settings.fictionality_conflict_integration,
            "auto": fictionality_settings.fictionality_integration_mode == "auto",
        }
