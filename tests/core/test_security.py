"""
Tests for security utilities.
"""

import pytest
import time
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
from src.core.security import (
    DataSanitizer,
    SecurityValidator,
    SecurityContext,
    SecurityLevel,
    Permission,
    SecurityManager,
    PathValidator,
    validate_path_safety,
    sanitize_path,
    secure_path_join,
)


class TestPathValidation:
    """Test path validation functions."""

    def test_validate_path_safety_safe_paths(self):
        """Test that safe paths are validated correctly."""
        safe_paths = [
            "/tmp/test.db",
            "data/emails.json",
            "./relative/path/file.txt",
            "C:\\Users\\test\\file.db",  # Windows-style path
        ]

        for path in safe_paths:
            assert validate_path_safety(path), f"Path should be safe: {path}"

    def test_validate_path_safety_traversal_attempts(self):
        """Test that directory traversal attempts are detected."""
        dangerous_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config",
            "/tmp/../../../root/.ssh/id_rsa",
            "data/../../../secret.txt",
            "/./././etc/passwd",
            "\\\\UNC\\path\\file",
        ]

        for path in dangerous_paths:
            assert not validate_path_safety(path), f"Path should be unsafe: {path}"

    def test_validate_path_safety_dangerous_characters(self):
        """Test that paths with dangerous characters are rejected."""
        dangerous_paths = [
            "data/file<>.txt",
            "test|pipe.db",
            "file?.sqlite",
            "data/*wildcard.db",
        ]

        for path in dangerous_paths:
            assert not validate_path_safety(path), f"Path should be unsafe: {path}"

    def test_validate_path_safety_with_base_dir(self):
        """Test path validation with base directory constraint."""
        base_dir = "/tmp"

        # Safe paths within base_dir
        assert validate_path_safety("/tmp/test.db", base_dir)
        assert validate_path_safety("test.db", base_dir)

        # Unsafe paths outside base_dir
        assert not validate_path_safety("/etc/passwd", base_dir)
        assert not validate_path_safety("../etc/passwd", base_dir)

    def test_sanitize_path_safe(self):
        """Test path sanitization for safe paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            safe_path = pathlib.Path(temp_dir) / "test.db"
            result = sanitize_path(str(safe_path))
            assert result == safe_path.resolve()

    def test_sanitize_path_unsafe(self):
        """Test path sanitization for unsafe paths."""
        unsafe_paths = [
            "../../../etc/passwd",
            "/tmp/../../../root/.ssh/id_rsa",
        ]

        for path in unsafe_paths:
            result = sanitize_path(path)
            assert result is None, f"Unsafe path should return None: {path}"

    def test_sanitize_path_with_base_dir(self):
        """Test path sanitization with base directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = pathlib.Path(temp_dir)
            safe_path = base_path / "subdir" / "file.db"

            # Safe path within base_dir
            result = sanitize_path(str(safe_path), temp_dir)
            assert result == safe_path

            # Unsafe path outside base_dir
            unsafe_path = "/etc/passwd"
            result = sanitize_path(unsafe_path, temp_dir)
            assert result is None

    def test_secure_path_join_safe(self):
        """Test secure path joining with safe components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = secure_path_join(temp_dir, "subdir", "file.db")
            expected = pathlib.Path(temp_dir) / "subdir" / "file.db"
            assert result == expected

    def test_secure_path_join_unsafe(self):
        """Test secure path joining with unsafe components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Unsafe component with traversal
            result = secure_path_join(temp_dir, "..", "etc", "passwd")
            assert result is None

def test_verify_invalid_token():
    manager = SecurityManager()
    # Test tampered data
    data = {"user": "test", "role": "reader"}
    token = manager.generate_signed_token(data)
    parts = token.split('.')
    tampered_token = f"{parts[0]}.invalid_signature"
    assert manager.verify_signed_token(tampered_token) is None
    # Test invalid format
    assert manager.verify_signed_token("invalid-token-format") is None


# --- PathValidator Tests ---

def test_is_safe_path_valid():
    """Test that safe paths within base directory are accepted"""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir) / "data"
        base_path.mkdir()
        safe_path = base_path / "test.db"
        assert PathValidator.is_safe_path(base_path, safe_path) is True

def test_is_safe_path_traversal():
    """Test that directory traversal attempts are blocked"""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir) / "data"
        base_path.mkdir()
        # Try to escape to parent directory
        traversal_path = base_path / ".." / "etc" / "passwd"
        assert PathValidator.is_safe_path(base_path, traversal_path) is False

def test_sanitize_filename_valid():
    """Test sanitization of valid filenames"""
    assert PathValidator.sanitize_filename("test.db") == "test.db"
    assert PathValidator.sanitize_filename("my_database.sqlite") == "my_database.sqlite"

def test_sanitize_filename_dangerous():
    """Test sanitization removes dangerous characters"""
    assert PathValidator.sanitize_filename("../../../etc/passwd") == "etcpasswd"
    assert PathValidator.sanitize_filename("test<script>.db") == "testscript.db"
    assert PathValidator.sanitize_filename("test.db\x00") == "test.db"

def test_sanitize_filename_edge_cases():
    """Test edge cases in filename sanitization"""
    assert PathValidator.sanitize_filename("") == "default.db"
    assert PathValidator.sanitize_filename(".hidden") == "default.db"
    assert PathValidator.sanitize_filename("..") == "default.db"
    assert PathValidator.sanitize_filename("   ") == "default.db"

def test_validate_database_path_valid():
    """Test validation of valid database paths"""
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        validated = PathValidator.validate_database_path(db_path, temp_dir)
        assert validated == db_path.resolve()

def test_validate_database_path_memory():
    """Test validation of in-memory database"""
    validated = PathValidator.validate_database_path(":memory:")
    assert str(validated) == ":memory:"

def test_validate_database_path_traversal():
    """Test that path traversal is blocked"""
    with tempfile.TemporaryDirectory() as temp_dir:
        base_dir = Path(temp_dir) / "safe"
        base_dir.mkdir()
        traversal_path = base_dir / ".." / "unsafe" / "bad.db"
        with pytest.raises(ValueError, match="escapes allowed directory"):
            PathValidator.validate_database_path(traversal_path, base_dir)

def test_validate_database_path_invalid():
    """Test validation of invalid paths"""
    with pytest.raises(ValueError):
        PathValidator.validate_database_path("")

    with pytest.raises(ValueError):
        PathValidator.validate_database_path("/nonexistent/path/../../../etc/passwd")

    # Absolute path component
    result = secure_path_join(temp_dir, "/etc", "passwd")
    assert result is None

    def test_secure_path_join_empty_components(self):
        """Test secure path joining with empty or invalid components."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Empty components should be handled
            result = secure_path_join(temp_dir, "", "file.db")
            assert result is not None
            assert str(result).endswith("file.db")


class TestDatabaseConfigSecurity:
    """Test that DatabaseConfig properly validates paths."""

    def test_database_config_safe_paths(self):
        """Test DatabaseConfig with safe paths."""
        from src.core.database import DatabaseConfig

        config = DatabaseConfig(data_dir="/tmp/test_data")
        assert config.data_dir == "/tmp/test_data"
        assert validate_path_safety(config.emails_file, config.data_dir)
        assert validate_path_safety(config.categories_file, config.data_dir)
        assert validate_path_safety(config.users_file, config.data_dir)
        assert validate_path_safety(config.email_content_dir, config.data_dir)

    def test_database_config_unsafe_data_dir(self):
        """Test DatabaseConfig rejects unsafe data directory."""
        from src.core.database import DatabaseConfig

        with pytest.raises(ValueError, match="Unsafe data directory path"):
            DatabaseConfig(data_dir="../../../etc")

    def test_database_config_unsafe_files(self):
        """Test DatabaseConfig rejects unsafe file paths."""
        from src.core.database import DatabaseConfig

        with pytest.raises(ValueError, match="Unsafe.*path"):
            DatabaseConfig(
                data_dir="/tmp",
                emails_file="/etc/passwd"
            )


class TestDataMigrationSecurity:
    """Test data migration script security."""

    def test_data_migration_path_validation(self):
        """Test that data migration validates paths."""
        import subprocess
        import sys

        # Test with safe paths (should succeed)
        result = subprocess.run([
            sys.executable, "deployment/data_migration.py",
            "--help"
        ], capture_output=True, text=True)

        # Should show help without errors
        assert result.returncode == 0
        assert "Data Migration Utility" in result.stdout

    @patch('deployment.data_migration.validate_path_safety')
    def test_data_migration_rejects_unsafe_paths(self, mock_validate):
        """Test that data migration rejects unsafe paths."""
        import subprocess
        import sys

        # Mock validation to return False for unsafe paths
        mock_validate.return_value = False

        result = subprocess.run([
            sys.executable, "deployment/data_migration.py",
            "validate-json",
            "--data-dir", "../../../etc",
            "--db-path", "test.db"
        ], capture_output=True, text=True)

        # Should exit with error due to unsafe path
        assert result.returncode == 1
        assert "Unsafe data directory path" in result.stderr
