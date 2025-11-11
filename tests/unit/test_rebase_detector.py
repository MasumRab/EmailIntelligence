import unittest
from unittest.mock import MagicMock
from src.services.rebase_detector import RebaseDetector

class TestRebaseDetector(unittest.TestCase):

    def test_identify_rebased_branches(self):
        # Arrange
        mock_git_wrapper = MagicMock()
        rebase_detector = RebaseDetector(mock_git_wrapper)

        # Act
        rebased_branches = rebase_detector.identify_rebased_branches()

        # Assert
        self.assertEqual(rebased_branches, ["feature/branch-a", "feature/branch-b"])

if __name__ == '__main__':
    unittest.main()
