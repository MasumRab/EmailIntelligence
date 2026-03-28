# Python Style Guide for EmailIntelligence

This style guide outlines the coding standards for Python code in the EmailIntelligence project. Following these guidelines will improve code readability, maintainability, and consistency across the codebase.

## General Principles

- **Readability**: Code should be easy to read and understand.
- **Simplicity**: Prefer simple solutions over complex ones.
- **Consistency**: Follow the same patterns throughout the codebase.
- **Documentation**: Document code appropriately with docstrings and comments.

## Code Formatting

### Line Length
- Maximum line length is 100 characters.
- Use line breaks for long lines, expressions, and function calls.

### Indentation
- Use 4 spaces for indentation (no tabs).
- Align continued lines with the opening delimiter or indent by 4 spaces.

### Imports
- Group imports in the following order, separated by a blank line:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Sort imports alphabetically within each group.
- Use absolute imports rather than relative imports.

Example:
```python
# Standard library
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Third-party libraries
import numpy as np
import pandas as pd
from fastapi import FastAPI

# Local modules
from src.backend.python_nlp.utils import format_text
```

### Whitespace
- Use blank lines to separate logical sections of code.
- Use a single blank line between functions and classes.
- Use two blank lines before top-level classes and functions.
- No trailing whitespace at the end of lines.
- Use spaces around operators and after commas.

### Comments and Docstrings
- Use docstrings for all public modules, functions, classes, and methods.
- Use triple double quotes (`"""`) for docstrings.
- Keep comments up-to-date when code changes.
- Comments should explain "why" not "what".
- Use inline comments sparingly.

Function docstring format:
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When and why this exception is raised
    """
```

## Naming Conventions

- **Modules**: Short, lowercase names. Underscores can be used if it improves readability.
- **Classes**: CapWords convention (e.g., `EmailFilter`, `NLPEngine`).
- **Functions and Methods**: lowercase with words separated by underscores (e.g., `analyze_email`).
- **Variables**: lowercase with words separated by underscores (e.g., `email_content`).
- **Constants**: All uppercase with words separated by underscores (e.g., `MAX_RETRY_COUNT`).
- **Private Methods/Variables**: Prefix with a single underscore (e.g., `_private_method`).

## Programming Practices

### Type Hints
- Use type hints for function parameters and return values.
- Use the `typing` module for complex types.

### Error Handling
- Use specific exception types rather than catching all exceptions.
- Provide meaningful error messages.
- Log exceptions with appropriate context.

### Function Design
- Functions should do one thing well.
- Keep functions short and focused.
- Limit the number of parameters.
- Use default parameter values when appropriate.

### Classes
- Follow the single responsibility principle.
- Use properties instead of getter/setter methods when appropriate.
- Implement `__str__` and `__repr__` methods for better debugging.

### Testing
- Write unit tests for all new code.
- Test edge cases and error conditions.
- Keep tests independent of each other.

## Tools

The project uses the following tools to enforce style:
- **Black**: For code formatting
- **Flake8**: For style guide enforcement
- **isort**: For import sorting
- **Pylint**: For code quality checks

## References

- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)