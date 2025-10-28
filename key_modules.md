# Key Modules and Responsibilities

## Core System Modules

### 1. Authentication Module (`modules/auth/`)
- **Responsibilities**: User authentication and authorization
- **API Endpoints**: `/api/auth/login`, `/api/auth/logout`, `/api/auth/register`
- **Key Features**: JWT token management, password hashing, session handling

### 2. Email Module (`modules/email/`)
- **Responsibilities**: Email management and processing
- **API Endpoints**: `/api/emails/`, `/api/emails/{id}`, `/api/emails/sync`
- **Key Features**: Email CRUD operations, synchronization with external sources

### 3. Categories Module (`modules/categories/`)
- **Responsibilities**: Email categorization system
- **API Endpoints**: `/api/categories/`, `/api/categories/{id}`
- **Key Features**: Category CRUD operations, email-category associations

### 4. Dashboard Module (`modules/dashboard/`)
- **Responsibilities**: System statistics and metrics
- **API Endpoints**: `/api/dashboard/stats`
- **Key Features**: Email statistics, performance metrics, system health

### 5. Workflows Module (`modules/workflows/`)
- **Responsibilities**: Workflow management and execution
- **API Endpoints**: `/api/workflows/`, `/api/workflows/{id}/execute`
- **Key Features**: Workflow CRUD, execution engine, scheduling

## Backend Components

### 1. Python NLP (`backend/python_nlp/`)
- **Responsibilities**: Natural language processing and AI analysis
- **Components**:
  - `nlp_engine.py`: Main NLP processing engine
  - `analysis_components/`: Individual analysis modules
    - `sentiment_model.py`: Sentiment analysis
    - `topic_model.py`: Topic classification
    - `intent_model.py`: Intent recognition
    - `urgency_model.py`: Urgency detection

### 2. Node Engine (`backend/node_engine/`)
- **Responsibilities**: Node-based workflow processing
- **Components**:
  - `workflow_engine.py`: Core workflow execution
  - `node_base.py`: Base node class
  - `security_manager.py`: Security controls
  - `workflow_manager.py`: Workflow lifecycle management

### 3. Python Backend (`backend/python_backend/`)
- **Responsibilities**: Legacy FastAPI application
- **Components**:
  - `main.py`: Legacy application entry point
  - `ai_engine.py`: Legacy AI processing
  - `database.py`: Legacy database management
  - Various route files for different features

## Core Infrastructure

### 1. Module Manager (`src/core/module_manager.py`)
- **Responsibilities**: Module discovery and loading
- **Key Features**: Dynamic module registration, error handling

### 2. Data Source (`src/core/data_source.py`)
- **Responsibilities**: Abstract data access layer
- **Key Features**: Database abstraction, multiple implementations

### 3. Database Manager (`src/core/database.py`)
- **Responsibilities**: JSON-based data storage
- **Key Features**: File storage, caching, indexing

### 4. Launcher (`launch.py`)
- **Responsibilities**: Unified application management
- **Key Features**: Environment setup, process management, dependency handling

## Frontend Components

### 1. React Client (`client/src/`)
- **Responsibilities**: Modern web interface
- **Components**:
  - `components/`: Reusable UI components
  - `pages/`: Page-level components
  - API integration with FastAPI backend

### 2. Gradio UI (Integrated in `src/main.py`)
- **Responsibilities**: Scientific exploration interface
- **Components**:
  - Tabbed interface with multiple views
  - Integration with FastAPI backend
  - Real-time data visualization

## Extension Points

### 1. Plugins (`backend/plugins/`)
- **Responsibilities**: Extendable functionality
- **Key Features**: Plugin architecture, dynamic loading

### 2. Extensions (`backend/extensions/`)
- **Responsibilities**: Additional features and integrations
- **Key Features**: Example extension template, loading mechanism