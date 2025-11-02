# Email Intelligence Platform - Python Backend

This directory contains the unified Python backend for the Email Intelligence Platform. It provides a comprehensive FastAPI application with integrated AI/NLP services, database management, and advanced node-based workflow system.

## Architecture Overview

The backend is organized into several key components:

### Core Services
- **FastAPI Application** (`main.py`): Main application entry point with CORS, middleware, and route registration
- **Authentication** (`auth.py`): JWT-based authentication and authorization
- **Database** (`database.py`, `json_database.py`): Data persistence with SQLite and JSON storage
- **AI Engine** (`ai_engine.py`): Advanced AI processing with multiple model support

### API Routes
- **Dashboard** (`dashboard_routes.py`): Analytics and statistics endpoints
- **Email Management** (`email_routes.py`): Email CRUD operations
- **Categories** (`category_routes.py`): Email categorization management
- **AI Processing** (`ai_routes.py`): AI analysis and model management
- **Workflow System** (`advanced_workflow_routes.py`): Node-based workflow management
- **Training** (`training_routes.py`): Model training and evaluation

### Services Layer
- **Email Service** (`services/email_service.py`): Email processing logic
- **Category Service** (`services/category_service.py`): Category management
- **Base Service** (`services/base_service.py`): Common service functionality

### Data Management
- **Email Data Manager** (`email_data_manager.py`): Email data operations
- **Category Data Manager** (`category_data_manager.py`): Category data operations
- **Model Manager** (`model_manager.py`): AI model management

### Workflow System
- **Node Engine** (`../node_engine/`): Core workflow execution engine
- **Security Manager** (`../node_engine/security_manager.py`): Workflow security controls
- **Workflow Routes** (`advanced_workflow_routes.py`): REST API for workflows

## Key Features

- **Node-Based Workflows**: Visual workflow creation with drag-and-drop nodes
- **AI Integration**: Sentiment analysis, topic modeling, intent detection
- **Security**: Execution sandboxing, signed tokens, RBAC, audit logging
- **Performance**: Caching, async processing, resource monitoring
- **Extensibility**: Plugin system for custom nodes and extensions

## New Architecture Benefits

- **Modular Design**: Clean separation between services, routes, and data management
- **Security First**: Comprehensive security controls for all operations
- **Scalable**: Async processing and resource management for high performance
- **Maintainable**: Well-structured code with clear responsibilities
- **Testable**: Comprehensive test suite with unit and integration tests

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