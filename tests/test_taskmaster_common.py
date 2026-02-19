"""
Tests for shared utilities in task_scripts/taskmaster_common.py
"""
import unittest
from pathlib import Path
import sys
import os

# Add the parent directory to path to import task_scripts
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from task_scripts.taskmaster_common import SecurityValidator

class TestTaskmasterCommon(unittest.TestCase):
    def test_validate_path_security_types(self):
        """Test that validate_path_security handles both str and Path objects."""
        test_file = "tasks/tasks.json"
        test_path = Path(test_file)
        
        # Test with string
        self.assertTrue(SecurityValidator.validate_path_security(test_file))
        
        # Test with Path object (this used to raise TypeError)
        self.assertTrue(SecurityValidator.validate_path_security(test_path))

    def test_validate_path_security_suspicious(self):
        """Test detection of truly suspicious patterns."""
        # Null byte
        self.assertFalse(SecurityValidator.validate_path_security("file\x00.txt"))
        
        # Directory traversal
        self.assertFalse(SecurityValidator.validate_path_security("../../../etc/passwd"))
        
        # Command substitution
        self.assertFalse(SecurityValidator.validate_path_security("file$(whoami).txt"))

if __name__ == '__main__':
    unittest.main()
