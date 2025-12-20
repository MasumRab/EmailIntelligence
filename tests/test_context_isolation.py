
import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Ensure root is in path
sys.path.insert(0, os.path.abspath("."))

from src.context_control.isolation import ContextIsolator
from src.context_control.models import AgentContext

class TestContextIsolator(unittest.TestCase):
    def setUp(self):
        self.mock_config_patcher = patch('src.context_control.isolation.get_current_config')
        self.mock_config = self.mock_config_patcher.start()
        self.mock_config.return_value = MagicMock()

        self.context = AgentContext(
            profile_id="test",
            agent_id="test_agent",
            environment_type="test",
            accessible_files=["*.py", "src/*"],
            restricted_files=["src/secrets.py"]
        )

    def tearDown(self):
        self.mock_config_patcher.stop()

    def test_compilation(self):
        isolator = ContextIsolator(self.context)
        # Verify patterns are compiled (not None)
        self.assertIsNotNone(isolator._accessible_patterns)
        self.assertIsNotNone(isolator._restricted_patterns)

    def test_empty_patterns(self):
        context = AgentContext(
            profile_id="empty",
            agent_id="empty_agent",
            environment_type="test",
            accessible_files=[],
            restricted_files=[]
        )
        isolator = ContextIsolator(context)
        self.assertIsNone(isolator._accessible_patterns)
        self.assertIsNone(isolator._restricted_patterns)

        self.assertFalse(isolator.is_file_accessible("anything.txt"))

    @patch.object(ContextIsolator, '_normalize_path', side_effect=lambda x: x)
    def test_matching(self, mock_normalize):
        isolator = ContextIsolator(self.context)

        # Allowed
        self.assertTrue(isolator.is_file_accessible("main.py"))
        self.assertTrue(isolator.is_file_accessible("src/utils.py"))

        # Blocked
        self.assertFalse(isolator.is_file_accessible("src/secrets.py"))

        # No match
        self.assertFalse(isolator.is_file_accessible("README.md"))

if __name__ == '__main__':
    unittest.main()
