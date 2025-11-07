# Project Structure Comparison

## CURRENT PROJECT STRUCTURE (Modular Architecture)
.
├── backend/
│   ├── data/                   # Data storage files
│   ├── extensions/             # Backend extensions
│   ├── node_engine/            # Node-based workflow engine
│   │   ├── email_nodes.py      # Node types for email processing
│   │   ├── node_base.py        # Base classes for nodes
│   │   ├── security_manager.py # Security components
│   │   ├── workflow_engine.py  # Advanced workflow engine
│   │   ├── workflow_manager.py # Workflow persistence
│   └── ...                 # Node engine components
│   ├── plugins/                # Plugin implementations
│   ├── python_backend/         # LEGACY: Old monolithic backend (deprecated)
│   │   ├── ...                 # Legacy components (marked for removal)
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
│   ├── advanced_workflow_system.md # Comprehensive workflow system documentation
│   ├── client_development.md
│   ├── deployment_guide.md
│   ├── env_management.md
│   ├── extensions_guide.md
│   ├── deployment/launcher_guide.md
│   ├── node_architecture.md
│   ├── project_documentation_guide.md
│   ├── python_style_guide.md
│   ├── server_development.md
│   └── workflow_system_analysis.md
├── models/                     # ML models
├── modules/                    # Modular extensions
│   ├── categories/             # Category management module
│   │   ├── __init__.py
│   │   ├── routes.py           # Category API routes
│   │   └── tests/              # Module tests
│   ├── default_ai_engine/      # Default AI engine module
│   │   ├── __init__.py
│   │   ├── engine.py           # AI engine implementation
│   │   └── analysis_components/ # AI analysis components
│   └── workflows/              # Workflow management module
│       ├── __init__.py
│       ├── ui.py               # Workflow UI components
│       └── tests/              # Workflow tests
├── src/                        # Core modular backend
│   ├── core/                   # Core components
│   │   ├── advanced_workflow_engine.py # Advanced workflow engine
│   │   ├── ai_engine.py        # AI analysis engine
│   │   ├── database.py         # Database management
│   │   ├── exceptions.py       # Custom exceptions
│   │   ├── models.py           # Pydantic models
│   │   ├── module_manager.py   # Module registration system
│   │   ├── performance_monitor.py # Performance monitoring
│   └── main.py                 # Application entry point
├── tests/                      # Test files
│   ├── core/                   # Core component tests
│   ├── modules/                # Modular component tests
│   └── conftest.py             # Test configuration
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
├── setup_linting.py            # Linting setup script
├── setup_python.sh             # Python setup shell script
├── SETUP.md                    # Manual setup guide
├── QWEN.md                     # Project documentation
├── README.md                   # Project documentation
└── ...

## Migration Status

The project is currently undergoing a migration from a monolithic architecture to a modular architecture:

- **Legacy components** are in `backend/python_backend/` (deprecated and will be removed)
- **New modular components** are in `src/` and `modules/`
- **Node engine** for workflow processing in `backend/node_engine/`
- **NLP components** remain in `backend/python_nlp/` but will be integrated into the new modular structure

This migration aims to improve:
- Modularity and maintainability
- Testability and extensibility
- Separation of concerns
- Code reuse and organization