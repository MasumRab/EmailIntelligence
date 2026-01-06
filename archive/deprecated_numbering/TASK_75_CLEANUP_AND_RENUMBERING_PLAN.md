# Task 75 Cleanup and Renumbering Plan

**Date:** January 6, 2026  
**Status:** Ready for Execution  
**Objective:** Consolidate orphaned Task 75 work into main task registry with proper numbering

---

## Executive Summary

Task 75 (Branch Clustering System) exists as 9 detailed markdown files in `task_data/` but is orphaned from the main task registry. This plan consolidates the work into proper task files while removing all orphaned references.

### Key Actions

1. **Rename task-75.md → task_002.md** (Branch Clustering System - Main Task)
2. **Consolidate task-75.1 through task-75.5 into task_002-clustering.md** (detailed implementation guide)
3. **Remove tasks 75.6-75.9** (Pipeline Integration, Visualization, Testing, Framework - belong in future phases)
4. **Update session_log.json** to reference task-002
5. **Remove all HANDOFF_75.*.md files** from archived_handoff/
6. **Remove all task-75.*.md backups**
7. **Update investigation documents** to reference proper numbering
8. **Clean up memory system** to remove Task 75 references

---

## Current State Analysis

### Files to Consolidate

**Main Task Files (task_data/):**
- task-75.md (1,294 lines) - Main task definition
- task-75.1.md (769 lines) - CommitHistoryAnalyzer
- task-75.2.md (727 lines) - CodebaseStructureAnalyzer
- task-75.3.md (661 lines) - DiffDistanceCalculator
- task-75.4.md (788 lines) - BranchClusterer
- task-75.5.md (755 lines) - IntegrationTargetAssigner
- task-75.6.md - PipelineIntegration (DEFER - Phase 2)
- task-75.7.md - VisualizationReporting (DEFER - Phase 3)
- task-75.8.md - TestingSuite (DEFER - Phase 3)
- task-75.9.md - FrameworkIntegration (DEFER - Phase 3)

**Handoff Files (task_data/archived_handoff/):**
- HANDOFF_75.1_CommitHistoryAnalyzer.md
- HANDOFF_75.2_CodebaseStructureAnalyzer.md
- HANDOFF_75.3_DiffDistanceCalculator.md
- HANDOFF_75.4_BranchClusterer.md
- HANDOFF_75.5_IntegrationTargetAssigner.md
- HANDOFF_75.6_PipelineIntegration.md
- HANDOFF_75.7_VisualizationReporting.md
- HANDOFF_75.8_TestingSuite.md
- HANDOFF_75.9_FrameworkIntegration.md

**Backup Files (task_data/backups/):**
- task-75.1.md through task-75.9.md (all backed up)

**System Files:**
- .backups/task-75.md.20260104_200852
- .backups/task-75.6.md.20260104_200852

**In-Memory References:**
- .agent_memory/session_log.json (lines 131-140: task_002_clustering reference)
- Various tracking documents referencing Task 75

**Tasks Directory:**
- tasks/task_075.md (existing, different content - Feature Branch Identification)

---

## Renumbering Strategy

### Option A: Use Task 002 (Recommended)

**Rationale:**
- Completes the task sequence (001 exists, 003-006 would be filled later)
- Maintains chronological consistency (Work on Task 75 happened after initial planning)
- Avoids conflicts with existing tasks (007, 079, 080, 083, 100, 101)
- Session log already references task_002_clustering

**File Mapping:**
```
task-75.md                  →  task_002.md (main task)
task-75.1 through 75.5      →  task_002-clustering.md (subtasks guide)
task-75.6 through 75.9      →  DEFERRED (Phase 2+ work)
```

### Option B: Use Task 006 (Alternative)

**Rationale:**
- Keeps tasks within 000-009 range
- Leaves room for tasks 003-005

**File Mapping:**
```
task-75.md                  →  task_006.md
task-75.1 through 75.5      →  task_006-clustering.md
```

---

## Detailed Execution Steps

### Phase 1: File Consolidation (15 minutes)

#### Step 1: Create task_002.md (Consolidate Main Task)

Combine:
- task-75.md (main content)
- task-75.1.md (CommitHistoryAnalyzer details in section)
- task-75.2.md (CodebaseStructureAnalyzer details)
- task-75.3.md (DiffDistanceCalculator details)
- task-75.4.md (BranchClusterer details)
- task-75.5.md (IntegrationTargetAssigner details)

Structure:
```
# Task 002: Branch Clustering System

## Overview
[From task-75.md]

## Status & Dependencies
[From task-75.md]

## Success Criteria
[From task-75.md]

## Subtasks & Details

### 002.1: CommitHistoryAnalyzer
[From task-75.1.md - condensed]

### 002.2: CodebaseStructureAnalyzer
[From task-75.2.md - condensed]

### 002.3: DiffDistanceCalculator
[From task-75.3.md - condensed]

### 002.4: BranchClusterer
[From task-75.4.md - condensed]

### 002.5: IntegrationTargetAssigner
[From task-75.5.md - condensed]

## Configuration & Defaults
[Consolidated from all files]

## Common Gotchas & Solutions
[Consolidated from all files]

## Integration Handoff
[Consolidated from all files]

## Done Definition
[From task-75.md]
```

#### Step 2: Create task_002-clustering.md (Implementation Guide)

Consolidate:
- task-75.1.md through task-75.5.md (complete subtask details)

Structure:
```
# Task 002: Branch Clustering System - Implementation Guide

## Subtask Overview & Execution Strategy

### Execution Strategy 1: Full Parallel (Recommended)
[From task-75.md]

### Subtasks 002.1-002.5 Details
[Complete details from individual files]
```

#### Step 3: Archive Deferred Tasks

Move to deferred/:
- task-75.6.md → deferred/task-075.6-pipeline-integration.md
- task-75.7.md → deferred/task-075.7-visualization.md
- task-75.8.md → deferred/task-075.8-testing.md
- task-75.9.md → deferred/task-075.9-framework.md

Create DEFERRED_TASKS.md explaining why tasks 6-9 are deferred.

### Phase 2: Reference Updates (20 minutes)

#### Step 4: Update session_log.json

```json
{
  "dependencies": {
    "task_002_clustering": {
      "status": "ready_for_implementation",
      "description": "Branch Clustering System",
      "blocks": ["task_007", "task_008"]
    }
  },
  "outstanding_todos": [
    {
      "id": "todo_impl_002",
      "title": "Implement Task 002: Branch Clustering System",
      "description": "Review task_002.md and task_002-clustering.md, implement CommitHistoryAnalyzer through IntegrationTargetAssigner",
      "status": "pending"
    }
  ]
}
```

#### Step 5: Update Tracking Documents

Search and replace:
- `Task 75` → `Task 002`
- `task-75` → `task-002`
- `75.1-75.5` → `002.1-002.5`
- `75.6-75.9` → `deferred` (with explanation)

Files to update:
- INVESTIGATION_INDEX.md
- INVESTIGATION_SUMMARY.md
- ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md
- MERGE_ISSUES_REAL_WORLD_RECOVERY.md
- QUICK_DIAGNOSIS_GUIDE.md
- TASK_75_DOCUMENTATION_INDEX.md → renamed to TASK_002_DOCUMENTATION_INDEX.md

### Phase 3: Cleanup (10 minutes)

#### Step 6: Remove Orphaned Files

Delete:
- All task-75.*.md files in task_data/ (keep backups for 30 days minimum)
- All HANDOFF_75.*.md files in task_data/archived_handoff/
- All task-75.*.md files in task_data/backups/
- All task-75.*.md files in .backups/
- Old investigation documents referencing Task 75 exclusively

#### Step 7: Clean Up tasks/task_075.md

Note: tasks/task_075.md contains different content (Feature Branch Identification). This is the OLD Task 75 and should be reviewed:
- Either merge into task_007.md (if related to branch identification)
- Or rename to task_007_legacy.md for reference

### Phase 4: Verification (10 minutes)

#### Step 8: Validation Checks

```bash
# Check no task-75 files remain
find . -name "*task-75*" -o -name "*Task 75*"  # Should be empty

# Check task_002 files exist
ls tasks/task_002.md tasks/task_002-clustering.md

# Check references updated
grep -r "Task 75\|task-75" . --exclude-dir=.git | grep -v ARCHIVE | grep -v old_

# Check session_log.json valid JSON
python -m json.tool .agent_memory/session_log.json

# Check no broken links in task files
grep "75\.[0-9]\|task-75" tasks/*.md  # Should be empty
```

#### Step 9: Documentation

Create CLEANUP_COMPLETION_REPORT.md documenting:
- All files consolidated
- All references updated
- Verification results
- Deferred tasks location
- Next steps for implementation

---

## Consolidated Task Content Structure

### task_002.md (Main Task)

**File Size:** ~4,500 lines (consolidated from 5 files)

**Sections:**
1. Overview & Purpose (from task-75.md)
2. Developer Quick Reference (consolidated)
3. Success Criteria (from task-75.md)
4. Execution Strategies (from task-75.md)
5. Integration Architecture (from task-75.md)
6. Configuration (consolidated from all files)
7. Subtask Details (002.1-002.5)
8. Performance Baselines
9. Common Gotchas & Solutions (consolidated, ~70+ items)
10. Integration Checkpoint
11. Done Definition

### task_002-clustering.md (Implementation Guide)

**File Size:** ~3,200 lines (consolidated from 5 files)

**Sections:**
1. Execution Strategies with Timelines
2. Detailed Subtask Specifications
   - 002.1: CommitHistoryAnalyzer (8 sub-subtasks)
   - 002.2: CodebaseStructureAnalyzer (8 sub-subtasks)
   - 002.3: DiffDistanceCalculator (8 sub-subtasks)
   - 002.4: BranchClusterer (8 sub-subtasks)
   - 002.5: IntegrationTargetAssigner (8 sub-subtasks)
3. Technical Reference (consolidated)
4. Configuration Examples (YAML)
5. Testing Strategy
6. Integration Handoff Details

---

## Risk Mitigation

### Potential Issues & Mitigation

| Issue | Mitigation |
|-------|-----------|
| Consolidation loses detail | Keep complete task-75.*.md copies in archive/ for 90 days |
| References break during update | Use find/replace with review on each match |
| task_075.md in tasks/ conflicts | Rename to task_007_legacy.md and document relationship |
| Session log has stale info | Regenerate with up-to-date dependency graph |
| Deferred tasks (75.6-75.9) lost | Move to deferred/ with clear tracking |
| Users look for task-75 docs | Create MIGRATED_TASKS.md with redirect table |

### Backup Strategy

Before any deletions:
```bash
# Create comprehensive backup
tar czf .backups/task-75_complete_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  task_data/task-75*.md \
  task_data/archived_handoff/HANDOFF_75*.md \
  task_data/backups/task-75*.md \
  .backups/task-75*

# Keep for 90 days minimum, then delete
```

---

## Success Criteria

Cleanup is complete when:

- [ ] task_002.md created and contains all core content
- [ ] task_002-clustering.md created with full implementation guide
- [ ] All task-75.*.md files removed from main task_data/
- [ ] All HANDOFF_75.*.md files removed
- [ ] All backup copies removed
- [ ] session_log.json updated with task_002 references
- [ ] All tracking documents updated (INVESTIGATION_INDEX.md, etc.)
- [ ] `find . -name "*task-75*"` returns only archived items
- [ ] `find . -name "*Task 75*"` returns only archived items
- [ ] CLEANUP_COMPLETION_REPORT.md created
- [ ] MIGRATED_TASKS.md created with redirect table
- [ ] No broken links in documentation
- [ ] No references to outdated numbering in active docs

---

## Post-Cleanup Next Steps

1. **Implementation Phase:** Follow task_002-clustering.md for execution
2. **Phase 2 Preparation:** Review deferred/task-075.6* through task-075.9* for future phases
3. **Task Registry:** Ensure tasks.json updated with task_002 entry
4. **Documentation:** Update project README to reference task_002

---

## Appendix A: File Mapping Reference

| Old Name | New Name | Status | Archive Path |
|----------|----------|--------|---|
| task-75.md | task_002.md | Active | archived/ |
| task-75.1.md | → task_002.md | Consolidated | archived/ |
| task-75.2.md | → task_002.md | Consolidated | archived/ |
| task-75.3.md | → task_002.md | Consolidated | archived/ |
| task-75.4.md | → task_002.md | Consolidated | archived/ |
| task-75.5.md | → task_002.md | Consolidated | archived/ |
| task-75.6.md | deferred/task-075.6* | Deferred | deferred/ |
| task-75.7.md | deferred/task-075.7* | Deferred | deferred/ |
| task-75.8.md | deferred/task-075.8* | Deferred | deferred/ |
| task-75.9.md | deferred/task-075.9* | Deferred | deferred/ |
| HANDOFF_75.*.md | → archived/HANDOFF_old/ | Archived | archived/ |
| task_075.md (tasks/) | task_007_legacy.md? | Review | tasks/ |

---

## Appendix B: Deferred Tasks Explanation

**Why are tasks 75.6-75.9 deferred?**

- **75.6 (PipelineIntegration):** Integrates all 5 analyzers; requires 75.1-75.5 complete
- **75.7 (VisualizationReporting):** Creates dashboards for clustering output; Phase 3 feature
- **75.8 (TestingSuite):** Comprehensive testing; follows implementation (Phase 2)
- **75.9 (FrameworkIntegration):** Deployment and production setup; Phase 3

These will be scheduled as:
- **Phase 2:** Tasks 002.6 (PipelineIntegration + Testing)
- **Phase 3:** Tasks 003.1 (Visualization) + 003.2 (Framework Integration)

See deferred/PHASE_2_AND_3_ROADMAP.md for planning.

---

**Prepared by:** Documentation Enhancement Agent  
**Ready for Execution:** Yes  
**Estimated Duration:** 55 minutes  
**Next Step:** Execute Phase 1 (File Consolidation)
