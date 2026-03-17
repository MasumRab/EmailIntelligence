# Scientific Branch — Conflict Resolution & Architecture Migration Plan

**Date:** 2026-03-17
**Repo:** `~/github/EmailIntelligence` (branch: `scientific`)
**Remote:** `origin/scientific` on `MasumRab/EmailIntelligence`

---

## 1. Root Cause Analysis

### Why the Conflicts Exist

The conflicts stem from **two simultaneous, divergent refactors** of the same `setup/` module system:

| Side | Commit | What It Did |
|------|--------|-------------|
| **HEAD (scientific)** | Local commits | Modularized `setup/launch.py` into `project_config.py`, `validation.py`, `services.py`, `environment.py` with uv-based dependency management and config-driven paths |
| **Main-line** (`a7da61cf`) | `perf: optimize ContextIsolator pattern matching` (from orchestration-tools lineage) | Also modularized setup/ but with simpler imports, added performance optimizations, assumed different module ownership boundaries |

Both branches broke `setup/launch.py` from a monolith into modules — but made **different architectural decisions** about what goes where.

### Conflict Categories

| Category | Files | Real Conflict? | Marker Count |
|----------|-------|---------------|--------------|
| **Module ownership** | `setup/launch.py`, `setup/services.py` | ✅ Real — same functions defined in different places | 28 + ~4 |
| **Config vs hardcoded** | `setup/validation.py`, `setup/project_config.py` | ✅ Real — one side uses config-driven paths, other hardcodes | ~3 |
| **Docstring/style** | `setup/environment.py` | ⚠️ Minor — mostly docstring wording + import order | 6 |
| **Repo hygiene** | `.gitattributes` | ⚠️ Minor — main-line adds line endings, scientific has none | 1 |
| **AI tool config** | `.gemini/commands/speckit.constitution.toml` | ⚠️ Minor — description text drift | 1 |
| **False positives** | `benchmark_conflicts.py`, `scripts/interactive_stash_resolver*.sh`, `INTERACTIVE_RESOLVER_ISSUES.md`, `TASKMASTER_BRANCH_CONVENTIONS.md` | ❌ Not conflicts — these files intentionally contain `<<<<<<<` strings as data/examples | 6 total |

### The Architectural Shift: `backend/` → `src/`

The migration is **partially complete**, creating a dual-path problem:

```
OLD (still exists):              NEW (canonical target):
backend/                         src/
├── node_engine/                 ├── core/
├── python_backend/              │   ├── database.py      ← DUPLICATE
│   ├── database.py              │   ├── ai_engine.py     ← DUPLICATE
│   ├── ai_engine.py             │   ├── caching.py       ← DUPLICATE
│   └── main.py                  │   ├── factory.py
├── python_nlp/                  │   └── ...
                                 ├── backend/             ← COPY of old backend/
                                 │   ├── python_backend/
                                 │   ├── python_nlp/
                                 │   └── node_engine/
                                 ├── main.py              ← DUPLICATE
                                 └── ...
```

**5 duplicate modules** exist across old and new locations:
- `database.py` → `src/backend/python_backend/` AND `src/core/`
- `ai_engine.py` → `src/backend/python_backend/` AND `src/core/`
- `caching.py` → `src/core/` AND `src/utils/`
- `factory.py` → `src/core/` AND `src/core/data/` AND `src/cli/commands/`
- `main.py` → `src/backend/python_backend/` AND `src/`

---

## 2. Conflict Resolution Plan — Preserving Both Sides

### Resolution Principle

> **Scientific branch provides the structural base; main-line provides tactical improvements to cherry-pick in.**

### Resolution Order (dependencies flow downward)

#### Step 1: `setup/project_config.py` — Establish Canonical Paths First

| Decision | Action |
|----------|--------|
| Take | **Scientific version** (real config system, not a stub) |
| Update | Service path mappings to reflect `src/` migration |
| Update | `get_critical_files()` to point to current canonical files |

```python
# FIX: Update these mappings
"python_backend": "src",           # was: backend/python_backend
"gradio_ui": "src",               # was: backend/python_backend  
"typescript_backend": "backend/server-ts",  # keep (not migrated)
"frontend": "client",             # keep
```

#### Step 2: `setup/validation.py` — Use New Config Paths

| From Scientific (keep) | From Main-line (port) |
|------------------------|----------------------|
| `get_project_config()` integration | Line-by-line conflict scanning for large files |
| Config-driven structure validation | More specific error messages with line numbers |
| Broader environment validation flow | — |

**Critical fix:** Unify Python version constraint — define once, import everywhere (or read from `pyproject.toml`).

**Critical fix:** Exclude false-positive files from conflict marker scanning:
- `benchmark_conflicts.py`
- `scripts/interactive_stash_resolver*.sh`
- `INTERACTIVE_RESOLVER_ISSUES.md`
- `TASKMASTER_BRANCH_CONVENTIONS.md`

#### Step 3: `setup/environment.py` — Keep Env Logic Out of Launcher

| From Scientific (keep) | From Main-line (port) |
|------------------------|----------------------|
| `create_venv`, `get_python_executable`, `get_venv_executable` | Conda detection/helpers (only if `--use-conda` is a supported CLI path) |
| uv dependency install flow | — |
| WSL support (`is_wsl()` via `/proc/version`) | — |
| Notmuch fallback behavior | — |
| NLTK/TextBlob setup | — |

**Discard:** Any imports from `setup.launch` back into `environment.py` (wrong dependency direction, circular import risk).

#### Step 4: `setup/services.py` — Consolidate Service Ownership

| From Scientific (keep) | From Main-line (port) |
|------------------------|----------------------|
| Config-driven service discovery / `validate_services()` | Simpler shared `process_manager` usage |
| Path safety validation | Frontend env var compatibility (`API_URL` + `VITE_API_URL`) |
| Smarter `dev` vs `start` npm script selection | — |
| `PYTHONPATH` handling for backend/Gradio startup | — |
| `setup_node_dependencies()` | — |

**Critical cleanup:** Ensure ONE definition of each function:
- `get_python_executable()`
- `start_backend()`
- `start_node_service()`
- `setup_node_dependencies()`
- `start_gradio_ui()`
- `validate_services()`
- `start_services()`

#### Step 5: `setup/launch.py` — Make It Thin (Last)

After modules are stable, `launch.py` becomes a **thin CLI/orchestration entrypoint only**.

| Keep from Scientific | Keep from Main-line |
|---------------------|---------------------|
| uv-based setup flow | Modular imports from `setup.*` |
| Any scientific-specific CLI flags | `process_manager` import |
| — | Optional command-pattern imports |

**Must NOT contain:**
- Local `ProcessManager` class
- Duplicated `check_python_version`, WSL helpers, env setup, service startup
- Any function that already lives in `setup.validation`, `setup.environment`, or `setup.services`

#### Step 6: Non-code Files

| File | Resolution |
|------|-----------|
| `.gitattributes` | **Take main-line** — adds line-ending normalization (reduces cross-platform noise) |
| `.gemini/commands/speckit.constitution.toml` | Manual merge description text. Lowest priority |
| False-positive files (5) | **No changes needed** — these are not real conflicts |

---

## 3. Import & Test Migration Plan

### 3A. Stale `backend.*` Imports That Must Change

These 6 files still import from the old `backend/` path and will break once `backend/` is removed:

| File | Current Import | Must Change To |
|------|---------------|---------------|
| `tests/backend/node_engine/test_security_manager.py` | `from backend.node_engine.security_manager import SecurityManager` | `from src.backend.node_engine.security_manager import SecurityManager` |
| `tests/test_prompt_engineer.py` | `from backend.python_nlp.ai_training import PromptEngineer` | `from src.backend.python_nlp.ai_training import PromptEngineer` |
| `tests/test_filter_api.py` | `from backend.python_nlp.smart_filters import EmailFilter` | `from src.backend.python_nlp.smart_filters import EmailFilter` |
| `plugins/example_workflow_plugin/__init__.py` | `from backend.python_nlp.smart_filters import SmartFilterManager` | `from src.backend.python_nlp.smart_filters import SmartFilterManager` |
| `plugins/example_workflow_plugin/__init__.py` | `from backend.node_engine.node_base import BaseNode, ...` | `from src.backend.node_engine.node_base import BaseNode, ...` |
| `plugins/example_workflow_plugin/__init__.py` | `from backend.node_engine.workflow_engine import WorkflowEngine` | `from src.backend.node_engine.workflow_engine import WorkflowEngine` |

### 3B. Internal `src/backend/` Files Still Using Old Paths

These files inside `src/backend/` still reference `backend.*` instead of `src.backend.*`:

| File | Count | Example |
|------|-------|---------|
| `src/backend/python_backend/gradio_app.py` | 1 | `from backend.python_nlp.nlp_engine import NLPEngine` |
| `src/backend/python_backend/enhanced_routes.py` | 4 | `from backend.node_engine.email_nodes import ...` |
| `src/backend/python_backend/advanced_workflow_routes.py` | 3 | `from backend.node_engine.security_manager import ...` |
| `src/backend/python_backend/workflow_manager.py` | 1 | deprecation warning referencing old path |
| `src/backend/python_backend/tests/*.py` | 5+ | `from backend.python_backend.database import ...` |

### 3C. Duplicate Module Resolution

| Module | Canonical Location | Action for Duplicate |
|--------|-------------------|---------------------|
| `database.py` | `src/core/database.py` | Keep `src/backend/python_backend/database.py` as compatibility shim → `from src.core.database import *` |
| `ai_engine.py` | `src/core/ai_engine.py` | Same shim pattern |
| `caching.py` | `src/core/caching.py` | Merge unique utils from `src/utils/caching.py`, then delete duplicate |
| `main.py` | `src/main.py` | `src/backend/python_backend/main.py` becomes a shim or is deleted |

### 3D. `conftest.py` Unification

Currently 3 conftest files all hacking `sys.path` differently:

| File | Current Behavior | Recommendation |
|------|-----------------|----------------|
| `./conftest.py` | `sys.path.insert(0, project_root)` | **Keep** — single canonical bootstrap |
| `./tests/conftest.py` | `sys.path.insert(0, parent_of_tests)` | **Simplify** — remove `sys.path` hack, rely on root conftest |
| `./src/backend/python_backend/tests/conftest.py` | `sys.path.insert(0, project_root)` | **Delete or simplify** — redundant with root |

**Better long-term fix:** Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```
Then remove all `sys.path.insert` hacks from conftest files.

### 3E. `sys.path` Hacks Across Codebase (10+ files)

These files manually manipulate `sys.path` and should be cleaned up once the package structure is canonical:

| File | Remove After Migration? |
|------|------------------------|
| `conftest.py` | Keep (or replace with pytest config) |
| `tests/conftest.py` | Remove hack |
| `setup/launch.py` | Remove — use proper package imports |
| `setup/test_config.py` | Remove hack |
| `setup/test_commands.py` | Remove hack |
| `tests/core/test_workflow_engine.py` | Remove hack |
| `tests/test_launcher.py` | Remove hack |
| `tests/test_workflow_engine.py` | Remove hack |
| `tests/modules/dashboard/test_dashboard.py` | Remove hack |
| `src/backend/node_engine/test_sanitization.py` | Remove hack |

---

## 4. Execution Checklist

### Phase 1: Resolve Conflicts (estimated: 2-3 hours)

```
[ ] 1.1  Resolve setup/project_config.py (take scientific, update paths)
[ ] 1.2  Resolve setup/validation.py (scientific base + main-line scan improvements)
[ ] 1.3  Resolve setup/environment.py (scientific base, port conda if needed)
[ ] 1.4  Resolve setup/services.py (scientific base, deduplicate functions)
[ ] 1.5  Resolve setup/launch.py (thin entrypoint, import from setup.*)
[ ] 1.6  Resolve .gitattributes (take main-line)
[ ] 1.7  Resolve .gemini/commands/speckit.constitution.toml (manual merge text)
[ ] 1.8  Confirm false-positive files need no changes (5 files)
```

### Phase 2: Fix Imports (estimated: 1-2 hours)

```
[ ] 2.1  Update 6 files with stale backend.* imports → src.* 
[ ] 2.2  Update src/backend/ internal imports to use src.backend.*
[ ] 2.3  Create compatibility shims for duplicate modules (or delete old copies)
[ ] 2.4  Verify all imports resolve: python -c "import src.core.database" etc.
```

### Phase 3: Fix Tests (estimated: 1-2 hours)

```
[ ] 3.1  Unify conftest.py (one sys.path strategy OR pytest pythonpath config)
[ ] 3.2  Update test imports from backend.* → src.*
[ ] 3.3  Run full test suite: pytest tests/ -v
[ ] 3.4  Fix any failures from import path changes
[ ] 3.5  Remove unnecessary sys.path hacks from 10+ files
```

### Phase 4: Clean Up & Push (estimated: 1 hour)

```
[ ] 4.1  Unstage the 529-file blob
[ ] 4.2  Recommit in logical groups (configs, source, tests, docs, scripts)
[ ] 4.3  Squash/fixup the 3 stash-apply commits
[ ] 4.4  Verify no conflict markers remain: grep -r "<<<<<<< " --include="*.py" .
[ ] 4.5  Verify no secrets staged
[ ] 4.6  Push: git push origin scientific
```

---

## 5. Risks & Guardrails

| Risk | Mitigation |
|------|-----------|
| Python version mismatch across files (`3.11` vs `3.12` vs `3.13`) | Define once in `pyproject.toml`, reference everywhere |
| `project_config` still points at legacy paths after merge | Step 1.1 explicitly updates these |
| Duplicate service functions remain in `services.py` | Step 1.4 requires single-owner-per-function audit |
| Old `backend.*` imports silently work via `sys.path` hacks, masking unfinished migration | Phase 3 removes the hacks so broken imports surface |
| False-positive conflict scanners block CI | Add exclusion list for known tool/doc files |

### One-Owner-Per-Concern Rule

| Concern | Owner Module |
|---------|-------------|
| CLI/orchestration | `setup/launch.py` |
| Environment/deps/venv/conda/WSL | `setup/environment.py` |
| Validation/checks | `setup/validation.py` |
| Service startup/lifecycle | `setup/services.py` |
| Path/service metadata | `setup/project_config.py` |

---

## 6. Open Questions

1. Is `--use-conda` still a supported CLI path? (Determines whether to port conda helpers)
2. Should `backend/` top-level directory be deleted or kept as a symlink to `src/backend/`?
3. Are external plugins depending on `backend.*` imports? (Determines shim vs hard-cut)
4. What is the authoritative Python version range? (`3.11+`? `3.12+`?)

---

*Analysis based on actual conflict inspection, import tracing, and module duplication audit of `~/github/EmailIntelligence` on 2026-03-17.*
