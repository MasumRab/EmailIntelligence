<<<<<<< HEAD
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


settings = Settings()
=======
>>>>>>> main
