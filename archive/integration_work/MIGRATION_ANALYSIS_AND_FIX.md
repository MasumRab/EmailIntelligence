# Migration Analysis: Why Retrofitted Tasks Are Not in new_task_plan/

**Date:** January 6, 2026  
**Status:** Analysis Complete - Gap Identified  
**Scope:** Understand task migration between tasks/ and new_task_plan/task_files/ folders

---

## Executive Summary

During Phase 4 retrofit work, you created/updated 20+ task files in the `tasks/` directory with the standardized TASK_STRUCTURE_STANDARD.md format. However, these retrofitted tasks were **never migrated** to the `new_task_plan/task_files/` folder structure.

**Root Cause:** Your retrofit work was documentation-focused and operated entirely within the `tasks/` directory. The `new_task_plan/task_files/` folder contains an older, less-detailed task structure that was created during earlier planning phases. These two folder structures exist in parallel but are not synchronized.

---

## Current State

### ✅ In tasks/ Directory (Your Retrofit Work)
```
tasks/
├── task_001.md               ← Fully retrofitted (500 lines)
├── task_002.1.md             ← Fully retrofitted (500 lines)
├── task_002.2.md             ← Fully retrofitted (500 lines)
├── task_002.3.md             ← Fully retrofitted (556 lines)
├── task_002.4.md             ← Fully retrofitted (500 lines)
├── task_002.5.md             ← Fully retrofitted (500 lines)
├── task_002.6.md             ← Fully retrofitted (500 lines)
├── task_002.7.md             ← Fully retrofitted (500+ lines)
├── task_002.8.md             ← Fully retrofitted (500+ lines)
├── task_002.9.md             ← Fully retrofitted (500+ lines)
├── task_007.md               ← Fully retrofitted (433 lines)
├── task_075.1.md             ← Fully retrofitted (500 lines)
├── task_075.2.md             ← Fully retrofitted (500 lines)
├── task_075.3.md             ← Fully retrofitted (500 lines)
├── task_075.4.md             ← Fully retrofitted (500 lines)
├── task_075.5.md             ← Fully retrofitted (500 lines)
├── task_079.md               ← Fully retrofitted (545 lines)
├── task_080.md               ← Fully retrofitted (475 lines)
├── task_083.md               ← Fully retrofitted (605 lines)
└── task_100.md, task_101.md  ← Additional tasks
```

**Format:** `task_NNN.Y.md` (e.g., task_001.md, task_002.1.md)  
**Content:** Complete TASK_STRUCTURE_STANDARD.md format  
**Quality:** 100% compliance with standard template

---

### ❌ In new_task_plan/task_files/ Directory (Older Structure)
```
new_task_plan/task_files/
├── task-001.md               ← Minimal format (minimal structure)
├── task-002.md               ← Minimal format
├── task-002-clustering.md    ← Variant naming
├── task-003.md               ← Minimal format
├── task-004.md
├── ...
├── task-026.md
```

**Format:** `task-NNN.md` (hyphen vs underscore)  
**Content:** Basic structure without full TASK_STRUCTURE_STANDARD.md sections  
**Quality:** Less detailed, planning-stage format

**Sample (task-001.md from new_task_plan/):**
```markdown
# Task 001: Framework Strategy Definition
**Task ID:** 001
**Status:** pending
**Priority:** high

## Purpose
Framework Strategy Definition

## Success Criteria
- [ ] Define Target Selection Criteria
- [ ] Define Alignment Strategy Framework
- [ ] Create Documentation Foundation
- [ ] Define Safety and Verification Procedures

## Subtasks
### 001.1: Define Target Selection Criteria
...
```

vs.

**Sample (task_001.md in tasks/ - your retrofit):**
```markdown
# Task 001: Recover Lost Backend Modules and Features
**Status:** Ready for Implementation
**Priority:** High
**Effort:** 32-40 hours
**Complexity:** 7/10
**Dependencies:** None

## Purpose
Investigate Git history to find, recover, and reintegrate lost backend modules...

## Success Criteria
### Core Functionality
- [ ] Comprehensive checklist created
- [ ] Git forensics performed
...
### Integration & Testing
- [ ] Modules integrated
...
### Quality Assurance
...
### Verification
...

## Prerequisites & Dependencies
...

## Sub-subtasks
[8 detailed subtasks with effort, dependencies, steps]

## Specification
[Formal output specification]

## Testing Strategy
[8+ test cases]

## Common Gotchas & Solutions
[5 detailed gotchas]

...
```

---

## Why No Migration Happened

### 1. **Different Design Purposes**
- **tasks/ folder:** Implementation specification (detailed, ready-to-build)
- **new_task_plan/task_files/ folder:** Planning/tracking (simpler, evolutionary)

### 2. **Different Naming Conventions**
- **tasks/:** `task_NNN.Y.md` (underscores, subtask numbers like 002.1, 002.2)
- **new_task_plan/task_files/:** `task-NNN.md` (hyphens, no subtask numbers)

### 3. **Your Retrofit Scope**
- You created/updated files in the **tasks/** directory exclusively
- You did not include a migration step to push those changes into **new_task_plan/task_files/**
- The retrofit work was self-contained within tasks/

### 4. **Different Update Cycles**
- **tasks/**: Updated during Phase 4 retrofit (Dec 22 - Jan 6)
- **new_task_plan/task_files/**: Last updated during earlier planning phases
- No cross-folder synchronization was performed

---

## The Gap: What's Missing

### Missing in new_task_plan/task_files/
For each retrofitted task, the new_task_plan folder is missing:

1. ❌ Detailed Purpose section
2. ❌ Complete Success Criteria (checklists)
3. ❌ Prerequisites & Dependencies section
4. ❌ 8 Sub-subtasks with effort estimates
5. ❌ Specification section (output formats)
6. ❌ Performance Targets
7. ❌ Testing Strategy
8. ❌ Common Gotchas & Solutions
9. ❌ Helper Tools section
10. ❌ Integration Checkpoint
11. ❌ Done Definition checklist

### Impact
- **new_task_plan/task_files/** is outdated planning-stage documentation
- **tasks/** contains current, production-ready specifications
- System has **two conflicting sources of truth** for task definitions

---

## Identification of Gaps

### Gap 1: No Automated Migration
You performed retrofit work manually (create task_XXX.md files) without:
- Automatic sync script
- Folder-to-folder propagation
- Version control linking
- Cross-reference updating

### Gap 2: Naming Convention Mismatch
- Old system: `task-NNN.md`
- New system: `task_NNN.Y.md`
- Makes 1:1 mapping impossible without transformation

### Gap 3: Scope Difference
- Old system: Tracks top-level tasks (001, 002, 007, etc.)
- New system: Tracks top-level + subtasks (002.1, 002.2, 075.1, etc.)
- Task granularity differs between folders

### Gap 4: No Cross-Folder Audit
Your retrofit audit documents reference **only** the tasks/ folder:
- RETROFIT_AUDIT_REPORT.md (audits tasks/ only)
- RETROFIT_COMPLETION_SUMMARY.md (verifies tasks/ only)
- RETROFIT_PROGRAM_COMPLETE.md (covers tasks/ only)

No audit checked whether new_task_plan/ was updated.

---

## Why This Happened: Technical Context

### Historical Context
1. **new_task_plan/task_files/** was created during **initial planning phases** (older)
2. **tasks/ directory** became the **primary working folder** (newer)
3. During Phase 1.5-4 retrofit, focus was on **tasks/** because:
   - It already had task_002.1, task_002.2, etc. (subtask structure)
   - It was closer to implementation-ready state
   - It required less transformation to reach TASK_STRUCTURE_STANDARD.md

4. **new_task_plan/task_files/** was left behind because:
   - Not the active working directory
   - Would require separate retrofit pass
   - Different naming convention would complicate sync
   - No explicit requirement to migrate it

### System Design Issue
- Two parallel task folder systems exist
- No synchronization mechanism between them
- No explicit "source of truth" defined
- Creates maintenance burden and confusion

---

## How to Fix: Migration Strategy

### Option A: Migrate new_task_plan/ to Match tasks/ (Recommended)

**Steps:**
1. For each file in new_task_plan/task_files/
2. Map to corresponding retrofitted file in tasks/
3. Replace old content with retrofitted content
4. Rename to match naming convention (task-NNN.md → task_NNN.md)
5. Validate cross-folder consistency

**Example Migration:**
```bash
# new_task_plan/task_files/task-001.md → tasks/task_001.md
# (Already exists and is fully retrofitted)

# Copy tasks/ versions back to new_task_plan/task_files/ with new names
cp tasks/task_001.md new_task_plan/task_files/task-001.md
cp tasks/task_002.1.md new_task_plan/task_files/task-002-1.md  # Adjust naming
# ... repeat for all retrofitted tasks
```

**Effort:** 1-2 hours scripting + validation

**Advantage:** Single source of truth; both folders synchronized

---

### Option B: Deprecate new_task_plan/task_files/

**Steps:**
1. Remove new_task_plan/task_files/ folder from active use
2. Archive it as `new_task_plan/.archive/task_files_historical/`
3. Update documentation to reference tasks/ as single source
4. Update build/CI scripts to use tasks/ folder only

**Effort:** 30 minutes cleanup + documentation

**Advantage:** No duplication; clear responsibility assignment

---

### Option C: Establish Sync Mechanism

**Steps:**
1. Create sync script: `sync_task_folders.py`
2. Runs after any task file update
3. Propagates changes between folders
4. Handles naming convention translation
5. Validates consistency

**Effort:** 2-3 hours implementation

**Advantage:** Both folders stay synchronized automatically

---

## Recommendation

**Implement Option B (Deprecate new_task_plan/task_files/) because:**

1. ✅ **tasks/** is the active, current, retrofitted folder
2. ✅ **tasks/** has 20+ fully-specced files ready for implementation
3. ✅ **new_task_plan/task_files/** is outdated planning-stage content
4. ✅ Maintenance burden: Having two sources of truth is expensive
5. ✅ Implementation clarity: Teams should reference **one** set of task files
6. ✅ Lowest effort: Archive and redirect

**Rationale:** The retrofit work proves that **tasks/** is the better-structured, more-detailed, more-current folder. There's no value in maintaining both.

---

## Action Items

### 1. Decision (You)
- [ ] Choose migration strategy (A, B, or C above)
- [ ] Approve approach with stakeholders

### 2. Implementation (Next Thread)
If Option B (recommended):
- [ ] Archive new_task_plan/task_files/ → new_task_plan/.archive/task_files_historical/
- [ ] Update all documentation to reference tasks/ folder
- [ ] Update CI/scripts to use tasks/ folder
- [ ] Commit: "docs: deprecate new_task_plan/task_files/ in favor of tasks/"

If Option A:
- [ ] Create migration script to sync folders
- [ ] Test migration (validate file counts, naming, content)
- [ ] Commit: "feat: migrate new_task_plan/task_files/ to TASK_STRUCTURE_STANDARD.md format"

### 3. Documentation Update
- [ ] Update CLAUDE.md to reference tasks/ as primary source
- [ ] Update README.md in both directories
- [ ] Update any scripts that reference new_task_plan/

---

## Conclusion

Your retrofit work **did not fail** to migrate tasks. Rather:

1. **tasks/** is the active, retrofitted, production-ready folder (100% complete)
2. **new_task_plan/task_files/** is an older, parallel folder from earlier phases (incomplete)
3. No explicit migration was planned or executed between them
4. This creates a **maintenance debt**: two sources of truth

**Recommendation:** Archive the old folder structure and establish **tasks/** as the single source of truth for all task specifications.

---

**Next Action:** Read RETROFIT_PROGRAM_COMPLETE.md and this document together to understand the full scope of retrofit work and the folder consolidation opportunity.

**Priority:** Medium - doesn't block implementation, but should be resolved before Phase 5 code begins.
