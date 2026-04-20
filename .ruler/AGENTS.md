# EmailIntelligence — AI Agent Instructions

## Project Overview
EmailIntelligence is a Python/FastAPI + React/TypeScript full-stack application for intelligent email analysis. Primary language is Python 3.11+.

## Branch Context
This branch (`orchestration-tools`) focuses on CLI tooling, agent infrastructure, and orchestration scripts. The full application backend (AI engine, database, FastAPI routes) lives on the `scientific` branch.

## Code Conventions
- Python: Black formatting, 100 char line length, type hints required, Google-style docstrings
- TypeScript: Strict mode, 2-space indent, semicolons, double quotes
- Shell: `set -euo pipefail`, quote all variables, use `mktemp` for temp files
- Test: pytest for Python, `cd client && npm run lint` for TypeScript

## Build Commands
- Backend: `python launch.py` (wrapper → `setup/launch.py`)
- Frontend: `cd client && npm run build`
- Test: `pytest` (Python), `cd client && npm run lint` (TypeScript)
- Lint: `flake8 .` / `mypy .` / `pylint src modules`

## Key Directories
- `src/cli/` — Modular CLI with subcommands: git, agent, task, analysis, infra, automation
- `src/core/` — Core interfaces, factory, conflict models, exceptions
- `src/strategy/` — Multi-phase resolution strategy, risk assessment, reordering
- `src/analysis/` — Code analysis modules
- `src/resolution/` — Conflict resolution engine
- `src/validation/` — Validation framework
- `src/git/` — Git integration layer
- `src/context_control/` — Context contamination prevention
- `src/utils/` — Shared utility modules
- `cli/` — Root CLI package (backward-compatible entry point via `emailintelligence_cli.py`)
- `setup/` — Unified launcher with DI container, routing, services, settings
- `client/` — React frontend (Vite + Radix UI + TanStack Query + Tailwind)
- `modules/` — Orchestration shell scripts (branch.sh, config.sh, safety.sh, etc.)
- `scripts/` — Automation and orchestration scripts (100+)
- `backend/python_backend/` — Deprecated Pydantic models (active backend is on `scientific`)
- `config/` — Distribution and default configuration
- `docs/handoff/` — Multi-phase agent rules handoff framework

## Task Management
This project uses Task Master AI for task tracking. See `.taskmaster/` for configuration.
Use `task-master list`, `task-master next`, `task-master show <id>` for workflow.

Recommended workflow:
- Start with `task-master next` or `task-master list`, then inspect details with `task-master show <id>`.
- Set the active task to `in-progress` when you begin work, and mark it `done`, `blocked`, `deferred`, or `cancelled` as the outcome becomes clear.
- Record implementation notes, discoveries, and follow-up work with `task-master update-subtask --id=<id> --prompt="..."` or `task-master update-task --id=<id> --prompt="..."`.
- When new work appears, add or decompose it with `task-master add-task --prompt="..."` or `task-master expand --id=<id>`.
- Prefer Task Master CLI or MCP commands over manual edits to files under `.taskmaster/`.

## Critical Rules
- NEVER commit secrets or API keys
- NEVER use `eval()` or `exec()`
- NEVER hard-code file paths
- Use dependency injection over global state
- Add type hints to all function parameters and return values
- Run `bash scripts/verify-agent-content.sh` to verify agent file accuracy after updates
