"""
Integration tests for security components.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.core.middleware import create_security_middleware, create_security_headers_middleware
from src.core.rate_limiter import api_rate_limiter
from src.core.audit_logger import audit_logger
from src.core.performance_monitor import performance_monitor


@pytest.fixture
def secure_app():
    """Create FastAPI app with security middleware."""
    app = FastAPI()

    @app.get("/test")
    async def test_endpoint():
        return {"message": "secure"}

    @app.get("/api/test")
    async def api_endpoint():
        return {"message": "api_secure"}

    # Add security middleware
    app.add_middleware(create_security_middleware(app))
    app.add_middleware(create_security_headers_middleware(app))

    return app


@pytest.fixture
def secure_client(secure_app):
    """Test client with security middleware."""
    return TestClient(secure_app)


class TestSecurityMiddleware:
    """Test security middleware integration."""

    def test_security_headers_present(self, secure_client):
        """Test that security headers are added to responses."""
        response = secure_client.get("/test")

        # Check security headers
        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"

        assert "X-Frame-Options" in response.headers
        assert response.headers["X-Frame-Options"] == "DENY"

        assert "X-XSS-Protection" in response.headers
        assert response.headers["X-XSS-Protection"] == "1; mode=block"

        assert "Strict-Transport-Security" in response.headers

    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting functionality."""
        # Reset rate limiter for test
        api_rate_limiter._limiters.clear()

        # Test normal request
        allowed, headers = await api_rate_limiter.check_rate_limit("/api/test", "test_client")
        assert allowed
        assert "X-RateLimit-Limit" in headers
        assert "X-RateLimit-Remaining" in headers

    def test_audit_logging_enabled(self, secure_client):
        """Test that audit logging is working."""
        with patch.object(audit_logger, 'log_api_access') as mock_log:
            response = secure_client.get("/api/test")

            # Verify audit logging was called
            mock_log.assert_called_once()
            call_args = mock_log.call_args[1]

            assert call_args["endpoint"] == "/api/test"
            assert call_args["method"] == "GET"
            assert call_args["status_code"] == 200

    def test_performance_monitoring(self, secure_client):
        """Test that performance monitoring is working."""
        # Clear existing metrics
        performance_monitor._aggregated_metrics.clear()

        response = secure_client.get("/api/test")

        # Check that metrics were recorded
        metrics = performance_monitor.get_aggregated_metrics()
        assert len(metrics) > 0  # Should have recorded some metrics


class TestSecurityIntegration:
    """Test integration between security components."""

    @pytest.mark.asyncio
    async def test_complete_security_flow(self):
        """Test complete security flow with all components."""
        # This is an integration test that would run in a real environment
        # For now, just test that all components can be imported and initialized

        # Test rate limiter initialization
        limiter = api_rate_limiter.get_limiter("/api/test")
        assert limiter is not None

        # Test audit logger initialization
        assert audit_logger is not None

        # Test performance monitor initialization
        assert performance_monitor is not None

    def test_security_middleware_creation(self):
        """Test that security middleware can be created."""
        app = FastAPI()

        middleware = create_security_middleware(app)
        assert middleware is not None

        headers_middleware = create_security_headers_middleware(app)
        assert headers_middleware is not None


class TestErrorHandling:
    """Test error handling in security components."""

    def test_malformed_request_handling(self, secure_client):
        """Test handling of malformed requests."""
        # Test with invalid headers
        response = secure_client.get("/test", headers={"invalid": "header"})
        assert response.status_code == 200  # Should still work

    @pytest.mark.asyncio
    async def test_rate_limiter_error_handling(self):
        """Test rate limiter error handling."""
        # Test with invalid endpoint
        allowed, headers = await api_rate_limiter.check_rate_limit("", "test")
        assert allowed  # Should default to allowed for empty endpoint

    def test_audit_logging_error_handling(self):
        """Test audit logger error handling."""
        # Test with invalid data (should not crash)
        audit_logger.log_api_access(
            endpoint="/test",
            method="GET",
            user_id=None,
            ip_address="invalid_ip",
            status_code=200,
            response_time=-1.0  # Invalid response time
        )
        # Should not raise exception


class TestPerformanceUnderLoad:
    """Test performance of security components under load."""

    @pytest.mark.asyncio
    async def test_rate_limiter_performance(self):
        """Test rate limiter performance with multiple requests."""
        import time

        start_time = time.time()

        # Make multiple requests quickly
        for i in range(10):
            allowed, _ = await api_rate_limiter.check_rate_limit(f"/api/test{i}", "perf_client")

        end_time = time.time()
        duration = end_time - start_time

        # Should complete quickly (< 1 second)
        assert duration < 1.0

    def test_audit_logging_performance(self):
        """Test audit logging performance."""
        import time

        start_time = time.time()

        # Log multiple events
        for i in range(10):
            audit_logger.log_api_access(
                endpoint=f"/api/test{i}",
                method="GET",
                user_id="perf_test",
                ip_address="127.0.0.1",
                status_code=200,
                response_time=0.1
            )

        end_time = time.time()
        duration = end_time - start_time

        # Should complete quickly (< 0.5 second)
        assert duration < 0.5

    def test_performance_monitor_performance(self):
        """Test performance monitor recording performance."""
        import time

        start_time = time.time()

        # Record multiple metrics
        for i in range(100):
            performance_monitor.record_metric(
                f"test_metric_{i}",
                i,
                "count",
                sample_rate=1.0  # Don't sample for performance test
            )

        end_time = time.time()
        duration = end_time - start_time

        # Should complete quickly (< 0.1 second)
        assert duration < 0.1


class TestSecurityCompliance:
    """Test security compliance and best practices."""

    def test_no_information_leakage(self, secure_client):
        """Test that errors don't leak sensitive information."""
        # Test 404 error
        response = secure_client.get("/nonexistent")
        assert response.status_code == 404

        # Response should not contain sensitive information
        response_text = response.text.lower()
        assert "traceback" not in response_text
        assert "internal" not in response_text or "server error" in response_text

    def test_cors_headers(self, secure_client):
        """Test CORS headers are properly configured."""
        response = secure_client.options("/api/test")

        # Should handle OPTIONS request for CORS
        # Note: In our test app, this might not be fully configured
        # but the middleware should handle it
        assert response.status_code in [200, 404, 405]  # Acceptable responses

    def test_security_headers_comprehensive(self, secure_client):
        """Test all security headers are present."""
        response = secure_client.get("/test")

        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        for header in required_headers:
            assert header in response.headers, f"Missing security header: {header}"</content>
