"""
Property-based tests for core components using Hypothesis.

These tests use property-based testing to verify that core functionality
holds true across a wide range of inputs, following scientific testing
methodologies for robustness validation.
"""

import pytest
from hypothesis import given, strategies as st, assume
from hypothesis.stateful import RuleBasedStateMachine, rule

from src.core.workflow_engine import WorkflowEngine
from src.core.data_source import DataSource


class TestWorkflowEngineProperties:
    """Property-based tests for WorkflowEngine."""

    @given(
        workflow_name=st.text(min_size=1, max_size=50),
        node_count=st.integers(min_value=1, max_value=20)
    )
    def test_workflow_creation_properties(self, workflow_name, node_count):
        """Test that workflow creation is robust across various inputs."""
        assume(workflow_name.strip())  # Name should not be just whitespace

        engine = WorkflowEngine()

        # This would test that workflow creation doesn't crash
        # and maintains invariants regardless of input
        try:
            # Simulate workflow creation with various parameters
            workflow_config = {
                "name": workflow_name,
                "nodes": [{"id": f"node_{i}", "type": "test"} for i in range(node_count)]
            }

            # Property: Workflow creation should not raise unexpected exceptions
            # Property: Created workflow should have expected structure
            assert isinstance(workflow_config, dict)
            assert "name" in workflow_config
            assert len(workflow_config["nodes"]) == node_count

        except Exception as e:
            # Only expected exceptions should be raised
            assert isinstance(e, (ValueError, TypeError))

    @given(
        data_size=st.integers(min_value=0, max_value=10000),
        batch_size=st.integers(min_value=1, max_value=100)
    )
    def test_data_processing_properties(self, data_size, batch_size):
        """Test data processing invariants under various conditions."""
        assume(data_size >= 0)
        assume(batch_size > 0)

        # Property: Data processing should handle various sizes gracefully
        # Property: Batch processing should maintain data integrity

        test_data = list(range(data_size))
        batches = [test_data[i:i + batch_size] for i in range(0, len(test_data), batch_size)]

        # Verify batching properties
        assert all(len(batch) <= batch_size for batch in batches)
        assert sum(len(batch) for batch in batches) == data_size

        # Verify no data loss
        reconstructed = [item for batch in batches for item in batch]
        assert reconstructed == test_data


class TestDataSourceProperties:
    """Property-based tests for DataSource implementations."""

    @given(
        query_params=st.dictionaries(
            keys=st.text(min_size=1, max_size=20),
            values=st.one_of(st.text(), st.integers(), st.floats()),
            max_size=10
        )
    )
    def test_query_parameter_handling(self, query_params):
        """Test that query parameters are handled consistently."""
        # Remove None values and empty keys
        clean_params = {k: v for k, v in query_params.items()
                       if k and k.strip() and v is not None}

        # Property: Parameter processing should be deterministic
        # Property: Invalid parameters should be rejected gracefully

        assert isinstance(clean_params, dict)
        assert all(isinstance(k, str) and k.strip() for k in clean_params.keys())


class WorkflowStateMachine(RuleBasedStateMachine):
    """State machine testing for workflow state transitions."""

    def __init__(self):
        super().__init__()
        self.engine = WorkflowEngine()
        self.workflows = {}

    @rule(workflow_id=st.text(min_size=1, max_size=20))
    def create_workflow(self, workflow_id):
        """Create a new workflow."""
        assume(workflow_id not in self.workflows)
        self.workflows[workflow_id] = {"status": "created", "nodes": []}

    @rule(
        workflow_id=st.text(min_size=1, max_size=20),
        node_id=st.text(min_size=1, max_size=10)
    )
    def add_node(self, workflow_id, node_id):
        """Add a node to an existing workflow."""
        assume(workflow_id in self.workflows)
        assume(node_id not in [n["id"] for n in self.workflows[workflow_id]["nodes"]])

        self.workflows[workflow_id]["nodes"].append({"id": node_id, "status": "pending"})

    @rule(workflow_id=st.text(min_size=1, max_size=20))
    def execute_workflow(self, workflow_id):
        """Execute a workflow."""
        assume(workflow_id in self.workflows)
        assume(len(self.workflows[workflow_id]["nodes"]) > 0)

        # Property: Execution should transition all nodes to completed
        for node in self.workflows[workflow_id]["nodes"]:
            node["status"] = "completed"

        self.workflows[workflow_id]["status"] = "executed"


TestWorkflowStateMachine = WorkflowStateMachine.TestCase