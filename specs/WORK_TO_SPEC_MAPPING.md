# Work to Spec Mapping

This document maps non-specs content (code, scripts, tests, docs) to the relevant specs folders.

## Mapping Summary

| Spec Folder | Content Categories |
|-------------|-------------------|
| `001-pr176-integration-fixes/` | PR-specific code, tests, hooks |
| `005-cli-architecture/` | CLI code, src/client/UI components |
| `006-unified-architecture/` | Core, backend, config, frontend |
| `007-merge-guidance/` | Git scripts, merge docs |
| `008-branch-comparison/` | Branch comparison docs |
| `009-implementation/` | Tests, validation, implementation tracking |
| `010-orchestration-workflow/` | Hooks, orchestration scripts, speckit |

---

## Detailed Mapping

### `001-pr176-integration-fixes/`

**Purpose:** Update PR-176 with branch changes via GitHub CLI

| Work Category | Files | Status |
|--------------|-------|--------|
| Tests | `test_*.py` | ✅ Implemented |
| Hooks | `scripts/hooks/*` | ✅ Implemented |
| Git automation | `scripts/*.sh` | ✅ Implemented |

---

### `005-cli-architecture/`

**Purpose:** CLI Integration & Architecture Alignment

| Work Category | Files | Status |
|--------------|-------|--------|
| CLI Backend | `src/backend/python_backend/*.py` | ✅ Implemented |
| Frontend | `src/client/src/**/*.tsx`, `src/client/index.html` | ✅ Implemented |

---

### `006-unified-architecture/`

**Purpose:** Unified Architectural Plan for Email Intelligence Platform

| Work Category | Files | Status |
|--------------|-------|--------|
| Core | `src/core/*.py`, `src/speckit/*.py` | ✅ Implemented |
| Backend | `src/backend/node_engine/*.py`, `src/backend/python_nlp/*.py` | ✅ Implemented |
| Config | `src/setup/.env.example`, `src/setup/pyproject.toml` | ✅ Implemented |
| Tests | `tests/*.py`, `src/backend/**/test_*.py` | ✅ Implemented |

---

### `007-merge-guidance/`

**Purpose:** Git Merge Guidance & Branch Strategy

| Work Category | Files | Status |
|--------------|-------|--------|
| Git scripts | `scripts/*.sh` | ✅ Implemented |
| Merge docs | `docs/git_workflow_plan.md` | ✅ Implemented |
| Orchestration docs | `docs/orchestration/*.md` | ✅ Implemented |

---

### `008-branch-comparison/`

**Purpose:** Scientific Branch vs Other Branches Comparison

| Work Category | Files | Status |
|--------------|-------|--------|
| Comparison docs | `docs/branch_history_001_pr176.md` | ✅ Implemented |

---

### `009-implementation/`

**Purpose:** Implementation Tracking & Validation

| Work Category | Files | Status |
|--------------|-------|--------|
| Test infrastructure | `tests/*.py`, `src/backend/**/test_*.py` | ✅ Implemented |
| Validation scripts | `test_*.py` | ✅ Implemented |

---

### `010-orchestration-workflow/`

**Purpose:** Orchestration Workflow System

| Work Category | Files | Status |
|--------------|-------|--------|
| Hooks | `scripts/hooks/*` | ✅ Implemented |
| Setup scripts | `src/setup/*.sh`, `src/setup/*.py` | ✅ Implemented |
| Speckit | `src/speckit/*.py`, `.specify/scripts/*` | ✅ Implemented |
| Orchestration docs | `docs/orchestration-workflow.md` | ✅ Implemented |
| Hook management | `docs/hook-version-mismatch-issue.md` | ✅ Implemented |

---

## Unmapped Content

These files don't have clear spec ownership:

| Files | Suggested Action |
|-------|-----------------|
| `temp-backup/tasks/*.md` | Archive or delete |
| `src/backend/db.ts` | Move to `006-unified-architecture/` |
| `src/backend/plugins/*` | Move to `006-unified-architecture/` |
| `modules/*` | Move to `006-unified-architecture/` |
| `AGENTS.md`, `GEMINI.md`, `CRUSH.md`, `IFLOW.md`, `LLXPRT.md` | Consolidate into specs |

---

## Gaps Analysis

### Specs with NO implementation mapping:
- `001-agent-context-control/` - No content mapped
- `001-rebase-analysis/` - No content mapped
- `002-agent-context-control/` - No content mapped
- `003-rebase-analysis/` - No content mapped

### Implementation without spec:
- `temp-backup/` - Orphaned task files
- `modules/` - No spec reference

---

## Next Steps

1. [ ] Assign `temp-backup/` content to specs or archive
2. [ ] Create spec for `modules/` if active
3. [ ] Mark implementation status in each spec's tasks.md
4. [ ] Consolidate root-level docs into spec folders
