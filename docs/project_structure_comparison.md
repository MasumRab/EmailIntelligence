# Project Structure Comparison

## OLD PROJECT STRUCTURE (Before Node-Based Workflow Implementation)
.
├── backend/
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
│   │   ├── workflow_engine.py  # OLD workflow engine (basic)
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
│   ├── client_development.md
│   ├── deployment_guide.md
│   ├── env_management.md
│   ├── extensions_guide.md
│   ├── launcher_guide.md
│   ├── node_architecture.md    # New documentation added
│   ├── python_style_guide.md
│   ├── server_development.md
│   └── ...
├── models/                     # ML models
├── modules/                    # Reusable modules
├── plugins/                    # Plugin implementations
├── src/                        # Source code
│   └── core/                   # Core platform components
│       ├── security.py         # Security framework (basic version)
│       └── ...
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
├── QWEN.md                     # Project documentation
├── README.md                   # Project documentation
└── ...

## NEW PROJECT STRUCTURE (After Node-Based Workflow Implementation)
.
├── backend/
│   ├── data/                   # Data storage files
│   ├── extensions/             # Backend extensions
│   ├── node_engine/            # NEW: Node-based workflow engine and specialized email nodes
│   │   ├── __init__.py
│   │   ├── email_nodes.py      # NEW: Node types (EmailSourceNode, PreprocessingNode, etc.)
│   │   ├── node_base.py        # NEW: Base classes for nodes and workflows
│   │   ├── security_manager.py # NEW: Security components for node system
│   │   ├── test_integration.py # NEW: Integration tests
│   │   ├── test_nodes.py       # NEW: Node tests
│   │   ├── test_sanitization.py # NEW: Sanitization tests
│   │   ├── test_security.py    # NEW: Security tests
│   │   ├── workflow_engine.py  # NEW: Advanced workflow engine
│   │   └── workflow_manager.py # NEW: Workflow persistence
│   ├── plugins/                # Plugin implementations
│   ├── python_backend/         # Main FastAPI application and Gradio UI
│   │   ├── notebooks/          # Jupyter notebooks for analysis
│   │   ├── tests/              # Backend tests
│   │   ├── ai_engine.py        # AI analysis engine
│   │   ├── advanced_workflow_routes.py # NEW: API endpoints for advanced workflows
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
│   │   ├── workflow_editor_ui.py # NEW: Gradio UI for node-based workflow editor
│   │   ├── workflow_engine.py  # OLD: Basic workflow engine (now coexists with new one)
│   │   ├── workflow_manager.py # OLD: Basic workflow manager (now coexists with new one)
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
│   ├── advanced_workflow_system.md # NEW: Comprehensive workflow system documentation
│   ├── client_development.md
│   ├── deployment_guide.md
│   ├── env_management.md
│   ├── extensions_guide.md
│   ├── launcher_guide.md
│   ├── node_architecture.md    # NEW: Architecture documentation for node system
│   ├── project_documentation_guide.md # NEW: Documentation maintenance guide
│   ├── python_style_guide.md
│   ├── server_development.md
│   └── workflow_system_analysis.md # NEW: This analysis report
├── models/                     # ML models
├── modules/                    # Reusable modules
├── plugins/                    # Plugin implementations
├── src/                        # Source code
│   └── core/                   # Core platform components
│       ├── advanced_workflow_engine.py # NEW: Advanced node-based workflow engine
│       ├── security.py         # Security framework (enhanced with workflow security)
│       └── workflow_engine.py  # OLD: Basic workflow engine
├── tests/                      # Test files
│   └── modules/
│       └── workflows/
│           └── test_workflows.py # Workflow-specific tests
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
├── QWEN.md                     # Project documentation
├── README.md                   # Project documentation
└── ...