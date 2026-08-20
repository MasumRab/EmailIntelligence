import pytest
import ipaddress
from unittest.mock import Mock, AsyncMock
from fastapi import Request
from src.core.middleware import SecurityMiddleware

@pytest.mark.asyncio
async def test_ip_spoofing_vulnerability():
    """
    Test that the SecurityMiddleware correctly handles IP spoofing attempts.

    Vulnerability: The middleware previously trusted X-Forwarded-For headers
    even when no trusted proxies were configured, allowing attackers to spoof their IP.
    """
    # Setup - No trusted proxies configured
    app = AsyncMock()
    middleware = SecurityMiddleware(app, trusted_proxies=[])

    # Mock request with X-Forwarded-For
    # In FastAPI/Starlette, headers are list of (bytes, bytes)
    scope = {
        "type": "http",
        "headers": [
            (b"x-forwarded-for", b"1.2.3.4"),
            (b"user-agent", b"test-agent")
        ],
        "client": ("6.6.6.6", 12345), # The real connection IP (e.g. attacker)
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }

    async def receive():
        return {"type": "http.request"}

    # Create Request object
    request = Request(scope, receive)

    # Check what IP is extracted
    # We test the internal method because that's where the logic resides
    client_ip = middleware._get_client_ip(request)

    # Assertion
    # If vulnerable, it returns "1.2.3.4" (the spoofed IP)
    # If secure, it should return "6.6.6.6" (the actual peer IP)
    assert client_ip == "6.6.6.6", f"VULNERABILITY DETECTED: IP Spoofing successful! Middleware accepted spoofed IP {client_ip} instead of real IP 6.6.6.6"

@pytest.mark.asyncio
async def test_trusted_proxy_logic():
    """
    Test that X-Forwarded-For is respected ONLY when coming from a trusted proxy.
    """
    # Setup - Trusted proxy configured (e.g., Load Balancer at 10.0.0.1)
    app = AsyncMock()
    middleware = SecurityMiddleware(app, trusted_proxies=["10.0.0.1/32"])

    # Scenario 1: Request from Trusted Proxy with X-Forwarded-For
    scope_trusted = {
        "type": "http",
        "headers": [
            (b"x-forwarded-for", b"203.0.113.1"), # Real client IP
        ],
        "client": ("10.0.0.1", 12345), # Trusted Proxy IP
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    request_trusted = Request(scope_trusted, lambda: None)
    ip_trusted = middleware._get_client_ip(request_trusted)
    assert ip_trusted == "203.0.113.1", f"Should trust proxy and return forwarded IP. Got {ip_trusted}"

    # Scenario 2: Request from UNTRUSTED source with X-Forwarded-For (Spoof attempt)
    scope_untrusted = {
        "type": "http",
        "headers": [
            (b"x-forwarded-for", b"203.0.113.1"), # Spoofed IP
        ],
        "client": ("6.6.6.6", 12345), # Untrusted IP (Attacker)
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    request_untrusted = Request(scope_untrusted, lambda: None)
    ip_untrusted = middleware._get_client_ip(request_untrusted)
    assert ip_untrusted == "6.6.6.6", f"Should IGNORE spoofed header from untrusted source. Got {ip_untrusted}"
