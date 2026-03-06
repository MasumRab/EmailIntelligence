# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-06
**Commit:** 927d7bba
**Branch:** perf-optimizations-ci-fixes-to-main

## OVERVIEW

EmailIntelligence — Full-stack email analysis with AI/NLP. Python FastAPI + Gradio backend, React + TypeScript frontend, Node.js Express secondary backend. Monorepo with active migration from legacy `src/backend/` to modular `modules/` architecture.

## STRUCTURE

```
./
├── src/
│   ├── main.py              # FastAPI + Gradio unified app
│   ├── core/                # Core business logic (8 large files, 5955 lines)
│   ├── backend/
│   │   ├── python_backend/  # DEPRECATED (49 files marked deprecated)
│   │   ├── python_nlp/      # NLP engine, models
│   │   └── node_engine/     # Node-based workflow engine
│   └── context_control/     # Agent context isolation (well-structured)
├── client/                  # React + Vite + TypeScript + wouter
├── server/                  # Express + TypeScript backend
├── modules/                 # Modular feature architecture (auth, email, workflows)
├── setup/                  # Launcher, environment setup
├── deployment/             # Docker configs
└── launch.py               # Unified entry point
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add new feature | `modules/` | New modular architecture |
| Fix backend bug | `src/core/` | Current active backend |
| Fix frontend bug | `client/src/` | React components |
| Legacy code | `src/backend/` | DEPRECATED - avoid |
| Workflow automation | `src/backend/node_engine/` | DAG-based engine |
| AI/NLP changes | `src/backend/python_nlp/` | nlp_engine.py is 1271 lines |

## CODE MAP

| Symbol | Type | Location | Refs | Role |
|--------|------|----------|------|------|
| `nlp_engine.py` | Module | src/backend/python_nlp/ | 1271 lines | CRITICAL - largest file |
| `database.py` | Module | src/core/ | 942 lines | Core infrastructure |
| `smart_filter_manager.py` | Module | src/core/ | 891 lines | Business logic |
| `advanced_workflow_engine.py` | Module | src/core/ | 775 lines | DAG execution |
| `workflow_engine.py` | Module | src/core/ | 685 lines | Legacy workflow |

## CONVENTIONS (THIS PROJECT)

- **Python**: black, flake8, isort, mypy (see pyproject.toml)
- **TypeScript**: Strict mode, path aliases (`@/*` → `client/src/*`)
- **Router**: wouter (not react-router-dom)
- **Entry point**: `launch.py` → `setup/launch.py`
- **Testing**: pytest >= 8.4.0
- **Package manager**: uv for Python, npm for Node.js

## ANTI-PATTERNS (THIS PROJECT)

1. **49 DEPRECATED files** in `src/backend/python_backend/` — Do NOT modify, migration in progress
2. **Zod version mismatch**: Root uses 3.x, client uses 4.x — Avoid shared validation schemas
3. **Dual backend**: Both FastAPI and Express running — Document rationale if adding new endpoints
4. **Duplicate modules**: Both `src/core/` and `src/backend/` have `database.py`, `exceptions.py`, etc. — Use `src/core/` for new code
5. **No ESLint/Prettier**: JavaScript/TypeScript lacks centralized linting

## UNIQUE STYLES

- **Gemini AI workflows**: 4 GitHub workflows using Gemini CLI for autonomous code review/triage
- **Context isolation system**: `src/context_control/` provides branch-based multi-agent isolation
- **Write-behind caching**: Database manager marks dirty data, saves on shutdown
- **Heavy content separation**: Email content in gzipped JSON files, light records in-memory

## COMMANDS

```bash
# Setup
python3 launch.py --setup

# Run all services
python3 launch.py

# Run specific
python3 launch.py --no-client --no-server-ts  # Backend only

# Test
pytest

# Lint
flake8 . && black --check . && mypy src/
```

## NOTES

- Active migration from `src/backend/` to `modules/` — prefer new modular structure
- Large files need refactoring: nlp_engine.py (1271), core/database.py (942), smart_filter_manager.py (891)
- `src/context_control/` is well-structured — use as pattern for new modules
- No monorepo tooling — multiple package.json files scattered
