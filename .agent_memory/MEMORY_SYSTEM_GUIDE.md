# Agent Memory System Guide

## Overview

The Agent Memory System is a structured JSON-based logging and retrieval mechanism designed for agentic workflows. It maintains persistent session state across work sessions, enabling agents to:

- Track objectives and completion status
- Log work activities with timestamps
- Manage artifact creation and verification
- Track task dependencies and blocking relationships
- Maintain decision history with rationale
- Prioritize outstanding todos
- Query metrics and progress

## Architecture

### Core Files

```
.agent_memory/
├── session_log.json        # Main memory storage (JSON)
├── memory_api.py           # Python API for accessing memory
└── MEMORY_SYSTEM_GUIDE.md  # This file
```

### Data Structure

The `session_log.json` file contains:

```json
{
  "session_metadata": {},      // Session info, agent name, thread URL
  "objectives": [],            // What the agent is trying to accomplish
  "context": {},               // Project/directory context
  "artifacts_created": [],     // Outputs generated
  "work_log": [],              // Timestamped activities
  "metrics": {},               // Quantified progress
  "dependencies": {},          // Task blocking relationships
  "decisions": [],             // Significant decisions made
  "outstanding_todos": []      // Action items
}
```

## Usage

### Basic Workflow

```python
from memory_api import AgentMemory

# Load or create session
memory = AgentMemory()
memory.load_session()

# Log work
memory.add_work_log(
    action="Analyzed task files",
    details="Reviewed all 9 Task 75 documentation files"
)

# Track objectives
memory.update_objective("obj_1", "completed")

# Add outstanding todos
memory.add_todo(
    todo_id="todo_1",
    title="Implement memory tracking API",
    description="Create Python interface for querying memory",
    priority="high"
)

# Query memory
outstanding = memory.get_outstanding_todos(priority="high")
blocked_tasks = memory.get_blocked_tasks()
ready_tasks = memory.get_ready_tasks()

# Save changes
memory.save_session()
```

### Common Operations

#### Track Work Activities

```python
memory.add_work_log(
    action="Applied 7 improvements to Task 75.1",
    details="Quick Navigation, Performance Baselines, ...",
    status="completed"
)

# Retrieve recent activities
recent_work = memory.get_work_log(limit=10)
```

#### Manage Objectives

```python
# Update objective status
memory.update_objective(
    obj_id="obj_1",
    status="completed"
)

# Get incomplete objectives
pending = memory.get_objectives(status="pending")
in_progress = memory.get_objectives(status="in_progress")
```

#### Track Artifacts

```python
memory.add_artifact(
    artifact_id="artifact_1",
    name="TASK_75_DOCUMENTATION_INDEX.md",
    description="Master index of all Task 75 files",
    file_path="/home/masum/github/PR/.taskmaster/TASK_75_DOCUMENTATION_INDEX.md",
    status="verified"
)
```

#### Manage Dependencies

The memory system tracks task blocking relationships:

```python
# Query blocked tasks
blocked = memory.get_blocked_tasks()
# Returns: [{'task': 'task_75_4', 'blocked_by': ['task_75_1', '...'], 'blocks': [...]}, ...]

# Query ready tasks
ready = memory.get_ready_tasks()
# Returns: ['task_75_1', 'task_75_2', 'task_75_3', ...]
```

#### Log Decisions

```python
memory.add_decision(
    decision_id="dec_1",
    decision="Use externalized YAML configuration for all tasks",
    rationale="Enables easy tuning without code changes",
    impact="30+ YAML templates created across all tasks"
)
```

#### Manage Todos

```python
# Add high-priority todo
memory.add_todo(
    todo_id="todo_1",
    title="Complete Task 75.1 implementation",
    description="Implement CommitHistoryAnalyzer class with all metrics",
    priority="high",
    depends_on=["setup_environment"]
)

# Update status
memory.update_todo("todo_1", "in_progress")

# Query todos
high_priority = memory.get_outstanding_todos(priority="high")
pending = memory.get_outstanding_todos(status="pending")
```

## Query Patterns

### Get Current Status

```python
memory.print_summary()  # Human-readable summary
```

### Check Implementation Readiness

```python
ready_tasks = memory.get_ready_tasks()
if 'task_75_1' in ready_tasks:
    print("Task 75.1 is ready for implementation")

blocked = memory.get_blocked_tasks()
for task_info in blocked:
    print(f"{task_info['task']} blocked by {task_info['blocked_by']}")
```

### Track Progress

```python
metrics = memory.get_metrics()
print(f"Files enhanced: {metrics.get('files_enhanced')}")
print(f"Total lines added: {metrics.get('total_lines_added')}")

objectives = memory.get_objectives()
completed = len(memory.get_objectives(status="completed"))
total = len(objectives)
print(f"Objectives: {completed}/{total} complete")
```

### Prioritize Work

```python
# Get high-priority pending todos
todos = memory.get_outstanding_todos(priority="high", status="pending")
for todo in todos:
    deps = todo.get("depends_on", [])
    if deps:
        print(f"{todo['title']} (depends on {deps})")
    else:
        print(f"{todo['title']} (ready to start)")
```

## Best Practices

### 1. Load Before Using

Always load existing session before making changes:

```python
memory = AgentMemory()
if memory.load_session():
    print("Loaded existing session")
else:
    print("Starting new session")
```

### 2. Save After Changes

Save session after significant updates:

```python
memory.add_work_log(...)
memory.update_todo(...)
memory.save_session()  # Persist changes
```

### 3. Timestamped Activities

All work logs are automatically timestamped:

```python
memory.add_work_log("Completed Task 75.1", "Implemented metrics")
# Automatically includes: "timestamp": "2025-01-05T12:34:56Z"
```

### 4. Use Meaningful IDs

Use descriptive, consistent IDs for todos and artifacts:

```python
# Good
memory.add_todo("todo_implement_75_1", "Implement Task 75.1", ...)

# Avoid
memory.add_todo("t1", "Do work", ...)
```

### 5. Document Dependencies

Always specify blocking relationships:

```python
memory.add_todo(
    "todo_implement_75_4",
    "Implement Task 75.4: BranchClusterer",
    depends_on=["todo_implement_75_1", "todo_implement_75_2", "todo_implement_75_3"]
)
```

### 6. Regular Summaries

Use print_summary() to review progress:

```python
memory.print_summary()
# Shows: Objectives, Todos, Ready Tasks, Blocked Tasks, Metrics
```

## Integration with Workflows

### Agent Handoff

When handing off work to another agent:

```python
# Current agent
memory.add_work_log("Completed phase 1", "All task files enhanced")
memory.update_objective("obj_1", "completed")
memory.save_session()

# New agent picks up
memory = AgentMemory()
memory.load_session()
outstanding = memory.get_outstanding_todos(priority="high")
```

### Task Sequencing

Use memory to enforce task sequencing:

```python
blocked_tasks = memory.get_blocked_tasks()
ready_tasks = memory.get_ready_tasks()

if 'task_75_4' in blocked_tasks:
    print("Task 75.4 blocked, cannot proceed")
    print(f"Blocked by: {task_info['blocked_by']}")
elif 'task_75_1' in ready_tasks:
    print("Start with Task 75.1")
```

### Progress Tracking

Monitor completion progress:

```python
def show_progress():
    objectives = memory.get_objectives()
    todos = memory.get_outstanding_todos()
    
    obj_done = len(memory.get_objectives(status="completed"))
    todo_done = len(memory.get_outstanding_todos(status="completed"))
    
    print(f"Objectives: {obj_done}/{len(objectives)}")
    print(f"Todos: {todo_done}/{len(todos)}")
```

## Data Schema Reference

### Session Metadata

```json
{
  "session_id": "T-019b8c8f-9c59-...",
  "start_time": "2025-01-05T00:00:00Z",
  "agent_name": "Documentation Enhancement Agent",
  "project": "Email Intelligence Branch Clustering System",
  "thread_url": "https://ampcode.com/threads/T-..."
}
```

### Work Log Entry

```json
{
  "timestamp": "2025-01-04T20:30:00Z",
  "action": "Applied 7 improvements to Task 75.1",
  "details": "Quick Navigation, Performance Baselines, ...",
  "status": "completed"
}
```

### Todo Entry

```json
{
  "id": "todo_1",
  "title": "Implement memory tracking system",
  "description": "Create structured session logging...",
  "priority": "high",
  "status": "pending",
  "assigned_to": "Documentation Enhancement Agent",
  "depends_on": ["todo_setup"]
}
```

### Objective Entry

```json
{
  "id": "obj_1",
  "title": "Apply 7 improvements to all 9 Task 75 files",
  "status": "completed",
  "completion_date": "2025-01-04T23:59:59Z"
}
```

## Troubleshooting

### Memory Not Loading

```python
memory = AgentMemory(".agent_memory")
if not memory.load_session():
    print("No existing session, starting fresh")
    # Initialize with defaults
```

### Corrupted JSON

If `session_log.json` becomes corrupted:

1. Check file syntax: `python -m json.tool .agent_memory/session_log.json`
2. Restore from backup if available
3. Or start fresh and re-populate memory

### Large Session Files

If session log grows large, consider archiving old entries:

```python
# Extract old work logs for archiving
old_logs = [log for log in memory.get_work_log(limit=1000) 
            if log['timestamp'] < '2025-01-01']
# Save to archive, clear from memory
```

## Future Enhancements

Potential improvements to the memory system:

- **Persistence Backends**: Support for database backends (SQLite, etc.)
- **Compression**: Automatic compression of large session files
- **Versioning**: Session snapshots at key milestones
- **Sync**: Multi-agent memory synchronization
- **Analytics**: Agent productivity metrics and trends
- **Visualization**: Dashboard showing session progress

## Summary

The Agent Memory System provides:

✅ **Structured Logging** - JSON-based session persistence  
✅ **Progress Tracking** - Objectives, todos, metrics  
✅ **Dependency Management** - Task blocking relationships  
✅ **Decision History** - Rationale for important choices  
✅ **Easy Querying** - Python API for common operations  
✅ **Agent Handoff** - Seamless work transfer between agents  

Use it to maintain continuity across long-running agentic workflows.
