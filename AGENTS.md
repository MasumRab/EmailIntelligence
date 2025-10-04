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
- **Line length**: 100 chars max, **Formatting**: Black, **Imports**: isort (black profile)
- **Naming**: snake_case functions/vars, CapWords classes, UPPER_CASE constants
- **Types**: Type hints required for all parameters/returns
- **Docstrings**: Google-style for public functions/classes
- **Error handling**: Specific exceptions, meaningful messages, appropriate logging

### TypeScript/React
- **Strict mode**: Enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- **JSX**: react-jsx transform, **Imports**: @/ for client src, @shared/ for shared types
- **Components**: Default export functions, PascalCase naming
- **Styling**: Tailwind CSS utilities, component-specific styles as needed
- **API**: Use api client from lib/api.ts for backend communication

## ⚠️ Critical Code Smells to Avoid
- **Circular Dependencies**: Avoid circular imports (especially AIEngine ↔ DatabaseManager)
- **Hard-coded Paths**: Never hard-code file paths or URLs
- **Missing Type Hints**: Add type hints to all function parameters and return values
- **Inconsistent Naming**: Follow established naming conventions strictly
- **Security**: Never expose secrets/keys, never log sensitive data