import unittest
from unittest.mock import patch
import sys
import os

# Add scripts directory to path to import merge_validator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from merge_validator import check_concurrent_changes

class TestMergeValidator(unittest.TestCase):

    @patch('merge_validator.run_git_command')
    def test_no_concurrent_changes(self, mock_run_git_command):
        # Mock behavior for git commands
        def side_effect(args):
            if args[0] == "merge-base":
                return "abcdef123456"
            elif args[0] == "diff" and "target" in args[2]:
                return "file1.txt\nfile2.txt"
            elif args[0] == "diff" and "source" in args[2]:
                return "file3.txt\nfile4.txt"
            return ""

        mock_run_git_command.side_effect = side_effect

        # Should return False (no conflicts)
        result = check_concurrent_changes("source", "target")
        self.assertFalse(result)

    @patch('merge_validator.run_git_command')
    def test_with_concurrent_changes(self, mock_run_git_command):
        def side_effect(args):
            if args[0] == "merge-base":
                return "abcdef123456"
            elif args[0] == "diff" and "target" in args[2]:
                return "file1.txt\nfile2.txt\ncommon.txt"
            elif args[0] == "diff" and "source" in args[2]:
                return "file3.txt\ncommon.txt"
            return ""

        mock_run_git_command.side_effect = side_effect

        # Should return True (conflicts exist)
        result = check_concurrent_changes("source", "target")
        self.assertTrue(result)

    @patch('merge_validator.run_git_command')
    def test_no_changes(self, mock_run_git_command):
        def side_effect(args):
            if args[0] == "merge-base":
                return "abcdef123456"
            elif args[0] == "diff":
                return "" # No files changed
            return ""

        mock_run_git_command.side_effect = side_effect

        # Should return False (no conflicts)
        result = check_concurrent_changes("source", "target")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
