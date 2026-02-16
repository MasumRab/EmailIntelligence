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

You can run any combination of services by using the `--no-<service>` flags.

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

### Other Commands

-   **System Info:** Print debug info about your environment.
    ```bash
    python launch.py --system-info
    ```
-   **Run Tests:** Run the test suite.
    ```bash
    python launch.py --stage test --unit
    ```

## Documentation

This project includes comprehensive documentation:

### Getting Started
- **[Getting Started Guide](docs/getting_started.md)**: Complete setup guide for new developers (under 30 minutes)
- **[Quick Start](#quick-start)**: Fast setup for experienced developers

### Development Guides
- **[Client Development Guide](docs/client_development.md)**: Frontend application structure and development
- **[Server Development Guide](docs/server_development.md)**: Backend components and development
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to the project

### Architecture & Design
- **[Architecture Overview](docs/architecture_overview.md)**: System architecture and design principles
- **[Architecture Decision Records](docs/adr/)**: Key design decisions and their rationale
- **[API Documentation](http://localhost:8000/docs)**: Interactive API documentation (when running)

### Deployment & Operations
- **[Deployment Guide](docs/deployment_guide.md)**: All deployment environments and strategies
- **[Environment Management Guide](docs/env_management.md)**: Python environment management
- **[Launcher Guide](docs/launcher_guide.md)**: Unified launcher system details

### Development Tools
- **[Extensions Guide](docs/extensions_guide.md)**: Using and developing extensions
- **[Python Style Guide](docs/python_style_guide.md)**: Code standards and conventions
- **[Testing Guide](docs/testing_guide.md)**: Testing strategies and tools

## AI Models Setup

The application's AI features (sentiment analysis, topic classification, etc.) rely on trained machine learning models (`.pkl` files located in `backend/python_nlp/`).

**1. Placeholder Models:**
When you first run `launch.py --stage dev`, it will create empty placeholder files for these models if they are missing. These placeholders **will not** provide any actual AI functionality.

**2. Training Actual Models:**
To enable AI features, you **must** replace these placeholders with actual trained models. The script `backend/python_nlp/ai_training.py` provides the framework for training these models. You will need to prepare your own labeled datasets.

## Configuration

Environment variables can be set in a `.env` file in the project root:

*   `DATABASE_URL`: Connection string for the database.
*   `GMAIL_CREDENTIALS_JSON`: JSON content of OAuth 2.0 Client ID credentials.
*   `NLP_MODEL_DIR`: Directory for trained NLP models.
*   `PORT`: Port for the Python FastAPI server.

## Security Considerations

-   **API Authentication:** JWT-based authentication.
-   **Secret Management:** Use environment variables. Do not commit secrets.
-   **Input Validation:** Sanitize all user input.
