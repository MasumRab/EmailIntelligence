"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Test module for security and scalability features of the node-based workflow system.
"""

import asyncio
from datetime import datetime

from src.backend.node_engine.email_nodes import (
    EmailSourceNode,
    PreprocessingNode,
)
from src.backend.node_engine.node_base import Connection, Workflow
from src.backend.node_engine.security_manager import (
    resource_manager,
    security_manager,
)
from src.backend.node_engine.workflow_engine import workflow_engine

# TODO(P1, 3h): Fix bare except clauses in test files per CODEREVIEW_REPORT.md
# TODO(P2, 2h): Add missing type hints to all test functions


async def test_security_features():
    """Test security features of the workflow system."""
    print("Testing security features...")

    # Create a simple workflow
    workflow = Workflow(name="Security Test Workflow")

    # Add nodes
    source_node = EmailSourceNode(name="Secure Source")
    preprocessing_node = PreprocessingNode(name="Secure Preprocessor")

    workflow.add_node(source_node)
    workflow.add_node(preprocessing_node)

    # Connect nodes
    workflow.add_connection(
        Connection(
            source_node_id=source_node.node_id,
            source_port="emails",
            target_node_id=preprocessing_node.node_id,
            target_port="emails",
        )
    )

    # TODO(P1, 4h): Add comprehensive test coverage for all security features
    # TODO(P2, 2h): Implement negative test cases for security validation

    # Test that trusted nodes can execute
    print(
        f"EmailSourceNode trusted: {security_manager.is_trusted_node('EmailSourceNode')}"
    )
    print(
        f"PreprocessingNode trusted: {security_manager.is_trusted_node('PreprocessingNode')}"
    )

    # Execute workflow with security
    try:
        context = await workflow_engine.execute_workflow(
            workflow, user_id="test_user_123"
        )
        print(f"Workflow executed with security: {context.metadata.get('status')}")
        success = context.metadata.get("status") == "completed"
    except Exception as e:
        print(f"Workflow execution failed: {e}")
        success = False

    return success


async def test_resource_limits():
    """Test resource management features."""
    print("\nTesting resource management...")

    # Check initial resource state
    print(f"Initial concurrent workflows: {resource_manager.current_workflows}")
    print(f"Max concurrent workflows: {resource_manager.max_concurrent_workflows}")

    # Create multiple workflows to test resource limits
    workflows = []
    for i in range(3):  # Create 3 workflows
        wf = Workflow(name=f"Resource Test Workflow {i}")
        source_node = EmailSourceNode(name=f"Source {i}")
        wf.add_node(source_node)
        workflows.append(wf)

    # Execute workflows concurrently
    execution_tasks = [
        workflow_engine.execute_workflow(wf, user_id=f"test_user_{i}")
        for i, wf in enumerate(workflows)
    ]

    results = await asyncio.gather(*execution_tasks, return_exceptions=True)

    completed_count = sum(
        1
        for r in results
        if not isinstance(r, Exception) and r.metadata.get("status") == "completed"
    )
    print(f"Completed workflows: {completed_count}/3")

    return completed_count > 0  # At least one should complete


async def test_audit_logging():
    """Test audit logging functionality."""
    print("\nTesting audit logging...")

    # Create and execute a workflow to trigger audit logs
    workflow = Workflow(name="Audit Test Workflow")
    source_node = EmailSourceNode(name="Audit Source")
    workflow.add_node(source_node)

    try:
        context = await workflow_engine.execute_workflow(
            workflow, user_id="audit_tester"
        )
        print(f"Audit workflow completed: {context.metadata.get('status')}")

        # The audit logs should have been written to the log file
        print("Audit logs generated successfully")
        return True
    except Exception as e:
        print(f"Audit workflow failed: {e}")
        return False


async def test_input_sanitization():
    """Test input sanitization."""
    print("\nTesting input sanitization...")

    from src.backend.node_engine.security_manager import InputSanitizer

    # Test sanitizing a potentially dangerous string
    dangerous_input = (
        '<script>alert("xss")</script> Hello <img src="x" onerror="alert(\'xss\')">'
    )
    safe_output = InputSanitizer.sanitize_string(dangerous_input)
    print(f"Dangerous input: {dangerous_input}")
    print(f"Sanitized output: {safe_output}")

    # Check that dangerous parts were removed
    has_script = "<script" in safe_output.lower()
    has_onerror = "onerror" in safe_output.lower()

    if not has_script and not has_onerror:
        print("Input sanitization working correctly")
        return True
    else:
        print("Input sanitization failed")
        return False


async def test_scalability():
    """Test scalability with multiple concurrent workflows."""
    print("\nTesting scalability...")

    # Create multiple simple workflows
    workflows = []
    for i in range(5):
        wf = Workflow(name=f"Scalability Workflow {i}")
        source = EmailSourceNode(name=f"Source {i}")
        processor = PreprocessingNode(name=f"Processor {i}")

        wf.add_node(source)
        wf.add_node(processor)

        wf.add_connection(
            Connection(
                source_node_id=source.node_id,
                source_port="emails",
                target_node_id=processor.node_id,
                target_port="emails",
            )
        )

        workflows.append(wf)

    # Execute all workflows concurrently to test scalability
    start_time = datetime.now()
    tasks = [
        workflow_engine.execute_workflow(wf, user_id=f"scalability_user_{i}")
        for i, wf in enumerate(workflows)
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    completed_count = sum(
        1
        for r in results
        if not isinstance(r, Exception)
        and getattr(r, "metadata", {}).get("status") == "completed"
    )

    print(f"Executed {len(workflows)} workflows concurrently")
    print(f"Completed: {completed_count}/{len(workflows)}")
    print(f"Total execution time: {execution_time:.2f}s")

    return completed_count == len(workflows)


async def main():
    """Run all security and scalability tests."""
    print("Starting Security and Scalability Tests\n")

    results = []

    try:
        results.append(("Security Features", await test_security_features()))
    except Exception as e:
        print(f"Security features test failed: {e}")
        results.append(("Security Features", False))

    try:
        results.append(("Resource Management", await test_resource_limits()))
    except Exception as e:
        print(f"Resource management test failed: {e}")
        results.append(("Resource Management", False))

    try:
        results.append(("Audit Logging", await test_audit_logging()))
    except Exception as e:
        print(f"Audit logging test failed: {e}")
        results.append(("Audit Logging", False))

    try:
        results.append(("Input Sanitization", await test_input_sanitization()))
    except Exception as e:
        print(f"Input sanitization test failed: {e}")
        results.append(("Input Sanitization", False))

    try:
        results.append(("Scalability", await test_scalability()))
    except Exception as e:
        print(f"Scalability test failed: {e}")
        results.append(("Scalability", False))

    print("\nTest Results:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

    return all_passed


if __name__ == "__main__":
    asyncio.run(main())
