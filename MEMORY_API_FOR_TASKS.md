# Memory API for Task Execution - Quick Integration Guide

**Version:** 1.0  
**Created:** January 6, 2026  
**Purpose:** How to integrate Memory API into task execution workflows  
**Audience:** Developers implementing tasks, team leads, agents

---

## What is the Memory API?

The Memory API (`.agent_memory/memory_api.py`) is a lightweight session tracking system that maintains project context across work sessions.

**Why use it?**
- ✅ Persists progress when switching between tasks
- ✅ Enables agent handoffs without context loss
- ✅ Documents decision history and blockers
- ✅ Helps multi-week implementations maintain continuity
- ✅ Optional - not required, but recommended

**Is it required?** No. Git commits are sufficient. But Memory API adds useful session continuity.

---

## Setup (One-Time, 2 minutes)

```python
# .agent_memory/memory_api.py exists and is ready to use
# No installation needed - uses only Python standard library

# Verify it exists
ls .agent_memory/memory_api.py
# Output: .agent_memory/memory_api.py (file found)
```

---

## Basic Pattern: Log Progress After Each Sub-Subtask

Add this pattern to task execution:

```python
from memory_api import AgentMemory

# 1. Load session at start of work
memory = AgentMemory()
memory.load_session()

# 2. Do your work...
# Implement sub-subtask 002.1.3

# 3. Log completion
memory.add_work_log(
    action="Completed Task 002.1.3",
    details="Implemented commit recency metric with exponential decay"
)

# 4. Mark subtask done
memory.update_todo("task_002_1_3", "completed")

# 5. Save
memory.save_session()
```

That's it. One 10-line pattern logs progress automatically.

---

## Integration Points for Task Files

### Point 1: Task Introduction (Start of task file)

In the "Purpose" or "Overview" section, add note about optional memory logging:

```markdown
## Overview

Create CommitHistoryAnalyzer class that extracts and scores commit history metrics.

**Optional:** Track progress using Memory API for multi-session work. See MEMORY_API_FOR_TASKS.md.
```

### Point 2: Implementation Guide (In each sub-subtask section)

In the "Implementation Guide" section for EACH sub-subtask:

```markdown
### 002.1.3: Implement Commit Recency Metric (3-4 hours)

[existing implementation steps...]

#### Progress Logging (Optional)

After completing this sub-subtask, log progress:

```python
from memory_api import AgentMemory
memory = AgentMemory()
memory.load_session()

memory.add_work_log(
    action="Completed 002.1.3: Commit Recency Metric",
    details="Exponential decay function, bounds checking, 100% test coverage"
)
memory.update_todo("task_002_1_3", "completed")
memory.save_session()
```

**What this does:**
- Logs completion for multi-session continuity
- Marks subtask as done in session
- Enables agent handoffs without context loss
- Optional - git commits are also sufficient
```

### Point 3: Testing Strategy Section

In the "Testing Strategy" section, add checkpoint logging:

```markdown
## Testing Strategy

### Unit Tests

[existing test requirements...]

#### Checkpoint: After Tests Pass

```python
# Log test completion
memory.add_work_log(
    action="Task 002.1 testing complete",
    details="All 8 unit tests passing, 95%+ coverage, edge cases verified"
)
```

This checkpoints completion for handoff to Task 002.4.
```

### Point 4: Done Definition Section

In the "Done Definition" section, add final logging:

```markdown
## Done Definition

Task 002.1 is done when:

1. ✅ All 8 sub-subtasks marked complete
2. ✅ Unit tests pass (>95% coverage)
3. ✅ Code review approved
4. ... (rest of criteria)

**Optional: Log final completion**

```python
memory.update_objective("obj_complete_task_002_1", "completed")
memory.save_session()
```
```

---

## Code Examples for Common Scenarios

### Scenario 1: Solo Developer, Single Session

```python
# At start of day
from memory_api import AgentMemory
memory = AgentMemory()
memory.load_session()

# Check what you're working on
outstanding = memory.get_outstanding_todos(priority="high", status="pending")
for todo in outstanding[:3]:  # Top 3 items
    print(f"TODO: {todo['title']}")

# ... do work on Task 002.1.3 ...

# Log progress
memory.add_work_log(
    action="Completed 002.1.3",
    details="Exponential decay implemented, normalized to [0,1]"
)
memory.update_todo("task_002_1_3", "completed")
memory.save_session()

# At end of day, show progress
memory.print_summary()
```

### Scenario 2: Multi-Session Work (Over Multiple Days)

```python
# Day 1 - Session Start
memory = AgentMemory()
memory.load_session()

memory.add_work_log("Starting Task 002.1", "Implementing CommitHistoryAnalyzer")
memory.update_todo("task_002_1", "in_progress")

# ... work for 4 hours ...

# Day 1 - Session End
memory.add_work_log("Day 1 progress", "Completed sub-subtasks 002.1.1 and 002.1.2")
memory.save_session()

# Day 2 - Session Start
memory.load_session()
memory.print_summary()
# Shows: 002.1.1 done, 002.1.2 done, 002.1.3-8 pending

# ... continue work ...

# Day 2 - Session End
memory.add_work_log("Day 2 progress", "Completed 002.1.3-5")
memory.save_session()

# Day 3 - Verify progress
memory.load_session()
todos_done = len(memory.get_outstanding_todos(status="completed"))
todos_total = len(memory.get_outstanding_todos())
print(f"Progress: {todos_done}/{todos_total} subtasks complete")
```

### Scenario 3: Agent Handoff

```python
# Agent A - End of shift
memory = AgentMemory()
memory.load_session()

memory.add_work_log(
    action="Agent A shift end",
    details="Completed 002.1.1-3, ready for 002.1.4"
)
memory.add_decision(
    decision_id="dec_1",
    decision="Use exponential decay for recency metric",
    rationale="Matches peer implementations, mathematically sound",
    impact="Consistent with downstream Task 002.4 expectations"
)
memory.save_session()

# Agent B - Start of shift
memory = AgentMemory()
memory.load_session()

# See exactly where Agent A left off
memory.print_summary()
# Shows: 002.1.1-3 done, decisions recorded, next: 002.1.4

print("Continuing from Agent A's work...")
todos_pending = memory.get_outstanding_todos(status="pending")
print(f"Next item: {todos_pending[0]['title']}")

# ... Agent B continues work ...

memory.add_work_log("Agent B continuing Task 002.1", "Starting 002.1.4")
memory.save_session()
```

### Scenario 4: Blocking & Dependencies

```python
memory = AgentMemory()
memory.load_session()

# Check if you can start Task 002.4
ready_tasks = memory.get_ready_tasks()
blocked_tasks = memory.get_blocked_tasks()

if 'task_002_4' in ready_tasks:
    print("Task 002.4 is ready to start")
    memory.add_work_log("Starting Task 002.4", "All dependencies complete")
elif 'task_002_4' in blocked_tasks:
    print("Task 002.4 blocked")
    task_info = [t for t in blocked_tasks if t['task'] == 'task_002_4'][0]
    print(f"Blocked by: {task_info['blocked_by']}")
    print("Wait for those to complete first")
```

### Scenario 5: Progress Metrics

```python
memory = AgentMemory()
memory.load_session()

# Get current metrics
metrics = memory.get_metrics()
print(f"Lines added so far: {metrics.get('lines_added', 0)}")
print(f"Files modified: {metrics.get('files_modified', 0)}")
print(f"Tests written: {metrics.get('tests_written', 0)}")

# Update metrics as work progresses
memory.update_metrics({
    "lines_added": 1247,
    "files_modified": 8,
    "tests_written": 12,
    "test_coverage": 95.2
})
memory.save_session()
```

---

## Integration Checklist for Task Files

When updating a task file with Memory API integration:

- [ ] Add optional note in Overview section
- [ ] Add code example in each Implementation Guide sub-subtask
- [ ] Add checkpoint logging in Testing Strategy section
- [ ] Add final logging in Done Definition section
- [ ] Reference this guide (MEMORY_API_FOR_TASKS.md)
- [ ] Make clear that it's optional (not required)
- [ ] Include copy-paste ready code snippets
- [ ] Don't clutch task file with too many details (keep external guide link short)

**Example format in task file:**

```markdown
#### Optional: Progress Logging

```python
from memory_api import AgentMemory
memory = AgentMemory()
memory.load_session()
memory.add_work_log("Completed 002.1.4", "BranchClusterer integration tested")
memory.save_session()
```

See MEMORY_API_FOR_TASKS.md § Scenario 1 for more examples.
```

---

## Common Patterns (Copy-Paste Ready)

### Log Sub-Subtask Completion

```python
from memory_api import AgentMemory

memory = AgentMemory()
memory.load_session()
memory.add_work_log("Completed [TASK ID]", "[WHAT YOU DID]")
memory.save_session()
```

### Mark Subtask Done

```python
memory.update_todo("task_002_1_3", "completed")
memory.save_session()
```

### Check What's Next

```python
outstanding = memory.get_outstanding_todos(priority="high", status="pending")
print(f"Next task: {outstanding[0]['title']}")
```

### Save Decision

```python
memory.add_decision(
    decision_id="dec_1",
    decision="[WHAT YOU DECIDED]",
    rationale="[WHY]",
    impact="[CONSEQUENCE]"
)
memory.save_session()
```

### Daily Progress Summary

```python
memory.print_summary()
```

### Verify Blocking Tasks

```python
blocked = memory.get_blocked_tasks()
for task in blocked:
    print(f"{task['task']} blocked by {task['blocked_by']}")
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'memory_api'"

**Fix:** Import from correct path:

```python
import sys
import os

# Add .agent_memory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".agent_memory"))
from memory_api import AgentMemory
```

### "session_log.json not found"

**Normal behavior** - script creates it automatically:

```python
memory = AgentMemory()
memory.load_session()  # Returns False, but creates default session
memory.save_session()  # Initializes file
```

### "Permission denied: .agent_memory/session_log.json"

**Fix:** Check file permissions:

```bash
# Check permissions
ls -la .agent_memory/session_log.json

# Fix if needed
chmod 644 .agent_memory/session_log.json
chmod 755 .agent_memory/
```

### "Session data not saving"

**Check:**

```python
success = memory.save_session()
if not success:
    print("Failed to save - check permissions")
else:
    print("Saved successfully")
```

### "Large session file causing slowness"

**Solution:** Archive old entries:

```python
# Get old work logs
old_logs = [log for log in memory.get_work_log(limit=1000) 
            if log['timestamp'] < '2026-01-01']

# Move to archive manually
# Then keep memory focused on active work
```

---

## Best Practices

### 1. Load at Start, Save at End

```python
# Session start
memory = AgentMemory()
memory.load_session()

# ... do work ...

# Session end
memory.save_session()
```

### 2. Log After Major Checkpoints

Don't log every single action. Log when:
- ✅ Sub-subtask completes
- ✅ Tests pass
- ✅ Code review approved
- ✅ Major decision made
- ✅ Session ends

### 3. Use Meaningful IDs

```python
# Good
memory.update_todo("task_002_1_3_recency_metric", "completed")

# Avoid
memory.update_todo("t1", "done")
```

### 4. Document Decisions

```python
# Include rationale so Agent B understands why you chose this approach
memory.add_decision(
    decision_id="dec_choose_scipy",
    decision="Use scipy.cluster.hierarchy for Ward linkage",
    rationale="Industry standard, proven on large datasets, good documentation",
    impact="Reduced implementation time by 40%, easier maintenance"
)
```

### 5. Keep Task Names Consistent

Use same task IDs across:
- Task files (task_002.1.md)
- Memory API todos ("task_002_1", "task_002_1_3", etc.)
- Git commits

---

## When NOT to Use Memory API

Memory API is optional. Use git commits alone if:
- [ ] Single-session, solo work
- [ ] No agent handoffs needed
- [ ] Work fits in one day
- [ ] Team prefers git as source of truth

**But Memory API is recommended if:**
- ✅ Multi-session work (work spans multiple days)
- ✅ Multiple developers/agents
- ✅ Need to preserve decisions made
- ✅ Complex task dependencies
- ✅ Want to document blockers and workarounds

---

## Integration with SCRIPTS_IN_TASK_WORKFLOW.md

This guide is linked from `SCRIPTS_IN_TASK_WORKFLOW.md` § Memory API section.

Both guides work together:
- **SCRIPTS_IN_TASK_WORKFLOW.md** - detailed API reference
- **MEMORY_API_FOR_TASKS.md** - quick integration patterns

Use this guide for "how do I integrate this into my task?" and the other guide for "what does this function do?"

---

## Next Steps

1. **Read** this guide (you're here)
2. **Review** `.agent_memory/MEMORY_SYSTEM_GUIDE.md` for full API docs
3. **Choose** to use or skip Memory API (it's optional)
4. **Integrate** into task_002.1-5.md files (add examples)
5. **Use** Memory API as you work on tasks
6. **Share** session file with next agent if handing off

---

## Reference

- **Quick API:** `.agent_memory/README.md`
- **Full API:** `.agent_memory/MEMORY_SYSTEM_GUIDE.md`
- **Architecture:** `.agent_memory/ARCHITECTURE.md`
- **Usage Examples:** `.agent_memory/example_usage.py`
- **Scripts Guide:** `SCRIPTS_IN_TASK_WORKFLOW.md`

---

**Last Updated:** January 6, 2026  
**Status:** Ready for Integration with Task Files
