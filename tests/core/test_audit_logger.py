
import pytest
import asyncio
import json
import os
import time
from queue import Empty
from unittest.mock import MagicMock, patch, call
from src.core.audit_logger import AuditLogger, AuditEvent, AuditEventType, AuditSeverity, audit_logger

@pytest.fixture
def temp_audit_files(tmp_path):
    log_file = tmp_path / "audit.log"
    json_file = tmp_path / "audit.jsonl"
    return str(log_file), str(json_file)

@pytest.fixture
def logger_instance(temp_audit_files):
    log_file, json_file = temp_audit_files
    # Use small flush interval for testing
    logger = AuditLogger(log_file=log_file, json_file=json_file, flush_interval=0.1)
    yield logger
    logger.shutdown()

def test_audit_event_structure():
    event = AuditEvent(
        event_id="test-id",
        timestamp="2023-01-01T00:00:00Z",
        event_type=AuditEventType.LOGIN_SUCCESS,
        severity=AuditSeverity.LOW,
        user_id="test-user",
        session_id="test-session",
        ip_address="127.0.0.1",
        user_agent="pytest",
        resource="auth",
        action="login",
        result="success",
        details={"method": "password"},
        metadata={}
    )
    data = event.to_dict()
    assert data["event_type"] == "login_success"
    assert data["severity"] == "low"
    assert data["user_id"] == "test-user"

def test_logger_initialization(logger_instance):
    assert logger_instance._processing_thread.is_alive()

def test_log_event_batching(logger_instance, temp_audit_files):
    log_file, json_file = temp_audit_files

    # Log multiple events
    count = 60 # more than batch size 50
    for i in range(count):
        logger_instance.log_security_event(
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.LOW,
            user_id=f"user_{i}",
            action="login"
        )

    # Wait for processing
    time.sleep(2.0)

    # Verify file content
    with open(json_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == count

    with open(log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == count

@patch("src.core.audit_logger.AuditLogger._write_batch")
def test_batch_processing_logic(mock_write_batch, temp_audit_files):
    log_file, json_file = temp_audit_files
    logger = AuditLogger(log_file=log_file, json_file=json_file, flush_interval=0.1)

    # Push 55 events
    for i in range(55):
        event = AuditEvent(
            event_id=f"id_{i}",
            timestamp="2023-01-01T00:00:00Z",
            event_type=AuditEventType.LOGIN_SUCCESS,
            severity=AuditSeverity.LOW,
            user_id=f"user_{i}",
            session_id=None, ip_address=None, user_agent=None,
            resource=None, action="test", result="success",
            details={}, metadata={}
        )
        logger._event_queue.put(event)

    # Allow thread to process
    time.sleep(1.0)
    logger.shutdown()

    # Expect calls to _write_batch
    # Since batch size is 50, it should be called at least twice (50 + 5)
    assert mock_write_batch.call_count >= 2

    # Verify batch sizes
    # First call should have roughly 50 (if queue was full enough when thread woke up)
    # The loop condition `while len(events_to_process) < 50` ensures max 50 per batch

    args_list = mock_write_batch.call_args_list
    total_processed = sum(len(args[0][0]) for args in args_list)
    assert total_processed == 55

def test_empty_queue_handling(logger_instance):
    # Ensure thread is alive and doesn't crash on empty queue
    time.sleep(2.0)
    assert logger_instance._processing_thread.is_alive()
