# Task ID: 66

**Title:** Implement Factory Functions for DatabaseManager Construction

**Status:** pending

**Dependencies:** 65

**Priority:** medium

**Description:** Create factory functions to properly construct and configure `DatabaseManager` instances, abstracting the dependency injection process for consumers and allowing for different configurations.

**Details:**

Develop one or more factory functions responsible for creating `DatabaseManager` instances. These functions should handle the creation of `DatabaseConfig` (potentially from environment variables or a configuration file) and any other dependencies like `EnhancedCachingManager` before injecting them into `DatabaseManager`. This centralizes object creation and promotes a clean API for consumers.

```python
# Assume EnhancedCachingManager and DatabaseConfig are defined

def create_enhanced_caching_manager() -> EnhancedCachingManager:
    # Logic to create and configure EnhancedCachingManager
    return EnhancedCachingManager(cache_size=200) # Example configuration

def create_database_manager_from_config(config: DatabaseConfig) -> DatabaseManager:
    cache_manager = create_enhanced_caching_manager()
    return DatabaseManager(config=config, cache_manager=cache_manager)

def create_default_database_manager() -> DatabaseManager:
    default_config = DatabaseConfig.create_default_config() # From task 64
    return create_database_manager_from_config(default_config)
```

**Test Strategy:**

Test the factory functions to ensure they correctly instantiate `DatabaseManager` with all its dependencies. Verify that different factory functions produce `DatabaseManager` instances with the expected configurations. Use mocks for `EnhancedCachingManager` during testing of the factory functions.

## Subtasks

### 66.1. Design and Define Core `get_database_manager` Factory Interface

**Status:** pending  
**Dependencies:** None  

Define the primary factory function `get_database_manager`'s signature, expected parameters, and return type. This function will serve as the entry point for obtaining `DatabaseManager` instances with various configurations.

**Details:**

Create an initial `get_database_manager` function. It should accept optional parameters for overriding default configuration sources or providing explicit configuration values. Consider using keyword-only arguments for clarity.

### 66.2. Implement `DatabaseConfig` Loading from Environment Variables within Factory

**Status:** pending  
**Dependencies:** 66.1  

Enhance the factory function to load `DatabaseConfig` parameters, such as database URI, pool size, etc., directly from environment variables if specific parameters are not provided explicitly.

**Details:**

Modify `get_database_manager` or a helper function to read relevant database configuration settings (e.g., `DB_ENGINE_URI`, `DB_POOL_SIZE`) from `os.getenv()`. Prioritize explicit parameters over environment variables.

### 66.3. Implement `DatabaseConfig` Loading from Configuration Files within Factory

**Status:** pending  
**Dependencies:** 66.2  

Extend the factory function to support loading `DatabaseConfig` from external configuration files (e.g., YAML, JSON, .ini). This allows for flexible deployment and management of settings.

**Details:**

Integrate a mechanism to parse configuration files (e.g., `config.yaml`, `config.json`) for `DatabaseConfig` parameters. Define a standard path for these files and a loading order (e.g., explicit args > env vars > config file > defaults).

### 66.4. Integrate Default `DatabaseConfig` Values as Fallback

**Status:** pending  
**Dependencies:** 66.3  

Ensure the factory function provides sensible default `DatabaseConfig` values if no configuration is found from explicit parameters, environment variables, or configuration files, ensuring a functional fallback.

**Details:**

Define a set of hardcoded default values for `DatabaseConfig` (e.g., SQLite in a temp directory) that are used if all other configuration sources are absent. Document these defaults clearly.

### 66.5. Implement `EnhancedCachingManager` Dependency Injection within Factory

**Status:** pending  
**Dependencies:** 66.4  

Manage the creation and injection of the `EnhancedCachingManager` dependency into the `DatabaseManager` instance through the factory function, ensuring proper lifecycle management.

**Details:**

Modify the `get_database_manager` factory to instantiate `EnhancedCachingManager` (potentially using its own factory or constructor with config parameters) and then pass it to the `DatabaseManager` constructor. Ensure `EnhancedCachingManager` config can also be parameterized.

### 66.6. Implement Instance Caching Strategy within the Factory

**Status:** pending  
**Dependencies:** 66.5  

Introduce a caching mechanism within the factory to prevent unnecessary re-creation of `DatabaseManager` instances when the configuration remains the same, promoting resource efficiency.

**Details:**

Implement a cache (e.g., a dictionary mapping config hashes to `DatabaseManager` instances) within the factory. Before creating a new instance, check the cache. If a matching instance exists, return it. Consider thread-safety for the cache.

### 66.7. Create Environment-Specific Factory Functions (Development, Test, Production)

**Status:** pending  
**Dependencies:** 66.6  

Develop specialized factory functions (e.g., `get_dev_database_manager`, `get_test_database_manager`, `get_prod_database_manager`) that pre-configure settings for different deployment environments.

**Details:**

Create wrapper functions around the main `get_database_manager` that automatically load environment-specific configurations (e.g., 'dev_config.json', 'test_config.env'). These should leverage the existing config loading hierarchy.

### 66.8. Implement Configuration Parameter Validation in Factory

**Status:** pending  
**Dependencies:** 66.7  

Add robust validation logic within the factory functions to check the integrity and correctness of `DatabaseConfig` parameters before attempting to create a `DatabaseManager` instance.

**Details:**

Before `DatabaseManager` instantiation, implement checks for mandatory fields (e.g., `engine_uri` cannot be empty), format validation (e.g., valid URI format), and range checks (e.g., `pool_size` > 0). Raise specific exceptions for validation failures.

### 66.9. Implement Robust Error Handling for Factory Failures

**Status:** pending  
**Dependencies:** 66.8  

Design and implement comprehensive error handling within the factory functions to gracefully manage scenarios like missing configuration, invalid connection parameters, and other instantiation failures.

**Details:**

Wrap critical sections of the factory logic in `try-except` blocks. Catch specific exceptions (e.g., `FileNotFoundError` for config files, connection errors from `create_engine`, validation errors). Log errors effectively and re-raise custom, descriptive exceptions if appropriate, leveraging Task 52's centralized error handling.

### 66.10. Create Specialized Factories for Different Database Configurations

**Status:** pending  
**Dependencies:** 66.9  

Develop additional specialized factory functions to create `DatabaseManager` instances configured for specific roles, such as primary, secondary, or read-only databases, each with tailored settings.

**Details:**

Create functions like `get_primary_db_manager()`, `get_read_only_db_manager()`. These functions will call the core `get_database_manager` with predefined or role-specific `DatabaseConfig` overrides.

### 66.11. Integrate Factory Functions with Application Initialization

**Status:** pending  
**Dependencies:** 66.10  

Modify the application's main initialization routine to use the new factory functions for instantiating the primary `DatabaseManager`, replacing direct instantiation.

**Details:**

Locate the `init_managers` function or similar entry point in the application (as seen in context `async def init_managers`). Replace `_db_manager = DatabaseManager(...)` with a call to the appropriate factory function, e.g., `_db_manager = get_database_manager()`. Ensure proper `async` handling if needed.

### 66.12. Update All Existing `DatabaseManager` Instantiation Sites to Use Factories

**Status:** pending  
**Dependencies:** 66.11  

Refactor all existing code that directly instantiates `DatabaseManager` to instead use the newly created factory functions, centralizing control over database instance creation.

**Details:**

Perform a codebase search for `DatabaseManager(...)` instantiations outside of the factory implementation. Replace each instance with a call to the most appropriate factory function (e.g., `get_database_manager()` or a specialized variant).

### 66.13. Implement Cleanup and Disposal Methods via Factory

**Status:** pending  
**Dependencies:** 66.12  

Provide a mechanism through the factory functions to properly close and dispose of `DatabaseManager` instances and their underlying resources (e.g., database connections), especially for cached instances.

**Details:**

Add a `dispose_database_manager()` function to the factory interface. This function should iterate through cached instances, calling their `.close()` or `.dispose()` methods. Ensure this is called during application shutdown or when a configuration change invalidates cached instances.

### 66.14. Develop Comprehensive Unit Tests for All Factory Functions

**Status:** pending  
**Dependencies:** 66.13  

Write a dedicated suite of unit tests for all implemented factory functions, covering various configuration inputs, dependency injection, caching, validation, and error handling scenarios.

**Details:**

Create a `test_database_manager_factories.py` file. Use mocking (e.g., `unittest.mock.patch`) to isolate the factory logic from actual database connections or complex dependencies. Cover all major paths, including default usage, environment variable overrides, config file usage, caching hits/misses, and all error conditions.

### 66.15. Document Factory Function Usage Patterns and Best Practices

**Status:** pending  
**Dependencies:** 66.14  

Create detailed documentation for developers on how to use the `DatabaseManager` factory functions, including configuration options, environment-specific setups, and common usage patterns.

**Details:**

Create a new section in the developer documentation or update an existing one. Include code examples for initializing `DatabaseManager` in different scenarios, explaining the order of precedence for configuration sources, detailing parameter validation, and advising on cleanup procedures. Mention how this setup works with different deployment scenarios (containerized, local, cloud).
