# Task 008.3: Integrate Backend-to-Src Migration Status Analysis

**Status:** pending
**Priority:** medium
**Effort:** 4-5 hours
**Complexity:** 6/10
**Dependencies:** 008.1, 008.2
**Created:** 2026-01-06
**Parent:** Task 008: Develop Feature Branch Identification and Categorization Tool

---

## Purpose

Analyze backend-to-src migration status for each feature branch.

---

## Details

Check migration progress and categorize branches by migration state.

### Steps

1. **Define migration criteria**
   - backend/ directory empty/removed
   - Files moved to src/
   - Import paths updated

2. **Analyze branch structure**
   ```python
   def check_migration_status(branch):
       result = subprocess.run(
           ["git", "ls-tree", "-r", "--name-only", branch],
           capture_output=True, text=True
       )
       files = result.stdout.strip().split('\n')
       
       has_backend = any(f.startswith('backend/') for f in files)
       has_src = any(f.startswith('src/') for f in files)
       
       # Determine status
       if has_backend and has_src:
           return "partial"
       elif has_backend:
           return "not_migrated"
       elif has_src:
           return "migrated"
       else:
           return "inconsistent"
   ```

3. **Categorize branches**

4. **Include in tool output**

---

## Success Criteria

- [ ] Migration status analyzed
- [ ] Branches categorized correctly
- [ ] Output includes migration field
- [ ] Statuses accurate

---

## Test Strategy

- Test branch with backend/ (not_migrated)
- Test branch with src/ only (migrated)
- Test branch with both (partial)
- Test mixed scenarios

---

## Implementation Notes

### Migration Analysis

```python
def analyze_migration_status(branch):
    """Analyze backend->src migration status."""
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", branch],
        capture_output=True, text=True
    )
    
    files = set(result.stdout.strip().split('\n'))
    
    # Check key indicators
    backend_files = [f for f in files if f.startswith('backend/')]
    src_files = [f for f in files if f.startswith('src/')]
    
    # Determine status
    if backend_files and not src_files:
        status = "not_migrated"
    elif src_files and not backend_files:
        status = "migrated"
    elif backend_files and src_files:
        status = "partial"
    else:
        status = "inconsistent"
    
    return {
        "status": status,
        "backend_count": len(backend_files),
        "src_count": len(src_files),
        "backend_files": backend_files[:5],  # First 5
    }
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Integration Checkpoint

**Task 008 Complete When:**
- [ ] All 3 subtasks complete
- [ ] Merge artifact detection working
- [ ] Content mismatch detection working
- [ ] Migration status analyzed
- [ ] Tool outputs complete categorization
