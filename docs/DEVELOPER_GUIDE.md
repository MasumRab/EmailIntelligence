# Email Intelligence Platform Developer Guide

## Overview

This guide provides comprehensive documentation for developers extending and maintaining the Email Intelligence Platform.

## Architecture Overview

The platform follows a modular architecture with clear separation of concerns:

```
src/core/          # Core system components
├── database.py    # Database management with security
├── security.py    # Path validation and security utilities
├── audit_logger.py # Comprehensive audit logging
├── rate_limiter.py # API rate limiting
├── middleware.py  # FastAPI security middleware
└── performance_monitor.py # Performance metrics

src/modules/       # Pluggable feature modules
docs/             # Documentation
tests/            # Test suites
```

## Core Components

### Security Module (`src/core/security.py`)

Provides essential security utilities for path validation and access control.

#### Path Validation

```python
from src.core.security import validate_path_safety, sanitize_path

# Validate a path for security
is_safe = validate_path_safety("/user/uploads/file.txt")
# Returns: True

is_safe = validate_path_safety("../../../etc/passwd")
# Returns: False (directory traversal detected)

# Sanitize a path
safe_path = sanitize_path("/tmp/user_file.db", base_dir="/tmp")
# Returns: Path object or None if unsafe
```

#### Key Functions

- **`validate_path_safety(path, base_dir=None)`**: Validates paths against directory traversal attacks
- **`sanitize_path(path, base_dir=None)`**: Resolves and sanitizes paths safely
- **`secure_path_join(base_dir, *paths)`**: Joins paths with security validation

### Audit Logging (`src/core/audit_logger.py`)

Comprehensive event logging for security monitoring and compliance.

```python
from src.core.audit_logger import audit_logger, AuditEventType, AuditSeverity

# Log a security event
audit_logger.log_security_event(
    event_type=AuditEventType.UNAUTHORIZED_ACCESS,
    severity=AuditSeverity.HIGH,
    user_id="user123",
    resource="/api/admin",
    action="GET",
    result="failure"
)

# Log API access
audit_logger.log_api_access(
    endpoint="/api/emails",
    method="GET",
    user_id="user123",
    ip_address="192.168.1.1",
    status_code=200,
    response_time=0.125
)
```

#### Audit Event Types

- `LOGIN_SUCCESS/FAILURE`: Authentication events
- `EMAIL_ACCESS/MODIFY/DELETE`: Email operations
- `WORKFLOW_START/END/ERROR`: Workflow execution
- `SECURITY_VIOLATION`: Security incidents
- `RATE_LIMIT_EXCEEDED`: Rate limit violations

### Rate Limiting (`src/core/rate_limiter.py`)

Token bucket algorithm for API rate limiting.

```python
from src.core.rate_limiter import api_rate_limiter

# Check rate limit for an endpoint
allowed, headers = await api_rate_limiter.check_rate_limit(
    endpoint="/api/emails",
    client_key="user123"
)

if not allowed:
    # Return rate limit exceeded response
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded"},
        headers=headers
    )
```

#### Custom Rate Limits

```python
from src.core.rate_limiter import RateLimiter, RateLimitConfig

# Create custom rate limiter
config = RateLimitConfig(requests_per_minute=100, burst_limit=20)
limiter = RateLimiter(config)
api_rate_limiter.add_endpoint_limit("/api/custom", config)
```

### Performance Monitoring (`src/core/performance_monitor.py`)

Efficient metrics collection with configurable sampling.

```python
from src.core.performance_monitor import performance_monitor

# Record a metric
performance_monitor.record_metric(
    name="api_response_time",
    value=0.125,
    unit="seconds",
    tags={"endpoint": "/api/emails", "method": "GET"}
)

# Time a function
@performance_monitor.time_function("my_function", sample_rate=0.1)
def my_function():
    # Function code here
    pass

# Get aggregated metrics
metrics = performance_monitor.get_aggregated_metrics()
```

### Security Middleware (`src/core/middleware.py`)

FastAPI middleware integrating all security components.

```python
from src.core.middleware import create_security_middleware

# Add to FastAPI app
app.add_middleware(create_security_middleware(app))
app.add_middleware(create_security_headers_middleware(app))
```

## Database Management

### Secure Database Configuration

```python
from src.core.database import DatabaseConfig, create_database_manager

# Create secure database configuration
config = DatabaseConfig(
    data_dir="/secure/data",
    # Paths are automatically validated
)

# Create database manager
db_manager = await create_database_manager(config)
```

### Security Validation

The database configuration automatically validates all paths:

```python
# This will raise ValueError for unsafe paths
try:
    config = DatabaseConfig(data_dir="../../../unsafe")
except ValueError as e:
    print(f"Security violation: {e}")
```

## Testing

### Test Setup

```python
# tests/conftest.py provides:
# - create_app(): Minimal FastAPI app for testing
# - mock_db_manager: Mocked database manager
# - client: FastAPI TestClient with dependency overrides

def test_my_endpoint(client: TestClient, mock_db_manager):
    # Mock database responses
    mock_db_manager.get_emails.return_value = []

    response = client.get("/api/emails")
    assert response.status_code == 200
```

### Security Testing

```python
from src.core.security import validate_path_safety

def test_path_validation():
    # Test safe paths
    assert validate_path_safety("/tmp/test.db")

    # Test dangerous paths
    assert not validate_path_safety("../../../etc/passwd")
```

## Extending the Platform

### Adding New API Endpoints

```python
from fastapi import APIRouter, Depends
from src.core.database import get_db
from src.core.middleware import create_security_middleware

router = APIRouter()

@router.get("/custom")
async def custom_endpoint(db=Depends(get_db)):
    # Your endpoint logic here
    return {"message": "Custom endpoint"}

# Register with main app
app.include_router(router, prefix="/api")
```

### Creating Custom Security Validators

```python
from src.core.security_validator import NodeSecurityValidator

class CustomValidator(NodeSecurityValidator):
    def validate_custom_logic(self, code: str) -> bool:
        # Your custom validation logic
        return "dangerous_function" not in code
```

### Adding Performance Metrics

```python
from src.core.performance_monitor import performance_monitor

# Add custom metrics
performance_monitor.record_metric(
    "custom_metric",
    value=42,
    unit="operations",
    tags={"component": "my_module"}
)
```

## Security Best Practices

### Input Validation

- Always validate user inputs using the security utilities
- Use type hints and Pydantic models for API validation
- Implement proper error handling without information leakage

### Path Security

```python
# Always use secure path operations
from src.core.security import secure_path_join

safe_path = secure_path_join("/app/data", user_input, "file.db")
if safe_path is None:
    raise ValueError("Unsafe path provided")
```

### Authentication & Authorization

- Use JWT tokens for API authentication
- Implement proper role-based access control
- Log all authentication and authorization events

### Error Handling

```python
from src.core.audit_logger import audit_logger, AuditSeverity

try:
    # Risky operation
    pass
except Exception as e:
    # Log security events
    audit_logger.log_security_event(
        event_type=AuditEventType.SECURITY_VIOLATION,
        severity=AuditSeverity.MEDIUM,
        details={"error": str(e), "operation": "risky_function"}
    )
    # Don't expose internal details
    raise HTTPException(status_code=500, detail="Internal server error")
```

## Monitoring & Observability

### Setting Up Monitoring

```python
# Add to your application startup
from src.core.performance_monitor import performance_monitor
from src.core.audit_logger import audit_logger

# Configure monitoring
performance_monitor = performance_monitor
audit_logger = audit_logger

# Metrics are automatically collected for API endpoints
# when using the security middleware
```

### Key Metrics to Monitor

- API response times and error rates
- Database query performance
- Security violation attempts
- Rate limiting effectiveness
- Resource utilization (CPU, memory, disk)

## Deployment

### Production Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  app:
    image: email-intelligence:latest
    environment:
      - DATA_DIR=/app/data
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

### Security Checklist

- [ ] All file paths validated using security utilities
- [ ] Rate limiting configured for all endpoints
- [ ] Audit logging enabled for security events
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] Error messages don't leak sensitive information
- [ ] Database paths secured against traversal attacks

## Troubleshooting

### Common Issues

1. **Path validation errors**: Ensure all file operations use the security utilities
2. **Rate limiting issues**: Check client keys and endpoint configurations
3. **Audit logging not working**: Verify file permissions on log directories
4. **Performance metrics missing**: Ensure middleware is properly configured

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug logging for security components
logger = logging.getLogger('src.core.security')
logger.setLevel(logging.DEBUG)
```

## Contributing

1. Follow security best practices for all new code
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure all code passes security validation
5. Add appropriate audit logging for security-sensitive operations</content>
</xai:function_call: <parameter name="path">/home/masum/github/EmailIntelligence/docs/DEVELOPER_GUIDE.md
