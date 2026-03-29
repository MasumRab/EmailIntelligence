import unittest
from unittest.mock import MagicMock
from src.services.rebase_analyzer import RebaseAnalyzer
from src.models.analysis import Intention, Commit
from datetime import datetime

class TestRebaseAnalyzer(unittest.TestCase):

    def test_analyze(self):
        # Arrange
        mock_git_wrapper = MagicMock()
        rebase_analyzer = RebaseAnalyzer(mock_git_wrapper)

        # Act
        intentions = rebase_analyzer.analyze("feature/branch-a")

        # Assert
        self.assertEqual(len(intentions), 1)
        self.assertIsInstance(intentions[0], Intention)
        self.assertEqual(intentions[0].description, "Implement user authentication feature.")

if __name__ == '__main__':
    unittest.main()
