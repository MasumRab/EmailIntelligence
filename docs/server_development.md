# EmailIntelligence Server Components

This directory contains the server-side components of the EmailIntelligence application. The server is split into two main parts:

1. **Python FastAPI Backend**: Provides AI and NLP capabilities through a REST API
2. **Python NLP Engine**: Implements the core AI and NLP functionality

## Directory Structure

- **python_backend/**: Contains the Python FastAPI backend
  - `main.py` - Main entry point for the FastAPI server
  - `run_server.py` - Script to run the FastAPI server
  - `ai_engine.py` - AI engine implementation
  - `gmail_service.py` - Gmail service implementation
  - `models.py` - Pydantic models for API requests/responses
  - `database.py` - Database connection and models
  - `metrics.py` - Prometheus metrics for monitoring
  - `performance_monitor.py` - Performance monitoring utilities
  - `smart_filters.py` - Smart filtering implementation

- **python_nlp/**: Contains the core NLP and AI functionality
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
python server/python_backend/run_server.py
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