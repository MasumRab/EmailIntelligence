"""
Unit tests for WorkflowContextManager.
"""

import pytest
from src.lib.workflow_context import WorkflowContextManager

def test_initial_state():
    """Verify the manager starts at 'start' step."""
    manager = WorkflowContextManager("test-guide")
    assert manager.get_current_step() == "start"
    assert manager.state.guide_name == "test-guide"
    assert not manager.state.is_completed

def test_transition():
    """Verify step transitions work correctly."""
    manager = WorkflowContextManager("test-guide")
    manager.transition_to("next-step")
    assert manager.get_current_step() == "next-step"

def test_context_updates():
    """Verify data can be stored and retrieved from context."""
    manager = WorkflowContextManager("test-guide")
    manager.update_context({"intent": "app_code", "count": 42})
    assert manager.get_context_value("intent") == "app_code"
    assert manager.get_context_value("count") == 42
    assert manager.get_context_value("missing", "default") == "default"

def test_completion():
    """Verify workflow can be marked completed."""
    manager = WorkflowContextManager("test-guide")
    manager.complete()
    assert manager.state.is_completed