# Orchestration Tools - Verification and Consistency System

A comprehensive verification and consistency system for multi-branch Git workflows with formal verification capabilities.

## Overview

The Orchestration Tools system provides:

- **Extended Test Scenario Coverage**: Comprehensive test scenarios for validating changes before merging
- **Key Context Verification**: Validation of environment variables, dependencies, configurations, and infrastructure state
- **Branch Integration Validation**: Multi-branch compatibility checking before merging
- **Consistency Verification**: Ensuring goals align with tasks and preventing scope drift
- **Context Contamination Prevention**: Identifying and preventing token wastage through context isolation
- **Token Optimization**: Minimizing token usage during instruction processing
- **Formal Verification Integration**: Validating verification logic with 99% coverage of critical paths

## Features

### Core Capabilities

- ✅ Modular verification architecture with role-based access control
- ✅ Structured logging with correlation IDs for traceability
- ✅ Multi-branch validation strategies
- ✅ Goal-task consistency tracking
- ✅ Context contamination analysis
- ✅ Token usage optimization and monitoring
- ✅ Formal verification tool integration

### User Stories

1. **US1**: Comprehensive Test Scenario Coverage
2. **US2**: Key Context Verification Checks
3. **US3**: Branch Integration Validation
4. **US4**: Goal-Task Consistency Verification
5. **US5**: Context Contamination Prevention
6. **US6**: Token Optimization
7. **US7**: Formal Verification Tools Integration

## Installation

### Prerequisites

- Python 3.11+
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/MasumRab/EmailIntelligence.git
cd EmailIntelligence/orchestration-tools

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

## Quick Start

```bash
# Run verification checks
python -m orchestration_tools verify

# Check context verification
python -m orchestration_tools context-verify

# Validate goal-task consistency
python -m orchestration_tools consistency-check

# Run formal verification
python -m orchestration_tools formal-verify
```

## Project Structure

```
orchestration-tools/
├── src/
│   ├── models/              # Data models (verification, context, etc.)
│   ├── services/            # Core services (verification, git, consistency, etc.)
│   ├── lib/                 # Utility libraries (test scenarios, helpers)
│   ├── cli/                 # CLI commands
│   └── __init__.py
├── tests/
│   ├── contract/            # Contract tests
│   ├── integration/         # Integration tests
│   ├── unit/               # Unit tests
│   └── conftest.py
├── config/
│   ├── verification_profiles.yaml
│   ├── auth_config.yaml
│   └── logging_config.yaml
├── docs/
│   ├── verification_guide.md
│   ├── architecture.md
│   └── api_reference.md
├── pyproject.toml
├── README.md
└── .env.example
```

## Configuration

### Environment Variables

See `.env.example` for all available configuration options.

### Verification Profiles

Configure verification behavior in `config/verification_profiles.yaml`:

```yaml
profiles:
  default:
    scenarios:
      - test_basic_functionality
      - test_git_operations
    context_checks:
      - environment_variables
      - dependency_versions
      - configuration_files
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test type
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m contract      # Contract tests only

# Run with coverage
pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Import sorting
isort src/ tests/
```

## Architecture

The system follows a layered architecture:

```
CLI Layer
    ↓
Service Layer (Verification, Git, Consistency, etc.)
    ↓
Model/Entity Layer
    ↓
Infrastructure Layer (Configuration, Logging, etc.)
```

### Key Components

- **VerificationService**: Orchestrates verification workflows
- **ContextVerificationService**: Validates environment and configuration
- **GitService**: Handles multi-branch Git operations
- **GoalTaskConsistencyService**: Ensures goal-task alignment
- **FormalVerificationService**: Runs formal verification tools
- **TokenOptimizationService**: Monitors and optimizes token usage

## Constitution Compliance

All implementation adheres to the Orchestration Tools Verification and Review Constitution:

- **Verification-First Development**: Comprehensive verification before merge
- **Goal-Task Consistency**: Continuous alignment checking
- **Role-Based Access Control**: Multiple permission levels with appropriate authentication
- **Context-Aware Verification**: Environment, config, dependency, and infrastructure validation
- **Observability**: Structured logging with correlation IDs
- **Performance & Efficiency**: Parallel processing and caching
- **Formal Verification**: 99% coverage of critical paths

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -m "feat: my feature"`
3. Push to branch: `git push origin feature/my-feature`
4. Create a Pull Request

## Documentation

- [Verification Guide](docs/verification_guide.md) - User guide for running verifications
- [Architecture](docs/architecture.md) - System design and components
- [API Reference](docs/api_reference.md) - API endpoint documentation
- [Implementation Plan](../specs/001-orchestration-tools-verification-review/plan.md) - Technical implementation details

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/MasumRab/EmailIntelligence/issues
- Documentation: https://github.com/MasumRab/EmailIntelligence/wiki
