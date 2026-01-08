# Command Specification for 5-Agent CLI Modularization

## Overview

This document specifies the modular command system for the EmailIntelligence CLI, implementing SOLID principles with coordinated agent development.

## Architecture

### SOLID Principles Applied

- **S**ingle Responsibility: Each command class has one responsibility
- **O**pen/Closed: Commands can be extended without modifying existing code
- **L**iskov Substitution: All commands implement the same interface
- **I**nterface Segregation: Command interface is focused and minimal
- **D**ependency Inversion: Commands depend on abstractions, not concretions

### Components

1. **Command Interface** (`interface.py`): Abstract base class defining the command contract
2. **Command Factory** (`factory.py`): Factory pattern for dependency injection
3. **Command Registry** (`registry.py`): Centralized command management and agent assignment

## Agent Coordination

### Agent Roles

| Agent | Role | Commands | Responsibility |
|-------|------|----------|----------------|
| **Agent 1** (Foundation) | Architecture & Infrastructure | N/A | Creates SOLID foundation, coordinates other agents |
| **Agent 2** (Analyze) | Analysis Commands | `analyze` | Implements repository conflict analysis |
| **Agent 3** (Resolve) | Resolution Commands | `resolve` | Implements conflict resolution strategies |
| **Agent 4** (Validate) | Validation Commands | `validate` | Implements validation and quality checks |
| **Agent 5** (History) | History Commands | `analyze-history`, `plan-rebase` | Implements git history analysis and planning |

### Command Specifications

#### 1. Analyze Command (Agent 2)

**Name**: `analyze`  
**Description**: Analyze repository conflicts between branches  

**Arguments**:
- `repo_path` (required): Path to the repository
- `--pr` (optional): Pull Request ID
- `--base-branch` (optional): Base branch for comparison (default: main)
- `--head-branch` (optional): Head branch for comparison (default: current)

**Dependencies**:
- `GitConflictDetector`: Detects conflicts between branches
- `ConstitutionalAnalyzer`: Analyzes conflict complexity
- `StrategyGenerator`: Generates resolution strategies
- `RepositoryOperations`: Repository operations

**Output**: Conflict analysis with risk levels and strategies

#### 2. Resolve Command (Agent 3)

**Name**: `resolve`  
**Description**: Resolve a specific conflict using a strategy  

**Arguments**:
- `conflict_id` (required): ID of the conflict to resolve
- `strategy_id` (required): ID of the strategy to use

**Dependencies**:
- `AutoResolver`: Executes resolution strategies
- `ValidationOrchestrator`: Validates resolution results

**Output**: Resolution result with success/failure status

#### 3. Validate Command (Agent 4)

**Name**: `validate`  
**Description**: Run validation checks on the codebase  

**Arguments**: None required  

**Dependencies**:
- `ValidationOrchestrator`: Runs validation checks
- All validation components

**Output**: Validation results with scores and recommendations

#### 4. Analyze History Command (Agent 5)

**Name**: `analyze-history`  
**Description**: Analyze git commit history and patterns  

**Arguments**:
- `--branch` (optional): Branch to analyze (default: HEAD)
- `--output` (optional): Output file for report

**Dependencies**:
- `GitHistory`: Retrieves commit history
- `CommitClassifier`: Classifies commits by type/risk

**Output**: Analysis report with commit statistics and patterns

#### 5. Plan Rebase Command (Agent 5)

**Name**: `plan-rebase`  
**Description**: Generate optimal rebase plan for a branch  

**Arguments**:
- `--branch` (optional): Branch to plan rebase for (default: HEAD)
- `--output` (required): Output file for rebase plan

**Dependencies**:
- `GitHistory`: Retrieves commit history
- `CommitClassifier`: Classifies commits
- `RebasePlanner`: Generates rebase plans

**Output**: Rebase plan file with recommended commit ordering

## Implementation Guidelines

### For Each Agent

1. **Create Command Class**: Implement the `Command` ABC
2. **Define Properties**: `name`, `description`
3. **Implement Methods**:
   - `add_arguments()`: Add command-specific arguments
   - `execute()`: Main command logic with error handling
   - `get_dependencies()`: Return required dependencies
   - `set_dependencies()` (optional): Store injected dependencies
4. **Handle Errors**: Return appropriate exit codes
5. **Test Thoroughly**: Unit tests for each command

### Command Class Template

```python
from argparse import Namespace
from typing import Any, Dict

from .interface import Command


class ExampleCommand(Command):
    @property
    def name(self) -> str:
        return "example"

    @property
    def description(self) -> str:
        return "Example command description"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--option", help="Example option")

    def get_dependencies(self) -> Dict[str, Any]:
        return {
            "dependency_name": DependencyClass
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._dependency = dependencies.get("dependency_name")

    async def execute(self, args: Namespace) -> int:
        try:
            # Command implementation
            return 0  # Success
        except Exception as e:
            print(f"Error: {e}")
            return 1  # Failure
```

## Integration Points

### CLI Entry Point Updates

The main CLI entry point (`emailintelligence_cli.py`) will need updates to:

1. Import the command registry
2. Register all command classes
3. Use the registry to dispatch commands
4. Maintain backward compatibility

### Dependency Management

Global dependencies should be injected through the factory:

```python
# In CLI entry point
dependencies = {
    "worktree_manager": WorktreeManager(),
    "conflict_detector": GitConflictDetector(),
    "analyzer": ConstitutionalAnalyzer(),
    # ... other dependencies
}

factory = CommandFactory(dependencies)
registry = CommandRegistry(factory)

# Register commands
registry.register_command(AnalyzeCommand, "analyze-agent")
# ... register other commands
```

## Testing Strategy

### Unit Tests
- Test each command class independently
- Mock dependencies in tests
- Test argument parsing
- Test error conditions

### Integration Tests
- Test full command execution
- Test dependency injection
- Test registry functionality

### Command Tests Template

```python
import pytest
from argparse import Namespace

from src.cli.commands.example_command import ExampleCommand


class TestExampleCommand:
    def test_name_property(self):
        cmd = ExampleCommand()
        assert cmd.name == "example"

    def test_execute_success(self):
        cmd = ExampleCommand()
        args = Namespace(option="test")
        result = await cmd.execute(args)
        assert result == 0

    def test_execute_failure(self):
        cmd = ExampleCommand()
        args = Namespace(option="invalid")
        result = await cmd.execute(args)
        assert result == 1
```

## Phase Implementation Order

1. **Phase 1** (COMPLETED): SOLID foundation ✅
2. **Phase 2** (COMPLETED): Individual command implementation ✅
3. **Phase 3** (COMPLETED): CLI integration ✅
4. **Phase 4** (COMPLETED): Testing ✅
5. **Phase 5** (COMPLETED): Documentation and cleanup ✅

## Implementation Status

### Command Classes

#### AnalyzeCommand
- **Status**: Implemented ✅
- **File**: `src/cli/commands/analyze_command.py`
- **Dependencies**: GitConflictDetector, ConstitutionalAnalyzer, StrategyGenerator, RepositoryOperations
- **Exit Codes**: 0 = Success, 1 = Error
- **Error Handling**: Prints error message to stderr, returns exit code 1
- **Tests**: `tests/unit/cli/commands/test_analyze_command.py`

#### ResolveCommand
- **Status**: Implemented ✅
- **File**: `src/cli/commands/resolve_command.py`
- **Dependencies**: AutoResolver, Validator
- **Exit Codes**: 0 = Success, 1 = Error
- **Error Handling**: Prints error message to stderr, returns exit code 1

#### ValidateCommand
- **Status**: Implemented ✅
- **File**: `src/cli/commands/validate_command.py`
- **Dependencies**: Validator
- **Exit Codes**: 0 = Success, 1 = Error
- **Error Handling**: Prints error message to stderr, returns exit code 1
- **Tests**: `tests/unit/cli/commands/test_validate_command.py`

#### AnalyzeHistoryCommand
- **Status**: Implemented ✅
- **File**: `src/cli/commands/analyze_history_command.py`
- **Dependencies**: GitHistory, CommitClassifier
- **Exit Codes**: 0 = Success, 1 = Error
- **Error Handling**: Prints error message to stderr, returns exit code 1

#### PlanRebaseCommand
- **Status**: Implemented ✅
- **File**: `src/cli/commands/plan_rebase_command.py`
- **Dependencies**: GitHistory, CommitClassifier, RebasePlanner
- **Exit Codes**: 0 = Success, 1 = Error
- **Error Handling**: Prints error message to stderr, returns exit code 1

### System Components

#### SOLID Foundation
- **Status**: Implemented ✅
- **Files**: `interface.py`, `factory.py`, `registry.py`
- **Features**: Command ABC, dependency injection, centralized management

#### CLI Integration
- **Status**: Implemented ✅
- **File**: `src/cli/commands/integration.py`
- **Features**: Factory setup, registry management, command dispatch
- **Entry Point**: `emailintelligence_cli.py` updated with modular support

#### Testing Framework
- **Status**: Implemented ✅
- **Unit Tests**: Command instantiation, argument parsing, dependency injection
- **Integration Tests**: Registry creation, command dispatch, agent assignment
- **Coverage**: 5 command classes + integration layer

## Quality Assurance

- All commands must implement the Command interface
- Commands must handle errors gracefully
- Exit codes must follow Unix conventions (0=success, 1=failure)
- Commands must be testable in isolation
- Dependencies must be properly injected

## Next Steps

1. Each agent implements their assigned commands following this specification
2. Commands are tested individually
3. CLI entry point is updated to use the new system
4. Integration testing ensures everything works together
5. Documentation is updated with new command structure