import pytest
from pathlib import Path
from src.backend.python_backend.workflow_manager import WorkflowManager, Workflow

@pytest.fixture
def temp_workflows_dir(tmp_path):
    workflows_dir = tmp_path / "workflows"
    workflows_dir.mkdir()
    return workflows_dir

def test_workflow_manager_save_path_traversal(temp_workflows_dir):
    manager = WorkflowManager(workflows_dir=str(temp_workflows_dir))
    workflow = Workflow(name="Test")
    
    # Attempt path traversal
    success = manager.save_workflow(workflow, filename="../malicious.json")
    
    assert not success, "save_workflow should fail on path traversal attempt"
    assert not (temp_workflows_dir.parent / "malicious.json").exists(), "File should not be written outside workflows_dir"

def test_workflow_manager_load_path_traversal(temp_workflows_dir):
    manager = WorkflowManager(workflows_dir=str(temp_workflows_dir))
    
    # Create a dummy file outside workflows_dir
    malicious_target = temp_workflows_dir.parent / "secret.json"
    malicious_target.write_text('{"name": "Secret"}')
    
    # Attempt to load it via path traversal
    loaded_workflow = manager.load_workflow(filename="../secret.json")
    
    assert loaded_workflow is None, "load_workflow should return None on path traversal attempt"

def test_workflow_manager_save_load_valid(temp_workflows_dir):
    manager = WorkflowManager(workflows_dir=str(temp_workflows_dir))
    workflow = Workflow(name="Valid Workflow")
    
    success = manager.save_workflow(workflow, filename="valid.json")
    assert success, "save_workflow should succeed for valid filename"
    
    loaded = manager.load_workflow(filename="valid.json")
    assert loaded is not None, "load_workflow should succeed for valid filename"
    assert loaded.name == "Valid Workflow"
