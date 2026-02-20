# Speckit Workflow Wrapper Documentation

## Overview

The Speckit Workflow Wrapper provides a **SOLID**, **modular** interface to execute parts of the Speckit Orchestration Command System as needed. It follows SOLID principles with clear separation of concerns and dependency injection.

## Architecture

### SOLID Principles Applied

1. **Single Responsibility Principle (SRP)**
   - `SpeckitEnvironmentValidator` - Environment validation only
   - `SpeckitTemplateProcessor` - Template processing only  
   - `SpeckitAgentContextManager` - Agent context management only
   - `SpeckitWorkflowOrchestrator` - Workflow orchestration only

2. **Open/Closed Principle (OCP)**
   - `SpeckitWorkflowComposer` - Open for extension, closed for modification
   - New workflow steps can be added without changing existing code

3. **Liskov Substitution Principle (LSP)**
   - All validator classes implement `IWorkflowValidator` interface
   - All processors implement `ITemplateProcessor` interface

4. **Interface Segregation Principle (ISP)**
   - Separate interfaces for each responsibility
   - Clients depend only on interfaces they use

5. **Dependency Inversion Principle (DIP)**
   - High-level modules depend on abstractions (interfaces)
   - `SpeckitWorkflowFactory` handles dependency injection

## Components

### Core Interfaces

```powershell
IWorkflowValidator     - Environment validation
ITemplateProcessor     - Template processing  
IAgentContextManager   - Agent context management
IWorkflowOrchestrator  - Workflow orchestration
```

### Implementation Classes

- `SpeckitEnvironmentValidator` - Validates git branch, resolves paths
- `SpeckitTemplateProcessor` - Copies templates, replaces variables
- `SpeckitAgentContextManager` - Parses plans, updates agent files
- `SpeckitWorkflowOrchestrator` - Manages handoffs between agents
- `SpeckitWorkflowComposer` - Coordinates workflow steps
- `SpeckitWorkflowFactory` - Creates configured instances

## Usage

### CLI Interface

```powershell
# Validate environment only
./SpeckitWorkflowCLI.ps1 -Action Validate

# Setup plan from template with variables
./SpeckitWorkflowCLI.ps1 -Action SetupPlan -Variables "PROJECT NAME=MyFeature,DATE=2025-01-15"

# Update specific agent contexts
./SpeckitWorkflowCLI.ps1 -Action UpdateContext -AgentTypes "claude,qwen"

# Execute full workflow
./SpeckitWorkflowCLI.ps1 -Action FullWorkflow -AgentTypes "claude,qwen,cursor-agent"

# Minimal setup (no agent updates)
./SpeckitWorkflowCLI.ps1 -Action MinimalSetup
```

### Programmatic Interface

```powershell
# Import wrapper
. ".specify/scripts/powershell/SpeckitWorkflowWrapper.ps1"

# Create wrapper instance
$wrapper = [SpeckitWorkflowWrapper]::new()

# Execute individual steps
$wrapper.ExecuteEnvironmentValidation()
$wrapper.ExecutePlanSetup(@{ "PROJECT NAME" = "MyFeature" })
$wrapper.ExecuteAgentContextUpdate(@("claude", "qwen"))

# Execute predefined workflows
$wrapper.ExecuteMinimalPlanSetup()
$wrapper.ExecuteFullPlanWorkflow(@("claude", "qwen", "cursor-agent"))
```

## Workflow Steps

### Available Steps

1. **ValidateEnvironment** - Check git branch, resolve paths
2. **SetupPlan** - Copy plan template, replace variables
3. **UpdateAgentContext** - Parse plan.md, update agent files
4. **ExecuteHandoffs** - Trigger next agents in workflow

### Predefined Combinations

- **MinimalSetup** - Validate + SetupPlan
- **FullWorkflow** - Validate + SetupPlan + UpdateAgentContext

## Configuration

### Agent Types Supported

- `claude` - CLAUDE.md
- `qwen` - .qwen/commands/speckit.implementation.toml
- `cursor-agent` - .cursor/rules/specify-rules.mdc
- `copilot` - .github/agents/copilot-instructions.md
- (Extendable via `GetAgentFilePaths()` method)

### Template Variables

Standard variables available for template replacement:

- `[PROJECT NAME]` - Current feature branch name
- `[DATE]` - Current date (yyyy-MM-dd)
- `[TECH_STACK]` - Computed technology stack from plan.md

## Extending the Wrapper

### Adding New Workflow Steps

1. Define new method in `SpeckitWorkflowComposer.ExecuteStep()`
2. Add corresponding public method in `SpeckitWorkflowWrapper`
3. Update CLI action validation if needed

### Adding New Agent Types

1. Update `GetAgentFilePaths()` in `SpeckitAgentContextManager`
2. Add to CLI help text and parameter validation
3. Update documentation

### Custom Template Processing

1. Extend `SpeckitTemplateProcessor` class
2. Override `ProcessTemplate()` method
3. Implement custom variable replacement logic

## Error Handling

- All operations return boolean success/failure
- Detailed error messages available via exception handling
- CLI provides JSON output for programmatic consumption
- Graceful fallbacks for missing templates/files

## Benefits

1. **Modularity** - Use only the components you need
2. **Testability** - Each component can be unit tested independently
3. **Extensibility** - Easy to add new workflow steps or agent types
4. **Maintainability** - Clear separation of concerns
5. **Flexibility** - Support for different execution patterns

## Migration from Original Scripts

The wrapper maintains compatibility with existing Speckit workflows while providing:

- Backward compatibility with existing template formats
- Same environment validation logic
- Identical agent context generation
- Enhanced error handling and logging
- Modular execution options
