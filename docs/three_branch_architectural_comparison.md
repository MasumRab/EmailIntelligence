# Three-Branch Architectural Comparison & Convergence Plan

**Date:** 2026-03-17
**Repo:** `MasumRab/EmailIntelligence`
**Branches:** `main`, `scientific`, `orchestration-tools`

---

## 1. Branch Divergence Overview

| Metric | main ↔ scientific | main ↔ orch-tools | scientific ↔ orch-tools |
|--------|-------------------|-------------------|------------------------|
| Commits ahead/behind | 85 / 1652 | 85 / 1127 | 573 / 48 |
| Files changed | 1,354 | 1,166 | 209 |
| Lines changed | +210K / -504K | +190K / -529K | +42K / -3.2K |
| Common ancestor | PR #194 merge | PR #194 merge | `c11366b6` |

**Key insight:** `scientific` and `orchestration-tools` are **close siblings** (only 209 files different), while `main` is the **frozen ancestor** 85 commits behind both.

---

## 2. Branch Identity & Purpose

### `main` — Frozen Production Baseline
- Last meaningful commit: PR #194 (`remove-deprecated-markers`)
- Still has: top-level `backend/`, `python_backend/`, Node.js files, `package.json`, `vite.config.ts`
- Has NOT undergone: `backend→src` migration, setup modularization, CLI framework
- Contains: legacy artifacts (`email_cache.db`, `sqlite.db`, `smart_filters.db`, analysis reports)
- **Status: Stale — needs to receive the architectural changes from scientific/orch-tools**

### `scientific` — Richest Application Codebase
- Full `src/` migration with 7 subpackages: `analysis/`, `cli/`, `context_control/`, `core/`, `git/`, `resolution/`, `strategy/`, `utils/`, `validation/`
- Rich `src/core/` with 33 modules (database, AI engine, auth, security, plugins, workflow, etc.)
- Retained `src/backend/` as a copy of old backend code (migration in progress)
- Full `modules/` (Python: auth, dashboard, email, workflows, etc.)
- Full `tests/` (21 test files + backend/, core/, modules/ subdirs, unit/ tests)
- Modularized `setup/` (project_config, validation, services, environment)
- 15+ AI tool configurations (.claude, .gemini, .cursor, .kilo, .kiro, .roo, .trae, .windsurf, etc.)
- **Status: Most complete application code, but has unresolved merge conflicts**

### `orchestration-tools` — CLI & Tooling Focus
- Lean `src/core/` with only 6 files (interfaces, exceptions, factory, conflict_models, commands)
- Full CLI command framework: `src/cli/commands/` (analyze, resolve, validate, plan-rebase, etc.)
- Rich orchestration tooling: `src/analysis/`, `src/resolution/`, `src/strategy/`, `src/validation/`
- Unique: `setup/routing.py`, `setup/args.py`, `setup/main.py` (command pattern launcher)
- Unique: `.cli_framework/` (distribution/install system)
- Unique: `modules/` repurposed as **shell script modules** (distribute.sh, validate.sh, config.sh, etc.)
- Removed: most application modules (no database, AI engine, auth, etc. in src/core/)
- Stripped `tests/` (8 test files only, focused on launch/hooks/validation)
- **Status: Best CLI/tooling architecture, but missing application core**

---

## 3. Structural Comparison Matrix

### `src/` Package Structure

| Package | main | scientific | orch-tools | Winner |
|---------|------|-----------|------------|--------|
| `src/core/` (app modules) | 33 files | 33 files | 6 files | **scientific** |
| `src/core/commands/` | ❌ | ❌ | ✅ `setup_command.py` | **orch-tools** |
| `src/cli/commands/` | 5 files | 5 files | 11 files | **orch-tools** |
| `src/analysis/` | ❌ | ✅ | ✅ | **shared** |
| `src/git/` | ❌ | ✅ | ✅ | **shared** |
| `src/resolution/` | ✅ | ✅ | ✅ | **shared** |
| `src/strategy/` | ✅ | ✅ | ✅ (richer) | **orch-tools** |
| `src/validation/` | ❌ | ✅ | ✅ (richer) | **orch-tools** |
| `src/utils/` | ❌ | ✅ | ✅ | **shared** |
| `src/context_control/` | ✅ | ✅ | ✅ (richer) | **orch-tools** |
| `src/lib/` | ❌ | ✅ `workflow_context.py` | ❌ | **scientific** |
| `src/backend/` (legacy copy) | ✅ (110+ files) | ✅ (110+ files) | ✅ (smaller) | **remove** |

### `setup/` Launcher System

| Component | main | scientific | orch-tools | Winner |
|-----------|------|-----------|------------|--------|
| `launch.py` | monolithic | modularized (conflicts) | command-pattern | **orch-tools** |
| `project_config.py` | ✅ | ✅ | ✅ | **scientific** (config-driven) |
| `validation.py` | ✅ | ✅ | ✅ | **merge both** |
| `services.py` | ✅ | ✅ | ✅ | **scientific** (richer) |
| `environment.py` | ✅ | ✅ | ✅ | **scientific** (uv support) |
| `routing.py` | ❌ | ❌ | ✅ | **orch-tools** (adopt) |
| `args.py` | ❌ | ❌ | ✅ | **orch-tools** (adopt) |
| `main.py` (entry) | ❌ | ❌ | ✅ | **orch-tools** (adopt) |
| `test_launch.py` | ❌ | ❌ | ✅ | **orch-tools** (adopt) |

### `modules/` Directory

| Branch | Content | Files |
|--------|---------|-------|
| main | Python application modules (auth, email, dashboard, workflows) | 14 dirs |
| scientific | Python application modules (subset: 8 dirs) | 8 dirs |
| orch-tools | **Shell script modules** (distribute, validate, config, etc.) | 8 .sh files |

**Conflict:** `modules/` means completely different things on different branches.

### `tests/` Coverage

| Area | main | scientific | orch-tools |
|------|------|-----------|------------|
| Core tests (auth, db, api, etc.) | ✅ 21 files | ✅ 21 files | ❌ Removed |
| Backend tests | ✅ | ✅ | ❌ |
| Module tests | ✅ | ✅ | ✅ (shell) |
| Launch/hook tests | ❌ | ✅ 4 files | ✅ 3 files |
| Unit tests | ❌ | ✅ `unit/` dir | ❌ |

### `backend/` (Top-Level)

| Branch | Status |
|--------|--------|
| main | **Deleted** (but contents live in `src/backend/`) |
| scientific | **Deleted** (but contents live in `src/backend/`) |
| orch-tools | **Still exists** with `python_backend/` |

---

## 4. Architectural Decisions Required

### Decision 1: Target Architecture for `src/`

**Recommendation: Merge scientific's rich core + orch-tools' CLI/strategy enhancements**

```
src/
├── __init__.py
├── main.py                          # From scientific
├── core/                            # From scientific (33 modules)
│   ├── commands/                    # From orch-tools (setup_command.py)
│   ├── database.py, ai_engine.py, auth.py, ...
│   ├── conflict_models.py          # Shared
│   ├── interfaces.py               # Shared
│   └── exceptions.py               # Shared
├── cli/commands/                    # From orch-tools (11 files, richer)
├── analysis/                        # Shared (merge any differences)
├── context_control/                 # From orch-tools (richer, has project.py)
├── git/                             # Shared
├── resolution/                      # Shared
├── strategy/                        # From orch-tools (has multi_phase, reordering, selector)
├── utils/                           # Merge (orch-tools has monitoring, rate_limit)
├── validation/                      # From orch-tools (comprehensive, quality, quick validators)
└── lib/                             # From scientific (workflow_context.py)
```

**DELETE:** `src/backend/` — complete the migration, don't carry the legacy copy.

---

### Decision 2: Target Architecture for `setup/`

**Recommendation: Orch-tools command-pattern launcher + scientific's config/services**

```
setup/
├── __init__.py
├── main.py                          # From orch-tools (clean entrypoint)
├── args.py                          # From orch-tools (argument parsing)
├── routing.py                       # From orch-tools (command routing)
├── launch.py                        # THIN orchestrator (not monolithic)
├── project_config.py                # From scientific (config-driven paths)
├── validation.py                    # Merge: scientific config + orch-tools scanning
├── services.py                      # From scientific (richer service management)
├── environment.py                   # From scientific (uv, WSL, notmuch support)
├── container.py                     # Shared
├── settings.py                      # Shared
├── utils.py                         # Shared
├── commands/                        # Shared
├── test_*.py                        # Merge all test files
├── requirements*.txt                # Shared
└── pyproject.toml                   # Merge
```

---

### Decision 3: `modules/` Directory Resolution

**Problem:** `modules/` means Python app modules on scientific, shell orchestration scripts on orch-tools.

**Recommendation:**
- Keep `modules/` for **Python application modules** (from scientific)
- Move orch-tools shell modules to `scripts/orchestration/modules/` or `.cli_framework/modules/`

---

### Decision 4: `backend/` Elimination

| Location | Action |
|----------|--------|
| Top-level `backend/` (orch-tools) | Delete — migrate to `src/` |
| `src/backend/` (scientific) | Delete — already migrated to `src/core/`, `modules/`, etc. |
| Imports: `from backend.*` | Rewrite to `from src.core.*` or `from src.backend.*` temporarily |

---

### Decision 5: `tests/` Unification

```
tests/
├── conftest.py                      # Single sys.path strategy
├── __init__.py
├── core/                            # From scientific (keep all)
├── backend/                         # From scientific (update imports)
├── modules/                         # Python tests from scientific + shell tests from orch-tools
├── unit/                            # From scientific
├── test_*.py                        # Merge all top-level test files
├── test_launch.py                   # From orch-tools
├── test_hooks.py                    # Shared
└── test_sync.py                     # Shared
```

---

## 5. Import Migration Map

### Stale Imports That Must Change

| Current Import | Target Import | Affected Files |
|---------------|--------------|----------------|
| `from backend.python_backend.database import ...` | `from src.core.database import ...` | tests, src/backend/ |
| `from backend.python_backend.ai_engine import ...` | `from src.core.ai_engine import ...` | tests |
| `from backend.python_nlp.smart_filters import ...` | `from src.core.smart_filter_manager import ...` | tests, plugins |
| `from backend.python_nlp.ai_training import ...` | `from modules.model_management import ...` or new location | tests |
| `from backend.node_engine.* import ...` | `from src.backend.node_engine.* import ...` (keep temporarily) | tests, plugins |
| `from setup.launch import ...` (internals) | `from setup.services import ...` / `from setup.environment import ...` | setup/ |

### Duplicate Module Canonical Locations

| Module | Keep (canonical) | Delete (duplicate) |
|--------|-----------------|-------------------|
| `database.py` | `src/core/database.py` | `src/backend/python_backend/database.py` |
| `ai_engine.py` | `src/core/ai_engine.py` | `src/backend/python_backend/ai_engine.py` |
| `caching.py` | `src/core/caching.py` | `src/utils/caching.py` (merge unique parts first) |
| `main.py` | `src/main.py` | `src/backend/python_backend/main.py` |
| `factory.py` | `src/core/factory.py` | Keep `src/core/data/factory.py` (different purpose), `src/cli/commands/factory.py` (CLI factory) |

---

## 6. Implementation Plan

### Phase 1: Prepare the Merge Target (on `scientific`)

```
[ ] 1.1  Resolve all 10 conflict-marker files (see conflict resolution plan)
[ ] 1.2  Unstage the 529-file staging blob
[ ] 1.3  Squash the 3 stash-apply commits
[ ] 1.4  Clean commit and push to origin/scientific
```

### Phase 2: Import Orch-tools Architecture into Scientific

```
[ ] 2.1  Cherry-pick or merge orch-tools CLI enhancements:
         - src/cli/commands/ (6 new files: analyze_history, plan_rebase, registry, etc.)
         - src/strategy/ (multi_phase_generator, reordering, selector)
         - src/validation/ (comprehensive, quality, quick validators)
         - src/context_control/ (project.py, richer config)
         - src/utils/ (monitoring, rate_limit)
[ ] 2.2  Import setup/ enhancements:
         - setup/routing.py (command routing)
         - setup/args.py (argument parsing)
         - setup/main.py (clean entrypoint)
         - setup/test_launch.py
[ ] 2.3  Import .cli_framework/ distribution system
[ ] 2.4  Resolve modules/ conflict (keep Python modules, relocate shell modules)
```

### Phase 3: Complete the `backend→src` Migration

```
[ ] 3.1  Identify all files in src/backend/ that have canonical equivalents in src/core/
[ ] 3.2  Create compatibility shims for src/backend/ modules → src/core/
[ ] 3.3  Update all imports: backend.* → src.core.* (6 external, 15+ internal)
[ ] 3.4  Update plugin imports
[ ] 3.5  Run full test suite to surface broken imports
[ ] 3.6  Delete src/backend/ once all imports are migrated
[ ] 3.7  Delete top-level backend/ if it still exists
```

### Phase 4: Unify Tests & Configuration

```
[ ] 4.1  Merge test files from all three branches
[ ] 4.2  Unify conftest.py (one sys.path strategy or pyproject.toml pythonpath)
[ ] 4.3  Update all test imports to use src.* canonical paths
[ ] 4.4  Add pytest pythonpath config to pyproject.toml
[ ] 4.5  Remove sys.path hacks from 10+ files
[ ] 4.6  Run full test suite: pytest tests/ -v
```

### Phase 5: Merge Scientific → Main

```
[ ] 5.1  Create PR: scientific → main
[ ] 5.2  Resolve any remaining conflicts (main is 85 commits behind)
[ ] 5.3  Delete legacy files from main that no longer exist
[ ] 5.4  Verify CI passes
[ ] 5.5  Merge
```

### Phase 6: Align Orchestration-Tools with New Main

```
[ ] 6.1  Rebase orchestration-tools onto new main
[ ] 6.2  Resolve any conflicts from the merge
[ ] 6.3  Verify orch-tools specific features still work
[ ] 6.4  Push updated orchestration-tools
```

---

## 7. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Import breakage during backend→src migration | 🔴 High | Create shims first, delete old modules only after all imports updated |
| modules/ namespace collision (Python vs shell) | 🟡 Medium | Relocate shell modules before merge |
| Loss of orch-tools CLI features during merge | 🟡 Medium | Cherry-pick individually, test each |
| Test failures from path changes | 🟡 Medium | Fix conftest.py first, then run tests incrementally |
| setup/launch.py re-conflict during merge | 🔴 High | Resolve scientific conflicts FIRST (Phase 1), then import orch-tools additions |
| main drift during multi-phase work | 🟢 Low | main is effectively frozen at PR #194 |

---

## 8. Branch Convergence Diagram

```
main (frozen at PR #194)
  │
  ├── scientific (1652 commits ahead)
  │     ├── Rich src/core/ (33 modules)
  │     ├── Full modules/ (Python app)
  │     ├── Full tests/ (21 files)
  │     ├── Setup modularization (conflicts)
  │     └── src/backend/ (legacy copy - DELETE)
  │
  └── orchestration-tools (1127 commits ahead)
        ├── Lean src/core/ (6 files)
        ├── Rich CLI framework (11 commands)
        ├── Rich strategy/validation
        ├── Command-pattern launcher
        ├── Shell orchestration modules
        └── top-level backend/ (DELETE)

CONVERGENCE TARGET:
  scientific + orch-tools CLI/strategy → new main
  ├── src/core/ (33 modules from scientific)
  ├── src/cli/ (11 commands from orch-tools)
  ├── src/strategy/ (rich from orch-tools)
  ├── src/validation/ (rich from orch-tools)
  ├── modules/ (Python app from scientific)
  ├── tests/ (merged from both)
  ├── setup/ (command-pattern from orch-tools + config from scientific)
  └── NO backend/ anywhere
```

---

## 9. Estimated Effort

| Phase | Work | Effort |
|-------|------|--------|
| 1. Resolve scientific conflicts | Fix 10 files, restage, squash | 2-3h |
| 2. Import orch-tools architecture | Cherry-pick CLI, strategy, setup | 4-6h |
| 3. Complete backend→src migration | Shims, import rewrites, cleanup | 4-6h |
| 4. Unify tests & config | Merge tests, fix conftest, paths | 2-3h |
| 5. Merge scientific → main | PR, resolve, verify | 2-3h |
| 6. Align orch-tools | Rebase, resolve, verify | 2-3h |
| **Total** | | **16-24h** |

---

*Analysis based on `git ls-tree`, `git diff --stat`, `git rev-list`, and file-by-file comparison across all three branches on 2026-03-17.*
