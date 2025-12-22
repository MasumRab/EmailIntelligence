import sys
import os
import unittest
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("src"))

from context_control.isolation import ContextIsolator
from context_control.models import AgentContext
from context_control.config import init_config

class TestContextIsolator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_config()

    def setUp(self):
        self.context = AgentContext(
            profile_id="test",
            agent_id="test_agent",
            environment_type="test",
            accessible_files=["*.py", "src/allowed/*.txt"],
            restricted_files=["secret_*.py", "src/restricted/*"]
        )
        self.isolator = ContextIsolator(self.context)
        # Mock _normalize_path to return path as-is for testing relative pattern matching
        # This mirrors how the class is tested in other suites and avoids absolute path issues
        self.isolator._normalize_path = lambda p: p

    def test_accessible_files(self):
        # Should match *.py
        self.assertTrue(self.isolator.is_file_accessible("main.py"))
        self.assertTrue(self.isolator.is_file_accessible("src/utils.py"))

        # Should match src/allowed/*.txt
        self.assertTrue(self.isolator.is_file_accessible("src/allowed/readme.txt"))

        # Should not match other extensions
        self.assertFalse(self.isolator.is_file_accessible("README.md"))
        self.assertFalse(self.isolator.is_file_accessible("src/image.png"))

    def test_restricted_files(self):
        # Restricted takes precedence

        # secret_key.py matches *.py (accessible) AND secret_*.py (restricted)
        # Should be False
        self.assertFalse(self.isolator.is_file_accessible("secret_key.py"))

        # src/restricted/data.py matches *.py (accessible) AND src/restricted/* (restricted)
        self.assertFalse(self.isolator.is_file_accessible("src/restricted/data.py"))

    def test_empty_patterns(self):
        context = AgentContext(
            profile_id="empty",
            agent_id="empty",
            environment_type="test",
            accessible_files=[],
            restricted_files=[]
        )
        isolator = ContextIsolator(context)

        # Nothing accessible by default
        self.assertFalse(isolator.is_file_accessible("any.file"))

    def test_filename_matching(self):
        # ContextIsolator matches against full path OR filename
        # patterns=["*.py"]

        # Path: /abs/path/to/script.py -> basename script.py matches *.py
        self.assertTrue(self.isolator.is_file_accessible("/abs/path/to/script.py"))

if __name__ == "__main__":
    unittest.main()
