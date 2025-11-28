# Task ID: 67

**Title:** Develop Deprecation Shims and Warning Mechanisms for Legacy API

**Status:** pending

**Dependencies:** 65, 66

**Priority:** medium

**Description:** Implement backward compatibility by creating deprecation shims for all public static methods and global variable access points related to the old `DatabaseManager` interface. Issue warnings when legacy APIs are used to guide migration.

**Details:**

For any static methods or direct global variable accesses that were part of the old `DatabaseManager` interface, create wrapper functions or properties that issue `DeprecationWarning`s. These shims should internally call the new, DI-based `DatabaseManager` instances, likely by using a globally accessible (but internally managed) `DatabaseManager` instance or a factory function. Document the migration path clearly.

```python
import warnings

# Global variable to hold a default DatabaseManager instance for shims
# This is an internal detail for backward compatibility, not a global state replacement
_legacy_db_manager = None

def _get_legacy_db_manager():
    global _legacy_db_manager
    if _legacy_db_manager is None:
        warnings.warn("Initializing default DatabaseManager via legacy API. Please migrate to dependency injection.", DeprecationWarning, stacklevel=2)
        _legacy_db_manager = create_default_database_manager() # Use factory from task 66
    return _legacy_db_manager

def legacy_load_emails():
    warnings.warn("Calling legacy_load_emails. Please use the new DatabaseManager API via dependency injection.", DeprecationWarning, stacklevel=2)
    return _get_legacy_db_manager().load_emails()

# Example of how to deprecate a global config access
def get_legacy_data_dir():
    warnings.warn("Accessing DATA_DIR via legacy global access. Please use DatabaseConfig.", DeprecationWarning, stacklevel=2)
    return _get_legacy_db_manager()._config.data_dir

```

**Test Strategy:**

Write tests that specifically invoke the deprecated APIs. Assert that `DeprecationWarning`s are correctly issued. Verify that the deprecated APIs still function as expected by internally delegating to the new DI-based `DatabaseManager`. Ensure existing functionalities are preserved.

## Subtasks

### 67.1. Identify all legacy DatabaseManager public static methods and global variables

**Status:** pending  
**Dependencies:** None  

Compile a comprehensive list of all public static methods and global variables previously associated with the old `DatabaseManager` interface that require deprecation shims and warnings.

**Details:**

Review the old `DatabaseManager` codebase, `DatabaseSession` initialization, and any direct global accesses to identify every entry point that needs to be covered by the deprecation process.

### 67.2. Define standard format for DeprecationWarning messages

**Status:** pending  
**Dependencies:** 67.1  

Establish a consistent and informative template for `DeprecationWarning` messages, ensuring they clearly state deprecation, suggest the new API, and link to migration guidance.

**Details:**

The warning message format should include the deprecated item, the reason for deprecation, the recommended new approach (DI-based `DatabaseManager`), and a placeholder for a migration guide URL.

### 67.3. Implement default DatabaseManager factory and access point for shims

**Status:** pending  
**Dependencies:** 67.2  

Create the `create_default_database_manager()` factory function (as described in task 66) and the global `_legacy_db_manager` instance, including a `DeprecationWarning` upon its first initialization.

**Details:**

This involves defining `_legacy_db_manager = None`, implementing `_get_legacy_db_manager()` to call `create_default_database_manager()` (from task 66), and issuing a `DeprecationWarning` via `warnings.warn` when `_legacy_db_manager` is first set.

### 67.4. Develop deprecation shim for a sample legacy static method (e.g., `legacy_load_emails`)

**Status:** pending  
**Dependencies:** 67.1, 67.2, 67.3  

Implement a backward compatibility shim for a specific legacy static method, ensuring it issues a `DeprecationWarning` and internally calls the new `DatabaseManager` instance.

**Details:**

Create a function `legacy_load_emails()` that calls `warnings.warn` with the defined format, then retrieves the DI-based `DatabaseManager` via `_get_legacy_db_manager()` and invokes its equivalent method (e.g., `load_emails()`).

### 67.5. Develop deprecation shim for a sample global variable access (e.g., `get_legacy_data_dir`)

**Status:** pending  
**Dependencies:** 67.1, 67.2, 67.3  

Implement a backward compatibility shim for accessing a global variable, issuing a `DeprecationWarning` and retrieving the value from the new `DatabaseManager` configuration.

**Details:**

Create a function `get_legacy_data_dir()` that calls `warnings.warn` with the defined format, then retrieves the DI-based `DatabaseManager` via `_get_legacy_db_manager()` and accesses its configuration (e.g., `_config.data_dir`).

### 67.6. Implement deprecation shims for all identified legacy static methods

**Status:** pending  
**Dependencies:** 67.1, 67.4  

Systematically create deprecation shims for all remaining public static methods identified in subtask 1, following the pattern established in subtask 4.

**Details:**

For each legacy static method, create a wrapper function that issues a `DeprecationWarning` using the standard format and delegates the call to the corresponding method on the `_get_legacy_db_manager()` instance.

### 67.7. Implement deprecation shims for all identified legacy global variable accesses

**Status:** pending  
**Dependencies:** 67.1, 67.5  

Systematically create deprecation shims for all remaining global variable access points identified in subtask 1, following the pattern established in subtask 5.

**Details:**

For each legacy global variable access, create a property or function that issues a `DeprecationWarning` using the standard format and retrieves the value from the `_get_legacy_db_manager()` instance's configuration or properties.

### 67.8. Create configuration option to enable/disable deprecation warnings

**Status:** pending  
**Dependencies:** 67.2  

Design and implement a mechanism (e.g., environment variable or configuration setting) to allow users to suppress or enable `DeprecationWarning`s during the migration period.

**Details:**

Implement a check within the warning issuance logic (e.g., in `warnings.warn` calls or a custom wrapper) that respects a configured setting (e.g., `LEGACY_DB_WARNINGS_ENABLED=false`).

### 67.9. Create test coverage for all deprecated API shims

**Status:** pending  
**Dependencies:** 67.6, 67.7  

Develop comprehensive unit tests for every deprecation shim to ensure they correctly issue warnings, maintain backward compatibility, and gracefully delegate to the new DI-based API.

**Details:**

Tests should cover: warning issuance (`DeprecationWarning`), correct functionality (return values, side effects), proper internal delegation to the new `DatabaseManager` instance, and handling of edge cases for each shimmed method/access.

### 67.10. Draft comprehensive migration guide for legacy API users

**Status:** pending  
**Dependencies:** 67.1, 67.6, 67.7  

Develop a detailed migration guide for users, explaining how to transition from the deprecated `DatabaseManager` APIs to the new dependency injection pattern, including code examples.

**Details:**

The guide should cover each deprecated method/global access, showing the old usage and the new, recommended DI-based approach. Include setup instructions for the new `DatabaseManager` and common migration scenarios.

### 67.11. Update API documentation to mark deprecated methods

**Status:** pending  
**Dependencies:** 67.10  

Modify the official API documentation to clearly mark all legacy `DatabaseManager` methods and global accesses as deprecated, providing links to the new API and the migration guide.

**Details:**

Add `@deprecated` decorators or equivalent documentation tags to the relevant code. Update docstrings and auto-generated documentation with explicit deprecation notices, recommended alternatives, and a link to the migration guide.

### 67.12. Design metrics tracking for deprecated API usage

**Status:** pending  
**Dependencies:** 67.6, 67.7  

Outline a strategy for tracking the usage of deprecated APIs, collecting data on frequency and call sites to inform future removal decisions.

**Details:**

Consider integrating logging of `DeprecationWarning` events with additional context (e.g., calling module, stack trace). Define how this data will be aggregated and analyzed to gauge the remaining usage of legacy APIs.

### 67.13. Establish deprecation timeline and communication plan

**Status:** pending  
**Dependencies:** 67.10, 67.11  

Define a clear timeline with milestones for the deprecation period, leading up to the eventual removal of the legacy `DatabaseManager` API, and plan communication to users.

**Details:**

The timeline should include stages like 'deprecated (with warnings)', 'warnings become errors', and 'removal'. Develop a communication plan for announcing deprecation to the community, including release notes and official announcements.

### 67.14. Draft removal plan and migration checklist for deprecated APIs

**Status:** pending  
**Dependencies:** 67.1, 67.13  

Create a detailed internal document outlining the steps and checklist for the eventual removal of each deprecated `DatabaseManager` API, ensuring a smooth transition.

**Details:**

For each deprecated item, specify the exact version in which it will be removed, the necessary code changes (e.g., deleting shims, removing old factory methods), and checks to confirm no remaining usage within the codebase. Include criteria for removal readiness based on metrics.

### 67.15. Implement graceful degradation for remaining legacy uses during transition (monitoring)

**Status:** pending  
**Dependencies:** 67.6, 67.7, 67.9  

Ensure that the deprecation shims are robust and handle potential failures or unexpected states gracefully, minimizing impact on legacy users during the migration period.

**Details:**

This involves adding robust error handling within the shims to catch exceptions from the underlying new `DatabaseManager` methods and re-raising them appropriately, or logging them without crashing the application. The goal is to maintain functionality, even if deprecated usage is not ideal.
