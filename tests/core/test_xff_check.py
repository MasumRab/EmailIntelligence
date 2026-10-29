import pytest
from unittest.mock import AsyncMock
from starlette.requests import Request
from src.core.middleware import SecurityMiddleware

def make(headers, client):
    app = AsyncMock()
    mw = SecurityMiddleware(app, trusted_proxies=["10.0.0.1/32", "10.0.0.5/32"])
    scope = {"type": "http", "headers": headers, "client": (client, 1234),
             "method": "GET", "path": "/", "scheme": "http", "query_string": b"", "app": app}
    return mw, Request(scope, lambda: None)

def test_leftmost_spoof_is_ignored():
    mw, req = make([(b"x-forwarded-for", b"1.2.3.4, 2.3.4.5")], "10.0.0.1")
    assert mw._get_client_ip(req) == "2.3.4.5"

def test_all_hops_trusted_falls_back_to_peer():
    mw, req = make([(b"x-forwarded-for", b"10.0.0.1, 10.0.0.1")], "10.0.0.1")
    assert mw._get_client_ip(req) == "10.0.0.1"

def test_malformed_hops_skipped():
    mw, req = make([(b"x-forwarded-for", b"not-an-ip, 2.3.4.5, 10.0.0.1")], "10.0.0.1")
    assert mw._get_client_ip(req) == "2.3.4.5"

def test_untrusted_peer_cannot_use_header():
    mw, req = make([(b"x-forwarded-for", b"1.2.3.4")], "6.6.6.6")
    assert mw._get_client_ip(req) == "6.6.6.6"

def test_untrusted_peer_xrealip_ignored():
    mw, req = make([(b"x-forwarded-for", b"1.2.3.4"), (b"x-real-ip", b"7.7.7.7")], "6.6.6.6")
    assert mw._get_client_ip(req) == "6.6.6.6"

def test_single_hop():
    mw, req = make([(b"x-forwarded-for", b"9.9.9.9")], "10.0.0.1")
    assert mw._get_client_ip(req) == "9.9.9.9"

def test_xrealip_malformed_is_ignored():
    mw, req = make([(b"x-forwarded-for", b"1.2.3.4"), (b"x-real-ip", b"999.999.999.999")], "10.0.0.1")
    assert mw._get_client_ip(req) != "999.999.999.999"

def test_xrealip_override_ignored():
    mw, req = make([(b"x-forwarded-for", b"1.2.3.4"), (b"x-real-ip", b"6.6.6.6")], "10.0.0.1")
    assert mw._get_client_ip(req) == "1.2.3.4"

def test_untrusted_peer_direct_ip():
    mw, req = make([(b"x-forwarded-for", b"1.2.3.4"), (b"x-real-ip", b"6.6.6.6")], "8.8.8.8")
    assert mw._get_client_ip(req) == "8.8.8.8"

def test_trusted_peer_xff_walk():
    app = AsyncMock()
    mw = SecurityMiddleware(app, trusted_proxies=["10.0.0.1/32", "10.0.0.5/32"])
    scope = {"type": "http", "headers": [(b"x-forwarded-for", b"9.9.9.9, 10.0.0.5")], "client": ("10.0.0.1", 1234),
             "method": "GET", "path": "/", "scheme": "http", "query_string": b"", "app": app}
    req = Request(scope, lambda: None)
    assert mw._get_client_ip(req) == "9.9.9.9"
