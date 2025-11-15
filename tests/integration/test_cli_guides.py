import unittest
from unittest.mock import patch, call
from io import StringIO
import sys

from setup.commands.guide_dev_command import GuideDevCommand
from setup.commands.guide_pr_command import GuidePrCommand

class TestCliGuides(unittest.TestCase):
    """
    Integration tests for the CLI guide commands.
    """

    def setUp(self):
        # Redirect stdout to capture print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.captured_stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('builtins.input', side_effect=['1'])
    def test_guide_dev_app_code_workflow(self, mock_input):
        """
        Test the 'application code' path of the guide-dev workflow.
        """
        command = GuideDevCommand()
        return_code = command.execute()
        
        output = self.captured_stdout.getvalue()
        self.assertEqual(return_code, 0)
        self.assertIn("Application Code Workflow", output)
        self.assertIn("No special commands are needed", output)

    @patch('setup.commands.guide_dev_command.GuideDevCommand._get_current_branch')
    @patch('builtins.input', side_effect=['2'])
    def test_guide_dev_orchestration_code_safe(self, mock_input, mock_get_branch):
        """
        Test the 'shared config' path when on the correct branch.
        """
        mock_get_branch.return_value = 'orchestration-tools'
        
        command = GuideDevCommand()
        return_code = command.execute()

        output = self.captured_stdout.getvalue()
        self.assertEqual(return_code, 0)
        self.assertIn("Shared Config Workflow", output)
        self.assertIn("You are on the 'orchestration-tools' branch.", output)
        self.assertIn("It is safe to edit", output)

    @patch('setup.commands.guide_dev_command.GuideDevCommand._get_current_branch')
    @patch('builtins.input', side_effect=['2'])
    def test_guide_dev_orchestration_code_unsafe(self, mock_input, mock_get_branch):
        """
        Test the 'shared config' path when on the wrong branch.
        """
        mock_get_branch.return_value = 'feature/some-feature'

        command = GuideDevCommand()
        return_code = command.execute()

        output = self.captured_stdout.getvalue()
        self.assertEqual(return_code, 0)
        self.assertIn("Shared Config Workflow", output)
        self.assertIn("You are currently on the 'feature/some-feature' branch", output)
        self.assertIn("Changes to shared files on this branch will be overwritten by the sync hooks", output)

    @patch('builtins.input', side_effect=['q'])
    def test_guide_dev_quit(self, mock_input):
        """
        Test quitting the guide-dev workflow.
        """
        command = GuideDevCommand()
        return_code = command.execute()

        output = self.captured_stdout.getvalue()
        self.assertEqual(return_code, 0)
        self.assertIn("Exiting guide.", output)

    # --- Tests for guide-pr ---

    @patch('builtins.input', side_effect=['1'])
    def test_guide_pr_orchestration_workflow(self, mock_input):
        """
        Test the 'orchestration change' path of the guide-pr workflow.
        """
        command = GuidePrCommand()
        return_code = command.execute()
        
        output = self.captured_stdout.getvalue()
        self.assertEqual(return_code, 0)
        self.assertIn("Orchestration Change Merge Workflow", output)
        self.assertIn("DO NOT use a standard 'git merge'", output)
        self.assertIn("reverse_sync_orchestration.sh", output)

    @patch('builtins.input', side_effect=['2'])
    def test_guide_pr_app_code_workflow(self, mock_input):
        """
        Test the 'application code' path of the guide-pr workflow.
        """
        command = GuidePrCommand()
        return_code = command.execute()
        
        output = self.captured_stdout.getvalue()
        self.assertEqual(return_code, 0)
        self.assertIn("Application Feature Merge Workflow", output)
        self.assertIn("You can use 'git merge'", output)
        self.assertIn("final_merge_approach.md", output)

if __name__ == '__main__':
    unittest.main()
