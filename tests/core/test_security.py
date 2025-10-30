<<<<<<< HEAD
import pytest
import time
from src.core.security import (
    DataSanitizer,
    SecurityValidator,
    SecurityContext,
    SecurityLevel,
    Permission,
    SecurityManager,
)

# --- DataSanitizer Tests ---

def test_sanitize_input_string():
    sanitized = DataSanitizer.sanitize_input("<script>alert('xss')</script> Hello")
    assert sanitized == "&lt;script>alert('xss')</script> Hello"

def test_sanitize_input_dict():
    data = {"<script>key": "value<script>"}
    sanitized = DataSanitizer.sanitize_input(data)
    assert sanitized == {"&lt;script>key": "value&lt;script>"}

def test_sanitize_input_list():
    data = ["item1<script>", "<script>item2"]
    sanitized = DataSanitizer.sanitize_input(data)
    assert sanitized == ["item1&lt;script>", "&lt;script>item2"]

def test_sanitize_output_string():
    data = "user password: mysecretpassword, token: mytoken"
    sanitized = DataSanitizer.sanitize_output(data)
    assert "mysecretpassword" not in sanitized
    assert "mytoken" not in sanitized
    assert "password: [REDACTED]" in sanitized
    assert "token: [REDACTED]" in sanitized

def test_sanitize_output_dict():
    data = {"user": "test", "password": "secret", "auth_key": "12345"}
    sanitized = DataSanitizer.sanitize_output(data)
    assert sanitized["user"] == "test"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["auth_key"] == "[REDACTED]"

# --- SecurityValidator Tests ---

@pytest.fixture
def valid_context():
    return SecurityContext(
        user_id="test_user",
        permissions=[Permission.READ, Permission.WRITE],
        security_level=SecurityLevel.INTERNAL,
        session_token="valid_token",
        created_at=time.time(),
        expires_at=time.time() + 3600,
        allowed_resources=["resource1", "resource2"],
    )

@pytest.fixture
def admin_context():
    return SecurityContext(
        user_id="admin_user",
        permissions=[Permission.ADMIN, Permission.READ, Permission.WRITE, Permission.EXECUTE],
        security_level=SecurityLevel.RESTRICTED,
        session_token="admin_token",
        created_at=time.time(),
        expires_at=time.time() + 3600,
        allowed_resources=["*"],
    )

def test_validate_access_success(valid_context):
    assert SecurityValidator.validate_access(valid_context, "resource1", Permission.READ) is True

def test_validate_access_permission_denied(valid_context):
    assert SecurityValidator.validate_access(valid_context, "resource1", Permission.EXECUTE) is False

def test_validate_access_resource_denied(valid_context):
    assert SecurityValidator.validate_access(valid_context, "resource3", Permission.READ) is False

def test_validate_access_expired(valid_context):
    valid_context.expires_at = time.time() - 1
    assert SecurityValidator.validate_access(valid_context, "resource1", Permission.READ) is False

def test_validate_data_access_sensitive_denied(valid_context):
    data = {"key": "value", "user_password": "123"}
    assert SecurityValidator.validate_data_access(valid_context, data) is False

def test_validate_data_access_sensitive_allowed(admin_context):
    data = {"key": "value", "user_password": "123"}
    assert SecurityValidator.validate_data_access(admin_context, data) is True

# --- SecurityManager Tests ---

def test_create_and_validate_session():
    manager = SecurityManager()
    context = manager.create_session("user1", [Permission.READ], SecurityLevel.PUBLIC)
    validated_context = manager.validate_session(context.session_token)
    assert validated_context is not None
    assert validated_context.user_id == "user1"

def test_validate_invalid_session():
    manager = SecurityManager()
    assert manager.validate_session("invalid_token") is None

def test_validate_expired_session():
    manager = SecurityManager()
    context = manager.create_session("user1", [Permission.READ], SecurityLevel.PUBLIC, duration_hours=-1)
    # Ensure a moment passes for expiry
    time.sleep(0.01)
    assert manager.validate_session(context.session_token) is None

def test_generate_and_verify_signed_token():
    manager = SecurityManager()
    data = {"user": "test", "role": "reader"}
    token = manager.generate_signed_token(data)
    assert token is not None
    verified_data = manager.verify_signed_token(token)
    assert verified_data == data

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
=======
"""
Tests for security utilities.
"""

import pytest
import tempfile
import pathlib
from unittest.mock import patch

from src.core.security import validate_path_safety, sanitize_path, secure_path_join


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
        assert "Unsafe data directory path" in result.stderr</content>
</xai:function_call: <parameter name="path">/home/masum/github/EmailIntelligence/tests/core/test_security.py
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2
