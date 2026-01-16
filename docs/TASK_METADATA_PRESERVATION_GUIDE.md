# Task Metadata Preservation Guide

## Overview

Task Master AI has a known limitation where custom fields added to `tasks.json` are stripped during serialization via `TaskEntity.toJSON()`. This guide documents:

1. **What fields are lost** during task-master operations
2. **How to preserve extended metadata** using structured embedding
3. **Backup strategies** to prevent data loss
4. **Canonical workflows** for using task-master without losing information

**Reference:** [GitHub Issue #1555](https://github.com/eyaltoledano/claude-task-master/issues/1555)

---

## Fields Not Captured by Task Master Schema

### Standard Schema (Preserved)

| Field | Task | Subtask | Notes |
|-------|------|---------|-------|
| `id` | ✅ | ✅ | Required, auto-managed |
| `title` | ✅ | ✅ | Required |
| `description` | ✅ | ✅ | Required |
| `status` | ✅ | ✅ | Required |
| `priority` | ✅ | ❌ | Tasks only |
| `dependencies` | ✅ | ✅ | Array of IDs |
| `details` | ✅ | ✅ | **Extension point** |
| `testStrategy` | ✅ | ❌ | Tasks only |
| `subtasks` | ✅ | ❌ | Nested array |
| `parentTaskId` | ❌ | ✅ | Auto-set |

### Extended Fields (Lost on Serialization)

| Field | Description | Workaround |
|-------|-------------|------------|
| `effort` | Time estimate (e.g., "2-3h") | Embed in `details` |
| `complexity` | Difficulty score (e.g., "7/10") | Use `analyze-complexity` + embed |
| `owner` | Assigned person | Embed in `details` |
| `initiative` | Grouping identifier | Embed in `details` |
| `blocks` | Downstream dependencies | Embed in `details` |
| `scope` | Task scope definition | Embed in `details` |
| `focus` | Primary focus area | Embed in `details` |
| `successCriteria` | Checklist of criteria | Embed in `details` |
| `progressLog` | Timestamped notes | Use `update-subtask` + embed |
| `testStrategy` (subtask) | Subtask test approach | Embed in subtask `details` |

---

## Metadata Embedding Strategy

### Structured Format in `details` Field

Use HTML comments to embed extended metadata that survives task-master operations:

```markdown
Implementation steps here...

1. Step one
2. Step two

<!-- EXTENDED_METADATA
effort: 2-3h
complexity: 7/10
owner: developer-name
initiative: Core Framework
blocks: Tasks 016-017
scope: Strategic framework definition
successCriteria:
  - Target selection criteria defined
  - Alignment strategy documented
  - All branches assessed
progressLog: |
  2026-01-06: Initial setup
  2026-01-07: Completed analysis
END_EXTENDED_METADATA -->
```

### Why HTML Comments?

1. **Invisible in rendered markdown** - Clean display
2. **Preserved by task-master** - Not stripped during AI operations
3. **Parseable** - Scripts can extract and update
4. **Human-editable** - Easy to manually modify

---

## The Task Metadata Manager Script

### Location
```
.taskmaster/scripts/task_metadata_manager.py
```

### Commands

```bash
# Embed metadata from markdown file into tasks.json
python scripts/task_metadata_manager.py embed --task 001

# Backup task markdown files (timestamped)
python scripts/task_metadata_manager.py backup --task 001
python scripts/task_metadata_manager.py backup --all

# List available backups
python scripts/task_metadata_manager.py list-backups --task 001

# Restore from backup (0 = most recent)
python scripts/task_metadata_manager.py restore --task 001 --index 0

# Generate metadata coverage report
python scripts/task_metadata_manager.py report
```

### Backup Directory Structure

```
.taskmaster/backups/task_markdown_backups/
├── task-001/
│   ├── task-001_20260113_120000.md
│   ├── task-001_json_20260113_120000.json
│   ├── task-001-1_20260113_120000.md
│   └── ...
├── task-002/
│   └── ...
```

---

## Canonical Workflows Using Task Master

### Workflow 1: Adding a New Task from Markdown

**Goal:** Load a richly-detailed markdown task into tasks.json without losing metadata.

```bash
# 1. Backup before any operation
python scripts/task_metadata_manager.py backup --all

# 2. Add parent task via CLI
task-master add-task --prompt="<task title and description>" --priority=high

# 3. Add subtasks with details including embedded metadata
task-master add-subtask --parent=1 --title="Subtask Title" \
  --description="Brief description" \
  --details="Implementation steps...

<!-- EXTENDED_METADATA
effort: 2-3h
complexity: 5/10
owner: TBD
successCriteria:
  - Criterion 1
  - Criterion 2
END_EXTENDED_METADATA -->"

# 4. Verify with show
task-master show 1
```

### Workflow 2: Enhancing Tasks with Complexity Analysis

**Goal:** Use `analyze-complexity` to add complexity scores, then preserve them.

```bash
# 1. Backup first
python scripts/task_metadata_manager.py backup --all

# 2. Run complexity analysis (creates separate report)
task-master analyze-complexity --research

# 3. View the report
task-master complexity-report

# 4. The complexity scores are in .taskmaster/reports/task-complexity-report.json
# They are NOT added to tasks.json automatically

# 5. To preserve complexity in tasks, embed it manually or via script:
python scripts/task_metadata_manager.py embed --task 001
```

### Workflow 3: Using Research for Task Enhancement

**Goal:** Use `--research` flag to enhance tasks with up-to-date information.

```bash
# 1. Backup first
python scripts/task_metadata_manager.py backup --task 001

# 2. Update task with research (CAUTION: may overwrite details)
task-master update-task 1 "Add implementation details for authentication" --research

# 3. If extended metadata was lost, restore from backup and re-embed
python scripts/task_metadata_manager.py list-backups --task 001
# If needed: python scripts/task_metadata_manager.py restore --task 001

# 4. Re-embed metadata from markdown source
python scripts/task_metadata_manager.py embed --task 001
```

### Workflow 4: Expanding Tasks into Subtasks

**Goal:** Use `expand` to break down tasks without losing parent metadata.

```bash
# 1. Backup first (CRITICAL - expand modifies the task)
python scripts/task_metadata_manager.py backup --task 001

# 2. Expand with research
task-master expand --id=1 --research --num=8

# 3. Check what was created
task-master show 1

# 4. Generated subtasks will have AI-generated details but NO extended metadata
# 5. For each subtask, add extended metadata manually:
task-master update-subtask --id=1.1 --prompt="Add effort estimate: 2-3h, complexity: 4/10"

# 6. Or update the markdown backup and re-embed
```

### Workflow 5: Recovering from Data Loss

**Goal:** Restore lost metadata after a destructive operation.

```bash
# 1. List available backups
python scripts/task_metadata_manager.py list-backups --task 001

# 2. Restore the most recent backup (index 0)
python scripts/task_metadata_manager.py restore --task 001 --index 0

# 3. Re-embed metadata into tasks.json
python scripts/task_metadata_manager.py embed --task 001

# 4. Regenerate task files from tasks.json
task-master generate
```

---

## Operations That Can Cause Data Loss

### High Risk (Always Backup First)

| Operation | Risk | What's Lost |
|-----------|------|-------------|
| `parse-prd` | HIGH | Replaces/appends tasks, loses hierarchy |
| `expand --id` | HIGH | May regenerate parent task details |
| `update-task --id` | MEDIUM | AI may overwrite details field |
| `update --from` | HIGH | Updates multiple tasks, can overwrite all |

### Safe Operations

| Operation | Risk | Notes |
|-----------|------|-------|
| `list` | NONE | Read-only |
| `show` | NONE | Read-only |
| `next` | NONE | Read-only |
| `set-status` | LOW | Only changes status field |
| `add-subtask` | LOW | Adds new, doesn't modify existing |
| `update-subtask --prompt` | LOW | Appends to details, doesn't replace |
| `generate` | LOW | Regenerates markdown from JSON |

---

## Best Practices

### Before Any Modification

```bash
# Always backup before destructive operations
python scripts/task_metadata_manager.py backup --all
```

### Markdown as Source of Truth

1. **Keep detailed markdown files** (task-001.md, task-001-1.md, etc.)
2. **Use tasks.json for task-master operations only**
3. **Sync metadata from markdown to JSON** using the embed command
4. **Never rely solely on tasks.json** for extended metadata

### Structured Details Field

Always include extended metadata in the `details` field using the HTML comment format:

```markdown
Your implementation details here...

<!-- EXTENDED_METADATA
effort: X hours
complexity: Y/10
owner: name
successCriteria:
  - Criterion 1
  - Criterion 2
END_EXTENDED_METADATA -->
```

### Regular Backups

Set up a pre-commit hook or cron job:

```bash
# In .git/hooks/pre-commit or as a scheduled task
cd .taskmaster && python scripts/task_metadata_manager.py backup --all
```

---

## Integration with Complexity Reports

Task Master's `analyze-complexity` command generates a separate report file, not in-task metadata. To preserve complexity scores:

1. Run `task-master analyze-complexity --research`
2. Check `.taskmaster/reports/task-complexity-report.json`
3. Extract complexity scores and embed them in task details:

```bash
# The report contains:
# {
#   "taskId": 1,
#   "complexityScore": 7,
#   "recommendedSubtasks": 8,
#   "reasoning": "..."
# }

# Embed in task details using update-subtask or manual edit
```

---

## Future: Metadata Field (PR #1557)

A proposed `metadata: Record<string, unknown>` field would:

- Allow arbitrary key-value pairs
- Be preserved across all operations
- Support: UUIDs, GitHub issues, effort, complexity, owner, etc.

Until merged, use the embedding strategy documented above.

---

## Summary

| Scenario | Action |
|----------|--------|
| Adding new task | Use `add-task` + `add-subtask` with embedded metadata in details |
| Before any update | Run `backup --all` |
| After parse-prd | Check what was created, add metadata via `update-subtask` |
| After expand | Verify subtasks, add extended metadata manually |
| Lost metadata | Restore from backup, re-embed |
| Complexity scores | Run `analyze-complexity`, embed scores in details |
| Research enhancement | Backup first, then `--research`, verify nothing lost |

---

*This guide ensures no task information is lost when using Task Master AI.*
