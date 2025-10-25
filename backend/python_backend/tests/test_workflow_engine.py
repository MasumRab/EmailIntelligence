import json
import os
from unittest.mock import MagicMock, call, mock_open, patch

import pytest

# Import the class to be tested and the constant
from backend.python_backend.workflow_engine import (

# Mocks for dependencies
@pytest.fixture
def mock_ai_engine():
    return MagicMock()


@pytest.fixture
def mock_filter_manager():
    return MagicMock()


@pytest.fixture
def mock_db_manager():
    return MagicMock()


@pytest.fixture
def workflow_engine():
    """Provides a clean WorkflowEngine instance for each test."""
    return WorkflowEngine()
def test_register_workflow(workflow_engine, mock_ai_engine, mock_filter_manager, mock_db_manager):
    """Tests that a workflow can be registered correctly."""
    mock_workflow = DefaultWorkflow(mock_ai_engine, mock_filter_manager, mock_db_manager)
    workflow_engine.register_workflow(mock_workflow)
    assert "default" in workflow_engine._workflows
    assert workflow_engine._workflows["default"] == mock_workflow


def test_set_active_workflow(workflow_engine, mock_ai_engine, mock_filter_manager, mock_db_manager):
    """Tests that an active workflow can be set."""
    mock_workflow = DefaultWorkflow(mock_ai_engine, mock_filter_manager, mock_db_manager)
    workflow_engine.register_workflow(mock_workflow)
    workflow_engine.set_active_workflow("default")
    assert workflow_engine.active_workflow is not None
    assert workflow_engine.active_workflow.name == "default"


def test_set_active_nonexistent_workflow(workflow_engine):
    """Tests that setting a nonexistent workflow raises a ValueError."""
    with pytest.raises(ValueError, match="Workflow 'nonexistent' not found."):
        workflow_engine.set_active_workflow("nonexistent")


@pytest.mark.asyncio
    mock_workflow_config = {
        "name": "my_file_workflow",
        "models": {"sentiment": "sentiment-default"},
    }

    m = mock_open(read_data=json.dumps(mock_workflow_config))

    with (
        patch("os.path.exists") as mock_exists,
        patch("os.listdir") as mock_listdir,
        patch("builtins.open", m),
    ):

        mock_exists.return_value = True
        mock_listdir.return_value = ["my_file_workflow.json"]

        await workflow_engine.discover_workflows(
            mock_ai_engine, mock_filter_manager, mock_db_manager
        )

        # Assert that both default and file-based workflows are registered
        assert "default" in workflow_engine.list_workflows()
        assert "my_file_workflow" in workflow_engine.list_workflows()
        assert isinstance(workflow_engine._workflows["my_file_workflow"], FileBasedWorkflow)

        # Assert that the default workflow is active by default
        assert workflow_engine.active_workflow.name == "default"


    new_config = {"name": "new_api_workflow", "models": {"topic": "topic-default"}}
    # Set up the engine with dependencies first
    workflow_engine._ai_engine = mock_ai_engine
    workflow_engine._filter_manager = mock_filter_manager
    workflow_engine._db = mock_db_manager

    m = mock_open()
    # Patch json.dump directly to avoid issues with how it calls write()
    with (
        patch("os.path.exists", return_value=False),
        patch("builtins.open", m),
        patch("json.dump") as mock_json_dump,
    ):

        await workflow_engine.create_and_register_workflow_from_config(new_config)

        # Verify the file was opened for writing
        m.assert_called_once_with(WORKFLOWS_DIR / "new_api_workflow.json", "w")

        # Verify that json.dump was called with the correct data and file handle
        mock_json_dump.assert_called_once_with(new_config, m(), indent=4)

        # Verify the workflow was registered
        assert "new_api_workflow" in workflow_engine.list_workflows()
        assert isinstance(workflow_engine._workflows["new_api_workflow"], FileBasedWorkflow)
