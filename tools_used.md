# Tools Used in Email Intelligence Platform

This document provides an overview of the tools and technologies used in the Email Intelligence Platform. It should be updated whenever new dependencies are added or removed from the project to maintain an accurate record of the technology stack.

## Purpose and Guidelines
This file serves as a reference for:
- New developers joining the project to understand the technology stack
- DevOps and deployment processes
- Technology decisions and planning
- Dependency management and security audits

To maintain this document, add or remove tools as they are incorporated or removed from the project. Group related tools under the appropriate categories.

## Development Tools
- **Python 3.12**: Core programming language
- **FastAPI**: Web framework for building the API backend
- **Gradio**: Framework for building the machine learning demos and UI
- **Pydantic**: Data validation and settings management
- **NLTK**: Natural Language Toolkit for text processing
- **Transformers**: Hugging Face library for pre-trained models
- **PyTorch**: Machine learning framework
- **Scikit-learn**: Machine learning library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing library
- **Matplotlib/Seaborn/Plotly**: Data visualization libraries
- **Python-dotenv**: Python package to load environment variables from .env files
- **Pyngrok**: Python wrapper for ngrok to expose local servers to the internet
- **Email-validator**: Python email validation library
- **Httpx**: Modern, fast HTTP client for Python

## Infrastructure & Deployment
- **uv**: Python package installer and resolver (faster alternative to pip)
- **Poetry**: Dependency management and packaging tool
- **Uvicorn**: ASGI server for running the FastAPI application
- **Node.js/npm**: JavaScript runtime and package manager for frontend
- **React**: Frontend library for building the user interface
- **Vite**: Frontend build tool for fast development
- **TypeScript**: Typed superset of JavaScript
- **SQLite**: Lightweight database for local development
- **Psycopg2-binary**: PostgreSQL database adapter for Python
- **RestrictedPython**: Restricted execution environment for Python code

## Testing & Quality
- **Pytest**: Testing framework for Python
- **Black**: Code formatter for Python
- **Flake8**: Linting tool for Python
- **isort**: Import sorting tool
- **Pylint**: Static code analysis tool
- **MyPy**: Static type checker

## Security & Performance
- **Bleach**: HTML sanitization library for security
- **psutil**: System and process utilities for monitoring
- **Joblib**: Tools for pipelining Python jobs

## Development Environment
- **Git**: Version control system
- **Virtual Environment (venv)**: Isolated Python environments
- **Pathlib**: Object-oriented filesystem paths
- **Logging**: Standard Python logging module
- **Jupyter**: Interactive development environment
- **Ipykernel**: IPython kernel for Jupyter
- **Ipywidgets**: Interactive HTML widgets for Jupyter

## AI/NLP Specific Tools
- **TextBlob**: Simplified text processing
- **SentencePiece**: Unsupervised text tokenizer
- **Accelerate**: Hugging Face library for easier multi-GPU training
- **Google APIs**: For Gmail integration
- **Scipy**: Scientific computing library

## Workflow & Node Engine
- **Custom Node Engine**: For node-based workflow processing
- **Security Manager**: For input sanitization and security checks
- **Workflow Manager**: For managing AI workflows
- **Plugin System**: Extensible architecture for adding features

## Code Quality & Linting Setup
- **setup_linting.py**: Custom script to install and configure code quality tools

## Launcher & Management
- **launch.py**: Unified launcher for all application components
- **run.py**: Development server runner