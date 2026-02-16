# EmailIntelligence - Unified Development Environment

EmailIntelligence is a full-stack application designed to provide intelligent email analysis and management capabilities. The project combines a Python FastAPI backend for AI/NLP tasks with a React frontend and a Gradio-based UI for scientific exploration, offering features such as sentiment analysis, topic classification, intent recognition, urgency detection, and smart filtering.

The application uses a modular architecture with a unified launcher system (`launch.py`), comprehensive environment management, and an extensions framework for customization. It supports multiple interfaces including a standard web interface, a Gradio-based UI for scientific exploration, and a node-based workflow system for creating complex email processing pipelines.

```
Gradio UI (gradio_app.py)
=========================
|
├── 📈 Dashboard Tab
|   └── Calls GET /api/dashboard/stats ──> Displays key metrics & charts
|
├── 📥 Inbox Tab
|   ├── Calls GET /api/emails ─────> Displays searchable email list
|   └── Calls GET /api/categories ─> Populates category filter dropdown
|
├── 📧 Gmail Tab
|   └── Calls POST /api/gmail/sync ──> Triggers Gmail synchronization
|
├── 🔬 AI Lab Tab (Advanced Tools)
|   ├── Analysis Sub-Tab ──────────> Calls POST /api/ai/analyze
|   └── Model Management Sub-Tab ────> Calls GET/POST /api/models/*
|
└── ⚙️ System Status Tab
    ├── Calls GET /health ───────────> Displays system health
    └── Calls GET /api/gmail/performance -> Displays performance metrics
```

## Prerequisites

- **Python 3.12+**: Required for the backend services
- **Node.js 16+**: Required for the frontend (optional if running API-only)
- **Git**: For cloning the repository
- **Conda (optional)**: For conda environment management (venv is used by default)

## Getting Started

A single script, `launch.py`, manages the entire development environment, from installing dependencies to running services.

### 1. First-Time Setup

Clone the repository and run the setup command. This will create a Python virtual environment, install all Python and Node.js dependencies, and download necessary machine learning model data.

```bash
git clone <your-repo-url>
cd <repository-name>
python3 launch.py --setup
```

**Note:** The setup installs CPU-only PyTorch for lightweight deployment. If you need GPU support, modify the PyTorch installation manually.

### 2. Running the Application

After the one-time setup, use the same script to launch all services:

```bash
python3 launch.py
```

This command will start:
- **Python FastAPI Backend** on `http://127.0.0.1:8000`
- **Gradio UI** on `http://127.0.0.1:7860` (or the next available port)
- **Node.js TypeScript Backend** (port managed by `npm`)
- **React Frontend** on `http://127.0.0.1:5173` (or the next available port)

Press `Ctrl+C` in the terminal to gracefully shut down all running services.

## Project Architecture

The application is composed of five main, interconnected services:

1.  **Python Backend (FastAPI):**
    -   Located in `backend/python_backend/`.
    -   Serves the primary REST API for core application logic, data processing, and AI/NLP tasks.
    -   Manages data storage (JSON files and SQLite databases).

2.  **Gradio UI:**
    -   Located in `backend/python_backend/gradio_app.py`.
    -   Provides a rich, interactive interface for scientific development, model testing, and data visualization. Intended for developers and data scientists.

3.  **Node-Based Workflow Engine:**
    -   Located in `backend/node_engine/`.
    -   Provides a modular, extensible architecture for creating complex email processing workflows.

4.  **TypeScript Backend (Node.js):**
    -   Located in `server/`.
    -   A secondary backend that handles specific API routes, demonstrating a polyglot microservice architecture.

5.  **React Frontend (Vite):**
    -   Located in `client/`.
    -   The main user-facing web application for end-users to interact with the Email Intelligence service.

## Directory Structure

```
.
├── backend/
│   ├── node_engine/      # Node-based workflow engine and specialized email nodes
│   ├── python_backend/   # Main Python FastAPI application and Gradio UI
│   └── python_nlp/       # NLP-specific modules and utilities
├── client/               # React/Vite frontend application
├── server/               # TypeScript/Node.js backend application
├── shared/               # Code/types shared between services
│
├── launch.py             # 🚀 Unified script to set up, manage, and run the project
├── pyproject.toml        # Python dependency definitions (for uv)
├── package.json          # Node.js workspace configuration
│
└── ...
```

## Launcher Usage

The `launch.py` script is the single entry point for all development tasks.

### Environment Management

-   **Force a clean setup:** Delete and recreate the environment from scratch.
    ```bash
    python3 launch.py --setup --force-recreate-venv
    ```
-   **Update all dependencies:**
    ```bash
    python3 launch.py --setup --update-deps
    ```

### Running Specific Services

You can run any combination of services by using the launcher scripts:
-   **Run only the Python backend and Gradio UI:**
    ```bash
    python launch.py --no-client --no-server-ts
    ```
-   **Run only the React client:**
    ```bash
    python launch.py --no-backend --no-ui --no-server-ts
    ```
-   **Run in "API only" mode (just the Python backend):**
    ```bash
    python launch.py --no-client --no-server-ts --no-ui
    ```
-   **Use a specific conda environment:**
    ```bash
    python launch.py --conda-env myenv
    ```

## Development Setup Details

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

## Critical Rules
- Avoid circular dependencies (AIEngine ↔ DatabaseManager)
- Never hard-code paths or expose secrets
- Use dependency injection over global state
- Check existing dependencies before adding new libraries
