import pytest
from unittest.mock import AsyncMock
from fastapi import Request
from src.core.middleware import SecurityMiddleware

@pytest.mark.asyncio
async def test_no_trusted_proxies_with_forged_header():
    """
    Test scenario: No trusted proxies configured, forged X-Forwarded-For header present.
    The direct peer IP should be returned, ignoring the header.
    """
    app = AsyncMock()
    middleware = SecurityMiddleware(app, trusted_proxies=[])
    
    scope = {
        "type": "http",
        "headers": [
            (b"x-forwarded-for", b"203.0.113.5, 10.0.0.1")
        ],
        "client": ("192.168.1.100", 12345),
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    
    request = Request(scope, receive=AsyncMock())
    client_ip = middleware._get_client_ip(request)
    
    assert client_ip == "192.168.1.100", f"Expected '192.168.1.100', got {client_ip}"


@pytest.mark.asyncio
async def test_trusted_proxy_with_valid_chain():
    """
    Test scenario: Trusted proxy configured. Peer is the trusted proxy.
    X-Forwarded-For chain: client_ip, trusted_proxy_2.
    It should skip trusted_proxy_2 from right to left, and find client_ip.
    """
    app = AsyncMock()
    # Trusting two proxies: 10.0.0.1 (immediate peer) and 10.0.0.2 (intermediate proxy)
    middleware = SecurityMiddleware(app, trusted_proxies=["10.0.0.1/32", "10.0.0.2/32"])
    
    scope = {
        "type": "http",
        "headers": [
            # 203.0.113.5 is the real client
            # 10.0.0.2 is another trusted proxy in the chain
            (b"x-forwarded-for", b"203.0.113.5, 10.0.0.2")
        ],
        "client": ("10.0.0.1", 12345), # Immediate peer is trusted proxy 1
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    
    request = Request(scope, receive=AsyncMock())
    client_ip = middleware._get_client_ip(request)
    
    # Starting from right: 10.0.0.2 is trusted. Next is 203.0.113.5 (not trusted) -> returns 203.0.113.5
    assert client_ip == "203.0.113.5", f"Expected '203.0.113.5', got {client_ip}"


@pytest.mark.asyncio
async def test_trusted_proxy_configured_peer_outside():
    """
    Test scenario: Trusted proxy configured, but the connection comes from an untrusted peer.
    The untrusted peer's IP should be returned, ignoring X-Forwarded-For.
    """
    app = AsyncMock()
    middleware = SecurityMiddleware(app, trusted_proxies=["10.0.0.1/32"])
    
    scope = {
        "type": "http",
        "headers": [
            (b"x-forwarded-for", b"203.0.113.5") # Spoofed IP
        ],
        "client": ("192.168.1.100", 12345), # Not a trusted proxy
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    
    request = Request(scope, receive=AsyncMock())
    client_ip = middleware._get_client_ip(request)
    
    assert client_ip == "192.168.1.100", f"Expected '192.168.1.100', got {client_ip}"


@pytest.mark.asyncio
async def test_trusted_proxy_chain_all_trusted():
    """
    Test scenario: Trusted proxy configured. Peer is the trusted proxy.
    X-Forwarded-For chain contains ONLY trusted proxies.
    It should return the leftmost proxy in the chain as the "furthest known client".
    """
    app = AsyncMock()
    middleware = SecurityMiddleware(app, trusted_proxies=["10.0.0.0/24"])
    
    scope = {
        "type": "http",
        "headers": [
            (b"x-forwarded-for", b"10.0.0.3, 10.0.0.2")
        ],
        "client": ("10.0.0.1", 12345),
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    
    request = Request(scope, receive=AsyncMock())
    client_ip = middleware._get_client_ip(request)
    
    assert client_ip == "10.0.0.3", f"Expected '10.0.0.3', got {client_ip}"

@pytest.mark.asyncio
async def test_trusted_proxy_invalid_ip_in_chain():
    """
    Test scenario: Trusted proxy configured. Peer is trusted.
    X-Forwarded-For chain contains an invalid IP format.
    It should return the invalid string rather than crashing or continuing.
    """
    app = AsyncMock()
    middleware = SecurityMiddleware(app, trusted_proxies=["10.0.0.1/32"])
    
    scope = {
        "type": "http",
        "headers": [
            (b"x-forwarded-for", b"203.0.113.5, not-an-ip")
        ],
        "client": ("10.0.0.1", 12345),
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    
    request = Request(scope, receive=AsyncMock())
    client_ip = middleware._get_client_ip(request)
    
    # 'not-an-ip' is untrusted (since it fails parsing), so it returns that
    assert client_ip == "not-an-ip", f"Expected 'not-an-ip', got {client_ip}"

@pytest.mark.asyncio
async def test_trusted_proxy_x_real_ip():
    """
    Test scenario: Trusted proxy configured. Peer is trusted.
    No X-Forwarded-For, but X-Real-IP is present.
    """
    app = AsyncMock()
    middleware = SecurityMiddleware(app, trusted_proxies=["10.0.0.1/32"])
    
    scope = {
        "type": "http",
        "headers": [
            (b"x-real-ip", b"203.0.113.5")
        ],
        "client": ("10.0.0.1", 12345),
        "method": "GET",
        "path": "/api/test",
        "scheme": "http",
        "query_string": b"",
        "app": app
    }
    
    request = Request(scope, receive=AsyncMock())
    client_ip = middleware._get_client_ip(request)
    
    assert client_ip == "203.0.113.5", f"Expected '203.0.113.5', got {client_ip}"