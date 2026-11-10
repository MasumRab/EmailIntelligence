import unittest
from unittest.mock import patch, MagicMock
import subprocess

from scripts.orchestration.branch_sequence import check_branch_status, process_branches


class TestBranchSequence(unittest.TestCase):
    @patch('subprocess.run')
    def test_clean_branch(self, mock_run):
        mock_run.return_value = MagicMock(stdout='tree oid\n', returncode=0)
        self.assertEqual(check_branch_status('clean_branch'), 'clean')

    @patch('subprocess.run')
    def test_conflicting_branch(self, mock_run):
        # A conflict leaves the merged tree id as the first stdout line.
        mock_run.return_value = MagicMock(
            stdout='1234567890abcdef1234567890abcdef12345678\n'
                   '100644 5626abf 1\tf.txt\n',
            stderr='',
            returncode=1,
        )
        self.assertEqual(check_branch_status('conflict_branch'), 'conflicting')

    @patch('subprocess.run')
    def test_error_branch(self, mock_run):
        # A failure to compute is not a conflict: exit 2 must not read as "conflicting".
        mock_run.return_value = MagicMock(stdout='', stderr='', returncode=2)
        self.assertEqual(check_branch_status('error_branch'), 'error')

    @patch('subprocess.run')
    def test_missing_branch_is_an_error_not_a_conflict(self, mock_run):
        # `git merge-tree --write-tree main nope` also exits 1, with no tree id.
        mock_run.return_value = MagicMock(
            stdout='',
            stderr='merge-tree: nope - not something we can merge\n',
            returncode=1,
        )
        self.assertEqual(check_branch_status('nope'), 'error')

    @patch('subprocess.run')
    def test_unsafe_ref_is_rejected_without_running_git(self, mock_run):
        self.assertEqual(check_branch_status('--upload-pack=evil'), 'error')
        mock_run.assert_not_called()

    @patch('scripts.orchestration.branch_sequence.check_branch_status')
    def test_process_branches(self, mock_check):
        mock_check.side_effect = ['clean', 'conflicting']
        results = process_branches(['b1', 'b2'])
        self.assertEqual(results, {'b1': 'clean', 'b2': 'conflicting'})


if __name__ == '__main__':
    unittest.main()
