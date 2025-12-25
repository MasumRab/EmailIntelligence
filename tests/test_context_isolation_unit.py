
import unittest
from unittest.mock import patch
from src.context_control.isolation import ContextIsolator
from src.context_control.models import AgentContext
from src.context_control.config import init_config
import re
import os

class TestContextIsolatorOptimized(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_config()

    def setUp(self):
        self.context = AgentContext(
            agent_id="test_agent",
            profile_id="default",
            environment_type="dev",
            accessible_files=["src/*.py", "tests/*.py"],
            restricted_files=["secrets.json", "*.env"]
        )
        # Patch normalize_path to be a pass-through to avoid absolute path issues
        # during unit testing of regex matching logic
        self.patcher = patch.object(ContextIsolator, '_normalize_path', side_effect=lambda x: x)
        self.patcher.start()

        self.isolator = ContextIsolator(self.context)

    def tearDown(self):
        self.patcher.stop()

    def test_accessible_patterns(self):
        # Should match
        self.assertTrue(self.isolator.is_file_accessible("src/main.py"))
        self.assertTrue(self.isolator.is_file_accessible("tests/test_main.py"))

        # Should not match (restricted)
        self.assertFalse(self.isolator.is_file_accessible("secrets.json"))
        self.assertFalse(self.isolator.is_file_accessible("prod.env"))

        # Should not match (not in accessible list)
        self.assertFalse(self.isolator.is_file_accessible("README.md"))

    def test_empty_patterns(self):
        empty_context = AgentContext(
            agent_id="empty",
            profile_id="default",
            environment_type="dev",
            accessible_files=[],
            restricted_files=[]
        )
        isolator = ContextIsolator(empty_context)
        self.assertFalse(isolator.is_file_accessible("anything.py"))

if __name__ == "__main__":
    unittest.main()
