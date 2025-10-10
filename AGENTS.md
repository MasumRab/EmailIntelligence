# EmailIntelligence Agent Guidelines

## Build/Lint/Test Commands
### Python Backend
- **Test all**: `pytest`
- **Test single file**: `pytest tests/test_file.py`
- **Test single function**: `pytest tests/test_file.py::TestClass::test_function`
- **Format**: `black .`
- **Lint**: `flake8 .`
- **Type check**: `mypy .`
<<<<<<< Updated upstream
- **Code quality**: `pylint src modules`

### Dependency Management
- **uv (default)**: `python launch.py --setup` - Uses uv for fast, reliable installs
- **Poetry**: `python launch.py --use-poetry --setup` - Alternative Poetry-based setup
- **Update deps**: `python launch.py --update-deps` - Updates all dependencies
- **CPU PyTorch**: Automatically installs CPU-only PyTorch for lightweight deployment

### TypeScript/React Frontend
- **Build**: `npm run build` (from client/)
- **Lint**: `npm run lint` (from client/)
- **Dev server**: `npm run dev` (from client/)

## Code Style Guidelines
### Python
- **Line length**: 100 chars max, Black formatting, isort imports (stdlib → third-party → local)
- **Naming**: snake_case functions/vars, CapWords classes, UPPER_CASE constants
- **Types**: Type hints required for all parameters/returns
- **Docstrings**: Google-style for public functions/classes
- **Error handling**: Specific exceptions, meaningful messages, logging

### TypeScript/React
- **Strict mode**: Enabled (noUnusedLocals, noUnusedParameters)
- **JSX**: react-jsx transform, @/ for client src, @shared/ for shared types
- **Components**: Default export functions, PascalCase naming
- **Styling**: Tailwind CSS utilities, component-specific styles
- **API**: Use api client from lib/api.ts

<<<<<<< Updated upstream
## Project Architecture & Patterns

### Architecture Overview
- **Frontend**: React (client/) with TypeScript, TailwindCSS, Radix UI components, Vite build system
- **Backend**: Modular Python with FastAPI for API endpoints and Gradio for UI, core in src/, modules in modules/
- **AI Engine**: Python-based NLP models for sentiment, intent, topic, and urgency analysis
- **Database**: SQLite for local storage and caching, JSON files for main application data

### Key Patterns to Follow
- Modular structure: core backend in src/, modular extensions in modules/, frontend in client/
- Local file-based storage: JSON files for main data, SQLite for smart filters and cache
- Launcher script (launch.py) handles environment setup and application startup
- Both unit and integration testing required for Python and TypeScript components

## ⚠️ Critical Code Smells to Avoid

### High Priority (Fix Immediately)
- **Circular Dependencies**: Avoid circular imports, especially between AIEngine and DatabaseManager
- **Inconsistent Exception Handling**: Use specific exceptions with meaningful error messages
- **Hard-coded Paths**: Never hard-code file paths or URLs

### Medium Priority (Address Soon)
- **Missing Type Hints**: Add type hints to all function parameters and return values
- **Code Duplication**: Extract common functionality into reusable functions/classes
- **Large Classes**: Break down classes violating Single Responsibility Principle
- **Inconsistent Naming**: Follow established naming conventions strictly
- **Global State Management**: Avoid global variables; use dependency injection

### General
- **Commits**: Meaningful messages focusing on "why" not "what"
- **Security**: Never expose secrets/keys, never log sensitive data
- **Dependencies**: Check existing usage before adding new libraries
=======
## Critical Rules
- Avoid circular dependencies (AIEngine ↔ DatabaseManager)
- Never hard-code paths or expose secrets
- Use dependency injection over global state
- Check existing dependencies before adding new libraries
>>>>>>> Stashed changes
