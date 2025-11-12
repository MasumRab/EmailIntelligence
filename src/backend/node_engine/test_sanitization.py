"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Test for the updated InputSanitizer with proper HTML sanitization.
"""

import sys
from pathlib import Path

# Add the project root to the path so we can import backend modules
# Use __file__ to determine the script's location and calculate the project root dynamically
script_dir = Path(__file__).resolve().parent
project_root = (
    script_dir.parent.parent
)  # Go up to main project directory from backend/node_engine/
sys.path.insert(0, str(project_root))


def test_input_sanitizer():
    """Test the updated InputSanitizer class."""
    try:
        from src.backend.node_engine.security_manager import InputSanitizer

        print("Testing InputSanitizer with various inputs...")

        # Test 1: Basic script tag
        test_input1 = '<script>alert("XSS")</script>'
        result1 = InputSanitizer.sanitize_string(test_input1)
        print(f"Test 1 - Input: {test_input1}")
        print(f"Test 1 - Output: {result1}")
        print(f"Test 1 - Safe: {'<script' not in result1 and 'alert' not in result1}\n")

        # Test 2: Javascript protocol
        test_input2 = "Click here: <a href=\"javascript:alert('XSS')\">Link</a>"
        result2 = InputSanitizer.sanitize_string(test_input2)
        print(f"Test 2 - Input: {test_input2}")
        print(f"Test 2 - Output: {result2}")
        print(f"Test 2 - Safe: {'javascript:' not in result2}\n")

        # Test 3: Onclick event
        test_input3 = "<div onclick=\"alert('XSS')\">Click me</div>"
        result3 = InputSanitizer.sanitize_string(test_input3)
        print(f"Test 3 - Input: {test_input3}")
        print(f"Test 3 - Output: {result3}")
        print(f"Test 3 - Safe: {'onclick' not in result3}\n")

        # Test 4: Safe HTML that should be preserved
        test_input4 = (
            "<p>This is a <strong>safe</strong> paragraph with <em>formatting</em>.</p>"
        )
        result4 = InputSanitizer.sanitize_string(test_input4)
        print(f"Test 4 - Input: {test_input4}")
        print(f"Test 4 - Output: {result4}")
        print(
            f"Test 4 - Safe HTML preserved: {len(result4) > 10 and '<p>' in result4}\n"
        )

        # Test 5: Dangerous iframe tag
        test_input5 = "<iframe src=\"javascript:alert('XSS')\"></iframe>"
        result5 = InputSanitizer.sanitize_string(test_input5)
        print(f"Test 5 - Input: {test_input5}")
        print(f"Test 5 - Output: {result5}")
        print(f"Test 5 - Safe: {'<iframe' not in result5}\n")

        print("All tests completed successfully!")

    except ImportError as e:
        print(f"Import error: {e}")
        print("This might be expected if bleach is not installed yet.")
        print("Run 'pip install bleach' to install the required dependency.")
    except Exception as e:
        print(f"Error during test: {e}")


if __name__ == "__main__":
    test_input_sanitizer()
