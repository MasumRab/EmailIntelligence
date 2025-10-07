# Email Intelligence - Unified Development Environment

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

- **Python:** Version 3.11-3.13
- **Node.js:** Version 18.x or higher (with `npm`)
- **Git:** For cloning the repository

## Getting Started

A single script, `launch.py`, manages the entire development environment, from installing dependencies to running services.

### 1. First-Time Setup

Clone the repository and run the setup command. This will create a Python virtual environment, install all Python and Node.js dependencies, and download necessary machine learning model data.

```bash
git clone <your-repo-url>
cd <repository-name>
python3 launch.py --setup
```

**Alternative: Using Poetry**

If you prefer Poetry for Python dependency management:

```bash
python3 launch.py --use-poetry --setup
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

2.  **Node Engine (Node-based Workflows):**
    -   Located in `backend/node_engine/`.
    -   Provides a modular, extensible node-based workflow system for email processing.
    -   Features specialized nodes for email sourcing, preprocessing, AI analysis, filtering, and action execution.
    -   Includes security and scalability features with audit logging and resource management.

3.  **Gradio UI:**
    -   Located in `backend/python_backend/gradio_app.py`.
    -   Provides a rich, interactive interface for scientific development, model testing, and data visualization. Intended for developers and data scientists.

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

Use `python3 launch.py --help` to see all available options.

## Development Notes

-   **Python Environment:** The launcher automatically creates and manages a virtual environment in the `./venv` directory. You do not need to activate it manually.
-   **Dependencies:** All Python dependencies are defined in `pyproject.toml` and installed with `uv`. All Node.js dependencies are defined in the `package.json` file of the respective `client/` or `server/` directory.
-   **IDE Configuration:** For the best IDE support (e.g., in VS Code), point your Python interpreter to the one inside the `./venv` directory.
-   **Data Storage:** This version uses local file-based storage, primarily located in `backend/python_backend/data/`. SQLite databases (`.db` files) are created in the project root.
-   **Node-based Workflows:** The new node engine in `backend/node_engine/` provides a modular, extensible architecture for creating complex email processing workflows. Nodes can be chained together to create sophisticated processing pipelines with security and scalability features.

## Troubleshooting

### Package Installation Issues

If you encounter issues with Python package installation:

1. **PyTorch Installation Fails:**
   - The setup installs CPU-only PyTorch for lightweight deployment
   - If you need GPU support, manually install PyTorch with CUDA after setup

2. **Missing Packages After Setup:**
   - Run `python launch.py --setup` again to verify and reinstall missing packages
   - Check the logs for specific error messages

3. **Using Poetry Instead of uv:**
   - Run `python launch.py --use-poetry --setup` for Poetry-based installation
   - Ensure Poetry is available in your PATH

4. **Uvicorn Not Found:**
   - Uvicorn should be installed automatically
   - If missing, run: `pip install uvicorn[standard]` in the venv

### Common Errors

- **"ModuleNotFoundError"**: Run setup again or check venv activation
- **Permission Errors**: Avoid running as administrator; use regular user account
- **Port Conflicts**: Services will use next available ports if defaults are taken