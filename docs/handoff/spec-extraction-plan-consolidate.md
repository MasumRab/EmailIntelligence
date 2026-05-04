# Spec Extraction Plan — For consolidate/cli-unification Branch

**Date:** 2026-04-14  
**Source:** Qwen agent multi-spec review analysis  
**Full Analysis:** `docs/handoff/spec-merge-analysis.md`

---

## Purpose

This branch (`consolidate/cli-unification`) accidentally accumulated spec content during consolidation. **Specs were not intended to be on this branch** — they were merged in from other branches (000-integrated-specs, scientific, etc.) during the consolidation process.

All spec content must be **extracted from this branch and moved to `000-integrated-specs`**, which is the canonical spec hub.

---

## Specs to Extract

### Unique Value Specs (Add to 000)

| Spec | Files | Notes |
|------|-------|-------|
| `specs/001-pr176-integration-fixes/` | 14 | GitHub CLI automation — unique scope |
| `specs/001-rebase-analysis/` | 6 | Same topic as 000's 010 — merge content |
| `specs/003-unified-git-analysis/` | 8 | Same topic as 000's 012 — merge content |
| `specs/005-cli-architecture/` | 11 | **HIGH VALUE** — architecture guides from scientific branch |
| `specs/006-unified-architecture/` | 12 | Architecture consolidation plan |
| `specs/007-merge-guidance/` | 8 | Practical merge guidance |
| `specs/008-branch-comparison/` | 7 | Branch comparison framework |
| `specs/009-implementation/` | 9 | Implementation framework |
| `specs/010-orchestration-workflow/` | 6 | Workflow orchestration |
| `WORK_TO_SPEC_MAPPING.md` | 1 | Cross-reference document |

### Overlapping Specs (Replace or Merge on 000)

| Spec | Files | Action on 000 |
|------|-------|---------------|
| `specs/004-guided-workflow/` | 23 (minus 3 backups) | **REPLACE** 000's version — 723 lines vs 48 |
| `specs/006-pr176-integration-fixes/` | 4 | **MERGE** — 3 path corrections to tasks.md |
| `specs/013-task-execution-layer/` | 4 | **MERGE** with 000's 007-task-execution-layer |

### Empty/Duplicate Specs (Don't Extract)

| Spec | Reason |
|------|--------|
| `specs/001-agent-context-control/spec.md` | Empty (0 bytes) |
| `specs/002-agent-context-control/spec.md` | Empty (0 bytes) |
| `specs/003-rebase-analysis/` | Exact duplicate of 001-rebase-analysis |
| `specs/004-guided-workflow/*.bak` (3 files) | Backup artifacts |

---

## What This Branch Loses

After extraction, this branch will no longer have the `specs/` directory or `WORK_TO_SPEC_MAPPING.md`. This is **intentional** — specs belong on `000-integrated-specs`, not here.

**Files remaining on this branch after extraction:**
- All application code (`src/`, `client/`, `modules/`, `conductor/`)
- All agent configs (`.agent/`, `.claude/`, `.clinerules/`, `.cursor/`, etc.)
- All documentation (`docs/`, `rules/`)
- All scripts and automation

---

## What This Branch Contributes

Despite being unintentional, the specs on this branch contain valuable content:

1. **Orchestration Core specification** (004) — Complete rewrite of 000's simple guided workflow with dev.py, DAG analysis, AST scanning, Pydantic models
2. **CLI architecture** (005) — Factory pattern, interface-based design from scientific branch
3. **Architecture guides** (006) — Production deployment prep, workflow system consolidation
4. **Merge guidance** (007) — Practical strategies that worked/failed
5. **Branch comparison** (008) — Analysis methodology
6. **Implementation framework** (009) — Structured implementation approach
7. **Orchestration workflow** (010) — Workflow orchestration design

---

## Extraction Method

To extract specs from this branch:

```bash
# On consolidate branch
# 1. Create archive of valuable specs
tar czf /tmp/specs-extract.tar.gz \
  specs/001-pr176-integration-fixes \
  specs/001-rebase-analysis \
  specs/003-unified-git-analysis \
  specs/005-cli-architecture \
  specs/006-unified-architecture \
  specs/007-merge-guidance \
  specs/008-branch-comparison \
  specs/009-implementation \
  specs/010-orchestration-workflow \
  specs/004-guided-workflow \
  specs/006-pr176-integration-fixes \
  specs/013-task-execution-layer \
  WORK_TO_SPEC_MAPPING.md

# 2. On 000 branch, extract and merge
# (See 000-integrated-specs consolidation plan)

# 3. Remove specs from consolidate branch
git rm -r specs/ WORK_TO_SPEC_MAPPING.md
git commit -m "chore: extract specs to 000-integrated-specs (canonical spec hub)"
```

---

*This document should be kept on the consolidate/cli-unification branch to track what was extracted and why.*
