# EmailIntelligence - Unified Development Environment (iFlow Context)

## Project Overview

EmailIntelligence is a full-stack application designed to provide intelligent email analysis and management capabilities. The project combines a Python FastAPI backend for AI/NLP tasks with a React frontend, offering features such as sentiment analysis, topic classification, intent recognition, urgency detection, and smart filtering.

The application uses a modular architecture with a unified launcher system (`launch.py`), comprehensive environment management, and an extensions framework for customization. It supports both a standard web interface and a Gradio-based UI for scientific exploration and direct AI model interaction.

## Key Technologies

- **Backend**: Python 3.12+, FastAPI, NLTK, scikit-learn, PyTorch, Transformers
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
├── launch.py               # Unified launcher script
├── pyproject.toml          # Python project configuration
├── package.json            # Node.js project configuration
├── README.md               # Project documentation
└── ...                     # Other configuration and documentation files
```

## Building and Running

### Prerequisites

- Python 3.12 or later
- Node.js 18 or later
- Git

### Quick Start

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd EmailIntelligence
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Run the application using the launcher:
   ```bash
   # Windows
   launch.bat --stage dev

   # Linux/macOS
   ./launch.sh --stage dev
   ```

This will:
- Set up the Python virtual environment
- Install Python dependencies
- Download necessary NLTK data
- Create placeholder AI model files
- Start the Python FastAPI server (default: port 8000)
- Start the React frontend development server (default: port 5173)

### Launcher Usage

The `launch.py` script is the central tool for managing the development environment:

- Setup: `python launch.py --setup`
- Run all services: `python launch.py`
- Run specific services:
  - Backend only: `python launch.py --no-client --no-ui`
  - Frontend only: `python launch.py --no-backend --no-ui`
  - Gradio UI only: `python launch.py --no-backend --no-client`

### AI Models Setup

The application's AI features require trained models. On first run, placeholder files are created. To enable actual AI functionality:

1. Prepare labeled datasets for training
2. Modify `backend/python_nlp/ai_training.py` to load your data
3. Train models and save them with the exact filenames expected by the application:
   - `backend/python_nlp/sentiment_model.pkl`
   - `backend/python_nlp/topic_model.pkl`
   - `backend/python_nlp/intent_model.pkl`
   - `backend/python_nlp/urgency_model.pkl`

### Environment Configuration

Key environment variables:
- `DATABASE_URL`: Database connection string
- `GMAIL_CREDENTIALS_JSON`: Gmail API credentials
- `NLP_MODEL_DIR`: Directory for trained NLP models
- `PORT`: Port for the Python FastAPI server (default: 8000)

## Development Conventions

### Code Organization

- Backend code is organized in `backend/python_backend/` with modular components
- NLP models and analysis components are in `backend/python_nlp/`
- Frontend code follows standard React patterns in `client/`
- Tests are located in `tests/`

### Python Development

- Uses `uv` for Python dependency management based on `pyproject.toml`
- Code formatting with `black` and `isort`
- Type checking with `mypy`
- Testing with `pytest`

### Frontend Development

- Uses Vite for building and development
- TypeScript for type safety
- React for UI components

### Testing

- Backend tests use `pytest`
- Frontend tests use Vitest

### Security Considerations

- Securely manage API keys and credentials
- Validate and sanitize user inputs
- Restrict CORS policy in production
- Ensure sensitive information is not excessively logged

## Gradio UI Structure

The Gradio interface provides an interactive web UI with the following tabs:
- Dashboard: Overview and metrics
- Inbox: Email listing and filtering
- Gmail: Gmail synchronization
- AI Lab: Advanced analysis tools and model management
- System Status: Health and performance metrics

## Advanced Features

### Node-Based Workflow Engine

The application includes a sophisticated node-based workflow system for creating complex email processing pipelines with:
- Visual workflow creation
- Security framework
- Extensibility through plugins
- Performance monitoring

### Extension System

EmailIntelligence supports an extension system for adding custom functionality:
- Extensions can be managed using `launch.py`
- Detailed documentation in `docs/extensions_guide.md`