# Key Modules

## Core System Modules

### 1. Main Application (`src/main.py`)
**Purpose**: Entry point and central coordinator for the entire application.

**Key Responsibilities**:
- Initialize FastAPI application with middleware and exception handlers
- Integrate Gradio UI with FastAPI server
- Manage module loading through ModuleManager
- Configure security headers and CORS policy
- Handle application lifecycle

**Dependencies**:
- FastAPI
- Gradio
- ModuleManager
- Core security components

**Design Patterns**:
- Factory pattern for application creation
- Middleware pattern for security headers
- Exception handling patterns

### 2. Module Manager (`src/core/module_manager.py`)
**Purpose**: Dynamic module discovery and registration system.

**Key Responsibilities**:
- Discover modules in the `modules/` directory
- Load module code dynamically
- Register module components with the main application
- Handle module loading errors gracefully

**Dependencies**:
- Python importlib
- Logging system
- Module registration interface

**Design Patterns**:
- Plugin architecture
- Dynamic code loading
- Convention over configuration

### 3. Factory System (`src/core/factory.py`)
**Purpose**: Dependency injection and service instance management.

**Key Responsibilities**:
- Provide singleton instances of core services
- Initialize services on first access
- Manage service lifecycle
- Support multiple data source implementations

**Key Functions**:
- `get_ai_engine()`: Provides AI engine instance
- `get_data_source()`: Provides data source instance
- `get_email_repository()`: Provides email repository instance

**Dependencies**:
- DataSource implementations
- EmailRepository implementations
- AI engine implementations

**Design Patterns**:
- Singleton pattern
- Factory pattern
- Dependency injection
- Async context management

## Data Layer Modules

### 4. Repository Pattern (`src/core/data/repository.py`)
**Purpose**: Abstraction layer for data operations.

**Components**:
- `EmailRepository`: Abstract interface defining data operations
- `DatabaseEmailRepository`: Concrete implementation delegating to DataSource

**Key Responsibilities**:
- Provide consistent interface for email data operations
- Decouple business logic from data storage implementation
- Support multiple data source backends

**Methods**:
- `create_email()`: Create new email record
- `get_email_by_id()`: Retrieve email by ID
- `get_emails()`: Retrieve emails with filtering and pagination
- `update_email()`: Update existing email
- `search_emails()`: Search emails by term

**Dependencies**:
- DataSource interface
- Python typing system

### 5. Data Sources (`src/core/database.py`, `src/core/notmuch_data_source.py`)
**Purpose**: Concrete implementations of data storage systems.

**Components**:
- `DatabaseManager`: JSON file storage with caching
- `NotmuchDataSource`: Integration with Notmuch email indexing

**Key Responsibilities**:
- Implement DataSource interface
- Handle data persistence
- Manage data indexing and caching
- Provide efficient data access patterns

**DatabaseManager Features**:
- JSON file storage with gzip compression
- In-memory caching for performance
- Write-behind caching strategy
- Separation of email metadata and content
- Category management

**NotmuchDataSource Features**:
- Integration with Notmuch email indexing system
- Fast email search capabilities
- Tag-based categorization

### 6. Data Source Interface (`src/core/data_source.py`)
**Purpose**: Abstract interface for all data source implementations.

**Key Responsibilities**:
- Define contract for data operations
- Ensure consistency across implementations
- Support async operations

**Methods**:
- All methods from EmailRepository interface
- `shutdown()`: Cleanup resources

## Business Logic Modules

### 7. AI Engine (`src/core/ai_engine.py`)
**Purpose**: Standardized interface for AI analysis capabilities.

**Components**:
- `BaseAIEngine`: Abstract interface for AI engines
- `ModernAIEngine`: Implementation using transformer models
- `AIAnalysisResult`: Standardized result structure

**Key Responsibilities**:
- Analyze email content for insights
- Provide consistent result format
- Manage model lifecycle
- Support health checking

**Analysis Capabilities**:
- Topic classification
- Sentiment analysis
- Intent recognition
- Urgency detection
- Category suggestion
- Risk flagging

### 8. Workflow Engine (`src/core/workflow_engine.py`)
**Purpose**: Node-based workflow processing system.

**Key Responsibilities**:
- Execute complex email processing workflows
- Manage workflow state
- Integrate with AI engine for analysis
- Support extensible node types

**Features**:
- Visual workflow creation
- Security framework
- Performance monitoring
- Plugin architecture

## Module System Modules

### 9. Email Module (`modules/email/`)
**Purpose**: Email management functionality.

**Key Responsibilities**:
- Provide email API endpoints
- Handle email CRUD operations
- Integrate with repository pattern
- Support search and filtering

**API Endpoints**:
- GET `/api/emails/`: Retrieve emails
- GET `/api/emails/{id}`: Retrieve specific email
- POST `/api/emails/`: Create new email
- PUT `/api/emails/{id}`: Update email
- DELETE `/api/emails/{id}`: Delete email

### 10. Authentication Module (`modules/auth/`)
**Purpose**: User authentication and authorization.

**Key Responsibilities**:
- User registration and login
- Token-based authentication
- Password management
- Access control

**API Endpoints**:
- POST `/api/auth/register`: User registration
- POST `/api/auth/login`: User login
- POST `/api/auth/logout`: User logout
- GET `/api/auth/me`: Current user info

### 11. Dashboard Module (`modules/dashboard/`)
**Purpose**: Administrative dashboard functionality.

**Key Responsibilities**:
- System statistics and metrics
- User management
- Model management
- Performance monitoring

**API Endpoints**:
- GET `/api/dashboard/stats`: System statistics
- GET `/api/dashboard/users`: User management
- GET `/api/dashboard/models`: Model management

### 12. Category Module (`modules/categories/`)
**Purpose**: Email categorization system.

**Key Responsibilities**:
- Category management
- Email categorization
- Category statistics

**API Endpoints**:
- GET `/api/categories/`: Retrieve categories
- POST `/api/categories/`: Create category
- PUT `/api/categories/{id}`: Update category
- DELETE `/api/categories/{id}`: Delete category

## External Integration Modules

### 13. Gmail Integration (`backend/python_nlp/gmail_service.py`)
**Purpose**: Integration with Gmail API for email retrieval.

**Key Responsibilities**:
- Authenticate with Gmail
- Retrieve emails from Gmail
- Sync emails with local storage
- Handle Gmail API errors

**Features**:
- OAuth2 authentication
- Incremental email sync
- Rate limiting compliance
- Error handling and retry logic

### 14. Notmuch Integration (`src/core/notmuch_data_source.py`)
**Purpose**: Integration with Notmuch email indexing system.

**Key Responsibilities**:
- Query Notmuch database
- Retrieve emails from Notmuch
- Manage Notmuch tags
- Convert Notmuch data to standard format

## Frontend Modules

### 15. React Frontend (`client/`)
**Purpose**: User interface for email management.

**Key Responsibilities**:
- Display email list and details
- Provide email search and filtering
- Enable email categorization
- Support user authentication

**Technology Stack**:
- React with TypeScript
- Vite build system
- Tailwind CSS styling
- Radix UI components

### 16. Gradio UI (`src/main.py`)
**Purpose**: Scientific exploration interface.

**Key Responsibilities**:
- Provide visual interface for AI analysis
- Enable workflow experimentation
- Support model testing
- Facilitate scientific exploration

**Features**:
- Tab-based interface
- Interactive components
- Real-time analysis
- Visualization capabilities

## Launcher Module

### 17. Unified Launcher (`launch.py`)
**Purpose**: Central tool for managing the development environment.

**Key Responsibilities**:
- Environment setup and configuration
- Dependency management
- Service orchestration
- Testing framework integration
- Deployment support

**Features**:
- Virtual environment management
- Cross-platform support
- Conda environment support
- Automated dependency installation
- Service lifecycle management

## Design Patterns and Principles

### 1. Dependency Injection
- Factory pattern in `src/core/factory.py`
- Service locator pattern for core components
- Lazy initialization for performance

### 2. Repository Pattern
- Abstraction of data access logic
- Decoupling of business logic from data storage
- Support for multiple data source implementations

### 3. Module System
- Convention-based module discovery
- Dynamic code loading
- Isolated module functionality
- Standardized registration interface

### 4. Layered Architecture
- Clear separation of concerns
- Presentation layer (UI/API)
- Business logic layer (Services/Engine)
- Data access layer (Repository/DataSource)

### 5. Plugin Architecture
- Extensible through modules
- Standardized interfaces
- Dynamic loading capabilities

These modules work together to create a flexible, extensible email intelligence platform that can be easily maintained and enhanced.