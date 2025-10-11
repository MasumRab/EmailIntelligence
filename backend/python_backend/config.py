"""
Configuration for the FastAPI application, using Pydantic's BaseSettings.
"""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    These settings are loaded from environment variables or a .env file.
    """

    DATA_DIR: Path = Path("backend/data")  # Default, can be overridden by DATA_DIR env var

    @property
    def EMAILS_FILE(self) -> Path:
        return self.DATA_DIR / "emails.json"

    @property
    def CATEGORIES_FILE(self) -> Path:
        return self.DATA_DIR / "categories.json"

    @property
    def USERS_FILE(self) -> Path:
        return self.DATA_DIR / "users.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single, reusable instance of the settings
settings = Settings()
