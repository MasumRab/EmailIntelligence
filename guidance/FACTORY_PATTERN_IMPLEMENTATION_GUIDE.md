# Factory Pattern Implementation Guide for Branches

## Overview
This guide explains how to implement the factory pattern in branches that may need it but don't have access to the complete implementation. The factory pattern is essential for service startup compatibility between different architectural approaches.

## What is the Factory Pattern?

The factory pattern provides a way to create application instances that are compatible with different architectural expectations. Specifically, it allows the remote branch's service startup pattern to work with local functionality.

### Remote Branch Expectation
```bash
uvicorn src.main:create_app --factory
```

### Local Branch Compatibility
The factory pattern bridges both approaches, allowing:
- Remote branch service startup patterns to work
- Local branch functionality to be preserved
- Context control patterns to be integrated

## Implementation Steps

### 1. Create the Factory Function
Create a `create_app()` function in `src/main.py`:

```python
from fastapi import FastAPI

def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    
    This function is compatible with the remote branch's service startup
    configuration that expects src.main:create_app with --factory option.
    It integrates context control patterns from the remote branch while
    preserving all functionality from the local branch.
    """
    app = FastAPI()
    
    # Add your routes and middleware here
    # Configure the application as needed
    
    return app
```

### 2. Ensure Service Startup Compatibility
Make sure your service startup configuration can work with both patterns:

```python
# For factory-based startup (remote branch expectation)
# Command: uvicorn src.main:create_app --factory

# For direct startup (local branch pattern)
# Command: uvicorn src.main:app
```

### 3. Preserve Local Functionality
Integrate your existing application with the factory pattern:

```python
from fastapi import FastAPI
from src.backend.python_backend.main import app as local_backend_app

def create_app() -> FastAPI:
    """Factory function that preserves local functionality."""
    # Use the actual backend app from local implementation
    app = local_backend_app
    
    # Add any additional configuration needed for remote compatibility
    # Add middleware, routes, etc.
    
    return app
```

## Command Structure for Different Branches

### For Branches WITHOUT Factory Pattern
If a branch needs to implement the factory pattern:

1. **Create the factory function** in `src/main.py`
2. **Integrate existing functionality** with the factory pattern
3. **Test service startup** with both approaches
4. **Validate functionality** is preserved

### For Branches WITH Factory Pattern
If a branch already has the factory pattern:

1. **Verify compatibility** with both architectural approaches
2. **Test service startup** patterns work correctly
3. **Ensure functionality** is preserved from both branches
4. **Validate context control** integration

## Example Implementation

Here's a complete example of how to implement the factory pattern in a branch that doesn't have it:

```python
"""
Factory module for creating the FastAPI application.

This module provides a create_app factory function that is compatible with
remote branch expectations while preserving local branch functionality.
"""

from fastapi import FastAPI
import logging
from typing import Optional
import os


def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(title="Email Intelligence API", version="1.0.0")
    
    # Add your existing routes and functionality here
    # For example:
    # from src.api.v1.router import router as api_router
    # app.include_router(api_router, prefix="/api/v1")
    
    # Add CORS middleware
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "factory": True}
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    return app


# For backward compatibility when called directly
if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        log_level="info"
    )
```

## Validation Steps

After implementing the factory pattern in a branch:

1. **Test service startup**:
   ```bash
   # Remote branch pattern
   uvicorn src.main:create_app --factory
   
   # Local branch pattern (if still needed)
   uvicorn src.main:app
   ```

2. **Verify functionality**:
   - All routes work correctly
   - All middleware functions properly
   - All dependencies are resolved
   - Context control (if applicable) works

3. **Check for import issues**:
   - No import-time initialization problems
   - All dependencies properly handled
   - Lazy initialization where appropriate

## Troubleshooting

### Common Issues

1. **Import-time initialization**: Move heavy initialization to runtime
2. **Missing dependencies**: Ensure all required modules are available
3. **Service startup failures**: Verify factory function returns proper app instance
4. **Context control conflicts**: Integrate context control patterns properly

### Solutions

1. **Use lazy initialization** for heavy components
2. **Verify import paths** are consistent
3. **Test incrementally** to isolate issues
4. **Create adapter layers** for different architectural approaches

## Best Practices

1. **Preserve functionality** from both architectural approaches
2. **Use adapter patterns** to bridge different components
3. **Test service startup** with both patterns before merging
4. **Document the factory implementation** for future reference
5. **Validate all functionality** is preserved after implementation

## Rollback Considerations

If the factory pattern implementation causes issues:

1. **Keep original implementation** in a backup
2. **Use conditional imports** to maintain compatibility
3. **Implement gradual migration** rather than wholesale changes
4. **Test thoroughly** before committing changes

## Conclusion

The factory pattern is a crucial component for merging branches with different architectural approaches. It allows service startup compatibility while preserving functionality from both branches. When implementing in branches that don't have it, follow the steps outlined above to ensure proper integration and compatibility.