# Large File Analysis: merge_task_manager.py

**Lines:** 1,495  
**Location:** `.taskmaster/task_scripts/merge_task_manager.py`  
**Last Modified:** March 29, 2026  
**Type:** Task file validation and repair utility  

---

## Purpose

Advanced task file manager for detecting and fixing issues in `tasks.json` during complex merge processes. Handles duplicate IDs, invalid JSON, dependency issues, orphaned subtasks, and provides backup/recovery.

---

## Structure

### Single Large Class: AdvancedTaskManager (1,356 lines)

**Constructor & Setup (lines 37-53, 17 lines):**
- Initialize paths and backup directory
- Setup logging
- Initialize validation state dictionaries

**Methods by Category:**

#### Security & Validation (lines 80-154, 75 lines)
| Method | Lines | Purpose |
|--------|-------|---------|
| `validate_path_security()` | 80-152 | Path traversal prevention |
| `create_backup()` | 154-180 | Backup file before operations |
| `check_merge_conflicts()` | 182-198 | Detect merge conflict markers |

#### File I/O (lines 200-386, 187 lines)
| Method | Lines | Purpose |
|--------|-------|---------|
| `load_tasks()` | 200-273 | Load and parse JSON with fixup |
| `attempt_json_fix()` | 275-338 | Attempt to repair broken JSON |
| `save_tasks()` | 340-366 | Save tasks back to file |
| `extract_tasks()` | 368-377 | Extract task list from data |
| `set_tasks()` | 379-384 | Set task list in data |

#### Analysis & Detection (lines 386-602, 217 lines)
| Method | Lines | Purpose |
|--------|-------|---------|
| `collect_all_task_ids()` | 386-423 | Gather all IDs from tasks |
| `validate_json_structure()` | 425-433 | Check JSON structure validity |
| `validate_duplicate_ids()` | 435-452 | Find duplicate IDs |
| `validate_task_structure()` | 454-489 | Check task field validity |
| `validate_dependencies()` | 491-512 | Validate dependency references |
| `build_dependency_graph()` | 514-550 | Build task dependency graph |
| `detect_circular_dependencies()` | 552-581 | Find circular deps |
| `validate_orphaned_subtasks()` | 583-600 | Find subtasks without parents |
| `validate_priority_consistency()` | 602-611 | Check priority consistency |

#### Repair/Fixing Methods (lines 613-1032, 420 lines)
| Method | Lines | Purpose |
|--------|-------|---------|
| `resolve_duplicate_ids()` | 613-706 | Merge/rename duplicate IDs (94 lines) |
| `merge_duplicate_task_fields()` | 708-784 | Merge fields from duplicate tasks |
| `fix_invalid_dependencies()` | 786-847 | Fix broken dependency references |
| `fix_missing_fields()` | 849-952 | Add missing required fields |
| `fix_priority_weaknesses()` | 954-986 | Repair invalid priorities |
| `fix_orphaned_subtasks()` | 988-1032 | Reattach orphaned subtasks |

#### Utilities (lines 1035-1360, 326 lines)
| Method | Lines | Purpose |
|--------|-------|---------|
| `restore_from_backup()` | 1035-1047 | Recover from backup file |
| `validate_and_fix()` | 1049-1281 | Main orchestration (233 lines) |
| `print_results()` | 1283-1309 | Format and print results |
| `get_statistics()` | 1311-1358 | Generate statistics report |
| `cleanup_backups()` | 1360-1388 | Remove old backups |

---

## Class Structure Summary

| Category | Lines | Methods | Purpose |
|----------|-------|---------|---------|
| Init & Setup | 17 | 1 | Initialize manager |
| Security | 75 | 3 | Validation & backups |
| File I/O | 187 | 5 | JSON read/write |
| Analysis | 217 | 9 | Detect issues |
| Repair | 420 | 6 | Fix issues (largest) |
| Utilities | 326 | 5 | Orchestration & output |
| **TOTAL** | **1,242** | **29** | Single class |

---

## Key Dependencies

**External:**
- argparse, copy, json, logging, re, shutil, tempfile, traceback
- collections (defaultdict, deque)
- datetime, pathlib

**Internal:**
- None (standalone utility)

**Nesting Depth:** Maximum 4 levels (in circular dependency detection)

---

## Proposed Decomposition

**Recommended Split:**

| Component | Files | Rationale |
|-----------|-------|-----------|
| Validators | `task_validators.py` | 9 validation methods (217 lines) |
| Repairers | `task_repairers.py` | 6 repair methods (420 lines) |
| File I/O | `task_io.py` | 5 file methods (187 lines) |
| CLI | `merge_task_manager.py` (refactored) | Orchestration layer (main()) |

**New Structure:**
```
task_scripts/
├── merge_task_manager.py (refactored, ~100 lines)
├── task_validators.py (217 lines)
├── task_repairers.py (420 lines)
└── task_io.py (187 lines)
```

**Effort:** 6-8 hours  
**Benefit:** Easier to test, reuse in other tools  
**Recommendation:** RECOMMENDED (high modularity potential)

---

## Code Quality Issues

1. **Large class:** 29 methods in one class
2. **Complex orchestration:** `validate_and_fix()` is 233 lines
3. **Duplicate logic:** Similar patterns in fix_* methods
4. **Type hints:** Incomplete (uses Optional, but not Union types)
5. **Error handling:** Mix of logging and exceptions

---

## Recommendation

**RECOMMENDED SPLIT** — High reusability potential:

- Validators could be used standalone for CI/CD checks
- Repairers could be used in different contexts
- File I/O could be reused for task export/import

**Effort:** 6-8 hours  
**Benefit:** ~40% code clarity, high reusability  
**Recommendation:** RECOMMENDED (secondary priority after emailintelligence_cli.py)

---

## Summary

**Size:** 1,495 lines (LARGE)  
**Complexity:** HIGH (29 methods, complex algorithms)  
**Maintainability:** MEDIUM (good modularity opportunity)  
**Modularity:** MEDIUM (could be split effectively)  
**Recommendation:** SPLIT RECOMMENDED (secondary priority)

