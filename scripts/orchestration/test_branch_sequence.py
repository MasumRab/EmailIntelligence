import unittest
from unittest.mock import patch, MagicMock
import subprocess

import os
import tempfile
import shutil

from scripts.orchestration.branch_sequence import check_branch_status, process_branches

class TestBranchSequenceRealGit(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        subprocess.run(["git", "init", "-b", "main"], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        
        with open("file.txt", "w") as f:
            f.write("initial\n")
        subprocess.run(["git", "add", "file.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "initial"], check=True)
        
        subprocess.run(["git", "checkout", "-b", "clean_branch"], check=True)
        with open("file2.txt", "w") as f:
            f.write("clean\n")
        subprocess.run(["git", "add", "file2.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "clean"], check=True)
        
        subprocess.run(["git", "checkout", "main"], check=True)
        subprocess.run(["git", "checkout", "-b", "conflict_branch"], check=True)
        with open("file.txt", "w") as f:
            f.write("conflict\n")
        subprocess.run(["git", "add", "file.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "conflict"], check=True)
        
        subprocess.run(["git", "checkout", "main"], check=True)
        with open("file.txt", "w") as f:
            f.write("main_change\n")
        subprocess.run(["git", "add", "file.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "main change"], check=True)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_real_git_clean(self):
        self.assertEqual(check_branch_status("clean_branch"), "clean")

    def test_real_git_conflict(self):
        self.assertEqual(check_branch_status("conflict_branch"), "conflicting")

    def test_real_git_unknown_branch(self):
        self.assertEqual(check_branch_status("no-such-branch-xyz"), "error")

class TestBranchSequence(unittest.TestCase):
    @patch('subprocess.run')
    def test_clean_branch(self, mock_run):
        base_mock = MagicMock(stdout='base_sha\n', returncode=0)
        tree_mock = MagicMock(stdout='some output', returncode=0)
        mock_run.side_effect = [base_mock, tree_mock]
        self.assertEqual(check_branch_status('clean_branch'), 'clean')

    @patch('subprocess.run')
    def test_conflicting_branch(self, mock_run):
        rev_mock = MagicMock(returncode=0)
        tree_mock = MagicMock(stdout='', returncode=1)
        mock_run.side_effect = [rev_mock, tree_mock]
        self.assertEqual(check_branch_status('conflict_branch'), 'conflicting')

    @patch('subprocess.run')
    def test_error_branch(self, mock_run):
        rev_mock = MagicMock(returncode=0)
        tree_mock = MagicMock(stdout='', returncode=2)
        mock_run.side_effect = [rev_mock, tree_mock]
        self.assertEqual(check_branch_status('error_branch'), 'error')

    @patch('scripts.orchestration.branch_sequence.check_branch_status')
    def test_process_branches(self, mock_check):
        mock_check.side_effect = ['clean', 'conflicting']
        results = process_branches(['b1', 'b2'])
        self.assertEqual(results, {'b1': 'clean', 'b2': 'conflicting'})

if __name__ == '__main__':
    unittest.main()
