"""The bleach-less fallback in InputSanitizer.sanitize_string must escape, not filter.

bleach is an optional dependency. When it is absent, the sanitizer has to fall
back to something that is safe on its own; a hand-written tag blacklist is not,
because it is case-sensitive and because its "neutralising" replacements used
character references that an HTML parser decodes straight back into the
dangerous form.
"""

import pytest

from src.backend.node_engine import security_manager
from src.backend.node_engine.security_manager import InputSanitizer, SanitizationLevel


@pytest.fixture
def no_bleach(monkeypatch):
    """Force the fallback path regardless of whether bleach is installed."""
    monkeypatch.setattr(security_manager, "bleach", None)


class TestSanitizeStringWithoutBleach:
    def test_uppercase_script_tag_is_escaped(self, no_bleach):
        # A case-sensitive blacklist lets <SCRIPT> through untouched.
        result = InputSanitizer.sanitize_string("<SCRIPT>alert(1)</SCRIPT>")

        assert "<SCRIPT>" not in result
        assert "<" not in result
        assert result == "&lt;SCRIPT&gt;alert(1)&lt;/SCRIPT&gt;"

    def test_all_html_significant_characters_are_escaped(self, no_bleach):
        result = InputSanitizer.sanitize_string('<a href="x" title=\'y\'>&</a>')

        assert "&lt;" in result
        assert "&gt;" in result
        assert "&amp;" in result
        assert "&quot;" in result
        assert "&#x27;" in result
        # Nothing left that an HTML parser would read as markup.
        for raw in ("<", ">", '"', "'"):
            assert raw not in result

    def test_event_handler_attributes_are_escaped(self, no_bleach):
        # The blacklist only knew "onerror" and "onload"; every other handler
        # (and the case variants of those two) passed through.
        result = InputSanitizer.sanitize_string(
            '<img src=x OnMouseOver=alert(1) ONERROR=alert(2)>'
        )

        assert "<img" not in result
        assert ">" not in result
        assert result.startswith("&lt;img")

    def test_javascript_url_is_not_rewritten_into_itself(self, no_bleach):
        # "javascript&#58;" decodes back to "javascript:" in an HTML parser, so
        # the old replacement restored the scheme it claimed to neutralise. The
        # safe answer is to escape the markup around it, not to mangle the text.
        result = InputSanitizer.sanitize_string('<a href="javascript:alert(1)">x</a>')

        assert "&#58;" not in result
        assert result == '&lt;a href=&quot;javascript:alert(1)&quot;&gt;x&lt;/a&gt;'

    def test_plain_text_is_unchanged(self, no_bleach):
        assert InputSanitizer.sanitize_string("Hello World") == "Hello World"

    @pytest.mark.parametrize("level", list(SanitizationLevel))
    def test_fallback_applies_at_every_level(self, no_bleach, level):
        result = InputSanitizer.sanitize_string("<script>x</script>", level)

        assert "<script>" not in result
        assert "&lt;script&gt;" in result
