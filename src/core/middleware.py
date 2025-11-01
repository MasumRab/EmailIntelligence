"""
FastAPI Middleware for Security, Audit Logging, and Performance Monitoring

Provides comprehensive middleware for API security, rate limiting, audit trails,
and performance monitoring with minimal overhead.
"""

import time
import logging
from typing import Callable, Optional
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
import ipaddress

from .rate_limiter import api_rate_limiter
from .audit_logger import audit_logger
from .performance_monitor import performance_monitor

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """
    FastAPI middleware for security, rate limiting, and audit logging.
    """

    def __init__(
        self,
        app,
        enable_rate_limiting: bool = True,
        enable_audit_logging: bool = True,
        enable_performance_monitoring: bool = True,
        trusted_proxies: Optional[list] = None
    ):
        self.app = app
        self.enable_rate_limiting = enable_rate_limiting
        self.enable_audit_logging = enable_audit_logging
        self.enable_performance_monitoring = enable_performance_monitoring
        self.trusted_proxies = trusted_proxies or []

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Create request wrapper
        request = Request(scope, receive)

        # Extract client information
        client_ip = self._get_client_ip(request)
        user_id = self._get_user_id(request)
        user_agent = request.headers.get("user-agent")

        # Rate limiting check
        if self.enable_rate_limiting:
            allowed, headers = await api_rate_limiter.check_rate_limit(
                request.url.path,
                client_ip  # Use IP as client key, could be enhanced with user_id
            )

            if not allowed:
                # Audit log rate limit violation
                if self.enable_audit_logging:
                    audit_logger.log_security_event(
                        event_type=audit_logger.AuditEventType.RATE_LIMIT_EXCEEDED,
                        severity=audit_logger.AuditSeverity.MEDIUM,
                        user_id=user_id,
                        ip_address=client_ip,
                        user_agent=user_agent,
                        resource=f"api:{request.url.path}",
                        action=f"{request.method} {request.url.path}",
                        result="failure",
                        details={"rate_limit_headers": headers}
                    )

                # Return rate limit exceeded response
                response = JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "message": "Too many requests. Please try again later."
                    },
                    headers=headers
                )
                await response(scope, receive, send)
                return

        # Start performance monitoring
        start_time = time.time()
        if self.enable_performance_monitoring:
            perf_context = performance_monitor.time_function(
                f"api_{request.method.lower()}_{request.url.path.replace('/', '_')}",
                tags={
                    "method": request.method,
                    "endpoint": request.url.path,
                    "user_id": user_id or "anonymous"
                },
                sample_rate=0.1  # Sample 10% of requests to reduce overhead
            )
            perf_context.__enter__()

        try:
            # Process the request
            response_sent = False

            async def send_wrapper(message):
                nonlocal response_sent
                if message["type"] == "http.response.start":
                    status_code = message["status"]

                    # Performance monitoring end
                    if self.enable_performance_monitoring:
                        perf_context.__exit__(None, None, None)

                    # Audit logging for API access
                    if self.enable_audit_logging:
                        response_time = time.time() - start_time
                        audit_logger.log_api_access(
                            endpoint=request.url.path,
                            method=request.method,
                            user_id=user_id,
                            ip_address=client_ip,
                            status_code=status_code,
                            response_time=response_time,
                            user_agent=user_agent
                        )

                await send(message)
                if message["type"] == "http.response.start":
                    response_sent = True

            await self.app(scope, receive, send_wrapper)

        except Exception as e:
            # Performance monitoring cleanup on error
            if self.enable_performance_monitoring:
                perf_context.__exit__(type(e), e, e.__traceback__)

            # Audit log the error
            if self.enable_audit_logging:
                audit_logger.log_security_event(
                    event_type=audit_logger.AuditEventType.SECURITY_VIOLATION,
                    severity=audit_logger.AuditSeverity.HIGH,
                    user_id=user_id,
                    ip_address=client_ip,
                    user_agent=user_agent,
                    resource=f"api:{request.url.path}",
                    action=f"{request.method} {request.url.path}",
                    result="error",
                    details={"error": str(e), "error_type": type(e).__name__}
                )

            raise

    def _get_client_ip(self, request: Request) -> str:
        """Extract real client IP, considering proxies."""
        # Check X-Forwarded-For header
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            # Take the first IP in the chain
            client_ip = forwarded_for.split(",")[0].strip()

            # Validate the IP from proxy
            real_ip = request.headers.get("x-real-ip")
            if real_ip and real_ip != client_ip:
                # Verify the proxy is trusted
                try:
                    proxy_ip = ipaddress.ip_address(request.client.host)
                    if any(proxy_ip in ipaddress.ip_network(proxy) for proxy in self.trusted_proxies):
                        return real_ip
                except:
                    pass

            return client_ip

        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"

    def _get_user_id(self, request: Request) -> Optional[str]:
        """Extract user ID from request (JWT token, session, etc.)."""
        # This is a placeholder - in a real implementation, you'd extract
        # the user ID from JWT tokens, session cookies, etc.
        # For now, we'll look for a simple header or query param

        user_id = request.headers.get("X-User-ID") or request.query_params.get("user_id")
        return user_id


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to responses.
    """

    def __init__(self, app):
        self.app = app
        self.security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.get("headers", [])
                # Add security headers
                for header_name, header_value in self.security_headers.items():
                    headers.append([header_name.encode(), header_value.encode()])
                message["headers"] = headers

            await send(message)

        await self.app(scope, receive, send_wrapper)


# Convenience functions for creating middleware
def create_security_middleware(
    app,
    enable_rate_limiting: bool = True,
    enable_audit_logging: bool = True,
    enable_performance_monitoring: bool = True,
    trusted_proxies: Optional[list] = None
):
    """Create security middleware with specified options."""
    return SecurityMiddleware(
        app,
        enable_rate_limiting=enable_rate_limiting,
        enable_audit_logging=enable_audit_logging,
        enable_performance_monitoring=enable_performance_monitoring,
        trusted_proxies=trusted_proxies
    )

def create_security_headers_middleware(app):
    """Create security headers middleware."""
    return SecurityHeadersMiddleware(app)
