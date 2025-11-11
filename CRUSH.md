<<<<<<< HEAD
# EmailIntelligence Agent Guidelines

## Build/Lint/Test Commands
### Python Backend
- **Test all**: `pytest`
- **Test single file**: `pytest tests/test_file.py`
- **Test single function**: `pytest tests/test_file.py::TestClass::test_function`
- **Format**: `black .`
- **Lint**: `flake8 . && pylint python_backend src modules`
- **Type check**: `mypy .`
- **Dependency Update**: `python launch.py --update-deps`

### TypeScript/React Frontend
- **Build**: `npm run build` (from client/)
- **Lint**: `npm run lint` (from client/)
- **Dev server**: `npm run dev` (from client/)

## Code Style Guidelines
### Python
- **Formatting**: Black (line length 100), isort (black profile)
- **Naming**: `snake_case` (functions/vars), `CapWords` (classes), `UPPER_CASE` (constants)
- **Types**: Type hints required for all parameters/returns
- **Docstrings**: Google-style for public functions/classes
- **Error handling**: Specific exceptions, meaningful messages, logging

### TypeScript/React
- **Strict mode**: Enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- **JSX**: react-jsx transform
- **Imports**: `@/` (client src), `@shared/` (shared types)
- **Components**: `PascalCase` naming, default export functions
- **Styling**: Tailwind CSS
- **API**: Use client from `lib/api.ts`

## ⚠️ Critical Rules to Follow
- Rigorously adhere to existing project conventions when reading or modifying code.
- Analyze surrounding code, tests, and configuration first before making changes.
- Mimic code style, framework choices, naming conventions, typing, and architectural patterns.
- NEVER assume a library/framework is available without verifying its established usage.
- Check imports, configuration files, or neighboring files to confirm usage before employing any library.
- Follow existing code style and structure strictly.
- Use existing libraries and utilities already established in the project.
- Follow existing architectural patterns.
- Understand local context (imports, functions/classes) to ensure changes integrate naturally.
- Make changes that are idiomatic to the existing codebase.
- Check existing dependencies before adding new libraries.
- Follow security best practices.

- No circular dependencies
- No hard-coded paths/secrets
- Strict typing (full annotations)
- Consistent naming conventions
- Security: Never expose or log sensitive data
- Global State: Use dependency injection over global state
=======
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
