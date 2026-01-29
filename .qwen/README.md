# Session Management System

This directory contains the session management system for the Taskmaster project. It provides state management, session tracking, and continuity across development sessions.

## Files

- `session_manager.py` - Core session management functionality
- `session_cli.py` - Command-line interface for session management
- `state.json` - Global project state and command history
- `session.json` - Current session information
- `handoff.json` - Pending handoffs between commands
- `predictions/` - Directory for prediction-related data
- Other command-specific directories for various development phases

## Usage

### Command-Line Interface

The session management system provides a CLI with the following commands:

```bash
# Start a new session with goals
python .qwen/session_cli.py start --goals "Goal 1,Goal 2,Goal 3"

# Show current session information
python .qwen/session_cli.py show

# Show project context
python .qwen/session_cli.py context

# End the current session
python .qwen/session_cli.py end
```

### Programmatic Usage

```python
from .qwen.session_manager import SessionManager

# Initialize session manager for the current project
sm = SessionManager("/path/to/project")

# Start a session
session_info = sm.start_session(
    goals=["Implement feature X", "Fix bug Y"]
)

# End the session
sm.end_session()

# Get current session info
current_session = sm.get_current_session()
```

## State Management

The system maintains state in three key files:

1. **state.json** - Tracks the current session ID and command history
2. **session.json** - Stores detailed information about the current session
3. **handoff.json** - Manages pending handoffs between different commands or processes

## Project Registration

Projects are registered in `~/.qwen/projects/registry.json` to enable cross-project functionality.

## Directory Structure

The system creates command-specific directories under `.qwen/` to organize data by development phase:

- `understand/` - Understanding phase data
- `analyze/` - Analysis phase data
- `implement/` - Implementation phase data
- `test/` - Testing phase data
- `document/` - Documentation phase data
- `verify/` - Verification phase data
- `migrate/` - Migration phase data
- `refactor/` - Refactoring phase data
- `enhance/` - Enhancement phase data
- `optimize/` - Optimization phase data
- `secure/` - Security phase data
- `deploy/` - Deployment phase data
- `monitor/` - Monitoring phase data
- `backup/` - Backup phase data
- `archive/` - Archive phase data
- `temp/` - Temporary data
- `predictions/` - Prediction-related data