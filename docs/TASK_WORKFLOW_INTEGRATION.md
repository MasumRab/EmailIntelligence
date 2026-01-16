# Task Workflow Integration Guide

## Overview

This document outlines how existing `.taskmaster/scripts/` tools integrate with the task metadata preservation workflow, enabling a complete pipeline from markdown source files to task-master operations without data loss.

---

## Script Ecosystem Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           TASK WORKFLOW PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐    ┌─────────────────┐    ┌──────────────────┐             │
│  │  Markdown   │───▶│  convert_md_to  │───▶│   tasks.json     │             │
│  │  Task Files │    │  _task_json.py  │    │   (with metadata)│             │
│  └─────────────┘    └─────────────────┘    └──────────────────┘             │
│         │                                           │                        │
│         │                                           ▼                        │
│         │           ┌─────────────────┐    ┌──────────────────┐             │
│         │           │  task-master    │◀───│  expand_subtasks │             │
│         │           │  CLI/MCP        │    │  .py             │             │
│         │           └─────────────────┘    └──────────────────┘             │
│         │                   │                                                │
│         ▼                   ▼                                                │
│  ┌─────────────┐    ┌─────────────────┐    ┌──────────────────┐             │
│  │  task_meta  │◀───│  RISK: Data     │───▶│  Backup/Restore  │             │
│  │  data_mgr   │    │  Loss Zone      │    │  Pipeline        │             │
│  └─────────────┘    └─────────────────┘    └──────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Existing Scripts by Category

### 1. Markdown → JSON Conversion

#### `convert_md_to_task_json.py`
**Purpose:** Convert a single markdown task file to tasks.json format

**Integration Point:** 
- **Input:** Task markdown files (task-001.md, etc.)
- **Output:** JSON structure compatible with tasks.json
- **Preserves:** `effort`, `complexity` (non-standard fields!)

```bash
# Convert single task markdown to JSON
python scripts/convert_md_to_task_json.py tasks/task-001.md > /tmp/task-001.json

# Merge into tasks.json (manual step needed)
```

**Enhancement Opportunity:** This script already extracts `effort` and `complexity` - integrate with `task_metadata_manager.py` to preserve them.

---

#### `expand_subtasks.py`
**Purpose:** Generate individual subtask markdown files from a parent task

**Integration Point:**
- **Input:** Parent task file with embedded subtask definitions
- **Output:** Individual task-XXX-Y.md files

```bash
# Expand subtasks from parent task
python scripts/expand_subtasks.py --task 001 --template tasks/task-001.md

# Creates: task-001-1.md, task-001-2.md, etc.
```

**Workflow Integration:**
1. Create detailed parent markdown with subtasks
2. Run `expand_subtasks.py` to generate individual files
3. Run `task_metadata_manager.py backup --task 001` to preserve
4. Use task-master CLI to load into tasks.json

---

### 2. Task Enhancement & Recovery

#### `enhance_tasks_from_archive.py`
**Purpose:** Enrich clean task files with content from archived versions

**Integration Point:**
- **Input:** Clean task files + archived task files
- **Output:** Enhanced task files with preserved details

```bash
# Enhance tasks from archive
python scripts/enhance_tasks_from_archive.py
```

**Use Case:** After a destructive task-master operation, recover lost details from archived versions.

---

#### `find_lost_tasks.py`
**Purpose:** Find tasks in git history that are not in current files

**Integration Point:**
- **Input:** Git history + current tasks.json
- **Output:** List of lost/missing tasks with details

```bash
# Find lost tasks in last 100 commits
python scripts/find_lost_tasks.py --commits 100 --output lost_tasks.json --verbose
```

**Recovery Workflow:**
1. After noticing data loss, run `find_lost_tasks.py`
2. Identify missing content from git history
3. Use `task_metadata_manager.py restore` if backups exist
4. Or manually recover from git history output

---

#### `regenerate_tasks_from_plan.py`
**Purpose:** Regenerate tasks.json from an enhanced plan markdown document

**Integration Point:**
- **Input:** Enhanced plan markdown (complete_new_task_outline_ENHANCED.md)
- **Output:** Fresh tasks.json with all task details

```bash
# Dry run to preview
python scripts/regenerate_tasks_from_plan.py --dry-run

# Validate the plan
python scripts/regenerate_tasks_from_plan.py --validate

# Regenerate tasks.json
python scripts/regenerate_tasks_from_plan.py
```

**Use Case:** When tasks.json is corrupted or needs complete regeneration from authoritative markdown source.

---

### 3. Task Querying & Analysis

#### `list_tasks.py`, `show_task.py`, `next_task.py`, `search_tasks.py`
**Purpose:** Query tasks without modifying them (safe operations)

```bash
# List pending high-priority tasks
python scripts/list_tasks.py --status pending --priority high --show-subtasks

# Show task details
python scripts/show_task.py 1

# Find next task to work on
python scripts/next_task.py

# Search for specific content
python scripts/search_tasks.py "validation" --show-context
```

**Integration:** Use these for read-only discovery before making changes.

---

#### `task_summary.py`
**Purpose:** Generate comprehensive task statistics

```bash
python scripts/task_summary.py
```

**Output:** Progress percentages, status breakdown, priority distribution.

---

#### `compare_task_files.py`
**Purpose:** Compare tasks across different JSON files

```bash
python scripts/compare_task_files.py
```

**Use Case:** Verify no data was lost after regeneration or migration.

---

### 4. Backup & Compression

#### `compress_progress.py`
**Purpose:** Compress and archive progress tracking files

```bash
# Compress backup directory
python scripts/compress_progress.py --compress --source backups/ --destination compressed/

# Verify compressed archive
python scripts/compress_progress.py --verify --source compressed/progress.tar.xz

# Decompress for restoration
python scripts/compress_progress.py --decompress --source compressed/progress.tar.xz --destination restore/
```

**Integration with Metadata Manager:**
```bash
# Create backup, then compress
python scripts/task_metadata_manager.py backup --all
python scripts/compress_progress.py --compress --source backups/task_markdown_backups --destination backups/compressed/
```

---

### 5. Shared Utilities (`task_scripts/taskmaster_common.py`)

#### Key Classes Available:

| Class | Purpose | Use In |
|-------|---------|--------|
| `SecurityValidator` | Path and input validation | All file operations |
| `BackupManager` | Centralized backup creation | Before destructive ops |
| `FileValidator` | Safe JSON loading with size limits | Parsing tasks.json |
| `TaskValidator` | Task search and validation | Query operations |
| `TaskComparison` | Compare task files | Migration validation |
| `TaskSummary` | Generate statistics | Reporting |

**Usage in Custom Scripts:**
```python
import sys
sys.path.append("task_scripts")
from taskmaster_common import SecurityValidator, BackupManager, FileValidator

# Validate paths before operations
if not SecurityValidator.validate_path_security(filepath):
    raise ValueError("Invalid path")

# Create backup before modifications
backup_mgr = BackupManager()
backup_path = backup_mgr.create_backup("tasks/tasks.json")

# Safely load JSON with size limits
data = FileValidator.load_json_secure("tasks/tasks.json", max_size_mb=50)
```

---

## Integrated Workflows

### Workflow A: Load Markdown Task to tasks.json (Full Preservation)

```bash
# 1. Backup existing state
python scripts/task_metadata_manager.py backup --all

# 2. Convert markdown to JSON structure (extracts effort, complexity)
python scripts/convert_md_to_task_json.py tasks/task-001.md > /tmp/task-001-converted.json

# 3. Review the converted structure
cat /tmp/task-001-converted.json | jq .

# 4. Add parent task via task-master (let AI generate some content)
task-master add-task --prompt="$(cat tasks/task-001.md | head -50)" --priority=high

# 5. Add subtasks from markdown definitions
# (Use expand_subtasks.py output or manual add-subtask calls)

# 6. Embed extended metadata into details field
python scripts/task_metadata_manager.py embed --task 001

# 7. Verify
task-master show 1
```

---

### Workflow B: Recover from Data Loss

```bash
# 1. Identify what was lost
python scripts/find_lost_tasks.py --commits 50 --output lost_tasks.json --verbose

# 2. Check local backups
python scripts/task_metadata_manager.py list-backups --task 001

# 3a. If backup exists, restore
python scripts/task_metadata_manager.py restore --task 001 --index 0

# 3b. If no backup, recover from git history
git show HEAD~5:tasks/task-001.md > /tmp/recovered-task-001.md

# 4. Regenerate from recovered markdown
python scripts/task_metadata_manager.py embed --task 001

# 5. If tasks.json is corrupted, regenerate from plan
python scripts/regenerate_tasks_from_plan.py --validate
python scripts/regenerate_tasks_from_plan.py
```

---

### Workflow C: Enhance Tasks with Research (Safe)

```bash
# 1. Backup first (CRITICAL)
python scripts/task_metadata_manager.py backup --task 001

# 2. Run complexity analysis (creates separate report)
task-master analyze-complexity --id=1 --research

# 3. View complexity report
task-master complexity-report

# 4. Expand with research (CAUTION: can modify details)
task-master expand --id=1 --research --num=8

# 5. Check if anything was lost
python scripts/compare_task_files.py

# 6. Re-embed extended metadata if needed
python scripts/task_metadata_manager.py embed --task 001

# 7. Update subtasks with implementation notes (safe - appends only)
task-master update-subtask --id=1.1 --prompt="Effort: 2-3h, Complexity: 4/10"
```

---

### Workflow D: Generate New Task Structure from Plan

```bash
# 1. Create enhanced plan markdown
# (docs/new_task_plan/complete_new_task_outline_ENHANCED.md)

# 2. Validate the plan
python scripts/regenerate_tasks_from_plan.py --validate

# 3. Dry run to preview
python scripts/regenerate_tasks_from_plan.py --dry-run

# 4. Backup current tasks.json
python scripts/task_metadata_manager.py backup --all

# 5. Regenerate tasks.json
python scripts/regenerate_tasks_from_plan.py

# 6. Generate individual task files
python scripts/split_enhanced_plan.py

# 7. Expand subtasks for each task
for task_id in 001 002 003; do
    python scripts/expand_subtasks.py --task $task_id
done

# 8. Generate metadata coverage report
python scripts/task_metadata_manager.py report
```

---

## Script Enhancement Recommendations

### 1. `convert_md_to_task_json.py`
**Current:** Extracts effort, complexity but doesn't embed in `details`
**Enhancement:** Add option to format extended metadata in HTML comments

```bash
python scripts/convert_md_to_task_json.py tasks/task-001.md --embed-metadata
```

### 2. `expand_subtasks.py`
**Current:** Generates subtask markdown files
**Enhancement:** Also update tasks.json with `add-subtask` calls

```bash
python scripts/expand_subtasks.py --task 001 --update-json
```

### 3. `task_metadata_manager.py`
**Current:** Backup, restore, embed, report
**Enhancement:** Add `sync` command to bidirectional sync markdown ↔ JSON

```bash
python scripts/task_metadata_manager.py sync --task 001 --direction md-to-json
python scripts/task_metadata_manager.py sync --task 001 --direction json-to-md
```

### 4. `compress_progress.py`
**Current:** Compress/decompress backup directories
**Enhancement:** Auto-backup before compression, verify after decompression

```bash
python scripts/compress_progress.py --compress --auto-backup --verify
```

---

## Pre-Operation Checklist

Before running ANY task-master command that modifies data:

- [ ] `python scripts/task_metadata_manager.py backup --all`
- [ ] Verify backup created: `ls -la backups/task_markdown_backups/`
- [ ] Note current task count: `task-master list | head -5`
- [ ] Run operation
- [ ] Verify no data loss: `python scripts/compare_task_files.py`
- [ ] Check metadata coverage: `python scripts/task_metadata_manager.py report`

---

## Command Quick Reference

| Goal | Command |
|------|---------|
| Backup all tasks | `python scripts/task_metadata_manager.py backup --all` |
| Find lost tasks | `python scripts/find_lost_tasks.py --commits 50` |
| Convert MD → JSON | `python scripts/convert_md_to_task_json.py <file>` |
| Expand subtasks | `python scripts/expand_subtasks.py --task <id>` |
| Regenerate from plan | `python scripts/regenerate_tasks_from_plan.py` |
| Compress backups | `python scripts/compress_progress.py --compress ...` |
| Query tasks safely | `python scripts/list_tasks.py --status pending` |
| Search tasks | `python scripts/search_tasks.py "keyword"` |
| Compare files | `python scripts/compare_task_files.py` |
| Metadata report | `python scripts/task_metadata_manager.py report` |

---

## See Also

- [TASK_METADATA_PRESERVATION_GUIDE.md](./TASK_METADATA_PRESERVATION_GUIDE.md) - Detailed metadata preservation
- [scripts/README.md](../scripts/README.md) - Complete script documentation
- [AGENTS.md](../AGENTS.md) - Agent integration guide
