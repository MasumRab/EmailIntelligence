# Project Configuration System

## Overview

The EmailIntelligence project uses a dynamic configuration system to define project structure and component locations. This prevents issues during major refactors when file locations change, as the system automatically discovers and validates the current project structure.

## Key Benefits

- **Refactor-Safe**: No hardcoded paths that break during restructuring
- **Auto-Discovery**: Automatically finds available services and components
- **Validation**: Ensures project structure integrity before operations
- **Extensible**: Easy to add new services or modify existing configurations

## Architecture

### Core Components

1. **ProjectConfig**: Main configuration class that manages project structure
2. **ProjectPaths**: Defines all standard directory paths
3. **ProjectComponents**: Defines components, services, and validation rules

### Configuration Discovery

The system automatically discovers:
- Project root directory
- Available services (Python backend, TypeScript backend, frontend)
- Critical files for merge conflict checking
- Required directories and files

## Usage

### Basic Usage

```python
from setup.project_config import get_project_config

config = get_project_config()

# Access paths
backend_path = config.paths.backend
python_backend = config.paths.python_backend

# Get service information
frontend_config = config.get_service_config("frontend")
frontend_path = config.get_service_path("frontend")

# Validate structure
issues = config.validate_structure()
if issues:
    print("Configuration issues found:", issues)
```

### Service Discovery

```python
# Auto-discover available services
services = config.discover_services()
# Returns: {"python_backend": {...}, "frontend": {...}, ...}
```

### Critical Files

```python
# Get files to check for merge conflicts
critical_files = config.get_critical_files()
# Includes backend Python files, NLP files, and core project files
```

## Configuration Structure

### Default Services

```python
services = {
    "python_backend": {
        "path": "backend/python_backend",
        "main_file": "main.py",
        "port": 8000
    },
    "typescript_backend": {
        "path": "backend/server-ts",
        "package_json": "package.json",
        "port": 8001
    },
    "frontend": {
        "path": "client",
        "package_json": "package.json",
        "port": 3000
    }
}
```

### Required Components

- **Directories**: `backend`, `client`, `shared`, `tests`
- **Files**: `pyproject.toml`, `README.md`, `requirements.txt`

## Integration with Launch Script

The launch script (`setup/launch.py`) now uses this configuration system for:

- **Merge Conflict Checking**: Dynamically determines which files to check
- **Component Validation**: Validates required directories and files
- **Service Startup**: Only starts services that exist and are properly configured
- **Dependency Setup**: Sets up dependencies for discovered services

## Testing

Run the configuration test:

```bash
cd setup
python test_config.py
```

This will verify:
- Correct project root detection
- Service discovery
- Path validation
- Structure integrity

## Extending the Configuration

### Adding New Services

```python
# In project_config.py, add to ProjectComponents.services
"new_service": {
    "path": "path/to/service",
    "type": "service_type",
    "config": "additional_config"
}
```

### Modifying Paths

```python
# Update ProjectPaths dataclass for new directory structures
@dataclass
class ProjectPaths:
    # ... existing fields ...
    new_directory: Path = field(init=False)

    def __post_init__(self):
        # ... existing initialization ...
        self.new_directory = self.root / "new_directory"
```

### Custom Validation

```python
def validate_custom_component(self) -> List[str]:
    """Custom validation logic."""
    issues = []
    # Add custom checks
    return issues
```

## Migration from Hardcoded Paths

### Before (Problematic)

```python
# Hardcoded paths that break during refactors
critical_files = [
    "backend/python_backend/main.py",
    "backend/python_backend/database.py",
    # ... many more hardcoded paths
]

# Service startup with hardcoded paths
start_node_service(ROOT_DIR / "client", "Frontend", port, url)
start_node_service(ROOT_DIR / "backend" / "server-ts", "Backend", port, url)
```

### After (Refactor-Safe)

```python
# Dynamic discovery
config = get_project_config()
critical_files = config.get_critical_files()

# Service startup with validation
available_services = validate_services()
if available_services.get("frontend"):
    frontend_path = config.get_service_path("frontend")
    start_node_service(frontend_path, "Frontend", port, url)
```

## Error Handling

The system gracefully handles missing components:

- **Missing Services**: Warns and skips unavailable services
- **Invalid Paths**: Validates before attempting operations
- **Import Errors**: Falls back gracefully for optional components
- **Configuration Issues**: Reports problems clearly for debugging

## Future Enhancements

- **Configuration Files**: Support for YAML/JSON configuration files
- **Environment Overrides**: Environment-specific path configurations
- **Plugin System**: Extensible service discovery
- **Caching**: Cache discovered services for performance