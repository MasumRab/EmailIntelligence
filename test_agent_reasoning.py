"""
Comprehensive unit tests for agent_reasoning.py

Tests the generate_reasoning_prompt function with:
- Happy paths and standard inputs
- Edge cases and boundary conditions  
- Special characters and unicode
- Various string formats and lengths
"""

import unittest
from agent_reasoning import generate_reasoning_prompt


class TestGenerateReasoningPrompt(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Core test suite for generate_reasoning_prompt function."""

    def test_basic_functionality(self):
        """Test basic operation with simple inputs."""
        result = generate_reasoning_prompt("Solve this", "thinking")
        self.assertIsInstance(result, str)
        self.assertIn("[thinking]", result)
        self.assertIn("Solve this", result)

    def test_empty_prompt(self):
        """Test with empty prompt string."""
        result = generate_reasoning_prompt("", "tag")
        self.assertIn("[tag]", result)

    def test_empty_tag(self):
        """Test with empty tag string."""
        result = generate_reasoning_prompt("prompt", "")
        self.assertIn("prompt", result)
        self.assertIn("[]", result)

    def test_both_empty(self):
        """Test with both parameters empty."""
        result = generate_reasoning_prompt("", "")
        self.assertEqual(result, "[] ")

    def test_multiline_prompt(self):
        """Test with multiline prompt."""
        prompt = "Line1\nLine2\nLine3"
        result = generate_reasoning_prompt(prompt, "multi")
        self.assertIn("Line1", result)
        self.assertIn("Line2", result)
        self.assertIn("[multi]", result)

    def test_special_chars_in_prompt(self):
        """Test special characters in prompt."""
        prompt = "!@#$%^&*()_+-={}[]|:;<>,.?/"
        result = generate_reasoning_prompt(prompt, "special")
        self.assertIn(prompt, result)

    def test_special_chars_in_tag(self):
        """Test special characters in tag."""
        result = generate_reasoning_prompt("text", "tag_with-dots.123")
        self.assertIn("[tag_with-dots.123]", result)

    def test_unicode_in_prompt(self):
        """Test unicode characters in prompt."""
        prompt = "你好 мир 🌍"
        result = generate_reasoning_prompt(prompt, "unicode")
        self.assertIn("你好", result)
        self.assertIn("🌍", result)

    def test_unicode_in_tag(self):
        """Test unicode in tag."""
        result = generate_reasoning_prompt("test", "тег")
        self.assertIn("[тег]", result)

    def test_very_long_prompt(self):
        """Test with very long prompt."""
        prompt = "A" * 10000
        result = generate_reasoning_prompt(prompt, "long")
        self.assertIn("[long]", result)
        self.assertTrue(len(result) > 10000)

    def test_very_long_tag(self):
        """Test with very long tag."""
        tag = "B" * 1000
        result = generate_reasoning_prompt("short", tag)
        self.assertTrue(len(result) > 1000)

    def test_whitespace_prompt(self):
        """Test prompt with only whitespace."""
        result = generate_reasoning_prompt("   \t\n  ", "ws")
        self.assertIn("[ws]", result)

    def test_whitespace_tag(self):
        """Test tag with whitespace."""
        result = generate_reasoning_prompt("text", "  spaced  ")
        self.assertIn("[  spaced  ]", result)

    def test_quotes_in_prompt(self):
        """Test various quote types."""
        prompt = '''He said "hello" and 'goodbye' with `backticks`'''
        result = generate_reasoning_prompt(prompt, "quotes")
        self.assertIn('"hello"', result)
        self.assertIn("'goodbye'", result)

    def test_brackets_in_tag(self):
        """Test brackets within tag."""
        result = generate_reasoning_prompt("test", "tag[nested]")
        self.assertIn("[tag[nested]]", result)

    def test_html_content(self):
        """Test HTML-like content."""
        prompt = "<div>Hello <b>World</b></div>"
        result = generate_reasoning_prompt(prompt, "html")
        self.assertIn("<div>", result)
        self.assertIn("</div>", result)

    def test_code_snippet(self):
        """Test code in prompt."""
        prompt = 'def foo():\n    return "bar"'
        result = generate_reasoning_prompt(prompt, "code")
        self.assertIn("def foo():", result)

    def test_json_content(self):
        """Test JSON-like content."""
        prompt = '{"key": "value", "num": 123}'
        result = generate_reasoning_prompt(prompt, "json")
        self.assertIn('"key"', result)

    def test_newline_types(self):
        """Test different newline types."""
        prompt = "A\nB\rC\r\nD"
        result = generate_reasoning_prompt(prompt, "newlines")
        self.assertIn("[newlines]", result)

    def test_tabs(self):
        """Test tab characters."""
        prompt = "Col1\tCol2\tCol3"
        result = generate_reasoning_prompt(prompt, "tabs")
        self.assertIn("\t", result)

    def test_numeric_tag(self):
        """Test numeric tag."""
        result = generate_reasoning_prompt("test", "12345")
        self.assertIn("[12345]", result)

    def test_mixed_case_tag(self):
        """Test mixed case tag."""
        result = generate_reasoning_prompt("test", "MiXeD")
        self.assertIn("[MiXeD]", result)

    def test_output_format(self):
        """Test output format structure."""
        result = generate_reasoning_prompt("prompt", "tag")
        self.assertEqual(result, "[tag] prompt")

    def test_tag_position(self):
        """Test tag appears before prompt."""
        result = generate_reasoning_prompt("after", "before")
        tag_pos = result.find("[before]")
        prompt_pos = result.find("after")
        self.assertLess(tag_pos, prompt_pos)

    def test_single_space_separator(self):
        """Test single space between tag and prompt."""
        result = generate_reasoning_prompt("text", "tag")
        self.assertTrue(result.startswith("[tag] "))

    def test_no_trailing_space_on_empty_prompt(self):
        """Test format when prompt is empty."""
        result = generate_reasoning_prompt("", "tag")
        # Should be "[tag] " with single space
        self.assertEqual(result, "[tag] ")

    def test_idempotent(self):
        """Test deterministic output."""
        r1 = generate_reasoning_prompt("test", "tag")
        r2 = generate_reasoning_prompt("test", "tag")
        self.assertEqual(r1, r2)

    def test_different_prompts_same_tag(self):
        """Test same tag with different prompts."""
        r1 = generate_reasoning_prompt("prompt1", "tag")
        r2 = generate_reasoning_prompt("prompt2", "tag")
        self.assertIn("[tag]", r1)
        self.assertIn("[tag]", r2)
        self.assertNotEqual(r1, r2)

    def test_same_prompt_different_tags(self):
        """Test same prompt with different tags."""
        r1 = generate_reasoning_prompt("prompt", "tag1")
        r2 = generate_reasoning_prompt("prompt", "tag2")
        self.assertNotEqual(r1, r2)

    def test_return_type(self):
        """Test return type is always string."""
        cases = [("a", "b"), ("", ""), ("1", "2")]
        for prompt, tag in cases:
            result = generate_reasoning_prompt(prompt, tag)
            self.assertIsInstance(result, str)

    def test_non_none_return(self):
        """Test never returns None."""
        result = generate_reasoning_prompt("", "")
        self.assertIsNotNone(result)

    def test_escape_sequences(self):
        """Test escape sequences."""
        prompt = "Line\\nWith\\tEscapes"
        result = generate_reasoning_prompt(prompt, "esc")
        self.assertIn(prompt, result)

    def test_single_char_prompt(self):
        """Test single character prompt."""
        result = generate_reasoning_prompt("X", "Y")
        self.assertEqual(result, "[Y] X")

    def test_repeated_chars(self):
        """Test repeated characters."""
        result = generate_reasoning_prompt("aaaa", "bbbb")
        self.assertEqual(result, "[bbbb] aaaa")

    def test_only_punctuation(self):
        """Test only punctuation."""
        result = generate_reasoning_prompt("!!!", "???")
        self.assertEqual(result, "[???] !!!")

    def test_url_in_prompt(self):
        """Test URL in prompt."""
        prompt = "Visit https://example.com/path?q=1"
        result = generate_reasoning_prompt(prompt, "url")
        self.assertIn("https://", result)

    def test_email_in_prompt(self):
        """Test email in prompt."""
        prompt = "user@example.com"
        result = generate_reasoning_prompt(prompt, "email")
        self.assertIn("@", result)

    def test_file_path(self):
        """Test file path."""
        prompt = "/usr/local/bin/python"
        result = generate_reasoning_prompt(prompt, "path")
        self.assertIn(prompt, result)

    def test_regex_pattern(self):
        """Test regex pattern."""
        prompt = r"^\d{3}-\d{4}$"
        result = generate_reasoning_prompt(prompt, "regex")
        self.assertIn(prompt, result)

    def test_sql_query(self):
        """Test SQL query."""
        prompt = "SELECT * FROM users;"
        result = generate_reasoning_prompt(prompt, "sql")
        self.assertIn("SELECT", result)

    def test_multiple_spaces(self):
        """Test multiple consecutive spaces."""
        prompt = "word1     word2"
        result = generate_reasoning_prompt(prompt, "spaces")
        self.assertIn("     ", result)

    def test_leading_spaces_in_prompt(self):
        """Test leading spaces preserved."""
        prompt = "   leading"
        result = generate_reasoning_prompt(prompt, "tag")
        self.assertIn("   leading", result)

    def test_trailing_spaces_in_prompt(self):
        """Test trailing spaces preserved."""
        prompt = "trailing   "
        result = generate_reasoning_prompt(prompt, "tag")
        self.assertIn("trailing   ", result)


class TestGenerateReasoningPromptRealWorld(unittest.TestCase):
    """Real-world scenario tests."""

    def test_code_review_prompt(self):
        """Test code review scenario."""
        prompt = """Review this code:

def divide(a, b):
    return a / b

What issues do you see?"""
        result = generate_reasoning_prompt(prompt, "review")
        self.assertIn("divide", result)
        self.assertIn("[review]", result)

    def test_math_problem(self):
        """Test math problem."""
        prompt = "Solve: 2x + 3 = 11"
        result = generate_reasoning_prompt(prompt, "math")
        self.assertEqual(result, "[math] Solve: 2x + 3 = 11")

    def test_logic_puzzle(self):
        """Test logic puzzle."""
        prompt = "If A>B and B>C, then A>C?"
        result = generate_reasoning_prompt(prompt, "logic")
        self.assertIn("A>B", result)

    def test_creative_writing(self):
        """Test creative writing prompt."""
        prompt = "Write a story about AI"
        result = generate_reasoning_prompt(prompt, "creative")
        self.assertEqual(result, "[creative] Write a story about AI")

    def test_data_analysis(self):
        """Test data analysis prompt."""
        prompt = "Analyze sales: Q1=100K, Q2=150K, Q3=120K"
        result = generate_reasoning_prompt(prompt, "analysis")
        self.assertIn("Q1=100K", result)

    def test_debugging_scenario(self):
        """Test debugging prompt."""
        prompt = "Error: NullPointerException at line 42"
        result = generate_reasoning_prompt(prompt, "debug")
        self.assertIn("Error:", result)

    def test_api_design(self):
        """Test API design prompt."""
        prompt = "Design REST API for user management"
        result = generate_reasoning_prompt(prompt, "api_design")
        self.assertIn("REST API", result)

    def test_security_audit(self):
        """Test security audit prompt."""
        prompt = "Check for SQL injection vulnerabilities"
        result = generate_reasoning_prompt(prompt, "security")
        self.assertIn("SQL injection", result)

    def test_performance_analysis(self):
        """Test performance analysis."""
        prompt = "Function takes 5s with 1000 items"
        result = generate_reasoning_prompt(prompt, "perf")
        self.assertIn("5s", result)

    def test_markdown_doc(self):
        """Test markdown documentation."""
        prompt = "# Header\n## Subheader\n- Item 1"
        result = generate_reasoning_prompt(prompt, "doc")
        self.assertIn("# Header", result)


if __name__ == '__main__':
    unittest.main()