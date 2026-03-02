# EmailIntelligence - Project Structure

## Directory Organization

### Core Application Structure
```
src/                          # Main application source code
├── core/                     # Core interfaces and models
│   ├── commands/            # Command pattern implementations
│   ├── conflict_models.py   # Git conflict data models
│   ├── exceptions.py        # Custom exception classes
│   ├── factory.py          # Factory pattern implementations
│   └── interfaces.py       # Core interface definitions
├── git/                     # Git operations and conflict detection
├── resolution/              # Conflict resolution algorithms
├── strategy/                # Strategy pattern implementations
├── utils/                   # Utility modules (caching, logging, monitoring)
├── validation/              # Validation and quality checking
└── context_control/         # Agent context and access control
```

### Orchestration & Tooling
```
scripts/                      # Orchestration and automation scripts
├── hooks/                   # Git hooks (pre-commit, post-checkout, etc.)
├── lib/                     # Shared shell libraries
├── agents/                  # Agent monitoring and integration
├── bash/                    # Bash-specific automation
├── powershell/              # PowerShell automation scripts
└── currently_disabled/      # Deprecated/disabled functionality

setup/                       # Environment setup and launcher
├── commands/                # CLI command implementations
├── launch.py               # Main launcher script
├── pyproject.toml          # Project configuration
├── requirements*.txt       # Dependency specifications
└── setup_environment_*.sh  # Platform-specific setup
```

### Configuration & Agent Integration
```
.claude/                     # Claude Code integration
├── agents/                  # Agent definitions
├── commands/                # Custom slash commands
├── memories/                # Agent memory and context
└── settings.json           # Claude configuration

.context-control/            # Branch-specific agent access control
├── profiles/                # Context profiles per branch
│   ├── main.json           # Main branch agent access
│   ├── orchestration-tools.json  # Orchestration branch access
│   └── scientific.json     # Scientific branch access

.specify/                    # Agent specifications and templates
├── memory/                  # Agent memory management
├── scripts/                 # Agent automation scripts
└── templates/               # Specification templates
```

### Multi-Agent Support
```
.agents/                     # Generic agent commands
.codebuddy/                  # CodeBuddy agent integration
.cursor/                     # Cursor IDE integration
.gemini/                     # Google Gemini integration
.github/                     # GitHub agent workflows
.kilo/                       # Kilo agent rules
.qwen/                       # Qwen agent integration
.windsurf/                   # Windsurf agent integration
```

## Core Components & Relationships

### 1. Orchestration Layer
- **Git Hooks**: Automated branch synchronization and conflict prevention
- **Script Library**: Shared utilities for cross-platform operations
- **Context Control**: Branch-specific agent access management
- **Stash Management**: Advanced Git stash resolution tools

### 2. Application Layer
- **CLI Framework**: Command-line interface with conflict detection
- **Web API**: FastAPI-based REST API for email processing
- **UI Components**: Gradio-based interactive interface
- **Data Models**: Pydantic models for type safety and validation

### 3. Integration Layer
- **Agent Framework**: Multi-agent development tool support
- **Database Abstraction**: Support for SQLite, PostgreSQL, Redis
- **External APIs**: Google Workspace, email providers
- **ML Pipeline**: Transformers, NLTK, scikit-learn integration

### 4. Infrastructure Layer
- **Environment Management**: Cross-platform setup and validation
- **Dependency Management**: Conditional package installation
- **Performance Monitoring**: Resource usage and bottleneck detection
- **Logging & Debugging**: Comprehensive logging across all components

## Architectural Patterns

### Command Pattern
- **Location**: `src/core/commands/`, `setup/commands/`
- **Purpose**: Encapsulates operations as objects for undo/redo and queuing
- **Implementation**: CLI commands, Git operations, validation steps

### Factory Pattern
- **Location**: `src/core/factory.py`, `setup/commands/command_factory.py`
- **Purpose**: Creates objects without specifying exact classes
- **Implementation**: Command creation, strategy selection, agent instantiation

### Strategy Pattern
- **Location**: `src/strategy/`
- **Purpose**: Defines family of algorithms and makes them interchangeable
- **Implementation**: Conflict resolution strategies, merge algorithms, validation approaches

### Observer Pattern
- **Location**: `scripts/agents/`, monitoring utilities
- **Purpose**: Notifies multiple objects about state changes
- **Implementation**: Agent health monitoring, performance tracking, Git hook notifications

### Repository Pattern
- **Location**: `src/git/repository.py`, database abstractions
- **Purpose**: Encapsulates data access logic
- **Implementation**: Git operations, database queries, configuration management

## Branch-Specific Architecture

### orchestration-tools Branch
- **Focus**: Tooling, scripts, Git hooks, agent configurations
- **Key Components**: `scripts/`, `setup/`, agent integration files
- **Isolation**: No application code, pure orchestration

### main Branch
- **Focus**: Stable application code and production configurations
- **Key Components**: `src/`, `tests/`, production documentation
- **Integration**: Receives orchestration updates via Git hooks

### scientific Branch
- **Focus**: ML/AI experimentation and research code
- **Key Components**: Jupyter notebooks, experimental algorithms, research documentation
- **Specialization**: Enhanced ML dependencies and research tools

## Data Flow Architecture

### 1. Input Processing
Email Data → FastAPI Endpoints → Pydantic Validation → Processing Queue

### 2. ML Pipeline
Raw Text → Preprocessing → Feature Extraction → Model Inference → Results

### 3. Orchestration Flow
Git Operations → Hook Triggers → Script Execution → Branch Synchronization → Agent Notifications

### 4. Agent Integration
User Commands → Agent Context → Tool Selection → Execution → Result Feedback