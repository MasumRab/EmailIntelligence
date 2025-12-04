"""
Configuration management for PR Resolution Automation System
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # GraphQL settings
    graphql_host: str = Field(default="0.0.0.0", description="GraphQL API host")
    graphql_port: int = Field(default=8000, description="GraphQL API port")
    graphql_max_query_complexity: int = Field(default=100, description="Maximum query complexity")

    # Performance requirements
    query_timeout_ms: int = Field(default=100, description="Query timeout in milliseconds")
    mutation_timeout_ms: int = Field(default=500, description="Mutation timeout in milliseconds")
    max_memory_mb: int = Field(default=2048, description="Maximum memory usage in MB")

    # Database
    neo4j_uri: str = Field(default="bolt://localhost:7687", description="Neo4j connection URI")
    neo4j_user: str = Field(default="neo4j", description="Neo4j username")
    neo4j_password: str = Field(description="Neo4j password")
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")

    # API settings
    api_version: str = Field(default="v1", description="API version")
    debug: bool = Field(default=False, description="Debug mode")

    # CORS settings
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )

    # Security
    secret_key: str = Field(..., description="Secret key for JWT tokens (env: SECRET_KEY)")
    access_token_expire_minutes: int = Field(default=30, description="Token expiration time")
    # Rate limiting
    rate_limit_requests: int = Field(default=100, description="Rate limit per minute")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")

    # OpenAI API settings
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4", description="OpenAI model to use")
    openai_max_tokens: int = Field(default=1000, description="Maximum tokens for OpenAI requests")
    openai_temperature: float = Field(default=0.3, description="OpenAI temperature for responses")
    openai_timeout: int = Field(default=60, description="OpenAI request timeout in seconds")
    openai_max_retries: int = Field(default=3, description="Maximum retries for OpenAI requests")

    # AI Rate limiting and caching
    ai_rate_limit_rpm: int = Field(default=3, description="AI requests per minute (OpenAI limit)")
    ai_cache_ttl: int = Field(default=3600, description="AI cache TTL in seconds (1 hour)")
    ai_batch_size: int = Field(default=10, description="Batch size for AI processing")
    ai_concurrent_requests: int = Field(default=2, description="Concurrent AI requests")

    # AI Processing settings
    ai_max_complexity_analysis: int = Field(
        default=50, description="Max complexity score to analyze"
    )
    ai_min_confidence_threshold: float = Field(
        default=0.7, description="Minimum confidence for AI suggestions"
    )
    ai_fallback_enabled: bool = Field(default=True, description="Enable AI fallback strategies")
    ai_circuit_breaker_threshold: int = Field(
        default=5, description="Circuit breaker failure threshold"
    )
    ai_circuit_breaker_timeout: int = Field(
        default=300, description="Circuit breaker timeout in seconds"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings()
