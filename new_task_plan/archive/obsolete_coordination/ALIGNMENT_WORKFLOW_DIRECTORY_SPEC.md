# Alignment Workflow Directory Specification

**Purpose:** Define a clean, minimal directory structure containing only files essential for complete branch alignment workflow execution  
**Scope:** Complete file inventory, organization strategy, and creation order  
**Goal:** Eliminate clutter, enable focus, support parallel team execution  
**Version:** 1.0  
**Created:** January 6, 2026  

---

## Executive Summary

This document specifies the creation of a pristine `new_task_plan/` directory containing only files necessary for executing the complete branch alignment workflow. All extraneous, deprecated, and redundant files are removed or archived.

**Key Principles:**
1. **Minimalism:** Only files that directly support workflow execution
2. **Clarity:** Every file has a clear, documented purpose
3. **Isolation:** Teams can work independently without navigating clutter
4. **Completeness:** Everything needed for execution is present
5. **Maintainability:** Easy to update and extend

---

## Current State: Files to Remove

### Root Level Files to Archive or Delete

| File | Action | Reason |
|------|--------|--------|
| `CLEAN_TASK_INDEX.md` | KEEP - reference/ | Task status matrix |
| `complete_new_task_outline_ENHANCED.md` | ARCHIVE - reference/ | Original specs (reference only) |
| `COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md` | ARCHIVE - reference/ | Historical reference |
| `INDEX_AND_GETTING_STARTED.md` | ARCHIVE - reference/ | Redundant with new navigation |
| `INTEGRATION_EXECUTION_CHECKLIST.md` | ARCHIVE - reference/ | Historical reference |
| `LOGGING_GUIDE.md` | KEEP - guidance/ | Active guidance |
| `LOGGING_SYSTEM_PLAN.md` | KEEP - guidance/ | Active guidance |
| `MIGRATION_FIX_SUMMARY.md` | ARCHIVE - reference/ | Historical reference |
| `NEW_TASK_FOLDER_INDEX.md` | DELETE | Redundant with NAVIGATION_GUIDE.md |
| `NEW_TASK_FOLDER_SYNC_PLAN.md` | DELETE | Historical, superseded |
| `README.md` | REPLACE | New comprehensive version |
| `RENUMBERING_021_TO_002_STATUS.md` | ARCHIVE - reference/ | Historical reference |
| `RENUMBERING_DECISION_TASK_021.md` | ARCHIVE - reference/ | Historical reference |
| `SYNC_COMPLETION_SUMMARY.md` | DELETE | Historical, superseded |
| `TASK_DEPENDENCY_VISUAL_MAP.md` | KEEP - reference/ | Active reference |
| `task_mapping.md` | KEEP - reference/ | Active reference |
| `WEEK_1_FINAL_SUMMARY.md` | ARCHIVE - archive/v1_planning/ | Historical reference |

### Files Already in Root to DELETE Immediately

```bash
# These files are duplicated, deprecated, or superseded
rm -f NEW_TASK_FOLDER_INDEX.md
rm -f NEW_TASK_FOLDER_SYNC_PLAN.md
rm -f SYNC_COMPLETION_SUMMARY.md
rm -f RENUMBERING_021_TO_002_STATUS.md
rm -f RENUMBERING_DECISION_TASK_TASK_021.md
```

---

## Target State: Clean Directory Structure

### Final Directory Tree

```
new_task_plan/                                    (Clean workspace root)
│
├── README.md                                     ENTRY POINT - Start here
├── QUICK_START.md                                QUICK REFERENCE - By role
├── NAVIGATION_GUIDE.md                           NAVIGATION - Complete map
│
├── task_files/                                   EXECUTABLE TASKS
│   ├── README.md                                 Subdir overview
│   ├── main_tasks/                               Parent task overviews
│   │   ├── task-001.md
│   │   ├── task-002.md
│   │   ├── task-003.md
│   │   ├── task-004.md
│   │   ├── task-005.md
│   │   ├── task-006.md
│   │   ├── task-007.md
│   │   ├── task-008.md
│   │   ├── task-009.md
│   │   ├── task-010.md
│   │   ├── task-011.md
│   │   ├── task-012.md
│   │   ├── task-013.md
│   │   ├── task-014.md
│   │   ├── task-015.md
│   │   ├── task-016.md
│   │   ├── task-017.md
│   │   ├── task-018.md
│   │   ├── task-019.md
│   │   ├── task-020.md
│   │   ├── task-021.md
│   │   ├── task-022.md
│   │   ├── task-023.md
│   │   ├── task-024.md
│   │   ├── task-025.md
│   │   └── task-026.md
│   │
│   └── subtasks/                                 Self-contained implementations
│       ├── task-001-1.md
│       ├── task-001-2.md
│       ├── task-001-3.md
│       ├── task-001-4.md
│       │
│       ├── task-002-1.md
│       ├── task-002-2.md
│       ├── task-002-3.md
│       ├── task-002-4.md
│       ├── task-002-5.md
│       ├── task-002-6.md
│       ├── task-002-7.md
│       ├── task-002-8.md
│       ├── task-002-9.md
│       │
│       ├── task-021-1.md
│       ├── task-021-2.md
│       ├── task-021-3.md
│       ├── task-021-4.md
│       ├── task-021-5.md
│       ├── task-021-6.md
│       ├── task-021-7.md
│       ├── task-021-8.md
│       ├── task-021-9.md
│       │
│       └── (subtasks for tasks 003-020, 022-026)
│
├── guidance/                                     REFERENCE MATERIALS
│   ├── README.md
│   ├── GUIDANCE_INDEX.md
│   │
│   ├── architecture_alignment/
│   │   ├── HYBRID_APPROACH.md
│   │   ├── ARCHITECTURAL_PATTERNS.md
│   │   ├── SERVICE_COMPATIBILITY.md
│   │   └── IMPORT_PATH_STANDARDS.md
│   │
│   ├── merge_strategy/
│   │   ├── FINAL_MERGE_STRATEGY.md
│   │   ├── HANDLING_INCOMPLETE_MIGRATIONS.md
│   │   ├── CONFLICT_RESOLUTION.md
│   │   └── BRANCH_TARGETING.md
│   │
│   ├── implementation_lessons/
│   │   ├── IMPLEMENTATION_SUMMARY.md
│   │   ├── BEST_PRACTICES.md
│   │   ├── COMMON_PITFALLS.md
│   │   └── PERFORMANCE_OPTIMIZATION.md
│   │
│   └── phase_findings/
│       ├── phase_001_framework_strategy/
│       │   └── FINDINGS.md
│       ├── phase_002_validation_framework/
│       │   └── FINDINGS.md
│       ├── phase_003_pre_merge_validation/
│       │   └── FINDINGS.md
│       ├── phase_004_branch_alignment/
│       │   └── FINDINGS.md
│       ├── phase_005_error_detection/
│       │   └── FINDINGS.md
│       ├── phase_006_backup_restore/
│       │   └── FINDINGS.md
│       ├── phase_007_branch_identification/
│       │   └── FINDINGS.md
│       ├── phase_008_documentation_automation/
│       │   └── FINDINGS.md
│       ├── phase_009_pattern_matcher/
│       │   └── FINDINGS.md
│       ├── phase_010_pattern_validator/
│       │   └── FINDINGS.md
│       ├── phase_011_pattern_storage/
│       │   └── FINDINGS.md
│       ├── phase_012_pattern_retrieval/
│       │   └── FINDINGS.md
│       ├── phase_013_pattern_prioritization/
│       │   └── FINDINGS.md
│       └── phase_014_integration_workflow/
│           └── FINDINGS.md
│
├── execution/                                     PLANNING & COORDINATION
│   ├── README.md
│   ├── EXECUTION_STRATEGIES.md
│   ├── CRITICAL_PATH.md
│   ├── PARALLEL_EXECUTION.md
│   ├── TEAM_ALLOCATION.md
│   ├── MILESTONE_DATES.md
│   ├── RISK_ANALYSIS.md
│   ├── DEPENDENCY_MATRIX.md
│   └── TEAM_PROGRESS_TEMPLATE.md
│
├── progress/                                      STATUS TRACKING (optional)
│   ├── README.md
│   ├── COMPLETION_STATUS.md
│   └── TEAM_PROGRESS_TEMPLATE.md
│
├── reference/                                     ACTIVE REFERENCES
│   ├── README.md
│   ├── CLEAN_TASK_INDEX.md
│   ├── TASK_DEPENDENCY_VISUAL_MAP.md
│   ├── task_mapping.md
│   └── TASK_STRUCTURE_STANDARD.md
│
└── archive/                                       HISTORICAL ONLY
    ├── README.md
    ├── v1_planning/
    │   ├── WEEK_1_FINAL_SUMMARY.md
    │   └── (other deprecated planning)
    ├── v2_iteration/
    │   └── (iteration documents)
    └── deprecated/
        └── (files no longer used)
```

---

## File Inventory: Essential vs Optional

### Essential Files (Must Exist)

| File | Purpose | Updated By |
|------|---------|------------|
| `README.md` | Entry point for all users | Maintainer |
| `QUICK_START.md` | Role-based quick start | Maintainer |
| `NAVIGATION_GUIDE.md` | Complete navigation reference | Maintainer |
| `task_files/main_tasks/task-*.md` | Task overviews | Task owners |
| `task_files/subtasks/task-*-*.md` | Implementation guides | Implementers |
| `guidance/GUIDANCE_INDEX.md` | Guidance lookup | Maintainer |
| `execution/DEPENDENCY_MATRIX.md` | Task dependencies | Architect |
| `progress/COMPLETION_STATUS.md` | Master status view | Team leads |

### Optional Files (Delete if Not Needed)

| File | When to Keep | When to Delete |
|------|--------------|----------------|
| `guidance/phase_findings/*/` | Phase has findings | No findings exist |
| `progress/TEAM_*.md` | Team actively tracking | Team not started |
| `execution/RISK_ANALYSIS.md` | Risks identified | No active risks |
| `execution/MILESTONE_DATES.md` | Active execution | Planning phase |
| `reference/TASK_DEPENDENCY_VISUAL_MAP.md` | Visual learner preference | Text-only preference |

### Deprecated Files (Archive or Delete)

| File | Archive Location | Action |
|------|------------------|--------|
| `complete_new_task_outline_ENHANCED.md` | archive/v1_planning/ | Archive |
| `COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md` | archive/v1_planning/ | Archive |
| `INDEX_AND_GETTING_STARTED.md` | archive/v1_planning/ | Archive |
| `INTEGRATION_EXECUTION_CHECKLIST.md` | archive/v1_planning/ | Archive |
| `MIGRATION_FIX_SUMMARY.md` | archive/v1_planning/ | Archive |
| `RENUMBERING_021_TO_002_STATUS.md` | archive/v1_planning/ | Archive |
| `RENUMBERING_DECISION_TASK_021.md` | archive/v1_planning/ | Archive |
| `WEEK_1_FINAL_SUMMARY.md` | archive/v1_planning/ | Archive |

---

## Workflow-Centric Organization

### Phase 1: Discovery & Research (Tasks 001-003)

**Files needed:**
```
task_files/main_tasks/task-001.md
task_files/main_tasks/task-002.md
task_files/main_tasks/task-003.md
task_files/subtasks/task-001-1.md through task-001-4.md
task_files/subtasks/task-002-1.md through task-002-9.md
task_files/subtasks/task-003-1.md through task-003-5.md
guidance/architecture_alignment/
guidance/phase_findings/phase_001_framework_strategy/
guidance/phase_findings/phase_002_validation_framework/
guidance/phase_findings/phase_003_pre_merge_validation/
execution/DEPENDENCY_MATRIX.md
```

**Navigation path:** README.md → task_files/main_tasks/task-001.md → subtask selection

### Phase 2: Analysis & Validation (Tasks 004-008)

**Files needed:**
```
task_files/main_tasks/task-004.md
task_files/main_tasks/task-005.md
task_files/main_tasks/task-006.md
task_files/main_tasks/task-007.md
task_files/main_tasks/task-008.md
task_files/subtasks/task-004-*.md
task_files/subtasks/task-005-*.md
task_files/subtasks/task-006-*.md
task_files/subtasks/task-007-*.md
task_files/subtasks/task-008-*.md
guidance/merge_strategy/
guidance/phase_findings/phase_004_branch_alignment/
guidance/phase_findings/phase_005_error_detection/
guidance/phase_findings/phase_006_backup_restore/
guidance/phase_findings/phase_007_branch_identification/
guidance/phase_findings/phase_008_documentation_automation/
```

**Navigation path:** QUICK_START.md → execution/TEAM_ALLOCATION.md → task_files/

### Phase 3: Pattern Management (Tasks 009-020)

**Files needed:**
```
task_files/main_tasks/task-009.md through task-020.md
task_files/subtasks/task-009-*.md through task-020-*.md
guidance/phase_findings/phase_009_pattern_matcher/ through phase_013_prioritization/
progress/COMPLETION_STATUS.md
```

**Navigation path:** NAVIGATION_GUIDE.md → task_files/subtasks/task-XX-Y.md

### Phase 4: Integration (Tasks 021-026)

**Files needed:**
```
task_files/main_tasks/task-021.md through task-026.md
task_files/subtasks/task-021-1.md through task-021-9.md
task_files/subtasks/task-022-*.md through task-026-*.md
execution/PARALLEL_EXECUTION.md
execution/MILESTONE_DATES.md
execution/RISK_ANALYSIS.md
```

**Navigation path:** execution/PARALLEL_EXECUTION.md → team allocation → task_files/

---

## Creation Order

### Step 1: Clean Slate

```bash
cd /home/masum/github/PR/.taskmaster/new_task_plan/

# Remove deprecated files immediately
rm -f NEW_TASK_FOLDER_INDEX.md
rm -f NEW_TASK_FOLDER_SYNC_PLAN.md
rm -f SYNC_COMPLETION_SUMMARY.md
rm -f RENUMBERING_021_TO_002_STATUS.md
rm -f RENUMBERING_DECISION_TASK_021.md

# Create directory structure
mkdir -p task_files/main_tasks
mkdir -p task_files/subtasks
mkdir -p guidance/architecture_alignment
mkdir -p guidance/merge_strategy
mkdir -p guidance/implementation_lessons
mkdir -p guidance/phase_findings/phase_001_framework_strategy
mkdir -p guidance/phase_findings/phase_002_validation_framework
mkdir -p guidance/phase_findings/phase_003_pre_merge_validation
mkdir -p guidance/phase_findings/phase_004_branch_alignment
mkdir -p guidance/phase_findings/phase_005_error_detection
mkdir -p guidance/phase_findings/phase_006_backup_restore
mkdir -p guidance/phase_findings/phase_007_branch_identification
mkdir -p guidance/phase_findings/phase_008_documentation_automation
mkdir -p guidance/phase_findings/phase_009_pattern_matcher
mkdir -p guidance/phase_findings/phase_010_pattern_validator
mkdir -p guidance/phase_findings/phase_011_pattern_storage
mkdir -p guidance/phase_findings/phase_012_pattern_retrieval
mkdir -p guidance/phase_findings/phase_013_pattern_prioritization
mkdir -p guidance/phase_findings/phase_014_integration_workflow
mkdir -p execution
mkdir -p progress
mkdir -p reference
mkdir -p archive/v1_planning
mkdir -p archive/v2_iteration
mkdir -p archive/deprecated
```

### Step 2: Create Navigation Documents

Create in this order:
1. `README.md` - Entry point
2. `QUICK_START.md` - Quick reference
3. `NAVIGATION_GUIDE.md` - Complete map

### Step 3: Create Task Files

Create in priority order:
1. Task 001 (Foundation) - blocks everything
2. Task 002 (Validation) - depends on 001
3. Task 021 (Integration) - parallel with 001
4. Tasks 003-020, 022-026

### Step 4: Populate Guidance

Copy from `task_data/guidance/`:
```bash
cp ../task_data/guidance/*.md guidance/
cp ../task_data/guidance/ARCHITECTURE_*.md guidance/architecture_alignment/
cp ../task_data/guidance/MERGE_*.md guidance/merge_strategy/
cp ../task_data/guidance/IMPLEMENTATION_*.md guidance/implementation_lessons/
```

Create:
- `guidance/GUIDANCE_INDEX.md`
- `guidance/phase_findings/*/FINDINGS.md` (as findings are discovered)

### Step 5: Create Execution Documents

Create in order:
1. `execution/DEPENDENCY_MATRIX.md`
2. `execution/CRITICAL_PATH.md`
3. `execution/EXECUTION_STRATEGIES.md`
4. `execution/PARALLEL_EXECUTION.md`
5. `execution/TEAM_ALLOCATION.md`
6. `execution/MILESTONE_DATES.md`
7. `execution/RISK_ANALYSIS.md`
8. `execution/TEAM_PROGRESS_TEMPLATE.md`

### Step 6: Set Up Progress Tracking

1. Create `progress/README.md`
2. Create `progress/COMPLETION_STATUS.md` template

### Step 7: Organize References

```bash
# Move active references
mv CLEAN_TASK_INDEX.md reference/
mv TASK_DEPENDENCY_VISUAL_MAP.md reference/
mv task_mapping.md reference/
cp ../task_data/TASK_STRUCTURE_STANDARD.md reference/

# Archive historical documents
mv complete_new_task_outline_ENHANCED.md archive/v1_planning/
mv COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md archive/v1_planning/
mv INDEX_AND_GETTING_STARTED.md archive/v1_planning/
mv INTEGRATION_EXECUTION_CHECKLIST.md archive/v1_planning/
mv MIGRATION_FIX_SUMMARY.md archive/v1_planning/
mv WEEK_1_FINAL_SUMMARY.md archive/v1_planning/
```

### Step 8: Create Archive Documentation

1. Create `archive/README.md`
2. Create `reference/README.md`
3. Create `progress/README.md`
4. Create `task_files/README.md`
5. Create `execution/README.md`
6. Create `guidance/README.md`

---

## Validation Commands

### Verify Structure

```bash
# Check all directories exist
ls -d task_files/main_tasks task_files/subtasks
ls -d guidance/architecture_alignment guidance/merge_strategy guidance/implementation_lessons
ls -d guidance/phase_findings/phase_001_framework_strategy
ls -d execution progress reference archive

# Check all root files exist
ls README.md QUICK_START.md NAVIGATION_GUIDE.md
```

### Verify Task Files

```bash
# Count task files
ls task_files/main_tasks/task-*.md | wc -l  # Should be 26
ls task_files/subtasks/task-*-*.md | wc -l  # Should be ~130

# Verify naming convention
ls task_files/subtasks/task-001-*.md
ls task_files/subtasks/task-002-*.md
ls task_files/subtasks/task-021-*.md
```

### Verify No Stray Files

```bash
# Check for files that should have been moved
ls *.md | grep -v -E "(README|QUICK_START|NAVIGATION_GUIDE)" && echo "STRAY FILES FOUND"
```

---

## Quick Reference by Role

### Developer Starting Work

```
1. Read README.md
2. Read QUICK_START.md (your role)
3. Go to task_files/subtasks/task-XX-Y.md
4. Implement following the guide
5. Log progress in progress/TEAM_*.md
```

### Team Lead Planning Execution

```
1. Read NAVIGATION_GUIDE.md
2. Read execution/EXECUTION_STRATEGIES.md
3. Review execution/DEPENDENCY_MATRIX.md
4. Create execution/TEAM_ALLOCATION.md
5. Track in progress/COMPLETION_STATUS.md
```

### Integration Specialist

```
1. Read execution/CRITICAL_PATH.md
2. Review execution/DEPENDENCY_MATRIX.md
3. Check progress/COMPLETION_STATUS.md
4. Reference guidance/ as needed
```

### New Team Member

```
1. Read README.md
2. Read NAVIGATION_GUIDE.md
3. Select task from task_files/subtasks/
4. Follow implementation guide
5. Ask questions in TEAM_*.md if blocked
```

---

## Maintenance Guidelines

### Adding New Task Files

1. Create `task_files/main_tasks/task-XX.md` if new main task
2. Create `task_files/subtasks/task-XX-Y.md` with 14 sections
3. Update `execution/DEPENDENCY_MATRIX.md`
4. Update `progress/COMPLETION_STATUS.md`

### Updating Guidance

1. Update relevant file in `guidance/`
2. Update `guidance/GUIDANCE_INDEX.md`
3. Update cross-references in task files if needed

### Archiving Completed Work

1. Move to `archive/v2_iteration/` with date
2. Update `archive/README.md`
3. Update `NAVIGATION_GUIDE.md` to note archived status

---

## Appendix A: File Count Summary

| Directory | File Count | Description |
|-----------|------------|-------------|
| Root | 3 | Navigation only |
| task_files/main_tasks | 26 | Task overviews |
| task_files/subtasks | ~130 | Implementation files |
| guidance/ | ~25 | Reference documents |
| execution/ | 8 | Planning documents |
| progress/ | 2 | Tracking templates |
| reference/ | 4 | Active references |
| archive/ | ~10 | Historical documents |
| **Total** | **~208** | Essential files only |

---

## Appendix B: Deleted File Log

Files removed during cleanup:

| File | Date Removed | Reason |
|------|--------------|--------|
| `NEW_TASK_FOLDER_INDEX.md` | 2026-01-06 | Redundant with NAVIGATION_GUIDE.md |
| `NEW_TASK_FOLDER_SYNC_PLAN.md` | 2026-01-06 | Superseded by new structure |
| `SYNC_COMPLETION_SUMMARY.md` | 2026-01-06 | Historical, no longer needed |
| `RENUMBERING_021_TO_002_STATUS.md` | 2026-01-06 | Historical reference only |
| `RENUMBERING_DECISION_TASK_021.md` | 2026-01-06 | Historical reference only |

---

**Document Version:** 1.0  
**Status:** Ready for Execution  
**Next Action:** Execute Step 1 - Clean Slate and Directory Creation
