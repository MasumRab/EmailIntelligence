# Email Intelligence - Scientific Branch

This is a streamlined version of the Email Intelligence application, focusing on core functionalities for local scientific and development use. It features a simplified environment setup and uses local file-based data storage.

## Prerequisites

*   **Python:** Version 3.12.x is required.
*   **Node.js:** A recent LTS version (e.g., 18.x or 20.x) is recommended.
*   **Git:** For cloning the repository.

## Setup and Running

1.  **Clone the Repository and Switch to the `scientific` Branch:**
    ```bash
    # Replace <repo_url> and <repo_name> with actual values
    git clone <repo_url>
    cd <repo_name>
    git checkout scientific
    ```

2.  **Run the Launcher Script:**
    This script automates the setup and launch process.
    *   For Linux/macOS:
        ```bash
        ./launch.sh
        ```
    *   For Windows:
        ```bash
        python launch.py
        ```

    The `launch.py` script will perform the following steps:
    *   Check your Python version.
    *   Create a Python virtual environment in the `./venv` directory if one doesn't already exist.
    *   Install the required Python dependencies from `requirements.txt` into the virtual environment.
    *   Download necessary NLTK data files (for text processing).
    *   Install Node.js dependencies for the client application (located in the `client/` directory) by running `npm install` in that directory.
    *   Start the Python backend server (FastAPI/Uvicorn). By default, it runs on `http://127.0.0.1:8000`.
    *   Start the Vite development server for the frontend. By default, it runs on `http://127.0.0.1:5173`.

3.  **Access the Application:**
    Once both servers have started successfully, open your web browser and navigate to the frontend URL, typically:
    `http://127.0.0.1:5173`

## Data Storage

This version uses local file-based storage:

*   **Main Application Data:** Email data, categories, and user information are stored as JSON files in the `backend/python_backend/data/` directory.
*   **Smart Filter Rules:** Configuration for smart filters is stored in an SQLite database file named `smart_filters.db` located in the project root.
*   **Email Cache:** A local cache for fetched email content is stored in `email_cache.db` in the project root.

These files will be created automatically when the application runs if they don't already exist.

## Stopping the Application

To stop both the backend and frontend servers, press `Ctrl+C` in the terminal window where `launch.sh` or `python launch.py` is running. The launcher script is designed to shut down all started processes gracefully.

## Development Notes

*   The Python backend is located in `backend/python_backend/`.
*   The NLP processing logic is in `backend/python_nlp/`.
*   The frontend client (React/Vite) is in `client/`.
*   Ensure the Python virtual environment (`venv/bin/activate` or `venv\Scripts\activate`) is active if you need to run Python commands manually.
```
