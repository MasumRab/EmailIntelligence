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

## iFlow CLI Core Mandates

### Conventions
- Rigorously adhere to existing project conventions when reading or modifying code
- Analyze surrounding code, tests, and configuration first before making changes
- Mimic code style, framework choices, naming conventions, typing, and architectural patterns

### Libraries/Frameworks
- NEVER assume a library/framework is available without verifying its established usage
- Check imports, configuration files, or neighboring files to confirm usage before employing any library

### Style & Structure
- Follow existing code style and structure strictly
- Use existing libraries and utilities already established in the project
- Follow existing architectural patterns

### Idiomatic Changes
- Understand local context (imports, functions/classes) to ensure changes integrate naturally
- Make changes that are idiomatic to the existing codebase

## iFlow CLI Task Management

iFlow CLI uses a todo system to manage and plan tasks:

```python
# Example of using todo system
todo_write([{
    "id": "1", 
    "task": "Implement new feature X", 
    "status": "pending"
}])
```

## iFlow CLI Software Engineering Workflow

When performing software engineering tasks, iFlow CLI follows this sequence:

1. **Understand**: Analyze the user's request and relevant codebase context
2. **Plan**: Build a coherent plan based on understanding
3. **Implement**: Use available tools to act on the plan
4. **Verify (Tests)**: Run project's testing procedures
5. **Verify (Standards)**: Execute project-specific build, linting and type-checking commands

## iFlow CLI Tools Available

iFlow CLI has access to various tools for software engineering tasks:

- `read_file`: Read file contents
- `write_file`: Write content to a file
- `replace`: Replace text within a file
- `search_file_content`: Search for patterns in files
- `glob`: Find files matching patterns
- `run_shell_command`: Execute shell commands
- `todo_write`/`todo_read`: Task management

## Building and Running

### Prerequisites

- Python 3.11 or later
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
- Core application logic is in `src/` with Gradio UI integration
- Tests are located in `tests/`
- AI models are organized in `models/` directory by type

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

### Module System

The platform uses a modular architecture:
- Core functionality in `src/core/`
- Features added via modules in `modules/`
- Easy extension and maintenance

## Development Commands

### Python Backend
- **Test all**: `pytest`
- **Format**: `black .`
- **Lint**: `flake8 . && pylint python_backend`
- **Type check**: `mypy .`

### TypeScript/React Frontend
- **Build**: `cd client && npm run build`
- **Lint**: `cd client && npm run lint`
- **Dev server**: `cd client && npm run dev`

## Code Style Guidelines

### Python
- **Line length**: 100 chars max
- **Formatting**: Black
- **Imports**: isort (black profile)
- **Naming**: snake_case functions/vars, CapWords classes
- **Types**: Type hints required for all parameters/returns
- **Docstrings**: Google-style for public functions/classes

### TypeScript/React
- **Strict mode**: Enabled
- **JSX**: react-jsx transform
- **Components**: Default export functions, PascalCase naming
- **Styling**: Tailwind CSS utilities

## Critical Rules

- Avoid circular dependencies
- Never hard-code paths or expose secrets
- Use dependency injection over global state
- Check existing dependencies before adding new libraries
- Follow security best practices