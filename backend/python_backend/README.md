<<<<<<< HEAD
# DEPRECATED: Python Backend README

**This directory is part of the deprecated `backend` package and will be removed in a future release.**

This directory contains the legacy monolithic Python backend for the EmailIntelligence application. It is a FastAPI application that handled all backend logic, including API endpoints, AI/NLP services, and database interactions.

## Migration Status

The functionality in this directory has been migrated to the new modular architecture:
- Core components are now in `src/core/`
- Feature modules are in `modules/`
- API routes are now defined in `modules/*/routes.py`
- Services are now defined in `modules/*/services.py`

## New Architecture

The new modular architecture provides:
- Better separation of concerns
- Improved testability
- Enhanced extensibility
- Clearer code organization

For more information about the new architecture, see:
- [Project Structure Comparison](docs/project_structure_comparison.md)
- [Backend Migration Guide](docs/backend_migration_guide.md)
- [Architecture Overview](docs/architecture_overview.md)

## Gradio Interface

A Gradio interface is available for interacting with some of the backend functionalities.
Currently, it supports:
- **AI Email Analysis**: Input an email's subject and content to get an AI-powered analysis.

### Running the Gradio App

1.  **Ensure dependencies are installed:**
    ```bash
    pip install -r requirements.txt
    # (Make sure you are in the root directory of the project or adjust path to requirements.txt)
    ```
    Alternatively, if you have `uv` installed:
    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Navigate to the Python backend directory:**
    ```bash
    cd backend/python_backend
    ```

3.  **Run the Gradio app:**
    ```bash
    python gradio_app.py
    ```

4.  The interface will typically be available at `http://127.0.0.1:7860` (or the next available port). Check the console output for the exact URL.
=======
>>>>>>> 837f0b4c3be0be620537c058dd8dba25d8ac010d
