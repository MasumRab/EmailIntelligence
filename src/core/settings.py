"""
Settings for the Email Intelligence Platform core modules.
"""

class Settings:
    """Settings class for core modules."""
    secret_key = "your-secret-key-here"
    algorithm = "HS256"
    access_token_expire_minutes = 30

settings = Settings()