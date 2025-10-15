"""
Test module for the node-based workflow system.

This module contains tests to verify that the node system works as expected.
"""

import asyncio
import json

from backend.node_engine.email_nodes import (
    ActionNode,
    AIAnalysisNode,
    EmailSourceNode,
    FilterNode,
    PreprocessingNode,
)
from backend.node_engine.node_base import Workflow
from backend.node_engine.workflow_engine import workflow_engine
from backend.node_engine.workflow_manager import workflow_manager


async def test_basic_workflow():
    """Test a basic workflow with multiple nodes."""
    print("Testing basic workflow execution...")

    # Create a simple workflow
    workflow = Workflow(name="Test Workflow")

    # Add nodes
    source_node = EmailSourceNode(name="Test Source")
    preprocessing_node = PreprocessingNode(name="Test Preprocessor")
    analysis_node = AIAnalysisNode(name="Test Analyzer")

    workflow.add_node(source_node)
    workflow.add_node(preprocessing_node)
    workflow.add_node(analysis_node)

    # Connect nodes
    workflow.add_connection(
        Connection(
            source_node_id=source_node.node_id,
            source_port="emails",
            target_node_id=preprocessing_node.node_id,
            target_port="emails",
        )
    )

    workflow.add_connection(
        Connection(
            source_node_id=preprocessing_node.node_id,
            source_port="processed_emails",
            target_node_id=analysis_node.node_id,
            target_port="emails",
        )
    )

    # Execute workflow
    context = await workflow_engine.execute_workflow(workflow)

    print(f"Workflow completed with status: {context.metadata.get('status')}")
    print(f"Execution path: {context.execution_path}")
    print(f"Errors: {len(context.errors)}")

    return context.metadata.get("status") == "completed"


async def test_sample_workflow():
    """Test the sample workflow from workflow_manager."""
    print("\nTesting sample workflow...")

    # Get the sample workflow
    sample_workflow = workflow_manager.create_sample_workflow()
    print(f"Created sample workflow: {sample_workflow.name}")
    print(f"Nodes: {len(sample_workflow.nodes)}")
    print(f"Connections: {len(sample_workflow.connections)}")

    # Execute the workflow
    context = await workflow_engine.execute_workflow(sample_workflow)

    print(f"Sample workflow completed with status: {context.metadata.get('status')}")
    print(f"Execution path: {context.execution_path}")
    print(f"Errors: {len(context.errors)}")

    return context.metadata.get("status") == "completed"


async def test_workflow_persistence():
    """Test saving and loading workflows."""
    print("\nTesting workflow persistence...")

    # Create and save a workflow
    workflow = workflow_manager.create_sample_workflow()
    saved_path = workflow_manager.save_workflow(workflow)
    print(f"Workflow saved to: {saved_path}")

    # Load the workflow
    loaded_workflow = workflow_manager.load_workflow(workflow.workflow_id)
    if loaded_workflow:
        print(f"Workflow loaded successfully: {loaded_workflow.name}")
        print(f"Nodes: {len(loaded_workflow.nodes)}")
        print(f"Connections: {len(loaded_workflow.connections)}")

        # Execute the loaded workflow
        context = await workflow_engine.execute_workflow(loaded_workflow)
        print(f"Loaded workflow executed with status: {context.metadata.get('status')}")

        return context.metadata.get("status") == "completed"
    else:
        print("Failed to load workflow")
        return False


async def test_node_types():
    """Test that all node types are properly registered."""
    print("\nTesting node type registration...")

    registered_types = workflow_engine.get_registered_node_types()
    expected_types = [
        "EmailSourceNode",
        "PreprocessingNode",
        "AIAnalysisNode",
        "FilterNode",
        "ActionNode",
    ]

    print(f"Registered node types: {registered_types}")

    all_registered = all(node_type in registered_types for node_type in expected_types)
    print(f"All expected node types registered: {all_registered}")

    return all_registered


async def main():
    """Run all tests."""
    print("Starting Node-Based Architecture Tests\n")

    results = []

    try:
        results.append(("Basic Workflow", await test_basic_workflow()))
    except Exception as e:
        print(f"Basic workflow test failed: {e}")
        results.append(("Basic Workflow", False))

    try:
        results.append(("Sample Workflow", await test_sample_workflow()))
    except Exception as e:
        print(f"Sample workflow test failed: {e}")
        results.append(("Sample Workflow", False))

    try:
        results.append(("Workflow Persistence", await test_workflow_persistence()))
    except Exception as e:
        print(f"Workflow persistence test failed: {e}")
        results.append(("Workflow Persistence", False))

    try:
        results.append(("Node Types", await test_node_types()))
    except Exception as e:
        print(f"Node types test failed: {e}")
        results.append(("Node Types", False))

    print("\nTest Results:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

    return all_passed


if __name__ == "__main__":
    # Import here to avoid circular dependency issues
    from backend.node_engine.node_base import Connection

    asyncio.run(main())
