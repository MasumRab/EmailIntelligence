# Data Flow Architecture

## Overview

This document describes the data flow throughout the EmailIntelligence application, showing how data moves between components and systems.

## 1. Email Ingestion Flow

```
External Email Sources
    ↓
┌─────────────────────────────────┐
│     Email Retrieval Module      │
├─────────────────────────────────┤
│ modules/email_retrieval/        │
│ - Gmail API Integration         │
│ - File Import                   │
│ - Manual Entry                  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│        Data Storage             │
├─────────────────────────────────┤
│ src/core/database.py            │
│ - JSON file storage             │
│ - Gzip compression              │
│ - In-memory caching             │
│ - Indexing for performance      │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│        Data Validation          │
├─────────────────────────────────┤
│ pydantic models                 │
│ - Email data structure          │
│ - Category definitions          │
│ - User information              │
└─────────────────────────────────┘
```

## 2. AI/NLP Processing Flow

```
Stored Email Data
    ↓
┌─────────────────────────────────┐
│      NLP Engine Pipeline        │
├─────────────────────────────────┤
│ backend/python_nlp/nlp_engine.py│
│ - Text preprocessing            │
│ - Feature extraction            │
│ - Model inference               │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│    Analysis Components          │
├─────────────────────────────────┤
│ sentiment_model.py              │
│ topic_model.py                  │
│ intent_model.py                 │
│ urgency_model.py                │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│     Results Storage             │
├─────────────────────────────────┤
│ Enriched email data with:       │
│ - Sentiment scores              │
│ - Topic classifications         │
│ - Intent predictions            │
│ - Urgency assessments           │
└─────────────────────────────────┘
```

## 3. API Request Flow

```
Client Requests (React/External)
    ↓
┌─────────────────────────────────┐
│      FastAPI Router             │
├─────────────────────────────────┤
│ src/main.py                     │
│ - Request validation            │
│ - Authentication middleware     │
│ - Rate limiting (if configured) │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│     Module Endpoints            │
├─────────────────────────────────┤
│ modules/*/routes.py             │
│ - Business logic implementation │
│ - Data transformation           │
│ - Error handling                │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Data Access Layer          │
├─────────────────────────────────┤
│ src/core/factory.py             │
│ src/core/data_source.py         │
│ - Abstract data operations      │
│ - Multiple backend support      │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Data Implementation        │
├─────────────────────────────────┤
│ src/core/database.py            │
│ backend/python_nlp/*            │
│ - Actual data retrieval         │
│ - Caching mechanisms            │
│ - File I/O operations           │
└─────────────────────────────────┘
    ↓
Response to Client
```

## 4. UI Interaction Flow

```
User Interface Actions
    ↓
┌─────────────────────────────────┐
│      Frontend Framework         │
├─────────────────────────────────┤
│ React (client/)                 │
│ Gradio (src/main.py UI)         │
│ - State management              │
│ - Component rendering           │
│ - User input handling           │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      API Communication          │
├─────────────────────────────────┤
│ HTTP/REST calls                 │
│ - GET/POST/PUT/DELETE           │
│ - JSON data exchange            │
│ - Authentication headers        │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Backend Processing         │
├─────────────────────────────────┤
│ FastAPI application             │
│ - Request parsing               │
│ - Business logic execution      │
│ - Data persistence              │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Response Formatting        │
├─────────────────────────────────┤
│ JSON serialization              │
│ - Data transformation           │
│ - Error response handling       │
│ - Caching headers               │
└─────────────────────────────────┘
    ↓
UI Update with Results
```

## 5. Workflow Processing Flow

```
Workflow Definition
    ↓
┌─────────────────────────────────┐
│      Workflow Engine            │
├─────────────────────────────────┤
│ backend/node_engine/            │
│ - Node execution                │
│ - Data flow management          │
│ - Error handling                │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Node Processing            │
├─────────────────────────────────┤
│ Individual node execution       │
│ - Data transformation           │
│ - External API calls            │
│ - Conditional logic             │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Data Persistence           │
├─────────────────────────────────┤
│ Results stored in:              │
│ - Database updates              │
│ - File outputs                  │
│ - External system updates       │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Notification System        │
├─────────────────────────────────┤
│ - Completion notifications      │
│ - Error alerts                  │
│ - Progress updates              │
└─────────────────────────────────┘
```

## 6. Authentication Flow

```
Login Request
    ↓
┌─────────────────────────────────┐
│      Auth Endpoint              │
├─────────────────────────────────┤
│ modules/auth/routes.py          │
│ - Credential validation         │
│ - Password verification         │
│ - Token generation              │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      User Verification          │
├─────────────────────────────────┤
│ src/core/database.py            │
│ - User lookup                   │
│ - Password comparison           │
│ - Account status check          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Token Creation             │
├─────────────────────────────────┤
│ JWT token generation            │
│ - User claims                   │
│ - Expiration time               │
│ - Signing                       │
└─────────────────────────────────┘
    ↓
Client with Auth Token

Subsequent Requests:
Client → Auth Middleware → Route Handler → Data Access → Response
```

## 7. Data Storage Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Directory                           │
├─────────────────────────────────────────────────────────────────┤
│ data/                                                           │
│ ├── emails.json.gz              ← Email records                │
│ ├── categories.json.gz          ← Category definitions          │
│ ├── users.json.gz               ← User accounts                │
│ ├── sender_labels.json          ← Sender categorization        │
│ ├── settings.json               ← Application settings          │
│ └── email_content/              ← Raw email content            │
│     ├── {message_id}.txt        ← Individual email bodies      │
│     └── attachments/            ← Email attachments            │
└─────────────────────────────────────────────────────────────────┘
    ↑
┌─────────────────────────────────────────────────────────────────┐
│                    Database Manager                             │
├─────────────────────────────────────────────────────────────────┤
│ src/core/database.py                                            │
│ - In-memory caching                                             │
│ - Indexing for fast lookups                                     │
│ - Thread-safe operations                                        │
│ - Automatic persistence                                         │
└─────────────────────────────────────────────────────────────────┘
    ↑
┌─────────────────────────────────────────────────────────────────┐
│                   Data Source Abstraction                       │
├─────────────────────────────────────────────────────────────────┤
│ src/core/data_source.py                                         │
│ - Abstract interface                                            │
│ - Multiple implementations possible                             │
│ - Consistent API across backends                                │
└─────────────────────────────────────────────────────────────────┘
```

## 8. Performance Monitoring Flow

```
Application Operations
    ↓
┌─────────────────────────────────┐
│      Performance Tracking       │
├─────────────────────────────────┤
│ backend/python_backend/         │
│ performance_monitor.py          │
│ - Operation timing              │
│ - Resource usage monitoring     │
│ - Performance logging           │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Metrics Collection         │
├─────────────────────────────────┤
│ - Duration measurements         │
│ - Memory usage tracking         │
│ - Error rate monitoring         │
│ - Throughput metrics            │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Data Aggregation           │
├─────────────────────────────────┤
│ modules/dashboard/routes.py     │
│ - Statistical analysis          │
│ - Trend identification          │
│ - Performance reporting         │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│      Visualization              │
├─────────────────────────────────┤
│ Dashboard UI                    │
│ - Real-time metrics display     │
│ - Historical data charts        │
│ - Performance alerts            │
└─────────────────────────────────┘
```

## Key Data Flow Principles

1. **Consistent Data Models**: All components use pydantic models for data validation
2. **Abstracted Data Access**: Data source abstraction allows for backend flexibility
3. **Asynchronous Processing**: Non-blocking operations for better performance
4. **Caching Strategy**: In-memory caching reduces file I/O for frequently accessed data
5. **Error Handling**: Comprehensive error handling at each layer
6. **Security**: Authentication and authorization at the API layer
7. **Monitoring**: Performance tracking throughout the system
8. **Scalability**: Stateless design allows for horizontal scaling