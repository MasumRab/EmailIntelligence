# Task Progress Logging Guide

## Overview

This guide explains how to log task progress, parameters, decisions, and outcomes in the branch alignment workflow.

## Purpose

- **Track parameters**: What inputs/configs were used
- **Record decisions**: What choices were made and why
- **Capture outcomes**: Results, success/failure, metrics
- **Enable speedups**: Document what worked/didn't work for future runs

## Logging Approach

We use a **hybrid approach**:
- **Inline Markdown**: Brief notes in task files
- **External JSON**: Structured data in `task_data/findings/`

## Directory Structure

```
task_data/findings/
├── phase1_foundational/     # Foundation tasks (001-003)
├── phase2_assessment/        # Assessment tasks (007-009)
├── phase3_build/            # Build tasks (004-006, 010-015)
├── phase4_execution/        # Execution tasks (016-017)
├── phase5_finalization/     # Finalization tasks (014, 015)
└── phase6_maintenance/      # Maintenance tasks (018-020)
```

## Logging Subtask Template

Add this to each task file:

```markdown
### X.X.N: Log Findings

**Purpose:** Record parameters, decisions, and outcomes for future improvements.

**Capture:**
- Parameters: [What inputs/configs were used?]
- Decision: [What choice was made and why?]
- Outcome: [What was the result?]

**Log to:** `task_data/findings/{phase}/{file}.json`

**Example:**
```json
{
  "task_id": "X.X.N",
  "timestamp": "2026-01-04T12:00:00Z",
  "parameters": {...},
  "decision": "...",
  "outcome": {...}
}
```
```

## JSON Schema

```json
{
  "task_id": "string (e.g., '3.1.4')",
  "timestamp": "ISO 8601 datetime",
  "phase": "string (e.g., 'phase3_build')",
  "parameters": {
    "git_command": "string",
    "branch_count": "integer",
    "threshold": "number"
  },
  "decision": {
    "choice": "string",
    "rationale": "string",
    "alternatives_considered": ["array"]
  },
  "outcome": {
    "success": "boolean",
    "duration_ms": "integer",
    "metrics": {}
  },
  "findings": {
    "pattern": "string or null",
    "recommendation": "string or null",
    "next_steps": ["array or null"]
  }
}
```

## Task-Phase Mapping

| Task | Phase | Log File |
|------|-------|----------|
| 001-003 | phase1_foundational | git_tooling.json, validation_command.json, linting_tools.json |
| 004-006 | phase3_build | error_detection.json, validation_framework.json, backup_mechanism.json |
| 007-009 | phase2_assessment | branch_features.json, target_assignments.json, clustering_results.json |
| 010-015 | phase3_build | alignment_logic.json, complex_handler.json, workflow_orchestration.json |
| 016-017 | phase4_execution | main_alignments.json, scientific_alignments.json |
| 018-020 | phase6_maintenance | regression_prevention.json, conflict_scan.json, dependency_reviews.json |

## Querying Findings

Use `scripts/query_findings.py`:

```bash
# Query all findings for a phase
python scripts/query_findings.py --phase phase2_assessment

# Query specific task
python scripts/query_findings.py --task 3.1.4

# Query by date range
python scripts/query_findings.py --from 2026-01-01 --to 2026-01-31
```

## Best Practices

1. **Log at checkpoints**: After each subtask completion
2. **Be specific**: Include actual values, not just descriptions
3. **Document failures**: What went wrong and how it was fixed
4. **Note patterns**: Repeated issues or successful approaches
5. **Update timestamps**: Always include when the entry was made

## Examples

### Non-Iterative Task (Task 001)

```markdown
### 001.3: Log Git Tooling Verification Findings

**Parameters:** git version 2.34.1, user.name set, user.email set
**Decision:** All core config present, only lfs filters missing
**Outcome:** Success, missing_items: ["filter.lfs"]
**Log to:** `task_data/findings/phase1_foundational/git_tooling.json`
```

### Iterative Task (Task 007)

```markdown
### 007.4: Log Branch Feature Extraction Outcome

**Parameters:** Branch: feature/test-branch, git_command: merge-base, features: 12
**Decision:** Used merge-base for distance calculation
**Outcome:** Success, duration_ms: 450, pattern: merge-base slower on large repos
**Log to:** `task_data/findings/phase2_assessment/branch_features.json`
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| JSON file doesn't exist | Create it with empty array `[]` |
| Schema validation error | Check against schema in this guide |
| Query returns nothing | Verify file path and task_id format |
| Timestamp format error | Use ISO 8601: `2026-01-04T12:00:00Z` |

---

**Created:** 2026-01-04  
**For:** Branch Alignment Task System  
**Maintainer:** Task Master AI