"""
Tests for src/core/audit_logger.py
"""

import pytest
from src.core.audit_logger import (
    AuditEventType,
    AuditSeverity,
    AuditEvent,
)


class TestAuditEventType:
    """Tests for AuditEventType enum."""

    def test_authentication_events_exist(self):
        """Test authentication event types exist."""
        assert AuditEventType.LOGIN_SUCCESS.value == "login_success"
        assert AuditEventType.LOGIN_FAILURE.value == "login_failure"
        assert AuditEventType.LOGOUT.value == "logout"
        assert AuditEventType.PASSWORD_CHANGE.value == "password_change"
        assert AuditEventType.PERMISSION_CHANGE.value == "permission_change"

    def test_data_operations_events_exist(self):
        """Test data operations event types exist."""
        assert AuditEventType.EMAIL_ACCESS.value == "email_access"
        assert AuditEventType.EMAIL_MODIFY.value == "email_modify"
        assert AuditEventType.EMAIL_DELETE.value == "email_delete"
        assert AuditEventType.CATEGORY_CREATE.value == "category_create"
        assert AuditEventType.CATEGORY_MODIFY.value == "category_modify"
        assert AuditEventType.CATEGORY_DELETE.value == "category_delete"

    def test_workflow_events_exist(self):
        """Test workflow event types exist."""
        assert AuditEventType.WORKFLOW_START.value == "workflow_start"
        assert AuditEventType.WORKFLOW_END.value == "workflow_end"
        assert AuditEventType.WORKFLOW_ERROR.value == "workflow_error"
        assert AuditEventType.NODE_EXECUTION.value == "node_execution"
        assert AuditEventType.NODE_ERROR.value == "node_error"

    def test_security_events_exist(self):
        """Test security event types exist."""
        assert AuditEventType.SECURITY_VIOLATION.value == "security_violation"
        assert AuditEventType.RATE_LIMIT_EXCEEDED.value == "rate_limit_exceeded"
        assert AuditEventType.SUSPICIOUS_ACTIVITY.value == "suspicious_activity"
        assert AuditEventType.UNAUTHORIZED_ACCESS.value == "unauthorized_access"

    def test_system_events_exist(self):
        """Test system event types exist."""
        assert AuditEventType.SYSTEM_STARTUP.value == "system_startup"
        assert AuditEventType.SYSTEM_SHUTDOWN.value == "system_shutdown"
        assert AuditEventType.CONFIG_CHANGE.value == "config_change"
        assert AuditEventType.BACKUP_START.value == "backup_start"
        assert AuditEventType.BACKUP_COMPLETE.value == "backup_complete"


class TestAuditSeverity:
    """Tests for AuditSeverity enum."""

    def test_all_severity_levels_exist(self):
        """Test all severity levels exist."""
        assert AuditSeverity.LOW.value == "low"
        assert AuditSeverity.MEDIUM.value == "medium"
        assert AuditSeverity.HIGH.value == "high"
        assert AuditSeverity.CRITICAL.value == "critical"

    def test_severity_count(self):
        """Test there are exactly 4 severity levels."""
        assert len(AuditSeverity) == 4

    def test_audit_event_types_are_unique(self):
        """Test that all AuditEventType values are unique."""
        values = [e.value for e in AuditEventType]
        assert len(values) == len(set(values)), "AuditEventType values are not unique"


class TestAuditEvent:
    """Tests for AuditEvent dataclass."""

    def test_audit_event_creation(self):
        """Test AuditEvent creation with all required fields."""
        event = AuditEvent(
            event_id="evt123",
            timestamp="2024-01-15T10:30:00Z",
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.LOW,
            user_id="user123",
            session_id="sess456",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0",
            resource="/api/auth/login",
            action="login",
            result="success",
            details={},
            metadata={},
        )

        assert event.event_id == "evt123"
        assert event.timestamp == "2024-01-15T10:30:00Z"
        assert event.event_type == AuditEventType.LOGIN_SUCCESS
        assert event.severity == AuditSeverity.LOW
        assert event.user_id == "user123"
        assert event.session_id == "sess456"
        assert event.ip_address == "192.168.1.1"
        assert event.user_agent == "Mozilla/5.0"
        assert event.resource == "/api/auth/login"
        assert event.action == "login"
        assert event.result == "success"

    def test_audit_event_with_optional_none_fields(self):
        """Test AuditEvent with optional fields set to None."""
        event = AuditEvent(
            event_id="evt789",
            timestamp="2024-01-15T10:30:00Z",
            event_type=AuditEventType.SYSTEM_STARTUP,
            severity=AuditSeverity.MEDIUM,
            user_id=None,
            session_id=None,
            ip_address=None,
            user_agent=None,
            resource=None,
            action="system_startup",
            result="success",
            details={},
            metadata={},
        )

        assert event.event_id == "evt789"
        assert event.event_type == AuditEventType.SYSTEM_STARTUP
        assert event.user_id is None
        assert event.session_id is None
        assert event.ip_address is None
        assert event.user_agent is None

    def test_audit_event_security_violation(self):
        """Test AuditEvent for security violation."""
        event = AuditEvent(
            event_id="sec001",
            timestamp="2024-01-15T10:30:00Z",
            event_type=AuditEventType.SECURITY_VIOLATION,
            severity=AuditSeverity.CRITICAL,
            user_id="bad_user",
            session_id="hijacked_session",
            ip_address="10.0.0.1",
            user_agent="SuspiciousBot",
            resource="/admin/config",
            action="unauthorized_access_attempt",
            result="failure",
            details={"reason": "invalid_token"},
            metadata={"attempts": 5},
        )

        assert event.event_type == AuditEventType.SECURITY_VIOLATION
        assert event.severity == AuditSeverity.CRITICAL
        assert event.user_id == "bad_user"
        assert event.result == "failure"

    def test_audit_event_data_operation(self):
        """Test AuditEvent for data operations."""
        event = AuditEvent(
            event_id="data001",
            timestamp="2024-01-15T10:30:00Z",
            event_type=AuditEventType.EMAIL_DELETE,
            severity=AuditSeverity.HIGH,
            user_id="admin123",
            session_id="admin_session",
            ip_address="192.168.1.100",
            user_agent="AdminConsole/1.0",
            resource="/emails/12345",
            action="delete",
            result="success",
            details={"email_subject": "Test Email"},
            metadata={"batch_id": None},
        )

        assert event.event_type == AuditEventType.EMAIL_DELETE
        assert event.severity == AuditSeverity.HIGH
        assert event.action == "delete"

    def test_audit_event_workflow(self):
        """Test AuditEvent for workflow operations."""
        start_event = AuditEvent(
            event_id="wf001",
            timestamp="2024-01-15T10:30:00Z",
            event_type=AuditEventType.WORKFLOW_START,
            severity=AuditSeverity.LOW,
            user_id="user123",
            session_id="sess456",
            ip_address="192.168.1.1",
            user_agent="WorkflowManager/1.0",
            resource="/workflows/email_processing",
            action="start",
            result="success",
            details={"workflow_name": "email_processing"},
            metadata={"priority": "normal"},
        )

        assert start_event.event_type == AuditEventType.WORKFLOW_START

        error_event = AuditEvent(
            event_id="wf002",
            timestamp="2024-01-15T10:35:00Z",
            event_type=AuditEventType.WORKFLOW_ERROR,
            severity=AuditSeverity.HIGH,
            user_id="user123",
            session_id="sess456",
            ip_address="192.168.1.1",
            user_agent="WorkflowManager/1.0",
            resource="/workflows/email_processing",
            action="execute",
            result="failure",
            details={"error": "node_timeout"},
            metadata={"retry_count": 3},
        )

        assert error_event.event_type == AuditEventType.WORKFLOW_ERROR
        assert error_event.severity == AuditSeverity.HIGH
        assert error_event.result == "failure"

    def test_audit_event_to_dict(self):
        """Test AuditEvent to_dict method."""
        event = AuditEvent(
            event_id="dict001",
            timestamp="2024-01-15T10:30:00Z",
            event_type=AuditEventType.EMAIL_ACCESS,
            severity=AuditSeverity.LOW,
            user_id="user456",
            session_id="sess789",
            ip_address="192.168.1.50",
            user_agent="EmailClient/2.0",
            resource="/emails/999",
            action="read",
            result="success",
            details={"subject": "Hello"},
            metadata={"folder": "inbox"},
        )

        data = event.to_dict()
        assert isinstance(data, dict)
        assert data["event_id"] == "dict001"
        assert data["event_type"] == "email_access"
        assert data["severity"] == "low"
        assert data["user_id"] == "user456"