# Multi-Agent Code Review System

## Overview

The Multi-Agent Code Review System is an automated code analysis tool that uses multiple specialized agents to perform comprehensive code reviews. Each agent focuses on a specific aspect of code quality:

1. **Security Review Agent** - Identifies potential security vulnerabilities
2. **Performance Review Agent** - Finds performance bottlenecks and optimization opportunities
3. **Quality Review Agent** - Evaluates code quality, maintainability, and best practices
4. **Architecture Review Agent** - Reviews architectural consistency and design patterns

## Installation

The system is included in the EmailIntelligence project and requires no additional installation. All dependencies are already specified in `pyproject.toml`.

## Usage

### Running a Code Review

To run a code review on the entire project:

```bash
python tools/review/main.py
```

To review specific files or directories:

```bash
python tools/review/main.py --target src/main.py backend/python_backend/
```

To generate a report in a specific format:

```bash
python tools/review/main.py --format markdown --output review_report.md
```

### Pre-Commit Hook

The system includes a pre-commit hook that automatically runs code review before each commit. To install it:

```bash
# Copy the hook to the git hooks directory
cp tools/review/pre_commit_hook.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Configuration

The review system can be configured using `tools/review/config.json`:

```json
{
  "review_agents": {
    "security": {
      "enabled": true,
      "priority": "high"
    },
    "performance": {
      "enabled": true,
      "priority": "medium"
    },
    "quality": {
      "enabled": true,
      "priority": "medium"
    },
    "architecture": {
      "enabled": true,
      "priority": "high"
    }
  },
  "trigger_events": {
    "pre_commit": true,
    "post_merge": true,
    "significant_changes": true
  },
  "file_patterns": {
    "include": [
      "**/*.py",
      "client/src/**/*.ts",
      "client/src/**/*.tsx"
    ],
    "exclude": [
      "node_modules/**",
      "venv/**",
      "**/*.test.py",
      "**/test_*.py"
    ]
  }
}
```

## Agent Details

### Security Review Agent

Identifies potential security vulnerabilities including:
- Hardcoded secrets (passwords, API keys, tokens)
- Insecure subprocess usage
- SQL injection vulnerabilities
- Code injection vulnerabilities (eval, exec)
- Input sanitization issues

### Performance Review Agent

Finds performance bottlenecks and optimization opportunities:
- Inefficient loops and algorithms
- Memory usage issues
- Database query optimization
- File I/O optimization
- Network call optimization

### Quality Review Agent

Evaluates code quality, maintainability, and best practices:
- Code complexity
- Documentation and comments
- Naming conventions
- Code duplication
- Error handling
- Test coverage

### Architecture Review Agent

Reviews architectural consistency and design patterns:
- Layer separation
- Dependency management
- Module organization
- Design patterns
- Code cohesion
- Component coupling

## Integration with Development Workflow

The system integrates with the development workflow in several ways:

1. **Pre-Commit Validation** - Automatically runs on every commit to prevent issues from being committed
2. **Post-Merge Analysis** - Runs after merging to ensure code quality in the main branch
3. **Significant Changes Review** - Triggers on significant changes to provide immediate feedback
4. **Manual Reviews** - Can be run manually at any time for comprehensive analysis

## Priority Levels

Issues are categorized by priority:
- **Critical** - Must be fixed immediately (security vulnerabilities, major performance issues)
- **High** - Should be fixed soon (architecture violations, significant quality issues)
- **Medium** - Consider fixing in the near future (moderate issues)
- **Low** - Nice to fix when time permits (minor issues, style improvements)

## Customization

The system can be customized by:
1. Modifying the configuration file
2. Extending existing agents
3. Creating new specialized agents
4. Adjusting the rules and patterns used by each agent

To create a new agent, extend the `BaseReviewAgent` class and implement the `review_file` method.