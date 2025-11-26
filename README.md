# Orchestration Tools Branch

This branch (`orchestration-tools`) serves as the **central source of truth** for development environment tooling, configuration management, scripts, and Git hooks that ensure consistency across all project branches.

## Purpose

The primary goal is to keep the core email intelligence codebase clean by separating orchestration concerns from application code. This branch will **NOT** be merged with other branches, but instead provides essential tools and configurations that are synchronized to other branches via Git hooks.

## Files to KEEP (Essential for Orchestration)

### Orchestration Scripts & Tools
- `scripts/` - All orchestration scripts and utilities
  - `install-hooks.sh` - Installs Git hooks for automated environment management
  - `cleanup_orchestration.sh` - Removes orchestration-specific files when not on orchestration-tools
  - `sync_setup_worktrees.sh` - Synchronizes worktrees for different branches
  - `reverse_sync_orchestration.sh` - Reverse synchronization for orchestration updates
  - `cleanup.sh` - Cleanup utilities
  - `lib/` - Shared utility libraries (common.sh, error_handling.sh, git_utils.sh, logging.sh, validation.sh)
  - `hooks/` - Git hook source files (pre-commit, post-checkout, post-commit, post-merge, post-push)

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

### Orchestration Documentation
- `docs/orchestration_summary.md` - Summary of orchestration workflow
- `docs/orchestration_validation_tests.md` - Validation tests for orchestration
- `docs/env_management.md` - Environment management documentation
- `docs/git_workflow_plan.md` - Git workflow planning
- `docs/current_orchestration_docs/` - All orchestration-specific documentation
- `docs/guides/` - Orchestration guides

## Files to REMOVE (Application-Specific)

The following files are NOT needed in this orchestration-focused branch and can be safely removed:

### Application Source Code
- `src/` - Application source code
- `modules/` - Application modules
- `backend/` - Backend implementation
- `client/` - Frontend implementation
- `tests/` - Application tests

### Application Data & Dependencies
- `data/` - Application data
- `node_modules/` - Node.js dependencies
- `performance_metrics_log.jsonl` - Runtime logs

### Application-Specific Configurations
- `.env.example` - Application environment example
- `.mcp.json` - MCP-specific configuration (if application-specific)
- `.rules` - Application-specific rules
- Any documentation files in `docs/` that are not orchestration-related

## Git Hook Behavior

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

1. **Always work in the orchestration-tools branch**
2. **Test your changes thoroughly**
3. **After pushing changes, other developers will receive updates automatically when switching branches**
4. **For immediate updates, run**: `scripts/install-hooks.sh --force`
5. **Refer to**: `docs/orchestration_hook_management.md` for detailed procedures

## Cleanup Strategy

To clean this branch for orchestration-only purposes:

```bash
# Remove application-specific directories
rm -rf src/
rm -rf modules/
rm -rf tests/
rm -rf data/
rm -rf backend/
rm -rf client/
rm -rf node_modules/

# Remove application-specific files
rm -f .env.example
rm -f .mcp.json
rm -f .rules
rm -f performance_metrics_log.jsonl

# Review docs/ and remove non-orchestration documentation
# (Keep orchestration_summary.md, orchestration_validation_tests.md, env_management.md, git_workflow_plan.md, and directories)
```

## Important Notes

<<<<<<< Updated upstream
**Step 3: Database Setup**
The application now uses SQLite. The database file (e.g., `sqlite.db`) will typically be created in the `backend` directory when the application starts or when database operations are first performed. Ensure the `backend` directory is writable.

**Step 4: Run the Application using the Launcher**
```bash
# For Windows (recommended - handles conda/venv automatically)
launch.bat --stage dev

# For Linux/macOS (ensure Python 3.11+ is available)
chmod +x launch.sh
./launch.sh --stage dev

# Or use Python directly (supports conda environments)
python launch.py --stage dev
```
This command will:
- Automatically detect and use conda environments if available, otherwise create/use a virtual environment
- Install Python dependencies using uv (or Poetry if specified)
- Download necessary NLTK data
- Create placeholder AI model files if actual models are not found (see [AI Models Setup](#ai-models-setup) for crucial next steps)
- Start the Python FastAPI AI server (default: port 8000) and the React frontend development server (default: port 5173)

The application will typically be available at http://localhost:5173.

**Environment Options:**
- **Conda users**: The launcher automatically detects conda environments. Use `--conda-env <name>` to specify a particular environment
- **Virtual environment**: Created automatically in `venv/` if conda is not available
- **System Python**: Use `--no-venv` to skip environment creation (not recommended)

**Important Next Steps:**
- **AI Models:** The Quick Start will get the application running, but AI features require trained models. Please see the [AI Models Setup](#ai-models-setup) section below for critical information.

This starts the application in a local development mode. For comprehensive setup instructions, alternative methods, and details on deploying to Docker, staging, or production environments, please refer to the [Launcher Guide](docs/launcher_guide.md) and the [Deployment Guide](docs/deployment_guide.md).

## Documentation

This project includes comprehensive documentation in the `docs/` directory:

- **[Client Development Guide](docs/client_development.md)**: Information about the frontend application, structure, and development.
- **[Server Development Guide](docs/server_development.md)**: Details about the backend components, structure, and development.
- **[Deployment Guide](docs/deployment_guide.md)**: Comprehensive guide covering all deployment environments (local, Docker, staging, production), setup, configuration, deployment strategies, and operational procedures.
- **[Environment Management Guide](docs/env_management.md)**: Details about the Python environment management system, `launch.py`, and related features.
- **[Launcher Guide](docs/launcher_guide.md)**: Comprehensive information about the unified launcher system (`launch.py`) and its command-line options.
- **[Extensions Guide](docs/extensions_guide.md)**: Information on how to use and develop extensions.
- **[Python Style Guide](docs/python_style_guide.md)**: Coding standards for Python code in the project.

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
<<<<<<< HEAD
*   **`GMAIL_TOKEN_PATH`**: File path for storing Gmail API OAuth 2.0 token (default: `token.json`). Ensure this file is in `.gitignore`.
=======
*   **`GMAIL_TOKEN_PATH`**: File path for storing Gmail API OAuth 2.0 token (default: `jsons/token.json`). Ensure this file is in `.gitignore`.
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2
*   **`NLP_MODEL_DIR`**: Directory for trained NLP models (default: `backend/python_nlp/`).
*   **`PORT`**: Port for the Python FastAPI server (default: `8000`).

Consult the respective guides in `docs/` for component-specific configurations.

## Security Considerations

When deploying or running this application, please consider the following:
*   **API Authentication:** JWT-based authentication has been implemented for all sensitive API endpoints. Users must authenticate using the `/api/auth/login` or `/api/token` endpoints to obtain an access token.
*   **Secret Management:** Securely manage `GMAIL_CREDENTIALS_JSON` (or `credentials.json`) and `token.json`. Use environment variables or a secret manager. Do not commit secrets to Git.
*   **Log Verbosity:** Ensure sensitive information is not excessively logged in production.
*   **CORS Policy:** Restrict CORS policy in `backend/python_backend/main.py` for production.
*   **Input Validation:** Validate and sanitize all user-supplied and external data.

## Gmail API Integration Setup

To connect to your Gmail account, configure Gmail API access:

1.  **Google Cloud Console:** Enable Gmail API, create OAuth 2.0 Client ID (Desktop app), and download credentials JSON.
2.  **Provide Credentials:**
    *   Set `GMAIL_CREDENTIALS_JSON` environment variable (recommended).
    *   Or, place downloaded JSON as `credentials.json` in project root. (Ensure it's gitignored).
3.  **One-Time Authorization:** The application will guide you through browser authorization when you first try to access Gmail features, creating `token.json` (or the path specified by `GMAIL_TOKEN_PATH`).
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
=======
- The root `launch.py` wrapper is essential and should be kept for backward compatibility
- The `setup/` directory is critical for environment setup and should be maintained
- All Git hooks in `scripts/hooks/` are essential for the orchestration workflow
- This branch serves as the single source of truth for all environment and tooling configurations
- Changes to orchestration-managed files require PRs through the automated system
>>>>>>> Stashed changes
