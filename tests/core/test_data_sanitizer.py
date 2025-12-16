"""
Tests for DataSanitizer.
"""

import pytest
from src.core.security import DataSanitizer

class TestDataSanitizer:
    """Test DataSanitizer methods."""

    def test_sanitize_input_basic_xss(self):
        """Test basic XSS sanitization (existing functionality)."""
        input_data = "<script>alert(1)</script>"
        sanitized = DataSanitizer.sanitize_input(input_data)
        # The current implementation replaces <script with &lt;script
        assert "&lt;script" in sanitized
        assert "<script" not in sanitized

    def test_sanitize_input_img_onerror(self):
        """Test XSS via img onerror (vulnerability)."""
        input_data = "<img src=x onerror=alert(1)>"
        sanitized = DataSanitizer.sanitize_input(input_data)
        # This is expected to fail with current implementation
        # We want it to be escaped, e.g. &lt;img ...
        assert "<img" not in sanitized
        assert "onerror" not in sanitized or "&lt;" in sanitized

    def test_sanitize_input_nested_dict(self):
        """Test sanitization of nested dictionaries."""
        input_data = {
            "key1": "<script>alert(1)</script>",
            "key2": {
                "key3": "<img src=x onerror=alert(1)>"
            }
        }
        sanitized = DataSanitizer.sanitize_input(input_data)
        assert "&lt;script" in sanitized["key1"]
        # Expected to fail currently
        assert "<img" not in sanitized["key2"]["key3"]

    def test_sanitize_output_redaction(self):
        """Test output redaction."""
        input_data = "password: mysecretpassword"
        sanitized = DataSanitizer.sanitize_output(input_data)
        assert "mysecretpassword" not in sanitized
        assert "[REDACTED]" in sanitized

    def test_sanitize_output_nested(self):
        """Test nested output redaction."""
        input_data = {
            "user": "jules",
            "auth_token": "secret_token_123"
        }
        sanitized = DataSanitizer.sanitize_output(input_data)
        assert sanitized["user"] == "jules"
        assert sanitized["auth_token"] == "[REDACTED]"
