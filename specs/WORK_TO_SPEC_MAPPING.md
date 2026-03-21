# Work to Spec Mapping

This document maps non-specs content (code, scripts, tests, docs) to the relevant specs folders.

## Mapping Summary

| Spec Folder | Content Categories |
|-------------|-------------------|
| `001-pr176-integration-fixes/` | PR-specific code, tests, hooks |
| `005-cli-architecture/` | CLI code, client/UI components |
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
| Tests | `test_*.py` | ⏳ Not implemented |
| Hooks | `scripts/hooks/*` | ⏳ Not implemented |
| Git automation | `scripts/*.sh` | ⏳ Not implemented |

---

### `005-cli-architecture/`

**Purpose:** CLI Integration & Architecture Alignment

| Work Category | Files | Status |
|--------------|-------|--------|
| CLI Backend | `backend/python_backend/*.py` | ⏳ Not implemented |
| Frontend | `client/src/**/*.tsx`, `client/index.html` | ⏳ Not implemented |

---

### `006-unified-architecture/`

**Purpose:** Unified Architectural Plan for Email Intelligence Platform

| Work Category | Files | Status |
|--------------|-------|--------|
| Core | `src/core/*.py`, `src/speckit/*.py` | ⏳ Not implemented |
| Backend | `backend/node_engine/*.py`, `backend/python_nlp/*.py` | ⏳ Not implemented |
| Config | `setup/.env.example`, `setup/pyproject.toml` | ⏳ Not implemented |
| Tests | `tests/*.py`, `backend/**/test_*.py` | ⏳ Not implemented |

---

### `007-merge-guidance/`

**Purpose:** Git Merge Guidance & Branch Strategy

| Work Category | Files | Status |
|--------------|-------|--------|
| Git scripts | `scripts/*.sh` | ⏳ Not implemented |
| Merge docs | `docs/git_workflow_plan.md` | ⏳ Not implemented |
| Orchestration docs | `docs/orchestration/*.md` | ⏳ Not implemented |

---

### `008-branch-comparison/`

**Purpose:** Scientific Branch vs Other Branches Comparison

| Work Category | Files | Status |
|--------------|-------|--------|
| Comparison docs | `docs/branch_history_001_pr176.md` | ⏳ Not implemented |

---

### `009-implementation/`

**Purpose:** Implementation Tracking & Validation

| Work Category | Files | Status |
|--------------|-------|--------|
| Test infrastructure | `tests/*.py`, `backend/**/test_*.py` | ⏳ Not implemented |
| Validation scripts | `test_*.py` | ⏳ Not implemented |

---

### `010-orchestration-workflow/`

**Purpose:** Orchestration Workflow System

| Work Category | Files | Status |
|--------------|-------|--------|
| Hooks | `scripts/hooks/*` | ⏳ Not implemented |
| Setup scripts | `setup/*.sh`, `setup/*.py` | ⏳ Not implemented |
| Speckit | `src/speckit/*.py`, `.specify/scripts/*` | ⏳ Not implemented |
| Orchestration docs | `docs/orchestration-workflow.md` | ✅ Implemented |
| Hook management | `docs/hook-version-mismatch-issue.md` | ✅ Implemented |

---

## Unmapped Content

These files don't have clear spec ownership:

| Files | Suggested Action |
|-------|-----------------|
| `temp-backup/tasks/*.md` | Archive or delete |
| `backend/db.ts` | Move to `006-unified-architecture/` |
| `backend/plugins/*` | Move to `006-unified-architecture/` |
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
