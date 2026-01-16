"""
Basic tests to verify security fixes in EmailIntelligence CLI
"""
import unittest
from pathlib import Path
from src.core.security import SecurityValidator


class TestSecurityFixes(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path.cwd()
        self.validator = SecurityValidator(self.repo_root)

    def test_safe_path_validation(self):
        """Test that safe paths are validated correctly"""
        # Valid path within repo
        valid_path = self.repo_root / "some" / "valid" / "path"
        self.assertTrue(self.validator.is_safe_path(valid_path))
        
        # Test with a path that resolves to repo root
        self.assertTrue(self.validator.is_safe_path(self.repo_root))

    def test_unsafe_path_detection(self):
        """Test that unsafe paths are detected"""
        # Path traversal attempt
        unsafe_path = self.repo_root / ".." / ".." / "etc" / "passwd"
        self.assertFalse(self.validator.is_safe_path(unsafe_path))
        
        # Absolute path outside repo
        # Note: This test may behave differently depending on the actual repo root
        # but the validator should catch paths that resolve outside the repo

    def test_pr_number_validation(self):
        """Test PR number validation"""
        # Valid PR numbers
        self.assertTrue(self.validator.is_valid_pr_number(1))
        self.assertTrue(self.validator.is_valid_pr_number(12345))
        
        # Invalid PR numbers
        self.assertFalse(self.validator.is_valid_pr_number(0))
        self.assertFalse(self.validator.is_valid_pr_number(-1))
        self.assertFalse(self.validator.is_valid_pr_number(100000))  # Too large

    def test_git_reference_validation(self):
        """Test git reference validation"""
        # Valid references
        self.assertTrue(self.validator.is_valid_git_reference("feature/new-auth"))
        self.assertTrue(self.validator.is_valid_git_reference("bugfix/login-issue"))
        self.assertTrue(self.validator.is_valid_git_reference("main"))
        self.assertTrue(self.validator.is_valid_git_reference("HEAD"))
        
        # Invalid references (dangerous patterns)
        self.assertFalse(self.validator.is_valid_git_reference("../malicious"))
        self.assertFalse(self.validator.is_valid_git_reference("feature@{dangerous}"))
        self.assertFalse(self.validator.is_valid_git_reference("normal\\path"))  # Windows path sep
        self.assertFalse(self.validator.is_valid_git_reference(""))  # Empty string

    def test_input_sanitization(self):
        """Test input sanitization"""
        dangerous_input = "normal_input;rm -rf /"
        sanitized = self.validator.sanitize_input(dangerous_input)
        self.assertNotIn(";", sanitized)
        self.assertNotIn("|", sanitized)
        self.assertNotIn("&", sanitized)
        
        # Normal input should remain mostly intact (semicolons removed though)
        normal_input = "feature/normal-branch"
        sanitized_normal = self.validator.sanitize_input(normal_input)
        expected = "feature/normal-branch"  # This should be unchanged since it has no dangerous chars
        self.assertEqual(expected, sanitized_normal)


if __name__ == '__main__':
    unittest.main()