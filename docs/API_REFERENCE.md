# Email Intelligence Platform API Reference

## Overview

The Email Intelligence Platform provides RESTful APIs for email processing, workflow management, AI analysis, and system monitoring.

## Authentication

All API endpoints require authentication via JWT tokens or API keys. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- General endpoints: 120 requests/minute
- Workflow endpoints: 30 requests/minute
- Model endpoints: 20 requests/minute

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)

## Core API Endpoints

### Health Check

**GET** `/health`

Returns system health status.

**Response:**
```json
{
  "status": "healthy"
}
```

### Email Management

#### List Emails
**GET** `/api/emails`

Retrieve paginated list of emails.

**Parameters:**
- `limit` (int, optional): Number of emails to return (default: 50, max: 100)
- `offset` (int, optional): Pagination offset (default: 0)
- `category_id` (int, optional): Filter by category ID
- `is_unread` (bool, optional): Filter by read status

**Response:**
```json
{
  "emails": [
    {
      "id": 1,
      "message_id": "abc123@example.com",
      "subject": "Test Email",
      "sender": "sender@example.com",
      "timestamp": "2024-01-01T12:00:00Z",
      "is_unread": true,
      "category_id": 1
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

#### Get Email
**GET** `/api/emails/{email_id}`

Retrieve detailed information about a specific email.

**Parameters:**
- `include_content` (bool, optional): Include full email content (default: true)

**Response:**
```json
{
  "id": 1,
  "message_id": "abc123@example.com",
  "subject": "Test Email",
  "sender": "sender@example.com",
  "content": "Full email content...",
  "timestamp": "2024-01-01T12:00:00Z",
  "is_unread": true,
  "category_id": 1,
  "labels": ["INBOX", "IMPORTANT"]
}
```

#### Update Email
**PUT** `/api/emails/{email_id}`

Update email properties.

**Request Body:**
```json
{
  "is_unread": false,
  "category_id": 2,
  "tags": ["important", "work"]
}
```

### Category Management

#### List Categories
**GET** `/api/categories`

Retrieve all email categories.

**Response:**
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Work",
      "color": "#FF6B6B",
      "email_count": 25
    }
  ]
}
```

#### Create Category
**POST** `/api/categories`

Create a new email category.

**Request Body:**
```json
{
  "name": "New Category",
  "color": "#4ECDC4"
}
```

#### Update Category
**PUT** `/api/categories/{category_id}`

Update an existing category.

**Request Body:**
```json
{
  "name": "Updated Category",
  "color": "#45B7D1"
}
```

### Workflow Management

#### List Workflows
**GET** `/api/workflows`

Retrieve available workflows.

**Response:**
```json
{
  "workflows": [
    {
      "id": "wf_123",
      "name": "Email Analysis Pipeline",
      "description": "Comprehensive email analysis workflow",
      "status": "active",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

#### Execute Workflow
**POST** `/api/workflows/{workflow_id}/execute`

Execute a workflow with given parameters.

**Request Body:**
```json
{
  "input_data": {
    "emails": ["email_id_1", "email_id_2"],
    "parameters": {
      "analysis_type": "comprehensive"
    }
  }
}
```

### AI Analysis

#### Analyze Email
**POST** `/api/ai/analyze`

Perform AI analysis on email content.

**Request Body:**
```json
{
  "subject": "Meeting Tomorrow",
  "content": "Let's meet tomorrow at 2 PM to discuss the project.",
  "analysis_type": "comprehensive"
}
```

**Response:**
```json
{
  "sentiment": "neutral",
  "sentiment_confidence": 0.85,
  "topic": "meeting",
  "topic_confidence": 0.92,
  "intent": "scheduling",
  "intent_confidence": 0.78,
  "urgency": "medium",
  "urgency_confidence": 0.71
}
```

### Dashboard & Monitoring

#### Get Dashboard Stats
**GET** `/api/dashboard/stats`

Retrieve consolidated dashboard statistics using repository pattern with caching.

**Authentication Required:** Bearer token

**Response:**
```json
{
  "total_emails": 1250,
  "categorized_emails": {
    "Work": 500,
    "Personal": 450,
    "Social": 200,
    "Other": 100
  },
  "unread_emails": 45,
  "auto_labeled": 320,
  "categories": 4,
  "time_saved": "10h 40m",
  "weekly_growth": {
    "emails": 1250,
    "percentage": 5.2
  },
  "performance_metrics": {
    "get_emails": 0.12,
    "search_emails": 0.08,
    "create_email": 0.25
  }
}
```

**Response Fields:**
- `total_emails` (int): Total number of emails in the system
- `categorized_emails` (Dict[str, int]): Breakdown of emails by category
- `unread_emails` (int): Number of unread emails
- `auto_labeled` (int): Number of emails auto-labeled by AI
- `categories` (int): Total number of categories
- `time_saved` (str): Estimated time saved from auto-labeling (format: "Xh Ym")
- `weekly_growth` (object): Weekly growth metrics
  - `emails` (int): Number of emails processed
  - `percentage` (float): Growth percentage
- `performance_metrics` (Dict[str, float]): Performance metrics for operations (seconds)

#### Performance Metrics
**GET** `/metrics`

Retrieve Prometheus-compatible metrics for monitoring.

### Gmail Integration

#### Sync Gmail
**POST** `/api/gmail/sync`

Synchronize emails from Gmail.

**Request Body:**
```json
{
  "maxEmails": 100,
  "queryFilter": "newer_than:7d",
  "includeAIAnalysis": true
}
```

#### Gmail Performance
**GET** `/api/gmail/performance`

Get Gmail integration performance metrics.

## Error Handling

All APIs return standardized error responses:

```json
{
  "detail": "Error description",
  "message": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (validation error)
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Too Many Requests (rate limited)
- `500`: Internal Server Error

## Security Features

- **Path Traversal Protection**: All file operations are validated for directory traversal attempts
- **Input Sanitization**: All user inputs are validated and sanitized
- **Rate Limiting**: Prevents API abuse and DoS attacks
- **Audit Logging**: All API calls are logged for security monitoring
- **CORS Protection**: Configurable cross-origin resource sharing
- **Security Headers**: Comprehensive security headers on all responses

## WebSocket Endpoints

### Workflow Status Updates
**WebSocket** `/ws/workflow/{workflow_id}`

Subscribe to real-time workflow execution updates.

**Messages:**
```json
{
  "type": "workflow_progress",
  "workflow_id": "wf_123",
  "status": "running",
  "progress": 0.75,
  "current_step": "AI Analysis"
}
```</content>
</xai:function_call: <parameter name="path">/home/masum/github/EmailIntelligence/docs/API_REFERENCE.md
