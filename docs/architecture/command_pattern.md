# Command Pattern Implementation

## Overview

The EmailIntelligence project uses a command pattern implementation to provide a modular and extensible architecture for handling different operations. This pattern allows for clean separation of concerns and makes it easy to add new commands without modifying existing code.

## Architecture

### Core Components

1. **Command Interface** (`setup/commands/command_interface.py`)
   - Abstract base class that defines the contract for all commands
   - Methods: `get_description()`, `validate_args()`, `execute()`, `cleanup()`

2. **Command Factory** (`setup/commands/command_factory.py`)
   - Factory class responsible for creating command instances
   - Maps command names to their corresponding classes
   - Provides methods to get available commands and their descriptions

3. **Concrete Commands** (`setup/commands/*.py`)
   - `SetupCommand` - Handles environment setup
   - `RunCommand` - Handles application execution
   - `TestCommand` - Handles test execution
   - `CheckCommand` - Handles system validation and checks

4. **Container** (`setup/container.py`)
   - Simple dependency injection container
   - Manages service lifecycle and dependencies

### Command Interface

All commands must implement the `Command` abstract base class:

```python
class Command(ABC):
    def __init__(self, args: Namespace = None):
        self.args = args

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def validate_args(self) -> bool:
        pass

    @abstractmethod
    def execute(self) -> int:
        pass

    def cleanup(self) -> None:
        pass
```

### Command Factory

The command factory is responsible for creating command instances:

```python
factory = get_command_factory()
command = factory.create_command("setup", args)
result = command.execute()
```

## Usage

### Command Line Interface

The command pattern is integrated into the main launcher:

```bash
# Setup the environment
python launch.py setup

# Run the application
python launch.py run

# Run tests
python launch.py test

# Run checks
python launch.py check
```

### Adding New Commands

To add a new command:

1. Create a new command class that inherits from `Command`
2. Implement the required abstract methods
3. Register the command in the `CommandFactory`
4. Add the command to the argument parser in `launch.py`

Example:

```python
# new_command.py
from .command_interface import Command

class NewCommand(Command):
    def get_description(self) -> str:
        return "Description of the new command"

    def validate_args(self) -> bool:
        # Validate command arguments
        return True

    def execute(self) -> int:
        # Execute the command logic
        return 0
```

## Benefits

1. **Modularity**: Each command is self-contained
2. **Extensibility**: Easy to add new commands
3. **Testability**: Commands can be tested in isolation
4. **Maintainability**: Clear separation of concerns
5. **Consistency**: Uniform interface for all operations

## Error Handling

The command pattern includes robust error handling:

- Argument validation before execution
- Exception handling during execution
- Cleanup operations after execution
- Proper exit codes for success/failure

## Testing

Commands can be tested using the test framework:

```bash
python setup/test_commands.py
```

This will test command creation and basic functionality.