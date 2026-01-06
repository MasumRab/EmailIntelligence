# Phase 7: Consolidation Cleanup Plan

**Status:** Ready to Execute (On Hold - 2 Week Verification Period)  
**Date:** January 6, 2026  
**Purpose:** Remove abandoned files after consolidation verified

---

## Cleanup Items (Priority Order)

### Priority 1: Immediate (Safe to Delete Anytime)
These files are definitely no longer needed.

#### Old Planning Files in new_task_plan/task_files/
```
task-001.md through task-026.md (26 files)
task-002-clustering.md (1 file)

Reason: Created Jan 4 during renumbering, superseded by Phase 3 tasks
Action: Already committed to delete in git (as part of consolidation)
Risk: LOW - These are purely planning-stage files, never referenced
Delete: YES - Can delete immediately
```

#### Orphaned task_data/ Folder (Phase 2 Old System)
```
task_data/task-75.md
task_data/task-75.1.md through task-75.9.md
task_data/[other files] (37 total)

Reason: Old task-75 format, never migrated, now task_075.1-5.md in /tasks/
Action: Move to archive with manifest
Risk: LOW - These are completely orphaned, referenced nowhere
Delete: After archival - Move to archive/deprecated_old_numbering/
```

### Priority 2: Conditional (Check References First)
These files exist but need verification before deletion.

#### /tasks/ Folder (Current System - 114 files)
```
tasks/task_*.md (all files)

Status: Now deprecated, kept as backup during 2-week verification period
Reason: Contains original Phase 3 task files as backup

Decision Framework:
1. ✅ If all references point to new_task_plan/task_files/ (YES)
2. ✅ If new_task_plan versions are complete and working (YES)
3. ⏳ After 2-week verification period with teams using new location
4. Then: Can delete /tasks/ OR keep as read-only archive

Timeline: Delete in Phase 7, Execution 2 weeks from now (~Jan 20)
Risk: MEDIUM - Some old documentation might have hardcoded /tasks/ paths
Action: One more comprehensive scan before final deletion
```

---

## Detailed Cleanup Steps

### Step 1: Archive Old Planning Files (task-001-026)

**Current Status:** 26 files in `new_task_plan/task_files/`

```bash
# Move to archive
mkdir -p archive/deprecated_old_numbering/
mv new_task_plan/task_files/task-00{1..9}.md archive/deprecated_old_numbering/
mv new_task_plan/task_files/task-0{1..2}{0..9}.md archive/deprecated_old_numbering/
mv new_task_plan/task_files/task-002-clustering.md archive/deprecated_old_numbering/

# Verify move
ls -1 archive/deprecated_old_numbering/ | wc -l
# Should output: 27 (26 files + task-002-clustering)
```

**Verification:**
- [ ] All 26+ files moved to archive
- [ ] No task-*.md files remain in new_task_plan/task_files/ (except task_*.md with underscores)
- [ ] Confirm new_task_plan/task_files/ has only 11 files:
  - task_007.md
  - task_075.1-5.md (5 files)
  - task_079.md, task_080.md, task_083.md (3 files)
  - INDEX.md, DEFERRED_TASKS.md (2 index files)

### Step 2: Archive Orphaned task_data/ Folder

**Current Status:** 37 files in task_data/

```bash
# Check what's in task_data
ls -1 task_data/ | head -20

# Move entire folder to archive
mkdir -p archive/orphaned_task_data/
mv task_data/* archive/orphaned_task_data/

# Create manifest
cat > archive/orphaned_task_data/README.md << 'EOF'
# Orphaned task_data/ Files

**Status:** Archived from active system  
**Date:** January 6, 2026  
**Reason:** Never migrated to current task system

These files were part of the old Task 75 structure (task-75.*.md format) 
that was superseded by the Phase 3 task system (task_075.*.md format).

All Task 75 functionality is now in:
- new_task_plan/task_files/task_075.1.md through task_075.5.md

These archived files are kept for historical reference only.
EOF

# Verify
ls -1 archive/orphaned_task_data/ | wc -l
# Should output: 37
```

**Verification:**
- [ ] All files moved from task_data/ to archive/orphaned_task_data/
- [ ] Archive/orphaned_task_data/README.md created with context
- [ ] task_data/ directory is now empty (can be removed)

### Step 3: Decision Point - Remove /tasks/ Folder (DEFERRED)

**Timeline:** Defer for 2 weeks (verify no regressions first)

```
Current Status:
- /tasks/ contains 114 files (now deprecated)
- new_task_plan/task_files/ contains 11 files (new system)
- All references updated to point to new location

Wait Period:
- Let teams use new location for 2 weeks
- Monitor for any issues or broken references
- Confirm no dependencies on /tasks/ remain

Decision (Jan 20, 2026):
- Option A: Delete /tasks/ entirely (complete cleanup)
- Option B: Archive as read-only backup (safety margin)
- Option C: Keep as mirror for transition period

Recommendation: Option A after verification complete
```

### Step 4: Final Verification Script

```bash
#!/bin/bash
# PHASE_7_CLEANUP_VERIFICATION.sh

echo "=== Phase 7 Cleanup Verification ==="
echo ""

# Check new_task_plan has exactly 11 files
count=$(ls -1 new_task_plan/task_files/ | wc -l)
echo "Files in new_task_plan/task_files/: $count (expected: 11)"
[ "$count" -eq 11 ] && echo "✓ PASS" || echo "✗ FAIL"
echo ""

# Check no task-* (hyphen format) in new_task_plan except cluster file
hyphen_count=$(ls -1 new_task_plan/task_files/task-*.md 2>/dev/null | wc -l)
echo "Hyphenated files in new_task_plan/task_files/: $hyphen_count (expected: 0)"
[ "$hyphen_count" -eq 0 ] && echo "✓ PASS" || echo "✗ FAIL - Manual cleanup needed"
echo ""

# Check archive has old files
archive_count=$(ls -1 archive/deprecated_old_numbering/ 2>/dev/null | wc -l)
echo "Archived planning files: $archive_count (expected: 27)"
[ "$archive_count" -eq 27 ] && echo "✓ PASS" || echo "⚠️  CHECK - Some files missing"
echo ""

# Check task_data is empty or archived
remaining=$(ls -1 task_data/ 2>/dev/null | wc -l)
echo "Files remaining in task_data/: $remaining (expected: 0)"
[ "$remaining" -eq 0 ] && echo "✓ PASS" || echo "⚠️  CHECK - Some files not archived"
echo ""

# Final documentation scan for /tasks/ references
refs=$(grep -r "tasks/task_" --include="*.md" . 2>/dev/null | grep -v "archive" | grep -v "new_task_plan" | grep -v "DEPRECATION_NOTICE" | wc -l)
echo "Remaining /tasks/ references in active docs: $refs (expected: 0)"
[ "$refs" -eq 0 ] && echo "✓ PASS" || echo "⚠️  WARNING - Some references remain"
```

---

## Execution Steps

### When Ready (After 2-Week Verification)

```bash
# 1. Run verification
bash PHASE_7_CLEANUP_VERIFICATION.sh

# 2. Archive old planning files
mkdir -p archive/deprecated_old_numbering/
mv new_task_plan/task_files/task-*.md archive/deprecated_old_numbering/

# 3. Archive task_data
mkdir -p archive/orphaned_task_data/
mv task_data/* archive/orphaned_task_data/
# (optionally delete empty task_data/ directory)

# 4. Create/update manifests
# See manifests section below

# 5. Verify cleanup
bash PHASE_7_CLEANUP_VERIFICATION.sh

# 6. Commit cleanup work
git add archive/
git commit -m "feat: complete consolidation phase 7 - archive old files and cleanup

- Archive 26 old planning files (task-001-026) to archive/deprecated_old_numbering/
- Archive 37 orphaned task_data files to archive/orphaned_task_data/
- Create manifests explaining what was archived and why
- Verify new_task_plan/task_files/ contains only 11 Phase 3 task files
- Confirm all documentation references point to new location

Final Status: Consolidation complete (7/7 phases)
- Single source of truth established: new_task_plan/task_files/
- Old systems archived and documented
- Team references updated
- No active code depends on deprecated /tasks/ location
"

# 7. Optional: Remove /tasks/ or archive it
# Decision: TBD after 2-week verification period
```

---

## Archive Manifests

### archive/deprecated_old_numbering/README.md

```markdown
# Deprecated Old Numbering System

**Date Archived:** January 6, 2026  
**Source:** new_task_plan/task_files/ (from Jan 4 renumbering work)  
**Reason:** Superseded by Phase 3 task system

**Contents:** 27 files
- task-001.md through task-026.md (26 planning files)
- task-002-clustering.md (duplicate/variant)

**Rationale:** These files were created during Task 021→002 renumbering on Jan 4.
They were not deleted when the Phase 3 system (task_007, task_075.1-5, task_079-083) 
became active. They represent planning-stage work that has been superseded by the 
final Phase 3 task specifications.

**Historical Value:** Shows evolution from original task numbering to Phase 3 structure.
Can be referenced for historical context but should not be used for active work.

**Current Active System:** new_task_plan/task_files/ (11 Phase 3 task files)
```

### archive/orphaned_task_data/README.md

```markdown
# Orphaned task_data/ Files

**Date Archived:** January 6, 2026  
**Source:** task_data/ (old Task 75 implementation)  
**Reason:** Never migrated to current task system

**Contents:** 37 files
- task-75.md, task-75.1.md through task-75.9.md (10 Task 75 files)
- [27 other files]

**Rationale:** These files used the old hyphenated naming convention (task-XX.md) 
and were never migrated to the current underscore format (task_XX.md). They represent 
Task 75 work from an earlier implementation that was superseded by the Phase 3 
BranchClusterer system.

**What Replaced This:**
- Task 075.1: CommitHistoryAnalyzer → new_task_plan/task_files/task_075.1.md
- Task 075.2: CodebaseStructureAnalyzer → new_task_plan/task_files/task_075.2.md
- Task 075.3: DiffDistanceCalculator → new_task_plan/task_files/task_075.3.md
- Task 075.4: BranchClusterer → new_task_plan/task_files/task_075.4.md
- Task 075.5: IntegrationTargetAssigner → new_task_plan/task_files/task_075.5.md

**Historical Value:** Shows implementation evolution and patterns; documents what was tried.
Should not be used for active development.

**Current Active System:** new_task_plan/task_files/ (Phase 3 tasks with underscore naming)
```

---

## Verification Checklist

Before committing Phase 7 cleanup:

- [ ] new_task_plan/task_files/ contains exactly 11 files
  - [ ] task_007.md
  - [ ] task_075.1.md, task_075.2.md, task_075.3.md, task_075.4.md, task_075.5.md
  - [ ] task_079.md, task_080.md, task_083.md
  - [ ] INDEX.md, DEFERRED_TASKS.md

- [ ] No task-*.md (hyphen) files in new_task_plan/task_files/

- [ ] archive/deprecated_old_numbering/ contains 26+ files
  - [ ] task-001.md through task-026.md
  - [ ] task-002-clustering.md
  - [ ] README.md explaining context

- [ ] archive/orphaned_task_data/ contains 37 files
  - [ ] task-75.*.md files
  - [ ] README.md explaining context

- [ ] task_data/ is empty (or deleted)

- [ ] All documentation references point to new_task_plan/task_files/

- [ ] /tasks/ folder marked with DEPRECATION_NOTICE.md

- [ ] Commit includes complete Phase 7 summary

---

## Timeline

| Event | Date |
|-------|------|
| Consolidation started | Jan 6, 13:12 |
| Phases 1-6 complete | Jan 6, 15:30 |
| **2-week verification period** | Jan 6 - Jan 20 |
| Phase 7 cleanup execution | Jan 20+ |
| Project cleanup verified | Jan 21+ |

---

## Notes

- Phase 7 is on hold pending 2-week verification period
- Current state is safe (no data loss, everything backed up)
- All active work can proceed using new_task_plan/task_files/
- /tasks/ remains available as safety fallback during transition
- Old files archived with full context for historical reference

---

**Prepared By:** Consolidation Process  
**Date:** January 6, 2026, 15:35  
**Next Action:** Execute Phase 7 on Jan 20+ after verification complete
