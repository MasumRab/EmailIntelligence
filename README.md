# Email Intelligence - Unified Development Environment

<<<<<<< HEAD
Welcome to the Email Intelligence project! This repository contains a complete ecosystem for building, testing, and running a sophisticated email analysis application. It includes a Python backend for core logic and AI, a Gradio interface for scientific development, a TypeScript backend for handling certain API routes, and a React-based web client.

This README provides a unified guide to setting up and running all components using the central `launch.py` script.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Launcher Usage](#launcher-usage)
- [Development Notes](#development-notes)

## Prerequisites

- **Python:** Version 3.12.x
- **Node.js:** Version 18.x or higher (with `npm`)
- **Git:** For cloning the repository
=======
This is a streamlined version of the Email Intelligence application, focusing on core functionalities for local scientific and development use. It features a simplified environment setup, a full-stack architecture with a Python backend and a React frontend, and local file-based data storage. The application leverages AI and NLP to automatically analyze, categorize, and manage emails.

## Key Features

*   **AI-Powered Email Analysis**: Automatically analyzes email content for topic, sentiment, intent, and urgency.
*   **Smart Categorization**: Suggests and applies categories to emails based on AI analysis.
*   **Intelligent Filtering**: Provides a system for creating and managing smart filters to automate email workflows.
*   **Local Data Storage**: Uses a combination of JSON files and SQLite for easy setup and data management.
*   **Comprehensive API**: A FastAPI backend provides a rich set of endpoints for managing emails, categories, and AI operations.
*   **Modern Frontend**: A responsive user interface built with React, TypeScript, and Vite.
*   **Unified Launcher**: A single `launch.py` script handles environment setup, dependency installation, and application startup.

## Project Architecture

The repository is organized into the following main directories:

*   `backend/`: Contains the Python backend, including the FastAPI application (`python_backend/`) and the core NLP logic (`python_nlp/`).
*   `client/`: The frontend React/Vite application.
*   `server/`: Contains TypeScript code related to the server, such as routes and services.
*   `shared/`: Holds shared code, such as Zod schemas, used by both the frontend and backend.
*   `tests/`: Contains tests for the various parts of the application.

## Prerequisites

*   **Python:** Version 3.11.x or 3.12.x is required.
*   **Node.js:** A recent LTS version (e.g., 18.x or 20.x) is recommended.
*   **Git:** For cloning the repository.
>>>>>>> origin/feature/git-history-analysis-report

## Getting Started

<<<<<<< HEAD
A single script, `launch.py`, manages the entire development environment, from installing dependencies to running services.

### 1. First-Time Setup

Clone the repository and run the setup command. This will create a Python virtual environment, install all Python and Node.js dependencies, and download necessary machine learning model data.

```bash
git clone <your-repo-url>
cd <repository-name>
python3 launch.py --setup
```

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

The application is composed of four main, interconnected services:

1.  **Python Backend (FastAPI):**
    -   Located in `backend/python_backend/`.
    -   Serves the primary REST API for core application logic, data processing, and AI/NLP tasks.
    -   Manages data storage (JSON files and SQLite databases).

2.  **Gradio UI:**
    -   Located in `backend/python_backend/gradio_app.py`.
    -   Provides a rich, interactive interface for scientific development, model testing, and data visualization. Intended for developers and data scientists.

3.  **TypeScript Backend (Node.js):**
    -   Located in `server/`.
    -   A secondary backend that handles specific API routes, demonstrating a polyglot microservice architecture.

4.  **React Frontend (Vite):**
    -   Located in `client/`.
    -   The main user-facing web application for end-users to interact with the Email Intelligence service.

## Directory Structure

```
.
├── backend/
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
=======
1.  **Clone the Repository:**
    ```bash
    git clone <your_repo_url>
    cd <repository_name>
    ```

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
>>>>>>> origin/feature/git-history-analysis-report

-   **Run only the Python backend and Gradio UI:**
    ```bash
    python3 launch.py --no-client --no-server-ts
    ```
-   **Run only the React client:**
    ```bash
    python3 launch.py --no-backend --no-ui --no-server-ts
    ```
-   **Run in "API only" mode (just the Python backend):**
    ```bash
    python3 launch.py --no-client --no-server-ts --no-ui
    ```

<<<<<<< HEAD
Use `python3 launch.py --help` to see all available options.

## Development Notes

-   **Python Environment:** The launcher automatically creates and manages a virtual environment in the `./venv` directory. You do not need to activate it manually.
-   **Dependencies:** All Python dependencies are defined in `pyproject.toml` and installed with `uv`. All Node.js dependencies are defined in the `package.json` file of the respective `client/` or `server/` directory.
-   **IDE Configuration:** For the best IDE support (e.g., in VS Code), point your Python interpreter to the one inside the `./venv` directory.
-   **Data Storage:** This version uses local file-based storage, primarily located in `backend/python_backend/data/`. SQLite databases (`.db` files) are created in the project root.
=======
## Data Storage

This version uses local file-based storage for simplicity:

*   **Main Application Data:** Email data, categories, and user information are stored as JSON files in the `backend/data/` directory.
*   **Smart Filter Rules:** Configuration for smart filters is stored in an SQLite database file named `smart_filters.db` in the `backend/python_nlp/` directory.
*   **Email Cache:** A local cache for fetched email content is stored in `email_cache.db` in the `backend/` directory.
*   **Synchronization Checkpoints**: Checkpoints for incremental email syncs are stored in `sync_checkpoints.db` in the `backend/python_nlp/` directory.

These files will be created automatically when the application runs if they do not already exist.

## Running Tests

The project includes a suite of tests to ensure code quality and correctness. To run the tests, use the `launch.py` script with the `--stage test` flag:

```bash
python launch.py --stage test
```

This will execute the default test suite, which includes both unit and integration tests.

## Code Quality and Linting

The project uses a set of tools to maintain code quality and consistency:

*   **Black**, **isort**, and **Pylint** for Python code formatting and linting.
*   **ESLint** and **Prettier** for TypeScript code formatting and linting.

To set up the necessary tools and configurations, run the `setup_linting.py` script:

```bash
python setup_linting.py
```

## Stopping the Application

To stop both the backend and frontend servers, press `Ctrl+C` in the terminal window where `launch.py` is running. The launcher script is designed to shut down all started processes gracefully.
>>>>>>> origin/feature/git-history-analysis-report
