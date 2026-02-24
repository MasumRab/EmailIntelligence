# CK Semantic Similarity & Cross-Task Analysis

**Date:** 2026-02-25
**Tool:** ck semantic search (BAAI/bge-small-en-v1.5, 15,313 chunks indexed)

---

## 1. Massive Section Duplication in Parent Tasks (CRITICAL)

The same pattern we fixed in tasks 010/011/012 exists in **17 more parent task files**. Each has 100+ `##` sections (should be ~13).

| File | Lines | Sections | Expected | Bloat Factor |
|------|-------|----------|----------|-------------|
| task_009.md | 4,946 | 121 | 13 | **9.3x** |
| task_001.md | 4,678 | 110 | 13 | **8.5x** |
| task_002.md | 4,435 | 128 | 13 | **9.8x** |
| task_018.md | 4,050 | 104 | 13 | **8.0x** |
| task_025.md | 4,041 | 104 | 13 | **8.0x** |
| task_015.md | 3,984 | 105 | 13 | **8.1x** |
| task_022.md | 3,968 | 104 | 13 | **8.0x** |
| task_021.md | 3,900 | 104 | 13 | **8.0x** |
| task_023.md | 3,861 | 104 | 13 | **8.0x** |
| task_020.md | 3,852 | 104 | 13 | **8.0x** |
| task_019.md | 3,840 | 109 | 13 | **8.4x** |
| task_024.md | 3,826 | 104 | 13 | **8.0x** |
| task_014.md | 3,781 | 110 | 13 | **8.5x** |
| task_016.md | 3,690 | 109 | 13 | **8.4x** |
| task_017.md | 3,612 | 109 | 13 | **8.4x** |
| task_013.md | 3,556 | 105 | 13 | **8.1x** |
| task_008.md | 2,253 | 69 | 13 | **5.3x** |
| task_005.md | 2,054 | 78 | 13 | **6.0x** |
| **TOTAL** | **67,327** | — | — | — |

**Estimated clean size:** ~6,000 lines (13 sections × ~30 lines × 18 files + subtask lists)
**Potential reduction:** ~61,000 lines (~91%)

---

## 2. IMPORTED_FROM Markers Still Present

45 `<!-- IMPORTED_FROM: ... -->` comment markers remain across 22 parent task files. These reference deleted directories (`enhanced_improved_tasks/`, `task_data/migration_backup_20260129/`).

**Affected files:** task_001, 002, 003, 004, 005, 006, 007, 008, 009, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 025, 026, 027, 028

---

## 3. overexpanded_backup/ Directory Inside tasks/

11 files in `tasks/overexpanded_backup/` are duplicates of current task files:

```
tasks/overexpanded_backup/task_001.md
tasks/overexpanded_backup/task_002.{1-9,md}
```

**Action:** Delete entire directory.

---

## 4. Cross-Task Logical Connections (Semantic Clusters)

ck semantic search reveals these thematic clusters where tasks share substantial overlapping content:

### Cluster A: Conflict Resolution & Rebase (score 0.84-0.87)
- **task_010.md** — Multilevel strategies for complex branches (iterative rebase)
- **task_014.md** — Conflict Detection and Resolution
- **task_009.md** (subtasks 009.6, 009.7) — Core alignment rebase operations
- **task_001.6.md** — Conflict resolution command reference
- **task_013.md** — Branch Backup Safety (pre-rebase safety)

**Finding:** Tasks 010 and 014 have ~40% overlapping content on conflict resolution workflows. Task 010.4 (focused conflict resolution) duplicates Task 014's core purpose.

### Cluster B: Validation & Testing (score 0.82-0.84)
- **task_017.md** — Validation Integration Framework
- **task_008.md** — Comprehensive Merge Validation Framework
- **task_015.md** — Validation and Verification
- **task_018.md** — End-to-End Testing and Reporting
- **task_011.md** — Integrate Validation into Alignment

**Finding:** Tasks 008, 015, and 017 all describe validation frameworks with near-identical architecture (pre-validation, execution, post-validation stages).

### Cluster C: Rollback & Recovery (score 0.80-0.83)
- **task_016.md** — Rollback and Recovery (3,690 lines!)
- **task_013.md** — Branch Backup and Safety
- **task_010.md** (subtask 010.7) — Rollback for complex branches
- **task_006.md** — Branch Backup and Restore Mechanism

**Finding:** Task 016 contains the rollback content from BOTH 013 and 006, effectively tripling it. Subtask 010.7 duplicates 016's purpose.

### Cluster D: Pipeline & Orchestration (score 0.82-0.84)
- **task_002.md** — Branch Clustering System overview
- **task_002.6.md** — PipelineIntegration
- **task_012.md** — Sequential Branch Alignment Workflow
- **task_005.md** — Branch Clustering System (same as 002?)

**Finding:** task_005.md and task_002.md appear to describe the same system (Branch Clustering). task_005.md may be a stale duplicate.

### Cluster E: Monitoring & Reporting (score 0.74-0.77)
- **task_021.md** — Maintenance and Monitoring (3,900 lines, duplicated sections)
- **task_002.7.md** — VisualizationReporting
- **task_020.md** — Documentation and Knowledge Management

**Finding:** task_021.md has identical config blocks appearing twice (lines 513 and 3009, lines 897 and 3393).

---

## 5. Recommended Actions

### Priority 1: Deduplicate 17 Parent Tasks (~3-4 hours)
Same procedure as tasks 010/011/012: merge best content, remove duplicates, comply with 14-section standard.

### Priority 2: Delete overexpanded_backup/ (1 minute)
```bash
rm -rf tasks/overexpanded_backup/
```

### Priority 3: Strip IMPORTED_FROM Markers (5 minutes)
```bash
find tasks/ -name 'task_0*.md' -exec sed -i '/<!-- IMPORTED_FROM:/d' {} +
```

### Priority 4: Investigate Task Overlaps (1-2 hours)
- Confirm whether task_005.md duplicates task_002.md
- Clarify boundary between tasks 008, 015, and 017 (all "validation frameworks")
- Clarify boundary between tasks 006, 013, and 016 (all "backup/recovery")
- Consider merging overlapping subtasks (010.4 ↔ 014, 010.7 ↔ 016)
