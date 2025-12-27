
import pytest
import os
import re
from unittest.mock import Mock, patch
from src.context_control.isolation import ContextIsolator
from src.context_control.models import AgentContext

# Mock for AgentContext since we don't have the full model
@pytest.fixture
def mock_agent_context():
    context = Mock(spec=AgentContext)
    context.agent_id = "test_agent"
    context.restricted_files = ["*.secret", "private/*"]
    context.accessible_files = ["*.txt", "public/*"]
    context.access_log = []
    context.profile_id = "default"
    return context

@pytest.fixture
def isolator(mock_agent_context):
    with patch("src.context_control.isolation.get_current_config"):
        return ContextIsolator(mock_agent_context)

def test_compile_patterns(isolator):
    patterns = ["*.txt", "src/*.py"]
    compiled = isolator._compile_patterns(patterns)
    # The new implementation returns a single Pattern object (or None)
    assert compiled is not None
    assert hasattr(compiled, "match")
    # Verify it matches
    assert compiled.match("test.txt")
    assert compiled.match("src/main.py")
    assert not compiled.match("test.md")

def test_compile_patterns_empty(isolator):
    patterns = []
    compiled = isolator._compile_patterns(patterns)
    assert compiled is None

def test_is_file_accessible_allowed(isolator):
    with patch("os.path.realpath", side_effect=lambda x: x):
        assert isolator.is_file_accessible("test.txt")
        assert isolator.is_file_accessible("public/readme.md")

def test_is_file_accessible_blocked(isolator):
    with patch("os.path.realpath", side_effect=lambda x: x):
        assert not isolator.is_file_accessible("secret.secret")
        assert not isolator.is_file_accessible("private/key.pem")

def test_is_file_accessible_no_match(isolator):
    with patch("os.path.realpath", side_effect=lambda x: x):
        assert not isolator.is_file_accessible("other.md")

def test_matches_patterns_optimization(isolator):
    # This test verifies the matching logic works as expected
    pattern = isolator._compile_patterns(["*.txt"])
    assert isolator._matches_patterns("test.txt", pattern)
    assert isolator._matches_patterns("/path/to/test.txt", pattern)
    assert not isolator._matches_patterns("test.md", pattern)

def test_matches_patterns_none(isolator):
    assert not isolator._matches_patterns("test.txt", None)
