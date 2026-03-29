import os


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


settings = Settings()
