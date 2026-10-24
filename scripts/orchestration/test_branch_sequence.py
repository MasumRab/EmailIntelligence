import unittest
from unittest.mock import patch, MagicMock
import subprocess

from scripts.orchestration.branch_sequence import check_branch_status, process_branches

class TestBranchSequence(unittest.TestCase):
    @patch('subprocess.run')
    def test_clean_branch(self, mock_run):
        base_mock = MagicMock(stdout='base_sha\n', returncode=0)
        tree_mock = MagicMock(stdout='some output', returncode=0)
        mock_run.side_effect = [base_mock, tree_mock]
        self.assertEqual(check_branch_status('clean_branch'), 'clean')

    @patch('subprocess.run')
    def test_conflicting_branch(self, mock_run):
        base_mock = MagicMock(stdout='base_sha\n', returncode=0)
        tree_mock = MagicMock(stdout='<<<<<<< HEAD\n===\n>>>>>>>', returncode=0)
        mock_run.side_effect = [base_mock, tree_mock]
        self.assertEqual(check_branch_status('conflict_branch'), 'conflicting')

    @patch('subprocess.run')
    def test_error_branch(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
        self.assertEqual(check_branch_status('error_branch'), 'error')

    @patch('scripts.orchestration.branch_sequence.check_branch_status')
    def test_process_branches(self, mock_check):
        mock_check.side_effect = ['clean', 'conflicting']
        results = process_branches(['b1', 'b2'])
        self.assertEqual(results, {'b1': 'clean', 'b2': 'conflicting'})

if __name__ == '__main__':
    unittest.main()
