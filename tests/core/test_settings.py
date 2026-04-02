"""
Tests for settings module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock


class TestSettings:
    """Test the Settings class."""

    def test_settings_creation_with_secret_key(self):
        """Test Settings creation with SECRET_KEY set."""
        with patch.dict(os.environ, {"SECRET_KEY": "test-secret-key"}):
            from src.core.settings import Settings
            settings = Settings()
            assert settings.secret_key == "test-secret-key"
            assert settings.algorithm == "HS256"

    def test_settings_default_algorithm(self):
        """Test Settings default algorithm."""
        with patch.dict(os.environ, {"SECRET_KEY": "test-key"}):
            from src.core.settings import Settings
            settings = Settings()
            assert settings.algorithm == "HS256"

    def test_settings_access_token_expire_minutes_default(self):
        """Test Settings default token expiration."""
        with patch.dict(os.environ, {"SECRET_KEY": "test-key"}):
            from src.core.settings import Settings
            settings = Settings()
            assert settings.access_token_expire_minutes == 30

    def test_settings_access_token_expire_minutes_custom(self):
        """Test Settings custom token expiration."""
        with patch.dict(os.environ, {"SECRET_KEY": "test-key", "ACCESS_TOKEN_EXPIRE_MINUTES": "60"}):
            from importlib import reload
            import src.core.settings as settings_module
            reload(settings_module)
            settings = settings_module.Settings()
            assert settings.access_token_expire_minutes == 60

    def test_settings_raises_without_secret_key(self):
        """Test Settings raises ValueError without SECRET_KEY."""
        # Clear the environment
        env_without_secret = os.environ.copy()
        if "SECRET_KEY" in env_without_secret:
            del env_without_secret["SECRET_KEY"]
        
        with patch.dict(os.environ, env_without_secret, clear=True):
            with pytest.raises(ValueError, match="SECRET_KEY environment variable must be set"):
                from importlib import reload
                import src.core.settings as settings_module
                # Reload to pick up the cleared environment
                reload(settings_module)
                settings_module.Settings()

    def test_settings_singleton(self):
        """Test the settings singleton."""
        with patch.dict(os.environ, {"SECRET_KEY": "test-key"}):
            from src.core.settings import settings
            assert settings is not None
            assert isinstance(settings.secret_key, str)


class TestSettingsIntegration:
    """Integration tests for Settings with environment."""

    def test_settings_with_empty_secret_key(self):
        """Test Settings handles empty SECRET_KEY."""
        with patch.dict(os.environ, {"SECRET_KEY": ""}):
            with pytest.raises(ValueError):
                from importlib import reload
                import src.core.settings as settings_module
                reload(settings_module)
                settings_module.Settings()