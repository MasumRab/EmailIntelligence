# Task 002 Renumbering Decision

**Date:** January 4, 2026  
**Issue:** Task 002 (Branch Clustering System) should be renumbered earlier to reflect zero blocking dependencies  
**Status:** PROPOSED FIX

---

## Blocking Dependency Analysis

### Task 002 Dependencies

**Hard Blocking Dependencies:** NONE  
**Soft Dependencies:** None (provides feedback to Task 001, not the reverse)

From COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md:
```
Task 002: Branch Clustering System

Depends On: None (independent start, parallel with 001)
Blocks:
- 022 (Recovery) - Uses clustering for branch selection
- 023 (Orchestration) - Uses clustering for target assignment
- 004-015 (Framework) - Feeds real metrics to 001, which feeds back
```

**Conclusion:** Task 002 has NO blocking dependencies. It can start immediately Week 1.

---

## Current Numbering Problem

```
INITIATIVE 1 (Foundation):
  001: Framework Strategy (no deps) ✓
  002: Merge Validation (no deps) ✓
  003: Pre-merge Scripts (no deps) ✓

INITIATIVE 2 (Core Framework):
  004-015: Core Alignment (depends: 001-003) ✓

INITIATIVE 3 (Analysis):
  021: Branch Clustering (depends: NONE) ← Should be EARLIER!

INITIATIVE 4 (Execution):
  022-023: Recovery, Orchestration (depends: 001, 021)

INITIATIVE 5 (Maintenance):
  024-026: Maintenance (depends: 004-015)
```

**Issue:** Task 002 appears to depend on 001-003 completion (position implies dependency), but actually runs parallel with Task 001.

---

## Renumbering Options

### Option A: Renumber to 002 (Minimal Change)
Shift current 002-003 to 003-004, cascade rest:

```
INITIATIVE 1:
  001: Framework Strategy
  002: Branch Clustering ← MOVED from 002 (I3.T0)
  003: Merge Validation ← SHIFTED from 002
  004: Pre-merge Scripts ← SHIFTED from 003

INITIATIVE 2:
  005-016: Core Alignment ← ALL SHIFTED +1 (004→005, 005→006, etc.)

INITIATIVE 3: (renamed, still parallel)
  (merged into Initiative 1 and 2)

INITIATIVE 4:
  017-018: Execution ← SHIFTED +1

INITIATIVE 5:
  019-021: Maintenance ← SHIFTED +1
```

**Impact:** +1 cascade across all tasks (001-026 → 001-027)

---

### Option B: Renumber to 001B / 001P (Parallel Indicator)
Keep existing numbering, add suffix:

```
INITIATIVE 1 (PARALLEL):
  001: Framework Strategy (main thread)
  001P: Branch Clustering (parallel thread) ← indicates parallel with 001
  002: Merge Validation
  003: Pre-merge Scripts

INITIATIVE 2-5: Unchanged (004-026)
```

**Impact:** No cascading, makes parallelism explicit  
**Problem:** Non-standard numbering

---

### Option C: Task 004 → Branch Clustering (Reverse Cascade)
Move 002 to become new Task 004, shift Initiative 2 to 005+:

```
INITIATIVE 1:
  001: Framework Strategy
  002: Merge Validation
  003: Pre-merge Scripts

INITIATIVE 2 (renamed Initiative 3):
  004: Branch Clustering ← MOVED from 021
  005: Core Alignment ← SHIFTED from 004 (004→005, 005→006, etc.)

...continues with -1 shift for current 021→004 move
```

**Impact:** Single large cascade (001-026 → 001-024, consolidates initiatives)

---

### Option D: Keep 002 (Current State)
Task 002 stays as Initiative 3, acknowledge parallel execution in documentation.

**Impact:** No changes, numbering implies dependency but doesn't actually exist

---

## Recommendation

**Choose Option A: Renumber to 002**

**Rationale:**
1. ✅ Reflects "can start immediately" (early position)
2. ✅ Maintains clear initiative structure (Initiative 1, 2, 3, 4, 5)
3. ✅ Preserves semantic meaning (002 = early framework task)
4. ✅ Cascading is manageable (all tasks shift +1)
5. ✅ Makes it explicit: Initiative 1 has tasks 001-004, Initiative 2 starts 005

**Downside:** All task IDs in tasks.json change (but could be isolated to new_task_plan/)

---

## Implementation Steps

### Phase 1: Update Reference Documents
1. CLEAN_TASK_INDEX.md - Update all task IDs (+1 cascade)
2. task_mapping.md - Add "Old Clean IDs → Recommended New IDs"
3. COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md - Renumber all references
4. TASK-021-SEQUENTIAL-EXECUTION-FRAMEWORK.md - Becomes TASK-002-SEQUENTIAL-EXECUTION-FRAMEWORK.md
5. TASK_DEPENDENCY_VISUAL_MAP.md - Update all diagrams
6. complete_new_task_outline_ENHANCED.md - Renumber initiatives

### Phase 2: Generate New Task Files
- Regenerate task-002.md through task-027.md (from task-001.md through task-026.md)
- Update all internal references (task-004.md → task-005.md, etc.)

### Phase 3: Update tasks.json (Optional)
- If keeping tasks.json as separate legacy structure: create migration guide
- If consolidating: regenerate tasks.json with new IDs (001-027)

---

## Mapping Table (Option A Recommended)

| Current Clean ID | Old ID | New ID | Initiative |
|---|---|---|---|
| 001 | 7 | 001 | I1 |
| 002 | 9 | 003 | I1 |
| 003 | 19 | 004 | I1 |
| 002 | 75 | 002 | I1 |
| 004 | 54 | 005 | I2 |
| 005 | 55 | 006 | I2 |
| ... | ... | +1 | I2-I5 |
| 026 | 40 | 027 | I5 |

---

## Next Steps

**Decision Required:** Choose option (recommend Option A)

**Then Execute:**
1. Update all documents with new numbering
2. Create migration guide for old→new ID mapping
3. Update task file names
4. Validate all cross-references

---

**Decision:** Ready to implement once approved.
