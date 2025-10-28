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
