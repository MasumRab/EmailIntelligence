# Task ID: 69

**Title:** Implement DatabaseManager Unit and Integration Tests with DI

**Status:** pending

**Dependencies:** 65, 66, 68

**Priority:** high

**Description:** Develop a comprehensive suite of unit and integration tests for the refactored `DatabaseManager` to validate its correct usage of dependency injection, configuration isolation, and its ability to operate correctly in parallel test environments.

**Details:**

Write detailed unit tests for `DatabaseManager` methods, ensuring all dependencies are mocked. Create integration tests that use real or in-memory `DatabaseConfig` objects and `EnhancedCachingManager` instances, verifying the interaction between these components. Focus on test data isolation by setting up and tearing down test data for each test case or using temporary files. Validate that `DatabaseManager` instances created with different configurations indeed operate on isolated datasets.

```python
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

def test_database_manager_with_custom_config(mocker):
    with TemporaryDirectory() as tmp_dir_str:
        tmp_data_dir = Path(tmp_dir_str)
        emails_file = tmp_data_dir / 'test_emails.json'
        emails_file.write_text('[]') # Initialize empty file

        test_config = DatabaseConfig(data_dir=tmp_data_dir, emails_file=emails_file)
        mock_cache_manager = mocker.Mock(spec=EnhancedCachingManager)
        db_manager = DatabaseManager(config=test_config, cache_manager=mock_cache_manager)

        # Perform operations and assert outcomes
        db_manager.load_emails() # Should use emails_file from test_config
        mock_cache_manager.do_something.assert_called_once() # Example interaction

def test_parallel_db_operations_isolation(mocker):
    # Simulate multiple test runs or concurrent operations
    # Use distinct temporary directories for each simulated 'instance'
    # Assert that data written by one instance is not visible to another
    pass
```

**Test Strategy:**

Execute unit and integration tests using the configured `pytest` environment. Verify that all tests pass, cover critical paths, and that no tests interfere with each other when run in parallel. Aim for high test coverage (90%+) on `DatabaseManager` and its associated components.

## Subtasks

### 69.1. Unit Test DatabaseManager Constructor and Dependency Assignment

**Status:** pending  
**Dependencies:** None  

Develop unit tests to verify that the `DatabaseManager` constructor (`__init__`) correctly initializes its `engine` and `schema_manager` attributes using the provided `engine_uri` and `base_dir`. Ensure `SchemaManager` is instantiated with the correct `engine` and `base_dir`.

**Details:**

Create a pytest fixture for mocking `create_engine`, `SchemaManager`, and `Path` objects. Test that `self.engine` is set to the mocked engine and `self.schema_manager` is an instance of the mocked `SchemaManager` with expected constructor arguments.

### 69.2. Implement Comprehensive Mocking for Database Operations in Unit Tests

**Status:** pending  
**Dependencies:** 69.1  

Create detailed mocks for `sqlalchemy.create_engine`, `SQLModel.metadata.create_all`, `sqlalchemy.inspect`, `Session`, and `text` calls to isolate `DatabaseManager` unit tests from actual database interactions.

**Details:**

Use `mocker.patch` to replace external database-related functions and classes. Mocks should simulate successful and failed operations for various scenarios (e.g., `inspect.get_table_names()` returning empty or populated lists, `Session` returning query results or raising exceptions).

### 69.3. Unit Test `initialize_database` for New Database Creation

**Status:** pending  
**Dependencies:** 69.2  

Develop unit tests for the `initialize_database` method when no tables exist in the database, verifying that `SQLModel.metadata.create_all` and `schema_manager.initialize_migrations` are called correctly.

**Details:**

Mock `inspect.get_table_names()` to return an empty list. Assert that `SQLModel.metadata.create_all(self.engine)` is called once, and `self.schema_manager.initialize_migrations(force=force_init_alembic)` is called. Test various combinations of `auto_upgrade` and `force_init_alembic`.

### 69.4. Unit Test `initialize_database` for Existing Database with Schema Checks

**Status:** pending  
**Dependencies:** 69.2  

Develop unit tests for the `initialize_database` method when tables already exist, focusing on the logic for `auto_upgrade` and `_should_auto_upgrade` using mocked `SchemaManager` methods.

**Details:**

Mock `inspect.get_table_names()` to return a non-empty list. Mock `self.schema_manager.check_schema_status()` and `self.schema_manager.ensure_schema_up_to_date()` to simulate scenarios where an upgrade is needed or not needed. Test both `auto_upgrade=True` and `auto_upgrade=False` cases.

### 69.5. Unit Test `reset_db` Method for Table Dropping and Recreation

**Status:** pending  
**Dependencies:** 69.2  

Create unit tests for the `reset_db` method, ensuring that it correctly disposes the engine, drops all tables, and optionally recreates them, including handling SQLite foreign key pragmas.

**Details:**

Mock `self.engine.dispose()`, `SQLModel.metadata.drop_all()`, and `self.initialize_database()`. Simulate `sqlite` engine URLs to check `PRAGMA foreign_keys` execution. Test `recreate_tables=True` and `recreate_tables=False` scenarios. Ensure rollback is called on exceptions.

### 69.6. Unit Test CRUD Operations (`upsert`, `get`, `delete`)

**Status:** pending  
**Dependencies:** 69.2  

Develop comprehensive unit tests for `upsert`, `get`, and `delete` methods, mocking `Session` interactions to cover create, update, retrieve (with filters/ordering), and deletion scenarios, including error conditions.

**Details:**

Mock `Session` methods (`exec`, `add`, `commit`, `refresh`, `delete`, `rollback`) to simulate database behavior. Test `upsert` for both new model creation and existing model updates. Test `get` with various `filters` and `order` options. Test `delete` for existing and non-existing rows, and for `IntegrityError`.

### 69.7. Integration Test `DatabaseManager` Initialization with In-Memory SQLite

**Status:** pending  
**Dependencies:** 69.1, 69.2  

Create integration tests for `DatabaseManager`'s initialization using a real in-memory SQLite database, verifying that tables are correctly created and migrations are initialized when no existing tables are found.

**Details:**

Set up a `DatabaseManager` with `engine_uri='sqlite:///:memory:'`. Call `initialize_database()` and then use `inspector` to verify that `SQLModel.metadata` tables exist. Verify `alembic_version` table is created by `SchemaManager`.

### 69.8. Integration Test `reset_db` with In-Memory SQLite

**Status:** pending  
**Dependencies:** 69.7  

Develop integration tests for the `reset_db` method using a real in-memory SQLite database to confirm tables are dropped and optionally recreated correctly, respecting foreign key constraints.

**Details:**

First, initialize the database and populate with some data. Then call `reset_db(recreate_tables=True)` and verify that data is gone and tables are present. Call `reset_db(recreate_tables=False)` and verify tables are gone. Ensure `PRAGMA foreign_keys` commands are effective.

### 69.9. Integration Test CRUD Operations with In-Memory SQLite

**Status:** pending  
**Dependencies:** 69.7  

Create integration tests for `upsert`, `get`, and `delete` methods against a real in-memory SQLite database, ensuring data persistence, retrieval, and deletion work end-to-end.

**Details:**

Define a simple SQLModel (`Team` from context could work, or a new test model). Perform `upsert` (create and update), `get` (individual and filtered lists), and `delete` operations. Verify results by performing subsequent `get` calls or direct database inspection.

### 69.10. Test Isolation with `TemporaryDirectory` for File-Based SQLite

**Status:** pending  
**Dependencies:** 69.7, 69.8, 69.9  

Implement test data isolation mechanisms for integration tests that use file-based SQLite databases, leveraging `tempfile.TemporaryDirectory` to ensure each test operates on its own isolated database instance.

**Details:**

Modify existing integration tests to use `f'sqlite:///{tmp_data_dir}/test.db'` as the `engine_uri` within a `TemporaryDirectory` context manager. Ensure the directory and database file are cleaned up after each test.

### 69.11. Concurrency Tests for `initialize_database` and `reset_db` Locks

**Status:** pending  
**Dependencies:** 69.7  

Develop concurrency tests for `initialize_database` and `reset_db` to validate the proper functioning of the `_init_lock` in `DatabaseManager` under parallel access.

**Details:**

Use Python's `threading` module or `pytest-asyncio` and `asyncio.gather` to simulate multiple concurrent calls to `initialize_database` and `reset_db`. Assert that only one operation proceeds while others are blocked or return appropriate 'already in progress' responses.

### 69.12. Test `DatabaseManager` Error Handling for Invalid `engine_uri`

**Status:** pending  
**Dependencies:** 69.1, 69.2  

Design test cases to verify how `DatabaseManager` handles errors arising from invalid or unreachable `engine_uri` during its operations.

**Details:**

Instantiate `DatabaseManager` with a malformed `engine_uri` (e.g., `invalid://path`). Attempt to call methods like `initialize_database()` or `_should_auto_upgrade()` and assert that `DatabaseManager` catches and logs exceptions, returning `Response(status=False)`.

### 69.13. Test Dependency Lifecycle Management for `DatabaseManager`

**Status:** pending  
**Dependencies:** 69.7, 69.11  

Validate that `DatabaseManager.close()` correctly disposes the underlying SQLAlchemy engine and releases resources. For `DatabaseSession` (if used by a factory), ensure singleton behavior and proper closure.

**Details:**

After performing database operations, call `db_manager.close()` and verify that `self.engine.dispose()` is invoked. If using a factory (like `get_db()`) that relies on `DatabaseSession`, ensure `DatabaseSession.close()` also works and subsequent `get_db()` calls re-initialize if needed.

### 69.14. Establish Test Coverage Requirements and Verification for DI Functionality

**Status:** pending  
**Dependencies:** 69.1, 69.3, 69.4, 69.5, 69.6, 69.7, 69.8, 69.9, 69.10, 69.11, 69.12, 69.13  

Define minimum test coverage targets for `DatabaseManager` and its related dependency injection mechanisms, and integrate coverage reporting into the CI/CD pipeline.

**Details:**

Configure `pytest-cov` to generate coverage reports. Aim for 90%+ coverage for `DatabaseManager` and associated `SchemaManager` methods directly related to dependency handling. Review coverage reports to identify uncovered branches or lines within DI-related code paths.

### 69.15. Document Testing Patterns and Practices for DI-Enabled Database Components

**Status:** pending  
**Dependencies:** 69.1, 69.2, 69.3, 69.4, 69.5, 69.6, 69.7, 69.8, 69.9, 69.10, 69.11, 69.12, 69.13, 69.14  

Document successful testing patterns, mocking strategies, and isolation techniques used for `DatabaseManager` and other DI-enabled database components, to serve as a guideline for future development.

**Details:**

Create a new section in the project's testing documentation (e.g., `TESTING.md`) outlining how to effectively unit test classes that rely on `SQLAlchemy` engines and `SQLModel` metadata. Include examples for mocking, using in-memory databases, and managing test data isolation using `TemporaryDirectory`.
