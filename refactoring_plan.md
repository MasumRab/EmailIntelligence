# Detailed Refactoring Plan

This plan outlines the concrete steps to transition the `src/core/` module towards a more functional, modular, and testable architecture, in line with the proposed design.

**Phase 1: Establish the New Architecture Foundation**

1.  **Step 1: Create Core Data Models (DTOs)**
    *   **Action:** Create a new file: `src/core/models.py`.
    *   **Details:** Define the immutable `Email` and `Category` `dataclasses` as specified in the architectural design. These will serve as the standardized data transfer objects throughout the application.

2.  **Step 2: Define the Abstract Data Source Interface**
    *   **Action:** Create a new directory `src/core/datasources/` and a file inside it: `src/core/datasources/interface.py`.
    *   **Details:** Define the `IEmailDataSource` Abstract Base Class (ABC). This interface will include all the abstract methods required for data manipulation (`get_email_by_id`, `get_emails`, `update_email`, `get_all_categories`, etc.), establishing a clear contract for all future data connectors.

**Phase 2: Migrate Existing Logic to the New Architecture**

3.  **Step 3: Implement the JSON File Data Source Connector**
    *   **Action:** Create a new file: `src/core/datasources/json_file_connector.py`.
    *   **Details:**
        *   Create a `JsonFileDataSource` class that inherits from and implements the `IEmailDataSource` interface.
        *   Migrate the data loading, saving, and querying logic from the existing `src/core/database.py` into this new class.
        *   Adapt the implementation to return the new immutable `Email` and `Category` dataclasses instead of dictionaries. All functions that previously modified data in-place must be rewritten to return new instances with the updated data.

4.  **Step 4: Deprecate the Old `DatabaseManager`**
    *   **Action:** Once the `JsonFileDataSource` is complete and tested, the old `src/core/database.py` file should be marked for deletion.

**Phase 3: Eliminate Global Singletons with Dependency Injection**

5.  **Step 5: Implement the Central `DataSourceManager`**
    *   **Action:** Create a new file: `src/core/dependencies.py`.
    *   **Details:**
        *   Implement the `DataSourceManager` class responsible for registering and managing all available data source connectors.
        *   Create a single, application-level instance of this manager at startup.

6.  **Step 6: Set Up Dependency Injection**
    *   **Action:** In the main application entry point (likely where the FastAPI app is created), create provider functions that make the `DataSourceManager` and the *active* `IEmailDataSource` available to the rest of the application.
    *   **Details:** This will replace all calls to the old global `get_db()`, `get_active_ai_engine()`, and `get_workflow_manager()` functions.

**Phase 4: Refactor Application Logic**

7.  **Step 7: Update Code to Use the New Interface**
    *   **Action:** Systematically search the codebase for all usages of the old global accessors (`get_db()`, etc.).
    *   **Details:** Refactor these parts of the application (e.g., API endpoints, workflow nodes) to declare their dependency on `IEmailDataSource`. They will receive the active connector automatically from the dependency injection system. Update the logic to use the methods and DTOs defined by the new interface.

**Phase 5: Code Consolidation and Deduplication**

8.  **Step 8: Consolidate Core Logic**
    *   **Problem:** Core application logic is duplicated across `src/core` and `backend/python_backend`. This includes `workflow_engine.py`, `ai_engine.py`, `database.py`, `models.py`, and `performance_monitor.py`. This is a major architectural flaw that increases maintenance overhead and the risk of bugs.
    *   **Action:** Merge the implementations from `backend/python_backend` into their `src/core` counterparts. The `src/core` directory should be the single source of truth. Once merged, remove the redundant files from `backend/python_backend`.

9.  **Step 9: Unify NLP Components**
    *   **Problem:** The NLP pipeline is implemented in two places: `backend/python_nlp` and `modules/default_ai_engine`. This suggests a refactoring was started but not completed.
    *   **Action:** Identify the most current implementation (likely in `modules/default_ai_engine`). Migrate any necessary features from the other implementation, and then remove the redundant `backend/python_nlp` directory. Update all imports to point to the unified module.

10. **Step 10: Centralize Constants and Exceptions**
    *   **Problem:** `constants.py` and `exceptions.py` are duplicated. This is a common source of subtle bugs when a value is updated in one place but not the other.
    *   **Action:** Consolidate each of these into a single file within `src/core/`. Update all imports throughout the application to reference these central files.

11. **Step 11: Refactor Versioned API Routes**
    *   **Problem:** API v1 routes (e.g., `routes/v1/category_routes.py`) are copy-pasted versions of the original routes, leading to code duplication.
    *   **Action:** Refactor the v1 routes to be thin wrappers. The core business logic should reside in the main route files, and the versioned routes should call that logic.

12. **Step 12: Clean Up Application Entry Points**
    *   **Problem:** The presence of `backend/python_backend/main.py` and `src/main.py`, as well as multiple launcher scripts, creates confusion about how to start the application.
    *   **Action:** Consolidate launch functionality into `launch.py`. Remove redundant launcher scripts.

13. **Step 13: Consolidate Test Fixtures**
    *   **Problem:** Test fixtures are duplicated in `backend/python_backend/tests/conftest.py` and `tests/conftest.py`.
    *   **Action:** Move all common test fixtures to the root `tests/conftest.py` file to make them globally available to all tests and remove duplication.
