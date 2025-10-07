# EmailIntelligence Project Context

## Project Overview

EmailIntelligence is an AI-powered email management application that provides intelligent analysis, categorization, and filtering for Gmail emails. The project combines Python NLP models with a modern React frontend, utilizing a simplified environment setup with local file-based data storage for scientific and development purposes.

### Key Features
- Gmail integration with OAuth
- AI-powered email analysis (sentiment, intent, topic, urgency)
- Smart filtering and categorization
- Performance metrics and analytics
- Dashboard with email insights

## Architecture

- **Frontend**: React (client/) with TypeScript, TailwindCSS, Radix UI components, and Vite build system
- **Backend**: Python with FastAPI for API endpoints and Gradio for UI
- **AI Engine**: Python-based NLP models for sentiment, intent, topic, and urgency analysis
- **Database**: SQLite for local storage and caching, with JSON files for main application data

## Project Structure

```
EmailIntelligence/
├── backend/
│   ├── python_backend/     # Python backend services (FastAPI)
│   ├── python_nlp/         # Python NLP models and analysis
│   └── tests/              # Backend tests
├── client/                 # React frontend application
├── server/                 # Alternative server directory (python_backend and python_nlp)
├── shared/                 # Shared TypeScript schemas
├── extensions/             # Extensible plugin system
├── models/                 # ML models
├── mock_models/            # Mock models for testing
├── docs/                   # Documentation
├── jsons/                  # JSON data files
├── .venv/                  # Python virtual environment
├── venv/                   # Alternative Python virtual environment
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
├── pyproject.toml          # Python project configuration
├── launch.py               # Main launcher script
├── launch.sh               # Linux/Mac launcher script
└── README.md               # Project documentation
```

## Technologies Used

- **Frontend**: React 18, TypeScript, TailwindCSS, Radix UI, Vite
- **Backend**: Python (3.11+), FastAPI, Uvicorn, Gradio
- **AI/ML**: PyTorch, Transformers, Scikit-learn, NLTK, Hugging Face models
- **Database**: SQLite, JSON files for local storage
- **Build Tools**: Vite, esbuild

## Setup and Running

The project includes a comprehensive launcher script that automates the setup process:

1. **Requirements**: Python 3.11.x and Node.js LTS
2. **Automatic Setup**: The `launch.py` script handles:
   - Virtual environment creation
   - Dependency installation
   - NLTK data downloads
   - Frontend dependency installation
   - Starting both backend (FastAPI) and frontend (Vite)

### Launch Options
- `python launch.py` - Standard development mode (both backend and frontend)
- `python launch.py --api-only` - Backend API server only
- `python launch.py --ui-only` - Frontend UI only
- `python launch.py --stage test` - Run tests
- Additional options for debugging, port configuration, and environment setup

## Data Storage

This version uses local file-based storage:
- **Main Application Data**: JSON files in `server/python_backend/data/`
- **Smart Filter Rules**: SQLite database in `smart_filters.db`
- **Email Cache**: SQLite database in `email_cache.db`

## Development Notes

- Python code follows PEP 8 style guidelines
- TypeScript is used for all frontend code
- Tests are required for both Python and TypeScript components
- The project includes both unit and integration testing capabilities
- Environment variables can be managed via .env files

## Key Dependencies

Python dependencies include:
- FastAPI for web framework
- PyTorch and Transformers for AI/ML
- NLTK for natural language processing
- Gradio for UI prototyping
- Scikit-learn for machine learning

Node.js dependencies are minimal, focusing on the build tools needed for the React frontend.

## Working with the Codebase

- Backend Python code is in `backend/python_backend/` and `backend/python_nlp/`
- Frontend React code would be in `client/src/` (not in current directory listing)
- Shared TypeScript schemas are in `shared/` for cross-project use
- Extensions support is available in the `extensions/` directory
- Testing is done with pytest for Python and vitest for TypeScript

## Environment Management

The project uses a Python virtual environment managed by the launch scripts. The virtual environment is created in the project root or in a dedicated `venv` directory. Dependencies are managed through `requirements.txt` and `pyproject.toml`.

## Troubleshooting

Common issues:
- Ensure Python 3.11.x is installed and accessible
- Make sure the virtual environment is properly activated
- NLTK data files need to be downloaded during initial setup
- Port conflicts may occur if services are already running

Use `python launch.py --system-info` to diagnose environment issues.