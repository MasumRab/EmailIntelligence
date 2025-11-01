# EmailIntelligence - Unified Development Environment

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [AI Models Setup](#ai-models-setup)
  - [Database Setup for Development](#database-setup-for-development)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Gmail API Integration Setup](#gmail-api-integration-setup)
- [Running the Application](#running-the-application)
- [AI System Overview](#ai-system-overview)
- [Building for Production](#building-for-production)
- [Database](#database)
- [Extension System](#extension-system)
- [Debugging Hangs](#debugging-hangs)

## Project Overview

EmailIntelligence is a full-stack application designed to provide intelligent email analysis and management capabilities. The project combines a Python FastAPI backend for AI/NLP tasks with a React frontend and a Gradio-based UI for scientific exploration, offering features such as sentiment analysis, topic classification, intent recognition, urgency detection, and smart filtering.

The application uses a modular architecture with a unified launcher system (`launch.py`), comprehensive environment management, and an extensions framework for customization. It supports multiple interfaces including a standard web interface, a Gradio-based UI for scientific exploration, and a node-based workflow system for creating complex email processing pipelines.

The Gradio UI acts as a full-featured client to the FastAPI backend.

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

Use `python launch.py --help` to see all available options.

## Development Notes

-   **Python Environment:** The launcher automatically creates and manages a virtual environment in the `./venv` directory. You do not need to activate it manually.
-   **Dependencies:** All Python dependencies are defined in `pyproject.toml` and installed with `uv`. All Node.js dependencies are defined in the `package.json` file of the respective `client/` or `server/` directory.
-   **IDE Configuration:** For the best IDE support (e.g., in VS Code), point your Python interpreter to the one inside the `./venv` directory.
-   **Data Storage:** This version uses local file-based storage, primarily located in `backend/python_backend/data/`. SQLite databases (`.db` files) are created in the project root.
-   **Node-based Workflows:** The new node engine in `backend/node_engine/` provides a modular, extensible architecture for creating complex email processing workflows. Nodes can be chained together to create sophisticated processing pipelines with security and scalability features.

## Troubleshooting

2.  **Run the Launcher Script:**
    This script automates the entire setup and launch process.

    *   For Linux/macOS:
        ```bash
        ./launch.sh
        ```
    *   For Windows:
        ```bash
        python launch.py
        ```

    The `launch.py` script will perform the following steps:
    *   Check your Python version and find a compatible interpreter.
    *   Create a Python virtual environment in the `./venv` directory.
    *   Install the required Python dependencies from `requirements.txt`.
    *   Download necessary NLTK data files for text processing.
    *   Install Node.js dependencies for the client application by running `npm install` in the `client/` directory.
    *   Start the Python backend server (FastAPI/Uvicorn), which by default runs on `http://127.0.0.1:8000`.
    *   Start the Vite development server for the frontend, which by default runs on `http://127.0.0.1:5173`.

## Data Storage

The fastest way to get EmailIntelligence running locally for development is by using the unified launcher. This process involves a few key steps:

**Step 1: Clone the Repository**
```bash
git clone <repository_url> # Replace <repository_url> with the actual URL
cd EmailIntelligence
```

**Step 2: Install Node.js Dependencies**
Before running the launcher for the first time, or if frontend/Node.js backend dependencies change, install them:
```bash
npm install
```
This command should be run in the project's root directory (where `package.json` is located).

**Step 3: Database Setup**
The application now uses SQLite. The database file (e.g., `sqlite.db`) will typically be created in the `backend` directory when the application starts or when database operations are first performed. Ensure the `backend` directory is writable.

**Step 4: Run the Application using the Launcher**
```bash
# For Windows (recommended - handles conda/venv automatically)
launch.bat --stage dev

# For Linux/macOS (ensure Python 3.12+ is available)
chmod +x launch.sh
./launch.sh --stage dev

# Or use Python directly (supports conda environments)
python launch.py --stage dev
```
This command will:
- Automatically detect and use conda environments if available, otherwise create/use a virtual environment
- Install Python dependencies using uv
- Download necessary NLTK data
- Create placeholder AI model files if actual models are not found (see [AI Models Setup](#ai-models-setup) for crucial next steps)
- Start the Python FastAPI AI server (default: port 8000) and the React frontend development server (default: port 5173)

The application will typically be available at http://localhost:5173.

**Environment Options:**
- **Conda users**: The launcher automatically detects conda environments. Use `--conda-env <name>` to specify a particular environment
- **Virtual environment**: Created automatically in `venv/` if conda is not available
- **System Python**: Use `--no-venv` to skip environment creation (not recommended)
- **CPU-only setup**: For systems without NVIDIA GPUs, see [CPU_SETUP.md](CPU_SETUP.md) for NVIDIA-free installation

**Important Next Steps:**
- **AI Models:** The Quick Start will get the application running, but AI features require trained models. Please see the [AI Models Setup](#ai-models-setup) section below for critical information.

This starts the application in a local development mode. For comprehensive setup instructions, alternative methods, and details on deploying to Docker, staging, or production environments, please refer to the [Launcher Guide](docs/launcher_guide.md) and the [Deployment Guide](docs/deployment_guide.md).

## Local Development Setup

For a more controlled setup process, especially for new contributors or clean environments, follow these detailed steps to set up your local development environment:

### Prerequisites

- **Python 3.12+**: Required for the backend services
- **Node.js 16+**: Required for the frontend (optional if running API-only)
- **Git**: For cloning the repository
- **Conda (optional)**: For conda environment management (venv is used by default)

### Step-by-Step Setup

**1. Clone and Navigate**
```bash
git clone https://github.com/MasumRab/EmailIntelligence.git
cd EmailIntelligence
```

**2. Install Node.js Dependencies**
```bash
npm install
```

**3. Set up Python Environment**

The launcher uses uv for dependency management:

```bash
python launch.py --setup
```
This creates a virtual environment in `venv/`, installs Python dependencies from `pyproject.toml`, and downloads NLTK data.

- **Using Conda:**
  ```bash
  python launch.py --setup --use-conda --conda-env emailintelligence
  ```
  (Replace `emailintelligence` with your preferred environment name)

**4. Verify Setup**
```bash
python launch.py --system-info
```
This prints detailed information about your system, Python environment, and project configuration.

**5. Start Development Services**
```bash
# Windows
launch.bat --stage dev

# Linux/macOS
./launch.sh --stage dev

# Or directly
python launch.py --stage dev
```

### Troubleshooting Common Issues

- **Python Version Error**: Ensure Python 3.12+ is installed and in PATH
- **Node.js Missing**: Install Node.js 16+ from nodejs.org
- **Permission Errors**: On Linux/macOS, ensure scripts are executable: `chmod +x launch.sh`
- **Port Conflicts**: Use `--port` and `--frontend-port` to specify different ports
- **Conda Issues**: If conda is not detected, the launcher falls back to venv

### Testing the Setup

To test your setup in a clean environment:
1. Create a new directory
2. Clone the repository fresh
3. Follow the steps above
4. Verify services start without errors
5. Check that http://localhost:5173 loads the frontend
6. Confirm API endpoints respond at http://localhost:8000/docs

### Development Workflow

After initial setup:
- Use `python launch.py --stage dev` to start all services
- Code changes auto-reload in development mode
- Access frontend at http://localhost:5173
- API documentation at http://localhost:8000/docs
- Gradio UI at http://localhost:7860 (if enabled)

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

## Setup

The primary method for setting up EmailIntelligence for development is using the sequence described in the [Quick Start](#quick-start):
1.  Clone the repository.
2.  Install development dependencies:
    - For Ubuntu/WSL environments, run `./setup_environment_wsl.sh` (requires sudo) to install all necessary system packages and create the Python virtual environment.
    - For other environments, install Node.js dependencies (`npm install`).
3.  Set up the PostgreSQL database (e.g., using `npm run db:setup` with Docker or configuring an existing instance).
4.  Run the unified launcher script (`launch.py` via `launch.bat` or `launch.sh`) with the `--stage dev` flag.

The launcher script (`launch.py`) handles:
- Python virtual environment activation (if created with setup_environment_wsl.sh).
- Python dependency installation from `requirements.txt`.
- NLTK data download.
- Creation of placeholder AI model files if they don't exist (this requires follow-up, see below).
- Starting the development servers.
For detailed setup instructions for various environments (local, Docker, staging, production), consult the [Deployment Guide](docs/deployment_guide.md).

Refer to the [Launcher Guide](docs/launcher_guide.md) for more advanced launcher options and troubleshooting.

### AI Models Setup

The application's AI features (sentiment analysis, topic classification, etc.) rely on trained machine learning models (`.pkl` files located in `backend/python_nlp/`).

**1. Placeholder Models:**
When you first run `launch.py --stage dev`, it will create empty placeholder files for these models if they are missing (e.g., `intent_model.pkl`, `sentiment_model.pkl`, `topic_model.pkl`, `urgency_model.pkl`). These placeholders **will not** provide any actual AI functionality and will likely cause errors if the AI features are invoked.

**2. Training Actual Models:**
To enable AI features, you **must** replace these placeholders with actual trained models. The script `backend/python_nlp/ai_training.py` provides the framework for training these models.

**Challenges and Guidance:**
-   **Training Data:** The `ai_training.py` script currently **does not include training data or direct guidance on acquiring it.** You will need to prepare your own labeled datasets (e.g., CSV files of emails with corresponding topics, sentiments, etc.) to train effective models. This is a non-trivial task and requires data that is representative of what you want to analyze.
-   **Customization Required:** You will likely need to modify `backend/python_nlp/ai_training.py` or create wrapper scripts to:
    *   Load your specific datasets.
    *   Configure the `ModelConfig` for each model type (topic, sentiment, intent, urgency) you intend to use.
    *   Train each model using the provided training classes.
    *   Save the trained models using the **exact filenames** expected by the application (e.g., `backend/python_nlp/topic_model.pkl`, `backend/python_nlp/sentiment_model.pkl`, etc.). The example `main()` in `ai_training.py` saves to a generic name like `model_<ID>.pkl`, which will need to be adjusted to the specific model names loaded by `backend/python_nlp/nlp_engine.py`.

**Recommendation:**
Developing or sourcing appropriate training data and adapting the `ai_training.py` script is a significant development task. For a quicker setup to explore non-AI features, you can proceed without fully trained models, but be aware that AI-dependent functionalities will not work.

*(Consider creating a dedicated guide in `docs/ai_model_training_guide.md` for more detailed future instructions on data preparation and model training workflows.)*

### Database Setup

The application uses an SQLite database. The database file (e.g., `sqlite.db`) is typically located in the `backend` directory. No special setup is usually required beyond ensuring the application has write permissions to create/manage this file.

## Configuration

This section details important environment variables used by the application. These can typically be set in a `.env` file in the project root or directly in your shell environment.

*   **`DATABASE_URL`**: Connection string for the database. For SQLite, this might be `sqlite:sqlite.db` or similar if used, though the application may default to a hardcoded path.
*   **`GMAIL_CREDENTIALS_JSON`**: JSON content of OAuth 2.0 Client ID credentials for Gmail API.
*   **`credentials.json` (File Alternative)**: Alternative to `GMAIL_CREDENTIALS_JSON`, placed in project root. Ensure this file is in `.gitignore` if used.
*   **`GMAIL_TOKEN_PATH`**: File path for storing Gmail API OAuth 2.0 token (default: `jsons/token.json`). Ensure this file is in `.gitignore`.
*   **`NLP_MODEL_DIR`**: Directory for trained NLP models (default: `backend/python_nlp/`).
*   **`PORT`**: Port for the Python FastAPI server (default: `8000`).

Consult the respective guides in `docs/` for component-specific configurations.

## Security Considerations

When deploying or running this application, please consider the following:
*   **API Authentication:** JWT-based authentication has been implemented for all sensitive API endpoints. Users must authenticate using the `/api/auth/login` or `/token` endpoints to obtain an access token.
*   **Secret Management:** Securely manage `GMAIL_CREDENTIALS_JSON` (or `credentials.json`) and `token.json`. Use environment variables or a secret manager. Do not commit secrets to Git.
*   **Log Verbosity:** Ensure sensitive information is not excessively logged in production.
*   **CORS Policy:** Restrict CORS policy in `backend/python_backend/main.py` for production.
*   **Input Validation:** Validate and sanitize all user-supplied and external data.
*   **Security Headers:** The application includes security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS, CSP) to protect against common web vulnerabilities.
*   **Error Handling:** Generic error messages are returned to prevent information disclosure.
*   **Database Security:** SQLite database paths are configurable via environment variables to prevent path traversal attacks.
*   **Common Pitfalls to Avoid:**
    - Never hardcode secrets in source code
    - Always use HTTPS in production
    - Regularly rotate API keys and tokens
    - Implement rate limiting for API endpoints
    - Keep dependencies updated to patch security vulnerabilities

## Gmail API Integration Setup

To connect to your Gmail account, configure Gmail API access:

1.  **Google Cloud Console:** Enable Gmail API, create OAuth 2.0 Client ID (Desktop app), and download credentials JSON.
2.  **Provide Credentials:**
    *   Set `GMAIL_CREDENTIALS_JSON` environment variable (recommended for production).
    *   Or, place downloaded JSON as `credentials.json` in the `jsons/` directory (recommended for development). (The `jsons/` directory is gitignored).
    *   Legacy: Place in project root as `credentials.json` (not recommended).
3.  **One-Time Authorization:** The application will guide you through browser authorization when you first try to access Gmail features, creating `token.json` in the `jsons/` directory (or the path specified by `GMAIL_TOKEN_PATH`).
4.  **Scopes Used:** `https://www.googleapis.com/auth/gmail.readonly`.

## Running the Application

Once [Setup](#setup) is complete (including Node.js dependencies, database, and consideration for AI models):

The recommended way to run the application for development is using the unified launcher:
```bash
# Windows (recommended - handles conda/venv automatically)
launch.bat --stage dev

# Linux/macOS
./launch.sh --stage dev

# Or use Python directly
python launch.py --stage dev
```
This typically starts:
- Python FastAPI AI Server (default: port 8000)
- React Frontend Development Server (default: port 5173, served by Vite)

**Environment Support:**
- **Conda**: Automatically detected and used if available
- **Virtual Environment**: Created automatically if conda not found
- **Custom Conda Environment**: Use `--conda-env <name>` to specify

For other modes (e.g., API-only, frontend-only) and advanced options, see the [Launcher Guide](docs/launcher_guide.md).
For information on running in Docker, staging, or production environments, see the [Deployment Guide](docs/deployment_guide.md).

### Running the Gradio Scientific UI

For scientific exploration, direct AI model interaction, or testing specific UI components, a Gradio-based interface is available. This is a Python-only, non-Dockerized deployment that runs independently of the main FastAPI backend and React frontend.

To launch the Gradio UI, use the `--gradio-ui` flag with the launcher script:

-   On Linux/macOS:
    ```bash
    ./launch.sh --gradio-ui
    ```
-   On Windows:
    ```bash
    launch.bat --gradio-ui
    ```
-   Or directly with Python:
    ```bash
    python launch.py --gradio-ui
    ```

You can also specify the host, port, and enable debug or sharing mode using the standard launcher arguments:
    ```bash
    python launch.py --gradio-ui --host 0.0.0.0 --port 7860 --debug --share
    ```
This will start the Gradio interface, typically accessible at the specified host and port (Gradio's default is 7860 if `--port` is not provided). The launcher automatically handles conda/venv environment detection.

## AI System Overview

The AI and NLP capabilities are primarily based on:
*   Locally trained classification models (e.g., Naive Bayes, Logistic Regression using `scikit-learn` or similar, saved as `.pkl` files) located in `backend/python_nlp/`. The training framework for these is in `backend/python_nlp/ai_training.py`.
*   Rule-based systems and heuristics can also be part of the NLP pipeline.
The system does not use external Large Language Models (LLMs) by default for its core classification tasks but includes a `PromptEngineer` class in `ai_training.py` which suggests capabilities for LLM interaction if developed further.

## Building for Production

To build the frontend for production:
```bash
npm run build
```
This command typically uses Vite to build the client, placing outputs in a `dist/` directory.

The Python server needs to be run separately in a production environment, typically using a WSGI/ASGI server like Gunicorn or Uvicorn.

For comprehensive information on building and deploying for production, including Docker builds and different environment strategies, please refer to the [Deployment Guide](docs/deployment_guide.md).

## Deployment with Docker

The project includes Dockerfiles and a `deploy.py` script to simplify building and deploying the application using Docker Compose.

### Prerequisites
- Docker and Docker Compose installed.

### Usage
Use the `deployment/deploy.py` script to manage your Docker deployments. It supports `dev` and `prod` environments.

**Build Images:**
```bash
python deployment/deploy.py <environment> build
# Example: python deployment/deploy.py prod build
```

**Start Services:**
```bash
python deployment/deploy.py <environment> up
# Example: python deployment/deploy.py dev up -d
```

**Stop Services:**
```bash
python deployment/deploy.py <environment> down
```

**View Logs:**
```bash
python deployment/deploy.py <environment> logs
```

For more details, refer to `deployment/README.md`.

## Database

The application now uses an SQLite database (e.g., `sqlite.db` in the `backend` directory).
- If `DATABASE_URL` is used, it should be set for SQLite (e.g., `sqlite:backend/sqlite.db`). Otherwise, the application defaults to a local file path.

## Extension System

EmailIntelligence features an extension system for adding custom functionality.
- Manage extensions using `launch.py` (e.g., `--list-extensions`, `--install-extension`).
- For developing extensions and more details, see the [Extensions Guide](docs/extensions_guide.md) and the [Environment Management Guide](docs/env_management.md#extension-system).

## Debugging Hangs

### Debugging Pytest Hangs
*   Use `pytest -vvv` or `pytest --capture=no`.
*   Isolate tests: `pytest path/to/test_file.py::test_name`.
*   Use `breakpoint()` or `import pdb; pdb.set_trace()`.
*   Check for timeouts logged by `deployment/run_tests.py`.

### Debugging NPM/Build Hangs
*   Examine verbose output (e.g., Vite's `--debug`, esbuild's `--log-level=verbose`).
*   Use `node --inspect-brk your_script.js`.
*   Check resource limits (memory, CPU).
*   Try cleaning cache/modules: `npm cache clean --force`, remove `node_modules` & `package-lock.json`, then `npm install`.

### General Debugging on Linux
*   Monitor resources: `top`, `htop`, `vmstat`.
*   Trace system calls: `strace -p <PID>`.
*   Check kernel messages: `dmesg -T`.
*   Ensure adequate disk space.

For more detailed guides and specific component documentation, please refer to the [Documentation](#documentation) section.

## Known Vulnerabilities

- Four moderate severity vulnerabilities related to `esbuild` persist as of the last audit.
- These vulnerabilities are due to `drizzle-kit` (and its transitive dependencies like `@esbuild-kit/core-utils`) requiring older, vulnerable versions of `esbuild`. Specifically, `drizzle-kit`'s dependency tree pulls in `esbuild@0.18.20` and `esbuild@0.19.12`, both of which are vulnerable (<=0.24.2).
- Attempts to override these nested `esbuild` versions to a non-vulnerable version (e.g., `^0.25.5`, which is used by other parts of this project like Vite) using npm's `overrides` feature in `package.json` were made. However, these overrides were not fully effective, with `npm list` indicating version incompatibilities for the overridden packages. `npm audit` continued to report the vulnerabilities.
- These `esbuild` vulnerabilities cannot be fully remediated without an update to `drizzle-kit` itself that addresses its `esbuild` dependency requirements, particularly for the deprecated `@esbuild-kit/*` packages.
- On a related note, `vite` and `@vitejs/plugin-react` were successfully updated to their latest compatible versions (`vite@6.3.5` and `@vitejs/plugin-react@4.5.2` respectively) during the audit process to address other potential issues and ensure compatibility.
