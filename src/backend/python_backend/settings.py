"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Configuration management for the Email Intelligence Platform
Using Pydantic Settings for environment-based configuration
"""

from pydantic import Field
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Email Intelligence Platform"
    app_version: str = "2.0.0"
    debug: bool = Field(default=False, env="DEBUG")

    # Database settings
    data_dir: str = Field(default="./data", env="DATA_DIR")
    emails_file: str = "emails.json.gz"
    categories_file: str = "categories.json.gz"
    users_file: str = "users.json.gz"

    # API settings
    api_prefix: str = "/api/v1"
    api_docs_enabled: bool = True

    # Security settings
    secret_key: str = Field(
        default=..., env="SECRET_KEY"
    )  # Required - must be set in environment
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # API Keys
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    deepseek_api_key: str = Field(default="", env="DEEPSEEK_API_KEY")
    groq_api_key: str = Field(default="", env="GROQ_API_KEY")
    cohere_api_key: str = Field(default="", env="COHERE_API_KEY")

    # CORS settings
    allowed_origins: list = [
        "http://localhost:5000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Performance settings
    max_concurrent_workflows: int = 10
    max_api_calls_per_minute: int = 100

    # Database compression settings
    gzip_compression_level: int = 6  # Default compression level

    @validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v):
        if not v:
            raise ValueError("SECRET_KEY environment variable must be set")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
