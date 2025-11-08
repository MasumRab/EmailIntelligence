# EmailIntelligence - Agent Development Guide

## Build/Test Commands
```bash
# Install: uv sync --dev
# Test all: uv run pytest src/backend/ modules/ -v
# Test single: uv run pytest src/backend/tests/test_file.py::TestClass::test_method -v
# Coverage: uv run pytest --cov=src --cov-report=term-missing
# Lint: uv run flake8 src/backend/
# Format: uv run black src/backend/ && uv run isort src/backend/
# Type check: uv run mypy src/backend/ --show-error-codes
```

## Architecture & Codebase Structure
- `src/backend/` - FastAPI backend, email processing, AI analysis, API routes
- `src/core/` - Shared utilities, security, performance monitoring, data management
- `modules/` - Plugin architecture for categories and workflows
- `tests/` - Test suite for backend and modules

## Code Style Guidelines
- **Imports**: Absolute from `src.backend`/`src.core`, group by type, use `isort`
- **Naming**: Classes=`PascalCase`, functions=`snake_case`, constants=`UPPER_CASE`, private=`_prefix`
- **Error Handling**: Custom exceptions, appropriate logging, meaningful API messages
- **Types**: Full annotations, use `typing` imports, `mypy` for checking
