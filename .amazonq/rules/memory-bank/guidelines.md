# EmailIntelligence - Development Guidelines

## Code Quality Standards

### Documentation Patterns
- **Module Docstrings**: All modules start with triple-quoted docstrings explaining purpose and functionality
- **Class Documentation**: Classes include comprehensive docstrings with purpose and usage examples
- **Method Documentation**: Methods use detailed docstrings with Args, Returns, and Raises sections
- **Inline Comments**: Strategic use of comments for complex logic and business rules

### File Organization Standards
- **Empty __init__.py Files**: Package initialization files are typically empty, following Python namespace package conventions
- **Single Responsibility**: Each module focuses on a specific domain (e.g., conflict_models.py for data structures, exceptions.py for error handling)
- **Logical Grouping**: Related functionality is grouped in dedicated directories (core/, cli/, setup/, scripts/)

### Import and Dependency Management
- **Standard Library First**: Standard library imports appear before third-party imports
- **Conditional Imports**: Optional dependencies are handled with try/except blocks and graceful fallbacks
- **Explicit Imports**: Specific imports preferred over wildcard imports for clarity

## Structural Conventions

### Data Modeling Patterns
- **Dataclasses for Data Structures**: Extensive use of `@dataclass` decorator for clean data models
- **Enums for Constants**: Enum classes for type-safe constant definitions (ConflictType, ConflictSeverity, RiskLevel)
- **Type Hints**: Comprehensive type annotations using `typing` module (List, Dict, Optional, Any)
- **Property Methods**: Use of `@property` decorators for computed attributes and data validation

### Error Handling Architecture
- **Custom Exception Hierarchy**: Well-defined exception classes inheriting from base EmailIntelligenceException
- **Specific Exception Types**: Dedicated exceptions for different error categories (ConflictDetectionError, ValidationError, GitOperationError)
- **Descriptive Error Messages**: Clear, actionable error messages with context information

### Configuration Management
- **Singleton Pattern**: Global configuration instances using module-level variables and getter functions
- **Environment Detection**: Automatic platform and environment detection with appropriate fallbacks
- **Conditional Configuration**: Different configurations based on environment (development, production, WSL)

## Practices and Patterns

### Object-Oriented Design
- **Factory Pattern**: Command factories for creating appropriate command instances
- **Strategy Pattern**: Multiple resolution strategies for different conflict types
- **Observer Pattern**: Event-driven architecture for monitoring and notifications
- **Repository Pattern**: Data access abstraction for Git operations and storage

### Functional Programming Elements
- **List Comprehensions**: Preferred over traditional loops for data transformation
- **Generator Expressions**: Used for memory-efficient data processing
- **Lambda Functions**: Strategic use for simple transformations and filtering
- **Context Managers**: Proper resource management using `with` statements

### Cross-Platform Compatibility
- **Path Handling**: Consistent use of `pathlib.Path` for cross-platform file operations
- **Platform Detection**: `platform.system()` checks for OS-specific behavior
- **Shell Script Compatibility**: POSIX-compliant shell scripts with Windows PowerShell alternatives
- **Environment Variables**: Proper handling of platform-specific environment variables

## Internal API Usage Patterns

### Git Operations
```python
# Standard git command execution pattern
result = subprocess.run(
    ["git", "merge-tree", "--name-only", base, branch_a, branch_b],
    cwd=self.repo_root,
    capture_output=True,
    text=True,
    check=True
)
```

### Process Management
```python
# Process lifecycle management
process = subprocess.Popen(cmd, cwd=ROOT_DIR)
process_manager.add_process(process)
# Automatic cleanup via atexit registration
```

### Configuration Loading
```python
# Singleton configuration pattern
def get_project_config():
    global _project_config
    if _project_config is None:
        _project_config = ProjectConfig()
    return _project_config
```

### Validation Patterns
```python
# Comprehensive validation with detailed results
def validate_context(self, context: AgentContext) -> ContextValidationResult:
    errors = []
    warnings = []
    # Validation logic...
    return ContextValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        context_id=context.profile_id,
    )
```

## Frequently Used Code Idioms

### Conditional Dependency Loading
```python
try:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
```

### Safe File Operations
```python
# Robust file reading with error handling
try:
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
except Exception as e:
    logger.warning(f"Could not read {file_path}: {e}")
```

### Command Line Argument Validation
```python
def validate_port(port: int) -> int:
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port: {port}. Port must be between 1 and 65535.")
    return port
```

### Logging Patterns
```python
# Structured logging with context
logger.info(f"🔍 Running merge-tree analysis: {branch_a} vs {branch_b}")
logger.error(f"Failed: {description}")
logger.debug(f"Returning cached context for {cache_key}")
```

## Popular Annotations and Decorators

### Type Annotations
- `Optional[str]`: For nullable string parameters
- `List[Dict[str, Any]]`: For collections of dictionaries
- `@dataclass`: For clean data structure definitions
- `@property`: For computed attributes and getters

### Method Decorators
- `@staticmethod`: For utility functions that don't need instance access
- `@classmethod`: For alternative constructors and factory methods
- `@atexit.register`: For cleanup functions that run on program exit

### Error Handling Annotations
```python
def method_name(self, param: str) -> ReturnType:
    """Method description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
        
    Raises:
        SpecificError: When specific condition occurs
        ValidationError: When validation fails
    """
```

## Performance and Resource Management

### Memory Efficiency
- **Lazy Loading**: Deferred initialization of heavy resources
- **Caching Strategies**: Strategic caching with cache invalidation
- **Generator Usage**: Memory-efficient iteration over large datasets
- **Resource Cleanup**: Proper cleanup of processes, files, and connections

### Async Patterns
- **Async/Await**: Modern asynchronous programming for I/O operations
- **Context Managers**: Proper resource management in async contexts
- **Process Pools**: Parallel execution for CPU-intensive tasks
- **Thread Safety**: Lock usage for shared resource protection

### Optimization Techniques
- **CPU-First Architecture**: Optimized for CPU-only environments
- **Conditional Dependencies**: Optional heavy dependencies to reduce installation size
- **Streaming Operations**: Processing large files without loading entirely into memory
- **Batch Processing**: Grouping operations for efficiency