"""
Advanced Audit Logging System for Email Intelligence Platform

Provides comprehensive event tracking, security monitoring, and compliance logging
with structured JSON output and configurable log levels.
"""

import json
import logging
import threading
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from queue import Queue
import atexit


logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Types of audit events."""

    # Authentication & Authorization
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    PERMISSION_CHANGE = "permission_change"

    # Data Operations
    EMAIL_ACCESS = "email_access"
    EMAIL_MODIFY = "email_modify"
    EMAIL_DELETE = "email_delete"
    CATEGORY_CREATE = "category_create"
    CATEGORY_MODIFY = "category_modify"
    CATEGORY_DELETE = "category_delete"

    # Workflow Operations
    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"
    WORKFLOW_ERROR = "workflow_error"
    NODE_EXECUTION = "node_execution"
    NODE_ERROR = "node_error"

    # Security Events
    SECURITY_VIOLATION = "security_violation"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    UNAUTHORIZED_ACCESS = "unauthorized_access"

    # System Events
    SYSTEM_STARTUP = "system_startup"
    SYSTEM_SHUTDOWN = "system_shutdown"
    CONFIG_CHANGE = "config_change"
    BACKUP_START = "backup_start"
    BACKUP_COMPLETE = "backup_complete"


class AuditSeverity(Enum):
    """Severity levels for audit events."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Structured audit event."""

    event_id: str
    timestamp: str
    event_type: AuditEventType
    severity: AuditSeverity
    user_id: Optional[str]
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    resource: Optional[str]  # What was accessed/modified
    action: str  # What happened
    result: str  # success/failure
    details: Dict[str, Any]
    metadata: Dict[str, Any]  # Additional context

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['severity'] = self.severity.value
        return data


class AuditLogger:
    """
    Advanced audit logger with asynchronous processing and multiple output formats.
    """

    def __init__(
        self,
        log_file: str = "logs/audit.log",
        json_file: str = "logs/audit.jsonl",
        max_queue_size: int = 1000,
        flush_interval: int = 5
    ):
        self.log_file = Path(log_file)
        self.json_file = Path(json_file)
        self.max_queue_size = max_queue_size
        self.flush_interval = flush_interval

        # Create log directories
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.json_file.parent.mkdir(parents=True, exist_ok=True)

        # Event queue for async processing
        self._event_queue: Queue[AuditEvent] = Queue(maxsize=max_queue_size)
        self._stop_event = threading.Event()

        # Start background processing thread
        self._processing_thread = threading.Thread(
            target=self._process_events,
            daemon=True,
            name="AuditLogger"
        )
        self._processing_thread.start()

        # Register cleanup
        atexit.register(self.shutdown)

        logger.info("AuditLogger initialized")

    def log_event(self, event: AuditEvent):
        """Log an audit event asynchronously."""
        try:
            self._event_queue.put_nowait(event)
        except asyncio.QueueFull:
            # If queue is full, log immediately to prevent data loss
            logger.warning(f"Audit queue full, logging synchronously: {event.event_id}")
            self._write_event_immediate(event)

    def log_security_event(
        self,
        event_type: AuditEventType,
        severity: AuditSeverity,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        resource: Optional[str] = None,
        action: str = "",
        result: str = "success",
        details: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a security-related event with automatic metadata collection."""
        import uuid

        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            resource=resource,
            action=action,
            result=result,
            details=details or {},
            metadata=metadata or {}
        )

        self.log_event(event)

    def log_workflow_event(
        self,
        workflow_name: str,
        event_type: AuditEventType,
        user_id: str,
        execution_id: Optional[str] = None,
        node_name: Optional[str] = None,
        duration: Optional[float] = None,
        error_message: Optional[str] = None
    ):
        """Log workflow-related events."""
        details = {
            "workflow_name": workflow_name,
            "execution_id": execution_id,
            "node_name": node_name,
            "duration_seconds": duration,
            "error_message": error_message
        }

        severity = AuditSeverity.LOW
        if event_type in [AuditEventType.WORKFLOW_ERROR, AuditEventType.NODE_ERROR]:
            severity = AuditSeverity.HIGH

        self.log_security_event(
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            resource=f"workflow:{workflow_name}",
            action=f"workflow_{event_type.value}",
            result="failure" if "error" in event_type.value else "success",
            details=details
        )

    def log_api_access(
        self,
        endpoint: str,
        method: str,
        user_id: Optional[str],
        ip_address: str,
        status_code: int,
        response_time: float,
        user_agent: Optional[str] = None
    ):
        """Log API access events."""
        severity = AuditSeverity.LOW
        if status_code >= 400:
            severity = AuditSeverity.MEDIUM if status_code < 500 else AuditSeverity.HIGH

        self.log_security_event(
            event_type=AuditEventType.EMAIL_ACCESS,  # Generic access event
            severity=severity,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            resource=f"api:{endpoint}",
            action=f"{method} {endpoint}",
            result="success" if status_code < 400 else "failure",
            details={
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "response_time_seconds": response_time
            }
        )

    def _process_events(self):
        """Background thread to process audit events."""
        while not self._stop_event.is_set():
            events_to_process = []

            # Collect events from queue
            try:
                while len(events_to_process) < 10:  # Process in batches
                    event = self._event_queue.get(timeout=1.0)
                    events_to_process.append(event)
                    self._event_queue.task_done()
            except asyncio.TimeoutError:
                pass  # No events available

            # Write events
            for event in events_to_process:
                self._write_event_immediate(event)

    def _write_event_immediate(self, event: AuditEvent):
        """Write a single event immediately."""
        try:
            # Write to text log
            log_line = (
                f"[{event.timestamp}] {event.severity.value.upper()} "
                f"{event.event_type.value} user={event.user_id or 'anonymous'} "
                f"resource={event.resource or 'unknown'} action='{event.action}' "
                f"result={event.result}"
            )

            if event.details:
                log_line += f" details={event.details}"

            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line + '\n')

            # Write to JSON log
            with open(self.json_file, 'a', encoding='utf-8') as f:
                json.dump(event.to_dict(), f, ensure_ascii=False)
                f.write('\n')

        except Exception as e:
            logger.error(f"Failed to write audit event {event.event_id}: {e}")

    def shutdown(self):
        """Shutdown the audit logger gracefully."""
        logger.info("Shutting down AuditLogger")

        self._stop_event.set()

        # Process remaining events
        try:
            while not self._event_queue.empty():
                event = self._event_queue.get(timeout=1.0)
                self._write_event_immediate(event)
                self._event_queue.task_done()
        except asyncio.TimeoutError:
            pass

        if self._processing_thread.is_alive():
            self._processing_thread.join(timeout=5.0)


# Global audit logger instance
audit_logger = AuditLogger()
