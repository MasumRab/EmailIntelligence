import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path to import merge_validator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from merge_validator import check_concurrent_changes, is_safe_ref

class TestMergeValidator(unittest.TestCase):
    def test_is_safe_ref(self):
        self.assertEqual(is_safe_ref("main"), "main")
        self.assertEqual(is_safe_ref("feature/branch-123"), "feature/branch-123")
        self.assertEqual(is_safe_ref("refs/heads/main"), "refs/heads/main")
        self.assertEqual(is_safe_ref("abcdef123456"), "abcdef123456")
        
        with self.assertRaises(SystemExit):
            is_safe_ref("-main")
        with self.assertRaises(SystemExit):
            is_safe_ref("main; echo 'evil'")
        with self.assertRaises(SystemExit):
            is_safe_ref("feature branch")

    @patch('subprocess.run')
    def test_no_concurrent_changes(self, mock_subprocess_run):
        # Mock behavior for subprocess.run
        def side_effect(*args, **kwargs):
            cmd = args[0]
            mock_result = MagicMock()
            if cmd[1] == "merge-base":
                mock_result.stdout = "abcdef123456"
            elif cmd[1] == "diff" and "target" in cmd[4]:
                mock_result.stdout = "file1.txt\nfile2.txt"
            elif cmd[1] == "diff" and "source" in cmd[4]:
                mock_result.stdout = "file3.txt\nfile4.txt"
            else:
                mock_result.stdout = ""
            return mock_result

        mock_subprocess_run.side_effect = side_effect

        # Should return False (no conflicts)
        result = check_concurrent_changes("source", "target")
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_with_concurrent_changes(self, mock_subprocess_run):
        def side_effect(*args, **kwargs):
            cmd = args[0]
            mock_result = MagicMock()
            if cmd[1] == "merge-base":
                mock_result.stdout = "abcdef123456"
            elif cmd[1] == "diff" and "target" in cmd[4]:
                mock_result.stdout = "file1.txt\nfile2.txt\ncommon.txt"
            elif cmd[1] == "diff" and "source" in cmd[4]:
                mock_result.stdout = "file3.txt\ncommon.txt"
            else:
                mock_result.stdout = ""
            return mock_result

        mock_subprocess_run.side_effect = side_effect

        # Should return True (conflicts exist)
        result = check_concurrent_changes("source", "target")
        self.assertTrue(result)

    @patch('subprocess.run')
    def test_no_changes(self, mock_subprocess_run):
        def side_effect(*args, **kwargs):
            cmd = args[0]
            mock_result = MagicMock()
            if cmd[1] == "merge-base":
                mock_result.stdout = "abcdef123456"
            elif cmd[1] == "diff":
                mock_result.stdout = "" # No files changed
            else:
                mock_result.stdout = ""
            return mock_result

        mock_subprocess_run.side_effect = side_effect

        # Should return False (no conflicts)
        result = check_concurrent_changes("source", "target")
        self.assertFalse(result)
        
    def test_invalid_branch_name(self):
        with self.assertRaises(SystemExit):
            check_concurrent_changes("-invalid", "main")

if __name__ == '__main__':
    unittest.main()
