# Email Intelligence Platform Troubleshooting Guide

## Overview

This guide helps diagnose and resolve common issues with the Email Intelligence Platform.

## Quick Diagnostics

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### Service Status
```bash
docker-compose ps
```

### Logs
```bash
# Application logs
docker-compose logs app

# All services
docker-compose logs

# Follow logs in real-time
docker-compose logs -f
```

## Common Issues and Solutions

### 1. Application Won't Start

**Symptoms:**
- Container fails to start
- Health check fails
- Port 8000 not accessible

**Solutions:**

1. **Check Dependencies:**
   ```bash
   python -c "import fastapi, uvicorn, gradio; print('Dependencies OK')"
   ```

2. **Verify Configuration:**
   ```bash
   # Check environment variables
   env | grep -E "(DATA_DIR|SECRET_KEY|DATABASE_URL)"

   # Check data directory exists
   ls -la ./data/
   ```

3. **Check Logs:**
   ```bash
   docker-compose logs app | tail -50
   ```

4. **Rebuild Container:**
   ```bash
   docker-compose build --no-cache app
   docker-compose up -d
   ```

### 2. Database Connection Issues

**Symptoms:**
- API returns 500 errors
- "Database connection failed" in logs
- SQLite database file missing/corrupted

**Solutions:**

1. **Check Database File:**
   ```bash
   ls -la ./data/production.db
   ```

2. **Verify Permissions:**
   ```bash
   chmod 644 ./data/production.db
   chown $(whoami):$(whoami) ./data/production.db
   ```

3. **Reset Database:**
   ```bash
   # Backup existing database
   cp ./data/production.db ./data/production.db.backup

   # Remove and restart (will recreate)
   rm ./data/production.db
   docker-compose restart app
   ```

4. **Check Database Integrity:**
   ```bash
   sqlite3 ./data/production.db "PRAGMA integrity_check;"
   ```

### 3. Gmail Integration Problems

**Symptoms:**
- Gmail sync fails
- Authentication errors
- API quota exceeded

**Solutions:**

1. **Verify Credentials:**
   ```bash
   ls -la ./secrets/
   # Should contain: credentials.json, token.json (or token.pickle)
   ```

2. **Refresh Token:**
   ```bash
   # Remove old token to force re-authentication
   rm ./secrets/token.json
   docker-compose restart app
   ```

3. **Check API Quota:**
   ```bash
   # Visit Google Cloud Console
   # APIs & Services > Dashboard > Gmail API > Quotas
   ```

4. **Test Connection:**
   ```bash
   curl http://localhost:8000/api/gmail/performance
   ```

### 4. Rate Limiting Issues

**Symptoms:**
- 429 Too Many Requests errors
- Legitimate requests blocked

**Solutions:**

1. **Check Rate Limits:**
   ```bash
   # Default limits:
   # General: 120/min, burst 20
   # Workflows: 30/min, burst 5
   # Models: 20/min, burst 3
   ```

2. **Monitor Rate Limit Headers:**
   ```bash
   curl -I http://localhost:8000/api/emails
   # Look for: X-RateLimit-*
   ```

3. **Adjust Limits (if needed):**
   ```python
   from src.core.rate_limiter import api_rate_limiter, RateLimitConfig

   # Increase limits for development
   config = RateLimitConfig(requests_per_minute=300, burst_limit=50)
   api_rate_limiter.add_endpoint_limit("/api/emails", config)
   ```

### 5. Performance Issues

**Symptoms:**
- Slow response times
- High CPU/memory usage
- Application becomes unresponsive

**Solutions:**

1. **Check System Resources:**
   ```bash
   # CPU and Memory usage
   docker stats

   # Application metrics
   curl http://localhost:9090/metrics
   ```

2. **Profile Performance:**
   ```python
   from src.core.performance_monitor import performance_monitor

   # Check slow endpoints
   metrics = performance_monitor.get_aggregated_metrics()
   for name, data in metrics.items():
       if data['avg'] > 1.0:  # Over 1 second
           print(f"Slow: {name} - {data['avg']}s avg")
   ```

3. **Optimize Database:**
   ```bash
   # Rebuild indexes
   sqlite3 ./data/production.db "REINDEX; VACUUM;"

   # Check query performance
   sqlite3 ./data/production.db "EXPLAIN QUERY PLAN SELECT * FROM emails LIMIT 50;"
   ```

### 6. Security Violations

**Symptoms:**
- Path traversal warnings in logs
- Security violation audit events
- Access denied errors

**Solutions:**

1. **Check Audit Logs:**
   ```bash
   tail -50 ./logs/audit.log
   ```

2. **Validate Paths:**
   ```python
   from src.core.security import validate_path_safety

   # Test suspicious paths
   test_paths = ["/etc/passwd", "../../../root", "data/../../../etc"]
   for path in test_paths:
       is_safe = validate_path_safety(path)
       print(f"{path}: {'SAFE' if is_safe else 'UNSAFE'}")
   ```

3. **Review Input Validation:**
   - Ensure all user inputs are validated
   - Check file upload paths
   - Verify API parameter sanitization

### 7. Test Suite Issues

**Symptoms:**
- Tests fail to run
- Import errors
- Mock failures

**Solutions:**

1. **Install Test Dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run Specific Tests:**
   ```bash
   # Run basic tests
   pytest tests/test_basic.py -v

   # Run with coverage
   pytest --cov=src --cov-report=html
   ```

3. **Fix Import Issues:**
   ```bash
   # Ensure src is in PYTHONPATH
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

### 8. Deployment Issues

**Symptoms:**
- Docker build fails
- Services don't start
- Network connectivity issues

**Solutions:**

1. **Build Issues:**
   ```bash
   # Clean build
   docker system prune -f
   docker-compose build --no-cache

   # Check build logs
   docker-compose build --progress=plain
   ```

2. **Network Issues:**
   ```bash
   # Check service connectivity
   docker-compose exec app curl -f http://localhost:8000/health

   # Check inter-service communication
   docker-compose exec app nslookup prometheus
   ```

3. **Volume Issues:**
   ```bash
   # Check volume permissions
   ls -la ./data/ ./logs/ ./secrets/

   # Fix permissions
   sudo chown -R 1000:1000 ./data/ ./logs/ ./secrets/
   ```

## Monitoring and Alerting

### Setting Up Alerts

1. **Prometheus Alerts:**
   ```yaml
   # Add to prometheus.yml
   rule_files:
     - "alert_rules.yml"
   ```

2. **Common Alerts:**
   - High error rate (>5%)
   - Slow response times (>2s)
   - Database connection failures
   - Disk space low (<10%)
   - Rate limit violations

### Log Analysis

```bash
# Search for errors
grep "ERROR" ./logs/*.log

# Find security violations
grep "SECURITY_VIOLATION" ./logs/audit.log

# Check rate limiting
grep "RATE_LIMIT_EXCEEDED" ./logs/audit.log
```

## Emergency Procedures

### Complete System Reset

```bash
# Stop all services
docker-compose down -v

# Remove all data (CAUTION!)
rm -rf ./data/* ./logs/* ./secrets/token.json

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# Reinitialize database
docker-compose exec app python -c "
from src.core.database import create_database_manager, DatabaseConfig
import asyncio

async def init():
    config = DatabaseConfig()
    db = await create_database_manager(config)
    print('Database initialized')

asyncio.run(init())
"
```

### Backup Recovery

```bash
# List available backups
./backup.sh list

# Restore from backup
./backup.sh restore ./backups/email_intelligence_20231201_120000.tar.gz

# Verify restoration
docker-compose restart app
curl http://localhost:8000/health
```

## Getting Help

### Debug Information

```bash
# System information
uname -a
docker --version
docker-compose --version

# Application version
git rev-parse HEAD

# Environment
env | grep -E "(DATA_DIR|DATABASE_URL|LOG_LEVEL)"
```

### Support Resources

1. **Documentation:**
   - API Reference: `docs/API_REFERENCE.md`
   - Developer Guide: `docs/DEVELOPER_GUIDE.md`

2. **Logs:**
   - Application: `./logs/app.log`
   - Audit: `./logs/audit.log`
   - Performance: `./logs/performance_metrics.jsonl`

3. **Monitoring:**
   - Grafana: http://localhost:3000
   - Prometheus: http://localhost:9090

### Escalation

If issues persist:
1. Check recent commits for breaking changes
2. Review configuration files
3. Test with minimal setup
4. Consider rolling back to previous version</content>
</xai:function_call: <parameter name="path">/home/masum/github/EmailIntelligence/docs/TROUBLESHOOTING.md
