# EmailIntelligence

EmailIntelligence is a full-stack application that provides intelligent email analysis and management capabilities. It combines a Node.js/TypeScript backend, a Python FastAPI backend for AI/NLP tasks, and a React frontend to deliver a comprehensive email intelligence solution.

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
- [Testing](#testing)

## Project Overview

EmailIntelligence helps users analyze, categorize, and manage their emails more efficiently through:
- Sentiment analysis of email content
- Topic classification and categorization
- Intent recognition
- Urgency detection
- Smart filtering and organization

The project uses a modular architecture with a unified launcher system, comprehensive environment management, and an extensions framework for easy customization.

## Project Structure

The project is organized into the following main components:

- **client/** - React frontend application. See [Client Development Guide](docs/client_development.md) for more details.
- **server/** - Backend services, including Node.js/TypeScript and Python FastAPI components. See [Server Development Guide](docs/server_development.md) for more details.
  - **server/python_nlp/** - Python NLP and AI components
  - **server/python_backend/** - Python FastAPI backend
- **deployment/** - Deployment configurations and scripts. See [Deployment Guide](docs/deployment_guide.md) for details.
- **extensions/** - Extension system for adding custom functionality. See [Extensions Guide](docs/extensions_guide.md) for details.
- **docs/** - Detailed documentation.
- **tests/** - Test suite for the application.
- **launch.py**, **launch.bat**, **launch.sh** - Unified launcher scripts. See [Launcher Guide](docs/launcher_guide.md).

## Prerequisites

To successfully set up and run EmailIntelligence, you will need the following:

*   **Node.js:** Version 18 or later recommended. You can download it from [nodejs.org](https://nodejs.org/).
*   **npm:** Included with Node.js. Used for managing frontend and Node.js backend dependencies.
*   **Python:** Version 3.11 or later recommended (Python 3.11 is particularly advised for Windows). You can download it from [python.org](https://www.python.org/downloads/).
*   **Git:** For cloning the repository. Download from [git-scm.com](https://git-scm.com/).
*   **PostgreSQL:** A running PostgreSQL database instance is required for data storage.
    *   The `DATABASE_URL` environment variable must be configured to point to your PostgreSQL instance (see [Configuration](#configuration)).
    *   For local development, using Docker is highly recommended to set up PostgreSQL easily. See [Database Setup for Development](#database-setup-for-development).
*   **Docker (Recommended for Development):** While not strictly mandatory for running the application if you have an existing PostgreSQL setup, Docker simplifies managing services like PostgreSQL locally. Download from [docker.com](https://www.docker.com/products/docker-desktop).

For detailed Python environment setup, refer to the [Environment Management Guide](docs/env_management.md).

## Quick Start

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

**Step 3: Set up PostgreSQL Database**
Ensure you have a PostgreSQL database running and the `DATABASE_URL` environment variable is set. For local development, the recommended way is:
```bash
# This uses Docker to start a PostgreSQL container and applies database migrations (by running `npm run db:push` internally).
# Ensure Docker is running before executing this command.
npm run db:setup
```
Alternatively, if you have an existing PostgreSQL instance, ensure `DATABASE_URL` is configured to point to it (see [Configuration](#configuration) for details on setting environment variables). You might need to manually apply database migrations using `npm run db:push` after setting up `DATABASE_URL`.

**Step 4: Run the Application using the Launcher**
```bash
# For Windows (ensure Python 3.11+ is your default python or use `py -3.11 launch.py --stage dev`)
launch.bat --stage dev

# For Linux/macOS (ensure Python 3.11+ or Python 3 is available)
chmod +x launch.sh
./launch.sh --stage dev
```
This command will:
- Set up the Python virtual environment and install Python dependencies.
- Download necessary NLTK data.
- Create placeholder AI model files if actual models are not found (see [AI Models Setup](#ai-models-setup) for crucial next steps).
- Start the Python FastAPI AI server (default: port 8000) and the Node.js backend/frontend development server (default: port 5000).

The application will typically be available at http://localhost:5000.

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
2.  Install Node.js dependencies (`npm install`).
3.  Set up the PostgreSQL database (e.g., using `npm run db:setup` with Docker or configuring an existing instance).
4.  Run the unified launcher script (`launch.py` via `launch.bat` or `launch.sh`) with the `--stage dev` flag.

The launcher script (`launch.py`) handles:
- Python virtual environment creation.
- Python dependency installation from `requirements.txt`.
- NLTK data download.
- Creation of placeholder AI model files if they don't exist (this requires follow-up, see below).
- Starting the development servers.
For detailed setup instructions for various environments (local, Docker, staging, production), consult the [Deployment Guide](docs/deployment_guide.md).

Refer to the [Launcher Guide](docs/launcher_guide.md) for more advanced launcher options and troubleshooting.

### AI Models Setup

The application's AI features (sentiment analysis, topic classification, etc.) rely on trained machine learning models (`.pkl` files located in `server/python_nlp/`).

**1. Placeholder Models:**
When you first run `launch.py --stage dev`, it will create empty placeholder files for these models if they are missing (e.g., `intent_model.pkl`, `sentiment_model.pkl`, `topic_model.pkl`, `urgency_model.pkl`). These placeholders **will not** provide any actual AI functionality and will likely cause errors if the AI features are invoked.

**2. Training Actual Models:**
To enable AI features, you **must** replace these placeholders with actual trained models. The script `server/python_nlp/ai_training.py` provides the framework for training these models.

**Challenges and Guidance:**
-   **Training Data:** The `ai_training.py` script currently **does not include training data or direct guidance on acquiring it.** You will need to prepare your own labeled datasets (e.g., CSV files of emails with corresponding topics, sentiments, etc.) to train effective models. This is a non-trivial task and requires data that is representative of what you want to analyze.
-   **Customization Required:** You will likely need to modify `server/python_nlp/ai_training.py` or create wrapper scripts to:
    *   Load your specific datasets.
    *   Configure the `ModelConfig` for each model type (topic, sentiment, intent, urgency) you intend to use.
    *   Train each model using the provided training classes.
    *   Save the trained models using the **exact filenames** expected by the application (e.g., `server/python_nlp/topic_model.pkl`, `server/python_nlp/sentiment_model.pkl`, etc.). The example `main()` in `ai_training.py` saves to a generic name like `model_<ID>.pkl`, which will need to be adjusted to the specific model names loaded by `server/python_nlp/nlp_engine.py`.

**Recommendation:**
Developing or sourcing appropriate training data and adapting the `ai_training.py` script is a significant development task. For a quicker setup to explore non-AI features, you can proceed without fully trained models, but be aware that AI-dependent functionalities will not work.

*(Consider creating a dedicated guide in `docs/ai_model_training_guide.md` for more detailed future instructions on data preparation and model training workflows.)*

### Database Setup for Development

The application requires a PostgreSQL database.
-   **Environment Variable:** Ensure the `DATABASE_URL` environment variable is correctly set to point to your PostgreSQL instance. (Example format: `postgresql://user:password@host:port/database_name`). This is typically managed via a `.env` file in the project root (ensure it's in `.gitignore`) or set in your shell environment.
-   **Recommended Method (Docker):**
    ```bash
    npm run db:setup
    ```
    This command uses `docker-compose` (typically from `deployment/docker-compose.dev.yml` or `docker-compose.yml` if configured for development) to start a PostgreSQL container. It then runs `npm run db:push` (which uses Drizzle ORM) to apply the latest database schema. Ensure Docker is installed and running.
-   **Manual Setup:** If you have an existing PostgreSQL server:
    1.  Create a database for EmailIntelligence.
    2.  Set the `DATABASE_URL` environment variable.
    3.  Run `npm run db:push` to apply schema migrations to your database.

## Configuration

This section details important environment variables used by the application. These can typically be set in a `.env` file in the project root or directly in your shell environment.

*   **`DATABASE_URL`**: Connection string for the PostgreSQL database.
    *   Example: `postgresql://user:password@host:port/database_name`
*   **`GMAIL_CREDENTIALS_JSON`**: JSON content of OAuth 2.0 Client ID credentials for Gmail API.
*   **`credentials.json` (File Alternative)**: Alternative to `GMAIL_CREDENTIALS_JSON`, placed in project root. Ensure this file is in `.gitignore` if used.
*   **`GMAIL_TOKEN_PATH`**: File path for storing Gmail API OAuth 2.0 token (default: `token.json`). Ensure this file is in `.gitignore`.
*   **`NLP_MODEL_DIR`**: Directory for trained NLP models (default: `server/python_nlp/`).
*   **`PORT`**: Port for the Python FastAPI server (default: `8000`).
*   **`NODE_PORT`**: Port for the Node.js server (default: `5000`, though often managed by Vite in dev).

Consult the respective guides in `docs/` for component-specific configurations.

## Security Considerations

When deploying or running this application, please consider the following:
*   **API Authentication:** Implement proper API security for sensitive operations. (Note: Current state might have basic or no auth for some dev routes).
*   **Secret Management:** Securely manage `GMAIL_CREDENTIALS_JSON` (or `credentials.json`) and `token.json`. Use environment variables or a secret manager. Do not commit secrets to Git.
*   **Log Verbosity:** Ensure sensitive information is not excessively logged in production.
*   **CORS Policy:** Restrict CORS policy in `server/python_backend/main.py` for production.
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
# Windows
launch.bat --stage dev

# Linux/macOS
./launch.sh --stage dev
```
This typically starts:
- Python FastAPI AI Server (default: port 8000)
- Node.js Backend and Frontend Development Server (default: port 5000, served by Vite)

For other modes (e.g., API-only, frontend-only) and advanced options, see the [Launcher Guide](docs/launcher_guide.md).
For information on running in Docker, staging, or production environments, see the [Deployment Guide](docs/deployment_guide.md).

### Running the Gradio Scientific UI

For scientific exploration, direct AI model interaction, or testing specific UI components, a Gradio-based interface is available. This is a Python-only, non-Dockerized deployment that runs independently of the main FastAPI backend and Node.js frontend.

To launch the Gradio UI, use the `--gradio-ui` flag with the launcher script:

-   On Linux/macOS:
    ```bash
    ./launch.sh --gradio-ui
    ```
-   On Windows:
    ```bash
    launch.bat --gradio-ui
    ```

You can also specify the host, port, and enable debug or sharing mode using the standard launcher arguments:
    ```bash
    ./launch.sh --gradio-ui --host 0.0.0.0 --port 7860 --debug --share
    ```
This will start the Gradio interface, typically accessible at the specified host and port (Gradio's default is 7860 if `--port` is not provided).

## AI System Overview

The AI and NLP capabilities are primarily based on:
*   Locally trained classification models (e.g., Naive Bayes, Logistic Regression using `scikit-learn` or similar, saved as `.pkl` files) located in `server/python_nlp/`. The training framework for these is in `server/python_nlp/ai_training.py`.
*   Rule-based systems and heuristics can also be part of the NLP pipeline.
The system does not use external Large Language Models (LLMs) by default for its core classification tasks but includes a `PromptEngineer` class in `ai_training.py` which suggests capabilities for LLM interaction if developed further.

## Building for Production

To build the frontend and Node.js backend for production:
```bash
npm run build
```
This command typically uses Vite to build the client and esbuild for the server, placing outputs in a `dist/` directory.

The Python server needs to be run separately in a production environment, typically using a WSGI/ASGI server like Gunicorn or Uvicorn.

For comprehensive information on building and deploying for production, including Docker builds and different environment strategies, please refer to the [Deployment Guide](docs/deployment_guide.md).

## Database

The application uses a PostgreSQL database.
- Configure `DATABASE_URL` environment variable (see [Configuration](#configuration) and [Database Setup for Development](#database-setup-for-development)).
- Schema migrations are handled by Drizzle ORM:
  - `npm run db:push`: Applies schema changes to the database.
  - `npm run db:generate`: Generates new migration files if you change Drizzle schema definitions (typically in `shared/schema.ts` or similar).
  (Or via `python deployment/deploy.py <env> migrate` for Dockerized environments as part of a deployment workflow).

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

## Testing

This project includes unit tests for the Python backend components, primarily focusing on the NLP functionalities.

### Python Test Setup

1.  **Install Python Development Dependencies:**
    Ensure you have Python installed (as per `pyproject.toml`, e.g., Python 3.11+). The development dependencies, including `pytest` and libraries like `textblob` and `nltk`, are listed in `pyproject.toml` under the `[project.group.dev.dependencies]` section. Install them using pip:
    ```bash
    pip install .[dev]
    ```
    (If you encounter issues with this, ensure your pip is up to date (`pip install --upgrade pip`) as support for `project.group` is relatively new. Alternatively, you might need to manually install the packages listed in the `dev` group.)

2.  **NLTK Data (for NLP tests):**
    The NLP tests require certain NLTK data packages. Download the 'punkt' tokenizer data:
    ```bash
    python -m nltk.downloader punkt
    ```

### Running Python Tests

To run all available Python unit tests, use the following npm script:

```bash
npm test
```

This command executes `pytest` with the necessary configurations. It currently runs tests located in `server/python_nlp/tests/` and ensures all these tests pass.

**Important Notes:**

*   **Excluded Tests:** Tests for the main Python backend (`server/python_backend/tests/`) are currently skipped. This is due to their dependency on the `server.python_nlp.action_item_extractor` module, which is not present in the current branch. The testing strategy focuses on the capabilities available within this branch.
*   **TypeScript Tests:** TypeScript-based tests for the frontend or Node.js server components are not executed by the `npm test` command.
