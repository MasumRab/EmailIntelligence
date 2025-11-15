"""
Unit tests for the WorkflowContextManager.
"""

import unittest
from src.lib.workflow_context import WorkflowContextManager

class TestWorkflowContextManager(unittest.TestCase):
    """
    Tests for the WorkflowContextManager class.
    """

    def test_initialization(self):
        """
        Test that the WorkflowContextManager can be initialized.
        """
        try:
            manager = WorkflowContextManager()
            self.assertIsNotNone(manager)
        except Exception as e:
            self.fail(f"WorkflowContextManager initialization failed with an error: {e}")

    def test_initial_stage(self):
        """
        Test that the initial stage is set correctly.
        """
        manager = WorkflowContextManager()
        self.assertEqual(manager.stage, "INITIAL")

    def test_context_management_protocol(self):
        """
        Test that the class works as a context manager.
        """
        try:
            with WorkflowContextManager() as guide:
                self.assertIsInstance(guide, WorkflowContextManager)
                self.assertEqual(guide.stage, "INITIAL")
        except Exception as e:
            self.fail(f"Using WorkflowContextManager as a context manager failed: {e}")

if __name__ == '__main__':
    unittest.main()
