# iFlow CLI Documentation

## Overview

iFlow CLI is an interactive command-line interface agent designed to assist with software engineering tasks in the EmailIntelligence project. It specializes in helping developers with code understanding, refactoring, testing, and implementation while strictly following project conventions.

## Core Mandates

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

## Task Management

iFlow CLI uses a todo system to manage and plan tasks:

```python
# Example of using todo system
todo_write([{
    "id": "1", 
    "task": "Implement new feature X", 
    "status": "pending"
}])
```

## Software Engineering Workflow

When performing software engineering tasks, iFlow CLI follows this sequence:

1. **Understand**: Analyze the user's request and relevant codebase context
2. **Plan**: Build a coherent plan based on understanding
3. **Implement**: Use available tools to act on the plan
4. **Verify (Tests)**: Run project's testing procedures
5. **Verify (Standards)**: Execute project-specific build, linting and type-checking commands

## Tools Available

iFlow CLI has access to various tools for software engineering tasks:

- `read_file`: Read file contents
- `write_file`: Write content to a file
- `replace`: Replace text within a file
- `search_file_content`: Search for patterns in files
- `glob`: Find files matching patterns
- `run_shell_command`: Execute shell commands
- `todo_write`/`todo_read`: Task management

## Project Structure

The EmailIntelligence project follows a microservices architecture:

```
.
├── backend/                    # Backend services
│   ├── python_backend/         # Main FastAPI application and Gradio UI
│   ├── python_nlp/             # NLP-specific modules
│   └── ...
├── client/                     # React frontend application
├── server/                     # TypeScript Node.js backend
├── shared/                     # Shared code between services
└── ...
```

## Key Technologies

- **Backend**: FastAPI, Python 3.12
- **Frontend**: React, TypeScript, Vite
- **AI/NLP**: Transformers, PyTorch, NLTK
- **Database**: JSON files, SQLite
- **Workflow Engine**: Node-based processing
- **Build Tools**: Vite

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