import unittest
from unittest.mock import MagicMock
from src.services.merge_verifier import MergeVerifier

class TestMergeVerifier(unittest.TestCase):

    def test_verify(self):
        # Arrange
        mock_git_wrapper = MagicMock()
        merge_verifier = MergeVerifier(mock_git_wrapper)

        # Act
        report = merge_verifier.verify("main")

        # Assert
        self.assertEqual(report, "All intentions have been fulfilled.")

if __name__ == '__main__':
    unittest.main()
