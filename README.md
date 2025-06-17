# EmailIntelligence

EmailIntelligence is a full-stack application that provides intelligent email analysis and management capabilities. It combines a Node.js/TypeScript backend, a Python FastAPI backend for AI/NLP tasks, and a React frontend to deliver a comprehensive email intelligence solution.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
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

## Quick Start

The fastest way to get EmailIntelligence running locally is using the unified launcher:

```bash
# Windows
launch.bat --stage dev

# Linux/macOS
chmod +x launch.sh
./launch.sh --stage dev
```
This will set up the Python environment, install dependencies, and start the necessary services. The application will typically be available at http://localhost:5000.

For alternative setup methods and more details, see the [Setup](#setup) section below and the [Launcher Guide](docs/launcher_guide.md).

## Documentation

This project includes comprehensive documentation in the `docs/` directory:

- **[Client Development Guide](docs/client_development.md)**: Information about the frontend application, structure, and development.
- **[Server Development Guide](docs/server_development.md)**: Details about the backend components, structure, and development.
- **[Deployment Strategies Overview](docs/deployment_strategies.md)**: Overview of different deployment approaches (local, Docker, staging, production).
- **[Deployment Guide](docs/deployment_guide.md)**: Specific instructions and configurations for deploying the application, primarily focusing on Docker-based setups.
- **[Environment Management Guide](docs/env_management.md)**: Details about the Python environment management system, `launch.py`, and related features.
- **[Launcher Guide](docs/launcher_guide.md)**: Comprehensive information about the unified launcher system (`launch.py`) and its command-line options.
- **[Extensions Guide](docs/extensions_guide.md)**: Information on how to use and develop extensions.
- **[Python Style Guide](docs/python_style_guide.md)**: Coding standards for Python code in the project.

## Prerequisites

*   Node.js (v18 or later recommended)
*   npm
*   Python (v3.11 or later recommended, as enforced by `launch.py`)

For detailed Python environment setup, refer to the [Environment Management Guide](docs/env_management.md).

## Setup

The primary method for setting up EmailIntelligence is using the unified launcher script (`launch.py` via `launch.bat` or `launch.sh`), as shown in the [Quick Start](#quick-start). This script handles:
- Python virtual environment creation.
- Python dependency installation.
- NLTK data download.
- Starting the development servers.

Refer to the [Launcher Guide](docs/launcher_guide.md) for more advanced setup options and troubleshooting.

### Manual Steps (Complementary to Launcher)

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd EmailIntelligence
    ```
2.  **Install Node.js Dependencies:**
    (The launcher doesn't handle this directly; `npm run dev` called by the launcher might, or you might run it as part of your workflow)
    ```bash
    npm install
    ```
3.  **AI Models:**
    The launch script (when run with `--stage dev` or during initial setup) creates placeholder AI model files (`.pkl`) in `server/python_nlp/`. For the application's AI features to function correctly, you **must** replace these with actual trained models. Refer to `server/python_nlp/ai_training.py` for details on model training.

For more detailed information on Python environment setup, see the [Environment Management Guide](docs/env_management.md).

## Configuration

This section details important environment variables used by the application.

*   **`DATABASE_URL`**: Connection string for the PostgreSQL database.
    *   Example: `postgresql://user:password@host:port/database_name`
*   **`GMAIL_CREDENTIALS_JSON`**: JSON content of OAuth 2.0 Client ID credentials for Gmail API.
*   **`credentials.json` (File Alternative)**: Alternative to `GMAIL_CREDENTIALS_JSON`, placed in project root.
*   **`GMAIL_TOKEN_PATH`**: File path for storing Gmail API OAuth 2.0 token (default: `token.json`).
*   **`NLP_MODEL_DIR`**: Directory for trained NLP models (default: `server/python_nlp/`).
*   **`PORT`**: Port for the Python FastAPI server (default: `8000`).

Consult the respective guides in `docs/` for component-specific configurations.

## Security Considerations

When deploying or running this application, please consider the following:
*   **API Authentication:** Implement proper API security for sensitive operations.
*   **Secret Management:** Securely manage `GMAIL_CREDENTIALS_JSON` (or `credentials.json`) and `token.json`. Use environment variables or a secret manager.
*   **Log Verbosity:** Ensure sensitive information is not excessively logged in production.
*   **CORS Policy:** Restrict CORS policy in `server/python_backend/main.py` for production.
*   **Input Validation:** Validate and sanitize all user-supplied and external data.

## Gmail API Integration Setup

To connect to your Gmail account, configure Gmail API access:

1.  **Google Cloud Console:** Enable Gmail API, create OAuth 2.0 Client ID (Desktop app), and download credentials JSON.
2.  **Provide Credentials:**
    *   Set `GMAIL_CREDENTIALS_JSON` environment variable (recommended).
    *   Or, place downloaded JSON as `credentials.json` in project root.
3.  **One-Time Authorization:** The application will guide you through browser authorization, creating `token.json`.
4.  **Scopes Used:** `https://www.googleapis.com/auth/gmail.readonly`.

## Running the Application

The recommended way to run the application for development is using the unified launcher:
```bash
# Windows
launch.bat --stage dev

# Linux/macOS
./launch.sh --stage dev
```
This typically starts:
- Python FastAPI AI Server (default: port 8000)
- Node.js Backend and Frontend Development Server (default: port 5000)

For other modes (e.g., API-only, frontend-only) and advanced options, see the [Launcher Guide](docs/launcher_guide.md).
For information on running in Docker, staging, or production environments, see the [Deployment Guide](docs/deployment_guide.md).

## AI System Overview

The AI and NLP capabilities are primarily based on:
*   Locally trained classification models (e.g., Naive Bayes, Logistic Regression) in `server/python_nlp/`.
*   Rule-based systems and heuristics.
The system does not use external Large Language Models (LLMs) by default.

## Building for Production

To build the frontend and Node.js backend for production:
```bash
npm run build
```
The Python server needs to be run separately in a production environment, typically using a WSGI server like Gunicorn.

For comprehensive deployment strategies, including Docker builds, refer to the [Deployment Strategies Overview](docs/deployment_strategies.md) and the [Deployment Guide](docs/deployment_guide.md).

## Database

The application uses a PostgreSQL database.
- Configure `DATABASE_URL` environment variable.
- Schema push/migrations can be handled by:
  ```bash
  npm run db:push
  ```
  (Or via `python deployment/deploy.py <env> migrate` for Dockerized environments).

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
