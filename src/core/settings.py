"""
Settings for the Email Intelligence Platform core modules.
"""

import os


class Settings:
    """Settings class for core modules."""

    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def __init__(self, raise_on_missing: bool = True):
        # Ensure a secret key is provided
        if raise_on_missing and not self.secret_key:
            raise ValueError("SECRET_KEY environment variable must be set")


class SettingsManager:
    """
    Settings manager for the Email Intelligence Platform.

    This class handles application settings and configuration.
    """

    def __init__(self):
        self.settings = Settings(raise_on_missing=False)

    def get_setting(self, key: str):
        """Get a setting value by key."""
        return getattr(self.settings, key, None)

    def set_setting(self, key: str, value):
        """Set a setting value."""
        setattr(self.settings, key, value)

    def get_all_settings(self):
        """Get all settings as a dictionary."""
        return self.settings.__dict__


# Create a default settings instance that doesn't raise
try:
    settings = Settings(raise_on_missing=False)
except ValueError:
    # Fallback if env var not set
    class FallbackSettings:
        secret_key = ""
        algorithm = "HS256"
        access_token_expire_minutes = 30
    settings = FallbackSettings()
