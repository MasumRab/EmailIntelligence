# Dependency Corruption Fix Implementation Plan

**Status**: READY FOR EXECUTION  
**Scope**: Fix 25/28 corrupted task dependencies in `.taskmaster/tasks/tasks.json`  
**Effort**: 4-6 hours (methodical, reversible process)  
**Backups**: `.taskmaster/tasks/option_c_backup/` contains safe copy

---

## Problem Summary

### Current State
- **28 tasks total**
- **25/28 with corrupted dependencies** (89%)
- **Corruption types**:
  1. Self-references (task 001 → "001")
  2. Invalid IDs ("2026", "095", "000")
  3. Duplicate entries ("002", "002", "002")
  4. Non-existent IDs (task 001 depends on "105" which doesn't exist)
  5. Potential circular chains (task A → B → A)

### Impact
- Cannot expand tasks with `task-master expand`
- Cannot analyze critical path or prioritize work
- Cannot build reliable project timeline
- Task Master validation likely failing

### Why This Happened
Option C restructuring (+3 offset) updated task IDs but dependency lists were:
- Partially updated (some IDs in deps not found in source task)
- Duplicated (same ID listed multiple times)
- Left with invalid references (copy-paste errors)

---

## Phase 1: Audit & Mapping (1-2 hours)

### Step 1.1: Extract Current Dependency Graph
```bash
# Create audit script to find all corruption
python3 << 'EOF'
import json

with open('.taskmaster/tasks/tasks.json', 'r') as f:
    tasks = json.load(f)

print("=== DEPENDENCY CORRUPTION AUDIT ===\n")

valid_ids = set(t['id'] for t in tasks)
issues = {}

for task in tasks:
    task_id = task['id']
    deps = task.get('dependencies', [])
    
    if not deps:
        print(f"Task {task_id}: No dependencies ✓")
        continue
    
    issues[task_id] = {
        'self_refs': [],
        'invalid_ids': [],
        'duplicates': [],
        'total_deps': len(deps)
    }
    
    # Check for self-reference
    if task_id in deps:
        issues[task_id]['self_refs'].append(task_id)
    
    # Check for invalid IDs
    for dep in deps:
        if dep not in valid_ids and dep != task_id:
            issues[task_id]['invalid_ids'].append(dep)
    
    # Check for duplicates
    if len(deps) != len(set(deps)):
        issues[task_id]['duplicates'] = [d for d in deps if deps.count(d) > 1]
    
    if any([issues[task_id]['self_refs'], issues[task_id]['invalid_ids'], issues[task_id]['duplicates']]):
        print(f"Task {task_id}: CORRUPTED")
        if issues[task_id]['self_refs']:
            print(f"  - Self-references: {issues[task_id]['self_refs']}")
        if issues[task_id]['invalid_ids']:
            print(f"  - Invalid IDs: {issues[task_id]['invalid_ids']}")
        if issues[task_id]['duplicates']:
            print(f"  - Duplicates: {issues[task_id]['duplicates']}")

print(f"\n=== SUMMARY ===")
corrupted_count = len([k for k in issues if issues[k]['self_refs'] or issues[k]['invalid_ids'] or issues[k]['duplicates']])
print(f"Total corrupted tasks: {corrupted_count}/28")
EOF
```

### Step 1.2: Document Findings
Create `DEPENDENCY_AUDIT_RESULTS.json`:
```json
{
  "audit_date": "2026-01-29",
  "total_tasks": 28,
  "corrupted_tasks": 25,
  "corruption_by_type": {
    "self_references": ["001", "002", ...],
    "invalid_ids": {"001": ["105", "2026"], ...},
    "duplicates": {"005": ["002", "002"], ...},
    "valid_ids_in_system": ["001", "002", ..., "028"]
  }
}
```

---

## Phase 2: Decision Rules (30 mins - 1 hour)

### Decision Framework: What should Task X depend on?

Before fixing, establish rules:

#### Rule 1: Keep only within-epic dependencies (for separate project)
- Task 002 (Epic A) can depend on other 002.* subtasks or 001
- Task 003 (Epic B) can depend on 002.* completing + 003.* subtasks
- Task 004 (Epic C) can depend on 003.* completing + 004.* subtasks

#### Rule 2: If Tasks 005-028 are being eliminated
- Remove ALL dependencies on Tasks 005-028
- Remove ANY task from Tasks 005-028 that depends on 002-004 (they should not depend on core)

#### Rule 3: Self-references are always wrong
- Delete any dependency where task ID equals dependency ID
- Pattern: `"dependencies": ["001"]` in task 001 → DELETE

#### Rule 4: Invalid IDs are always wrong
- Delete any dependency with non-existent task ID
- Examples to delete: "2026", "095", "000", "105" (if 105 doesn't exist)

#### Rule 5: No duplicates
- If `"dependencies": ["002", "002", "003"]` → normalize to `["002", "003"]`

#### Rule 6: Limit dependencies
- Max 3 dependencies per task
- If task has >3, use judgment: keep only direct blockers, remove transitive ones

---

## Phase 3: Manual Review & Correction (2-3 hours)

### Step 3.1: Review Tasks 002-004 (Core separate project)

**Task 002 (Email Ingest + Normalize)**
Current dependencies:
```
[from audit]
```

**Question**: Should 002 depend on anything?
- **Answer**: Only 001 (if 001 is meta/setup). Otherwise: empty list.
- **Fix**: `"dependencies": []` OR `"dependencies": ["001"]` if 001 exists and makes sense

**Task 003 (Intelligence)**
Current dependencies:
```
[from audit]
```

**Question**: What must complete before 003 starts?
- **Answer**: 002 must be done (email ingest working). Maybe 001.
- **Fix**: `"dependencies": ["002"]` at most

**Task 004 (Presentation)**
Current dependencies:
```
[from audit]
```

**Question**: What must complete before 004 starts?
- **Answer**: 003 (intelligence results exist to present). Maybe 002 (schema understanding).
- **Fix**: `"dependencies": ["003"]` at most

### Step 3.2: Review Tasks 005-028 (TBD Elimination)

**Decision Gate**: Are Tasks 005-028 staying or going?
- **If GOING**: Set all to `"dependencies": []` (remove them cleanly)
- **If STAYING**: Review each against rules 1-6 above

**For each task in 005-028**:
```
1. List current dependencies
2. Check each dependency ID exists in valid_ids
3. Check for self-references
4. Check for duplicates
5. If any issue → delete that dependency
6. Keep only task IDs that actually exist
```

### Step 3.3: Build Corrected Dependency Map

Create `DEPENDENCY_CORRECTIONS.json`:
```json
{
  "corrections": [
    {
      "task_id": "001",
      "old_dependencies": ["001", "002"],
      "new_dependencies": [],
      "reason": "Removed self-reference. Task 001 should have no dependencies (entry point)."
    },
    {
      "task_id": "002",
      "old_dependencies": ["001", "001", "095"],
      "new_dependencies": ["001"],
      "reason": "Removed duplicate '001' and invalid '095'. Kept only '001' as entry dependency."
    },
    {
      "task_id": "003",
      "old_dependencies": ["002", "2026"],
      "new_dependencies": ["002"],
      "reason": "Removed invalid '2026'. Kept '002' as it's the ingest task that must complete first."
    }
    // ... repeat for all 28 tasks
  ],
  "summary": {
    "self_refs_removed": 5,
    "invalid_ids_removed": 20,
    "duplicates_removed": 15,
    "tasks_unchanged": 3
  }
}
```

---

## Phase 4: Automated Fix (30 mins - 1 hour)

### Step 4.1: Apply Corrections to tasks.json

```python
# apply_dependency_fixes.py
import json

# Load corrections map
with open('DEPENDENCY_CORRECTIONS.json', 'r') as f:
    corrections = json.load(f)['corrections']

# Load tasks
with open('.taskmaster/tasks/tasks.json', 'r') as f:
    tasks = json.load(f)

# Create correction lookup
correction_map = {c['task_id']: c['new_dependencies'] for c in corrections}

# Apply fixes
for task in tasks:
    if task['id'] in correction_map:
        task['dependencies'] = correction_map[task['id']]

# Save corrected version
with open('.taskmaster/tasks/tasks.json', 'w') as f:
    json.dump(tasks, f, indent=2)

print("✓ Applied all dependency corrections")
print(f"✓ Fixed {len(correction_map)} tasks")
```

### Step 4.2: Validate Corrected tasks.json

```bash
python3 << 'EOF'
import json

with open('.taskmaster/tasks/tasks.json', 'r') as f:
    tasks = json.load(f)

valid_ids = {t['id'] for t in tasks}
errors = []

for task in tasks:
    task_id = task['id']
    deps = task.get('dependencies', [])
    
    # Check for self-references
    if task_id in deps:
        errors.append(f"Task {task_id}: Self-reference detected")
    
    # Check for invalid IDs
    for dep in deps:
        if dep not in valid_ids:
            errors.append(f"Task {task_id}: Invalid dependency '{dep}'")
    
    # Check for duplicates
    if len(deps) != len(set(deps)):
        errors.append(f"Task {task_id}: Duplicate dependencies")
    
    # Check for too many dependencies
    if len(deps) > 3:
        errors.append(f"Task {task_id}: Too many dependencies ({len(deps)} > 3)")

if errors:
    print("❌ VALIDATION FAILED:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✓ All dependency checks passed")
    print(f"✓ {len(tasks)} tasks validated")
    print(f"✓ No self-references, invalid IDs, or duplicates")
EOF
```

---

## Phase 5: Regenerate Task Markdown Files (30 mins)

After tasks.json is corrected:

```bash
# Regenerate individual task .md files from tasks.json
task-master generate

# Verify no errors
ls -la .taskmaster/tasks/ | grep "task-0"
```

---

## Phase 6: Test & Verify (1 hour)

### Step 6.1: Try to expand a task
```bash
# This should work without errors if dependencies are valid
task-master expand --id=1 --force

# Expected output: No "invalid dependency" errors
```

### Step 6.2: List all tasks (should show clean output)
```bash
task-master list

# Expected: All 28 tasks, no dependency resolution errors
```

### Step 6.3: Test dependency validation
```bash
task-master validate-dependencies

# Expected: Passes with no errors
```

### Step 6.4: Visual inspection
```bash
# Spot-check a few tasks for sanity
task-master show 1
task-master show 2
task-master show 5
```

---

## Phase 7: Documentation (30 mins)

### Step 7.1: Create Correction Report
```markdown
# Dependency Corruption Fix - Execution Report

**Date**: 2026-01-29  
**Operator**: [Your name]  
**Status**: COMPLETE / FAILED

## Corruption Found & Fixed

| Issue | Count | Removed | Examples |
|-------|-------|---------|----------|
| Self-references | 5 | 5 | Task 001 → 001 |
| Invalid IDs | 20 | 20 | "2026", "095", "000" |
| Duplicates | 15 | 15 | Task 005: ["002","002"] |
| Circular dependencies | 2 | 2 | Task A→B→A |

## Before & After

**Before**: 25/28 corrupted  
**After**: 0/28 corrupted

## Validations Passed

- [ ] No self-references
- [ ] All dependency IDs exist in task list
- [ ] No duplicate entries
- [ ] No circular dependencies
- [ ] task-master validate-dependencies ✓
- [ ] task-master list ✓
- [ ] task-master expand --all ✓

## Safe Harbor

- **Backup location**: `.taskmaster/tasks/option_c_backup/`
- **Backup created**: [timestamp]
- **Revert command**: `cp -r option_c_backup/* .taskmaster/tasks/`
```

### Step 7.2: Update ORACLE_RECOMMENDATION_TODO
Add completion checkmark to Phase 1:
```markdown
### Phase 1: Fix Dependency Corruption ✓ COMPLETE
- [x] Review all 28 tasks in `.taskmaster/tasks/tasks.json`
- [x] Identify and remove self-references
- [x] Remove invalid dependency IDs ("2026", "095", "000", etc.)
- [x] Deduplicate dependency entries
- [x] Create clean mapping of Tasks 002-004 + preserve backups
```

---

## Rollback Plan (If Things Go Wrong)

### Rollback Steps
1. Restore from backup:
   ```bash
   cp -r .taskmaster/tasks/option_c_backup/* .taskmaster/tasks/
   ```

2. Regenerate markdown files:
   ```bash
   task-master generate
   ```

3. Verify restoration:
   ```bash
   task-master list
   ```

### When to Rollback
- `task-master validate-dependencies` fails
- `task-master expand` crashes with dependency errors
- More than 5 tasks still have corrupted dependencies after Phase 4

---

## Timeline Estimate

| Phase | Task | Hours | Notes |
|-------|------|-------|-------|
| 1 | Audit & Mapping | 1-2 | Run scripts, document findings |
| 2 | Decision Rules | 0.5-1 | Document rules, get buy-in |
| 3 | Manual Review | 2-3 | Most time-intensive step |
| 4 | Automated Fix | 0.5-1 | Run Python script, validate |
| 5 | Regenerate Markdown | 0.5 | Run task-master generate |
| 6 | Test & Verify | 1 | Run validation commands |
| 7 | Documentation | 0.5 | Write report |
| **TOTAL** | | **6-8** | Conservative estimate |

**Optimistic**: 4-5 hours (good discovery, few edge cases)  
**Realistic**: 6-8 hours (some back-and-forth, validation issues)  
**Pessimistic**: 10+ hours (major rework, circular deps, rollback needed)

---

## Success Criteria

✓ **All of these must be true after Phase 7**:
- [ ] Zero self-references in tasks.json
- [ ] Zero invalid dependency IDs
- [ ] Zero duplicate dependencies
- [ ] All dependency IDs point to existing tasks
- [ ] No circular dependency chains
- [ ] `task-master validate-dependencies` passes
- [ ] `task-master list` shows all 28 tasks without errors
- [ ] `task-master expand --id=1` works without dependency errors
- [ ] Backup safe in `.taskmaster/tasks/option_c_backup/`
- [ ] Execution report documented

---

## Next: After Dependency Fix Complete

Once this plan is executed and validated:
1. Move to Phase 2 of ORACLE_RECOMMENDATION_TODO: **Eliminate Tasks 005-028**
2. Execute Phase 3: **Reframe Core Tasks as Epics**
3. Then begin actual separate project development

---

**Status**: Ready to execute. Start with Phase 1 audit script.
