# Quickstart Guide: Agent Context Control

**Date**: 2025-11-10 | **Spec**: specs/001-agent-context-control/spec.md | **Data Models**: specs/001-agent-context-control/data-model.md

## Overview

This guide gets you started with the Agent Context Control system in under 10 minutes. The system automatically detects your Git branch and provides appropriate context isolation for AI agents.

## Prerequisites

- Python 3.11+
- Git repository
- Basic understanding of JSON/YAML configuration

## Installation

### Option 1: Install from Source

```bash
# Clone the repository
git clone https://github.com/your-org/agent-context-control.git
cd agent-context-control

# Install in development mode
pip install -e .
```

### Option 2: Install from PyPI

```bash
pip install agent-context-control
```

## Basic Usage

### 1. Initialize Context Control

```python
from context_control import ContextController

# Initialize with default settings
controller = ContextController()

# Or with custom configuration
controller = ContextController(
    context_dir="./my-contexts",
    encryption_enabled=True
)
```

### 2. Detect Current Context

```python
# Automatically detect branch and load context
context = controller.get_context()

print(f"Current context: {context.context_id}")
print(f"Environment: {context.environment}")
print(f"Max concurrent tasks: {context.max_concurrent_tasks}")
```

### 3. Check Feature Flags

```python
# Check if features are enabled
if context.is_feature_enabled("advanced_logging"):
    print("Advanced logging is enabled")
    # Configure advanced logging
else:
    print("Using basic logging")
```

### 4. Access Environment Variables

```python
# Get environment-specific variables
api_key = context.get_env_var("MY_API_KEY")
database_url = context.get_env_var("DATABASE_URL", "sqlite:///default.db")
```

## Creating Context Profiles

### Basic Context Profile

Create a JSON file in your `.agent-context/` directory:

```json
{
  "context_id": "main-development",
  "branch": "main",
  "environment": "development",
  "agent_config": {
    "max_concurrent_tasks": 3,
    "timeout_seconds": 60,
    "memory_limit_mb": 512
  },
  "feature_flags": {
    "debug_mode": true,
    "performance_monitoring": false
  },
  "api_keys": {
    "openai_api_key": "your-development-key-here"
  }
}
```

### Advanced Context Profile

```json
{
  "context_id": "feature-ai-integration",
  "branch": "feature/ai-integration",
  "environment": "development",
  "agent_config": {
    "max_concurrent_tasks": 5,
    "timeout_seconds": 300,
    "memory_limit_mb": 1024,
    "custom_settings": {
      "model": "gpt-4",
      "temperature": 0.7
    }
  },
  "feature_flags": {
    "ai_integration": true,
    "experimental_features": true,
    "detailed_logging": true
  },
  "api_keys": {
    "openai_api_key": "sk-proj-...",
    "anthropic_api_key": "sk-ant-...",
    "google_ai_key": "AIza..."
  },
  "metadata": {
    "created_by": "developer@example.com",
    "purpose": "AI integration testing",
    "review_required": true
  }
}
```

## CLI Usage

### Initialize a New Project

```bash
# Initialize context control in current directory
context-control init

# Initialize with custom settings
context-control init --context-dir .contexts --encrypt
```

### List Available Contexts

```bash
# Show all context profiles
context-control list

# Show contexts for current branch
context-control list --current
```

### Validate Context Files

```bash
# Validate all context files
context-control validate

# Validate specific file
context-control validate main.json
```

### Get Current Context

```bash
# Show current context information
context-control current

# Export context as JSON
context-control current --json
```

### Create New Context

```bash
# Create context interactively
context-control create

# Create from template
context-control create --template development --branch feature/new-feature
```

## Integration Examples

### With AI Agent Framework

```python
from context_control import ContextController
from my_agent_framework import Agent

class ContextAwareAgent(Agent):
    def __init__(self):
        super().__init__()
        self.context_controller = ContextController()

    def initialize(self):
        """Initialize agent with context-aware settings."""
        context = self.context_controller.get_context()

        # Configure based on context
        self.max_tasks = context.max_concurrent_tasks
        self.timeout = context.timeout_seconds

        # Set API keys from context
        if context.is_feature_enabled("openai_integration"):
            self.openai_key = context.get_env_var("OPENAI_API_KEY")

        # Environment-specific logging
        if context.environment == "production":
            self.enable_production_logging()
        else:
            self.enable_debug_logging()

    def process_task(self, task):
        """Process task with context awareness."""
        context = self.context_controller.get_context()

        # Context-specific processing
        if context.is_feature_enabled("performance_monitoring"):
            start_time = time.time()

        result = super().process_task(task)

        if context.is_feature_enabled("performance_monitoring"):
            duration = time.time() - start_time
            self.log_performance(task.id, duration)

        return result
```

### With Web Framework

```python
from flask import Flask, g
from context_control import ContextController

app = Flask(__name__)
context_controller = ContextController()

@app.before_request
def load_context():
    """Load context for each request."""
    g.context = context_controller.get_context()

@app.route('/api/tasks')
def get_tasks():
    """API endpoint with context-aware behavior."""
    context = g.context

    # Context-specific API behavior
    if context.is_feature_enabled("rate_limiting"):
        # Apply rate limiting
        pass

    if context.environment == "production":
        # Production-specific logic
        tasks = get_production_tasks()
    else:
        # Development/staging logic
        tasks = get_development_tasks()

    return {"tasks": tasks, "context": context.context_id}

@app.route('/debug')
def debug_info():
    """Debug endpoint only available in non-production."""
    context = g.context

    if context.environment == "production":
        return {"error": "Debug not available in production"}, 403

    return {
        "context": context.dict(),
        "feature_flags": context.feature_flags,
        "config": context.agent_config
    }
```

### With Testing Framework

```python
import pytest
from context_control import ContextController

@pytest.fixture(scope="session")
def context_controller():
    """Provide context controller for tests."""
    return ContextController()

@pytest.fixture
def current_context(context_controller):
    """Provide current context for tests."""
    return context_controller.get_context()

def test_feature_flag_integration(current_context):
    """Test that feature flags work correctly."""
    if current_context.is_feature_enabled("test_feature"):
        # Test feature-specific behavior
        assert some_feature_works()
    else:
        # Test default behavior
        assert default_behavior_works()

def test_environment_isolation(context_controller):
    """Test that different branches get different contexts."""
    # Test main branch
    context_main = context_controller.get_context_for_branch("main")
    assert context_main.environment == "production"

    # Test development branch
    context_dev = context_controller.get_context_for_branch("develop")
    assert context_dev.environment == "development"

    # Contexts should be different
    assert context_main.context_id != context_dev.context_id
```

## Configuration Options

### Environment Variables

```bash
# Override context directory
export AGENT_CONTEXT_DIR="/path/to/contexts"

# Force specific context
export AGENT_CONTEXT_ID="custom-context"

# Disable encryption (not recommended for production)
export AGENT_CONTEXT_ENCRYPT="false"

# Set encryption key
export AGENT_CONTEXT_KEY="your-32-char-encryption-key-here"
```

### Configuration File

Create `context-control.yaml`:

```yaml
context_dir: ".agent-context"
encryption:
  enabled: true
  key: "your-encryption-key"
cache:
  enabled: true
  ttl_seconds: 300
validation:
  strict: true
  schema_version: "1.0.0"
```

## Troubleshooting

### Common Issues

**"Context file not found"**

```bash
# Check if context directory exists
ls -la .agent-context/

# Create default context
context-control create --branch main --environment development
```

**"Branch detection failed"**

```bash
# Check git status
git status

# Manual branch detection
git branch --show-current

# Force specific context
export AGENT_CONTEXT_ID="main-development"
```

**"Validation errors"**

```bash
# Validate all files
context-control validate

# Check specific file
context-control validate main.json --verbose
```

**"Permission denied"**

```bash
# Fix permissions on context directory
chmod 755 .agent-context/
chmod 644 .agent-context/*.json
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

controller = ContextController()
context = controller.get_context()
```

Or via environment:

```bash
export AGENT_CONTEXT_DEBUG="true"
```

## Advanced Usage

### Custom Context Detection

```python
from context_control import ContextController, BranchDetector

class CustomDetector(BranchDetector):
    def detect_branch(self, repo_path: str) -> str:
        # Custom branch detection logic
        branch = super().detect_branch(repo_path)

        # Add custom logic
        if branch.startswith("feature/"):
            return f"feature-{branch.split('/', 1)[1]}"

        return branch

# Use custom detector
controller = ContextController(branch_detector=CustomDetector())
```

### Context Hooks

```python
from context_control import ContextController, ContextHook

class LoggingHook(ContextHook):
    def on_context_load(self, context):
        print(f"Loaded context: {context.context_id}")

    def on_context_switch(self, old_context, new_context):
        print(f"Switched from {old_context.context_id} to {new_context.context_id}")

controller = ContextController(hooks=[LoggingHook()])
```

### Performance Monitoring

```python
import time
from context_control import ContextController

controller = ContextController()

# Measure context loading performance
start = time.perf_counter()
context = controller.get_context()
duration = time.perf_counter() - start

print(f"Context loaded in {duration:.3f} seconds")
assert duration < 0.5  # Performance requirement
```

## Next Steps

- Read the [full specification](spec.md) for detailed requirements
- Explore the [data models](data-model.md) for advanced usage
- Check the [API contracts](contracts/) for integration details
- Review the [implementation plan](plan.md) for development roadmap

## Support

- **Documentation**: [Full API Reference](contracts/)
- **Issues**: [GitHub Issues](https://github.com/your-org/agent-context-control/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/agent-context-control/discussions)