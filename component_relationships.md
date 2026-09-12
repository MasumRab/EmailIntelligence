# Component Relationships

## Core System Components

### 1. Main Application (`src/main.py`)
- **Depends on**: FastAPI, Gradio, ModuleManager
- **Responsibilities**:
  - Creates and configures the main FastAPI application
  - Integrates Gradio UI with FastAPI
  - Initializes and loads modules
  - Sets up middleware and exception handlers

### 2. Module Manager (`src/core/module_manager.py`)
- **Depends on**: Python importlib, logging
- **Depends on (modules)**: All modules in `modules/` directory
- **Responsibilities**:
  - Discovers and loads modules dynamically
  - Registers module components with main application
  - Manages module lifecycle

### 3. Factory System (`src/core/factory.py`)
- **Depends on**: DataSource implementations, EmailRepository implementations
- **Used by**: API routes, services
- **Responsibilities**:
  - Provides singleton instances of core services
  - Manages dependency injection
  - Initializes services on first access

## Data Layer Components

### 4. Repository Pattern (`src/core/data/repository.py`)
- **EmailRepository**: Abstract interface for email data operations
- **DatabaseEmailRepository**: Implementation that delegates to DataSource
- **Relationships**:
  - Depends on DataSource interface
  - Used by API routes and services

### 5. Data Sources (`src/core/data_source.py`, `src/core/database.py`, `src/core/notmuch_data_source.py`)
- **DataSource**: Abstract interface for data operations
- **DatabaseManager**: JSON file storage implementation with caching
- **NotmuchDataSource**: Integration with Notmuch email indexing system
- **Relationships**:
  - Implements DataSource interface
  - Used by DatabaseEmailRepository

## Business Logic Components

### 6. AI Engine (`src/core/ai_engine.py`)
- **BaseAIEngine**: Abstract interface for AI analysis
- **ModernAIEngine**: Implementation using transformer models
- **AIAnalysisResult**: Standardized result structure
- **Relationships**:
  - Used by services that require email analysis
  - Independent of data layer

### 7. Workflow Engine (`src/core/workflow_engine.py`)
- **Responsibilities**: Node-based workflow processing
- **Relationships**:
  - Integrates with AI engine for analysis
  - Uses data layer for persistence
  - Exposed through API routes

## Module Components

### 8. Email Module (`modules/email/`)
- **Depends on**: FastAPI, core components (factory, models)
- **Provides**: Email API routes
- **Relationships**:
  - Registered with ModuleManager
  - Uses factory for dependency injection
  - Integrates with data layer through repository pattern

### 9. Authentication Module (`modules/auth/`)
- **Depends on**: FastAPI, core security components
- **Provides**: Authentication API routes
- **Relationships**:
  - Registered with ModuleManager
  - Used by other modules for authentication

### 10. Dashboard Module (`modules/dashboard/`)
- **Depends on**: FastAPI, core components
- **Provides**: Dashboard API routes and UI components
- **Relationships**:
  - Registered with ModuleManager
  - Integrates with data layer for statistics

## External Integrations

### 11. Gmail Integration (`backend/python_nlp/gmail_service.py`)
- **Depends on**: Google API client libraries
- **Used by**: Services that require Gmail access
- **Relationships**:
  - Integrates with data layer for email storage
  - Uses AI engine for analysis

### 12. Notmuch Integration (`src/core/notmuch_data_source.py`)
- **Depends on**: Notmuch Python bindings
- **Implements**: DataSource interface
- **Relationships**:
  - Alternative to DatabaseManager
  - Used through repository pattern

## Frontend Components

### 13. React Frontend (`client/`)
- **Depends on**: TypeScript, React, Vite
- **Communicates with**: FastAPI backend via HTTP
- **Relationships**:
  - Consumes API endpoints
  - Displays data from backend
  - Provides user interface

### 14. Gradio UI (`src/main.py`)
- **Integrated with**: FastAPI application
- **Provides**: Scientific exploration interface
- **Relationships**:
  - Embedded within FastAPI app
  - Can access same backend services

## Launcher System

### 15. Unified Launcher (`launch.py`)
- **Depends on**: Python standard library, subprocess management
- **Controls**: Entire application lifecycle
- **Relationships**:
  - Manages all services (backend, frontend, Gradio)
  - Handles environment setup and dependency management
  - Orchestrates testing and deployment

## Component Interaction Diagram

```
+------------------+     +------------------+     +------------------+
|   React Frontend |     |    Gradio UI     |     |  TypeScript Backend|
|   (client/)      |     |   (embedded)     |     |  (backend/server-ts)|
+------------------+     +------------------+     +------------------+
         |                        |                         |
         | HTTP Requests          | HTTP Requests           | HTTP Requests
         v                        v                         v
+---------------------------------------------------------------+
|                    FastAPI Application (src/main.py)          |
|                    + ModuleManager                            |
|                    + Gradio Integration                       |
+---------------------------------------------------------------+
         |                        |                         |
         | API Routes             | Module Components       | Dependencies
         v                        v                         v
+------------------+     +------------------+     +------------------+
|   Module Routes  |     |  Module UI       |     |   Core Services  |
| (modules/*/)     |     |  Components      |     | (src/core/*)     |
+------------------+     +------------------+     +------------------+
         |                        |                         |
         | Repository Pattern     | UI Integration          | Factory Pattern
         v                        v                         v
+------------------+     +------------------+     +------------------+
|  EmailRepository |     | Gradio Components|     | Service Factory  |
| (src/core/data/) |     |                  |     | (src/core/factory.py)|
+------------------+     +------------------+     +------------------+
         |                        |                         |
         | Data Operations        | Scientific UI           | Dependency Injection
         v                        v                         v
+------------------+     +------------------+     +------------------+
|   Data Sources   |     |   AI Analysis    |     |  External APIs   |
| (DataSource impl)|     |  (AI Engine)     |     | (Gmail, Notmuch) |
+------------------+     +------------------+     +------------------+
```

## Key Dependencies

1. **API Routes → Repository Pattern**: All API endpoints use repository for data access
2. **Repository → Data Sources**: Repository delegates to concrete data source implementations
3. **Modules → Core Services**: Modules depend on core services through factory pattern
4. **Frontend → API**: Frontend communicates with backend exclusively through API
5. **Launcher → All Services**: Launcher orchestrates all application components

## Data Flow Patterns

1. **Read Operation**:
   Frontend → API Route → Repository → Data Source → Database

2. **Write Operation**:
   Frontend → API Route → Repository → Data Source → Database

3. **AI Analysis**:
   Email Data → AI Engine → Analysis Result → Storage

4. **Module Registration**:
   Launcher → Module Manager → Module → Main Application

This architecture ensures loose coupling between components while maintaining clear responsibility boundaries.