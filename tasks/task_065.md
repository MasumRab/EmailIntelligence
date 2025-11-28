# Task ID: 65

**Title:** Refactor DatabaseManager for Constructor Dependency Injection

**Status:** pending

**Dependencies:** 64

**Priority:** high

**Description:** Modify the `DatabaseManager` class to accept a `DatabaseConfig` object and its internal dependencies (e.g., `EnhancedCachingManager`) directly via its constructor, completely eliminating reliance on global state and the singleton pattern.

**Details:**

Update the `DatabaseManager` class to remove any `__new__` or `__init__` logic enforcing a singleton pattern. Modify its `__init__` method signature to explicitly accept `DatabaseConfig` and any other internal dependencies (e.g., `cache_manager: EnhancedCachingManager`). Ensure all internal methods that previously accessed global variables now retrieve these values from the injected `DatabaseConfig` object.

```python
# Assume EnhancedCachingManager is a dependency
class EnhancedCachingManager:
    def __init__(self, cache_size: int = 100):
        self.cache_size = cache_size
        # ... initialization logic ...

class DatabaseManager:
    # Remove any singleton pattern implementation

    def __init__(
        self,
        config: DatabaseConfig,
        cache_manager: EnhancedCachingManager  # Injected dependency
    ):
        self._config = config
        self._cache_manager = cache_manager
        # Initialize database connections, file paths using self._config
        self.emails_filepath = self._config.emails_file
        # ... other initializations ...

    def load_emails(self):
        # Use self._config and self._cache_manager instead of globals
        with open(self.emails_filepath, 'r', encoding='utf-8') as f:
            # ... logic ...
            pass
```

**Test Strategy:**

Write unit tests for `DatabaseManager` that involve instantiating it with different `DatabaseConfig` objects and mocked `EnhancedCachingManager` instances. Verify that it correctly uses the injected dependencies for its operations. Ensure that multiple instances of `DatabaseManager` can be created and operate independently without state conflicts.

## Subtasks

### 65.1. Identify Global/Singleton Dependencies in DatabaseManager

**Status:** pending  
**Dependencies:** None  

Perform a thorough code audit of the `DatabaseManager` class to identify all dependencies that are currently accessed via global state, module-level variables, or singleton patterns. This includes `DatabaseConfig` and `EnhancedCachingManager` as explicitly mentioned, but also any other hidden dependencies.

**Details:**

Scan the `DatabaseManager` class (`src/backend/database_manager.py` or similar) for direct imports of global objects, module-level variable accesses, `__new__` method overrides, or static methods that implicitly rely on global state. Document each identified dependency and its current access method.

### 65.2. Design DatabaseManager Constructor for Dependency Injection

**Status:** pending  
**Dependencies:** 65.1  

Define the new `__init__` method signature for `DatabaseManager` to explicitly accept all identified dependencies (e.g., `DatabaseConfig`, `EnhancedCachingManager`) as parameters.

**Details:**

Based on the findings from subtask 1, draft the `__init__` signature for `DatabaseManager`. Ensure type hints are used for clarity and correctness (e.g., `config: DatabaseConfig`, `cache_manager: EnhancedCachingManager`). Initialize internal instance variables with these injected dependencies.

### 65.3. Implement Dependency Validation in DatabaseManager Constructor

**Status:** pending  
**Dependencies:** 65.2  

Add robust validation logic within the `DatabaseManager` constructor to ensure that all injected dependencies are not `None` and are of the expected types. Raise appropriate exceptions for invalid dependencies.

**Details:**

Inside the `__init__` method, add `assert` statements or `if` conditions to check for `None` values for critical dependencies. Use `isinstance()` checks to verify the type of injected objects. Raise `TypeError` or `ValueError` with clear messages if validation fails.

### 65.4. Create Factory Functions for DatabaseManager Construction

**Status:** pending  
**Dependencies:** 65.3  

Develop one or more factory functions or a builder class responsible for constructing `DatabaseManager` instances, encapsulating the creation of its dependencies.

**Details:**

Create a new module (e.g., `src/backend/database/database_manager_factory.py`) with functions like `create_default_database_manager()` or a `DatabaseManagerBuilder` class. These factories will be responsible for creating `DatabaseConfig`, `EnhancedCachingManager`, and then instantiating `DatabaseManager` with these objects.

### 65.5. Update All DatabaseManager Usage Sites

**Status:** pending  
**Dependencies:** 65.4  

Locate and modify all existing instantiations of `DatabaseManager` throughout the codebase to use the new constructor-based dependency injection or the newly created factory functions.

**Details:**

Perform a global search for `DatabaseManager(` instantiations. For each found instance, update it to pass the required `DatabaseConfig` and `EnhancedCachingManager` objects, either directly or by calling the appropriate factory function.

### 65.6. Implement Error Handling for Missing Dependencies

**Status:** pending  
**Dependencies:** 65.5  

Enhance error handling mechanisms for scenarios where dependencies are not properly provided during `DatabaseManager` instantiation, beyond basic constructor validation.

**Details:**

Review the call sites identified in subtask 5. Implement try-except blocks or assertion failures in relevant calling code to gracefully handle `TypeError` or `ValueError` exceptions that might be raised by the `DatabaseManager` constructor if dependencies are missing or invalid, providing user-friendly error messages or logging.

### 65.7. Design Backward Compatibility Shims

**Status:** pending  
**Dependencies:** 65.5  

Create backward-compatible interfaces or shims to allow gradual migration for external modules or older code that might still implicitly rely on the old `DatabaseManager` singleton behavior.

**Details:**

If direct global search cannot cover all implicit usages, consider creating a deprecated proxy class or a function that wraps the new `DatabaseManager` initialization using default dependencies, warning users of its deprecated status. This allows older code to continue functioning while providing a clear path for migration.

### 65.8. Update Test Code for DatabaseManager

**Status:** pending  
**Dependencies:** 65.5  

Modify existing unit, integration, and end-to-end tests related to `DatabaseManager` to pass dependencies via its constructor or the new factory methods.

**Details:**

Review all test files that import or instantiate `DatabaseManager`. Update test fixtures or setup methods to provide mocked or real `DatabaseConfig` and `EnhancedCachingManager` instances to the `DatabaseManager` constructor. Ensure all tests still pass with the refactored initialization.

### 65.9. Create DI Configuration for Different Environments

**Status:** pending  
**Dependencies:** 65.4  

Establish a mechanism (e.g., configuration files, a DI container setup) to define how `DatabaseManager` and its dependencies are instantiated for different environments (e.g., development, testing, production).

**Details:**

Implement a configuration strategy. This could involve using environment variables, a dedicated YAML/JSON configuration file, or integrating a simple dependency injection container (e.g., `inject`, `dependency_injector`) to manage the lifecycle and instantiation of `DatabaseManager` and its dependencies based on the current environment.

### 65.10. Implement Pre-Initialization Dependency Correctness Validation

**Status:** pending  
**Dependencies:** 65.3, 65.9  

Introduce a validation layer that checks the correctness and readiness of `DatabaseManager`'s dependencies *before* the `DatabaseManager` object is fully initialized, especially for dependencies that might connect to external services.

**Details:**

For `DatabaseConfig`, ensure all necessary paths exist or credentials are valid. For `EnhancedCachingManager`, ensure it's properly configured (e.g., cache size is positive). This validation should ideally happen in the factory or DI configuration layer before passing objects to the `DatabaseManager` constructor.

### 65.11. Design Proper Disposal/Cleanup of Dependencies

**Status:** pending  
**Dependencies:** 65.2  

Define and implement mechanisms for proper disposal or cleanup of resources held by `DatabaseManager`'s dependencies (e.g., database connections, cache connections) if they are created and managed by the `DatabaseManager`'s lifecycle.

**Details:**

If `DatabaseManager` is responsible for closing connections or releasing resources of its injected dependencies, implement `__del__` methods, `close()` methods, or context manager protocols (`__enter__`, `__exit__`) in `DatabaseManager` or its dependencies. Ensure dependencies are properly shut down to prevent resource leaks.

### 65.12. Update Documentation for New Initialization Patterns

**Status:** pending  
**Dependencies:** 65.5  

Revise all relevant documentation (e.g., API docs, READMEs, developer guides) to reflect the new constructor-based dependency injection pattern for `DatabaseManager`.

**Details:**

Update the docstrings of `DatabaseManager` and its factory functions. Add or modify sections in developer guides explaining how to instantiate and use `DatabaseManager` with its dependencies. Emphasize the removal of global state and singletons.

### 65.13. Create Migration Guide for DatabaseManager Usage

**Status:** pending  
**Dependencies:** 65.12  

Draft a detailed migration guide for developers on how to update existing code that uses `DatabaseManager` to conform to the new dependency injection pattern.

**Details:**

Create a `MIGRATION_GUIDE.md` or a section in an existing developer guide. This guide should outline the steps to identify old usage, how to obtain or create dependencies, and how to instantiate the new `DatabaseManager`. Include code examples for both old and new approaches.

### 65.14. Implement Dependency Lifecycle Management

**Status:** pending  
**Dependencies:** 65.9  

Establish a consistent strategy for managing the lifecycle of `DatabaseManager`'s dependencies (e.g., singleton-per-app, per-request, transient) within the application's overall architecture.

**Details:**

If a DI container is used (from subtask 9), configure it to manage the lifecycles of `DatabaseConfig` and `EnhancedCachingManager`. For example, `DatabaseConfig` might be a singleton, while `EnhancedCachingManager` could be a singleton or configured to be created on demand if its state is not global. Document these decisions.

### 65.15. Test Refactored DatabaseManager with Various Configurations

**Status:** pending  
**Dependencies:** 65.8, 65.10, 65.14  

Perform comprehensive testing of the refactored `DatabaseManager` using a variety of dependency configurations, including valid, invalid, and edge-case scenarios.

**Details:**

Create a dedicated test suite for `DatabaseManager` that instantiates it with different mock `DatabaseConfig` objects (e.g., valid paths, invalid paths, empty config) and `EnhancedCachingManager` instances (e.g., different cache sizes, mock objects with different behaviors). Verify `DatabaseManager`'s functionality and error handling in each scenario.
