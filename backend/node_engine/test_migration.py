"""
Test module for workflow migration utilities.
"""

import asyncio

from backend.node_engine.migration_utils import (
    WorkflowMigrationManager,
    generate_migration_plan,
    get_migration_report,
    migrate_legacy_workflow,
)


def test_migration_utilities():
    """Test the workflow migration utilities."""
    print("Testing workflow migration utilities...")

    # Create a sample legacy workflow configuration
    legacy_config = {
        "name": "Sample Legacy Workflow",
        "description": "A sample workflow for testing migration",
        "models": {"sentiment": "sentiment-default", "topic": "topic-default"},
    }

    print(f"Legacy config: {legacy_config}")

    # Test migration report
    print("\n1. Testing migration report...")
    report = get_migration_report(legacy_config)
    print(f"Migration report: {report}")

    # Test migration plan
    print("\n2. Testing migration plan...")
    plan = generate_migration_plan(legacy_config)
    print(f"Migration plan keys: {list(plan.keys())}")

    # Test actual migration
    print("\n3. Testing actual migration...")
    try:
        node_workflow = migrate_legacy_workflow(legacy_config, "Test Migrated Workflow")
        print(f"Migrated workflow name: {node_workflow.name}")
        print(f"Number of nodes: {len(node_workflow.nodes)}")
        print(f"Number of connections: {len(node_workflow.connections)}")

        # Print node information
        for node_id, node in node_workflow.nodes.items():
            print(f"  - Node: {node.name} ({node.__class__.__name__})")

        # Print connection information
        for conn in node_workflow.connections:
            print(
                f"  - Connection: {conn.source_node_id}:{conn.source_port} -> {conn.target_node_id}:{conn.target_port}"
            )

        print("[PASS] Migration test passed!")
        return True

    except Exception as e:
        print(f"[FAIL] Migration test failed: {e}")
        return False


def test_migration_manager():
    """Test the migration manager functionality."""
    print("\n\nTesting migration manager...")

    manager = WorkflowMigrationManager()

    # Test with a simple config
    legacy_config = {
        "name": "Manager Test Workflow",
        "description": "Testing migration manager",
        "models": {"sentiment": "test-sentiment", "topic": "test-topic"},
    }

    try:
        plan = manager.generate_migration_plan(legacy_config)
        print(f"[PASS] Migration manager test passed! Plan has keys: {list(plan.keys())}")
        return True
    except Exception as e:
        print(f"[FAIL] Migration manager test failed: {e}")
        return False


if __name__ == "__main__":
    print("Starting workflow migration utility tests...\n")

    results = []
    results.append(test_migration_utilities())
    results.append(test_migration_manager())

    print(f"\nTest Results: {sum(results)}/{len(results)} passed")

    if all(results):
        print("[SUCCESS] All migration utility tests passed!")
    else:
        print("[ERROR] Some tests failed.")
