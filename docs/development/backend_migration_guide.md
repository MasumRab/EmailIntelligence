# Backend Migration Guide: From `backend/` to `src/`

## 1. Introduction

This document outlines the plan and rationale for migrating the existing backend codebase from the `backend/` directory to the new modular architecture under `src/`. The `backend/` package is now deprecated and will be removed in a future release. The new `src/` architecture aims to improve modularity, maintainability, testability, and extensibility, addressing technical debt and preparing the platform for future growth.

**Overarching Task:** [task-18 - Backend Migration to src/](backlog/tasks/task-18 - Backend-Migration-to-src.md)

## 2. Rationale for Migration

The primary reasons for this migration include:

*   **Modularity:** The `backend/` package grew organically, leading to tightly coupled components and unclear separation of concerns. The `src/` architecture enforces a modular design, making it easier to understand, develop, and test individual components.
*   **Maintainability:** A modular and well-structured codebase is inherently easier to maintain, debug, and refactor.
*   **Testability:** The new architecture promotes dependency injection and clearer interfaces, significantly improving the ability to write comprehensive unit and integration tests.
*   **Extensibility:** New features, data sources, AI models, and workflow nodes can be added with minimal impact on existing code.
*   **Scalability:** The new design patterns and architectural choices are better suited for scaling the application.
*   **Technical Debt:** Addresses accumulated technical debt in the older `backend/` implementation.

## 3. High-Level Migration Roadmap

The migration will be executed in phases, focusing on core components first:

*   **Phase 1: Core Infrastructure & Data Abstraction (`src/core/`)**
    *   Migrate database management (e.g., `DatabaseManager`, `JSONDataManager`) to a unified `DataSource` abstraction.
    *   Establish core services and dependency injection mechanisms.
    *   Implement foundational security and performance monitoring.
*   **Phase 2: AI Engine & NLP Components (`modules/default_ai_engine/`, `modules/email/`)**
    *   Migrate AI analysis logic to the new `BaseAIEngine` interface.
    *   Integrate NLP components as modular services.
*   **Phase 3: Node-Based Workflow System (`src/core/advanced_workflow_engine.py`, `modules/workflows/`)**
    *   Migrate and enhance the node-based workflow engine.
    *   Ensure compatibility with existing workflow definitions (via migration utilities).
    *   Integrate node types as modular components.
*   **Phase 4: API Routes & Services (`src/main.py`, `modules/*/routes.py`)**
    *   Migrate existing FastAPI routes to the new modular structure, leveraging services and data sources.
    *   Ensure backward compatibility where necessary (e.g., via API versioning).
*   **Phase 5: Plugin System Integration (`src/core/module_manager.py`, `modules/`)**
    *   Ensure the new plugin system is fully functional and supports dynamic loading of modules.
*   **Phase 6: Deprecation & Cleanup**
    *   Remove deprecated `backend/` code after successful migration and thorough testing.

## 4. Component-Specific Migration Details

### 4.1. Database Management

*   **Old Location:** `backend/python_backend/database.py`, `backend/python_backend/json_database.py`
*   **New Location:** `src/core/database.py`, `src/core/data_source.py`, `src/core/factory.py`
*   **Key Changes:**
    *   Introduction of `DataSource` abstract base class (`src/core/data_source.py`).
    *   `DatabaseManager` (and potentially other data sources like `NotmuchDataSource`) now implement `DataSource`.
    *   A `DataSourceFactory` (`src/core/factory.py`) is used to provide the correct `DataSource` implementation via dependency injection.
    *   Elimination of global state and singleton patterns in favor of explicit dependency injection.
*   **Migration Steps:**
    1.  Ensure `DatabaseManager` in `src/core/database.py` fully implements `DataSource`.
    2.  Implement `DataSourceFactory` to select between `DatabaseManager` and other data sources.
    3.  Update all services and routes to depend on `DataSource` interface, not concrete implementations.
    4.  Remove `backend/python_backend/database.py` and `backend/python_backend/json_database.py`.

### 4.2. AI Engine & NLP Components

*   **Old Location:** `backend/python_backend/ai_engine.py`, `backend/python_nlp/nlp_engine.py`
*   **New Location:** `src/core/ai_engine.py`, `modules/default_ai_engine/` (or similar module for concrete implementation)
*   **Key Changes:**
    *   Introduction of `BaseAIEngine` abstract base class (`src/core/ai_engine.py`).
    *   Concrete AI engine implementations (e.g., `DefaultAIEngine`) will implement `BaseAIEngine`.
    *   NLP components (sentiment, topic, intent models) will be integrated within the new AI engine module.
*   **Migration Steps:**
    1.  Create a concrete `DefaultAIEngine` (or similar) in `modules/default_ai_engine/` that implements `BaseAIEngine`.
    2.  Port the core NLP logic from `backend/python_nlp/nlp_engine.py` into the new AI engine implementation.
    3.  Update services and routes to use the `BaseAIEngine` interface.
    4.  Remove `backend/python_backend/ai_engine.py` and `backend/python_nlp/nlp_engine.py`.

### 4.3. Node-Based Workflow System

*   **Old Location:** `backend/node_engine/`, `backend/python_backend/workflow_engine.py`, `backend/python_backend/workflow_manager.py`
*   **New Location:** `src/core/advanced_workflow_engine.py`, `modules/workflows/`
*   **Key Changes:**
    *   The `src/core/advanced_workflow_engine.py` provides the robust, NetworkX-based workflow engine.
    *   Node definitions (e.g., `EmailSourceNode`, `PreprocessingNode`) will be moved to `modules/workflows/nodes/` or similar.
    *   Workflow persistence and management will be handled by the new `WorkflowManager` in `src/core/advanced_workflow_engine.py`.
*   **Migration Steps:**
    1.  Port node definitions from `backend/node_engine/email_nodes.py` to the new modular structure (e.g., `modules/workflows/nodes/`).
    2.  Ensure the `WorkflowManager` in `src/core/advanced_workflow_engine.py` can load and manage these new node definitions.
    3.  Update API routes (`backend/python_backend/node_workflow_routes.py`, `backend/python_backend/advanced_workflow_routes.py`) to use the new workflow engine.
    4.  Remove `backend/node_engine/` and related workflow files from `backend/python_backend/`.

### 4.4. API Routes & Services

*   **Old Location:** `backend/python_backend/*.py` (e.g., `email_routes.py`, `category_routes.py`)
*   **New Location:** `src/main.py`, `modules/*/routes.py`, `modules/*/services.py`
*   **Key Changes:**
    *   FastAPI application (`src/main.py`) will dynamically load routes from modules.
    *   Services (e.g., `EmailService`, `CategoryService`) will encapsulate business logic and depend on `DataSource` and `BaseAIEngine` interfaces.
*   **Migration Steps:**
    1.  Create new service classes (e.g., `EmailService`, `CategoryService`) in their respective modules (e.g., `modules/email/services.py`, `modules/categories/services.py`).
    2.  Port existing route logic from `backend/python_backend/` into new modular routes (e.g., `modules/email/routes.py`).
    3.  Ensure `src/main.py` correctly discovers and mounts these new routes.
    4.  Remove old route files from `backend/python_backend/`.

## 5. Developer Guidelines

*   **New Development:** All new features and bug fixes should target the `src/` architecture.
*   **Contribution to Migration:** When working on migration tasks, prioritize moving functionality to `src/` and updating dependencies.
*   **Using New Components:** Always prefer importing from `src/` or `modules/` for core functionalities.
*   **Testing:** Ensure comprehensive test coverage for all migrated components.
*   **Deprecation Warnings:** Pay attention to deprecation warnings and update code accordingly.

## 6. Cross-references

*   **Overarching Migration Task:** [task-18 - Backend Migration to src/](backlog/tasks/task-18 - Backend-Migration-to-src.md)
*   **Related Tasks:**
    *   [task-7 - Phase 2: Import Consolidation - Update all imports to use Node Engine as primary workflow system](backlog/tasks/task-7 - Phase-2-Import-Consolidation-Update-all-imports-to-use-Node-Engine-as-primary-workflow-system.md)
    *   [task-6 - Phase 1: Feature Integration - Integrate NetworkX graph operations, security context, and performance monitoring into Node Engine](backlog/tasks/task-6 - Phase-1-Feature-Integration-Integrate-NetworkX-graph-operations-security-context-and-performance-monitoring-into-Node-Engine.md)
    *   [task-10 - Code Quality Refactoring - Split large NLP modules, reduce code duplication, and break down high-complexity functions](backlog/tasks/task-10 - Code-Quality-Refactoring-Split-large-NLP-modules-reduce-code-duplication-and-break-down-high-complexity-functions.md)
    *   [task-3 - Implement SOLID Email Data Source Abstraction](backlog/tasks/task-3 - Implement-SOLID-Email-Data-Source-Abstraction.md)
    *   [task-8 - Security & Performance Hardening - Enhance security validation, audit logging, rate limiting, and performance monitoring](backlog/tasks/task-8 - Security-and-Performance-Hardening-Enhance-security-validation-audit-logging-rate-limiting-and-performance-monitoring.md)
    *   [task-11 - Testing & Documentation Completion - Achieve 95%+ test coverage and complete comprehensive documentation](backlog/tasks/task-11 - Testing-and-Documentation-Completion-Achieve-95-test-coverage-and-complete-comprehensive-documentation.md)
*   **Relevant Documentation:**
    *   [Architecture Overview](docs/architecture/architecture_overview.md)
    *   [Advanced Workflow System](docs/architecture/advanced_workflow_system.md)
    *   [Project Structure Comparison](docs/guides/project_structure_comparison.md)
    *   [Extensions Guide](docs/development/extensions_guide.md)
