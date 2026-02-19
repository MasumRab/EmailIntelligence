# ⚠️ DEPRECATED: Old Task Numbering Systems (task-001 through task-020, task-075.x)

**Status:** ❌ DEPRECATED as of January 6, 2026
**Replacement:** TASK_STRUCTURE_STANDARD.md numbering
**Current Active Tasks:** 12 files (task_001.md, task_002.1-9.md, task_002-clustering.md, task_002.md)

---

## DO NOT USE THESE NUMBERING SYSTEMS

### ❌ DEPRECATED (Don't use)
```
task-001.md   task-002.md   task-003.md   ... task-020.md
task-001      task-002      task-003      ... task-020
task-075.md   task-075.1.md task-075.2.md ... task-075.9.md
new_task_plan/task_files/
```

### ✅ USE CURRENT SYSTEM INSTEAD
```
task_001.md              ← Branch Alignment Framework Definition
task_002.1.md - 002.9.md ← Branch Clustering System (Stage 1-3)
task_002-clustering.md   ← Implementation Guide for Clustering System
task_002.md              ← Consolidated Branch Clustering System Overview
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
| task-001 | Branch Alignment Framework | task_001.md | Active (enhanced) |
| task-075.1-9 | Branch Clustering System | task_002.1-9.md | Active (enhanced) |
| task-002 | Branch Clustering System | task_002.md | Active (consolidated) |
| task-003 | (Integrated into Task 002) | task_002.3.md | Active (integrated) |
| task-004 | (Integrated into Task 002) | task_002.4.md | Active (integrated) |
| task-005 | (Integrated into Task 002) | task_002.5.md | Active (integrated) |
| task-006 | (Integrated into Task 002) | task_002.6.md | Active (integrated) |
| task-007 | (Integrated into Task 002) | task_002.7.md | Active (integrated) |
| task-008 | (Integrated into Task 002) | task_002.8.md | Active (integrated) |
| task-009 | (Integrated into Task 002) | task_002.9.md | Active (integrated) |
| task-075.1 | CommitHistoryAnalyzer | task_002.1.md | Active (enhanced) |
| task-075.2 | CodebaseStructureAnalyzer | task_002.2.md | Active (enhanced) |
| task-075.3 | DiffDistanceCalculator | task_002.3.md | Active (enhanced) |
| task-075.4 | BranchClusterer | task_002.4.md | Active (enhanced) |
| task-075.5 | IntegrationTargetAssigner | task_002.5.md | Active (enhanced) |
| task-075.6 | PipelineIntegration | task_002.6.md | Active (enhanced) |
| task-075.7 | VisualizationReporting | task_002.7.md | Active (enhanced) |
| task-075.8 | TestingSuite | task_002.8.md | Active (enhanced) |
| task-075.9 | FrameworkIntegration | task_002.9.md | Active (enhanced) |

---

## Correct Task Structure (Current)

### Current active tasks:

```
Current: Branch Clustering & Alignment System

1. Task 001: Branch Alignment Strategy Framework
   └─ File: tasks/task_001.md
   └─ Scope: Define alignment strategy and decision criteria
   └─ Status: Enhanced, ready for implementation

2. Tasks 002.1-9: Branch Clustering System (Stage 1-3)
   ├─ task_002.1.md: CommitHistoryAnalyzer
   ├─ task_002.2.md: CodebaseStructureAnalyzer
   ├─ task_002.3.md: DiffDistanceCalculator
   ├─ task_002.4.md: BranchClusterer
   ├─ task_002.5.md: IntegrationTargetAssigner
   ├─ task_002.6.md: PipelineIntegration
   ├─ task_002.7.md: VisualizationReporting
   ├─ task_002.8.md: TestingSuite
   └─ task_002.9.md: FrameworkIntegration
   └─ Scope: Complete 3-stage clustering and alignment system
   └─ Status: Enhanced with 14-section standard, ready for implementation

3. Task 002: Consolidated Branch Clustering System Overview
   └─ File: tasks/task_002.md
   └─ Scope: Complete system overview and integration guide
   └─ Dependencies: Tasks 002.1-9
   └─ Status: Consolidated, ready for implementation
```

---

## Where to Find Current Tasks

```bash
# Correct location for current tasks
/home/masum/github/PR/.taskmaster/tasks/

# All 12 Branch Clustering System tasks
task_001.md
task_002.md
task_002.1.md
task_002.2.md
task_002.3.md
task_002.4.md
task_002.5.md
task_002.6.md
task_002.7.md
task_002.8.md
task_002.9.md
task_002-clustering.md
```

---

## What Happened to Old Files?

### Original Task 75 files (task-75.x.md)
- ❌ Migrated: task-75.1.md through task-75.9.md
- 🔄 Renamed to: task_002.1.md through task_002.9.md
- ✅ Enhanced: All content preserved and expanded with 14-section standard
- 📁 Location: Archived in task_data/migration_backup_20260129/ for reference

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
