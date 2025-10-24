# EmailIntelligence Agent Guidelines

## Build/Lint/Test Commands
### Python Backend
- **Test all**: `pytest`
- **Test single file**: `pytest tests/test_file.py`
- **Test single function**: `pytest tests/test_file.py::TestClass::test_function`
- **Format**: `black .`
- **Lint**: `flake8 .`
- **Type check**: `mypy .`
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
- **Error handling**: Specific exceptions, meaningful messages, appropriate logging

### TypeScript/React
- **Strict mode**: Enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- **JSX**: react-jsx transform, **Imports**: @/ for client src, @shared/ for shared types
- **Components**: Default export functions, PascalCase naming
- **Styling**: Tailwind CSS utilities, component-specific styles as needed
- **API**: Use api client from lib/api.ts for backend communication

## Troubleshooting

### Port Binding Errors (e.g., [Errno 10048])
If you encounter port binding errors like "only one usage of each socket address (protocol/network address/port) is normally permitted", it means the port is already in use by another process.

**Procedure to identify and fix:**

1. **Identify the process using the port:**
   ```bash
   netstat -ano | findstr :PORT_NUMBER
   ```
   Replace `PORT_NUMBER` with the conflicting port (e.g., 8000 for backend, 7860 for Gradio).

2. **Note the PID (Process ID) from the output.**

3. **Kill the process:**
   ```bash
   taskkill /f /pid PID_NUMBER
   ```
   Replace `PID_NUMBER` with the PID from step 1.

4. **Verify the port is free:**
   ```bash
   netstat -ano | findstr :PORT_NUMBER
   ```
   Should show no results.

5. **Retry the launch:**
   ```bash
   python launch.py
   ```

**Alternative:** Use different ports by modifying the launch script or passing port arguments.

**Prevention:** Always shut down services properly with Ctrl+C before restarting.


## ⚠️ Critical Rules & Code Smells to Avoid
- **Circular Dependencies**: Avoid circular imports (especially AIEngine ↔ DatabaseManager)
- **Hard-coded Paths**: Never hard-code file paths or URLs
- **Missing Type Hints**: Add type hints to all function parameters and return values
- **Inconsistent Naming**: Follow established naming conventions strictly
- **Security**: Never expose secrets/keys, never log sensitive data
- **Global State**: Use dependency injection over global state
- **Dependencies**: Check existing dependencies before adding new libraries
