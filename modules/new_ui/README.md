# Email Intelligence Platform - New UI Module

This module provides a modern Gradio-based frontend for the Email Intelligence Platform.

## Features

*   **Email Analysis:** Analyze emails using the backend AI engine (Sentiment, Topic, Intent, Urgency).
*   **Workflow Management:** List and run workflows (via generic storage/adapter).
*   **Smart Filters:** Create and save smart filters.
*   **Dashboard:** View system performance metrics.
*   **System Health:** Monitor CPU/Memory usage.

## Installation

1.  Ensure you have the main project dependencies installed.
2.  Install UI-specific dependencies:
    ```bash
    pip install -r modules/new_ui/requirements.txt
    ```

## Running the App

You can run the app directly using Python.

### Local Development (Default)

Runs on `http://127.0.0.1:7860`.

```bash
python modules/new_ui/app.py
```

### Custom Host/Port (e.g., for Docker)

```bash
GRADIO_SERVER_NAME=0.0.0.0 GRADIO_SERVER_PORT=7860 python modules/new_ui/app.py
```

## Backend Integration

This UI connects to the core backend services via `backend_adapter.py`.

*   **Analysis:** Calls `src.core.ai_engine.ModernAIEngine`.
*   **Metrics:** Calls `src.core.performance_monitor.performance_monitor`.
*   **Workflows:** Attempts to call `src.core.workflow_engine`, with fallback to `modules/new_ui/data/` for storage.
*   **Persistence:** Uses generic local JSON files in `modules/new_ui/data/` for items like Smart Filters, as the core DatabaseManager is specialized for structured Email/Category data.

## Configuration

*   `GRADIO_SERVER_NAME`: Hostname to bind to (default: `127.0.0.1`).
*   `GRADIO_SERVER_PORT`: Port to bind to (default: `7860`).
