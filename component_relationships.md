# Component Relationships

## 1. Application Flow

```
launch.py
    ↓
src/main.py (FastAPI + Gradio)
    ↓
src/core/module_manager.py
    ↓
modules/*/__init__.py (register functions)
    ↓
modules/*/routes.py (API endpoints)
    ↓
src/core/factory.py (data source)
    ↓
src/core/data_source.py (abstraction)
    ↓
src/core/database.py (implementation)
```

## 2. Data Flow

```
Email Sources
    ↓
Data Ingestion (modules/email/)
    ↓
src/core/database.py
    ↓
API Endpoints (modules/*/)
    ↓
Frontend Clients
    ↳ React (client/)
    ↳ Gradio UI (/ui)
```

## 3. Module Registration

Each module follows this pattern:

```
modules/module_name/
├── __init__.py
│   └── register(app, gradio_app)
│       ├── app.include_router(router, prefix="/api/...")
│       └── gradio_app integration (if applicable)
├── routes.py
│   └── APIRouter with endpoints
└── models.py (optional)
    └── Pydantic models
```

## 4. Data Source Hierarchy

```
src/core/data_source.py (ABC)
    ├── src/core/database.py
    │   └── JSON file storage with caching
    └── src/core/notmuch_data_source.py
        └── Alternative implementation
```

## 5. AI/NLP Pipeline

```
Email Content
    ↓
backend/python_nlp/nlp_engine.py
    ↓
Analysis Components:
├── sentiment_model.py
├── topic_model.py
├── intent_model.py
└── urgency_model.py
    ↓
Enriched Email Data
```

## 6. Frontend Integration

```
React Components (client/src/)
    ↓
API Calls (/api/...)
    ↓
FastAPI Routes (modules/*/)
    ↓
Data Source (src/core/)
```

## 7. Process Management

```
launch.py
    ↓
ProcessManager
    ├── Backend (FastAPI)
    ├── Frontend (React dev server)
    └── Gradio UI
```