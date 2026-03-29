import os
from typing import Optional


class Settings:
    """Settings class for core modules."""

    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Rate limiting settings
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    
    # Redis settings
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    def __init__(self):
        pass


class SettingsManager:
    """Settings manager for the Email Intelligence Platform."""

    def __init__(self):
        self.settings = Settings()

    def get_setting(self, key: str):
        """Get a setting value by key."""
        return getattr(self.settings, key, None)

    def set_setting(self, key: str, value):
        """Set a setting value."""
        setattr(self.settings, key, value)

    def get_all_settings(self):
        """Get all settings as a dictionary."""
        return self.settings.__dict__


settings = Settings()
