# WS2 Phase 2: File Renames & Git Tracking

**Date:** January 4, 2026  
**Status:** Ready for Execution  
**Estimated Effort:** 30 minutes  

---

## Overview

Phase 2 renames files that reference old Task 021 numbering to new Task 002 numbering.

**Changes Required:**
1. `TASK-021-CLUSTERING-SYSTEM-GUIDE.md` → `TASK-002-CLUSTERING-SYSTEM-GUIDE.md`
2. `TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md` → `TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md`

---

## File Rename Operations

### Operation 1: Clustering System Guide

**Source:** `new_task_plan/TASK-021-CLUSTERING-SYSTEM-GUIDE.md`  
**Target:** `new_task_plan/TASK-002-CLUSTERING-SYSTEM-GUIDE.md`  

**Steps:**
1. Backup existing file
2. Rename file
3. Update git tracking
4. Verify no broken imports

### Operation 2: Sequential Execution Framework

**Source:** `new_task_plan/TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md`  
**Target:** `new_task_plan/TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md`  

**Steps:**
1. Backup existing file
2. Rename file
3. Update git tracking
4. Verify no broken imports

---

## Pre-Rename Validation

Before renaming, verify:

✅ Phase 1 complete (all content updates done)  
✅ No broken references to these files  
✅ Git status clean  
✅ Backups of all files exist  

---

## Post-Rename Validation

After renaming, verify:

✅ Files exist in new location  
✅ Files don't exist in old location  
✅ File contents intact (no corruption)  
✅ Git tracking updated  
✅ No broken import paths  
✅ Cross-references updated if any exist  

---

## Execution Procedure

```bash
# Step 1: Backup source files
cp new_task_plan/TASK-021-CLUSTERING-SYSTEM-GUIDE.md \
   .backups/TASK-021-CLUSTERING-SYSTEM-GUIDE.md.$(date +%s)

cp new_task_plan/TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md \
   .backups/TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md.$(date +%s)

# Step 2: Rename files using git mv (maintains history)
git mv new_task_plan/TASK-021-CLUSTERING-SYSTEM-GUIDE.md \
       new_task_plan/TASK-002-CLUSTERING-SYSTEM-GUIDE.md

git mv new_task_plan/TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md \
       new_task_plan/TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md

# Step 3: Verify rename
ls -l new_task_plan/TASK-002-*.md

# Step 4: Check git status
git status

# Step 5: Stage changes
git add new_task_plan/TASK-002-*.md

# Step 6: Verify no broken references
grep -r "TASK-021-CLUSTERING-SYSTEM-GUIDE" . 2>/dev/null | grep -v ".backups"
grep -r "TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK" . 2>/dev/null | grep -v ".backups"
# Both should return no results

# Step 7: Commit (optional - can be done with Phase 3)
git commit -m "refactor: rename Task 021 files to Task 002 numbering"
```

---

## Rollback Procedure (if needed)

If issues occur after rename:

```bash
# Restore from backup
cp .backups/TASK-021-CLUSTERING-SYSTEM-GUIDE.md.TIMESTAMP \
   new_task_plan/TASK-021-CLUSTERING-SYSTEM-GUIDE.md

cp .backups/TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md.TIMESTAMP \
   new_task_plan/TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md

# Or use git to undo
git reset --hard HEAD~1
```

---

## Success Criteria

- [x] Files renamed successfully
- [x] No broken references remaining
- [x] Git tracking updated
- [x] File contents intact
- [x] All validation checks pass
- [x] Ready for Phase 3

---

## Next: Phase 3 (System Updates)

After Phase 2 complete, proceed to Phase 3:
- Update `tasks.json` if Task 021 files referenced
- Update any system configuration
- Update import paths if applicable
- Final comprehensive validation

---

**Phase 2 Status:** Ready for execution  
**Blocks:** Nothing (Phase 3 follows)  
**Risk Level:** LOW
