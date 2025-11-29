# Email Intelligence

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

## Getting Started

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

## Development Workflow

The `main` branch serves as the primary integration branch for stable releases. Currently, feature, bug, feat, and fix branches are merged into `main` as they are completed and tested.

In the future, the `scientific` and `sqlite` branches will be integrated into `main` to consolidate advanced AI features and database optimizations.

This approach maintains a stable `main` branch while allowing parallel development on specialized branches.

## Continuous Integration

The project uses GitHub Actions for continuous integration on the `main` and `scientific` branches. The CI pipeline includes:

*   **Automated Testing**: Runs the full test suite using pytest with coverage reporting.
*   **Code Quality Checks**: Performs linting with Flake8, code formatting checks with Black and isort, and type checking with mypy.
*   **Dependabot Auto-Merge**: Automatically merges Dependabot pull requests after successful CI checks.

CI runs on every push and pull request to the specified branches, ensuring code quality and preventing regressions.

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

## Development Notes

-   **Python Environment:** The launcher automatically creates and manages a virtual environment in the `./venv` directory. You do not need to activate it manually.
-   **Dependencies:** All Python dependencies are defined in `pyproject.toml` and installed with `uv`. All Node.js dependencies are defined in the `package.json` file of the respective `client/` or `server/` directory.
-   **IDE Configuration:** For the best IDE support (e.g., in VS Code), point your Python interpreter to the one inside the `./venv` directory.
-   **Data Storage:** This version uses local file-based storage, primarily located in `backend/python_backend/data/`. SQLite databases (`.db` files) are created in the project root.