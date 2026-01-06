# ⚠️ DEPRECATED: Old Task Numbering System (task-001 through task-020)

**Status:** ❌ DEPRECATED as of January 6, 2026  
**Replacement:** TASK_STRUCTURE_STANDARD.md numbering  
**Current Active Tasks:** 9 files (task_007.md, task_075.1-5.md, task_079-083.md)

---

## DO NOT USE THIS NUMBERING SYSTEM

### ❌ DEPRECATED (Don't use)
```
task-001.md   task-002.md   task-003.md   ... task-020.md
task-001      task-002      task-003      ... task-020
new_task_plan/task_files/
```

### ✅ USE CURRENT SYSTEM INSTEAD
```
task_007.md              ← Branch Alignment Strategy Framework
task_075.1.md - 075.5.md ← Alignment Analyzers (Stage 1-2)
task_079.md              ← Orchestration Framework
task_080.md              ← Validation Integration
task_083.md              ← E2E Testing & Reporting
```

---

## Why the Change?

The old task numbering (task-001 through task-020) was a **planning-stage view** of the project created during early phases. As the project evolved, the numbering was consolidated and reorganized to focus on the **Phase 3 Alignment Framework** scope.

### What Changed
| Old | Status | Reason |
|-----|--------|--------|
| task-001 through task-020 | Superseded | Planning-stage numbering |
| new_task_plan/task_files/ | Removed | Outdated structure |
| Tasks 001, 002 | Consolidated | Merged into Phase 3 tasks |

### What's Current Now
| New | Status | Scope |
|-----|--------|-------|
| task_007.md | Active | Alignment Strategy (Phase 3) |
| task_075.1-5.md | Active | Alignment Analyzers (Phase 3) |
| task_079-083.md | Active | Orchestration Framework (Phase 3) |
| TASK_STRUCTURE_STANDARD.md | Active | Template for all new tasks |

---

## Quick Migration Guide

If you encounter old references, use this mapping:

| Old Task ID | Maps To | New File | Current Status |
|-------------|---------|----------|-----------------|
| task-001 | Alignment Strategy | task_007.md | Active (retrofitted) |
| task-002 | Validation/Clustering | task_079.md + task_075.1-5.md | Active (retrofitted) |
| task-003 | Pre-merge Validation | task_080.md | Active (retrofitted) |
| task-004 | Alignment Framework | task_079.md | Active (retrofitted) |
| task-005 | Error Detection | task_083.md | Active (retrofitted) |
| task-006 | Backup/Restore | (Deferred) | Not in Phase 3 scope |
| task-007 | Feature ID Tool | task_075.1-3.md | Active (renamed) |
| task-008 | Changes Summary | task_083.md | Active (integrated) |
| task-009 | Post-alignment | task_083.md | Active (integrated) |
| task-010-020 | Various | (Deferred) | Not in Phase 3 scope |

---

## Correct Task Structure (Phase 3)

### Current active tasks:

```
Phase 3: Alignment Framework

1. Task 007: Branch Alignment Strategy Framework
   └─ File: tasks/task_007.md
   └─ Scope: Define alignment strategy framework
   └─ Status: Retrofitted, ready for implementation

2. Tasks 075.1-5: Alignment Analyzers
   ├─ task_075.1.md: CommitHistoryAnalyzer
   ├─ task_075.2.md: CodebaseStructureAnalyzer
   ├─ task_075.3.md: DiffDistanceCalculator
   ├─ task_075.4.md: BranchClusterer
   └─ task_075.5.md: IntegrationTargetAssigner
   └─ Scope: Stage 1-2 analyzers for alignment
   └─ Status: Retrofitted, ready for implementation

3. Task 079: Parallel Alignment Orchestration Framework
   └─ File: tasks/task_079.md
   └─ Scope: Execute parallel alignment safely
   └─ Dependencies: Task 007
   └─ Status: Retrofitted, ready for implementation

4. Task 080: Pre-merge Validation Framework
   └─ File: tasks/task_080.md
   └─ Scope: Validate alignment before merge
   └─ Dependencies: Task 079
   └─ Status: Retrofitted, ready for implementation

5. Task 083: E2E Testing and Reporting
   └─ File: tasks/task_083.md
   └─ Scope: Comprehensive testing framework
   └─ Dependencies: Task 079, 080
   └─ Status: Retrofitted, ready for implementation
```

---

## Where to Find Current Tasks

```bash
# Correct location for current tasks
/home/masum/github/PR/.taskmaster/tasks/

# All 9 Phase 3 tasks
task_007.md
task_075.1.md
task_075.2.md
task_075.3.md
task_075.4.md
task_075.5.md
task_079.md
task_080.md
task_083.md
```

---

## What Happened to Old Files?

### `new_task_plan/task_files/` folder
- ❌ Removed: task-001.md through task-020.md
- 📦 Archived: All files preserved in git history
- 🔍 Recoverable: Use `git log --all --full-history` if needed
- ✅ Decision: Focus on Phase 3 current scope only

### Historical documents referencing old numbering
- ❌ Deprecated but preserved for reference
- 📂 Location: Archive folder with deprecation index
- 🔗 Cross-reference: TASK_NUMBERING_DEPRECATION_PLAN.md

---

## For Developers

### If you see old task references in code:

**Before:**
```python
# WRONG - These tasks don't exist anymore
# TODO: Implement per task-002 clustering system
# TODO: Follow task-003 validation approach
```

**After:**
```python
# CORRECT - Reference current Phase 3 tasks
# TODO: Implement per task_079 orchestration framework
# TODO: Follow task_080 validation approach
```

### If you find old documentation:

1. Check if it's historical/archived
   - Is it in `/archive/` or `/deprecated/`? → It's historical, don't reference
   
2. Check if it needs updating
   - Is it in active project folder? → Update references to current tasks
   
3. When in doubt:
   - Reference: PROJECT_STATE_PHASE_3_READY.md (current state)
   - Reference: tasks/task_007.md etc. (current active tasks)
   - Reference: TASK_STRUCTURE_STANDARD.md (current template)

---

## How to Know You Have the Right Task

### Characteristics of CURRENT tasks:
✅ Located in `/tasks/` directory (not `new_task_plan/`)  
✅ Follow TASK_STRUCTURE_STANDARD.md format  
✅ Have 11 required sections (Purpose, Success Criteria, etc.)  
✅ Have 8 sub-subtasks with effort estimates  
✅ Referenced in PROJECT_STATE_PHASE_3_READY.md  
✅ File count: exactly 9 tasks (007, 075.1-5, 079-083)  

### Characteristics of OLD tasks (deprecated):
❌ Located in `new_task_plan/task_files/` (deleted)  
❌ Named `task-001.md` through `task-020.md` format  
❌ Don't follow TASK_STRUCTURE_STANDARD.md  
❌ Only mentioned in historical documents  
❌ Referenced in archived deprecation documents  

---

## Questions?

**Q: Where are the old task files?**  
A: Removed from active project. Historical copies preserved in git history. Reference TASK_NUMBERING_DEPRECATION_PLAN.md for details.

**Q: Why was the numbering changed?**  
A: Project scope narrowed from 20 planning-stage tasks to 9 focused Phase 3 implementation tasks. Numbering was consolidated to reflect current scope.

**Q: Which task should I work on?**  
A: See PROJECT_STATE_PHASE_3_READY.md for implementation sequence and current status.

**Q: What if I need to reference old work?**  
A: Check git history or archive folder. But for current implementation, use only Phase 3 tasks (007, 075.1-5, 079-083).

**Q: Are the old tasks lost?**  
A: No—all preserved in git history and task_data/ archive. But they're not part of Phase 3 scope.

---

## Summary

| Aspect | Old | New |
|--------|-----|-----|
| **Task count** | 20 files | 9 files |
| **Numbering** | task-NNN.md | task_NNN.md / task_NNN.Y.md |
| **Location** | new_task_plan/task_files/ | tasks/ |
| **Format** | Minimal | TASK_STRUCTURE_STANDARD.md |
| **Scope** | Planning stage | Phase 3 implementation |
| **Status** | Deprecated | Active |

---

**Deprecation Date:** January 6, 2026  
**Replacement Standard:** TASK_STRUCTURE_STANDARD.md  
**Reference:** TASK_NUMBERING_DEPRECATION_PLAN.md (detailed analysis)  
**Current State:** PROJECT_STATE_PHASE_3_READY.md

---

**⚠️ DO NOT USE OLD TASK IDs IN NEW CODE OR DOCUMENTATION**

Use Phase 3 task numbers: 007, 075.1-5, 079-083 only.
