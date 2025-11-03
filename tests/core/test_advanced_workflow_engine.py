import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
=======
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
>>>>>>> origin/main

from src.core.advanced_workflow_engine import (
    BaseNode,
    NodeMetadata,
    Workflow,
    WorkflowManager,
    WorkflowRunner,
=======
    WorkflowRunner,
    WorkflowManager,
>>>>>>> origin/main
)

# --- Mock Nodes for Testing ---


class MockSimpleNode(BaseNode):
    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Mock Simple Node",
            description="A simple mock node.",
            version="1.0",
            input_types={"input_val": int},
            output_types={"output_val": int},
        )
=======
class MockSimpleNode(BaseNode):
    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(name="Mock Simple Node", description="A simple mock node.", version="1.0", input_types={"input_val": int}, output_types={"output_val": int})
>>>>>>> origin/main

    async def process(self, inputs: dict) -> dict:
        input_val = inputs.get("input_val", 0)
        return {"output_val": input_val * 2}


class MockBranchNode(BaseNode):
    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Mock Branch Node",
            description="A node with multiple outputs.",
            version="1.0",
            input_types={"input_val": int},
            output_types={"branch1": int, "branch2": int},
        )
=======
class MockBranchNode(BaseNode):
    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(name="Mock Branch Node", description="A node with multiple outputs.", version="1.0", input_types={"input_val": int}, output_types={"branch1": int, "branch2": int})
>>>>>>> origin/main

    async def process(self, inputs: dict) -> dict:
        input_val = inputs.get("input_val", 0)
        return {"branch1": input_val + 1, "branch2": input_val - 1}


class MockExceptionNode(BaseNode):
    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(
            name="Mock Exception Node",
            description="A node that always raises an exception.",
            version="1.0",
            input_types={},
            output_types={},
        )
=======
class MockExceptionNode(BaseNode):
    def get_metadata(self) -> NodeMetadata:
        return NodeMetadata(name="Mock Exception Node", description="A node that always raises an exception.", version="1.0", input_types={}, output_types={})
>>>>>>> origin/main

    async def process(self, inputs: dict) -> dict:
        raise ValueError("This node is designed to fail.")


# --- Workflow Tests ---


=======
# --- Workflow Tests ---

>>>>>>> origin/main
def test_workflow_creation_and_structure():
    wf = Workflow(name="Test Workflow")
    node1_id = wf.add_node("MockSimpleNode", node_id="node1")
    node2_id = wf.add_node("MockSimpleNode", node_id="node2")
    wf.add_connection(node1_id, "output_val", node2_id, "input_val")

    assert len(wf.nodes) == 2
    assert len(wf.connections) == 1
    assert wf.get_execution_order() == ["node1", "node2"]


=======
>>>>>>> origin/main
def test_workflow_cycle_detection():
    wf = Workflow(name="Cyclic Workflow")
    node1_id = wf.add_node("MockSimpleNode", node_id="node1")
    node2_id = wf.add_node("MockSimpleNode", node_id="node2")
    wf.add_connection(node1_id, "output_val", node2_id, "input_val")
    wf.add_connection(node2_id, "output_val", node1_id, "input_val")  # Cycle
=======
    wf.add_connection(node2_id, "output_val", node1_id, "input_val") # Cycle
>>>>>>> origin/main

    with pytest.raises(ValueError, match="Workflow contains cycles"):
        wf.get_execution_order()


=======
>>>>>>> origin/main
def test_workflow_serialization():
    wf = Workflow(name="Serialization Test")
    node1_id = wf.add_node("MockSimpleNode", node_id="node1", x=10, y=20)
    data = wf.to_dict()
    new_wf = Workflow.from_dict(data)

    assert new_wf.name == "Serialization Test"
    assert len(new_wf.nodes) == 1
    assert new_wf.nodes[0]["id"] == "node1"


# --- WorkflowRunner Tests ---


=======
# --- WorkflowRunner Tests ---

>>>>>>> origin/main
@pytest.mark.asyncio
async def test_run_simple_workflow():
    wf = Workflow(name="Simple Runner Test")
    node1_id = wf.add_node("MockSimpleNode", node_id="start_node")
    node2_id = wf.add_node("MockSimpleNode", node_id="end_node")
    wf.add_connection(node1_id, "output_val", node2_id, "input_val")

    registry = {"MockSimpleNode": MockSimpleNode}
    runner = WorkflowRunner(registry)
    result = await runner.run_workflow(wf, initial_inputs={"input_val": 5})

    assert result.status == "success"
    assert result.node_results["start_node"]["output_val"] == 10
    assert result.node_results["end_node"]["output_val"] == 20


=======
>>>>>>> origin/main
@pytest.mark.asyncio
async def test_run_workflow_with_exception():
    wf = Workflow(name="Exception Test")
    wf.add_node("MockExceptionNode", node_id="fail_node")

    registry = {"MockExceptionNode": MockExceptionNode}
    runner = WorkflowRunner(registry)
    result = await runner.run_workflow(wf)

    assert result.status == "failed"
    assert "This node is designed to fail" in result.error


# --- WorkflowManager Tests ---


=======
# --- WorkflowManager Tests ---

>>>>>>> origin/main
@pytest.fixture
def manager(tmp_path):
    # Use a temporary directory for workflow files
    return WorkflowManager(workflows_dir=str(tmp_path))


=======
>>>>>>> origin/main
def test_manager_node_registration(manager):
    manager.register_node_type("MockSimpleNode", MockSimpleNode)
    assert "MockSimpleNode" in manager.get_registered_node_types()


=======
>>>>>>> origin/main
def test_manager_workflow_persistence(manager):
    wf = manager.create_workflow(name="Persistence Test")
    wf.add_node("MockSimpleNode", node_id="node1")

    saved = manager.save_workflow(wf)
    assert saved is True

    loaded_wf = manager.load_workflow(manager.list_workflows()[0])
    assert loaded_wf is not None
    assert loaded_wf.name == "Persistence Test"
    assert loaded_wf.workflow_id == wf.workflow_id


=======
>>>>>>> origin/main
@pytest.mark.asyncio
async def test_manager_end_to_end_execution(manager):
    manager.register_node_type("MockSimpleNode", MockSimpleNode)
    wf = manager.create_workflow(name="E2E Test")
    node1_id = wf.add_node("MockSimpleNode", node_id="node1")

    result = await manager.execute_workflow(wf.workflow_id, initial_inputs={"input_val": 10})

    assert result.status == "success"
    assert result.node_results["node1"]["output_val"] == 20
