# Comprehensive Plan: new_task_plan Logging System & Improvements

## Document Overview

| Aspect | Detail |
|--------|--------|
| **Purpose** | Introduce task progress logging + fix identified issues |
| **Scope** | new_task_plan/task_files/ + related documentation |
| **Approach** | Hybrid logging (Markdown inline + JSON external) |
| **Based On** | TOML task plan analysis, new_task_plan comparison |
| **Created** | 2026-01-04 |
| **Status** | Draft - Pending Review |

---

## 1. Executive Summary

This plan introduces a **task progress logging system** to track parameters, decisions, and outcomes as tasks progress. It also addresses **structural inconsistencies** identified between TOML and new_task_plan task formats.

### Key Goals

1. **Capture findings** at each task checkpoint for future improvements
2. **Enable speedups** by documenting what worked/didn't work
3. **Align structures** between TOML (6-phase) and new_task_plan (4-initiative)
4. **Preserve context** for multi-session work

### Expected Outcome

A unified task system where each task file contains inline logging references linked to structured external JSON logs in `task_data/findings/`.

---

## 2. Current State Analysis

### 2.1 new_task_plan Structure

| Component | Status | Details |
|-----------|--------|---------|
| **Task Files** | 20 files (task-001.md to task-020.md) | Located in `new_task_plan/task_files/` |
| **Initiatives** | 4 groups | Foundation, Build, Execution, Maintenance |
| **Iteration Support** | Implicit | Subtasks, no explicit `[ITERATE]` markers |
| **Logging** | None | No findings capture system |
| **Broken References** | 6 references | `backlog/` links, `tasks.json` mentions |

### 2.2 Identified Issues

| Issue | Location | Impact |
|-------|----------|--------|
| Missing Assessment Phase | new_task_plan | No equivalent for TOML 2.1-2.4 |
| Missing Finalization Phase | new_task_plan | No equivalent for TOML 5.1-5.4 |
| Broken `backlog/` reference | task-002.md | Non-existent file |
| `tasks.json` references | Multiple docs | Deprecated system |
| Inconsistent structure | All files | TOML has subtasks, new_task doesn't |

### 2.3 Task Distribution

| TOML Phase | TOML Tasks | new_task_plan Tasks | Gap |
|------------|------------|---------------------|-----|
| 1: Foundation | 1.1-1.5 | 001-003 | +2 tasks |
| 2: Assessment | 2.1-2.4 | None | **MISSING** |
| 3: Build | 3.1-3.7 | 004-015 | Partial |
| 4: Execution | 4.1-4.5 | 016-017 | **MISSING** |
| 5: Finalization | 5.1-5.4 | None | **MISSING** |
| 6: Maintenance | 6.1-6.4 | 018-020 | Partial |

---

## 3. Logging System Design

### 3.1 Hybrid Approach

**Inline Markdown** (in task files):
```markdown
### 3.1.4: Log Findings

**Parameters:** Git command used, branch count, feature types
**Decision:** Used merge-base over diff for performance
**Outcome:** 450ms per branch, acceptable for N<50 branches
**Log to:** `task_data/findings/phase3_build/error_detection.json`
```

**External JSON** (in `task_data/findings/`):
```json
{
  "task_id": "3.1.4",
  "timestamp": "2026-01-04T12:00:00Z",
  "parameters": {"git_cmd": "merge-base", "branches": 23},
  "decision": "Used merge-base over diff for performance",
  "outcome": {"duration_ms": 450, "status": "acceptable"}
}
```

### 3.2 Directory Structure

```
.taskmaster/
├── task_data/findings/
│   ├── phase1_foundational/
│   │   ├── git_tooling.json
│   │   ├── validation_command.json
│   │   ├── linting_tools.json
│   │   ├── primary_backups.json
│   │   └── branch_protection.json
│   ├── phase2_assessment/
│   │   ├── branch_features.json
│   │   ├── target_assignments.json
│   │   ├── clustering_results.json
│   │   └── priority_scores.json
│   ├── phase3_build/
│   │   ├── error_detection.json
│   │   ├── validation_framework.json
│   │   ├── backup_mechanism.json
│   │   ├── branch_id_tool.json
│   │   ├── alignment_logic.json
│   │   ├── complex_handler.json
│   │   └── workflow_orchestration.json
│   ├── phase4_execution/
│   │   ├── checklist_loading.json
│   │   ├── main_alignments.json
│   │   ├── scientific_alignments.json
│   │   ├── orchestration_alignments.json
│   │   └── complex_branches.json
│   ├── phase5_finalization/
│   │   ├── branch_collection.json
│   │   ├── changes_summaries.json
│   │   ├── pr_outcomes.json
│   │   └── checklist_updates.json
│   └── phase6_maintenance/
│       ├── regression_prevention.json
│       ├── conflict_scan.json
│       ├── dependency_reviews.json
│       └── documentation_updates.json
```

### 3.3 Logging Schema

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | e.g., "3.1.4" |
| `timestamp` | ISO 8601 | When entry was created |
| `phase` | string | e.g., "phase3_build" |
| `parameters` | object | Inputs, configs, thresholds |
| `decision` | object | Choice made + rationale |
| `outcome` | object | Result, metrics, success/failure |
| `findings` | object | Patterns, recommendations |

---

## 4. Changes to new_task_plan Files

### 4.1 Tasks to Modify

| Task ID | File | Type | Logging Subtasks |
|---------|------|------|------------------|
| 001 | task-001.md | Non-iterative | 1 logging subtask |
| 002 | task-002.md | Non-iterative | 1 logging subtask |
| 003 | task-003.md | Non-iterative | 1 logging subtask |
| 004 | task-004.md | Non-iterative | 1 logging subtask |
| 005 | task-005.md | Non-iterative | 1 logging subtask |
| 006 | task-006.md | Non-iterative | 1 logging subtask |
| 007 | task-007.md | **Iterative** | 2 logging subtasks |
| 008 | task-008.md | **Iterative** | 2 logging subtasks |
| 009 | task-009.md | **Iterative** | 2 logging subtasks |
| 010 | task-010.md | **Iterative** | 2 logging subtasks |
| 011 | task-011.md | **Iterative** | 2 logging subtasks |
| 012 | task-012.md | **Iterative** | 2 logging subtasks |
| 013 | task-013.md | **Iterative** | 2 logging subtasks |
| 014 | task-014.md | Non-iterative | 1 logging subtask |
| 015 | task-015.md | **Iterative** | 2 logging subtasks |
| 016 | task-016.md | **Iterative** | 2 logging subtasks |
| 017 | task-017.md | **Iterative** | 2 logging subtasks |
| 018 | task-018.md | Non-iterative | 1 logging subtask |
| 019 | task-019.md | **Iterative** | 2 logging subtasks |
| 020 | task-020.md | **Iterative** | 2 logging subtasks |

**Total:** 20 tasks modified, ~35 new logging subtasks added

### 4.2 Logging Subtask Template

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
  "parameters": {...},
  "decision": "...",
  "outcome": {...}
}
```
```

### 4.3 Fixes Required

| Issue | File | Fix |
|-------|------|-----|
| Broken `backlog/` link | task-002.md | Remove reference |
| Deprecated `tasks.json` | CLEAN_TASK_INDEX.md | Remove mentions |
| Missing Assessment Phase | new_task_plan | Add tasks 021-024 (future) |
| Missing Finalization Phase | new_task_plan | Add tasks 025-028 (future) |

---

## 5. Other Fixes Required

### 5.1 Documentation Updates

| File | Issue | Fix |
|------|-------|-----|
| `new_task_plan/CLEAN_TASK_INDEX.md` | `tasks.json` references | Remove 10+ mentions |
| `new_task_plan/task_mapping.md` | Old task references | Archive or update |
| `new_task_plan/complete_new_task_outline_ENHANCED.md` | `tasks.json` references | Remove references |

### 5.2 Directory Cleanup

| Action | Location |
|--------|----------|
| Archive `new_task_plan/old/` | → `tasks/archive/new_task_plan_old/` |
| Remove `backlog/` reference | From task-002.md |
| Delete `tasks_data_formatted_tasks.md` | Already in archive |

### 5.3 Structural Alignments

| Change | Purpose |
|--------|---------|
| Add `[ITERATE]` markers | Match TOML structure |
| Add "Depends on" field | Track dependencies |
| Add "Status" consistency | All tasks have clear status |

---

## 6. Implementation Steps

### Phase 1: Infrastructure Setup (Day 1)

| Step | Action | Output |
|------|--------|--------|
| 1.1 | Create `task_data/findings/` directories | 6 phase directories |
| 1.2 | Create `LOGGING_GUIDE.md` | Documentation file |
| 1.3 | Create `scripts/query_findings.py` | Query utility |
| 1.4 | Create `.gitkeep` files in findings dirs | Enable git tracking |

### Phase 2: Fix Broken References (Day 2)

| Step | Action | Output |
|------|--------|--------|
| 2.1 | Remove `backlog/` from task-002.md | Clean reference |
| 2.2 | Remove `tasks.json` from CLEAN_TASK_INDEX.md | Updated index |
| 2.3 | Archive old formatted task files | Cleanup new_task_plan |

### Phase 3: Add Logging to Tasks (Days 3-5)

| Step | Action | Tasks Modified |
|------|--------|----------------|
| 3.1 | Add logging subtasks to Foundation tasks | 001-003 |
| 3.2 | Add logging subtasks to Build tasks | 004-015 |
| 3.3 | Add logging subtasks to Execution tasks | 016-017 |
| 3.4 | Add logging subtasks to Maintenance tasks | 018-020 |

### Phase 4: Documentation Updates (Day 6)

| Step | Action | Output |
|------|--------|--------|
| 4.1 | Update CLEAN_TASK_INDEX.md | Remove deprecated refs |
| 4.2 | Update AGENTS.md | Document logging commands |
| 4.3 | Update CLAUDE.md | Include logging workflow |

### Phase 5: Testing & Validation (Day 7)

| Step | Action | Output |
|------|--------|--------|
| 5.1 | Test query_findings.py script | Verified queries |
| 5.2 | Validate all JSON logs | Schema compliance |
| 5.3 | Review task file changes | Consistency check |

---

## 7. Timeline Summary

| Phase | Day | Effort |
|-------|-----|--------|
| Infrastructure Setup | 1 | 4 hours |
| Fix Broken References | 2 | 4 hours |
| Add Logging (Foundation) | 3 | 4 hours |
| Add Logging (Build) | 4 | 4 hours |
| Add Logging (Execution + Maintenance) | 5 | 4 hours |
| Documentation Updates | 6 | 4 hours |
| Testing & Validation | 7 | 4 hours |

**Total Effort:** ~2 days (can be done incrementally)

---

## 8. Files to Create

| File | Location | Purpose |
|------|----------|---------|
| `LOGGING_GUIDE.md` | `new_task_plan/` | Logging documentation |
| `query_findings.py` | `scripts/` | Query utility script |
| 6 phase directories | `task_data/findings/` | Log file storage |

**Total New Files:** 1 guide + 1 script + 6 directories + 29 JSON templates

---

## 9. Files to Modify

| File | Changes |
|------|---------|
| `new_task_plan/task_files/task-001.md` through task-020.md | Add logging subtasks |
| `new_task_plan/CLEAN_TASK_INDEX.md` | Remove `tasks.json` refs |
| `new_task_plan/task_files/task-002.md` | Remove `backlog/` ref |

**Total Modified Files:** 21 files

---

## 10. Files to Archive

| File | New Location |
|------|--------------|
| `new_task_plan/old/` | `tasks/archive/new_task_plan_old/` |

---

## 11. Tradeoffs Summary

| Decision | Option Chosen | Rationale |
|----------|---------------|-----------|
| Logging Format | Hybrid (Markdown + JSON) | Human + machine access |
| Scope | All 20 tasks | Complete tracking |
| Query Method | grep + Python script | Flexible access |
| Iteration Markers | Add `[ITERATE]` | Match TOML |

---

## 12. Success Criteria

| Criterion | Measure |
|-----------|---------|
| All 20 tasks have logging subtasks | 20 tasks × 1-2 logging subtasks |
| All log files accessible | `task_data/findings/` populated |
| Queries work | `query_findings.py` returns results |
| Broken references fixed | 0 `backlog/`, `tasks.json` refs |
| Documentation updated | AGENTS.md, CLAUDE.md updated |

---

## 13. Next Steps

1. **Review this plan** - Confirm scope and approach
2. **Approve implementation** - Begin Phase 1
3. **Execute phases** - Follow timeline in Section 6
4. **Validate results** - Use success criteria in Section 12

---

## Appendix A: Complete Task-Logging Mapping

| Task | File | Phase | Log File | Subtasks |
|------|------|-------|----------|----------|
| 001 | task-001.md | Foundation | git_tooling.json | 1 |
| 002 | task-002.md | Foundation | validation_command.json | 1 |
| 003 | task-003.md | Foundation | linting_tools.json | 1 |
| 004 | task-004.md | Build | error_detection.json | 1 |
| 005 | task-005.md | Build | validation_framework.json | 1 |
| 006 | task-006.md | Build | backup_mechanism.json | 1 |
| 007 | task-007.md | Assessment | branch_features.json | 2 |
| 008 | task-008.md | Assessment | target_assignments.json | 2 |
| 009 | task-009.md | Assessment | clustering_results.json | 2 |
| 010 | task-010.md | Execution | priority_scores.json | 2 |
| 011 | task-011.md | Execution | main_alignments.json | 2 |
| 012 | task-012.md | Execution | scientific_alignments.json | 2 |
| 013 | task-013.md | Execution | orchestration_alignments.json | 2 |
| 014 | task-014.md | Finalization | changes_summaries.json | 1 |
| 015 | task-015.md | Finalization | pr_outcomes.json | 2 |
| 016 | task-016.md | Finalization | checklist_updates.json | 2 |
| 017 | task-017.md | Maintenance | regression_prevention.json | 2 |
| 018 | task-018.md | Maintenance | conflict_scan.json | 1 |
| 019 | task-019.md | Maintenance | dependency_reviews.json | 2 |
| 020 | task-020.md | Maintenance | documentation_updates.json | 2 |

---

## Appendix B: JSON Log Schema Reference

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

---

## Appendix C: Logging Subtask Examples by Task Type

### Non-Iterative Task Example (Task 001)

```markdown
### 001.3: Log Git Tooling Verification Findings

**Purpose:** Record git environment configuration for future reproducibility.

**Capture:**
- Parameters: git version, user.name, user.email, config completeness
- Decision: [Which git config items were set/missing?]
- Outcome: [Was environment verified successfully?]

**Log to:** `task_data/findings/phase1_foundational/git_tooling.json`

**Example:**
```json
{
  "task_id": "001.3",
  "parameters": {
    "git_version": "2.34.1",
    "user_name_set": true,
    "user_email_set": true,
    "config_completeness": 0.95
  },
  "decision": "All core config present, only lfs filters missing",
  "outcome": {
    "success": true,
    "missing_items": ["filter.lfs"]
  }
}
```
```

### Iterative Task Example (Task 007)

```markdown
### 007.1: Log Branch Feature Extraction Parameters

**Purpose:** Record iteration parameters for batch processing.

**Capture:**
- Parameters: Branch patterns, git commands, feature types
- Decision: [Which features to extract?]
- Outcome: [How many branches processed?]

**Log to:** `task_data/findings/phase2_assessment/branch_features.json`
```

```markdown
### 007.N: Log Branch Feature Extraction Outcome

**Purpose:** Record per-iteration results and patterns.

**Capture:**
- Parameters: Branch name, feature extraction time
- Decision: [Any adjustments made during iteration?]
- Outcome: [Success/failure, metrics, patterns observed]

**Log to:** `task_data/findings/phase2_assessment/branch_features.json`

**Example:**
```json
{
  "task_id": "007.4",
  "iteration_item": "feature/test-branch",
  "parameters": {
    "git_command": "git merge-base main origin/feature/test-branch",
    "features": ["commit_date", "merge_base", "file_changes"]
  },
  "decision": "Used merge-base for distance calculation",
  "outcome": {
    "success": true,
    "duration_ms": 450,
    "features_collected": 12
  },
  "findings": {
    "pattern": "merge-base slower on repos with 50k+ commits",
    "recommendation": "Consider caching merge-base results"
  }
}
```
```

---

**End of Plan Document**

This plan is ready for review and implementation approval.
