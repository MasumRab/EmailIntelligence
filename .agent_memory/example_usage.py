#!/usr/bin/env python3
"""
Example usage of the Agent Memory System.

Demonstrates common patterns for tracking agent work, managing objectives,
and querying session state.
"""

from memory_api import AgentMemory, create_or_load_memory


def example_basic_workflow():
    """Example: Basic workflow with objectives and todos."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Workflow")
    print("="*80)
    
    memory = create_or_load_memory(".agent_memory")
    
    # Log an activity
    memory.add_work_log(
        action="Initialized agent memory system",
        details="Set up structured session logging for Task 75 work"
    )
    
    # Check outstanding todos
    high_priority = memory.get_outstanding_todos(priority="high")
    print(f"\nHigh Priority Todos: {len(high_priority)}")
    for todo in high_priority[:3]:
        print(f"  - [{todo['status'].upper()}] {todo['title']}")
    
    memory.save_session()
    print("\n✓ Session saved")


def example_track_implementation():
    """Example: Track implementation progress."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Track Implementation Progress")
    print("="*80)
    
    memory = create_or_load_memory(".agent_memory")
    
    # Start implementing Task 75.1
    memory.update_todo("todo_1", "in_progress")
    memory.add_work_log(
        action="Started Task 75.1 implementation",
        details="Beginning CommitHistoryAnalyzer class development"
    )
    
    # Check what's ready to implement
    ready = memory.get_ready_tasks()
    print(f"\nTasks ready for implementation: {len(ready)}")
    for task in ready:
        print(f"  ✓ {task}")
    
    # Check what's blocked
    blocked = memory.get_blocked_tasks()
    print(f"\nBlocked tasks: {len(blocked)}")
    for task_info in blocked:
        print(f"  ✗ {task_info['task']} (blocked by {', '.join(task_info['blocked_by'])})")
    
    memory.save_session()


def example_decision_tracking():
    """Example: Track significant decisions."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Decision Tracking")
    print("="*80)
    
    memory = create_or_load_memory(".agent_memory")
    
    # Add a decision
    memory.add_decision(
        decision_id="dec_impl_1",
        decision="Use subprocess with 30-second timeout for git commands",
        rationale="Prevents hanging on large repositories (10,000+ commits)",
        impact="All analyzers (75.1-75.3) now handle timeout gracefully"
    )
    
    # View decisions
    decisions = memory.memory.get("decisions", [])
    print(f"\nSignificant Decisions: {len(decisions)}")
    for dec in decisions[-3:]:  # Show last 3
        print(f"\n  Decision: {dec['decision']}")
        print(f"  Rationale: {dec['rationale']}")
        print(f"  Impact: {dec['impact']}")
    
    memory.save_session()


def example_milestone_completion():
    """Example: Complete a milestone."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Milestone Completion")
    print("="*80)
    
    memory = create_or_load_memory(".agent_memory")
    
    # Update metrics
    memory.update_metrics(
        files_enhanced=9,
        improvements_applied=7,
        total_lines_added=3190,
        task_75_1_status="ready_for_implementation"
    )
    
    # Log milestone
    memory.add_work_log(
        action="Documentation enhancement phase complete",
        details="All 9 Task 75 files enhanced with 7 improvements",
        status="completed"
    )
    
    # Show summary
    memory.print_summary()


def example_agent_handoff():
    """Example: Prepare for agent handoff."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Prepare for Agent Handoff")
    print("="*80)
    
    memory = create_or_load_memory(".agent_memory")
    
    # Add todos for next agent
    memory.add_todo(
        todo_id="todo_impl_75_1",
        title="Implement Task 75.1: CommitHistoryAnalyzer",
        description="Create Python class with 5 normalized metrics",
        priority="high",
        depends_on=[]
    )
    
    memory.add_todo(
        todo_id="todo_impl_75_2",
        title="Implement Task 75.2: CodebaseStructureAnalyzer",
        description="Create Python class with 4 normalized metrics",
        priority="high",
        depends_on=[]
    )
    
    # Log handoff
    memory.add_work_log(
        action="Prepared for implementation agent handoff",
        details="All todos created with dependencies and priorities",
        status="completed"
    )
    
    # Show outstanding work
    outstanding = memory.get_outstanding_todos()
    print(f"\nOutstanding Work Items: {len(outstanding)}")
    for todo in outstanding[:5]:
        deps = f" (depends on {', '.join(todo['depends_on'])})" if todo.get('depends_on') else ""
        print(f"  [{todo['priority'].upper()}] {todo['title']}{deps}")
    
    memory.save_session()
    print("\n✓ Ready for handoff")


def example_query_patterns():
    """Example: Common query patterns."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Common Query Patterns")
    print("="*80)
    
    memory = create_or_load_memory(".agent_memory")
    
    print("\nQuery Pattern 1: Get all high-priority pending todos")
    todos = memory.get_outstanding_todos(priority="high", status="pending")
    print(f"Found: {len(todos)}")
    
    print("\nQuery Pattern 2: Get metrics")
    metrics = memory.get_metrics()
    print(f"Files enhanced: {metrics.get('files_enhanced')}")
    print(f"Lines added: {metrics.get('total_lines_added')}")
    
    print("\nQuery Pattern 3: Get completed objectives")
    objectives = memory.get_objectives(status="completed")
    print(f"Completed: {len(objectives)}")
    for obj in objectives:
        print(f"  ✓ {obj['title']}")
    
    print("\nQuery Pattern 4: Get recent work log")
    recent = memory.get_work_log(limit=5)
    print(f"Recent activities:")
    for log in recent:
        print(f"  - {log['timestamp']}: {log['action']}")
    
    print("\nQuery Pattern 5: Check task readiness")
    ready = memory.get_ready_tasks()
    blocked = memory.get_blocked_tasks()
    print(f"Ready for implementation: {len(ready)}")
    print(f"Currently blocked: {len(blocked)}")


def example_create_context():
    """Example: Initialize new session context."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Initialize New Session")
    print("="*80)
    
    memory = AgentMemory(".agent_memory")
    
    # Start fresh session
    memory.memory = {
        "session_metadata": {
            "session_id": "T-new-session",
            "start_time": "2025-01-05T12:00:00Z",
            "agent_name": "Implementation Agent",
            "project": "Task 75 Implementation",
            "thread_url": "https://ampcode.com/threads/T-..."
        },
        "objectives": [
            {
                "id": "impl_1",
                "title": "Implement all Stage One analyzers (75.1-75.3)",
                "status": "pending",
                "completion_date": None
            }
        ],
        "context": {
            "directory": "/home/masum/github/PR/.taskmaster",
            "repository": "https://github.com/MasumRab/EmailIntelligence",
            "task_focus": "Task 75 Implementation"
        },
        "artifacts_created": [],
        "work_log": [],
        "metrics": {},
        "dependencies": {},
        "decisions": [],
        "outstanding_todos": []
    }
    
    memory.save_session()
    print("✓ New session created")
    memory.print_summary()


def main():
    """Run all examples."""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█  AGENT MEMORY SYSTEM - USAGE EXAMPLES" + " "*39 + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    try:
        example_basic_workflow()
        example_track_implementation()
        example_decision_tracking()
        example_milestone_completion()
        example_agent_handoff()
        example_query_patterns()
        # example_create_context()  # Uncomment to create fresh session
        
        print("\n" + "█"*80)
        print("█ All examples completed successfully!" + " "*41 + "█")
        print("█"*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
