# Branches to NEVER Merge Into orchestration-tools or scientific

**Status:** ⚠️ Critical Reference Document  
**Date:** January 6, 2026

---

## Quick Reference: DO NOT MERGE THESE

### ❌ TASKMASTER BRANCHES (5 total)
```
feature/taskmaster-protection
taskmaster
remotes/origin/feature/taskmaster-protection
remotes/origin/taskmaster
remotes/origin/users/masum/*taskmaster*
```
**Reason:** Contains .taskmaster/ setup code (not alignment-related)

---

### ❌ BOLT-OPTIMIZATION BRANCHES (52+ total)
```
remotes/origin/bolt-*
  (all 52+ branches starting with "bolt-")
```
**Reason:** Auto-generated optimization experiments, untested, bloatware

---

### ❌ ORCHESTRATION-TOOLS VARIANTS (14 total)
```
orchestration-tools-changes*
orchestration-tools-consolidated*
orchestration-tools-launch-refractor
```
**Reason:** Old abandoned variants with conflicts

---

### ❌ TASK EXECUTION BRANCHES (17 total)
```
001-*
002-*
003-*
```
**Reason:** Old task/execution attempts, superseded, conflicting

---

### ❌ EXPERIMENTAL/FEATURE BRANCHES (80+ total)
```
align-feature-notmuch-tagging-*
backend-refactor
clean-launch-refactor
docs/comprehensive-documentation
feature/backend-to-src-migration
feature/documentation-merge
feature-notmuch-tagging-*
migration-completion-branch
sourcery-ai-fixes-main*
```
**Reason:** Experimental code, out-of-scope for alignment

---

### ❌ GITBUTLER WORKSPACE (1 total)
```
gitbutler/workspace
```
**Reason:** IDE-specific workspace file, not actual code

---

### ❌ ARCHIVE/BACKUP/REMOTE BRANCHES (100+ total)
```
remotes/origin/archive/*
remotes/origin/backup/*
remotes/origin/users/masum/*
[and 100+ other remote branches]
```
**Reason:** Explicitly non-production, historical only

---

## ✅ BRANCHES THAT ARE SAFE (3 total)

```
✅ main                    - Production code (stable)
✅ orchestration-tools     - Alignment framework (Phase 3, active)
✅ scientific              - Pre-production testing
```

---

## Safe Merge Direction

```
orchestration-tools (Phase 3)
         ↓
      scientific (testing)
         ↓
        main (production)
```

**Everything else branches SHOULD BE DELETED, never merged.**

---

## Summary

| Category | Count | Action |
|----------|-------|--------|
| Taskmaster | 5 | DELETE |
| Bolt-optimization | 52+ | DELETE |
| Orchestration variants | 14 | DELETE |
| Task execution | 17 | DELETE |
| Experimental features | 80+ | DELETE |
| Archive/backup/remotes | 100+ | DELETE |
| Gitbutler workspace | 1 | DELETE |
| **SAFE TO USE** | **3** | **KEEP** |
| **TOTAL TO DELETE** | **275** | **DELETE ASAP** |

---

## Before Merging Anything

**ALWAYS CHECK:**
```bash
# 1. What branch are you on?
git branch

# 2. Is it one of the 3 safe branches?
# (main, orchestration-tools, scientific)
# YES? OK to proceed
# NO? STOP and delete it instead

# 3. Before merging, verify:
git log --oneline -20
git diff <target-branch>..<current-branch> | head -100

# 4. If you see files that shouldn't be merged:
# taskmaster-* files, bolt-* changes, experimental code
# ABORT MERGE - wrong branch!
```

---

## Critical Safety Rules

1. ❌ NEVER merge taskmaster-* into orchestration-tools
2. ❌ NEVER merge bolt-* into orchestration-tools
3. ❌ NEVER merge orchestration-tools-changes into orchestration-tools
4. ❌ NEVER merge 001/002/003 branches
5. ❌ NEVER merge experimental feature branches
6. ❌ NEVER merge from remotes/origin/* directly

---

**Reference:** Full analysis in BRANCH_ANALYSIS_AND_CLEANUP_RECOMMENDATIONS.md
