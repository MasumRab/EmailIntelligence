<<<<<<< HEAD
<<<<<<< HEAD:docs/deployment_guide.md
=======
=======
<<<<<<<< HEAD:docs/deployment_guide.md
========
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
# EmailIntelligence Deployment Guide

This guide covers deployment and development setup for the EmailIntelligence project. The application uses a unified launcher script for development and deployment.

## Development and Deployment

The EmailIntelligence platform uses a unified launcher script (`launch.py`) for all development and deployment needs. This approach simplifies setup and ensures consistency across environments.

### Development Environment

**Purpose:** Local development with hot-reloading and debugging capabilities.

**Features:**
*   FastAPI backend with auto-reload
*   React frontend with hot module replacement
*   Integrated Gradio UI
*   SQLite database for local development
*   Modular architecture with plugin system

**Setup:**
```bash
# Install dependencies
python launch.py --setup

# Start development servers
python launch.py
```

**Services Started:**
- **Backend API:** http://127.0.0.1:8000
- **Gradio UI:** http://127.0.0.1:7860
- **React Frontend:** http://127.0.0.1:5173

### Production Deployment

**Current Approach:** The platform is designed for deployment on cloud platforms. Production deployment typically involves:

1. **Cloud Deployment:** Deploy to services like Railway, Render, or Vercel
2. **Database:** Use managed database services (PostgreSQL on cloud providers)
3. **Static Assets:** Serve React build files through CDN or web server

**Environment Variables:**
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Application
SECRET_KEY=your-secret-key
DEBUG=False
PORT=8000

# External Services
OPENAI_API_KEY=your-key
GMAIL_CREDENTIALS_PATH=/path/to/credentials
```

## Architecture Overview

The EmailIntelligence platform follows a modular architecture:

### Core Components
- **Backend:** FastAPI-based REST API with modular extensions
- **Frontend:** React application with TypeScript
- **UI:** Gradio interface for interactive AI workflows
- **Database:** SQLite for development, PostgreSQL for production
- **AI Engine:** Modular NLP processing with plugin system

### Module System
The application uses a plugin-based architecture where features are implemented as modules:
- `modules/categories/` - Category management
- `modules/default_ai_engine/` - AI processing
- `modules/workflows/` - Workflow orchestration

### Launcher Script
The `launch.py` script provides unified management:
- Environment setup and dependency installation
- Service orchestration (backend, frontend, UI)
- Development server management
- Production-ready configuration

## Launcher Commands

The `launch.py` script provides the following commands:

### Setup Commands
```bash
# Initial setup with dependency installation
python launch.py --setup

# Update all dependencies
python launch.py --update-deps

# Setup with uv
python launch.py --setup
```

### Development Commands
```bash
# Start all services (backend, frontend, Gradio UI)
python launch.py

# Start only backend and UI
python launch.py --no-client

# Start only frontend
python launch.py --no-backend --no-ui

# Start with custom ports
python launch.py --port 8001 --gradio-port 7861
```

### Environment Options
```bash
# Force recreate virtual environment
python launch.py --setup --force-recreate-venv

# Skip virtual environment setup
python launch.py --no-venv

# Use custom environment file
python launch.py --env-file .env.production
```

### Testing
```bash
# Run tests (pytest)
pytest

# Run specific test file
pytest tests/modules/categories/test_categories.py

# Run with coverage
pytest --cov=src --cov-report=html
```

## Testing

A comprehensive suite of tests is available to ensure the quality and stability of the EmailIntelligence application. Tests are executed using pytest. For detailed information on the testing strategy, different types of tests, and specific test cases, refer to the test files in the `tests/` directory.

## Directory Structure

- `deployment/`: Contains deployment-related scripts and utilities.
  - `test_stages.py`: Script for testing deployment stages.
- `launch.py`: Unified launcher script for development and deployment.
- `backend/python_backend/metrics.py`: Provides Prometheus metrics for application monitoring.

## Prerequisites

- Python 3.12 or higher
- PostgreSQL (for local development)
- Node.js and npm (for frontend development)

## Environment Variables

The following environment variables are used by the application:

- `DATABASE_URL`: PostgreSQL connection string
- `NODE_ENV`: Environment name (development, staging, production)
- `PORT`: Port for the backend server

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/EmailIntelligence.git
    cd EmailIntelligence
    ```

2.  **Set up the development environment:**
    ```bash
    python launch.py --setup
    python launch.py
    ```

3.  **Access the application:**
    - Backend: http://localhost:8000
    - Frontend: http://localhost:5173
    - Gradio UI: http://localhost:7860



## Troubleshooting

If you encounter issues, check the application logs in the terminal where you ran `python launch.py`.

For database issues, ensure your DATABASE_URL is correctly set and the PostgreSQL service is running.
<<<<<<< HEAD
>>>>>>> 61a41ae340efd5cf9fff01717c04000fdf7e4da5:docs/old_workflow_docs/deployment_guide.md
=======
>>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613:docs/old_workflow_docs/deployment_guide.md
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
