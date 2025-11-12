<<<<<<< HEAD
# Orchestration Tools Branch
=======
# EmailIntelligence - Unified Development Environment
>>>>>>> scientific

This branch (`orchestration-tools`) serves as the **central source of truth** for development environment tooling, configuration management, scripts, and Git hooks that ensure consistency across all project branches.

## Purpose

The primary goal is to keep the core email intelligence codebase clean by separating orchestration concerns from application code. This branch will **NOT** be merged with other branches, but instead provides essential tools and configurations that are synchronized to other branches via Git hooks.

<<<<<<< HEAD
## Files to KEEP (Essential for Orchestration)
=======
EmailIntelligence is a full-stack application designed to provide intelligent email analysis and management capabilities. The project combines a Python FastAPI backend for AI/NLP tasks with a React frontend and a Gradio-based UI for scientific exploration, offering features such as sentiment analysis, topic classification, intent recognition, urgency detection, and smart filtering.

The application uses a modular architecture with a unified launcher system (`launch.py`), comprehensive environment management, and an extensions framework for customization. It supports multiple interfaces including a standard web interface, a Gradio-based UI for scientific exploration, and a node-based workflow system for creating complex email processing pipelines.
>>>>>>> scientific

### Orchestration Scripts & Tools
- `scripts/` - All orchestration scripts and utilities
  - `install-hooks.sh` - Installs Git hooks for automated environment management
  - `cleanup_orchestration.sh` - Removes orchestration-specific files when not on orchestration-tools
  - `sync_setup_worktrees.sh` - Synchronizes worktrees for different branches
  - `reverse_sync_orchestration.sh` - Reverse synchronization for orchestration updates
  - `cleanup.sh` - Cleanup utilities
  - `handle_stashes.sh` - Automated stash resolution for multiple branches
  - `stash_analysis.sh` - Analyze stashes and provide processing recommendations
  - `stash_details.sh` - Show detailed information about each stash
  - `interactive_stash_resolver.sh` - Interactive conflict resolution for stashes
  - `stash_manager.sh` - Main interface for all stash operations (deprecated, use optimized version)
  - `stash_manager_optimized.sh` - Optimized main interface with improved performance
  - `handle_stashes_optimized.sh` - Optimized automated stash resolution for multiple branches
  - `stash_analysis.sh` - Analyze stashes and provide processing recommendations
  - `stash_details.sh` - Show detailed information about each stash
  - `interactive_stash_resolver_optimized.sh` - Optimized interactive conflict resolution for stashes
  - `lib/` - Shared utility libraries (common.sh, error_handling.sh, git_utils.sh, logging.sh, validation.sh)
  - `hooks/` - Git hook source files (pre-commit, post-checkout, post-commit, post-merge, post-push)

<<<<<<< HEAD
### Setup & Environment Management
- `setup/` - Launch scripts and environment setup
  - `launch.py` - Main launcher with environment setup functionality
  - `pyproject.toml` - Python project configuration
  - `requirements.txt` - Runtime dependencies
  - `requirements-dev.txt` - Development dependencies
  - `setup_environment_*.sh` - Environment setup scripts
  - `launch.*` - Cross-platform launch scripts

### Configuration Files
- `.flake8`, `.pylintrc` - Python linting configuration
- `.gitignore`, `.gitattributes` - Git configuration
- `launch.py` (root wrapper) - Forwards to setup/launch.py (backward compatibility)

### Agent Context & Development Environment Files
- `AGENTS.md` - Task Master and agent integration guide
- `CLAUDE.md` - Claude Code auto-loaded context and MCP configuration
- `.claude/` - Claude Code integration directory (settings, custom commands)
- `.mcp.json` - MCP server configuration for agent tools integration
- `.context-control/profiles/` - Context profiles for branch-specific agent access control
- `.specify/` - Agent specification and rule files
- `.taskmaster/` - Task Master configuration and task management

### Orchestration Documentation
- `docs/orchestration_summary.md` - Summary of orchestration workflow
- `docs/orchestration_validation_tests.md` - Validation tests for orchestration
- `docs/env_management.md` - Environment management documentation
- `docs/git_workflow_plan.md` - Git workflow planning
- `docs/stash_resolution_procedure.md` - Basic procedure for resolving stashes
- `docs/complete_stash_resolution_procedure.md` - Complete procedure with all details
- `docs/interactive_stash_resolution.md` - Guide to using interactive conflict resolution
- `docs/stash_management_tools.md` - Comprehensive guide to stash management tools
- `docs/stash_scripts_improvements.md` - Summary of improvements made to stash scripts
- `docs/current_orchestration_docs/` - All orchestration-specific documentation
- `docs/guides/` - Orchestration guides

## Files to REMOVE (Application-Specific)

The following files are NOT needed in this orchestration-focused branch and can be safely removed:

### Application Source Code
- `src/` - Application source code (except `src/core/` if shared with core utilities)
- `modules/` - Application modules
- `backend/` - Backend implementation
- `client/` - Frontend implementation
- `tests/` - Application tests
- `plugins/` - Plugin implementations

### Application Data & Dependencies
- `data/` - Application data
- `node_modules/` - Node.js dependencies
- `performance_metrics_log.jsonl` - Runtime logs
- `.venv/` - Virtual environment (will be recreated)
- `venv/` - Alternative virtual environment directory
=======
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
>>>>>>> scientific

### Deprecated or Redundant Files
- `.rules` - Application-specific rules (keep integration settings, remove app-specific rules)
- `.env.example` - Application environment example (keep shared environment config templates only)
- Old deployment configs or scripts unrelated to orchestration setup
- Any documentation files in `docs/` that are application-specific (not orchestration-related)

## Git Hook Behavior

<<<<<<< HEAD
### `pre-commit` Hook
- **Purpose**: Prevent accidental changes to orchestration-managed files
- **Behavior**: Allows all changes on orchestration-tools; warns on orchestration-managed file changes on other branches

### `post-checkout` Hook
- **Purpose**: Sync essential files when switching branches
- **Behavior**: Syncs setup/ directory, shared configs, and installs hooks when switching FROM orchestration-tools; skips sync when switching TO orchestration-tools

### `post-merge` Hook
- **Purpose**: Ensure environment consistency after merges
- **Behavior**: Syncs setup/ directory, installs/updates Git hooks, cleans up temporary worktrees

### `post-push` Hook
- **Purpose**: Detect orchestration changes and create PRs
- **Behavior**: Creates automatic draft PRs when orchestration-managed files are changed on non-orchestration branches

## Development Workflow

1. **For orchestration development**: Work directly in `orchestration-tools` branch
2. **For environment setup**: The `setup/` directory contains all necessary tools
3. **For configuration changes**: Make changes in orchestration-tools, they propagate automatically
4. **For Git hook management**: Use `install-hooks.sh` to install consistent hook versions

## Branch Policy

- **This branch will NOT be merged with other branches**
- **Focus only on orchestration tools, scripts, and configurations**
- **Remove application-specific files to keep the branch clean**
- **Maintain backward compatibility for the launch system**
- **Ensure all hooks and automation scripts work correctly**

## Hook Management and Updates

When making changes to orchestration files, follow these important steps:
=======
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
>>>>>>> scientific

1. **Always work in the orchestration-tools branch**
2. **Test your changes thoroughly**
3. **After pushing changes, other developers will receive updates automatically when switching branches**
4. **For immediate updates, run**: `scripts/install-hooks.sh --force`
5. **Refer to**: `docs/orchestration_hook_management.md` for detailed procedures

## Cleanup Strategy

To clean this branch for orchestration-only purposes, follow this comprehensive cleanup guide:

### Phase 1: Remove Application Code
```bash
# Remove application source directories
rm -rf src/backend/ src/core/ src/frontend/  # Keep only src/context_control if shared
rm -rf modules/
rm -rf tests/
rm -rf plugins/
```

### Phase 2: Remove Application Data & Runtime Files
```bash
# Remove runtime artifacts
rm -rf data/
rm -rf node_modules/
rm -rf __pycache__/
rm -rf .pytest_cache/
rm -rf .venv/ venv/
rm -f performance_metrics_log.jsonl
rm -f *.db *.sqlite*
```

### Phase 3: Clean Documentation
```bash
<<<<<<< HEAD
# Keep orchestration docs, remove application-specific documentation
# Keep: docs/orchestration_*.md, docs/env_management.md, docs/git_workflow_plan.md, 
#       docs/stash_*.md, docs/guides/, docs/current_orchestration_docs/
# Remove application-specific docs and READMEs from feature/module directories
```

### Phase 4: Clean Configuration Files
=======
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
>>>>>>> scientific
```bash
# Keep MCP, Claude, and context control configs (for agent integration)
# Keep: .mcp.json, .claude/, AGENTS.md, CLAUDE.md, .context-control/profiles/, .specify/, .taskmaster/

# Remove application-specific configs
rm -f .env.example  # (or keep only shared templates)
rm -f deployment/docker-compose*.yml  # Unless essential for orchestration
rm -f nginx/  # Remove unless used for setup
```

### Phase 5: Documentation Review
After cleanup, run:
```bash
git status --short
# Review remaining files to ensure all are orchestration-related
# Run: git rm --cached <file> to untrack files, then commit
```

### Important: Preserve Agent Integration Context
When cleaning, **DO NOT REMOVE** these files as they are essential for:
- Automated task management with Task Master
- Claude Code context and MCP tool integration
- Branch-specific agent access control
- Development environment consistency

Keep:
- `AGENTS.md` - Essential for agent workflow documentation
- `CLAUDE.md` - Auto-loaded context for AI development tools
- `.claude/` - Custom slash commands and tool configurations
- `.mcp.json` - MCP server configuration for orchestration tools
- `.context-control/` - Context profiles ensuring agents have appropriate access per branch
- `.specify/` - Agent specifications and behavioral rules
- `.taskmaster/` - Task tracking and orchestration task management

## Important Notes

- The root `launch.py` wrapper is essential and should be kept for backward compatibility
- The `setup/` directory is critical for environment setup and should be maintained
- All Git hooks in `scripts/hooks/` are essential for the orchestration workflow
- This branch serves as the single source of truth for all environment and tooling configurations
- Changes to orchestration-managed files require PRs through the automated system
- Agent context files (AGENTS.md, CLAUDE.md, .claude/, .mcp.json, .context-control/, .specify/, .taskmaster/) are CRITICAL for maintaining agent integration and should always be preserved
- These agent integration files are synchronized across all branches via the post-checkout hook to ensure consistent agent access control and task management
- Context control profiles ensure agents have appropriate access per branch (e.g., scientific branch agents don't see orchestration scripts)
- Task Master configurations are used for centralized task tracking and workflow automation across branches