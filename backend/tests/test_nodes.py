import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add the agent module path so we can import nodes
# This handles the __file__.resolve().parents[3] correctly based on our test's location
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "agent"))

try:
    from nodes import _get_active_context, generate_plan, MAX_CONTEXT_LENGTH, CONTEXT_FILE
except ImportError:
    # If not found directly, try relative import assuming standard PYTHONPATH
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from backend.src.agent.nodes import _get_active_context, generate_plan, MAX_CONTEXT_LENGTH, CONTEXT_FILE


class TestNodesActiveContext(unittest.TestCase):

    def setUp(self):
        # We ensure docs/ exists relative to where the code runs, although the test is mocked out mostly
        if not CONTEXT_FILE.parent.exists():
            CONTEXT_FILE.parent.mkdir(parents=True)

    def tearDown(self):
        if CONTEXT_FILE.exists():
            CONTEXT_FILE.unlink()

    def test_get_active_context_missing_file(self):
        if CONTEXT_FILE.exists():
            CONTEXT_FILE.unlink()

        result = _get_active_context()
        self.assertEqual(result, "*Context file not found*")

    def test_get_active_context_reads_content(self):
        test_content = "# Active GitHub Context\n- `src/main.py` (modified)"
        CONTEXT_FILE.write_text(test_content, encoding="utf-8")

        result = _get_active_context()
        self.assertEqual(result, test_content)

    def test_get_active_context_truncates_long_content(self):
        # Create content longer than MAX_CONTEXT_LENGTH
        long_content = "A" * (MAX_CONTEXT_LENGTH + 100)
        CONTEXT_FILE.write_text(long_content, encoding="utf-8")

        result = _get_active_context()

        # It should end with the truncation indicator
        self.assertTrue(result.endswith("...[TRUNCATED: Additional PR context hidden to prevent context overflow]..."))
        # Total length should be exactly MAX_CONTEXT_LENGTH
        self.assertEqual(len(result), MAX_CONTEXT_LENGTH)
        # The beginning should still be 'A's
        self.assertTrue(result.startswith("A" * 100))

    def test_generate_plan_injects_context(self):
        test_content = "# Active GitHub Context\n- `src/main.py` (modified)"
        CONTEXT_FILE.write_text(test_content, encoding="utf-8")

        prompt = "Fix the authentication bug."
        plan_payload = generate_plan(prompt)

        # Check if the active context is in the generated payload
        self.assertIn(test_content, plan_payload)
        # Check if the user prompt is in the generated payload
        self.assertIn(prompt, plan_payload)
        # Check if the warning is present
        self.assertIn("DO NOT DUPLICATE WORK IN THESE FILES", plan_payload)

if __name__ == "__main__":
    unittest.main()
