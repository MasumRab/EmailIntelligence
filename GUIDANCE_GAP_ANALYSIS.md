# Guidance Directory Gap Analysis

## Purpose
Identify what information exists in `/guidance/` that needs to be transferred to task files in `/new_task_plan/task_files/`.

---

## What's In `/guidance/` (Source)

### Core Implementation Files
- `src/main.py` - Factory pattern (`create_app()`)
- `validate_architecture_alignment.py` - Validation script (5 checks)

### Documentation Files (11 total)
- README.md, SUMMARY.md, QUICK_REFERENCE_GUIDE.md
- MERGE_GUIDANCE_DOCUMENTATION.md
- IMPLEMENTATION_SUMMARY.md
- ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md
- HANDLING_INCOMPLETE_MIGRATIONS.md
- FINAL_MERGE_STRATEGY.md
- ARCHITECTURE_ALIGNMENT_IMPLEMENTATION_GUIDE.md

---

## What's Missing From Task Files

### Gap 1: Factory Pattern
| In guidance/ | In task files |
|--------------|---------------|
| `src/main.py` with `create_app()` | NOT REFERENCED |
| Service startup: `uvicorn src.main:create_app --factory` | NOT DOCUMENTED |

**Location to fix:** task-001.md, task-002.md

### Gap 2: Validation Framework
| In guidance/ | In task files |
|--------------|---------------|
| `validate_architecture_alignment.py` | NOT REFERENCED |
| 5 validation checks | NOT DOCUMENTED |
| Validation commands | NOT PROVIDED |

**Location to fix:** task-002.md

### Gap 3: Import Path Patterns
| In guidance/ | In task files |
|--------------|---------------|
| `backend.*` → `src.backend.*` pattern | NOT SHOWN |
| Detection commands | NOT PROVIDED |

**Location to fix:** task-003.md

### Gap 4: Rollback Plan
| In guidance/ | In task files |
|--------------|---------------|
| 5-step rollback procedure | NOT IN TASK FILES |
| Recovery steps | NOT IN TASK FILES |

**Location to fix:** task-006.md

### Gap 5: Pre-Merge Checklist
| In guidance/ | In task files |
|--------------|---------------|
| 8-item checklist | ONLY 1 ITEM MENTIONED |

**Location to fix:** task-001.md

### Gap 6: Common Gotchas
| In guidance/ | In task files |
|--------------|---------------|
| 7 documented gotchas | NOT IN TASK FILES |

**Location to fix:** task-001.md

### Gap 7: Lessons Learned
| In guidance/ | In task files |
|--------------|---------------|
| 7 what-worked strategies | NOT IN TASK FILES |
| 6 what-didn't failures | NOT IN TASK FILES |
| 4 key insights | NOT IN TASK FILES |

**Location to fix:** task-001.md

---

## Summary

| Category | Items | Task Files Affected |
|----------|-------|---------------------|
| Factory Pattern | 1 file | task-001.md, task-002.md |
| Validation Framework | 1 file + 5 checks | task-002.md |
| Import Patterns | Examples + commands | task-003.md |
| Rollback Plan | 5 steps | task-006.md |
| Pre-Merge Checklist | 8 items | task-001.md |
| Common Gotchas | 7 items | task-001.md |
| Lessons Learned | 17 items | task-001.md |

**Total items to transfer:** ~40 specific pieces of guidance
**Files to update:** 4 task files (task-001.md, task-002.md, task-003.md, task-006.md)

---

## Transfer Priority

1. **Critical:** Factory pattern, validation framework, rollback plan
2. **High:** Pre-merge checklist, common gotchas
3. **Medium:** Lessons learned, import patterns

---

## Files Reference

**Source:** `/home/masum/github/PR/.taskmaster/guidance/`
**Target:** `/home/masum/github/PR/.taskmaster/new_task_plan/task_files/`
