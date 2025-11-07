"""
Application settings management for the Email Intelligence Platform.
This module uses Pydantic's BaseSettings to load configuration from
environment variables and .env files, ensuring a robust and type-safe
configuration system.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """
    Defines the application's configuration settings, loaded from environment
    variables or a .env file.
    """

    # --- General Application Settings ---
    app_name: str = "Email Intelligence Platform"
    debug: bool = Field(False, description="Enable debug mode for verbose logging and diagnostics.")

    # --- Database Configuration ---
    # Specifies the directory where all application data is stored.
    data_dir: str = Field("data", description="Directory to store application data.")

    # --- Security and Authentication ---
    # The secret key is critical for signing JWT tokens and other cryptographic operations.
    # It should be a long, random string and kept secret in production.
    secret_key: str = Field(..., description="A strong secret key for cryptographic operations.")

    # The algorithm used for signing JWT tokens.
    jwt_algorithm: str = Field("HS256", description="The algorithm to use for JWT signing.")

    # Defines the expiration time for access tokens.
    access_token_expire_minutes: int = Field(30, description="Access token expiration time in minutes.")

    # --- Gmail API Integration ---
    # These settings are required for the application to interact with the Gmail API.
    # They are typically obtained from the Google Cloud Console.
    google_client_id: str = Field(None, description="Google OAuth 2.0 Client ID.")
    google_client_secret: str = Field(None, description="Google OAuth 2.0 Client Secret.")
    google_redirect_uri: str = Field("http://localhost:8000/auth/callback", description="Google OAuth 2.0 Redirect URI.")

    # --- CORS (Cross-Origin Resource Sharing) ---
    # A list of allowed origins for CORS. Use "*" to allow all, but it's more
    # secure to list specific domains in production.
    allowed_origins: str = Field("http://localhost:3000,http://127.0.0.1:3000", description="Comma-separated list of allowed CORS origins.")

    class Config:
        # Pydantic settings configuration
        # - `env_file`: Specifies the file to load environment variables from.
        # - `env_file_encoding`: The encoding of the .env file.
        # - `case_sensitive`: If True, environment variable names are case-sensitive.
        model_config = SettingsConfigDict(
            env_file="/app/.env",
            env_file_encoding="utf-8",
            case_sensitive=False
        )

# Create a single, importable instance of the settings
# This instance will be populated by Pydantic upon first import.
settings = AppSettings()
