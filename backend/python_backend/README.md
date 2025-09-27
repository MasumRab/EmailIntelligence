# Python Backend README

This directory contains the Python backend services for the application.

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
    cd server/python_backend
    ```

3.  **Run the Gradio app:**
    ```bash
    python gradio_app.py
    ```

4.  The interface will typically be available at `http://127.0.0.1:7860` (or the next available port). Check the console output for the exact URL.
