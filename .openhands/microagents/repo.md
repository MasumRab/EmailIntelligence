# EmailIntelligence Repository

## Purpose

EmailIntelligence is an AI-powered email management application that provides intelligent email processing, categorization, and analysis. The application combines natural language processing (NLP) capabilities with a modern web interface to help users manage their email communications more effectively.

Key features include:
- **AI-powered email analysis**: Sentiment analysis, topic classification, intent detection, and urgency assessment
- **Smart categorization**: Automatic email categorization with customizable categories
- **Gmail integration**: Direct integration with Gmail API for email synchronization
- **Intelligent filtering**: Smart filter generation and management
- **Performance monitoring**: Real-time performance tracking and analytics
- **Modern web interface**: React-based frontend with responsive design

## General Setup

The repository follows a modern Python development setup using:

- **Package Management**: UV (modern Python package manager) with `pyproject.toml` configuration
- **Python Version**: Requires Python 3.11+ (supports up to 3.12)
- **Virtual Environment**: Automated virtual environment management via launcher
- **Dependencies**: Comprehensive dependency management with version locking (`uv.lock`)
- **Launcher System**: Inspired by Stable Diffusion WebUI with unified `launch.py` script

### Key Setup Files:
- `pyproject.toml`: Main project configuration and dependencies
- `uv.lock`: Locked dependency versions for reproducible builds
- `launch.py`: Unified launcher script for automated setup and deployment
- `requirements.txt` & `requirements_versions.txt`: Legacy requirement files
- `requirements-dev.txt`: Development-specific dependencies

### Environment Management:
- Automatic virtual environment creation and management
- NLTK data download automation
- Cross-platform support (Windows, Linux, macOS)
- Stage-specific configurations (dev, test, staging, prod)

## Repository Structure

```
EmailIntelligence/
├── backend/                    # Backend services and data
│   ├── python_backend/         # FastAPI backend application
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── models.py          # Pydantic data models
│   │   ├── database.py        # Database management (JSON-based)
│   │   ├── ai_engine.py       # AI engine adapter
│   │   ├── *_routes.py        # API route handlers
│   │   └── tests/             # Backend unit tests
│   ├── python_nlp/            # NLP processing engine
│   │   ├── nlp_engine.py      # Core NLP processing
│   │   ├── gmail_integration.py # Gmail API integration
│   │   ├── gmail_service.py   # Gmail AI service
│   │   └── smart_retrieval.py # Smart email retrieval
│   ├── extensions/            # Extension system
│   └── data/                  # JSON data storage
├── client/                    # React frontend application
│   ├── src/                   # React source code
│   ├── index.html            # HTML entry point
│   └── package.json          # Node.js dependencies
├── docs/                      # Documentation
├── shared/                    # Shared TypeScript schemas
├── launch.py                  # Main launcher script
├── pyproject.toml            # Project configuration
├── uv.lock                   # Dependency lock file
└── README.md                 # Project documentation
```

### Core Components:

1. **Backend (`backend/python_backend/`)**:
   - FastAPI-based REST API
   - Pydantic models for data validation
   - JSON-based data storage
   - Comprehensive test suite

2. **NLP Engine (`backend/python_nlp/`)**:
   - Advanced NLP processing using transformers
   - Gmail API integration
   - Smart email retrieval algorithms
   - Performance monitoring

3. **Frontend (`client/`)**:
   - React with TypeScript
   - Vite build system
   - Modern UI components

4. **Launcher System**:
   - Automated environment setup
   - Cross-platform compatibility
   - Stage-specific configurations
   - Process management

### Data Storage:
- **Application Data**: JSON files in `backend/data/`
- **Smart Filters**: SQLite database (`smart_filters.db`)
- **Email Cache**: SQLite database (`email_cache.db`)

### Testing:
- **Unit Tests**: Comprehensive test suite using pytest
- **Test Coverage**: Coverage reporting available
- **Async Testing**: Full async/await support with pytest-asyncio

### Development Tools:
- **Code Quality**: Black, isort, flake8, pylint, mypy
- **Dependency Management**: UV with automatic updates
- **Performance Monitoring**: Built-in performance tracking
- **Extension System**: Modular extension architecture

## CI/CD Information

**Note**: No GitHub Actions workflows are currently configured in this repository. The project relies on local development tools and manual testing processes.

### Available Development Commands:
- `python launch.py --stage dev`: Run in development mode
- `python launch.py --stage test`: Run test suite
- `python launch.py --api-only`: Run backend only
- `python launch.py --frontend-only`: Run frontend only
- `python launch.py --system-info`: Display system information

### Code Quality Tools:
- **Linting**: flake8, pylint
- **Formatting**: black, isort
- **Type Checking**: mypy
- **Testing**: pytest with async support
- **Coverage**: pytest-cov integration

The repository is designed for local development and deployment, with a focus on scientific and research applications.