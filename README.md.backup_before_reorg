# EmailIntelligence CLI - AI-powered Git Worktree-based Conflict Resolution Tool

## Overview
EmailIntelligence is an advanced conflict resolution system that uses constitutional/specification-driven analysis to intelligently resolve git merge conflicts. It provides a structured workflow for managing complex branch alignments while ensuring code quality and architectural compliance.

## Architecture

### Modular Design
The application follows the Single Responsibility Principle with the following modules:

- **Core**: Contains configuration, security validation, and git operations
- **Application**: Contains main application logic
- **API**: Contains FastAPI endpoints
- **CLI**: Contains command-line interface (this file)

### Security Features
- Path traversal prevention
- Input validation for PR numbers and git references
- Safe subprocess execution
- Restricted CORS origins in API

### Configuration Management
- Centralized configuration using ConfigurationManager
- Secure default values
- Validation of configuration parameters

## Installation

### Prerequisites
- Python 3.8+
- Git with worktree support

### Setup
```bash
pip install -e .
```

Or install dependencies directly:
```bash
pip install -r requirements.txt
```

## Usage

### CLI Commands
```bash
# Setup resolution workspace
eai setup-resolution --pr 123 --source-branch feature/auth --target-branch main

# Analyze constitutional compliance
eai analyze-constitutional --pr 123 --constitution ./constitutions/auth.yaml

# Develop resolution strategy
eai develop-spec-kit-strategy --pr 123 --worktrees --interactive

# Execute content alignment
eai align-content --pr 123 --interactive --checkpoint-each-step

# Validate resolution
eai validate-resolution --pr 123 --comprehensive
```

### API Usage
Start the API server:
```bash
uvicorn src.api.main:app --reload
```

Then make requests to the endpoints:
- `GET /` - Health check
- `POST /setup-resolution/` - Setup resolution workspace
- `GET /health` - Health check

## Security

### Input Validation
- PR numbers are validated to be within reasonable bounds
- Git references are validated to prevent command injection
- File paths are validated to prevent directory traversal

### Safe Operations
- Subprocess calls use parameterized commands to prevent injection
- Path operations are validated before execution
- Configuration values are validated before use

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8 .
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License
MIT