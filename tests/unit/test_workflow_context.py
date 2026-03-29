import pytest
from src.lib.workflow_context import WorkflowContextManager

def test_workflow_context_initialization():
    """Test that the context manager initializes with no active workflow."""
    manager = WorkflowContextManager()
    assert manager.current_workflow is None
    assert manager.current_step is None

def test_context_manager_protocol():
    """Test that the class works as a context manager."""
    with WorkflowContextManager() as manager:
        assert isinstance(manager, WorkflowContextManager)
        manager.start_workflow("test")
        assert manager.current_workflow == "test"
    
    # After exit, it should be cleared
    assert manager.current_workflow is None

def test_start_workflow():
    """Test starting a workflow."""
    manager = WorkflowContextManager()
    manager.start_workflow("guide-dev")
    assert manager.current_workflow == "guide-dev"
    assert manager.current_step == "start"

def test_transition_step():
    """Test transitioning to a new step."""
    manager = WorkflowContextManager()
    manager.start_workflow("guide-pr")
    manager.transition_to("select_type")
    assert manager.current_step == "select_type"

def test_clear_context():
    """Test clearing the context."""
    manager = WorkflowContextManager()
    manager.start_workflow("guide-dev")
    manager.clear_context()
    assert manager.current_workflow is None
    assert manager.current_step is None

def test_guide_output(capsys):
    """Test the guide method output."""
    manager = WorkflowContextManager()
    manager.guide("Hello World")
    captured = capsys.readouterr()
    assert "[GUIDE] Hello World" in captured.out
