# Task ID: 35

**Title:** Refactor ContextController Config Initialization for Thread Safety

**Status:** pending

**Dependencies:** 30

**Priority:** medium

**Description:** Refactor the ContextController's configuration initialization to eliminate global state mutation, implement a factory pattern, ensure thread safety, and document the new initialization process.

**Details:**

The current `ContextController` implementation, likely in `src/backend/context_control/context_control.py`, suffers from fragility due to direct modification of a module-level global variable, `_global_config`, within its constructor or initialization logic. This introduces thread-safety issues and hidden side effects across different parts of the application. The goal is to refactor this critical component to be robust and predictable.

**Implementation Steps:**

1.  **Remove Global State Mutation:** Identify and eliminate all direct modifications to `_global_config` or any other module-level global configuration state within `src/backend/context_control/context_control.py`. The configuration should not be implicitly changed by an object's instantiation.
2.  **Implement Config Factory Pattern:** Create a dedicated factory mechanism for loading and providing `ContextController` configurations. This could be a static method within `ContextController` (e.g., `ContextController.from_config_source()`) or a separate `ContextConfigFactory` class. This factory will be responsible for encapsulating the logic of reading config files, environment variables, or other sources.
3.  **Explicit Config Passing:** Modify `ContextController`'s constructor (`__init__`) to accept its configuration explicitly as an argument, rather than relying on global state. This makes dependencies clear and the class more testable.
4.  **Ensure Thread-Safe Config Singleton (if applicable):** If the loaded configuration itself needs to be a singleton across the application, ensure its instantiation and retrieval via the factory is thread-safe. This might involve using `threading.Lock` or `functools.lru_cache` with a lock if the config loading is expensive and should only happen once. The primary goal is thread-safe *config initialization*, so the singleton pattern should be applied to the config loading process, not necessarily the `ContextController` instance itself.
5.  **Document Initialization Order:** Update the relevant documentation (e.g., `docs/dev_guides/context_control_module.md` if it exists, or a new section in `src/backend/context_control/README.md`) to clearly describe the new configuration initialization flow, the role of the factory, and how `ContextController` instances receive their configuration.
6.  **Update Call Sites:** Identify and update all parts of the codebase that instantiate or rely on `ContextController` to use the new factory pattern and explicit config passing.

### Tags:
- `work_type:refactoring`
- `work_type:architectural-improvement`
- `component:context-control`
- `component:configuration`
- `scope:thread-safety`
- `scope:backend-core`
- `purpose:stability`
- `purpose:predictability`
- `purpose:testability`

**Test Strategy:**

Develop a comprehensive test suite to validate the refactored configuration initialization, focusing on thread safety and correctness under various conditions.

1.  **Unit Tests for Factory:**
    *   Verify the config factory correctly loads configurations from various sources (e.g., mock config files, environment variables).
    *   Test different valid and invalid configuration scenarios.
    *   Ensure the factory returns immutable config objects or copies to prevent external modification if designed as such.
2.  **Unit Tests for ContextController Constructor:**
    *   Ensure `ContextController` instances correctly use the explicitly passed configuration.
    *   Verify that passing different configurations results in `ContextController` instances behaving as expected.
3.  **Thread-Safety Tests:**
    *   Write tests using Python's `threading` module to simulate multiple threads concurrently attempting to initialize or retrieve configurations via the new factory.
    *   Verify that no race conditions occur, `_global_config` (if still present in a modified role, which should be avoided) is not mutated unexpectedly, and each thread receives a consistent and correct configuration.
    *   Specifically, test scenarios where the config loading might be expensive or involve shared resources, ensuring the singleton pattern for config is effective.
4.  **Integration Tests:**
    *   Perform integration tests to ensure that existing functionalities that rely on `ContextController` still work correctly with the new initialization pattern.
    *   Use `pytest-mock` or similar libraries to isolate tests where necessary, but also ensure end-to-end flow is validated.

## Subtasks

### 35.1. Analyze and Eliminate Global _global_config Mutation

**Status:** pending  
**Dependencies:** None  

Thoroughly analyze `src/backend/context_control/context_control.py` to identify and eliminate all direct modifications to `_global_config` or any other module-level global configuration state within the `ContextController`'s constructor or initialization logic. This is crucial for resolving thread-safety issues and hidden side effects.

**Details:**

Conduct a static analysis and code review of `src/backend/context_control/context_control.py`. Pinpoint any lines of code that directly assign values to `_global_config` or other global variables intended to hold configuration data. Refactor these assignments to ensure the configuration is not implicitly changed by object instantiation. Document the identified global state mutations and their removal.

### 35.2. Implement Config Factory Pattern for ContextController

**Status:** pending  
**Dependencies:** 35.1  

Create a dedicated factory mechanism for loading and providing `ContextController` configurations. This factory will encapsulate the logic of reading config files, environment variables, or other sources, ensuring a centralized and reusable configuration retrieval process.

**Details:**

Design and implement a factory (e.g., a static method within `ContextController` like `ContextController.from_config_source()`, or a new `ContextConfigFactory` class) responsible for loading configuration. This factory should handle reading configuration from various sources (e.g., `config/*.json` files, environment variables). The factory's responsibility is to produce a valid configuration object (e.g., a Pydantic model) that can be passed to `ContextController`.

### 35.3. Modify ContextController for Explicit Config Passing

**Status:** pending  
**Dependencies:** None  

Refactor the `ContextController`'s constructor (`__init__`) to explicitly accept its configuration as an argument, making its dependencies clear and enhancing testability. Update any internal methods that previously relied on global state to use this passed configuration.

**Details:**

Change the signature of `ContextController.__init__` to accept a configuration object (e.g., `config: ContextConfig`). Update all internal usages within the `ContextController` class that previously accessed `_global_config` to instead use attributes of the `self.config` object. This ensures that each `ContextController` instance operates with its own explicitly provided configuration.

### 35.4. Ensure Thread-Safe Config Singleton (if applicable)

**Status:** pending  
**Dependencies:** None  

If the loaded configuration itself needs to be a singleton across the application (e.g., to prevent redundant expensive loading), ensure its instantiation and retrieval via the factory is thread-safe.

**Details:**

If the `ContextConfigFactory` (or equivalent) might be called multiple times and the configuration loading is expensive or involves shared resources, implement thread-safe mechanisms (e.g., `threading.Lock`, `functools.lru_cache` with a lock) within the factory to ensure the configuration object is loaded only once and its retrieval is safe from race conditions. This applies to the config *object* itself, not the `ContextController` instances.

### 35.5. Document New Configuration Initialization Process

**Status:** pending  
**Dependencies:** 35.3  

Update relevant documentation (e.g., `docs/dev_guides/context_control_module.md` or a new section in `src/backend/context_control/README.md`) to clearly describe the new configuration initialization flow, the role of the factory, and how `ContextController` instances receive their configuration.

**Details:**

Create or update documentation to explain the architectural changes to `ContextController`'s configuration. Detail how to use the new factory to obtain configuration objects and how to instantiate `ContextController` by explicitly passing the configuration. Provide code examples and explain the benefits (testability, predictability, thread safety).

### 35.6. Update All Call Sites to Use New Factory and Explicit Config Passing

**Status:** pending  
**Dependencies:** 35.3  

Identify and refactor all parts of the codebase that instantiate or rely on `ContextController` to use the new factory pattern for obtaining configurations and explicitly passing them to `ContextController` instances.

**Details:**

Perform a global search across the codebase for `ContextController` instantiations or usages that might implicitly rely on global configuration. Modify these call sites to first use the new config factory (e.g., `config = ContextController.from_config_source(...)`) and then pass this `config` object explicitly to the `ContextController` constructor (e.g., `controller = ContextController(config=config)`).
