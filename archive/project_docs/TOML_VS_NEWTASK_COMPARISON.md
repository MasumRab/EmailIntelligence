# TOML vs new_task_plan: Ordering and Implementation Comparison

## Overview

This document compares two task representation systems:
1. **TOML** (`tasks/archive/toml_task_plan.md`) - 6 phases, 29 tasks, structured with subtasks
2. **new_task_plan** (`new_task_plan/task_files/`) - 20 tasks, initiative-based, standalone files

---

## Structural Comparison

| Aspect | TOML | new_task_plan |
|--------|------|---------------|
| **Organization** | 6 Phases (1-6) | 4 Initiatives |
| **Task Count** | 29 tasks + 29 subtasks | 20 tasks + 112 subtasks |
| **Numbering** | Phase.Task.Subtask (2.1.1) | Sequential 001-020 |
| **File Format** | Single file (TOML) | 20 Markdown files |
| **Iteration Support** | Explicit [ITERATE] + subtasks | Implicit in subtasks |
| **Dependencies** | `depends_on = ["X.Y"]` | None (no cross-references) |
| **Status** | All `pending` | Mixed (pending, blocked, deferred) |
| **Priority** | None | high/medium/low |

---

## Phase/Initiative Mapping

| TOML Phase | new_task_plan Initiative | Alignment |
|------------|-------------------------|-----------|
| **1: Foundation** | Initiative 1 (001-003) | Partial - TOML has 5 tasks, new_task has 3 |
| **2: Assessment** | Part of Initiative 2 | **MISSING** in new_task - no equivalent |
| **3: Build Framework** | Initiative 2 (004-015) | Matches - both cover tool development |
| **4: Execution** | Initiative 3 (016-017) | Partial - TOML has 5 tasks, new_task has 2 |
| **5: Finalization** | Part of Initiative 2 | **MISSING** in new_task - no equivalent |
| **6: Maintenance** | Initiative 4 (018-020) | Matches - both cover stability |

---

## Task Ordering Comparison

### TOML Order (Sequential by Phase)
```
1.1 → 1.2 → 1.3 → 1.4 → 1.5
      ↓
2.1 → 2.2 → 2.3 → 2.4
      ↓
3.1 → 3.2 → 3.3 → 3.4 → 3.5 → 3.6 → 3.7
      ↓
4.1 → 4.2 → 4.3 → 4.4 → 4.5
      ↓
5.1 → 5.2 → 5.3 → 5.4
      ↓
6.1 → 6.2 → 6.3 → 6.4
```

### new_task_plan Order (Initiative + Sequence)
```
Initiative 1: 001 → 002 → 003
Initiative 2: 004 → 005 → 006 → 007 → 008 → 009 → 010 → 011 → 012 → 013 → 014 → 015
Initiative 3: 016 → 017
Initiative 4: 018 → 019 → 020
```

---

## Key Ordering Differences

| Issue | TOML | new_task_plan |
|-------|------|---------------|
| **Assessment Phase** | 2.1-2.4 with subtasks | **MISSING** - no equivalent tasks |
| **Finalization Phase** | 5.1-5.4 with subtasks | **MISSING** - scattered in 008, 015 |
| **Execution Structure** | 4.1 (load) → 4.2-4.4 (iterate per group) → 4.5 (complex) | 016 (scientific) → 017 (orchestration) - no per-group iteration |
| **Maintenance Structure** | 6.1-6.4 with iteration subtasks | 018-020 (separate tasks) - no iteration notation |

---

## Implementation Detail Comparison

### Example: Branch Identification Task

**TOML (Task 2.1 - Assessment Phase)**
```toml
[[Phase2_Assessment.task]]
id = "2.1"
title = "[ITERATE] Branch Identification & Feature Extraction"
description = "Use git commands to list branches and extract features. ITERATES through all branches."

  [[[Phase2_Assessment.task.subtask]]]
  id = "2.1.1"
  title = "Prepare Branch Enumeration"
  
  [[[Phase2_Assessment.task.subtask]]]
  id = "2.1.2"
  title = "Extract Per-Branch Features"
  
  [[[Phase2_Assessment.task.subtask]]]
  id = "2.1.3"
  title = "Store Feature Vectors"
```

**new_task_plan (Task 007 - Build Initiative)**
```markdown
# Task 007: Develop Feature Branch Identification Tool

## Purpose
Create a Python tool to automatically identify active feature branches...

## Implementation Details
The tool should use GitPython or direct git CLI commands to:
1. List all remote feature branches
2. For each branch, determine common ancestor
3. Analyze git log...
4. Calculate codebase similarity
5. Suggest optimal primary target
6. Output categorized list

## Subtasks
### 007.1: Implement Active Branch Identification
### 007.2: Implement Git History Analysis
### 007.3: Implement Similarity Analysis
### 007.4: Implement Branch Age Analysis
### 007.5: Integrate Backend-to-Src Migration Analysis
### 007.6: Create Structured JSON Output
```

### Key Differences

| Aspect | TOML | new_task_plan |
|--------|------|---------------|
| **Focus** | Phase-based workflow | Feature-based tool |
| **Iteration** | Explicit [ITERATE] marker | Implicit in task description |
| **Steps** | 3 structured subtasks | 6 functional subtasks |
| **Commands** | Reference git commands | Full git/GitPython details |
| **Output** | Feature vectors stored | JSON/CSV file output |
| **Context** | Part of assessment workflow | Standalone tool |

---

## Iteration Pattern Comparison

### TOML Iteration Pattern
```
Task X: [ITERATE] Task Name
├── Subtask X.1: Setup iteration
├── Subtask X.2: Process per item
├── Subtask X.3: Validate per item
└── Subtask X.4: Cleanup/aggregate
```

**Examples in TOML:**
- 2.1, 2.2, 2.3, 2.4 (Assessment - per branch/group)
- 4.2, 4.3, 4.4 (Execution - per branch group)
- 4.5 (Execution - iterative rebase)
- 5.2, 5.3, 5.4 (Finalization - per aligned branch)
- 6.2, 6.3 (Maintenance - per area/file)

### new_task_plan Iteration Pattern
```
Task XXX: Task Name
├── Subtask XXX.1: Implementation step
├── Subtask XXX.2: Implementation step
└── Subtask XXX.N: Implementation step
```

**Examples in new_task_plan:**
- Task 007: 6 subtasks (no iteration marker)
- Task 010: 7 subtasks (no iteration marker)
- Task 013: 7 subtasks (orchestration only)

---

## Missing Tasks in new_task_plan

| TOML Task | Description | new_task_plan Status |
|-----------|-------------|---------------------|
| 1.5 | Configure Branch Protection Rules | Part of 004 |
| 2.1-2.4 | Assessment (all 4 tasks) | **MISSING** |
| 4.1 | Load Branch Checklist | **MISSING** |
| 6.2-6.3 | Maintenance iteration | Part of 018-020 |

---

## Duplicate/Fragmented Tasks in new_task_plan

| Concept | TOML | new_task_plan | Issue |
|---------|------|---------------|-------|
| Error Detection | 3.1 | 005 | Matches |
| Validation Framework | 3.2 | 002, 012 | Split across tasks |
| Branch Backup | 3.3 | 006 | Matches |
| Branch Identification | 3.4 | 007 | Matches |
| Alignment Logic | 3.5 | 010 | Matches |
| Complex Branch Handler | 3.6 | 011 | Matches |
| Orchestration | 3.7 | 013 | Matches |
| CHANGES_SUMMARY | 5.2 | 008 | Matches |
| PR Creation | 5.3 | (in 013) | Fragmented |
| Checklist Update | 5.4 | (in 008) | Fragmented |
| Regression Prevention | 6.1 | 018 | Matches |

---

## Recommendation: Unified Structure

Based on the comparison, the **TOML structure is superior** for:
1. Clear phase-based workflow
2. Explicit iteration notation
3. Proper dependency tracking
4. Self-contained subtask structure

The **new_task_plan format is superior** for:
1. Detailed implementation guidance
2. Git commands and examples
3. Test strategies
4. Human readability during execution

### Proposed Unified Approach

Use TOML for task structure with new_task_plan content merged into subtask descriptions:

```toml
[[Phase4_Execution.task]]
id = "4.2"
title = "[ITERATE] Execute Main Branch Alignments"
description = "For each feature branch targeting main, execute alignment workflow..."

  [[[Phase4_Execution.task.subtask]]]
  id = "4.2.1"
  title = "Process Next Main-Target Branch"
  description = """
  1. Select next branch from main-target group
  2. Create backup: git branch backup/<branch> <branch>
  3. Integrate changes from main:
     - Option A (rebase): git rebase main
     - Option B (merge): git merge main --no-ff
  4. Reference: new_task_plan/task-010.md for core logic
  """
```

---

## Summary

| Criterion | TOML | new_task_plan | Winner |
|-----------|------|---------------|--------|
| Phase Clarity | 6 distinct phases | 4 initiatives | TOML |
| Task Ordering | Logical workflow | Arbitrary | TOML |
| Iteration Support | Explicit [ITERATE] | Implicit | TOML |
| Implementation Details | Minimal | Extensive | new_task_plan |
| Git Commands | References | Full examples | new_task_plan |
| Dependencies | Tracked | None | TOML |
| File Management | Single file | 20 files | TOML |
| Executability | High | Medium | TOML |

**Conclusion:** Adopt TOML as primary structure, enhance subtask descriptions with new_task_plan implementation details.
