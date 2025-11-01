# Contributing to EmailIntelligence

Thank you for your interest in contributing to EmailIntelligence! This document provides guidelines and information for contributors.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:
- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## Getting Started

1. **Set up your development environment** following the [Getting Started Guide](docs/getting_started.md)
2. **Familiarize yourself with the codebase** by reading the [Architecture Overview](docs/architecture_overview.md)
3. **Check existing issues** in the backlog to find tasks to work on
4. **Join our community** discussions for questions and collaboration

## Branch Naming Standards

We use standardized branch naming to maintain consistency across the repository:

### Branch Types
- **`feature/short-description`** - New features and enhancements
- **`bugfix/short-description`** - Bug fixes and patches
- **`hotfix/short-description`** - Urgent production fixes
- **`refactor/short-description`** - Code refactoring and restructuring
- **`docs/short-description`** - Documentation updates

### Examples
```bash
git checkout -b feature/email-filtering-enhancement
git checkout -b bugfix/api-authentication-fix
git checkout -b refactor/workflow-engine-consolidation
git checkout -b docs/setup-instructions-update
```

### Guidelines
- Use lowercase letters and hyphens for separation
- Keep descriptions concise but descriptive
- Reference issue numbers when applicable: `bugfix/123-auth-validation`
- Avoid generic names like `fix-bug` or `new-feature`

## Development Workflow

### 1. Choose a Task
- Check the `backlog/tasks/` directory for available tasks
- Look for tasks marked as "To Do" or "In Progress"
- Comment on issues to indicate interest

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

### 3. Implement Changes
- Follow the acceptance criteria in the task description
- Write tests for new functionality
- Update documentation as needed
- Ensure code follows our standards

### 4. Test Your Changes
```bash
# Run full test suite
pytest

# Run specific tests
pytest tests/path/to/test.py

# Check code quality
black . --check
isort . --check
flake8 src/
mypy src/
```

### 5. Commit Changes
```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add new email filtering capability

- Implement advanced filtering logic
- Add tests for filter validation
- Update API documentation

Closes #123"
```

### 6. Create Pull Request
- Push your branch: `git push origin feature/your-feature-name`
- Create a PR with a clear description
- Reference the task number in the PR description
- Request review from maintainers

## Code Standards

### Python Code Style
- **Formatting**: Black (100 character line length)
- **Imports**: isort (stdlib → third-party → local)
- **Linting**: flake8
- **Type Hints**: Required for all function parameters and return values
- **Docstrings**: Google-style for public functions/classes

### TypeScript/React Code Style
- **Strict Mode**: Enabled
- **JSX**: react-jsx transform
- **Imports**: @/ for client src, @shared/ for shared types
- **Components**: Default export functions, PascalCase naming
- **Styling**: Tailwind CSS utilities

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Naming Conventions
- **Python**: snake_case for functions/variables, PascalCase for classes
- **TypeScript**: camelCase for variables/functions, PascalCase for components/types
- **Files**: kebab-case for file names, PascalCase for React components

## Testing

### Test Structure
```
tests/
├── core/           # Core functionality tests
├── modules/        # Module-specific tests
├── integration/    # Integration tests
└── conftest.py     # Test configuration
```

### Test Guidelines
- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Coverage**: Aim for 80%+ code coverage
- **Mocking**: Use pytest-mock for external dependencies

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/core/test_security.py

# Watch mode (requires pytest-watch)
pytest --watch
```

## Documentation

### Documentation Types
- **Code Comments**: Explain complex logic, not obvious behavior
- **Docstrings**: Document all public APIs
- **READMEs**: Component-level documentation
- **Guides**: User and developer guides in `docs/`
- **API Docs**: Auto-generated from code comments

### Documentation Standards
- **Language**: American English
- **Format**: Markdown for guides, reStructuredText for API docs
- **Structure**: Clear headings, code examples, screenshots where helpful
- **Updates**: Keep documentation current with code changes

## Pull Request Process

### PR Requirements
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Self-review completed
- [ ] Related issues linked

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] Self-review completed
```

### Review Process
1. **Automated Checks**: CI runs tests and linting
2. **Peer Review**: At least one maintainer review required
3. **Approval**: Maintainers approve and merge
4. **Deployment**: Automated deployment to staging

## Issue Reporting

### Bug Reports
- **Title**: Clear, descriptive title
- **Description**: Steps to reproduce, expected vs actual behavior
- **Environment**: OS, Python/Node versions, browser
- **Logs**: Error messages, stack traces
- **Screenshots**: Visual issues

### Feature Requests
- **Title**: Clear feature description
- **Use Case**: Why is this feature needed?
- **Implementation Ideas**: How could this be implemented?
- **Alternatives**: Considered alternatives

### Task Format
Tasks follow a standardized format in `backlog/tasks/`:
- **Title**: Clear, actionable description
- **Description**: Context and purpose
- **Acceptance Criteria**: Specific, testable requirements
- **Implementation Notes**: Technical details and approach

## Getting Help

- **Documentation**: Check `docs/` directory first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub discussions for questions
- **Community**: Join our community channels

## Recognition

Contributors are recognized through:
- GitHub contributor statistics
- Mention in release notes
- Contributor spotlight in documentation
- Invitation to become maintainers

Thank you for contributing to EmailIntelligence! 🎉