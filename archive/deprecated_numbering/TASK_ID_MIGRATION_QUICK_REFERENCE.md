# Task ID Migration Quick Reference

**One-page cheat sheet for migrating from old to new task numbering**

---

## In Two Minutes

### OLD SYSTEM ❌ (Deprecated)
```
task-001, task-002, task-003, ... task-020
new_task_plan/task_files/
```

### NEW SYSTEM ✅ (Current)
```
task_007.md, task_075.1.md, task_075.2.md, ... task_083.md
tasks/ directory
```

---

## Old ID → New ID Mapping

| Old ID | Old Name | New ID | New Name | File | Status |
|--------|----------|--------|----------|------|--------|
| 001 | Framework Strategy | 007 | Branch Alignment Strategy | task_007.md | ✅ Active |
| 002 | Merge Validation | 079 | Orchestration | task_079.md | ✅ Active |
| 003 | Pre-merge Validation | 080 | Validation Integration | task_080.md | ✅ Active |
| 004 | Alignment Framework | 079 | Orchestration | task_079.md | ✅ Active |
| 005 | Error Detection | 083 | E2E Testing | task_083.md | ✅ Active |
| 006 | Backup/Restore | — | (Deferred) | — | ⏸️ Deferred |
| 007 | Feature ID Tool | 075.1-3 | Analyzers | task_075.1.md etc. | ✅ Active |
| 008 | Changes Summary | 083 | E2E Testing | task_083.md | ✅ Active |
| 009 | Post-alignment | 083 | E2E Testing | task_083.md | ✅ Active |
| 010-020 | Various | — | (Deferred) | — | ⏸️ Deferred |

---

## Current Phase 3 Tasks (9 Total)

```
✅ task_007.md
   └─ Branch Alignment Strategy Framework (40-48 hrs)

✅ task_075.1.md - task_075.5.md
   ├─ CommitHistoryAnalyzer (24-32 hrs)
   ├─ CodebaseStructureAnalyzer (24-32 hrs)
   ├─ DiffDistanceCalculator (20-28 hrs)
   ├─ BranchClusterer (20-28 hrs)
   └─ IntegrationTargetAssigner (20-28 hrs)

✅ task_079.md
   └─ Parallel Alignment Orchestration (24-32 hrs)

✅ task_080.md
   └─ Validation Integration (20-28 hrs)

✅ task_083.md
   └─ E2E Testing & Reporting (28-36 hrs)
```

---

## Location Reference

| What | Old | New |
|------|-----|-----|
| Task files | `new_task_plan/task_files/` ❌ | `tasks/` ✅ |
| Current state | `PROJECT_REFERENCE.md` ❌ | `PROJECT_STATE_PHASE_3_READY.md` ✅ |
| Task format | Custom | `TASK_STRUCTURE_STANDARD.md` ✅ |
| Template | None | `TASK_STRUCTURE_STANDARD.md` ✅ |

---

## If You See...

### ❌ Wrong References
```
"Per task-002 clustering..."
"See new_task_plan/task_files/task-003.md"
"Based on task-007 feature ID tool..."
```

### ✅ Right References
```
"Per task_079 orchestration framework..."
"See tasks/task_080.md for validation..."
"Based on task_075.1-3 analyzers..."
```

---

## Before You Start Phase 3 Implementation

✅ Know current task IDs: 007, 075.1-5, 079-083  
✅ Know current location: `tasks/` directory  
✅ Know current format: TASK_STRUCTURE_STANDARD.md  
✅ Know current state: PROJECT_STATE_PHASE_3_READY.md  
✅ Know what's deferred: Tasks 006, 010-020 (not Phase 3)  
✅ Don't reference: task-001 through task-020  

---

## Questions

**Q: What's task_075.1 vs task-007 (old)?**  
A: Different tasks. task-007 was old "Feature ID Tool", now task_075.1 is "CommitHistoryAnalyzer". They're related but not identical.

**Q: Can I use old task files?**  
A: No. Old files deleted. Use current tasks in `/tasks/` directory.

**Q: Are old tasks still available?**  
A: In git history only. For current work, use new tasks.

**Q: Why the change?**  
A: Project scope narrowed from 20 planning tasks to 9 Phase 3 implementation tasks.

---

## Key Files

| File | Purpose | Status |
|------|---------|--------|
| OLD_TASK_NUMBERING_DEPRECATED.md | Why old system is gone | 📖 Read this first |
| TASK_NUMBERING_DEPRECATION_PLAN.md | Full deprecation details | 📖 Full reference |
| PROJECT_STATE_PHASE_3_READY.md | Current project status | 📖 Current truth |
| TASK_STRUCTURE_STANDARD.md | Task template | 📖 All tasks follow this |
| tasks/task_007.md etc. | Current active tasks | 🔧 Implement these |

---

**Print this and post it.** Share with team before Phase 3 implementation begins.

**Last Updated:** January 6, 2026  
**Status:** Active - Current task numbering reference
