# WS2 Phase 3: System Updates & Final Validation

**Date:** January 4, 2026  
**Status:** Planned for after Phase 2  
**Estimated Effort:** 1-2 hours  

---

## Overview

Phase 3 completes the renumbering by updating system configuration files and validating end-to-end integration.

---

## Tasks

### Phase 3.1: tasks.json Update (if applicable)

**File:** `.taskmaster/tasks/tasks.json`

**Changes:**
- Check if Task 021 referenced in JSON
- Update IDs if needed (unlikely - should reference Task 002, etc.)
- Validate JSON syntax

**Validation:**
```bash
python3 -m json.tool .taskmaster/tasks/tasks.json > /dev/null
```

### Phase 3.2: Import Path Verification

**Scope:** Check for any hardcoded file paths

**Commands:**
```bash
grep -r "TASK-021" . --exclude-dir=.backups --exclude-dir=.git
grep -r "task-021" . --exclude-dir=.backups --exclude-dir=.git
grep -r "Task-021" . --exclude-dir=.backups --exclude-dir=.git
# All should return zero results
```

### Phase 3.3: Configuration File Updates

Check if config.json or other system config files reference Task 021 paths:

```bash
grep -l "021" config.json .taskmaster/config.json 2>/dev/null
```

### Phase 3.4: Cross-Reference Validation

Verify all cross-references between updated files still work:

```bash
# Check for any remaining broken references
grep -r "TASK-021" . 2>/dev/null | grep -v ".backups" | grep -v ".git"
# Should return 0 results
```

---

## Comprehensive Final Validation

### Validation Checklist

- [ ] No "Task 021" references in active project (only in WS2 docs)
- [ ] All "Task 002" references properly updated (340+)
- [ ] All cascading task numbers consistent (022→023, etc.)
- [ ] File renames completed (Phase 2)
- [ ] No broken import paths
- [ ] No broken cross-references
- [ ] JSON files all valid
- [ ] Markdown files all renderable
- [ ] Git tracking clean
- [ ] All backups preserved

### Validation Commands

```bash
# 1. Final Task 021 check (should be 0 outside WS2 docs)
grep -r "Task 021" . 2>/dev/null | grep -v ".backups" | grep -v ".git" | grep -v "WS2-PHASE" | wc -l

# 2. Task 002 verification (should be 340+)
grep -r "Task 002" . 2>/dev/null | grep -v ".backups" | grep -v ".git" | wc -l

# 3. JSON validation
for f in .taskmaster/config.json .taskmaster/tasks/tasks.json state.json; do
  if [ -f "$f" ]; then
    python3 -m json.tool "$f" > /dev/null && echo "✓ $f" || echo "✗ $f"
  fi
done

# 4. No broken file references
grep -r "TASK-021" . 2>/dev/null | grep -v ".backups" | grep -v ".git"

# 5. Git status
git status
```

---

## Summary Statistics

**Phase 1 Results:**
- Documents updated: 24+
- Task 021 references eliminated: 300
- Task 002 references added: 342
- Backup files created: 67

**Phase 2 Results:**
- Files renamed: 2
- Git history preserved: Yes

**Phase 3 Results:**
- System configs updated: TBD
- Final validation: TBD
- End-to-end integration: TBD

---

## Success Criteria

When Phase 3 complete:

✅ Zero Task 021 references in active project  
✅ All Task 002 references verified  
✅ All cascading task numbers consistent  
✅ All system files updated  
✅ All import paths valid  
✅ All cross-references functional  
✅ 100% JSON validation pass  
✅ Full audit trail via backups  
✅ Ready for production deployment  

---

## Git Commit Strategy

After Phase 3 validation complete:

```bash
# Staged: All Phase 1-3 changes
git add .

# Commit: Document complete refactoring
git commit -m "refactor: complete Task 021→002 renumbering (WS2 Phases 1-3)

- Phase 1: Update all documentation (24 files)
- Phase 2: Rename Task-021 files to Task-002
- Phase 3: System updates and final validation

Task 021 (Branch Clustering) now Task 002
Task 022 → Task 023 through Task 026 → Task 027
All 342 Task 002 references verified
Zero broken references remaining
Full backup trail preserved in .backups/"

# Verify commit
git log -1
```

---

## Rollback Safety

If issues found during Phase 3:

**Option A: Partial Rollback**
```bash
# Revert just Phase 3 changes
git reset --soft HEAD~1
# Fix issues
# Re-commit
```

**Option B: Full Rollback**
```bash
# Restore everything from Phase 1 backups
for file in .backups/*.TIMESTAMP; do
  cp "$file" "${file%.TIMESTAMP}"
done
```

---

## Timeline

- **Phase 1 Complete:** ✅ Documentation updates done
- **Phase 2 Ready:** File renames pending (30 min)
- **Phase 3 Ready:** System updates pending (1-2 hours)
- **Total WS2 Duration:** ~3-4 hours (comprehensive, safe renumbering)

---

## Next Steps

1. Execute Phase 2 (file renames)
2. Validate Phase 2 output
3. Execute Phase 3 (system updates)
4. Run comprehensive final validation
5. Git commit all changes
6. Complete WS2 renumbering project

---

**Phase 3 Status:** Ready for execution after Phase 2  
**Blocks:** Nothing (final phase)  
**Risk Level:** LOW (comprehensive validation reduces risk)
