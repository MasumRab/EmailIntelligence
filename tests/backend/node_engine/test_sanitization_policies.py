
import pytest
import json
from src.backend.node_engine.security_manager import InputSanitizer, SanitizationLevel

class TestSanitizationPolicies:

    def test_strict_policy(self):
        # Strict should remove all tags
        input_str = "<p>Hello <strong>World</strong></p>"
        expected = "Hello World"
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.STRICT)
        assert result == expected

        # Dangerous input
        # Note: bleach strips tags but keeps content. 'alert(1)' remains as text.
        input_str = "<script>alert(1)</script>Strict"
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.STRICT)
        assert "<script>" not in result
        assert "alert(1)" in result
        assert "Strict" in result

    def test_standard_policy(self):
        # Standard should allow basic tags
        input_str = "<p>Hello <strong>World</strong></p>"
        # bleach produces consistent output
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.STANDARD)
        assert "<p>" in result
        assert "<strong>" in result
        assert "Hello" in result

        # Should not allow div in standard
        input_str = "<div>Div content</div>"
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.STANDARD)
        assert "Div content" in result
        assert "<div>" not in result

        # Dangerous input
        input_str = "<script>alert(1)</script>"
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.STANDARD)
        assert "<script>" not in result

    def test_permissive_policy(self):
        # Permissive allows more tags like div
        input_str = "<div>Div content</div>"
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.PERMISSIVE)
        assert "<div>" in result
        assert "Div content" in result

        # Permissive allows iframe (configured in policy)
        input_str = '<iframe src="http://example.com"></iframe>'
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.PERMISSIVE)
        assert "<iframe" in result

        # But still sanitizes dangerous attributes/tags
        input_str = '<script>alert(1)</script>'
        result = InputSanitizer.sanitize_string(input_str, SanitizationLevel.PERMISSIVE)
        assert "<script>" not in result

    def test_default_level(self):
        # Default should be STANDARD
        input_str = "<div>Div content</div>"
        result = InputSanitizer.sanitize_string(input_str)
        # Standard doesn't allow div
        assert "<div>" not in result
        assert "Div content" in result

    def test_sanitize_json(self):
        data = {
            "safe": "<p>Safe</p>",
            "unsafe": "<script>alert(1)</script>",
            "nested": {
                "val": "<strong>Bold</strong>"
            },
            "list": ["<em>Italic</em>", "<script>bad</script>"]
        }
        json_str = json.dumps(data)

        # Test with Standard
        cleaned = InputSanitizer.sanitize_json(json_str, SanitizationLevel.STANDARD)
        assert cleaned["safe"] == "<p>Safe</p>"
        assert "<script>" not in cleaned["unsafe"]
        assert cleaned["nested"]["val"] == "<strong>Bold</strong>"
        assert cleaned["list"][0] == "<em>Italic</em>"
        assert "<script>" not in cleaned["list"][1]

        # Test with Strict
        cleaned_strict = InputSanitizer.sanitize_json(json_str, SanitizationLevel.STRICT)
        assert cleaned_strict["safe"] == "Safe"
        assert cleaned_strict["nested"]["val"] == "Bold"
