# Manual Setup & Troubleshooting Guide

This document provides instructions for manual environment setup and solutions to common problems. For most users, the automated `launch.py` script is the recommended way to manage the project.

**Primary Method:** Use the [main README.md guide](README.md) and the `launch.py` script for a one-command setup and launch experience.

## Table of Contents
- [When to Use This Guide](#when-to-use-this-guide)
- [Manual Environment Setup](#manual-environment-setup)
  - [1. Python Environment (venv)](#1-python-environment-venv)
  - [2. Node.js Dependencies](#2-nodejs-dependencies)
- [Manual Execution](#manual-execution)
  - [Running the Python Backend](#running-the-python-backend)
  - [Running the Gradio UI](#running-the-gradio-ui)
  - [Running the Node.js Services](#running-the-nodejs-services)
- [Troubleshooting](#troubleshooting)

## When to Use This Guide

You should only need this guide if:
- The `python3 launch.py --setup` command fails for an unknown reason.
- You want to set up the environment manually for debugging purposes.
- You need to run individual components of the application without using the launcher.

## Manual Environment Setup

### 1. Python Environment (venv)

This process creates a virtual environment and installs all Python packages using `uv`.

```bash
# 1. Create a Python 3.12 virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Install the 'uv' package manager into the venv
pip install -U uv

# 4. Install all project dependencies from pyproject.toml
# The --all-extras flag includes development dependencies (for testing, etc.)
uv sync --active --all-extras

# 5. Download NLTK data
python -c "import nltk; [nltk.download(d, quiet=True) for d in ['punkt', 'stopwords', 'wordnet', 'vader_lexicon', 'averaged_perceptron_tagger', 'brown']]"
```

### 2. Node.js Dependencies

This process installs dependencies for both the frontend client and the TypeScript backend.

```bash
# 1. Install dependencies for the React client
npm install --prefix client

# 2. Install dependencies for the TypeScript server
npm install --prefix server
```

## Manual Execution

If you want to run services individually, first activate the Python virtual environment (`source venv/bin/activate`), then run the following commands in separate terminal windows.

### Running the Python Backend

```bash
uvicorn backend.python_backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Running the Gradio UI

```bash
python backend/python_backend/gradio_app.py
```

### Running the Node.js Services

```bash
# To run the frontend client (http://localhost:5173)
npm run dev --prefix client

# To run the TypeScript backend
npm run dev --prefix server
```

## Troubleshooting

-   **`ModuleNotFoundError` in Python:**
    Your virtual environment is likely corrupted or wasn't activated.
    1.  Ensure your venv is active: `source venv/bin/activate`.
    2.  If the error persists, force a clean setup with the launcher: `python3 launch.py --setup --force-recreate-venv`.

-   **`uv` fails with cache errors:**
    Sometimes the `uv` cache can become corrupted. Clear it and reinstall.
    ```bash
    uv cache clean
    uv sync --active --all-extras --reinstall
    ```

-   **Node.js `npm install` fails:**
    This can be due to a corrupted cache or lockfile.
    ```bash
    # For the client
    rm -rf client/node_modules client/package-lock.json
    npm install --prefix client

    # For the server
    rm -rf server/node_modules server/package-lock.json
    npm install --prefix server
    ```

-   **Port Conflicts (`Address already in use`):**
    If a port (e.g., 8000, 5173) is in use, you can either stop the conflicting process or use the launcher's flags to change ports.
    ```bash
    # Run Python backend on port 8001
    python3 launch.py --port 8001
    ```