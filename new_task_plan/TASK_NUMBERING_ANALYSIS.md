# Task Numbering Analysis for new_task_plan

## Current Situation

### Confusion Sources
1. **Task 75 → Task 021 → Task 002** - Multiple renumberings created confusion
2. **Two Task 002s exist** - Different initiatives sharing same number

---

## Correct Task Numbering (Final)

### Main Tasks (001-026)

| ID | Initiative | Source | Description |
|----|------------|--------|-------------|
| 001 | 1 | Task 7 | Framework Strategy Definition |
| 002 | 1 | Task 9 | **Merge Validation Framework** (NOT clustering!) |
| 003-020 | 2 | Various | Core Alignment Framework |
| 002 | 3 | Task 75 | **Branch Clustering System** (DIFFERENT initiative!) |
| 021-026 | 3-5 | Various | Integration & Maintenance |

### The Dual Task 002 Problem

| ID | Full Name | Source | Subtasks |
|----|-----------|--------|----------|
| 002 | Merge Validation Framework | Task 9 | 9 subtasks (002.1-002.9) |
| 002 | Branch Clustering System | Task 75 | 9 subtasks (002.1-002.9) |

**These are TWO DIFFERENT initiatives with the same task number!**

### Resolution in new_task_plan

For the clustering system (Initiative 3), use:
- **Main file:** `task-002.md` (Clustering System, NOT Validation)
- **Subtask files:** `task-002-1.md` through `task-002-9.md`

For the validation framework (Initiative 1), use:
- **Main file:** `task-002-validation.md` (renamed to avoid confusion)
- **Subtask files:** `task-002-validation-1.md` etc.

---

## Mapping: Original → Current → Target

### Clustering System (Initiative 3)

| Original | Current (tasks/) | Target (new_task_plan/) |
|----------|------------------|-------------------------|
| 75.1 | task_075.1.md | task-002-1.md |
| 75.2 | task_075.2.md | task-002-2.md |
| 75.3 | task_075.3.md | task-002-3.md |
| 75.4 | task_075.4.md | task-002-4.md |
| 75.5 | task_075.5.md | task-002-5.md |
| 75.6 | archived | task-002-6.md |
| 75.7 | archived | task-002-7.md |
| 75.8 | archived | task-002-8.md |
| 75.9 | archived | task-002-9.md |

### Validation Framework (Initiative 1)

| Original | Current | Target |
|----------|---------|--------|
| 9.1 | (needs creation) | task-002-validation-1.md |
| ... | ... | ... |

---

## What Was Created Incorrectly

### Files Created as task-021-*.md (WRONG)
These were created using intermediate numbering that should NOT be used:

```bash
task-021-1.md  # Should be task-002-1.md
task-021-2.md  # Should be task-002-2.md
task-021-3.md  # Should be task-002-3.md
task-021-4.md  # Should be task-002-4.md
task-021-5.md  # Should be task-002-5.md
task-021-6.md  # Should be task-002-6.md
task-021-7.md  # Should be task-002-7.md
task-021-8.md  # Should be task-002-8.md
task-021-9.md  # Should be task-002-9.md
```

### Corrections Needed

1. **Rename files:**
   ```bash
   mv task-021-1.md task-002-1.md
   mv task-021-2.md task-002-2.md
   # ... etc
   ```

2. **Update content references:**
   - Task 021 → Task 002
   - Task 021-4 → Task 002-4
   - Remove references to "intermediate numbering"

3. **Combine handoff files:**
   - task-021-1.md already has combined content ✓
   - task-021-2.md through task-021-9.md need handoffs combined

---

## Correct new_task_plan Structure

```
new_task_plan/
├── task_files/
│   ├── main_tasks/
│   │   ├── task-001.md           # Framework Strategy
│   │   ├── task-002.md           # Branch Clustering System (Initiative 3)
│   │   ├── task-002-validation.md # Merge Validation (Initiative 1) - renamed
│   │   ├── task-003.md           # Pre-Merge Validation
│   │   ├── task-004.md           # Branch Alignment
│   │   ├── task-005.md           # Error Detection
│   │   ├── task-006.md           # Backup & Restore
│   │   ├── task-007.md           # Branch Identification
│   │   ├── task-008.md           # Documentation Automation
│   │   └── task-021.md           # (DOES NOT EXIST - use task-002.md)
│   │
│   └── subtasks/
│       ├── task-002-1.md         # CommitHistoryAnalyzer
│       ├── task-002-2.md         # CodebaseStructureAnalyzer
│       ├── task-002-3.md         # DiffDistanceCalculator
│       ├── task-002-4.md         # BranchClusterer
│       ├── task-002-5.md         # IntegrationTargetAssigner
│       ├── task-002-6.md         # PipelineIntegration
│       ├── task-002-7.md         # VisualizationReporting
│       ├── task-002-8.md         # TestingSuite
│       └── task-002-9.md         # FrameworkIntegration
```

---

## Why Task 021 Should NOT Exist

From `archive/README.md`:
```
- ❌ task-021.md or task-021.1 through task-021.9 (intermediate numbering)
```

Task 021 was an intermediate number during the transition:
- Original: Task 75 (Branch Clustering)
- Intermediate: Task 021
- Final: Task 002 (Clustering System)

Since the final mapping uses Task 002 (not 021), files should be named accordingly.

---

## Action Items

1. [ ] Rename task-021-*.md → task-002-*.md (9 files)
2. [ ] Update internal references in each file (021 → 002)
3. [ ] Combine handoff content for task-002-2.md through task-002-9.md
4. [ ] Verify task-002.md main file is the Clustering System (not Validation)
5. [ ] Create task-002-validation.md for the Validation Framework

---

## Reference Documents

- `task_mapping.md` - Official mapping from old to new IDs
- `MIGRATION_FIX_SUMMARY.md` - Documents the dual Task 002 issue
- `CLEAN_TASK_INDEX.md` - Shows both Task 002s with clarification
- `archive/README.md` - Lists what NOT to create
