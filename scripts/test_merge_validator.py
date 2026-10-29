import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add scripts directory to path to import merge_validator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from merge_validator import check_concurrent_changes, safe_ref

def _run(stdout="", rc=0):
    return MagicMock(stdout=stdout, stderr="", returncode=rc)

class TestMergeValidator(unittest.TestCase):
    def test_safe_ref(self):
        self.assertEqual(safe_ref('refs/heads/main'), 'refs/heads/main')
        
        with self.assertRaises(ValueError):
            safe_ref('-x')
        with self.assertRaises(ValueError):
            safe_ref('a b')
        with self.assertRaises(ValueError):
            safe_ref('HEAD~1')

    @patch('merge_validator.subprocess.run')
    def test_conflict_detected(self, mock_run):
        mock_run.side_effect = [
            _run("abc123\n"),        # git merge-base
            _run("a.py\nb.py\n"),    # target changed
            _run("b.py\nc.py\n"),    # source changed
        ]
        self.assertTrue(check_concurrent_changes("source", "target"))
        self.assertEqual(mock_run.call_count, 3)

    @patch('merge_validator.subprocess.run')
    def test_no_conflict(self, mock_run):
        mock_run.side_effect = [_run("abc123\n"), _run("a.py\n"), _run("b.py\n")]
        self.assertFalse(check_concurrent_changes("source", "target"))

    def test_invalid_ref_raises(self):
        with self.assertRaises(ValueError):
            check_concurrent_changes("-invalid", "main")

if __name__ == '__main__':
    unittest.main()
