# EmailIntelligence Agent Guidelines

## Build/Lint/Test Commands

### Python Backend
- **Test all**: `pytest`
- **Test single file**: `pytest backend/python_backend/tests/test_file.py`
- **Test single function**: `pytest backend/python_backend/tests/test_file.py::TestClass::test_function`
- **Format**: `black .`
- **Lint**: `flake8 .`
- **Import sort**: `isort .`
- **Type check**: `mypy .`
- **Code quality**: `pylint backend`

### TypeScript/React Frontend
- **Build**: `npm run build` (runs tsc && vite build)
- **Lint**: `npm run lint` (eslint with --ext ts,tsx)
- **Dev server**: `npm run dev` (vite)

## Code Style Guidelines

### Python
- **Line length**: 100 characters max
- **Formatting**: Black (auto-formats code)
- **Imports**: isort with black profile, grouped as: stdlib → third-party → local
- **Naming**: snake_case for functions/variables, CapWords for classes, UPPER_CASE for constants
- **Types**: Use type hints for all function parameters and return values
- **Docstrings**: Google-style docstrings for all public functions/classes
- **Error handling**: Specific exceptions, meaningful error messages, appropriate logging
- **Linting**: flake8 (ignores E203, W503), pylint (disables C0111, C0103, C0303, etc.)

### TypeScript/React
- **Strict mode**: Enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- **JSX**: react-jsx transform
- **Imports**: Path mapping with @/ for client src, @shared/ for shared types
- **Components**: Default export functions, PascalCase naming
- **Styling**: Tailwind CSS for utilities, component-specific styles as needed
- **API**: Use api client from lib/api.ts for backend communication

## Project Architecture & Patterns

### Architecture Overview
- **Frontend**: React (client/) with TypeScript, TailwindCSS, Radix UI components, Vite build system
- **Backend**: Python with FastAPI for API endpoints and Gradio for UI
- **AI Engine**: Python-based NLP models for sentiment, intent, topic, and urgency analysis
- **Database**: SQLite for local storage and caching, JSON files for main application data

### Key Patterns to Follow
- Modular structure: separate directories for backend, frontend, and NLP components
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