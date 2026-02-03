# Project Identity: Branch Alignment Tooling

**CRITICAL: READ BEFORE ANY MIGRATION OR RESTORATION**

---

## This Repository Contains Branch Alignment Tasks

| Project | Location | Purpose | Status |
|---------|----------|---------|--------|
| **Branch Alignment** | `.taskmaster/tasks/task_001-028.md` | Git branch clustering, merge automation, validation | ACTIVE - Canonical |

---

## ⛔ MIGRATION RULES

### DO NOT:
- Rewrite alignment tasks (001-028) outside branch alignment scope
- Merge non-alignment content into alignment task files
- Treat historical pivot proposals as canonical for this project

### DO:
- Keep alignment tasks focused on: git, branches, merges, rebases, clustering, validation
- Reference this file before any task restructuring

---

## Task 002-004 Canonical Definitions

These are **Branch Alignment** tasks, not external pivots:

| Task | Canonical Purpose | NOT This |
|------|-------------------|----------|
| **002** | Branch Clustering System (git metrics, commit analysis, BranchClusterer) | ❌ Non-alignment scope |
| **003** | Pre-merge Validation Scripts (critical file checks) | ❌ Non-alignment scope |
| **004** | Core Branch Alignment Framework (git hooks, local alignment) | ❌ Non-alignment scope |

---

## Why This Confusion Exists

The `ORACLE_RECOMMENDATION_TODO.md` contains historical scope pivot proposals that were not executed.

**These proposals were NOT executed.** The canonical task set remains Branch Alignment.

---

## Decision Status

| Decision | Status | Resolution |
|----------|--------|------------|
| Project identity | ✅ DECIDED | Branch Alignment Tooling |
| Task 002-004 purpose | ✅ DECIDED | Branch clustering/validation/framework |
| Epic pivot proposals | ❌ REJECTED | Not applicable to this project |

---

## For Future Agents

If you are performing:
- **Task restoration**: Restore alignment content only
- **Task augmentation**: Add alignment-related specs only
- **Migration work**: Do not cross-pollinate from non-alignment sources into `tasks/`

If you encounter pivot definitions, they are **historical proposals only** and should not override the canonical task definitions in `tasks/*.md`.

---

**Last Updated**: 2026-02-03
**Reason**: Prevent conflation of Branch Alignment and EmailIntelligence projects
