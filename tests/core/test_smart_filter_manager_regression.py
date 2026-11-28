import pytest
from unittest.mock import MagicMock
from src.core.smart_filter_manager import SmartFilterManager, _EmailContext

def test_email_context_lazy_evaluation():
    email = {"subject": "HELLO WORLD", "content": "THIS IS SPAM"}
    ctx = _EmailContext(email, "example.com", "sender@example.com")
    
    # Assert private fields are uninitialized
    assert ctx._subject_lower is None
    assert ctx._content_lower is None
    
    # First access computes them
    subject = ctx.subject_lower
    assert subject == "hello world"
    assert ctx._subject_lower == "hello world"
    
    content = ctx.content_lower
    assert content == "this is spam"
    assert ctx._content_lower == "this is spam"

def test_email_context_fallback_body():
    email = {"subject": "Test", "body": "BODY FALLBACK"}
    ctx = _EmailContext(email, "test.com", "user@test.com")
    assert ctx.content_lower == "body fallback"

