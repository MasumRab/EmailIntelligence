from unittest.mock import AsyncMock

import pytest

# The 'client' fixture is defined in conftest.py and mocks all external services.


def test_list_workflows(client):
    """Tests the endpoint for listing available workflows."""
    response = client.get("/api/workflows")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_set_active_workflow(client, mock_workflow_engine):
    """Tests setting an active workflow."""
    workflow_name = "default"
    # Configure the mock to "know" about the workflow before the call
    mock_workflow_engine._workflows = {workflow_name: "mock_workflow_object"}

    response = client.put(f"/api/workflows/active/{workflow_name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Active workflow set to '{workflow_name}'."}
    # Verify the mock was called correctly
    mock_workflow_engine.set_active_workflow.assert_called_once_with(workflow_name)


def test_set_nonexistent_active_workflow(client, mock_workflow_engine):
    """Tests setting a nonexistent workflow returns a 404."""
    # Configure the mock to raise a ValueError, as the real engine would
    mock_workflow_engine.set_active_workflow.side_effect = ValueError(
        "Workflow 'nonexistent' not found."
    )

    response = client.put("/api/workflows/active/nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_and_activate_new_workflow(client, mock_workflow_engine):
    """
    Tests that a new workflow can be created via the API and then immediately activated.
    This verifies that the workflow persistence bug is fixed.
    """
    new_workflow_config = {
        "name": "my_brand_new_workflow",
        "description": "A test workflow created via API.",
        "models": {"sentiment": "sentiment-default", "topic": "topic-default"},
    }

    # Configure the mock for create_and_register_workflow_from_config
    async def mock_create(config):
        # Simulate the workflow being registered by adding it to the mock's internal dict
        mock_workflow_engine._workflows[config["name"]] = "mocked_new_workflow_object"
        return True

    # Use an AsyncMock for the side_effect since the original function is async
    mock_workflow_engine.create_and_register_workflow_from_config = AsyncMock(
        side_effect=mock_create
    )

    # 1. Create the new workflow
    response_create = client.post("/api/workflows", json=new_workflow_config)
    assert response_create.status_code == 200
    assert (
        response_create.json()["message"]
        == "Workflow 'my_brand_new_workflow' created successfully."
    )

    # 2. Immediately try to activate the new workflow
    response_activate = client.put("/api/workflows/active/my_brand_new_workflow")
    assert response_activate.status_code == 200
    assert response_activate.json()["message"] == "Active workflow set to 'my_brand_new_workflow'."

    # 3. Verify the mocks were called as expected
    mock_workflow_engine.set_active_workflow.assert_called_with("my_brand_new_workflow")
