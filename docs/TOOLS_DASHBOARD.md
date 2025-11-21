# Tools Dashboard

## Overview

The Tools Dashboard provides a centralized web interface for accessing and managing the various scripts, tools, and isolated components within the Email Intelligence platform. This dashboard helps prevent context contamination by providing safe, controlled access to potentially isolated functionality.

## Features

### Tool Categories

The dashboard organizes tools into the following categories:

- **Context Control**: Tools for managing agent context isolation
- **Monitoring**: Agent performance and health monitoring tools
- **Analysis**: Codebase analysis and validation scripts
- **Validation**: Import validation and integrity checking
- **Task Management**: Task completion tracking and prediction
- **Maintenance**: System maintenance and documentation tools

### Available Tools

#### Context Control Tools
- `context-control`: CLI tool for Agent Context Control
- Health check: `validate_context`

#### Monitoring Tools
- `agent_performance_monitor`: Real-time agent performance metrics
- `agent_health_monitor`: Monitor agent health status
- Health checks: `check_agent_health`, `check_agent_status`

#### Analysis Tools
- `codebase_analysis`: Comprehensive codebase analysis
- `analyze_repo`: Repository analysis and metrics
- Health checks: `check_codebase`, `check_repo_analysis`

#### Validation Tools
- `validate_imports`: Import validation for CI/CD pipeline
- `worktree_context_detector`: Detect worktree context for git hooks
- `incremental_validator`: Incremental validation of changes
- `validation_cache`: Cache validation results for performance

#### Task Management Tools
- `task_completion_tracker`: Track task completion progress
- `completion_predictor`: Predict task completion times

#### Maintenance Tools
- `maintenance_scheduler`: Schedule maintenance tasks
- `maintenance_docs`: Generate maintenance documentation

## Accessing the Dashboard

1. Navigate to `/tools` in the web application
2. The dashboard will automatically load and display tool status
3. Tools are organized by category using tabs
4. System health overview shows total tools and healthy tools count

## Using Tools

### Executing Scripts

1. Click the **"Execute"** button on any tool card
2. The script will run with a 30-second timeout
3. Results are displayed in the "Recent Executions" section
4. Success/failure status is indicated with color coding

### Monitoring Tool Health

- **Green (✓)**: Tool is healthy and can be executed
- **Red (✗)**: Tool has errors (import errors, missing files, etc.)
- **Yellow (⚠)**: Tool has warnings (not executable, etc.)
- **Blue (⟳)**: Tool status is being checked

## Security Considerations

### Isolation Boundaries
- Scripts run in separate processes with timeout protection
- Working directory is controlled and validated
- PYTHONPATH is set to project root for proper imports
- File system access is restricted to project boundaries

### Authentication
- All dashboard access requires user authentication
- Tool execution is logged with user information
- Access control follows the same patterns as other dashboard features

## API Endpoints

### GET `/api/tools/dashboard`
Returns the complete tools dashboard data including:
- Tool status information
- System health metrics
- Available categories

### POST `/api/tools/execute`
Executes a script with the specified parameters:
```json
{
  "script_name": "context-control",
  "args": ["--validate"],
  "working_directory": null
}
```

### GET `/api/tools/categories`
Returns list of available tool categories.

### GET `/api/tools/tools/{category}`
Returns tools filtered by category.

## Development and Testing

### Running Tests
```bash
pytest tests/test_tools_dashboard.py -v
```

### Adding New Tools
To add a new tool to the dashboard:

1. Add tool configuration to `AVAILABLE_TOOLS` in `tools_dashboard_routes.py`
2. Ensure the script exists and is executable
3. Add appropriate health check logic if needed
4. Update tests to cover the new tool

### Tool Configuration Format
```python
{
    "name": "tool_name",
    "category": "Tool Category",
    "description": "Description of what the tool does",
    "script_path": "relative/path/to/script.py",
    "health_check": "health_check_function_name"
}
```

## Troubleshooting

### Common Issues

1. **Tool shows as "not found"**
   - Verify the script path exists relative to project root
   - Check file permissions

2. **Tool shows "import error"**
   - Ensure all dependencies are installed
   - Check PYTHONPATH configuration

3. **Script execution times out**
   - Scripts have a 30-second timeout by default
   - Long-running scripts may need to be run directly

4. **Permission denied errors**
   - Ensure scripts have execute permissions
   - Check file system permissions

### Logs and Debugging
- Tool execution is logged to the application logs
- Failed executions include error output
- Check browser developer tools for API errors

## Integration with Isolation Issues

This dashboard directly addresses the isolation concerns identified in the codebase:

1. **Centralized Access**: Provides safe access to potentially isolated scripts
2. **Health Monitoring**: Shows which tools are properly isolated and functional
3. **Controlled Execution**: Prevents accidental execution of isolation-breaking code
4. **Status Tracking**: Helps identify which tools need refactoring for proper isolation

## Future Enhancements

- Add script execution history and logs
- Implement tool dependency management
- Add batch execution capabilities
- Integrate with Task Master AI for automated tool execution
- Add real-time execution progress indicators