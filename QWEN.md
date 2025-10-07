# Email Intelligence Platform - Development Context

## Project Overview

The Email Intelligence Platform is a comprehensive email analysis application that leverages AI and NLP to automatically analyze, categorize, and manage emails. The project follows a microservices architecture with multiple interconnected services:

1. **Python Backend (FastAPI)**: Primary REST API for core application logic, data processing, and AI/NLP tasks
2. **Gradio UI**: Interactive interface for scientific development, model testing, and data visualization
3. **Node-Based Workflow Engine**: Sophisticated workflow system with dependency management and visual editor
4. **TypeScript Backend (Node.js)**: Secondary backend for specific API routes
5. **React Frontend (Vite)**: Main user-facing web application

The project is designed with a modular architecture that supports plugins, workflow management, and performance monitoring. It uses local file-based storage (JSON/GZipped files) and SQLite for data persistence.

## Key Features

- **AI-Powered Email Analysis**: Automatic analysis of emails for topic, sentiment, intent, and urgency
- **Smart Categorization**: AI-driven suggestions and application of categories to emails
- **Intelligent Filtering**: System for creating and managing smart filters to automate workflows
- **Model Management**: Dynamic loading and management of AI models
- **Node-Based Workflows**: Visual workflow system with drag-and-drop interface (inspired by ComfyUI)
- **Workflow Engine**: Configurable workflows for email processing
- **Performance Monitoring**: Real-time performance tracking and metrics
- **Plugin System**: Extensible architecture with plugin support
- **Enterprise Security**: Multi-layer security with authentication, authorization, and audit logging

## Project Structure

```
.
├── backend/                    # Backend services
│   ├── data/                   # Data storage files
│   ├── extensions/             # Backend extensions
│   ├── plugins/                # Plugin implementations
│   ├── python_backend/         # Main FastAPI application and Gradio UI
│   │   ├── notebooks/          # Jupyter notebooks for analysis
│   │   ├── tests/              # Backend tests
│   │   ├── ai_engine.py        # AI analysis engine
│   │   ├── category_routes.py  # Category management routes
│   │   ├── database.py         # Database management
│   │   ├── email_routes.py     # Email processing routes
│   │   ├── enhanced_routes.py  # Enhanced feature routes
│   │   ├── gradio_app.py       # Gradio UI application
│   │   ├── main.py             # FastAPI main application
│   │   ├── model_manager.py    # AI model management
│   │   ├── models.py           # Pydantic models
│   │   ├── performance_monitor.py # Performance monitoring
│   │   ├── plugin_manager.py   # Plugin management
│   │   ├── workflow_engine.py  # Workflow processing engine
│   │   ├── workflow_manager.py # Workflow persistence
│   │   ├── workflow_editor_ui.py # Node-based workflow editor UI
│   │   ├── advanced_workflow_routes.py # Advanced workflow API routes
│   │   └── ...                 # Other backend modules
│   └── python_nlp/             # NLP-specific modules
│       ├── analysis_components/ # NLP analysis components
│       ├── tests/              # NLP tests
│       ├── nlp_engine.py       # Core NLP engine
│       ├── smart_filters.py    # Smart filtering system
│       └── ...                 # Other NLP modules
├── client/                     # React frontend application
├── server/                     # TypeScript Node.js backend
├── shared/                     # Shared code between services
├── config/                     # Configuration files
├── data/                       # Application data
├── deployment/                 # Deployment configurations
├── docs/                       # Documentation
├── models/                     # ML models
├── modules/                    # Reusable modules
├── plugins/                    # Plugin implementations
├── src/                        # Source code
│   └── core/                   # Core platform components
│       ├── advanced_workflow_engine.py # Advanced node-based workflow engine
│       ├── security.py         # Security framework
│       └── workflow_engine.py  # Basic workflow engine
├── tests/                      # Test files
├── .github/                    # GitHub configurations
├── .config/                    # Configuration files
├── .continue/                  # Continue configurations
├── .openhands/                 # OpenHands configurations
├── .qwen/                      # Qwen Code configurations
├── jules-scratch/             # Scratch directory
├── launch.py                   # Unified launcher script
├── pyproject.toml              # Python project configuration
├── package.json                # Node.js project configuration
├── requirements.txt            # Python dependencies
├── requirements-dev.txt        # Development dependencies
├── run.py                      # Development server runner
├── setup_linting.py            # Linting setup script
├── setup_python.sh             # Python setup shell script
├── SETUP.md                    # Manual setup guide
├── QWEN.md                     # Current file
├── README.md                   # Project documentation
└── ...
```

## Building and Running

### Prerequisites
- Python 3.12.x
- Node.js 18.x or higher (with npm)
- Git for cloning the repository

### Setup and Running

The project uses a unified launcher script (`launch.py`) for all operations:

**First-time setup:**
```bash
python launch.py --setup
```

**Running the application:**
```bash
python launch.py
```

This starts:
- Python FastAPI Backend on `http://127.0.0.1:8000`
- Gradio UI on `http://127.0.0.1:7860` (or next available port)
- Node.js TypeScript Backend (port managed by npm)
- React Frontend on `http://127.0.0.1:5173` (or next available port)

**Additional launcher options:**
- `--no-backend`: Don't start the Python backend
- `--no-ui`: Don't start the Gradio UI
- `--no-client`: Don't start the Node.js frontend
- `--debug`: Enable debug/reload mode
- `--port`: Set port for Python backend
- `--gradio-port`: Set port for Gradio UI

### Manual Setup Alternative

If the automated setup fails, refer to `SETUP.md` for manual setup instructions:

**Python environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -U uv
uv sync --active --all-extras
python -c "import nltk; [nltk.download(d, quiet=True) for d in ['punkt', 'stopwords', 'wordnet', 'vader_lexicon', 'averaged_perceptron_tagger', 'brown']]"
```

**Node.js dependencies:**
```bash
npm install --prefix client
npm install --prefix server
```

**Manual execution:**
```bash
# Python backend
uvicorn backend.python_backend.main:app --host 127.0.0.1 --port 8000 --reload

# Gradio UI
python backend/python_backend/gradio_app.py

# React frontend
npm run dev --prefix client

# TypeScript backend
npm run dev --prefix server
```

### Development Tools

**Code Quality Setup:**
Run `setup_linting.py` to install and configure code quality tools:
```bash
python setup_linting.py
```

This installs and configures:
- Black (for code formatting)
- Flake8 (for linting)
- isort (for import sorting)
- Pylint (for code analysis)
- MyPy (for type checking)

## Key Technologies

- **Backend**: FastAPI, Python 3.12
- **Frontend**: React, TypeScript, Vite
- **Database**: JSON files, SQLite, with potential for PostgreSQL
- **AI/NLP**: Transformers, PyTorch, NLTK, scikit-learn
- **UI**: Gradio for scientific interface, React for user interface
- **Workflow Engine**: Node-based processing inspired by ComfyUI
- **Deployment**: Multi-stage setup through unified launcher

## New Node-Based Workflow System

The platform has been enhanced with a sophisticated node-based workflow system:

### Core Components:
- **src/core/advanced_workflow_engine.py**: Advanced node-based workflow engine with security and performance features
- **src/core/security.py**: Enterprise-grade security framework
- **backend/python_backend/workflow_editor_ui.py**: Visual workflow editor UI
- **backend/python_backend/advanced_workflow_routes.py**: API endpoints for workflow management

### Key Features:
- **Node-Based Processing**: Visual workflow creation with drag-and-drop interface
- **Security Framework**: Multi-layer security with authentication, authorization, and audit logging
- **Extensibility**: Plugin system for adding new node types
- **Performance Monitoring**: Built-in metrics collection and monitoring
- **Enterprise Features**: Data sanitization, execution sandboxing, audit trails

### API Endpoints:
- `POST /api/workflows/advanced/workflows` - Create new workflows
- `GET /api/workflows/advanced/workflows` - List available workflows
- `GET /api/workflows/advanced/workflows/{id}` - Get specific workflow
- `PUT /api/workflows/advanced/workflows/{id}` - Update workflow
- `DELETE /api/workflows/advanced/workflows/{id}` - Delete workflow
- `POST /api/workflows/advanced/workflows/{id}/execute` - Execute workflow
- `GET /api/workflows/advanced/nodes` - List available node types
- `GET /api/workflows/advanced/execution/status` - Get execution status
- `POST /api/workflows/advanced/execution/cancel/{id}` - Cancel execution

## Special Components

- **Model Manager**: Handles dynamic loading/unloading of AI models
- **Workflow Engine**: Manages configurable email processing workflows
- **Performance Monitor**: Tracks system performance metrics
- **Plugin Manager**: Enables extensible functionality
- **Security Manager**: Provides enterprise-grade security
- **Smart Filters**: Provides advanced email filtering capabilities