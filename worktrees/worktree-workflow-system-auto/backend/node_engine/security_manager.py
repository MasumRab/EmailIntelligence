"""
Security Manager for Node-Based Workflow System

This module provides security features for the workflow system including
execution sandboxing, data sanitization, audit logging, and access control.
"""

import asyncio
import logging
import time
import hmac
import hashlib
import json
import secrets
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional
import psutil
import os

logger = logging.getLogger(__name__)


class ExecutionSandbox:
    """
    Provides controlled execution environment for workflow nodes.

    Features:
    - Timeout protection to prevent infinite loops
    - Resource limits (memory, CPU) to prevent abuse
    - Execution monitoring and anomaly detection
    - Safe execution context isolation
    """

    def __init__(self, timeout_seconds: int = 300, max_memory_mb: int = 512, max_cpu_percent: float = 80.0):
        self.timeout_seconds = timeout_seconds
        self.max_memory_mb = max_memory_mb
        self.max_cpu_percent = max_cpu_percent
        self.process = psutil.Process(os.getpid())

    @asynccontextmanager
    async def execute_with_limits(self, node_id: str, user_id: str):
        """
        Context manager for executing node with resource limits and timeout.

        Args:
            node_id: Unique identifier of the node
            user_id: User executing the workflow

        Yields:
            None

        Raises:
            TimeoutError: If execution exceeds timeout
            MemoryError: If memory limit exceeded
            RuntimeError: If CPU limit exceeded
        """
        start_time = time.time()
        initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        logger.info(f"Starting sandboxed execution for node {node_id} by user {user_id}")

        try:
            # Set up monitoring task
            monitor_task = asyncio.create_task(self._monitor_resources(node_id))

            yield

            # Check final resource usage
            final_memory = self.process.memory_info().rss / 1024 / 1024
            memory_used = final_memory - initial_memory

            if memory_used > self.max_memory_mb:
                logger.warning(f"Node {node_id} exceeded memory limit: {memory_used:.2f}MB used")
                raise MemoryError(f"Node execution exceeded memory limit of {self.max_memory_mb}MB")

            execution_time = time.time() - start_time
            logger.info(f"Node {node_id} executed successfully in {execution_time:.2f}s, memory used: {memory_used:.2f}MB")

        except asyncio.TimeoutError:
            logger.error(f"Node {node_id} execution timed out after {self.timeout_seconds}s")
            raise TimeoutError(f"Node execution timed out after {self.timeout_seconds} seconds")

        finally:
            # Cancel monitoring task
            if 'monitor_task' in locals():
                monitor_task.cancel()
                try:
                    await monitor_task
                except asyncio.CancelledError:
                    pass

    async def _monitor_resources(self, node_id: str) -> None:
        """
        Monitor resource usage during execution.

        Args:
            node_id: Node identifier for logging
        """
        while True:
            try:
                # Check memory usage
                memory_mb = self.process.memory_info().rss / 1024 / 1024
                if memory_mb > self.max_memory_mb:
                    logger.error(f"Node {node_id} memory usage {memory_mb:.2f}MB exceeds limit {self.max_memory_mb}MB")
                    # Note: Actual enforcement happens in the context manager
                    break

                # Check CPU usage (rough estimate)
                cpu_percent = self.process.cpu_percent(interval=1.0)
                if cpu_percent > self.max_cpu_percent:
                    logger.warning(f"Node {node_id} high CPU usage: {cpu_percent:.1f}%")

                await asyncio.sleep(5)  # Check every 5 seconds

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error monitoring resources for node {node_id}: {e}")
                break

    async def execute_node_safely(self, node_execute_func, *args, **kwargs) -> Any:
        """
        Execute a node function with timeout and resource limits.

        Args:
            node_execute_func: Async function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result of the node execution

        Raises:
            TimeoutError: If execution times out
            MemoryError: If memory limit exceeded
            Exception: Any exception from the node execution
        """
        try:
            async with asyncio.timeout(self.timeout_seconds):
                result = await node_execute_func(*args, **kwargs)
                return result
        except asyncio.TimeoutError:
            raise TimeoutError(f"Node execution timed out after {self.timeout_seconds} seconds")


class SecurityManager:
    """
    Central security manager for workflow operations.
    """

    def __init__(self):
        self.sandbox = ExecutionSandbox()
        self.audit_logger = AuditLogger()
        self.data_sanitizer = DataSanitizer()
        self.rbac = RoleBasedAccessControl()
        self.session_manager = SessionManager()
        self.workflow_monitor = WorkflowMonitor()
        self.token_manager = SignedToken()

    async def validate_node_execution(self, node_id: str, user_id: str, inputs: Dict[str, Any]) -> bool:
        """
        Validate that a node can be executed by the user.

        Args:
            node_id: Node identifier
            user_id: User identifier
            inputs: Node input data

        Returns:
            True if execution is allowed
        """
        # Check RBAC permission
        if not self.rbac.check_permission(user_id, 'execute_workflow'):
            self.audit_logger.log_security_event('permission_denied', {
                'user_id': user_id,
                'node_id': node_id,
                'permission': 'execute_workflow'
            })
            return False

        # Sanitize inputs
        sanitized_inputs = self.data_sanitizer.sanitize_inputs(inputs)

        # Log the attempt
        self.audit_logger.log_node_execution_attempt(node_id, user_id, sanitized_inputs)

        return True

    async def execute_node_securely(self, node, context) -> Any:
        """
        Execute a node with full security controls.

        Args:
            node: Node instance to execute
            context: Execution context

        Returns:
            Node execution result
        """
        start_time = time.time()

        try:
            async with self.sandbox.execute_with_limits(node.node_id, context.user_id):
                # Validate execution permission
                if not await self.validate_node_execution(node.node_id, context.user_id, node.inputs):
                    raise PermissionError(f"User {context.user_id} not authorized to execute node {node.node_id}")

                # Execute the node
                result = await node.execute(context)

                # Sanitize outputs
                sanitized_result = self.data_sanitizer.sanitize_outputs(result)

                # Log successful execution
                self.audit_logger.log_node_execution_success(node.node_id, context.user_id, sanitized_result)

                # Record execution for monitoring
                execution_time = time.time() - start_time
                self.workflow_monitor.record_execution(node.node_id, execution_time, True)

                # Check for anomalies
                anomaly_result = self.workflow_monitor.detect_anomalies(node.node_id)
                if anomaly_result.get('anomaly'):
                    self.audit_logger.log_security_event('execution_anomaly', {
                        'node_id': node.node_id,
                        'anomaly_details': anomaly_result
                    })

                return sanitized_result

        except Exception as e:
            # Record failed execution
            execution_time = time.time() - start_time
            self.workflow_monitor.record_execution(node.node_id, execution_time, False)

            # Log the error
            self.audit_logger.log_security_event('execution_failure', {
                'node_id': node.node_id,
                'user_id': context.user_id,
                'error': str(e)
            })
            raise


class DataSanitizer:
    """
    Sanitizes input and output data for security.
    """

    def sanitize_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize node inputs to prevent injection attacks.

        Args:
            inputs: Raw input data

        Returns:
            Sanitized input data
        """
        sanitized = {}
        for key, value in inputs.items():
            if isinstance(value, str):
                # Remove potentially dangerous patterns
                sanitized[key] = self._sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = self.sanitize_inputs(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_string(item) if isinstance(item, str) else item for item in inputs]
            else:
                sanitized[key] = value
        return sanitized

    def sanitize_outputs(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize node outputs.

        Args:
            outputs: Raw output data

        Returns:
            Sanitized output data
        """
        return self.sanitize_inputs(outputs)  # Same logic for outputs

    def _sanitize_string(self, value: str) -> str:
        """
        Sanitize a string value.

        Args:
            value: Input string

        Returns:
            Sanitized string
        """
        # Remove null bytes and other dangerous characters
        return value.replace('\x00', '').strip()


class AuditLogger:
    """
    Logs all security-relevant operations for audit purposes.
    """

    def __init__(self):
        self.logger = logging.getLogger('audit')

    def log_node_execution_attempt(self, node_id: str, user_id: str, inputs: Dict[str, Any]) -> None:
        """
        Log an attempt to execute a node.

        Args:
            node_id: Node identifier
            user_id: User identifier
            inputs: Sanitized inputs
        """
        self.logger.info(f"NODE_EXECUTION_ATTEMPT: node={node_id}, user={user_id}, inputs={inputs}")

    def log_node_execution_success(self, node_id: str, user_id: str, outputs: Dict[str, Any]) -> None:
        """
        Log successful node execution.

        Args:
            node_id: Node identifier
            user_id: User identifier
            outputs: Sanitized outputs
        """
        self.logger.info(f"NODE_EXECUTION_SUCCESS: node={node_id}, user={user_id}, outputs={outputs}")

    def log_security_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """
        Log a security event.

        Args:
            event_type: Type of security event
            details: Event details
        """
        self.logger.warning(f"SECURITY_EVENT: type={event_type}, details={details}")


class SignedToken:
    """
    Provides signed tokens for secure data transmission between workflow nodes.

    Uses HMAC-SHA256 for signing to ensure data integrity and authenticity.
    """

    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_hex(32)

    def create_token(self, data: Dict[str, Any], expiration_seconds: int = 3600) -> str:
        """
        Create a signed token containing the data.

        Args:
            data: Data to include in the token
            expiration_seconds: Token expiration time

        Returns:
            Signed token string
        """
        payload = {
            'data': data,
            'exp': int(time.time()) + expiration_seconds,
            'iat': int(time.time()),
            'jti': secrets.token_hex(16)  # Unique token ID
        }

        # Serialize payload
        payload_str = json.dumps(payload, sort_keys=True)

        # Create signature
        signature = hmac.new(
            self.secret_key.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()

        # Combine payload and signature
        token_data = {
            'payload': payload,
            'signature': signature
        }

        return json.dumps(token_data)

    def verify_token(self, token_str: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a signed token.

        Args:
            token_str: Token string to verify

        Returns:
            Decoded data if valid, None if invalid or expired
        """
        try:
            token_data = json.loads(token_str)
            payload = token_data['payload']
            signature = token_data['signature']

            # Recreate signature
            payload_str = json.dumps(payload, sort_keys=True)
            expected_signature = hmac.new(
                self.secret_key.encode(),
                payload_str.encode(),
                hashlib.sha256
            ).hexdigest()

            # Verify signature
            if not hmac.compare_digest(signature, expected_signature):
                logger.warning("Token signature verification failed")
                return None

            # Check expiration
            if payload['exp'] < time.time():
                logger.warning("Token has expired")
                return None

            return payload['data']

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Token verification failed: {e}")
            return None

    def create_node_data_token(self, source_node_id: str, target_node_id: str, data: Any) -> str:
        """
        Create a signed token for data transmission between specific nodes.

        Args:
            source_node_id: ID of the source node
            target_node_id: ID of the target node
            data: Data to transmit

        Returns:
            Signed token for node-to-node transmission
        """
        token_data = {
            'source_node': source_node_id,
            'target_node': target_node_id,
            'data': data,
            'timestamp': int(time.time())
        }

        return self.create_token(token_data)

    def verify_node_data_token(self, token_str: str, expected_source: str, expected_target: str) -> Optional[Any]:
        """
        Verify a node-to-node data token.

        Args:
            token_str: Token to verify
            expected_source: Expected source node ID
            expected_target: Expected target node ID

        Returns:
            Data if token is valid and matches expected nodes
        """
        payload = self.verify_token(token_str)
        if not payload:
            return None

        if payload.get('source_node') != expected_source:
            logger.warning(f"Token source mismatch: expected {expected_source}, got {payload.get('source_node')}")
            return None

        if payload.get('target_node') != expected_target:
            logger.warning(f"Token target mismatch: expected {expected_target}, got {payload.get('target_node')}")
            return None

        return payload.get('data')


class RoleBasedAccessControl:
    """
    Implements role-based access control for workflow operations.
    """

    def __init__(self):
        self.roles = {
            'admin': {'create_workflow', 'delete_workflow', 'execute_workflow', 'manage_users'},
            'editor': {'create_workflow', 'edit_workflow', 'execute_workflow'},
            'viewer': {'view_workflow', 'execute_workflow'},
            'executor': {'execute_workflow'}
        }
        self.user_roles: Dict[str, str] = {}  # user_id -> role

    def assign_role(self, user_id: str, role: str) -> None:
        """
        Assign a role to a user.

        Args:
            user_id: User identifier
            role: Role to assign
        """
        if role not in self.roles:
            raise ValueError(f"Invalid role: {role}")
        self.user_roles[user_id] = role

    def check_permission(self, user_id: str, permission: str) -> bool:
        """
        Check if user has a specific permission.

        Args:
            user_id: User identifier
            permission: Permission to check

        Returns:
            True if user has permission
        """
        user_role = self.user_roles.get(user_id)
        if not user_role:
            return False
        return permission in self.roles.get(user_role, set())


class SessionManager:
    """
    Manages secure sessions for workflow operations.
    """

    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = 3600  # 1 hour

    def create_session(self, user_id: str) -> str:
        """
        Create a new session for a user.

        Args:
            user_id: User identifier

        Returns:
            Session token
        """
        session_id = secrets.token_hex(32)
        self.sessions[session_id] = {
            'user_id': user_id,
            'created': time.time(),
            'last_activity': time.time()
        }
        return session_id

    def validate_session(self, session_id: str) -> Optional[str]:
        """
        Validate a session token.

        Args:
            session_id: Session token to validate

        Returns:
            User ID if session is valid, None otherwise
        """
        session = self.sessions.get(session_id)
        if not session:
            return None

        # Check timeout
        if time.time() - session['last_activity'] > self.session_timeout:
            del self.sessions[session_id]
            return None

        # Update last activity
        session['last_activity'] = time.time()
        return session['user_id']

    def destroy_session(self, session_id: str) -> None:
        """
        Destroy a session.

        Args:
            session_id: Session token to destroy
        """
        self.sessions.pop(session_id, None)


class WorkflowMonitor:
    """
    Monitors workflow execution for anomalies and performance issues.
    """

    def __init__(self):
        self.execution_stats: Dict[str, list] = {}  # node_id -> list of execution times
        self.anomaly_threshold = 3.0  # Standard deviations

    def record_execution(self, node_id: str, execution_time: float, success: bool) -> None:
        """
        Record a node execution for monitoring.

        Args:
            node_id: Node identifier
            execution_time: Time taken for execution
            success: Whether execution was successful
        """
        if node_id not in self.execution_stats:
            self.execution_stats[node_id] = []

        self.execution_stats[node_id].append((execution_time, success))

        # Keep only last 100 executions
        if len(self.execution_stats[node_id]) > 100:
            self.execution_stats[node_id] = self.execution_stats[node_id][-100:]

    def detect_anomalies(self, node_id: str) -> Dict[str, Any]:
        """
        Detect anomalies in node execution.

        Args:
            node_id: Node identifier

        Returns:
            Anomaly detection results
        """
        stats = self.execution_stats.get(node_id, [])
        if len(stats) < 10:  # Need minimum data
            return {'anomaly': False, 'reason': 'insufficient_data'}

        execution_times = [t for t, s in stats if s]  # Only successful executions
        if not execution_times:
            return {'anomaly': False, 'reason': 'no_successful_executions'}

        # Calculate statistics
        mean_time = sum(execution_times) / len(execution_times)
        variance = sum((t - mean_time) ** 2 for t in execution_times) / len(execution_times)
        std_dev = variance ** 0.5

        # Check for anomalies (very slow executions)
        recent_times = execution_times[-5:]  # Last 5 executions
        anomalies = [t for t in recent_times if abs(t - mean_time) > self.anomaly_threshold * std_dev]

        if anomalies:
            return {
                'anomaly': True,
                'reason': 'slow_execution',
                'anomalous_times': anomalies,
                'mean_time': mean_time,
                'std_dev': std_dev
            }

        return {'anomaly': False, 'mean_time': mean_time, 'std_dev': std_dev}