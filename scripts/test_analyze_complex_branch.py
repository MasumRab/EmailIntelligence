import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import scripts.analyze_complex_branch as analyzer

class TestAnalyzeComplexBranch(unittest.TestCase):

    @patch('subprocess.run')
    def test_simple_branch(self, mock_run):
        def side_effect(command, *args, **kwargs):
            mock = MagicMock()
            if "--is-ancestor" in command:
                mock.returncode = 0 # Not divergent
            elif "--merges" in command:
                mock.stdout = "0\n"
                mock.returncode = 0
            elif "--count" in command:
                mock.stdout = "5\n"
                mock.returncode = 0
            elif "--name-only" in command:
                mock.stdout = "file1.txt\nfile2.txt\n"
                mock.returncode = 0
            return mock
            
        mock_run.side_effect = side_effect
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        analyzer.analyze_branch("feature-branch", "main")
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("SIMPLE", output)
        self.assertIn("FAST-FORWARD MERGE", output)
        self.assertNotIn("COMPLEX", output)

    @patch('subprocess.run')
    def test_divergent_simple_branch(self, mock_run):
        def side_effect(command, *args, **kwargs):
            mock = MagicMock()
            if "--is-ancestor" in command:
                mock.returncode = 1 # Divergent
            elif "--merges" in command:
                mock.stdout = "0\n"
                mock.returncode = 0
            elif "--count" in command:
                mock.stdout = "5\n"
                mock.returncode = 0
            elif "--name-only" in command:
                mock.stdout = "file1.txt\nfile2.txt\n"
                mock.returncode = 0
            return mock
            
        mock_run.side_effect = side_effect
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        analyzer.analyze_branch("feature-branch", "main")
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("SIMPLE", output)
        self.assertIn("STANDARD REBASE", output)
        self.assertNotIn("COMPLEX", output)

    @patch('subprocess.run')
    def test_complex_branch_with_merges(self, mock_run):
        def side_effect(command, *args, **kwargs):
            mock = MagicMock()
            if "--is-ancestor" in command:
                mock.returncode = 1 # Divergent
            elif "--merges" in command:
                mock.stdout = "2\n" # Has merge commits
                mock.returncode = 0
            elif "--count" in command:
                mock.stdout = "20\n"
                mock.returncode = 0
            elif "--name-only" in command:
                mock.stdout = "file1.txt\nfile2.txt\n"
                mock.returncode = 0
            return mock
            
        mock_run.side_effect = side_effect
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        analyzer.analyze_branch("feature-branch", "main")
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("COMPLEX", output)
        self.assertIn("MULTILEVEL ITERATIVE REBASE", output)

    @patch('subprocess.run')
    def test_complex_branch_many_commits(self, mock_run):
        def side_effect(command, *args, **kwargs):
            mock = MagicMock()
            if "--is-ancestor" in command:
                mock.returncode = 1 # Divergent
            elif "--merges" in command:
                mock.stdout = "0\n"
                mock.returncode = 0
            elif "--count" in command:
                mock.stdout = "60\n" # Over threshold (50)
                mock.returncode = 0
            elif "--name-only" in command:
                mock.stdout = "file1.txt\nfile2.txt\n"
                mock.returncode = 0
            return mock
            
        mock_run.side_effect = side_effect
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        analyzer.analyze_branch("feature-branch", "main")
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("COMPLEX", output)
        self.assertIn("MULTILEVEL ITERATIVE REBASE", output)
        
if __name__ == '__main__':
    unittest.main()
