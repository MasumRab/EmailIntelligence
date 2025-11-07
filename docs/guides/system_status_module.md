# System Status Module Documentation

## Overview

The System Status module provides comprehensive monitoring and health checking capabilities for the Email Intelligence Platform. It offers both UI-based monitoring through the Gradio interface and API-based health endpoints for programmatic access to system status and performance metrics.

## Architecture

### Key Components

#### 1. Gradio UI System Status Tab (`src/main.py`)
The primary user interface for system monitoring, displaying real-time system information and metrics.

#### 2. API Health Endpoints (`src/core/model_routes.py`)
RESTful API endpoints providing programmatic access to health status and system metrics.

#### 3. Health Check Methods
Various components implement health check methods for comprehensive system validation.

### Data Flow
```
Gradio UI → System Status Tab → API Calls → Health Endpoints → Component Health Checks
                              ↓
                    Real-time Data Collection → Display Updates
```

### Integration Points
- **Dashboard API:** `/api/dashboard/stats` for email statistics
- **Gmail API:** `/api/gmail/performance` for Gmail connectivity status
- **Model Manager:** Health checks for AI model system
- **Plugin System:** Plugin manager status monitoring

## Core Classes & Functions

### Gradio UI Components

#### `create_system_status_tab()`
```python
def create_system_status_tab():
    """Create the System Status tab with monitoring and diagnostics."""

    def refresh_system_status():
        """Refresh and return current system status."""
        # System information collection
        # Resource usage monitoring
        # API status checks
        # Return formatted status data
```

### API Endpoints

#### Health Status Endpoint
```python
@router.get("/health", response_model=HealthStatus)
async def get_health_status(
    manager: DynamicModelManager = Depends(get_model_manager)
):
    """Get overall health status of the model management system."""
    try:
        return HealthStatus(**manager.get_health_status())
    except Exception as e:
        logger.error(f"Error getting health status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get health status")
```

#### System Metrics Endpoint
```python
@router.get("/metrics", response_model=SystemMetrics)
async def get_system_metrics(
    manager: DynamicModelManager = Depends(get_model_manager)
):
    """Get comprehensive system performance metrics."""
    try:
        return SystemMetrics(**manager.get_system_metrics())
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system metrics")
```

## Configuration

### Environment Variables
```bash
# System monitoring configuration
SYSTEM_MONITORING_ENABLED=true
HEALTH_CHECK_INTERVAL=30
METRICS_RETENTION_DAYS=7

# API endpoints
HEALTH_CHECK_TIMEOUT=5
METRICS_UPDATE_INTERVAL=60
```

### Runtime Configuration
```python
from src.main import create_system_status_tab

# System status tab configuration
system_status_config = {
    "refresh_interval": 30,  # seconds
    "show_detailed_metrics": True,
    "alert_thresholds": {
        "cpu_percent": 80,
        "memory_percent": 85,
        "disk_percent": 90
    }
}
```

## Usage Examples

### Basic System Status Monitoring

```python
# In Gradio UI - automatic system status display
from src.main import create_system_status_tab

# Create and display system status tab
system_tab = create_system_status_tab()
# Tab automatically refreshes every 30 seconds with current system data
```

### API Health Check

```python
import requests

# Check system health via API
response = requests.get("http://localhost:8000/api/models/health")
if response.status_code == 200:
    health_data = response.json()
    print(f"System Health: {health_data['status']}")
    print(f"Active Models: {health_data['active_models']}")
    print(f"Memory Usage: {health_data['memory_usage_mb']} MB")
```

### Programmatic Status Retrieval

```python
from src.core.dynamic_model_manager import DynamicModelManager

# Get detailed system status
manager = DynamicModelManager()
health_status = manager.get_health_status()

print(f"System Status: {health_status['status']}")
print(f"Loaded Models: {health_status['loaded_models']}")
print(f"Total Memory: {health_status['total_memory_mb']} MB")
print(f"GPU Memory: {health_status['gpu_memory_mb']} MB")
```

## API Reference

### Health Status Endpoint

**GET** `/api/models/health`

Returns comprehensive health status of the AI model management system.

**Response:**
```json
{
  "status": "healthy",
  "active_models": 3,
  "total_memory_mb": 2048,
  "gpu_memory_mb": 1024,
  "loaded_models": [
    {
      "id": "sentiment-model-v1",
      "status": "healthy",
      "memory_usage": 256
    }
  ],
  "timestamp": "2025-10-31T14:30:00Z"
}
```

**Error Responses:**
- `500 Internal Server Error`: Health check failed

### System Metrics Endpoint

**GET** `/api/models/metrics`

Returns detailed system performance metrics.

**Response:**
```json
{
  "total_models": 5,
  "loaded_models": 3,
  "total_memory_usage_mb": 2048,
  "gpu_memory_usage_mb": 1024,
  "average_load_time_ms": 1250.5,
  "total_load_count": 150,
  "health_score": 95.2,
  "uptime_seconds": 3600
}
```

## Performance Considerations

### Resource Monitoring
- **CPU Usage:** Monitored via `psutil.cpu_percent()`
- **Memory Usage:** Tracked via `psutil.virtual_memory()`
- **Disk Usage:** Monitored via `psutil.disk_usage('/')`
- **GPU Memory:** AI model memory consumption tracking

### Health Check Performance
- **Response Time:** < 500ms for health endpoint
- **Memory Overhead:** < 10MB for monitoring components
- **CPU Impact:** < 1% additional CPU usage
- **Update Frequency:** Configurable refresh intervals

### Optimization Strategies
```python
# Configure monitoring intervals
monitoring_config = {
    "health_check_interval": 30,  # seconds
    "metrics_collection_interval": 60,  # seconds
    "data_retention_days": 7
}

# Enable selective monitoring
selective_monitoring = {
    "cpu_monitoring": True,
    "memory_monitoring": True,
    "disk_monitoring": True,
    "network_monitoring": False,  # Disabled for performance
    "gpu_monitoring": True
}
```

## Security Considerations

### Access Control
- Health endpoints require authentication
- Sensitive system information protected
- Rate limiting on monitoring endpoints
- Audit logging of health check access

### Data Protection
```python
# Sanitize sensitive system information
def sanitize_system_info(system_data):
    """Remove sensitive information from system status."""
    sanitized = system_data.copy()

    # Remove sensitive paths
    if 'system_info' in sanitized:
        # Keep only non-sensitive system information
        safe_info = {
            'os': sanitized['system_info'].get('os'),
            'python_version': sanitized['system_info'].get('python_version'),
            'cpu_count': sanitized['system_info'].get('cpu_count')
        }
        sanitized['system_info'] = safe_info

    return sanitized
```

## Monitoring & Observability

### Health Check Metrics
```python
# Health status indicators
health_indicators = {
    "database": "healthy",      # Database connectivity
    "models": "healthy",        # AI model system
    "memory": "warning",        # Memory usage > 80%
    "disk": "healthy",          # Disk space adequate
    "network": "healthy"        # Network connectivity
}

# Overall system health score
overall_health = calculate_health_score(health_indicators)
```

### Logging and Alerts
```python
import logging

logger = logging.getLogger('system_status')

# Health check logging
logger.info("System health check completed successfully")
logger.warning("High memory usage detected: 85%")
logger.error("Database connectivity lost")

# Alert thresholds
alert_config = {
    "memory_threshold": 85,     # Alert when > 85%
    "disk_threshold": 90,       # Alert when > 90%
    "cpu_threshold": 80,        # Alert when > 80%
    "response_time_threshold": 2000  # Alert when > 2 seconds
}
```

### Dashboard Integration
```python
# System status dashboard components
dashboard_components = {
    "system_info": {
        "os": "Linux",
        "version": "Ubuntu 24.04",
        "uptime": "2 days, 4 hours"
    },
    "resource_usage": {
        "cpu": "45%",
        "memory": "2.1 GB / 8 GB",
        "disk": "120 GB / 500 GB"
    },
    "service_status": {
        "api": "healthy",
        "database": "healthy",
        "models": "healthy"
    }
}
```

## Troubleshooting

### Common Issues

#### High Memory Usage
```
Symptoms: System showing >80% memory usage
```

**Diagnosis:**
```bash
# Check memory usage details
ps aux --sort=-%mem | head -10

# Check for memory leaks in Python
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
```

**Solutions:**
```python
# Enable memory optimization
from src.core.dynamic_model_manager import DynamicModelManager

manager = DynamicModelManager()
await manager.optimize_memory()

# Adjust model cache settings
config = {
    "max_cached_models": 2,
    "memory_cleanup_interval": 300  # 5 minutes
}
```

#### Slow Health Check Response
```
Symptoms: Health endpoint taking >2 seconds
```

**Diagnosis:**
```bash
# Time the health check
time curl http://localhost:8000/api/models/health

# Check system resource usage
top -b -n1 | head -20
```

**Solutions:**
```python
# Optimize health check configuration
health_config = {
    "parallel_checks": True,
    "timeout_seconds": 5,
    "cache_results": True,
    "cache_ttl": 30
}
```

#### Database Connectivity Issues
```
Symptoms: Dashboard stats showing "API unavailable"
```

**Diagnosis:**
```bash
# Test database connectivity
curl http://localhost:8000/api/dashboard/stats

# Check database logs
tail -f logs/database.log
```

**Solutions:**
```python
# Configure database connection
db_config = {
    "host": "localhost",
    "port": 5432,
    "timeout": 10,
    "retry_attempts": 3,
    "connection_pool_size": 10
}
```

### Debug Mode

```python
# Enable detailed system status logging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('system_status')
logger.debug("Detailed system status debugging enabled")
```

## Development Notes

### Testing

```bash
# Run system status tests
pytest tests/modules/system_status/ -v

# Test health endpoints
pytest tests/core/test_health_endpoints.py -v

# Integration tests
pytest tests/integration/test_system_monitoring.py -v
```

### Code Style

```python
# System status monitoring best practices
class SystemMonitor:
    """Monitor system health and performance."""

    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check_health(self) -> dict:
        """Perform comprehensive health check."""
        try:
            # Collect system metrics
            cpu_usage = await self._get_cpu_usage()
            memory_info = await self._get_memory_info()
            disk_usage = await self._get_disk_usage()

            # Validate thresholds
            health_status = self._validate_thresholds(
                cpu_usage, memory_info, disk_usage
            )

            return {
                "status": health_status,
                "cpu_usage": cpu_usage,
                "memory_info": memory_info,
                "disk_usage": disk_usage,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
```

### Contributing

1. **Health Checks**: Add new health check methods to relevant components
2. **Metrics**: Include new metrics in system monitoring
3. **UI Updates**: Update Gradio UI when adding new monitoring features
4. **API Updates**: Document new health endpoints in API reference

## Migration Guide

### From Legacy Monitoring

#### Changes in Health Check API
```python
# Old approach
health_data = get_system_health()

# New approach
from src.core.dynamic_model_manager import DynamicModelManager

manager = DynamicModelManager()
health_data = await manager.get_health_status()
```

#### Updated Monitoring Configuration
```python
# Old config
monitoring_config = {
    "interval": 60,
    "enabled": True
}

# New config
monitoring_config = {
    "health_check_interval": 30,
    "metrics_collection_interval": 60,
    "alert_thresholds": {
        "cpu_percent": 80,
        "memory_percent": 85
    },
    "enabled": True
}
```

## Changelog

### Version 1.0.0
- **Added:** Comprehensive system status monitoring
- **Added:** Gradio UI system status tab
- **Added:** API health check endpoints
- **Added:** Real-time performance metrics
- **Added:** Alert and notification system

---

*Module Version: 1.0.0*
*Last Updated: 2025-10-31*
*API Version: v1*
*Health Check Endpoint: GET /api/models/health*
