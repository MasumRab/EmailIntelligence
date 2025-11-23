# EmailIntelligence Agent Guidelines

## Build/Lint/Test Commands
### Python Backend
- **Test all**: `pytest`
- **Test single file**: `pytest python_backend/tests/test_file.py`
- **Test single function**: `pytest python_backend/tests/test_file.py::TestClass::test_function`
- **Format**: `black .`
- **Lint**: `flake8 . && pylint python_backend`
- **Type check**: `mypy .`

### TypeScript/React Frontend
- **Build**: `cd client && npm run build`
- **Lint**: `cd client && npm run lint`
- **Dev server**: `cd client && npm run dev`

## Code Style Guidelines
### Python
- **Formatting**: Black (line length 100), isort (black profile)
- **Naming**: `snake_case` (functions/vars), `CapWords` (classes), `UPPER_CASE` (constants)
- **Types**: Type hints required for all parameters/returns
- **Docstrings**: Google-style for public functions/classes
- **Error handling**: Specific exceptions, meaningful messages, logging

### TypeScript/React
- **Strict mode**: Enabled
- **Imports**: `@/` (client src), `@shared/` (shared types)
- **Components**: `PascalCase` naming, default export functions
- **Styling**: Tailwind CSS
- **API**: Use client from `lib/api.ts`

## ⚠️ Critical Rules to Follow
- No circular dependencies
- No hard-coded paths/secrets
- Strict typing (full annotations)
- Consistent naming conventions
- Security: Never expose or log sensitive data

