"""
Unit tests for the Settings configuration module.
"""

import os
import sys
import pytest


class TestSettings:
    """Test the Settings class configuration."""

    def test_settings_class_attributes_exist(self):
        """Test that Settings class has all expected attributes as class attributes."""
        from src.config.settings import Settings
        settings = Settings()
        
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'algorithm')
        assert hasattr(settings, 'access_token_expire_minutes')
        assert hasattr(settings, 'rate_limit_window')
        assert hasattr(settings, 'rate_limit_requests')
        assert hasattr(settings, 'redis_url')

    def test_settings_default_values(self):
        """Test that default values are set correctly for class attributes."""
        from src.config.settings import Settings
        
        assert Settings.algorithm == "HS256"
        assert Settings.access_token_expire_minutes == 30
        assert Settings.rate_limit_window == 60
        assert Settings.rate_limit_requests == 100
        assert Settings.redis_url == "redis://localhost:6379"

    def test_settings_instance_not_none(self):
        """Test that the module-level settings instance is not None."""
        from src.config import settings
        assert settings is not None

    def test_settings_instance_types(self):
        """Test that settings instance has correct types for all attributes."""
        from src.config import settings
        
        assert isinstance(settings.secret_key, str)
        assert isinstance(settings.algorithm, str)
        assert isinstance(settings.access_token_expire_minutes, int)
        assert isinstance(settings.rate_limit_window, int)
        assert isinstance(settings.rate_limit_requests, int)
        assert isinstance(settings.redis_url, str)

    def test_settings_integer_types(self):
        """Test that integer settings are actually integers."""
        from src.config import settings
        
        assert isinstance(settings.access_token_expire_minutes, int)
        assert isinstance(settings.rate_limit_window, int)
        assert isinstance(settings.rate_limit_requests, int)

    def test_settings_string_types(self):
        """Test that string settings are actually strings."""
        from src.config import settings
        
        assert isinstance(settings.secret_key, str)
        assert isinstance(settings.algorithm, str)
        assert isinstance(settings.redis_url, str)

    def test_algorithm_is_hs256(self):
        """Test that the default algorithm is HS256."""
        from src.config.settings import Settings
        assert Settings.algorithm == "HS256"

    def test_rate_limit_defaults(self):
        """Test rate limit default values are reasonable."""
        from src.config.settings import Settings
        
        assert Settings.rate_limit_window > 0
        assert Settings.rate_limit_requests > 0
        assert Settings.rate_limit_window >= 1
        assert Settings.rate_limit_requests >= 1

    def test_redis_url_format(self):
        """Test that Redis URL is a valid format."""
        from src.config.settings import Settings
        assert Settings.redis_url.startswith("redis://")

    def test_settings_init_does_nothing(self):
        """Test that __init__ doesn't raise any exceptions."""
        from src.config.settings import Settings
        settings = Settings()
        assert settings is not None


class TestSettingsEnvVarReading:
    """Test that Settings reads environment variables at class definition time."""

    def test_env_var_read_at_class_definition(self):
        """Test that environment variables are read when class is defined."""
        os.environ["TEST_SECRET"] = "my-test-secret"
        
        test_code = '''import os

class TestSettings:
    secret_key = os.getenv("TEST_SECRET", "default")
    rate_limit = int(os.getenv("TEST_RATE", "100"))
'''
        
        with open('/tmp/test_env_settings.py', 'w') as f:
            f.write(test_code)
        
        if 'test_env_settings' in sys.modules:
            del sys.modules['test_env_settings']
        
        # Add /tmp to path so module can be found
        sys.path.insert(0, '/tmp')
        from test_env_settings import TestSettings
        
        assert TestSettings.secret_key == "my-test-secret"
        
        # Cleanup path
        sys.path.remove('/tmp')
        del os.environ["TEST_SECRET"]

    def test_integer_conversion_in_class_body(self):
        """Test that integers are properly converted from string env vars."""
        os.environ["TEST_INT"] = "42"
        
        test_code = '''import os

class TestIntSettings:
    my_int = int(os.getenv("TEST_INT", "0"))
'''
        
        with open('/tmp/test_int_settings.py', 'w') as f:
            f.write(test_code)
        
        if 'test_int_settings' in sys.modules:
            del sys.modules['test_int_settings']
        
        # Add /tmp to path so module can be found
        sys.path.insert(0, '/tmp')
        from test_int_settings import TestIntSettings
        
        assert TestIntSettings.my_int == 42
        assert isinstance(TestIntSettings.my_int, int)
        
        # Cleanup path
        sys.path.remove('/tmp')
        del os.environ["TEST_INT"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
