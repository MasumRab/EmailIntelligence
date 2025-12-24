
import unittest
from unittest.mock import MagicMock, patch
import os
from src.context_control.isolation import ContextIsolator
from src.context_control.models import AgentContext

class TestContextIsolator(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_context = MagicMock(spec=AgentContext)
        self.mock_context.agent_id = "test_agent"
        self.mock_context.access_log = []

        # Default empty patterns
        self.mock_context.restricted_files = []
        self.mock_context.accessible_files = []

        self.mock_config = MagicMock()

    def test_accessible_patterns(self):
        # Setup specific patterns
        self.mock_context.accessible_files = ["src/*.py", "README.md"]
        self.mock_context.restricted_files = []

        isolator = ContextIsolator(self.mock_context, self.mock_config)

        # Test accessible files
        # Note: We mock _normalize_path to return the path as-is to avoid OS dependency in unit test
        with patch.object(isolator, '_normalize_path', side_effect=lambda x: x):
            self.assertTrue(isolator.is_file_accessible("src/main.py"))
            self.assertTrue(isolator.is_file_accessible("README.md"))

            # Test non-accessible files
            self.assertFalse(isolator.is_file_accessible("src/data.json"))
            self.assertFalse(isolator.is_file_accessible("setup.py"))

    def test_restricted_patterns(self):
        self.mock_context.accessible_files = ["src/*"]
        self.mock_context.restricted_files = ["src/secret.py"]

        isolator = ContextIsolator(self.mock_context, self.mock_config)

        with patch.object(isolator, '_normalize_path', side_effect=lambda x: x):
            # Should be blocked despite matching accessible pattern
            self.assertFalse(isolator.is_file_accessible("src/secret.py"))

            # Should be accessible
            self.assertTrue(isolator.is_file_accessible("src/other.py"))

    def test_no_patterns(self):
        self.mock_context.accessible_files = []
        self.mock_context.restricted_files = []

        isolator = ContextIsolator(self.mock_context, self.mock_config)

        with patch.object(isolator, '_normalize_path', side_effect=lambda x: x):
            self.assertFalse(isolator.is_file_accessible("anything.py"))

    def test_filename_matching(self):
        # The current implementation (and the optimized one) checks against full path AND filename
        self.mock_context.accessible_files = ["config.py"]

        isolator = ContextIsolator(self.mock_context, self.mock_config)

        with patch.object(isolator, '_normalize_path', side_effect=lambda x: x):
            self.assertTrue(isolator.is_file_accessible("/path/to/config.py"))

if __name__ == '__main__':
    unittest.main()
