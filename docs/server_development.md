# EmailIntelligence Server Components

The server-side components of the EmailIntelligence application are split into multiple parts:

1. **Node.js/TypeScript Backend** (`backend/server-ts/`): Handles the main application logic, database interactions, and serves the frontend
2. **Python FastAPI Backend** (`src/`): Provides AI and NLP capabilities through a REST API
3. **Python NLP Engine** (`backend/python_nlp/`): Implements the core AI and NLP functionality

## Directory Structure

- **backend/server-ts/**: Contains the Node.js/TypeScript backend files
  - `index.ts` - Main entry point for the Node.js server
  - `routes.ts` - API route definitions
  - `db.ts` - Database connection and models
  - `python-bridge.ts` - Bridge to communicate with the Python backend
  - `gmail-ai-service.ts` - Service for Gmail AI integration
  - `ai-engine.ts` - TypeScript interface to the AI engine
  - `storage.ts` - File storage utilities
  - `vite.ts` - Vite configuration for serving the frontend

- **src/**: Contains the Python FastAPI backend
  - `main.py` - Main entry point for the FastAPI server
  - `core/` - Core modules (ai_engine, database, etc.)
  - `models/` - Pydantic models for API requests/responses

- **backend/python_nlp/**: Contains the Python NLP engine
  - `gmail_service.py` - Gmail service implementation
  - `smart_filters.py` - Smart filtering implementation

- **backend/python_nlp/**: Contains the core NLP and AI functionality
  - `nlp_engine.py` - Core NLP engine implementation
  - `ai_training.py` - Model training utilities
  - `gmail_integration.py` - Gmail API integration
  - `gmail_service.py` - Gmail service implementation
  - `gmail_metadata.py` - Gmail metadata extraction
  - `data_strategy.py` - Data processing strategies
  - `smart_filters.py` - Smart filtering implementation
  - `smart_retrieval.py` - Smart retrieval implementation
  - `retrieval_monitor.py` - Monitoring for retrieval operations

## Running the Servers

### Node.js/TypeScript Backend

```bash
# From the project root
npm run dev
```

### Python FastAPI Backend

```bash
# From the project root
python -m uvicorn src.main:create_app --factory --host 0.0.0.0 --port 8000
```

Or use the unified launcher:

```bash
# From the project root
python launch.py --stage dev
```

## API Documentation

The Python FastAPI backend provides automatic API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

When developing server components, follow these guidelines:

1. **TypeScript Backend**:
   - Follow the TypeScript style guide
   - Use the provided database models and utilities
   - Add new routes in `routes.ts`

2. **Python Backend**:
   - Follow the [Python Style Guide](python_style_guide.md)
   - Use FastAPI dependency injection for services
   - Add new endpoints in `main.py`

3. **Python NLP**:
   - Follow the [Python Style Guide](python_style_guide.md)
   - Add new NLP functionality in appropriate modules
   - Train models using `ai_training.py`