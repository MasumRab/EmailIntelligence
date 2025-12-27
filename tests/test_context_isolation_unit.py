
import unittest
import os
import re
from typing import List, Pattern, Optional
from src.context_control.isolation import ContextIsolator
from src.context_control.models import AgentContext
from unittest.mock import MagicMock, patch

class TestContextIsolator(unittest.TestCase):
    def setUp(self):
        # Mock Context
        self.context = MagicMock(spec=AgentContext)
        self.context.agent_id = "test_agent"
        self.context.profile_id = "default"
        self.context.restricted_files = ["*.secret", "config.json"]
        self.context.accessible_files = ["src/*.py", "README.md", "docs/**/*"]
        self.context.access_log = []

        with patch('src.context_control.isolation.get_current_config'), \
             patch('src.context_control.isolation.get_context_logger'):
            self.isolator = ContextIsolator(self.context)

    def test_compile_patterns_returns_single_regex(self):
        # Access private method for testing
        patterns = ["*.py", "*.txt"]
        compiled = self.isolator._compile_patterns(patterns)

        # Optimized implementation returns a single compiled Pattern
        self.assertIsInstance(compiled, re.Pattern)

        # Verify it matches both types
        self.assertTrue(compiled.match("test.py"))
        self.assertTrue(compiled.match("test.txt"))
        self.assertFalse(compiled.match("test.js"))

    def test_file_access(self):
        # We need to mock _normalize_path because os.path.realpath will resolve to absolute path
        # and our patterns are relative glob patterns.
        # In a real scenario, patterns might be absolute or we rely on filename match.

        with patch.object(self.isolator, '_normalize_path', side_effect=lambda x: x):
            # Test restricted
            self.assertFalse(self.isolator.is_file_accessible("data.secret"))
            self.assertFalse(self.isolator.is_file_accessible("config.json"))

            # Test accessible
            self.assertTrue(self.isolator.is_file_accessible("src/main.py"))
            self.assertTrue(self.isolator.is_file_accessible("README.md"))

            # Test default deny
            self.assertFalse(self.isolator.is_file_accessible("random.bin"))

    def test_matches_patterns(self):
        pattern = self.isolator._compile_patterns(["*.py"])
        self.assertTrue(self.isolator._matches_patterns("test.py", pattern))
        self.assertFalse(self.isolator._matches_patterns("test.txt", pattern))

        # Test filename fallback
        self.assertTrue(self.isolator._matches_patterns("/path/to/test.py", pattern))

if __name__ == '__main__':
    unittest.main()
