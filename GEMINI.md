<<<<<<< HEAD
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
=======
# Gemini Agent Instructions for EmailIntelligence

This document provides the necessary context and instructions for the Gemini AI agent to effectively assist with development tasks on the EmailIntelligence project.

## 1. Project Overview & Goal

EmailIntelligence is a full-stack application designed for intelligent email analysis and management. It integrates with Gmail to provide features like sentiment analysis, topic classification, intent recognition, and urgency detection.

The primary goal is to leverage AI to help users manage their email more efficiently.

## 2. Architecture & Technology

The project follows a modern web architecture with distinct frontend and backend components:

-   **Frontend (`client/`)**: A React application built with TypeScript, Vite, and styled with Tailwind CSS and Radix UI.
-   **Backend**:
    -   **Python/FastAPI (`backend/python_backend/`)**: Serves the primary AI/NLP functionalities.
    -   **Node.js/Express (`server/`)**: Handles other backend services.
-   **AI/ML (`backend/python_nlp/`)**: Core NLP models and logic using PyTorch, Transformers, and NLTK.
-   **Database**: SQLite for local data storage and email caching.
-   **Shared Types (`shared/`)**: TypeScript schemas are located here for consistency between frontend and backend.

## 3. Building, Running, and Testing

The `launch.py` script is the unified entry point for managing the development environment.

### Primary Commands

-   **Initial Setup**:
    ```bash
    python launch.py --setup
    ```
    This command creates the Python virtual environment (`.venv/`), installs all Python and Node.js dependencies, and downloads necessary NLTK data.

-   **Run Development Servers**:
    ```bash
    python launch.py
    ```
    This starts the Python FastAPI backend and the React frontend development server.
    -   Python Backend: `http://localhost:8000`
    -   React Frontend: `http://localhost:5173` (or as specified by Vite)

-   **Run Gradio UI (for AI model interaction)**:
    ```bash
    python launch.py --gradio-ui
    ```

### Language-Specific Commands

#### Python (Backend)

-   **Run Tests**:
    ```bash
    pytest
    ```
-   **Format Code**:
    ```bash
    black .
    ```
-   **Lint Code**:
    ```bash
    flake8 . && pylint python_backend
    ```
-   **Type Check**:
    ```bash
    mypy .
    ```

#### TypeScript/React (Frontend)

-   **Run Linter**:
    ```bash
    cd client && npm run lint
    ```
-   **Run Dev Server Only**:
    ```bash
    cd client && npm run dev
    ```
-   **Build for Production**:
    ```bash
    npm run build
    ```

## 4. Development Conventions

Adherence to the following conventions is critical.

### Python
-   **Formatting**: Use `black` with a line length of 100 characters.
-   **Imports**: Use `isort` with the "black" profile.
-   **Typing**: All function parameters and return values **must** have type hints.
-   **Docstrings**: Use Google-style for all public modules, functions, and classes.
-   **Naming**: Use `snake_case` for functions and variables, and `CapWords` for classes.

### TypeScript/React
-   **Imports**: Use the alias `@/` for imports from `client/src` and `@shared/` for shared schemas.
-   **Component Naming**: Use `PascalCase` for component files and function names.
-   **Styling**: Use Tailwind CSS utility classes for styling.

### Critical Rules to Follow
1.  **No Circular Dependencies**: Be especially careful with imports between core modules.
2.  **No Hard-coded Paths/Secrets**: Use environment variables or configuration files.
3.  **Strict Typing**: Ensure all new code is fully type-annotated.
4.  **Consistent Naming**: Follow the established naming conventions strictly.
>>>>>>> main
