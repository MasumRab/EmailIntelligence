# Complete Task Workflow Guide

**Single source of truth for Task Master workflows in this project.**

---

## Document Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DOCUMENTATION HIERARCHY                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  THIS FILE (COMPLETE_TASK_WORKFLOW.md)                              │
│  └── Master workflow reference                                       │
│                                                                      │
│  AGENTS.md / CLAUDE.md                                              │
│  └── Agent-specific command reference                                │
│                                                                      │
│  TASK_ENHANCEMENT_PROCEDURES.md                                      │
│  └── Field-by-field enhancement guide                                │
│                                                                      │
│  TASK_METADATA_PRESERVATION_GUIDE.md                                 │
│  └── Technical details on metadata preservation                      │
│                                                                      │
│  scripts/README.md                                                   │
│  └── Script usage reference                                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### Document Types & Data Flow

```
┌──────────────┐     parse-prd      ┌──────────────┐     generate      ┌──────────────┐
│     PRD      │ ──────────────────▶│  tasks.json  │ ─────────────────▶│   Task MD    │
│ (High-level) │                    │  (Database)  │                    │  (Detailed)  │
└──────────────┘                    └──────────────┘                    └──────────────┘
     │                                     │                                   │
     │                                     │                                   │
     ▼                                     ▼                                   ▼
 Requirements                         CLI/MCP                           Implementation
 Goals, Scope                        Operations                         Specs, Details
 User Stories                        Status Updates                     Success Criteria
                                     Dependencies                       Test Strategy
```

| Document | Purpose | Location | Created By |
|----------|---------|----------|------------|
| **PRD** | High-level requirements, goals, scope | `.taskmaster/docs/*.txt` | Human/Research |
| **tasks.json** | Task database (CLI-managed) | `.taskmaster/tasks/tasks.json` | `parse-prd`, CLI |
| **Task MD** | Detailed implementation specs | `.taskmaster/tasks/task-*.md` | `generate`, Manual |

### Workflow Direction

```
✅ CORRECT: PRD → tasks.json → Task MD
❌ WRONG:   Task MD → tasks.json (loses structure)
```

---

## Workflow 1: New Initiative (Start from PRD)

### When to Use
- Starting a new feature, project, or initiative
- Major new functionality that needs planning

### Steps

```bash
# 1. Create PRD document
cat > .taskmaster/docs/my-feature-prd.md << 'EOF'
# Feature Name PRD

## Overview
Brief description of what this feature does.

## Goals
- Goal 1
- Goal 2

## Requirements
### Functional Requirements
- FR1: Description
- FR2: Description

### Non-Functional Requirements
- NFR1: Performance target
- NFR2: Security requirement

## Success Criteria
- SC1: Measurable outcome
- SC2: Verification method
EOF

# 2. Parse PRD to generate tasks
task-master parse-prd .taskmaster/docs/my-feature-prd.md --research

# 3. Analyze complexity
task-master analyze-complexity --research

# 4. Expand complex tasks into subtasks
task-master expand --all --research

# 5. Generate task markdown files
task-master generate

# 6. Enhance task markdowns with additional details
# (See Workflow 3)
```

### Adding to Existing Tasks

```bash
# Use --append to add new tasks without overwriting
task-master parse-prd .taskmaster/docs/new-feature-prd.md --append --research
```

---

## Workflow 2: Daily Task Execution

### Starting Work

```bash
# 1. Find next task
task-master next

# 2. View task details
task-master show <id>

# 3. Mark as in-progress
task-master set-status --id=<id> --status=in-progress
```

### During Work

```bash
# Log implementation notes
task-master update-subtask --id=<id> --prompt="Completed X, discovered Y needs attention"

# Research for guidance
task-master research "How should I handle edge case X?" --id=<id> --save-to=<id>
```

### Completing Work

```bash
# 1. Mark task complete
task-master set-status --id=<id> --status=done

# 2. Get next task
task-master next
```

---

## Workflow 3: Task Enhancement (Add Details to Existing Tasks)

### When to Use
- Adding Success Criteria, Test Strategy, Effort estimates
- Enriching task details after initial generation
- Recovering from data loss

### Pre-Enhancement Backup (CRITICAL)

```bash
# ALWAYS backup before any enhancement work
python scripts/task_metadata_manager.py backup --all
```

### Enhancement Methods by Field

| Field | Method | Command |
|-------|--------|---------|
| Title/Description | CLI | `task-master update-task <id> <prompt>` |
| Details | CLI | `task-master update-task <id> <prompt>` |
| Status | CLI | `task-master set-status --id=<id> --status=<status>` |
| Dependencies | CLI | `task-master add-dependency --id=<id> --depends-on=<id>` |
| Complexity | CLI | `task-master analyze-complexity --id=<id> --research` |
| Success Criteria | Research + Embed | See below |
| Test Strategy | Research + Embed | See below |
| Effort Estimate | Research + Embed | See below |
| Owner | Manual + Embed | Edit markdown directly |

### Using Research to Generate Content

```bash
# Generate Success Criteria
task-master research "Generate measurable success criteria for this task. Include P0 (must have), P1 (should have), P2 (nice to have). Each criterion should be specific, measurable, and verifiable." --id=<id> --save-file

# Generate Test Strategy
task-master research "Generate a comprehensive test strategy. Include unit tests with inputs/outputs, integration tests, and manual validation steps. Specify coverage targets." --id=<id> --save-file

# Generate Effort Estimate
task-master research "Estimate effort in hours. Consider complexity, dependencies, testing, documentation. Break down by phase if applicable." --id=<id> --save-file

# View research output
ls .taskmaster/docs/research/
cat .taskmaster/docs/research/<latest-file>.md
```

### Adding Extended Metadata to Task MD

1. **Edit the task markdown file** (`.taskmaster/tasks/task-<id>.md`)
2. **Add the EXTENDED_METADATA block** at the end of the Details section:

```markdown
## Details

Implementation steps here...

<!-- EXTENDED_METADATA
effort: 2-3h
complexity: 7/10
owner: developer-name
initiative: Core Framework
successCriteria:
  - Criterion 1 with specific measurable outcome
  - Criterion 2 with validation method
  - Criterion 3 with acceptance threshold
testStrategy: |
  Unit: Component tests for each function
  Integration: End-to-end workflow validation
  Validation: Manual review and sign-off
END_EXTENDED_METADATA -->
```

3. **Embed metadata to tasks.json**:

```bash
python scripts/task_metadata_manager.py embed --task <id>
```

4. **Verify**:

```bash
python scripts/task_metadata_manager.py report
```

---

## Workflow 4: Recovery from Data Loss

### When Task Master Stripped Your Metadata

```bash
# 1. List available backups
python scripts/task_metadata_manager.py list-backups --task <id>

# 2. Restore from most recent backup (index 0)
python scripts/task_metadata_manager.py restore --task <id> --index 0

# 3. Re-embed metadata to tasks.json
python scripts/task_metadata_manager.py embed --task <id>
```

### When No Backup Exists

```bash
# Try to recover from archive
python scripts/enhance_tasks_from_archive.py

# Or recover from git history
python scripts/find_lost_tasks.py --commits 100 --output lost_tasks.json
```

---

## Field Reference

### Fields Fully Supported by Task Master CLI

| Field | Create | Update | Notes |
|-------|--------|--------|-------|
| id | `parse-prd` | Auto | Never manually edit |
| title | `parse-prd`, `add-task` | `update-task` | |
| description | `parse-prd`, `add-task` | `update-task` | |
| details | `parse-prd` | `update-task`, `update-subtask` | Extension point for metadata |
| status | Auto | `set-status` | pending/in-progress/done/review/deferred/cancelled/blocked |
| priority | `parse-prd` | `update-task` | high/medium/low |
| dependencies | `parse-prd` | `add-dependency`, `remove-dependency` | |
| subtasks | `expand` | `add-subtask` | |

### Fields Requiring Research + Embed

| Field | Generate | Embed | Preserve |
|-------|----------|-------|----------|
| successCriteria | `research "Generate success criteria..."` | Add to EXTENDED_METADATA | `backup --all` before CLI ops |
| testStrategy | `research "Generate test strategy..."` | Add to EXTENDED_METADATA | `backup --all` before CLI ops |
| effort | `research "Estimate effort..."` | Add to EXTENDED_METADATA | `backup --all` before CLI ops |

### Fields Manual Only

| Field | Edit | Notes |
|-------|------|-------|
| owner | Edit task MD directly | Add to EXTENDED_METADATA |
| initiative | Edit task MD directly | Add to EXTENDED_METADATA |
| blocks | Edit task MD directly | Add to EXTENDED_METADATA |

---

## Best Practices

### Before Any CLI Operation

```bash
# ALWAYS backup first
python scripts/task_metadata_manager.py backup --all
```

### Task Markdown Structure

```markdown
# Task ID: XXX Task Title

**Status:** pending
**Priority:** high
**Effort:** X-Y hours
**Complexity:** N/10
**Dependencies:** Task X, Task Y
**Owner:** developer-name

---

## Purpose

Brief description of what this task accomplishes.

---

## Details

Implementation steps and technical details.

<!-- EXTENDED_METADATA
effort: X-Yh
complexity: N/10
owner: developer-name
successCriteria:
  - Criterion 1
  - Criterion 2
testStrategy: |
  Unit: ...
  Integration: ...
END_EXTENDED_METADATA -->

---

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2

---

## Test Strategy

### Unit Tests
- Test 1

### Integration Tests
- Test 2

---

## Progress Log

### YYYY-MM-DD
- Update notes
```

### PRD Structure

```markdown
# Feature/Initiative Name PRD

## Overview
Brief description.

## Goals
- Goal 1
- Goal 2

## Requirements

### Functional Requirements
- FR1: Description
- FR2: Description

### Non-Functional Requirements
- NFR1: Description

## User Stories
- As a [user], I want [feature] so that [benefit]

## Success Criteria
- SC1: Measurable outcome
- SC2: Verification method

## Out of Scope
- Item 1 (explicitly excluded)

## Dependencies
- External dependency 1

## Timeline
- Phase 1: Description (Week X)
- Phase 2: Description (Week Y)
```

---

## Quick Command Reference

### Task Master CLI

```bash
# Initialization
task-master init
task-master models --setup
task-master parse-prd <file> [--append] [--research]

# Task Management
task-master list
task-master next
task-master show <id>
task-master set-status --id=<id> --status=<status>
task-master add-task --prompt="..." [--research]
task-master update-task <id> <prompt>
task-master update-subtask --id=<id> --prompt="..."
task-master remove-task --id=<id>

# Analysis
task-master analyze-complexity [--id=<ids>] [--research]
task-master complexity-report
task-master research "<prompt>" --id=<id> [--save-file] [--save-to=<id>]

# Expansion
task-master expand --id=<id> [--research] [--force]
task-master expand --all [--research]

# Dependencies
task-master add-dependency --id=<id> --depends-on=<id>
task-master remove-dependency --id=<id> --depends-on=<id>
task-master validate-dependencies
task-master fix-dependencies

# Generation
task-master generate
```

### Metadata Manager

```bash
# Backup
python scripts/task_metadata_manager.py backup --all
python scripts/task_metadata_manager.py backup --task <id>

# Restore
python scripts/task_metadata_manager.py list-backups --task <id>
python scripts/task_metadata_manager.py restore --task <id> --index 0

# Embed
python scripts/task_metadata_manager.py embed --task <id>

# Report
python scripts/task_metadata_manager.py report
```

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [TASK_ENHANCEMENT_PROCEDURES.md](TASK_ENHANCEMENT_PROCEDURES.md) | Field-by-field enhancement details |
| [TASK_METADATA_PRESERVATION_GUIDE.md](TASK_METADATA_PRESERVATION_GUIDE.md) | Technical metadata preservation |
| [scripts/README.md](../scripts/README.md) | Script usage reference |
| [AGENTS.md](../AGENTS.md) | Agent integration guide |
