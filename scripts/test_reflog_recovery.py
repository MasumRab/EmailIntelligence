import unittest
from unittest.mock import patch, MagicMock
import json
import subprocess
from reflog_recovery import get_reflog_history, generate_restore_command, analyze_recovery_options

class TestReflogRecovery(unittest.TestCase):
    
    @patch('subprocess.run')
    def test_get_reflog_history_success(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "a1b2c3d|commit: Add new feature\ne4f5g6h|commit: Fix bug"
        mock_run.return_value = mock_result
        
        entries = get_reflog_history("main", 2)
        
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["hash"], "a1b2c3d")
        self.assertEqual(entries[0]["message"], "commit: Add new feature")
        self.assertEqual(entries[1]["hash"], "e4f5g6h")
        self.assertEqual(entries[1]["message"], "commit: Fix bug")
        
        mock_run.assert_called_once_with(
            ['git', 'reflog', 'show', 'main', '-n', '2', '--format=%h|%gs'],
            capture_output=True,
            text=True,
            check=True
        )
        
    @patch('subprocess.run')
    def test_get_reflog_history_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git', stderr="fatal: ambiguous argument 'main'")
        
        entries = get_reflog_history("main")
        self.assertEqual(entries, [])
        
    def test_generate_restore_command(self):
        cmd = generate_restore_command("feature-branch", "a1b2c3d")
        self.assertEqual(cmd, "git branch -f feature-branch a1b2c3d")
        
    @patch('reflog_recovery.get_reflog_history')
    def test_analyze_recovery_options(self, mock_get_history):
        mock_get_history.return_value = [
            {"hash": "a1b2c3d", "message": "commit: Add new feature"},
            {"hash": "e4f5g6h", "message": "commit: Fix bug"}
        ]
        
        result = analyze_recovery_options("main")
        
        self.assertEqual(result["branch"], "main")
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["recovery_options"]), 2)
        
        opt0 = result["recovery_options"][0]
        self.assertEqual(opt0["index"], 0)
        self.assertEqual(opt0["commit_hash"], "a1b2c3d")
        self.assertEqual(opt0["restore_command"], "git branch -f main a1b2c3d")
        
    @patch('reflog_recovery.get_reflog_history')
    def test_analyze_recovery_options_no_history(self, mock_get_history):
        mock_get_history.return_value = []
        
        result = analyze_recovery_options("unknown-branch")
        
        self.assertEqual(result["branch"], "unknown-branch")
        self.assertEqual(result["status"], "error")
        self.assertTrue("No reflog history found" in result["message"])

if __name__ == '__main__':
    unittest.main()
