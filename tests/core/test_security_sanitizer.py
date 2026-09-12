
import pytest
from src.core.security import DataSanitizer

class TestDataSanitizerImproved:
    def test_sanitize_output_json_strings(self):
        """Test that JSON strings are correctly sanitized"""
        test_cases = [
            ('{"password": "super secret value"}', '{"password": [REDACTED]}'),
            ('{"api_key": "12345-abc"}', '{"api_key": [REDACTED]}'),
            ('{"secret": "value_with_no_spaces"}', '{"secret": [REDACTED]}'),
        ]

        for input_str, expected in test_cases:
            assert DataSanitizer.sanitize_output(input_str) == expected

    def test_sanitize_output_partial_matches(self):
        """Test that keys containing sensitive words are redacted"""
        # "api_key" contains "key", "auth_token" contains "token"
        test_cases = [
            ('auth_token: abc12345', 'auth_token: [REDACTED]'),
            ('my_secret_code: 999', 'my_secret_code: [REDACTED]'),
        ]

        for input_str, expected in test_cases:
            assert DataSanitizer.sanitize_output(input_str) == expected

    def test_sanitize_output_nested_json(self):
        """Test sanitization of nested JSON strings"""
        input_str = '{"nested": {"secret_code": "donotshare", "public": "ok"}}'
        expected = '{"nested": {"secret_code": [REDACTED], "public": "ok"}}'
        assert DataSanitizer.sanitize_output(input_str) == expected

    def test_sanitize_output_plain_text(self):
        """Test sanitization of plain text logs"""
        input_str = 'plain_password: my_password'
        # Note: Unquoted values with spaces are tricky, but our regex handles non-spaces well
        expected = 'plain_password: [REDACTED]'
        assert DataSanitizer.sanitize_output(input_str) == expected

    def test_preserves_non_sensitive(self):
        """Test that non-sensitive data is preserved"""
        input_str = '{"username": "jdoe", "role": "admin"}'
        assert DataSanitizer.sanitize_output(input_str) == input_str
