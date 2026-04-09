# EmailIntelligence — AI Agent Instructions

## Project Overview
EmailIntelligence is a Python/FastAPI + React/TypeScript full-stack application for intelligent email analysis. Primary language is Python 3.11+.

## Code Conventions
- Python: Black formatting, 100 char line length, type hints required, Google-style docstrings
- TypeScript: Strict mode, 2-space indent, semicolons, double quotes
- Test: pytest for Python, npm run test for TypeScript

## Build Commands
- Backend: `python launch.py`
- Frontend: `cd client && npm run build`
- Test: `pytest` (Python), `cd client && npm run lint` (TypeScript)
- Lint: `flake8 .` / `mypy .` / `pylint src modules`

## Key Directories
- `src/core/` — AI engine, database manager, workflow engines
- `backend/python_backend/` — FastAPI backend
- `client/` — React frontend (Vite)
- `modules/` — Pluggable feature modules
- `rules/` — Shared YAML linting rules

## Task Management
This project uses Task Master AI for task tracking. See `.taskmaster/` for configuration.
Use `task-master list`, `task-master next`, `task-master show <id>` for workflow.

## Critical Rules
- NEVER commit secrets or API keys
- NEVER use `eval()` or `exec()`
- NEVER hard-code file paths
- Use dependency injection over global state
- Add type hints to all function parameters and return values
