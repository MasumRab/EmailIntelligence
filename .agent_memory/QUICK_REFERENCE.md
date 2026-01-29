# Agent Memory System - Quick Reference

## One-Minute Setup

```python
from memory_api import create_or_load_memory

# Load existing or create new session
memory = create_or_load_memory()

# Save after changes
memory.save_session()
```

## Common Commands

### Log Work
```python
memory.add_work_log("Action description", "Detailed information")
```

### Manage Todos
```python
# Add todo
memory.add_todo("todo_1", "Title", "Description", priority="high")

# Update status
memory.update_todo("todo_1", "in_progress")

# Get todos
todos = memory.get_outstanding_todos(priority="high")
```

### Check Status
```python
# Ready to implement
ready = memory.get_ready_tasks()

# Currently blocked
blocked = memory.get_blocked_tasks()

# Summary
memory.print_summary()
```

### Track Metrics
```python
# Update metrics
memory.update_metrics(files_enhanced=9, lines_added=3190)

# Retrieve metrics
metrics = memory.get_metrics()
```

## API Reference

| Method | Purpose |
|--------|---------|
| `load_session()` | Load from disk |
| `save_session()` | Persist changes |
| `add_work_log()` | Log activity |
| `get_work_log()` | Retrieve logs |
| `add_todo()` | Create todo |
| `update_todo()` | Update status |
| `get_outstanding_todos()` | Query todos |
| `get_blocked_tasks()` | See blocked tasks |
| `get_ready_tasks()` | See ready tasks |
| `update_objective()` | Update objective |
| `get_objectives()` | Query objectives |
| `add_decision()` | Log decision |
| `add_artifact()` | Track output |
| `update_metrics()` | Update metrics |
| `print_summary()` | Human-readable |

## Query Examples

```python
# High-priority pending todos
high_priority = memory.get_outstanding_todos(priority="high", status="pending")

# Recent work (last 10 entries)
recent = memory.get_work_log(limit=10)

# Completed objectives
done = memory.get_objectives(status="completed")

# Check what's ready vs blocked
ready = memory.get_ready_tasks()      # Can start now
blocked = memory.get_blocked_tasks()  # Waiting
```

## Current Session

**Thread:** T-019b8c8f-9c59-769d-9b08-011b24e1565b  
**Status:** 2/3 objectives complete

### Ready Tasks
- task_75_1 (CommitHistoryAnalyzer)
- task_75_2 (CodebaseStructureAnalyzer)
- task_75_3 (DiffDistanceCalculator)

### Key Metrics
- Files enhanced: 9/9
- Lines added: 3,190
- Gotchas documented: 72
- YAML configs: 30

## Quick Examples

### Start of Day
```python
memory = create_or_load_memory()
todos = memory.get_outstanding_todos(priority="high")
ready = memory.get_ready_tasks()
print(f"Ready to work on: {ready}")
```

### During Work
```python
memory.add_work_log("Started implementation", "Working on metrics")
memory.update_todo("task_1", "in_progress")
memory.save_session()
```

### End of Day
```python
memory.update_metrics(progress="50%")
memory.print_summary()  # See what's done
memory.save_session()
```

### Agent Handoff
```python
# Current agent
memory.add_work_log("Phase complete", "Ready for next phase")
memory.save_session()

# Next agent
memory = create_or_load_memory()
todos = memory.get_outstanding_todos()
# Continue from where previous agent left off
```

## Full Docs

- **Complete Guide:** MEMORY_SYSTEM_GUIDE.md
- **Examples:** example_usage.py
- **API Details:** memory_api.py
- **Architecture:** ARCHITECTURE.md

## Performance

All operations complete in <100ms:
- Load: <50ms
- Save: <100ms
- Query: <10ms

Storage: ~5 KB per session
