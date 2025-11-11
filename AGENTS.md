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
- **Conda Support**: `python launch.py --conda-env <name>` - Use specific conda environment

### TypeScript/React Frontend
- **Build**: `npm run build` (from client/)
- **Lint**: `npm run lint` (from client/)
- **Dev server**: `npm run dev` (from client/)

## Architecture & Codebase Structure

### Services
- **Python Backend (FastAPI)**: Core API at `backend/python_backend/` with AI engine, database, workflows
- **React Frontend (Vite)**: User interface at `client/` with TypeScript, Tailwind CSS, Radix UI
- **Node.js TypeScript Backend**: Secondary API routes at `server/` with Express, Drizzle ORM
- **Gradio UI**: Interactive interface integrated with Python backend for scientific development

### Key Modules
- **Core Components**: `src/core/` - AI engine, database manager, workflow engines, security
- **Modules**: `modules/` - Pluggable features (categories, AI engine, workflows)
- **Backend Extensions**: `backend/` - Additional Python services, plugins, NLP components
- **Shared Code**: `shared/` - Cross-service utilities and types

### Databases & Storage
- **SQLite**: Primary database (`.db` files in project root and `data/`)
- **JSON Files**: Configuration and cached data in `data/` directory
- **Configurable Data Directory**: Via `DATA_DIR` environment variable

### APIs
- **FastAPI**: Main REST API on port 8000 (`/api/*`)
- **Express**: Secondary Node.js API routes
- **Internal APIs**: Workflow execution, AI model management, performance monitoring

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

<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

**CRITICAL GUIDANCE**

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_workflow_overview()` tool to load the tool-oriented overview (it lists the matching guide tools).

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:
- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and completion
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->
