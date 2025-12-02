from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "a_default_secret_key"  # Default is insecure, should be overridden by env var
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
