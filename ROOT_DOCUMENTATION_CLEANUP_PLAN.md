# Root Documentation Cleanup Plan

**Status:** READY TO EXECUTE  
**Date:** January 6, 2026  
**Objective:** Archive outdated docs, consolidate into single source of truth

---

## Problem Statement

Root directory contains 118 markdown files, of which ~40 are:
- Outdated planning documents from Phase 1-2
- References to old task-NNN numbering system
- Historical analysis that contradicts current PROJECT_STATE_PHASE_3_READY.md
- Duplicate information now in standardized task files

**Impact:** Teams may reference incorrect task IDs, old processes, or outdated frameworks.

---

## Archive Categories

### 1. PHASE PLANNING DOCUMENTS (Historical, Archive)
These describe work already completed. Archive to prevent confusion:

```
├── PHASE_1_IMPLEMENTATION_COMPLETE.md
├── PHASE_1_STATUS_SUMMARY.md
├── PHASE_1.5_COMPLETION_SUMMARY.txt
├── PHASE_1_STATUS_SUMMARY.md
├── PHASE_2_4_DECISION_FRAMEWORK.md
├── PHASE_4_DEFERRED.md
├── PHASES_1_5_2_4_COMPLETE_EXECUTIVE_SUMMARY.md
├── PHASES_1_5_2_4_COMPLETE.txt
├── PHASES_2_4_EXECUTION_COMPLETE.md
└── CURRENT_STATUS_PHASE_1.5_COMPLETE.md
```

**Count:** 10 files  
**Action:** Archive to `archive/phase_planning/`

---

### 2. OLD TASK NUMBERING REFERENCES (Deprecated)
Documents that reference task-001 through task-020 or old numbering:

```
├── NEW_TASK_PLAN_EVALUATION_AND_PROCESSING_PLAN.md
├── TASK_75_CLEANUP_AND_RENUMBERING_PLAN.md
├── TASK_NUMBERING_IMPLEMENTATION_CHECKLIST.md
├── TASK_NUMBERING_ISSUE_ANALYSIS.md
├── TASK_RETROFIT_PLAN.md
├── TASK_ID_MIGRATION_QUICK_REFERENCE.md
├── OLD_TASK_NUMBERING_DEPRECATED.md (keep - it's the deprecation notice)
├── TASK_NUMBERING_DEPRECATION_PLAN.md (keep - it's the official plan)
└── ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md
```

**Count:** 9 files (2 to keep, 7 to archive)  
**Action:** Archive to `archive/deprecated_numbering/`

---

### 3. RETROFITTING & CONSOLIDATION WORK (Complete, Keep Summary Only)
Documents describing completed retrofit work:

```
├── COMPREHENSIVE_RETROFIT_PLAN.md
├── RETROFIT_AUDIT_REPORT.md
├── RETROFIT_COMPLETION_SUMMARY.md
├── RETROFIT_PROGRAM_COMPLETE.md
├── REFACTORING_COMPLETE_GATE_APPROVED.md
├── REFACTORING_STATUS_VERIFIED.md
└── TASK_RETROFIT_PLAN.md (already in archive list)
```

**Count:** 7 files  
**Action:** Keep RETROFIT_COMPLETION_SUMMARY.md (summarizes completion), archive others to `archive/retrofit_work/`

---

### 4. INTEGRATION & CONSOLIDATION DOCUMENTS (Completed)
Documents describing work that's finished or now incorporated:

```
├── MIGRATION_ANALYSIS_AND_FIX.md
├── MIGRATION_COMPLETION_REPORT.md
├── MIGRATION_VERIFICATION_COMPLETE.md
├── CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md (keep - active plan)
├── NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md (keep - active plan)
├── HANDOFF_INTEGRATION_BEFORE_AFTER.md
├── HANDOFF_INTEGRATION_COMPLETE.md
├── INTEGRATION_DOCUMENTATION_INDEX.md (reference)
├── INTEGRATION_GUIDE_SUMMARY.md
├── INTEGRATION_TRACKING.md
├── NEW_TASK_FOLDER_SYNC_COMPLETION_REPORT.md
├── README_INTEGRATION_COMPLETE.md
└── START_HERE_INTEGRATION.md
```

**Count:** 13 files (2 to keep)  
**Action:** Keep CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md and NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md (active), archive rest

---

### 5. INVESTIGATION & ANALYSIS (Completed)
Documents from investigation phases that are now resolved:

```
├── INVESTIGATION_INDEX.md
├── INVESTIGATION_SUMMARY.md
├── COMPLETE_READING_SUMMARY.md
├── COMPLETE_ANALYSIS_INDEX.md
├── ROOT_CAUSE_AND_FIX_ANALYSIS.md
├── CONSOLIDATED_INVESTIGATION_RESOLUTION.md
├── AGENT_MEMORY_INVESTIGATION_REPORT.md
├── AGENT_MEMORY_IMPLEMENTATION_SUMMARY.md
├── AGENT_GUIDANCE_PLAN.md
├── QUICK_DIAGNOSIS_GUIDE.md
└── FINDINGS_GUIDE.md
```

**Count:** 11 files  
**Action:** Archive to `archive/investigation_work/`

---

### 6. CLEANUP & VERIFICATION WORK (Completed)
Documents describing cleanup phases:

```
├── CLEANUP_BEFORE_AFTER.md
├── CLEANUP_NON_ALIGNMENT_TASKS.md
├── CLEANUP_STATUS_FINAL.md
├── CLEANUP_VERIFICATION_FINAL.txt
├── CLEANUP_VERIFICATION_REPORT.md
├── CLEANUP_SCRIPT.sh
├── EXECUTIVE_CLEANUP_SUMMARY.md
├── COMPLETION_SUMMARY.txt
├── COMPLETION_STATUS.md
├── VERIFY_ORCHESTRATION_TOOLS_CLEAN.md
└── SESSION_COMPLETION_SUMMARY.md
```

**Count:** 11 files  
**Action:** Archive to `archive/cleanup_work/`

---

### 7. BRANCH & MERGE DOCUMENTATION
Task-specific guides that are now in task files:

```
├── BRANCH_ALIGNMENT_SYSTEM.md
├── BRANCH_ANALYSIS_AND_CLEANUP_RECOMMENDATIONS.md
├── BRANCHES_TO_NEVER_MERGE.md
├── MERGE_ISSUES_REAL_WORLD_RECOVERY.md
└── IMPROVEMENTS_SUMMARY.md
```

**Count:** 5 files  
**Action:** Archive to `archive/task_context/`

---

### 8. IMPLEMENTATION & PROJECT DOCS (Keep or Archive Selectively)
Documents that may have current value:

```
KEEP (Still Relevant):
├── PROJECT_STATE_PHASE_3_READY.md (✅ CURRENT - describes Phase 3 readiness)
├── TASK_STRUCTURE_STANDARD.md (✅ CURRENT - standard for all tasks)
├── SCRIPTS_IN_TASK_WORKFLOW.md (✅ CURRENT - script reference)
├── MEMORY_API_FOR_TASKS.md (✅ CURRENT - progress logging)
├── CLAUDE.md (✅ CURRENT - auto-loaded context)
├── AGENT.md (✅ CURRENT - agent guidance)
├── AGENTS.md (✅ CURRENT - agent guidance from system)
├── README.md (✅ CURRENT - overview)
├── opencode.json (✅ CURRENT - config)
├── config.json (✅ CURRENT - config)
├── state.json (✅ CURRENT - state)
└── plan.md (⚠️ REVIEW - may need archiving)

ARCHIVE (Superseded):
├── PROJECT_REFERENCE.md (outdated task refs - superseded by current tasks)
├── TASK_HIERARCHY_VISUAL_MAP.md (old numbering - create new one)
├── TASK_HIERARCHY_DOCUMENTATION_INDEX.md (old numbering)
├── START_HERE_PHASE_1.5.md (historical phase doc)
├── START_HERE_APPROVAL_GUIDE.md (old approval process)
├── START_HERE_PHASE_1.5.md (historical)
├── START_DEVELOPMENT.md (historical)
├── QUICK_START_ALL_PHASES.md (historical)
├── QUICK_START_APPROVAL_GUIDE.md (historical)
└── QUICKSTART_IMPROVEMENTS.md (historical)
```

**Action:** Archive outdated START_HERE, PROJECT_REFERENCE, etc. to `archive/project_docs/`

---

## Archive Directory Structure

```
archive/
├── deprecated_numbering/
│   ├── TASK_NUMBERING_ISSUE_ANALYSIS.md
│   ├── TASK_NUMBERING_IMPLEMENTATION_CHECKLIST.md
│   ├── TASK_ID_MIGRATION_QUICK_REFERENCE.md
│   ├── TASK_RETROFIT_PLAN.md
│   ├── NEW_TASK_PLAN_EVALUATION_AND_PROCESSING_PLAN.md
│   ├── TASK_75_CLEANUP_AND_RENUMBERING_PLAN.md
│   ├── ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md
│   └── INDEX.md (explains deprecated numbering)
│
├── phase_planning/
│   ├── PHASE_1_IMPLEMENTATION_COMPLETE.md
│   ├── PHASE_1_STATUS_SUMMARY.md
│   ├── PHASE_2_4_DECISION_FRAMEWORK.md
│   ├── PHASES_1_5_2_4_COMPLETE_EXECUTIVE_SUMMARY.md
│   ├── CURRENT_STATUS_PHASE_1.5_COMPLETE.md
│   └── INDEX.md (explains phase planning docs)
│
├── retrofit_work/
│   ├── COMPREHENSIVE_RETROFIT_PLAN.md
│   ├── RETROFIT_AUDIT_REPORT.md
│   ├── REFACTORING_COMPLETE_GATE_APPROVED.md
│   ├── REFACTORING_STATUS_VERIFIED.md
│   └── INDEX.md (explains retrofit work)
│
├── integration_work/
│   ├── MIGRATION_ANALYSIS_AND_FIX.md
│   ├── MIGRATION_COMPLETION_REPORT.md
│   ├── HANDOFF_INTEGRATION_BEFORE_AFTER.md
│   ├── NEW_TASK_FOLDER_SYNC_COMPLETION_REPORT.md
│   ├── INTEGRATION_GUIDE_SUMMARY.md
│   ├── INTEGRATION_TRACKING.md
│   └── INDEX.md
│
├── investigation_work/
│   ├── INVESTIGATION_SUMMARY.md
│   ├── COMPLETE_ANALYSIS_INDEX.md
│   ├── ROOT_CAUSE_AND_FIX_ANALYSIS.md
│   ├── AGENT_MEMORY_INVESTIGATION_REPORT.md
│   ├── AGENT_GUIDANCE_PLAN.md
│   └── INDEX.md
│
├── cleanup_work/
│   ├── CLEANUP_BEFORE_AFTER.md
│   ├── CLEANUP_VERIFICATION_REPORT.md
│   ├── EXECUTIVE_CLEANUP_SUMMARY.md
│   ├── SESSION_COMPLETION_SUMMARY.md
│   └── INDEX.md
│
├── project_docs/
│   ├── PROJECT_REFERENCE.md (with deprecation notice at top)
│   ├── TASK_HIERARCHY_DOCUMENTATION_INDEX.md
│   ├── START_HERE_PHASE_1.5.md
│   ├── QUICK_START_ALL_PHASES.md
│   ├── START_DEVELOPMENT.md
│   └── INDEX.md
│
├── task_context/
│   ├── BRANCH_ALIGNMENT_SYSTEM.md
│   ├── MERGE_ISSUES_REAL_WORLD_RECOVERY.md
│   ├── BRANCHES_TO_NEVER_MERGE.md
│   └── INDEX.md
│
└── README.md (master archive index)
```

---

## Implementation Phases

### Phase 1: Create Archive Structure (15 minutes)

```bash
mkdir -p /home/masum/github/PR/.taskmaster/archive/{deprecated_numbering,phase_planning,retrofit_work,integration_work,investigation_work,cleanup_work,project_docs,task_context}
```

---

### Phase 2: Move Files (30 minutes)

**Step A: Deprecated Numbering**
```bash
mv TASK_NUMBERING_ISSUE_ANALYSIS.md archive/deprecated_numbering/
mv TASK_NUMBERING_IMPLEMENTATION_CHECKLIST.md archive/deprecated_numbering/
mv TASK_ID_MIGRATION_QUICK_REFERENCE.md archive/deprecated_numbering/
mv TASK_RETROFIT_PLAN.md archive/deprecated_numbering/
mv NEW_TASK_PLAN_EVALUATION_AND_PROCESSING_PLAN.md archive/deprecated_numbering/
mv TASK_75_CLEANUP_AND_RENUMBERING_PLAN.md archive/deprecated_numbering/
mv ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md archive/deprecated_numbering/
```

**Step B: Phase Planning**
```bash
mv PHASE_1_IMPLEMENTATION_COMPLETE.md archive/phase_planning/
mv PHASE_1_STATUS_SUMMARY.md archive/phase_planning/
mv PHASE_2_4_DECISION_FRAMEWORK.md archive/phase_planning/
mv PHASES_1_5_2_4_COMPLETE_EXECUTIVE_SUMMARY.md archive/phase_planning/
mv CURRENT_STATUS_PHASE_1.5_COMPLETE.md archive/phase_planning/
mv PHASE_4_DEFERRED.md archive/phase_planning/
# etc...
```

**Step C: Retrofit Work**
```bash
mv COMPREHENSIVE_RETROFIT_PLAN.md archive/retrofit_work/
mv RETROFIT_AUDIT_REPORT.md archive/retrofit_work/
mv REFACTORING_COMPLETE_GATE_APPROVED.md archive/retrofit_work/
# etc...
```

**Step D: Integration Work**
```bash
mv MIGRATION_ANALYSIS_AND_FIX.md archive/integration_work/
mv MIGRATION_COMPLETION_REPORT.md archive/integration_work/
mv HANDOFF_INTEGRATION_BEFORE_AFTER.md archive/integration_work/
# etc...
```

**Step E: Investigation Work**
```bash
mv INVESTIGATION_SUMMARY.md archive/investigation_work/
mv COMPLETE_ANALYSIS_INDEX.md archive/investigation_work/
mv ROOT_CAUSE_AND_FIX_ANALYSIS.md archive/investigation_work/
# etc...
```

**Step F: Cleanup Work**
```bash
mv CLEANUP_BEFORE_AFTER.md archive/cleanup_work/
mv CLEANUP_VERIFICATION_REPORT.md archive/cleanup_work/
mv EXECUTIVE_CLEANUP_SUMMARY.md archive/cleanup_work/
# etc...
```

**Step G: Project Docs (Superseded)**
```bash
mv PROJECT_REFERENCE.md archive/project_docs/
mv TASK_HIERARCHY_DOCUMENTATION_INDEX.md archive/project_docs/
mv START_HERE_PHASE_1.5.md archive/project_docs/
# etc...
```

---

### Phase 3: Create Archive Index Files (15 minutes)

For each archive subdirectory, create an INDEX.md explaining what's there and why it was archived.

---

### Phase 4: Update Root Documentation (15 minutes)

Create/update these files in root:

**Updated README.md**
- Remove references to archived documents
- Point to active documentation
- List archived docs at bottom with links

**NEW: CURRENT_DOCUMENTATION_MAP.md**
- Map what current team should read
- By role (developer, manager, architect)
- Links ONLY to active documents

**NEW: ARCHIVE_README.md**
- Explain what's in archive and why
- When to reference archived material
- How to interpret historical documents

---

## Files to KEEP in Root (Current, Active)

These are the only `.md` files that should be in root after cleanup:

```
ACTIVE DOCUMENTATION (Keep in root):
├── README.md (updated - points to current docs)
├── CLAUDE.md (auto-loaded context)
├── AGENT.md (agent instructions)
├── AGENTS.md (system agent guidance)
├── PROJECT_STATE_PHASE_3_READY.md (CURRENT - Phase 3 status)
├── TASK_STRUCTURE_STANDARD.md (CURRENT - task template)
├── NEW_TASK_PLAN_CONSOLIDATION_STRATEGY.md (CURRENT - consolidation plan)
├── CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md (CURRENT - implementation)
├── TASK_NUMBERING_DEPRECATION_PLAN.md (CURRENT - deprecation notice)
├── OLD_TASK_NUMBERING_DEPRECATED.md (CURRENT - deprecation notice)
├── SCRIPTS_IN_TASK_WORKFLOW.md (CURRENT - helper scripts)
├── MEMORY_API_FOR_TASKS.md (CURRENT - progress logging)
├── ROOT_DOCUMENTATION_CLEANUP_PLAN.md (THIS FILE - cleanup plan)
├── CURRENT_DOCUMENTATION_MAP.md (NEW - what to read)
├── ARCHIVE_README.md (NEW - archive index)
├── CURRENT_STATUS_SUMMARY.txt (NEW - 1-page status)
└── config.json, state.json, opencode.json (config)

HISTORICAL/REFERENCE (Archive these):
├── All PHASE_*.md files
├── All TASK_NUMBERING_*.md files (except deprecation)
├── All PROJECT_REFERENCE.md (superseded)
├── All START_HERE_*.md files (except CLAUDE.md)
├── All CLEANUP_*.md files
├── All INTEGRATION_*.md files
├── etc. (see list above)
```

---

## Files to Keep in new_task_plan/

After consolidation is complete:

```
KEEP (Active):
├── README.md (updated - points to task_files/)
├── task_files/
│   ├── task_007.md
│   ├── task_075.1-5.md
│   ├── task_079-083.md
│   ├── INDEX.md
│   └── DEFERRED_TASKS.md
├── TASK_DEPENDENCY_VISUAL_MAP.md (updated with new numbering)
└── planning_docs/
    └── (old planning materials, archived)

ARCHIVE (Move to new_task_plan/archive/):
├── CLEAN_TASK_INDEX.md
├── complete_new_task_outline_ENHANCED.md
├── COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md (old numbering)
├── RENUMBERING_021_TO_002_STATUS.md
├── RENUMBERING_DECISION_TASK_021.md
├── INDEX_AND_GETTING_STARTED.md
├── task_mapping.md
├── INTEGRATION_EXECUTION_CHECKLIST.md
├── TASK-001-INTEGRATION-GUIDE.md
├── TASK-021-*.md (all old task guides)
└── All other .md planning documents
```

---

## Success Criteria

After cleanup is complete:

- ✅ Root directory has only 15-20 active `.md` files (down from 118)
- ✅ All active files are current and relevant
- ✅ All archived files are in `archive/` with clear categorization
- ✅ Archive has an INDEX.md explaining what's there and why
- ✅ No references to task-001 through task-020 in active docs
- ✅ No outdated PHASE_*.md files in root
- ✅ New team member can read CURRENT_DOCUMENTATION_MAP.md to know what to read
- ✅ All task consolidation files are active (CONSOLIDATION_IMPLEMENTATION_CHECKLIST.md, etc.)

---

## Implementation Checklist

### Phase 1: Create Archive Structure
- [ ] Create archive/ subdirectories
- [ ] Verify all subdirectories created

### Phase 2: Move Files
- [ ] Move deprecated numbering files
- [ ] Move phase planning files
- [ ] Move retrofit work files
- [ ] Move integration work files
- [ ] Move investigation work files
- [ ] Move cleanup work files
- [ ] Move project docs files
- [ ] Move task context files
- [ ] Verify no files left behind
- [ ] Verify files moved (not copied)

### Phase 3: Create Archive Indices
- [ ] Create archive/README.md (master index)
- [ ] Create archive/deprecated_numbering/INDEX.md
- [ ] Create archive/phase_planning/INDEX.md
- [ ] Create archive/retrofit_work/INDEX.md
- [ ] Create archive/integration_work/INDEX.md
- [ ] Create archive/investigation_work/INDEX.md
- [ ] Create archive/cleanup_work/INDEX.md
- [ ] Create archive/project_docs/INDEX.md
- [ ] Create archive/task_context/INDEX.md

### Phase 4: Create Root Documentation
- [ ] Update README.md (remove archived refs)
- [ ] Create CURRENT_DOCUMENTATION_MAP.md
- [ ] Create ARCHIVE_README.md (points to archive/)
- [ ] Create CURRENT_STATUS_SUMMARY.txt (1-page overview)

### Phase 5: Verification
- [ ] Root has only active docs (~15-20 files)
- [ ] Archive has all moved files
- [ ] All archive subdirectories have INDEX.md
- [ ] CURRENT_DOCUMENTATION_MAP.md is clear and useful
- [ ] No broken references in active documents
- [ ] Git add all changes

---

## Timeline

| Phase | Task | Duration |
|-------|------|----------|
| 1 | Create structure | 15 min |
| 2 | Move files | 30 min |
| 3 | Create indices | 15 min |
| 4 | Update root docs | 15 min |
| 5 | Verification | 15 min |
| **Total** | **Complete cleanup** | **~90 min** |

---

**Status:** READY TO EXECUTE  
**Estimated Effort:** 90 minutes  
**Next Step:** Execute Phase 1 (create archive structure)
