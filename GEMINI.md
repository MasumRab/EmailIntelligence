# GEMINI.md

## Project Overview

This is a comprehensive Email Intelligence platform designed for sophisticated email analysis and processing. The project is a full-stack application with a modular, microservices-oriented architecture.

**Core Technologies:**

*   **Python Backend:**
    *   **FastAPI:** Serves the primary REST API for core application logic, data processing, and AI/NLP tasks.
    *   **Gradio:** Provides an interactive web UI for scientific development, model testing, and data visualization.
    *   **Modular Design:** The backend is highly extensible, with core functionality in `src/core` and additional features implemented as modules in the `modules/` directory.
*   **TypeScript Backend (Node.js):**
    *   Located in the `server/` directory, this backend handles specific API routes, demonstrating a polyglot microservice architecture.
*   **React Frontend (Vite):**
    *   The main user-facing web application, located in the `client/` directory.
*   **Node-Based Workflow Engine:**
    *   A sophisticated, extensible workflow system inspired by ComfyUI and other node-based processing frameworks. This allows for the creation of complex, chained processing pipelines for emails.
*   **Data Storage:**
    *   The application uses a combination of local file-based storage (JSON files in `data/`) and SQLite databases for caching and data management.

## Building and Running

The entire development environment is managed by the central `launch.py` script.

**First-Time Setup:**

To set up the project for the first time, including creating a Python virtual environment, installing all Python and Node.js dependencies, and downloading necessary machine learning models, run:

```bash
python launch.py --setup
```

**Running the Application:**

To launch all services (Python backend, Gradio UI, TypeScript backend, and React frontend), run:

```bash
python launch.py
```

The services will be available at the following default ports:

*   **Python FastAPI Backend:** `http://127.0.0.1:8000`
*   **Gradio UI:** `http://127.0.0.1:7860`
*   **React Frontend:** `http://127.0.0.1:5173`

**Running Specific Services:**

You can run specific services by using the `--no-<service>` flags. For example, to run only the Python backend and Gradio UI, use:

```bash
python launch.py --no-client --no-server-ts
```

For more options, run `python launch.py --help`.

## Development Conventions

*   **Modular Architecture:** New features should be added as modules in the `modules/` directory to maintain a clean and extensible codebase.
*   **Dependency Management:**
    *   Python dependencies are defined in `pyproject.toml` and managed with `uv` (or optionally, Poetry).
    *   Node.js dependencies are defined in the `package.json` files within the `client/` and `server/` directories.
*   **IDE Configuration:** For the best development experience, configure your IDE to use the Python interpreter located in the `./venv` directory.
*   **Workflow Engine:** The node-based workflow engine in `backend/node_engine/` is the preferred way to implement complex email processing logic. New processing steps should be created as custom nodes.
