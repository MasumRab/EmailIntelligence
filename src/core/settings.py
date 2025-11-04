"""
Settings for the Email Intelligence Platform core modules.
"""

import os
from typing import Optional


class Settings:
    """Settings class for core modules."""

    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def __init__(self):
        # Ensure a secret key is provided
        if not self.secret_key:
            raise ValueError("SECRET_KEY environment variable must be set")


class SettingsManager:
    """
    Settings manager for the Email Intelligence Platform.
    
    This class handles application settings and configuration.
    """
    
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
settings_manager = SettingsManager()
