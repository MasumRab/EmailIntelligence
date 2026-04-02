"""
Tests for src/core/settings.py
"""

import os
import pytest
from src.core import settings


class TestSettings:
    """Tests for Settings class."""

    def test_settings_algorithm_is_hs256(self):
        """Test that default algorithm is HS256."""
        assert settings.settings.algorithm == "HS256"

    def test_settings_default_token_expiry(self):
        """Test default token expiry is 30 minutes."""
        assert settings.settings.access_token_expire_minutes == 30

    def test_settings_has_secret_key(self):
        """Test that settings has a secret key set."""
        # The global settings instance should have a secret key from environment
        assert settings.settings.secret_key != ""

    def test_settings_secret_key_is_string(self):
        """Test that secret key is a string."""
        assert isinstance(settings.settings.secret_key, str)

    def test_settings_token_expiry_is_integer(self):
        """Test that token expiry is an integer."""
        assert isinstance(settings.settings.access_token_expire_minutes, int)
        assert settings.settings.access_token_expire_minutes > 0