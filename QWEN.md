# Email Intelligence Platform - Development Context

## Project Overview

The Email Intelligence Platform is a state-of-the-art, modular AI processing platform for email analysis, inspired by leading AI frameworks like automatic1111's stable-diffusion-webui, Stability-AI/StableSwarmUI, and comfyanonymous/ComfyUI. The platform features a node-based processing system, extensible plugin architecture, and comprehensive UI for both developers and end-users.

This is a multi-service application built with Python (FastAPI) for the backend, Gradio for the developer interface, Node.js/TypeScript for secondary services, and React/Vite for the frontend. The platform implements a modular architecture with plugin support and node-based processing workflows.

## Project Structure

```
.
├── backend/                     # Python backend services
│   ├── python_backend/          # Main FastAPI application and Gradio UI
│   ├── python_nlp/              # NLP-specific modules and utilities
│   └── plugins/                 # Extensible plugin system for custom processing nodes
├── client/                      # React/Vite frontend application
├── server/                      # TypeScript/Node.js backend application
├── shared/                      # Code/types shared between services
├── workflows/                   # Node-based processing pipeline definitions
├── models/                      # AI model management and caching system
├── data/                        # Data storage (JSON files, SQLite databases)
├── launch.py                    # 🚀 Unified script to set up, manage, and run the project
├── docker-compose.yml          # Container orchestration for production deployment
├── pyproject.toml              # Python dependency definitions (for uv)
├── package.json                # Node.js workspace configuration
└── ...
```

## Technologies & Dependencies

### Python Backend
- **Framework**: FastAPI for the main API
- **UI**: Gradio for the scientific development interface
- **NLP/AI**: NLTK, TextBlob, Transformers, PyTorch, Scikit-learn
- **Data Processing**: Pandas, NumPy, Matplotlib, Plotly
- **Authentication**: Google API Python Client, Google Auth libraries
- **Database**: SQLite and PostgreSQL support

### Frontend
- **Framework**: React with Vite
- **TypeScript**: For the Node.js backend
- **UI Components**: Standard web technologies

## Running the Application

### Prerequisites
- **Python**: Version 3.12.x
- **Node.js**: Version 18.x or higher (with `npm`)
- **Git**: For cloning the repository
- **Docker**: (Optional) For containerized deployment

### Setup & Execution
1. **First-time setup**:
   ```bash
   python3 launch.py --setup
   ```

2. **Run all services**:
   ```bash
   python3 launch.py
   ```

This starts:
- Python FastAPI Backend on `http://127.0.0.1:8000`
- Gradio UI on `http://127.0.0.1:7860` (node-based workflow editor)
- Node.js TypeScript Backend
- React Frontend on `http://127.0.0.1:5173`

### Launcher Options
- `--setup --force-recreate-venv`: Clean setup
- `--setup --update-deps`: Update dependencies
- `--no-client --no-server-ts`: Run only Python backend and Gradio UI
- `--no-backend --no-ui --no-server-ts`: Run only React client
- `--help`: All available options

## Project Architecture

### 1. Python Backend (FastAPI)
- Located in `backend/python_backend/`
- Serves the primary REST API with plugin architecture for extending functionality
- Implements node-based processing workflows for email analysis
- Manages data storage (JSON files and SQLite databases)

### 2. Gradio UI
- Located in `backend/python_backend/gradio_app.py`
- Features drag-and-drop node-based workflow editor inspired by ComfyUI
- Provides real-time processing visualization and monitoring
- Intended for developers, data scientists, and advanced users

### 3. TypeScript Backend (Node.js)
- Located in `server/`
- Handles specific API routes and service integrations
- Demonstrates a polyglot microservice architecture

### 4. React Frontend (Vite)
- Located in `client/`
- Main user-facing web application with intuitive email processing workflows
- Includes audit trails and performance metrics for AI processing operations

## Plugin System

The platform supports a modular plugin architecture:
- Plugins can be added to the `backend/plugins/` directory
- New processing nodes follow standardized interfaces
- Processing pipelines built using a node-based system similar to ComfyUI

Base plugin interfaces are defined in `backend/plugins/base_plugin.py`:
- `BasePlugin`: Abstract base class for all plugins
- `ProcessingNode`: Base class for processing nodes in the workflow system

## Development Conventions

### Python
- Uses Python 3.12+
- Formatting with Black (line length 100)
- Import sorting with isort (Black profile)
- Type checking with MyPy
- Linting with Flake8 and Pylint

### Code Organization
- Clear separation of concerns between services
- Dependency injection for loose coupling
- Standardized interfaces for extensibility
- Proper error handling with custom exceptions

### Git Workflow
- Dependencies managed via `pyproject.toml` and `package.json`
- Virtual environment managed automatically by `launch.py`
- Environment variables for configuration (e.g., `GMAIL_CREDENTIALS_JSON`)

## Key Features

1. **Modular Architecture**: Plugin system allows extending functionality without modifying core code
2. **Node-based Workflows**: Visual workflow editor for building complex email processing pipelines
3. **AI/NLP Processing**: Advanced email analysis with sentiment, topic modeling, and categorization
4. **Multi-Service Architecture**: FastAPI, Gradio, React, and TypeScript services working together
5. **Gmail Integration**: Full integration with Gmail API for email processing
6. **Model Management**: Caching mechanism for AI models with fallback capabilities

## Operational Limits & Configuration

### Gmail API Integration Limits
- **Rate Limiting**: 
  - Daily queries: 1,000,000,000 (effectively unlimited for most use cases)
  - Queries per 100 seconds: 250
  - Queries per second: 5 (practical limit to avoid bursts)
  - Maximum concurrent requests: 10
  - Initial backoff: 1.0 second
  - Maximum backoff: 60.0 seconds
  - Backoff multiplier: 2.0

### Data Processing Limits
- **Email Retrieval**:
  - Messages per request: 100 (maximum batch size from Gmail API)
  - Default pagination limit: 50 emails per page across search and retrieval functions
  - Strategy limits: Daily sync (1000), Weekly bulk (5000), Historical import (10000)

### Model Management
- **Registered Models**:
  - Sentiment model: 15.2 MB
  - Topic model: 22.1 MB  
  - Intent model: 18.7 MB
  - Urgency model: 12.5 MB
- **Model Manager**: Handles dynamic loading/unloading with thread-safe operations

### Data Storage
- **Database Connections**: SQLite-based with file locking for concurrent access
- **Caching**: SQLite-based email cache with content hashing
- **Synchronization**: Incremental sync with pagination tokens

## Current Operational Configuration

The Email Intelligence Platform currently has well-defined operational limits especially for Gmail API integration. The configuration is primarily handled through:
- Environment variables for credentials and paths
- Rate limiting configuration in `gmail_integration.py`
- Default pagination limits in database operations
- Model management with size tracking and loading states

### Recommended Updates to Operational Limits

1. **Add Environment Variable Controls**: Operational limits should be configurable via environment variables for easier deployment in different environments
2. **Memory Usage Limits**: Add configuration for maximum memory usage by the model manager to prevent out-of-memory issues
3. **Processing Timeouts**: Add configurable timeout values for long-running operations
4. **Batch Processing Limits**: Add configurable limits for bulk email processing operations
5. **Model Loading Limits**: Add maximum models that can be loaded simultaneously based on system memory

## Configuration

- Environment variables in `.env` files (not committed)
- Gmail credentials via `GMAIL_CREDENTIALS_JSON` environment variable
- Configuration files in the `config/` directory
- Model download and caching system

## Testing

- Python tests in `backend/python_backend/tests/` and `backend/python_nlp/tests/`
- Use pytest for test execution
- Code coverage with pytest-cov

## Deployment

- Docker Compose configuration available in `docker-compose.yml`
- Production-ready configuration with PostgreSQL database
- Environment variable-based configuration for security