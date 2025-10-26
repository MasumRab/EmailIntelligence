# Email Intelligence - Unified Development Environment

Welcome to the Email Intelligence project! This repository contains a complete ecosystem for building, testing, and running a sophisticated email analysis application. It includes a Python backend for core logic and AI, a Gradio interface for scientific development, a TypeScript backend for handling certain API routes, and a React-based web client.

This README provides a unified guide to setting up and running all components using the central `launch.py` script.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [AI Models Setup](#ai-models-setup)
  - [Database Setup for Development](#database-setup-for-development)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Gmail API Integration Setup](#gmail-api-integration-setup)
- [Running the Application](#running-the-application)
- [AI System Overview](#ai-system-overview)
- [Building for Production](#building-for-production)
- [Database](#database)
- [Extension System](#extension-system)
- [Debugging Hangs](#debugging-hangs)

## Project Overview

- **Python:** Version 3.11-3.13
- **Node.js:** Version 18.x or higher (with `npm`)
- **Git:** For cloning the repository

## Getting Started

A single script, `launch.py`, manages the entire development environment, from installing dependencies to running services. It supports both venv and Conda environments and handles Python version detection automatically.

For convenience, simple wrapper scripts are provided:
- `launch.bat` (Windows)
- `launch.sh` (Linux/macOS)

User customizations can be added to `launch-user.env`.

### 1. First-Time Setup

Clone the repository and run the setup command. This will create a Python virtual environment, install all Python and Node.js dependencies, and download necessary machine learning model data.

```bash
git clone <your-repo-url>
cd <repository-name>
python3 launch.py --setup
```

**Alternative: Using Poetry**

If you prefer Poetry for Python dependency management:

```bash
python3 launch.py --use-poetry --setup
```

**Note:** The setup installs CPU-only PyTorch for lightweight deployment. If you need GPU support, modify the PyTorch installation manually.

### 2. Running the Application

After the one-time setup, use the same script to launch all services:

```bash
python3 launch.py
```

This command will start:
- **Python FastAPI Backend** on `http://127.0.0.1:8000`
- **Gradio UI** on `http://127.0.0.1:7860` (or the next available port)
- **Node.js TypeScript Backend** (port managed by `npm`)
- **React Frontend** on `http://127.0.0.1:5173` (or the next available port)

Press `Ctrl+C` in the terminal to gracefully shut down all running services.

## Project Architecture

The application follows a modular architecture composed of interconnected services:

1.  **Modular Python Backend (FastAPI + Gradio):**
    -   Core located in `src/`, with modular components in `modules/`.
    -   Serves the primary REST API for core application logic, data processing, and AI/NLP tasks.
    -   Integrated Gradio UI for scientific development, model testing, and data visualization.
    -   Modular design allows easy extension with new features via modules.
    -   Manages data storage (JSON files and SQLite databases), now with a configurable data directory.
    -   Enhanced email search and update functionalities.
    -   API routes for workflows, models, and performance are explicitly included, while `training_routes` has been removed.

2.  **Node-Based Workflow Engine:**
    -   Located in `src/core/advanced_workflow_engine.py` and `backend/node_engine/`.
    -   Implements a sophisticated, extensible workflow system inspired by ComfyUI, automatic1111, and Stability-AI frameworks.
    -   Features node-based processing architecture with dependency management, plugin extensibility, and enterprise-grade security.

3.  **TypeScript Backend (Node.js):**
    -   Located in `server/`.
    -   A secondary backend that handles specific API routes, demonstrating a polyglot microservice architecture.

4.  **React Frontend (Vite):**
    -   Located in `client/`.
    -   The main user-facing web application for end-users to interact with the Email Intelligence service.

## Gradio UI Structure

The Gradio interface provides an interactive web UI for the Email Intelligence Platform:

```
Email Intelligence Platform (Gradio UI)
├── 📊 Dashboard
│   ├── Overview & Metrics
│   ├── System Status
│   └── Recent Activity Feed
├── 📧 Email Analysis
│   ├── Single Email Processor
│   ├── Batch Email Analysis
│   ├── Results Visualization
│   └── Export Options
├── 🏷️ Categories
│   ├── Category Management
│   ├── Category Statistics
│   ├── Bulk Category Operations
│   └── Category-Based Filtering
├── ⚙️ Workflows
│   ├── Node-Based Workflow Builder
│   ├── Workflow Template Library
│   ├── Workflow Execution Monitor
│   └── Workflow Performance Analytics
├── 🤖 AI Engine
│   ├── Model Selection & Configuration
│   ├── Training Data Management
│   ├── Model Performance Metrics
│   └── Custom Model Upload
└── 🔧 Settings
    ├── System Configuration
    ├── Data Management Tools
    ├── API Key Management
    └── User Preferences
```

### Gradio UI Enhancements

#### Email Retrieval and Filtering Tab

**Objective:** Implement a new Gradio tab for interactive email retrieval and filtering, leveraging the existing backend filtering capabilities.

**Requirements:**

*   **Email Listing:** Display a paginated list of emails, showing key information (subject, sender, date, categories).
*   **Search Functionality:**
    *   Text search across email subjects, senders, and content.
    *   Filter by category (dropdown/multi-select).
    *   Filter by read/unread status.
*   **Email Details View:** Allow users to click on an email to view its full content and analysis results.
*   **Action Buttons:**
    *   Mark as read/unread.
    *   Assign/change category.
    *   Trigger re-analysis by the active workflow.
*   **Integration:** Utilize the existing FastAPI backend endpoints for email retrieval, search, and updates.
*   **User Experience:** Provide a clear, intuitive interface for exploring and managing emails.

## Directory Structure

```
.
├── src/                        # Core platform components
│   └── core/                   # Core components (AI engine, database, workflows, etc.)
│       ├── advanced_workflow_engine.py # Advanced node-based workflow engine
│       ├── security.py         # Security framework
│       └── workflow_engine.py  # Basic workflow engine
├── modules/                    # Reusable modules
│   ├── categories/             # Category management module
│   ├── default_ai_engine/      # Default AI engine module
│   └── workflows/              # Workflow management module
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
├── plugins/                    # Plugin implementations
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
├── run.py                      # DEPRECATED: Use launch.py instead
├── setup_linting.py            # Linting setup script
├── setup_python.sh             # Python setup shell script
├── SETUP.md                    # Manual setup guide
├── QWEN.md                     # Development context
└── ...
```

## Project Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Email Intelligence Platform                       │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   React Client  │    │  TypeScript     │    │   Modular Python │         │
│  │   (Vite)        │◄──►│  Backend        │◄──►│   Backend        │         │
│  │                 │    │  (Node.js)      │    │   (FastAPI)      │         │
│  │ • User Interface│    │ • API Routes    │    │ • Core API       │         │
│  │ • Dashboard     │    │ • Middleware    │    │ • AI Engine      │         │
│  │ • Email Upload  │    │ • Auth          │    │ • Database       │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│         │                   │                       │                       │
│         └───────────────────┼───────────────────────┘                       │
│                             │                                               │
│                    ┌────────▼────────┐                                       │
│                    │   Gradio UI     │                                       │
│                    │   Interface     │                                       │
│                    │                 │                                       │
│                    │ • Interactive   │                                       │
│                    │ • Data Viz      │                                       │
│                    │ • Model Testing │                                       │
│                    └─────────────────┘                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                          Module System                                 │ │
│  │                                                                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │ Categories  │  │ AI Engine   │  │ Workflows   │  │  Custom     │   │ │
│  │  │ Module      │  │ Module      │  │ Module     │  │  Modules    │   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                        Data Flow                                        │ │
│  │                                                                       │ │
│  │  Email Input → Preprocessing → AI Analysis → Categorization → Output  │ │
│  │                                                                       │ │
│  │  ↳ JSON Storage    ↳ SQLite Cache    ↳ Workflow Engine    ↳ API       │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

```
Email Processing Pipeline
─────────────────────────

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Input      │ -> │Preprocessing│ -> │ AI Analysis │ -> │Categorization│
│  • Raw      │    │ • Clean     │    │ • Sentiment │    │ • Tags      │
│    Emails   │    │ • Tokenize  │    │ • Intent    │    │ • Priority  │
│  • Files    │    │ • Normalize │    │ • Urgency   │    │ • Custom    │
│  • API      │    │             │    │ • Topic     │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Storage    │    │   Cache     │    │  Workflow   │    │   Output    │
│  • JSON     │    │ • SQLite    │    │  • Nodes    │    │ • API       │
│    Files    │    │ • Fast      │    │  • Chains   │    │ • UI        │
│  • Database │    │   Access    │    │  • Custom   │    │ • Export    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

Key Components:
• Modular AI Engine: Pluggable analysis models
• Node-Based Workflows: Composable processing pipelines
• Real-time Processing: Streaming and batch capabilities
• Extensible Architecture: Easy addition of new modules
```

## Project Architecture

The application follows a modular architecture composed of interconnected services:

1.  **Modular Python Backend (FastAPI + Gradio):**
    -   Core located in `src/`, with modular components in `modules/`.
    -   Serves the primary REST API for core application logic, data processing, and AI/NLP tasks.
    -   Integrated Gradio UI for scientific development, model testing, and data visualization.
    -   Modular design allows easy extension with new features via modules.
    -   Manages data storage (JSON files and SQLite databases), now with a configurable data directory.
    -   Enhanced email search and update functionalities.
    -   API routes for workflows, models, and performance are explicitly included, while `training_routes` has been removed.

2.  **Node-Based Workflow Engine:**
    -   Located in `src/core/advanced_workflow_engine.py` and `backend/node_engine/`.
    -   Implements a sophisticated, extensible workflow system inspired by ComfyUI, automatic1111, and Stability-AI frameworks.
    -   Features node-based processing architecture with dependency management, plugin extensibility, and enterprise-grade security.

3.  **TypeScript Backend (Node.js):**
    -   Located in `server/`.
    -   A secondary backend that handles specific API routes, demonstrating a polyglot microservice architecture.

4.  **React Frontend (Vite):**
    -   Located in `client/`.
    -   The main user-facing web application for end-users to interact with the Email Intelligence service.

## Gradio UI Structure

The Gradio interface provides an interactive web UI for the Email Intelligence Platform:

```
Email Intelligence Platform (Gradio UI)
├── 📊 Dashboard
│   ├── Overview & Metrics
│   ├── System Status
│   └── Recent Activity Feed
├── 📧 Email Analysis
│   ├── Single Email Processor
│   ├── Batch Email Analysis
│   ├── Results Visualization
│   └── Export Options
├── 🏷️ Categories
│   ├── Category Management
│   ├── Category Statistics
│   ├── Bulk Category Operations
│   └── Category-Based Filtering
├── ⚙️ Workflows
│   ├── Node-Based Workflow Builder
│   ├── Workflow Template Library
│   ├── Workflow Execution Monitor
│   └── Workflow Performance Analytics
├── 🤖 AI Engine
│   ├── Model Selection & Configuration
│   ├── Training Data Management
│   ├── Model Performance Metrics
│   └── Custom Model Upload
└── 🔧 Settings
    ├── System Configuration
    ├── Data Management Tools
    ├── API Key Management
    └── User Preferences
```

### Gradio UI Enhancements

#### Email Retrieval and Filtering Tab

**Objective:** Implement a new Gradio tab for interactive email retrieval and filtering, leveraging the existing backend filtering capabilities.

**Requirements:**

*   **Email Listing:** Display a paginated list of emails, showing key information (subject, sender, date, categories).
*   **Search Functionality:**
    *   Text search across email subjects, senders, and content.
    *   Filter by category (dropdown/multi-select).
    *   Filter by read/unread status.
*   **Email Details View:** Allow users to click on an email to view its full content and analysis results.
*   **Action Buttons:**
    *   Mark as read/unread.
    *   Assign/change category.
    *   Trigger re-analysis by the active workflow.
*   **Integration:** Utilize the existing FastAPI backend endpoints for email retrieval, search, and updates.
*   **User Experience:** Provide a clear, intuitive interface for exploring and managing emails.

## Directory Structure

```
.
├── src/                        # Core platform components
│   └── core/                   # Core components (AI engine, database, workflows, etc.)
│       ├── advanced_workflow_engine.py # Advanced node-based workflow engine
│       ├── security.py         # Security framework
│       └── workflow_engine.py  # Basic workflow engine
├── modules/                    # Reusable modules
│   ├── categories/             # Category management module
│   ├── default_ai_engine/      # Default AI engine module
│   └── workflows/              # Workflow management module
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
├── plugins/                    # Plugin implementations
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
├── run.py                      # DEPRECATED: Use launch.py instead
├── setup_linting.py            # Linting setup script
├── setup_python.sh             # Python setup shell script
├── SETUP.md                    # Manual setup guide
├── QWEN.md                     # Development context
└── ...
```

## Project Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Email Intelligence Platform                       │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   React Client  │    │  TypeScript     │    │   Modular Python │         │
│  │   (Vite)        │◄──►│  Backend        │◄──►│   Backend        │         │
│  │                 │    │  (Node.js)      │    │   (FastAPI)      │         │
│  │ • User Interface│    │ • API Routes    │    │ • Core API       │         │
│  │ • Dashboard     │    │ • Middleware    │    │ • AI Engine      │         │
│  │ • Email Upload  │    │ • Auth          │    │ • Database       │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│         │                   │                       │                       │
│         └───────────────────┼───────────────────────┘                       │
│                             │                                               │
│                    ┌────────▼────────┐                                       │
│                    │   Gradio UI     │                                       │
│                    │   Interface     │                                       │
│                    │                 │                                       │
│                    │ • Interactive   │                                       │
│                    │ • Data Viz      │                                       │
│                    │ • Model Testing │                                       │
│                    └─────────────────┘                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                          Module System                                 │ │
│  │                                                                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │ Categories  │  │ AI Engine   │  │ Workflows   │  │  Custom     │   │ │
│  │  │ Module      │  │ Module      │  │ Module     │  │  Modules    │   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                        Data Flow                                        │ │
│  │                                                                       │ │
│  │  Email Input → Preprocessing → AI Analysis → Categorization → Output  │ │
│  │                                                                       │ │
│  │  ↳ JSON Storage    ↳ SQLite Cache    ↳ Workflow Engine    ↳ API       │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

```
Email Processing Pipeline
─────────────────────────

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Input      │ -> │Preprocessing│ -> │ AI Analysis │ -> │Categorization│
│  • Raw      │    │ • Clean     │    │ • Sentiment │    │ • Tags      │
│    Emails   │    │ • Tokenize  │    │ • Intent    │    │ • Priority  │
│  • Files    │    │ • Normalize │    │ • Urgency   │    │ • Custom    │
│  • API      │    │             │    │ • Topic     │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Storage    │    │   Cache     │    │  Workflow   │    │   Output    │
│  • JSON     │    │ • SQLite    │    │  • Nodes    │    │ • API       │
│    Files    │    │ • Fast      │    │  • Chains   │    │ • UI        │
│  • Database │    │   Access    │    │  • Custom   │    │ • Export    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

Key Components:
• Modular AI Engine: Pluggable analysis models
• Node-Based Workflows: Composable processing pipelines
• Real-time Processing: Streaming and batch capabilities
• Extensible Architecture: Easy addition of new modules
```

## Launcher Usage

## Prerequisites

To successfully set up and run EmailIntelligence, you will need the following:

You can run any combination of services by using the `--no-<service>` flags.

-   **Run only the Python backend and Gradio UI:**
    ```bash
    python3 launch.py --no-client --no-server-ts
    ```
-   **Run only the React client:**
    ```bash
    python3 launch.py --no-backend --no-ui --no-server-ts
    ```
-   **Run in "API only" mode (just the Python backend):**
    ```bash
    python3 launch.py --no-client --no-server-ts --no-ui
    ```

Use `python3 launch.py --help` to see all available options.

## Development Notes

-   **Python Environment:** The launcher automatically creates and manages a virtual environment in the `./venv` directory. You do not need to activate it manually.
-   **Dependencies:** All Python dependencies are defined in `pyproject.toml` and installed with `uv`. All Node.js dependencies are defined in the `package.json` file of the respective `client/` or `server/` directory.
-   **IDE Configuration:** For the best IDE support (e.g., in VS Code), point your Python interpreter to the one inside the `./venv` directory.
-   **Data Storage:** This version uses local file-based storage, primarily located in `data/`. SQLite databases (`.db` files) are created in the project root. The data directory is now configurable via the `DATA_DIR` environment variable.
-   **Modular Architecture:** The application uses a modular design where core functionality is in `src/core/`, and features are added via modules in `modules/`. This allows for easy extension and maintenance.
-   **Node-based Workflows:** The node engine in `backend/node_engine/` provides a modular, extensible architecture for creating complex email processing workflows. Nodes can be chained together to create sophisticated processing pipelines with security and scalability features.
-   **New Node-Based Workflow System:** The platform has been enhanced with a sophisticated node-based workflow system:

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
-   **Performance Monitoring:** The `@log_performance` decorator has been refactored for improved flexibility and direct logging to a file.
-   **Dependency Management:** Enhanced testing for Node.js dependency installation ensures more robust setup.
-   **Special Components:**
    - **Model Manager**: Handles dynamic loading/unloading of AI models
    - **Workflow Engine**: Manages configurable email processing workflows
    - **Performance Monitor**: Tracks system performance metrics
    - **Plugin Manager**: Enables extensible functionality
    - **Security Manager**: Provides enterprise-grade security
    - **Smart Filters**: Provides advanced email filtering capabilities


## Troubleshooting

### Package Installation Issues

If you encounter issues with Python package installation:

1. **PyTorch Installation Fails:**
   - The setup installs CPU-only PyTorch for lightweight deployment
   - If you need GPU support, manually install PyTorch with CUDA after setup

2. **Missing Packages After Setup:**
   - Run `python launch.py --setup` again to verify and reinstall missing packages
   - Check the logs for specific error messages

3. **Using Poetry Instead of uv:**
   - Run `python launch.py --use-poetry --setup` for Poetry-based installation
   - Ensure Poetry is available in your PATH

4. **Uvicorn Not Found:**
   - Uvicorn should be installed automatically
    - If missing, run: `pip install uvicorn[standard]` in the venv

### Common Errors

- **"ModuleNotFoundError"**: Run setup again or check venv activation
- **Permission Errors**: Avoid running as administrator; use regular user account
- **Port Conflicts**: Services will use next available ports if defaults are taken

## Prerequisites

To successfully set up and run EmailIntelligence, you will need the following:

You can run any combination of services by using the `--no-<service>` flags.

-   **Run only the Python backend and Gradio UI:**
    ```bash
    python3 launch.py --no-client --no-server-ts
    ```
-   **Run only the React client:**
    ```bash
    python3 launch.py --no-backend --no-ui --no-server-ts
    ```
-   **Run in "API only" mode (just the Python backend):**
    ```bash
    python3 launch.py --no-client --no-server-ts --no-ui
    ```

Use `python3 launch.py --help` to see all available options.

## Development Notes

-   **Python Environment:** The launcher automatically creates and manages a virtual environment in the `./venv` directory. You do not need to activate it manually.
-   **Dependencies:** All Python dependencies are defined in `pyproject.toml` and installed with `uv`. All Node.js dependencies are defined in the `package.json` file of the respective `client/` or `server/` directory.
-   **IDE Configuration:** For the best IDE support (e.g., in VS Code), point your Python interpreter to the one inside the `./venv` directory.
-   **Data Storage:** This version uses local file-based storage, primarily located in `data/`. SQLite databases (`.db` files) are created in the project root. The data directory is now configurable via the `DATA_DIR` environment variable.
-   **Modular Architecture:** The application uses a modular design where core functionality is in `src/core/`, and features are added via modules in `modules/`. This allows for easy extension and maintenance.
-   **Node-based Workflows:** The node engine in `backend/node_engine/` provides a modular, extensible architecture for creating complex email processing workflows. Nodes can be chained together to create sophisticated processing pipelines with security and scalability features.
-   **New Node-Based Workflow System:** The platform has been enhanced with a sophisticated node-based workflow system:

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
-   **Performance Monitoring:** The `@log_performance` decorator has been refactored for improved flexibility and direct logging to a file.
-   **Dependency Management:** Enhanced testing for Node.js dependency installation ensures more robust setup.
-   **Special Components:**
    - **Model Manager**: Handles dynamic loading/unloading of AI models
    - **Workflow Engine**: Manages configurable email processing workflows
    - **Performance Monitor**: Tracks system performance metrics
    - **Plugin Manager**: Enables extensible functionality
    - **Security Manager**: Provides enterprise-grade security
    - **Smart Filters**: Provides advanced email filtering capabilities

## Quick Start

The fastest way to get EmailIntelligence running locally for development is by using the unified launcher. This process involves a few key steps:

**Step 1: Clone the Repository**
```bash
git clone <repository_url> # Replace <repository_url> with the actual URL
cd EmailIntelligence
```

**Step 2: Install Node.js Dependencies**
Before running the launcher for the first time, or if frontend/Node.js backend dependencies change, install them:
```bash
npm install
```
This command should be run in the project's root directory (where `package.json` is located).

**Step 3: Database Setup**
The application now uses SQLite. The database file (e.g., `sqlite.db`) will typically be created in the `backend` directory when the application starts or when database operations are first performed. Ensure the `backend` directory is writable.

**Step 4: Run the Application using the Launcher**
```bash
# Using the unified launcher (works on all platforms)
python launch.py --stage dev

# Or use convenience wrappers:
# Windows: launch.bat --stage dev
# Linux/macOS: ./launch.sh --stage dev
```
This command will:
- Set up the Python virtual environment and install Python dependencies.
- Download necessary NLTK data.
- Create placeholder AI model files if actual models are not found (see [AI Models Setup](#ai-models-setup) for crucial next steps).
- Start the Python FastAPI AI server (default: port 8000) and the React frontend development server (default: port 5173).

The application will typically be available at http://localhost:5173.

**Important Next Steps:**
- **AI Models:** The Quick Start will get the application running, but AI features require trained models. Please see the [AI Models Setup](#ai-models-setup) section below for critical information.

This starts the application in a local development mode. For comprehensive setup instructions, alternative methods, and details on deploying to Docker, staging, or production environments, please refer to the [Launcher Guide](docs/launcher_guide.md) and the [Deployment Guide](docs/deployment_guide.md).

## Documentation

This project includes comprehensive documentation in the `docs/` directory:

- **[Client Development Guide](docs/client_development.md)**: Information about the frontend application, structure, and development.
- **[Server Development Guide](docs/server_development.md)**: Details about the backend components, structure, and development.
- **[Deployment Guide](docs/deployment_guide.md)**: Comprehensive guide covering all deployment environments (local, Docker, staging, production), setup, configuration, deployment strategies, and operational procedures.
- **[Environment Management Guide](docs/env_management.md)**: Details about the Python environment management system, `launch.py`, and related features.
- **[Launcher Guide](docs/launcher_guide.md)**: Comprehensive information about the unified launcher system (`launch.py`) and its command-line options.
- **[Extensions Guide](docs/extensions_guide.md)**: Information on how to use and develop extensions.
- **[Python Style Guide](docs/python_style_guide.md)**: Coding standards for Python code in the project.

## Setup

The primary method for setting up EmailIntelligence for development is using the sequence described in the [Quick Start](#quick-start):
1.  Clone the repository.
2.  Install Node.js dependencies (`npm install`).
3.  Set up the PostgreSQL database (e.g., using `npm run db:setup` with Docker or configuring an existing instance).
4.  Run the unified launcher script (`python launch.py`) with the `--stage dev` flag.

The launcher script (`launch.py`) handles:
- Python virtual environment creation.
- Python dependency installation from `requirements.txt`.
- NLTK data download.
- Creation of placeholder AI model files if they don't exist (this requires follow-up, see below).
- Starting the development servers.
For detailed setup instructions for various environments (local, Docker, staging, production), consult the [Deployment Guide](docs/deployment_guide.md).

Refer to the [Launcher Guide](docs/launcher_guide.md) for more advanced launcher options and troubleshooting.

### AI Models Setup

The application's AI features (sentiment analysis, topic classification, etc.) rely on trained machine learning models (`.pkl` files located in `backend/python_nlp/`).

**1. Placeholder Models:**
When you first run `launch.py --stage dev`, it will create empty placeholder files for these models if they are missing (e.g., `intent_model.pkl`, `sentiment_model.pkl`, `topic_model.pkl`, `urgency_model.pkl`). These placeholders **will not** provide any actual AI functionality and will likely cause errors if the AI features are invoked.

**2. Training Actual Models:**
To enable AI features, you **must** replace these placeholders with actual trained models. The script `backend/python_nlp/ai_training.py` provides the framework for training these models.

**Challenges and Guidance:**
-   **Training Data:** The `ai_training.py` script currently **does not include training data or direct guidance on acquiring it.** You will need to prepare your own labeled datasets (e.g., CSV files of emails with corresponding topics, sentiments, etc.) to train effective models. This is a non-trivial task and requires data that is representative of what you want to analyze.
-   **Customization Required:** You will likely need to modify `backend/python_nlp/ai_training.py` or create wrapper scripts to:
    *   Load your specific datasets.
    *   Configure the `ModelConfig` for each model type (topic, sentiment, intent, urgency) you intend to use.
    *   Train each model using the provided training classes.
    *   Save the trained models using the **exact filenames** expected by the application (e.g., `backend/python_nlp/topic_model.pkl`, `backend/python_nlp/sentiment_model.pkl`, etc.). The example `main()` in `ai_training.py` saves to a generic name like `model_<ID>.pkl`, which will need to be adjusted to the specific model names loaded by `backend/python_nlp/nlp_engine.py`.

**Recommendation:**
Developing or sourcing appropriate training data and adapting the `ai_training.py` script is a significant development task. For a quicker setup to explore non-AI features, you can proceed without fully trained models, but be aware that AI-dependent functionalities will not work.

*(Consider creating a dedicated guide in `docs/ai_model_training_guide.md` for more detailed future instructions on data preparation and model training workflows.)*

### Database Setup

The application uses an SQLite database. The database file (e.g., `sqlite.db`) is typically located in the `backend` directory. No special setup is usually required beyond ensuring the application has write permissions to create/manage this file.

## Configuration

This section details important environment variables used by the application. These can typically be set in a `.env` file in the project root or directly in your shell environment.

*   **`DATABASE_URL`**: Connection string for the database. For SQLite, this might be `sqlite:sqlite.db` or similar if used, though the application may default to a hardcoded path.
*   **`GMAIL_CREDENTIALS_JSON`**: JSON content of OAuth 2.0 Client ID credentials for Gmail API.
*   **`credentials.json` (File Alternative)**: Alternative to `GMAIL_CREDENTIALS_JSON`, placed in project root. Ensure this file is in `.gitignore` if used.
*   **`GMAIL_TOKEN_PATH`**: File path for storing Gmail API OAuth 2.0 token (default: `token.json`). Ensure this file is in `.gitignore`.
*   **`NLP_MODEL_DIR`**: Directory for trained NLP models (default: `backend/python_nlp/`).
*   **`PORT`**: Port for the Python FastAPI server (default: `8000`).

Consult the respective guides in `docs/` for component-specific configurations.

## Security Considerations

When deploying or running this application, please consider the following:
*   **API Authentication:** Implement proper API security for sensitive operations. (Note: Current state might have basic or no auth for some dev routes).
*   **Secret Management:** Securely manage `GMAIL_CREDENTIALS_JSON` (or `credentials.json`) and `token.json`. Use environment variables or a secret manager. Do not commit secrets to Git.
*   **Log Verbosity:** Ensure sensitive information is not excessively logged in production.
*   **CORS Policy:** Restrict CORS policy in `backend/python_backend/main.py` for production.
*   **Input Validation:** Validate and sanitize all user-supplied and external data.

## Gmail API Integration Setup

To connect to your Gmail account, configure Gmail API access:

1.  **Google Cloud Console:** Enable Gmail API, create OAuth 2.0 Client ID (Desktop app), and download credentials JSON.
2.  **Provide Credentials:**
    *   Set `GMAIL_CREDENTIALS_JSON` environment variable (recommended).
    *   Or, place downloaded JSON as `credentials.json` in project root. (Ensure it's gitignored).
3.  **One-Time Authorization:** The application will guide you through browser authorization when you first try to access Gmail features, creating `token.json` (or the path specified by `GMAIL_TOKEN_PATH`).
4.  **Scopes Used:** `https://www.googleapis.com/auth/gmail.readonly`.

## Running the Application

Once [Setup](#setup) is complete (including Node.js dependencies, database, and consideration for AI models):

The recommended way to run the application for development is using the unified launcher:
```bash
# Cross-platform (recommended)
python launch.py --stage dev

# Or use convenience wrappers:
# Windows: launch.bat --stage dev
# Linux/macOS: ./launch.sh --stage dev
```
This typically starts:
- Python FastAPI AI Server (default: port 8000)
- React Frontend Development Server (default: port 5173, served by Vite)

For other modes (e.g., API-only, frontend-only) and advanced options, see the [Launcher Guide](docs/launcher_guide.md).
For information on running in Docker, staging, or production environments, see the [Deployment Guide](docs/deployment_guide.md).

### Running the Gradio Scientific UI

For scientific exploration, direct AI model interaction, or testing specific UI components, a Gradio-based interface is available. This is a Python-only, non-Dockerized deployment that runs independently of the main FastAPI backend and React frontend.

To launch the Gradio UI, use the launcher script with service selection flags:

```bash
# Cross-platform
python launch.py --no-backend --no-client

# Or use convenience wrappers:
# Windows: launch.bat --no-backend --no-client
# Linux/macOS: ./launch.sh --no-backend --no-client
```

You can also specify the host, port, and enable debug or sharing mode using the standard launcher arguments:
    ```bash
    python launch.py --no-backend --no-client --host 0.0.0.0 --port 7860 --debug --share
    ```
This will start the Gradio interface, typically accessible at the specified host and port (Gradio's default is 7860 if `--port` is not provided).

## AI System Overview

The AI and NLP capabilities are primarily based on:
*   Locally trained classification models (e.g., Naive Bayes, Logistic Regression using `scikit-learn` or similar, saved as `.pkl` files) located in `backend/python_nlp/`. The training framework for these is in `backend/python_nlp/ai_training.py`.
*   Rule-based systems and heuristics can also be part of the NLP pipeline.
The system does not use external Large Language Models (LLMs) by default for its core classification tasks but includes a `PromptEngineer` class in `ai_training.py` which suggests capabilities for LLM interaction if developed further.

## Building for Production

To build the frontend for production:
```bash
npm run build
```
This command typically uses Vite to build the client, placing outputs in a `dist/` directory.

The Python server needs to be run separately in a production environment, typically using a WSGI/ASGI server like Gunicorn or Uvicorn.

For comprehensive information on building and deploying for production, including Docker builds and different environment strategies, please refer to the [Deployment Guide](docs/deployment_guide.md).

## Deployment with Docker

The project includes Dockerfiles and a `deploy.py` script to simplify building and deploying the application using Docker Compose.

### Prerequisites
- Docker and Docker Compose installed.

### Usage
Use the `deployment/deploy.py` script to manage your Docker deployments. It supports `dev` and `prod` environments.

**Build Images:**
```bash
python deployment/deploy.py <environment> build
# Example: python deployment/deploy.py prod build
```

**Start Services:**
```bash
python deployment/deploy.py <environment> up
# Example: python deployment/deploy.py dev up -d
```

**Stop Services:**
```bash
python deployment/deploy.py <environment> down
```

**View Logs:**
```bash
python deployment/deploy.py <environment> logs
```

For more details, refer to `deployment/README.md`.

## Database

The application now uses an SQLite database (e.g., `sqlite.db` in the `backend` directory).
- If `DATABASE_URL` is used, it should be set for SQLite (e.g., `sqlite:backend/sqlite.db`). Otherwise, the application defaults to a local file path.

## Extension System

EmailIntelligence features an extension system for adding custom functionality.
- Manage extensions using `launch.py` (e.g., `--list-extensions`, `--install-extension`).
- For developing extensions and more details, see the [Extensions Guide](docs/extensions_guide.md) and the [Environment Management Guide](docs/env_management.md#extension-system).

## Debugging Hangs

### Debugging Pytest Hangs
*   Use `pytest -vvv` or `pytest --capture=no`.
*   Isolate tests: `pytest path/to/test_file.py::test_name`.
*   Use `breakpoint()` or `import pdb; pdb.set_trace()`.
*   Check for timeouts logged by `deployment/run_tests.py`.

### Debugging NPM/Build Hangs
*   Examine verbose output (e.g., Vite's `--debug`, esbuild's `--log-level=verbose`).
*   Use `node --inspect-brk your_script.js`.
*   Check resource limits (memory, CPU).
*   Try cleaning cache/modules: `npm cache clean --force`, remove `node_modules` & `package-lock.json`, then `npm install`.

### General Debugging on Linux
*   Monitor resources: `top`, `htop`, `vmstat`.
*   Trace system calls: `strace -p <PID>`.
*   Check kernel messages: `dmesg -T`.
*   Ensure adequate disk space.

For more detailed guides and specific component documentation, please refer to the [Documentation](#documentation) section.

## Known Vulnerabilities

- Four moderate severity vulnerabilities related to `esbuild` persist as of the last audit.
- These vulnerabilities are due to `drizzle-kit` (and its transitive dependencies like `@esbuild-kit/core-utils`) requiring older, vulnerable versions of `esbuild`. Specifically, `drizzle-kit`'s dependency tree pulls in `esbuild@0.18.20` and `esbuild@0.19.12`, both of which are vulnerable (<=0.24.2).
- Attempts to override these nested `esbuild` versions to a non-vulnerable version (e.g., `^0.25.5`, which is used by other parts of this project like Vite) using npm's `overrides` feature in `package.json` were made. However, these overrides were not fully effective, with `npm list` indicating version incompatibilities for the overridden packages. `npm audit` continued to report the vulnerabilities.
- These `esbuild` vulnerabilities cannot be fully remediated without an update to `drizzle-kit` itself that addresses its `esbuild` dependency requirements, particularly for the deprecated `@esbuild-kit/*` packages.
- On a related note, `vite` and `@vitejs/plugin-react` were successfully updated to their latest compatible versions (`vite@6.3.5` and `@vitejs/plugin-react@4.5.2` respectively) during the audit process to address other potential issues and ensure compatibility.
