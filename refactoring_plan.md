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
