"""
Settings for the Email Intelligence Platform core modules.
"""

class Settings:
    """Settings class for core modules."""
    secret_key = "your-secret-key-here"
    algorithm = "HS256"
    access_token_expire_minutes = 30


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