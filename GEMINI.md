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
    This command creates the Python virtual environment (`venv/`), installs all Python and Node.js dependencies, and downloads necessary NLTK data.

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
