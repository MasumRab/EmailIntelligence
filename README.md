# Email Intelligence - Unified Development Environment

Welcome to the Email Intelligence project! This repository contains a complete ecosystem for building, testing, and running a sophisticated email analysis application. It includes a Python backend for core logic and AI, a Gradio interface for scientific development, a TypeScript backend for handling certain API routes, and a React-based web client.

This README provides a unified guide to setting up and running all components using the central `launch.py` script.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Architecture](#project-architecture)
- [Directory Structure](#directory-structure)
- [Launcher Usage](#launcher-usage)
- [Development Notes](#development-notes)

## Prerequisites

- **Python:** Version 3.11-3.13
- **Node.js:** Version 18.x or higher (with `npm`)
- **Git:** For cloning the repository

## Getting Started

A single script, `launch.py`, manages the entire development environment, from installing dependencies to running services.

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
    -   Manages data storage (JSON files and SQLite databases).

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

## Directory Structure

```
.
├── src/                  # Core modular Python backend (FastAPI + Gradio)
│   ├── core/             # Core components (AI engine, database, workflows, etc.)
│   └── main.py           # Application entry point
├── modules/              # Modular extensions
│   ├── categories/       # Category management module
│   ├── default_ai_engine/# Default AI engine module
│   └── workflows/        # Workflow management module
├── backend/
│   ├── node_engine/      # Node-based workflow engine and specialized email nodes
│   └── python_nlp/       # NLP-specific modules and utilities (legacy)
├── client/               # React/Vite frontend application
├── server/               # TypeScript/Node.js backend application
├── shared/               # Code/types shared between services
│
├── launch.py             # 🚀 Unified script to set up, manage, and run the project
├── pyproject.toml        # Python dependency definitions (for uv)
├── package.json          # Node.js workspace configuration
│
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

The `launch.py` script is the single entry point for all development tasks.

### Environment Management

-   **Force a clean setup:** Delete and recreate the environment from scratch.
    ```bash
    python3 launch.py --setup --force-recreate-venv
    ```
-   **Update all dependencies:**
    ```bash
    python3 launch.py --setup --update-deps
    ```

### Running Specific Services

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

-   **Python Environment:** The launcher automatically creates and manages a virtual environment in the `./.venv` directory. You do not need to activate it manually.
-   **Dependencies:** All Python dependencies are defined in `pyproject.toml` and installed with `uv`. All Node.js dependencies are defined in the `package.json` file of the respective `client/` or `server/` directory.
-   **IDE Configuration:** For the best IDE support (e.g., in VS Code), point your Python interpreter to the one inside the `./.venv` directory.
-   **Data Storage:** This version uses local file-based storage, primarily located in `data/`. SQLite databases (`.db` files) are created in the project root.
-   **Modular Architecture:** The application uses a modular design where core functionality is in `src/core/`, and features are added via modules in `modules/`. This allows for easy extension and maintenance.
-   **Node-based Workflows:** The node engine in `backend/node_engine/` provides a modular, extensible architecture for creating complex email processing workflows. Nodes can be chained together to create sophisticated processing pipelines with security and scalability features.


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
    - If missing, run: `pip install uvicorn[standard]` in the .venv

### Common Errors

- **"ModuleNotFoundError"**: Run setup again or check .venv activation
- **Permission Errors**: Avoid running as administrator; use regular user account
- **Port Conflicts**: Services will use next available ports if defaults are taken
