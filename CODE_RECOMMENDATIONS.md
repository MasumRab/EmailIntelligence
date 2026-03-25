# Code Recommendations

This document contains the code recommendations extracted from the tmp.md file to fix import issues in the context_control module.

## 1. Fix the import issues

### core.py

Add the following import after line 5:

```python
from .project import ProjectConfigLoader
```

### __init__.py

Replace lines 7-8 with:

```python
from .exceptions import (
    ContextNotFoundError,
    ContextValidationError,
    EnvironmentDetectionError,
)
from .models import (
    AgentContext,
    ContextProfile,
    ContextValidationResult,
    ProjectConfig,
```

### validation.py

Add the following import at the top of the file, after line 3:

```python
import fnmatch
```

### project.py (new file)

Create the file `src/context_control/project.py` with the following content:

```python
"""Project configuration loader for Agent Context Control."""
from pathlib import Path
from typing import Optional
from .config import get_current_config
from .logging import get_context_logger
from .models import ProjectConfig
logger = get_context_logger()
class ProjectConfigLoader:
    """Loads project-specific configuration settings."""
    def __init__(self, config=None):
        """Initialize the project config loader.
        Args:
            config: Optional configuration override
        """
        self.config = config or get_current_config()
    def load_project_config(self) -> ProjectConfig:
        """Load project configuration from various sources.
        Returns:
            ProjectConfig instance with merged settings
        # For now, return a default configuration
        # In a real implementation, this would load from project files
        return ProjectConfig(
            project_name="default",
            project_type="generic",
            max_context_length=4096,
            enable_code_execution=False,
            enable_file_writing=False,
            enable_shell_commands=False,
            preferred_models=["gpt-4", "claude-3"],
        )
```

## 2. Notes

- The refactoring steps and backwards compatibility changes have been discussed and applied in the chat history.
- This document focuses on the missing code that was recommended to fix the import issues.
- For the full context of the refactoring, please refer to the chat history in tmp.md.
