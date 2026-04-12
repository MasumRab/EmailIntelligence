# EmailIntelligence - Unified Development Environment (iFlow Context)

## Project Overview

EmailIntelligence is a full-stack application designed to provide intelligent email analysis and management capabilities. The project combines a Python FastAPI backend for AI/NLP tasks with a React frontend, offering features such as sentiment analysis, topic classification, intent recognition, urgency detection, and smart filtering.

The application uses a modular architecture with a unified launcher system (`launch.py`), comprehensive environment management, and an extensions framework for customization. It supports both a standard web interface and a Gradio-based UI for scientific exploration and direct AI model interaction.

## iFlow CLI Overview

iFlow CLI is an interactive command-line interface agent designed to assist with software engineering tasks in the EmailIntelligence project. It specializes in helping developers with code understanding, refactoring, testing, and implementation while strictly following project conventions.

## Key Technologies

- **Backend**: Python 3.11+, FastAPI, NLTK, scikit-learn, PyTorch, Transformers
- **Frontend**: React (Vite), TypeScript
- **NLP/AI**: Custom NLP engine with sentiment, topic, intent, and urgency analysis models
- **Database**: SQLite (default)
- **Deployment**: Docker support, unified launcher script
- **Workflow Engine**: Node-based workflow system for email processing
- **Extension System**: Plugin architecture for extending functionality

## Project Structure

```
EmailIntelligence/
├── backend/
│   ├── python_backend/     # Main FastAPI application and Gradio UI
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── gradio_app.py   # Gradio UI application
│   │   ├── ai_engine.py    # AI analysis engine
│   │   ├── database.py     # Database management
│   │   └── ...             # Other backend modules
│   └── python_nlp/         # Core NLP models and analysis components
│       ├── nlp_engine.py   # Main NLP engine
│       └── ...             # Analysis components (sentiment, topic, etc.)
├── client/                 # React frontend application
├── src/                    # Main application entry point with Gradio UI
├── modules/                # Modular functionality extensions
├── launch.py               # Unified launcher script
├── pyproject.toml          # Python project configuration
├── package.json            # Node.js project configuration
├── README.md               # Project documentation
└── ...                     # Other configuration and documentation files
```
```

