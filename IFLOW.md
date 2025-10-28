# EmailIntelligence - Unified Development Environment (iFlow Context)

## Project Overview

EmailIntelligence is a full-stack application designed to provide intelligent email analysis and management capabilities. The project combines a Python FastAPI backend for AI/NLP tasks with a React frontend and a Gradio-based UI for scientific exploration, offering features such as sentiment analysis, topic classification, intent recognition, urgency detection, and smart filtering.

The application uses a modular architecture with a unified launcher system (`launch.py`), comprehensive environment management, and an extensions framework for customization. It supports multiple interfaces including a standard web interface, a Gradio-based UI for scientific exploration, and a node-based workflow system for creating complex email processing pipelines.

## iFlow CLI Overview

iFlow CLI is an interactive command-line interface agent designed to assist with software engineering tasks in the EmailIntelligence project. It specializes in helping developers with code understanding, refactoring, testing, and implementation while strictly following project conventions.

## Key Technologies

- **Backend**: Python 3.12+, FastAPI, NLTK, scikit-learn, PyTorch, Transformers
- **Frontend**: React (Vite), TypeScript
- **NLP/AI**: Custom NLP engine with sentiment, topic, intent, and urgency analysis models using Hugging Face transformers
- **Database**: SQLite (default)
- **Deployment**: Docker support, unified launcher script
- **Workflow Engine**: Node-based workflow system for email processing
- **Extension System**: Plugin architecture for extending functionality

## Project Structure

```
EmailIntelligence/
├── backend/
│   ├── python_backend/     # Legacy FastAPI application
│   │   ├── main.py         # Legacy FastAPI app entry point
│   │   ├── ai_engine.py    # Legacy AI analysis engine
│   │   ├── database.py     # Legacy database management
│   │   └── ...             # Other legacy backend modules
│   ├── python_nlp/         # Core NLP models and analysis components
│   │   ├── nlp_engine.py   # Main NLP engine
│   │   └── ...             # Analysis components (sentiment, topic, etc.)
│   └── node_engine/        # Node-based workflow engine
├── client/                 # React frontend application
├── src/                    # Main application entry point with Gradio UI
│   ├── main.py             # Main application with FastAPI and Gradio integration
│   └── core/               # Core modules and managers
├── modules/                # Modular functionality extensions
├── models/                 # AI model files organized by type
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
- Set up the Python virtual environment or conda environment
- Install Python dependencies using uv
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
- Run with conda environment: `python launch.py --conda-env myenv`

## AI Models Setup

The application's AI features require trained models. On first run, placeholder files are created. To enable actual AI functionality:

1. Prepare labeled datasets for training
2. Modify training scripts to load your data
3. Train models and save them with the exact filenames expected by the application:
   - `models/sentiment/` - Sentiment analysis models
   - `models/topic/` - Topic classification models
   - `models/intent/` - Intent recognition models
   - `models/urgency/` - Urgency detection models

Models are now organized in the `models/` directory with subdirectories for each model type.

## Environment Configuration

Key environment variables:
- `DATABASE_URL`: Database connection string
- `GMAIL_CREDENTIALS_JSON`: Gmail API credentials
- `NLP_MODEL_DIR`: Directory for trained NLP models (default: `models/`)
- `PORT`: Port for the Python FastAPI server (default: `8000`)

## Development Conventions

### Code Organization

- Backend code is organized in `backend/python_backend/` (legacy) and `backend/python_nlp/` (NLP components)
- Core application logic is in `src/` with Gradio UI integration
- Node-based workflow engine in `backend/node_engine/`
- Modular functionality in `modules/`
- Frontend code follows standard React patterns in `client/`
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
- Simple UI (A): User-friendly interface for running pre-built workflows
- Visual Editor (B): Node-based workflow editor
- Admin Dashboard (C): Power-user dashboard for managing models, users, and system performance
- Workflows: Node engine workflow system

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
<<<<<<< HEAD
    "id": "1", 
    "task": "Implement new feature X", 
=======
    "id": "1",
    "task": "Implement new feature X",
>>>>>>> origin/feature-dashboard-stats-endpoint
    "status": "pending"
}])
```

<<<<<<< HEAD
## Session Documentation and Tracking

For documented development sessions, iFlow CLI follows the workflow outlined in `docs/iflow_development_workflow.md`. Session logs are stored in the `backlog/sessions/` directory with the naming convention `IFLOW-YYYYMMDD-XXX.md`.

- Main session log: `SESSION_LOG.md`
- Individual session logs: `backlog/sessions/IFLOW-YYYYMMDD-XXX.md`
- Development workflow guide: `docs/iflow_development_workflow.md`

=======
>>>>>>> origin/feature-dashboard-stats-endpoint
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
<<<<<<< HEAD

## Automated Code Review

The EmailIntelligence project includes a Multi-Agent Code Review System that automatically analyzes code for:

- Security vulnerabilities
- Performance bottlenecks
- Code quality issues
- Architectural inconsistencies

The system is integrated into the development workflow and can be run manually or automatically during pre-commit hooks. See `docs/multi_agent_code_review.md` for detailed information.
=======
>>>>>>> origin/feature-dashboard-stats-endpoint

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

### Enhanced Filtering System

The application features an advanced email filtering system with:
- Multi-criteria filtering (keyword, sender, recipient, category, date/time, size)
- Complex Boolean logic (AND, OR, NOT operations)
- UI component for creating and managing filters
- Integration with the workflow system

### Module System

The platform uses a modular architecture:
- Core functionality in `src/core/`
- Features added via modules in `modules/`
- Easy extension and maintenance
- Modules can register API routes and UI components

### Migration to Modern Architecture

The project is currently undergoing a migration from a monolithic structure to a modular architecture:
- Legacy components are in `backend/python_backend/`
- New modular components are in `src/` and `modules/`
- Node engine for workflow processing in `backend/node_engine/`

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