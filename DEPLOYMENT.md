# EmailIntelligence Deployment Frameworks

This document provides an overview of the deployment frameworks created for the EmailIntelligence project. These frameworks enable agile development by supporting multiple environments with different configurations.

## Overview

We've created four deployment frameworks:

1. **Local Development Environment** - For quick testing and development
2. **Docker-based Development** - For consistent development environments
3. **Staging Environment** - For testing before production
4. **Production Deployment** - For the final deployment

Each framework is designed to support the specific needs of its environment while maintaining consistency across environments.

## Deployment Frameworks

### 1. Local Development Environment

The local development environment is designed for quick testing and development on your local machine. It provides a simple way to run the Python backend with hot-reloading and debugging.

**Key Features:**
- Hot-reloading for quick development
- Direct access to the file system
- Simple setup with minimal dependencies
- Easy debugging

**Implementation:**
- `deployment/local_dev.py` - Script to run the local development server
- Uses `uvicorn` with reload enabled
- Connects to a local PostgreSQL database

**Usage:**
```bash
python deployment/deploy.py local up
```

### 2. Docker-based Development Environment

The Docker-based development environment provides a consistent development experience across different machines. It uses Docker Compose to run the backend, frontend, and database services.

**Key Features:**
- Containerized services (backend, frontend, database)
- Volume mounts for live code changes
- Isolated environment that matches production
- Consistent environment across team members

**Implementation:**
- `deployment/Dockerfile.backend` - Multi-stage Dockerfile for the backend (development stage used)
- `deployment/Dockerfile.frontend` - Dockerfile for the frontend (if applicable for this environment, or note if dev server is used)
- `deployment/docker-compose.yml` - Base Docker Compose configuration
- `deployment/docker-compose.dev.yml` - Docker Compose overrides for development
- Volume mounts for code changes
This setup uses a base configuration file with environment-specific overrides for clarity and maintainability.

**Usage:**
```bash
python deployment/deploy.py dev up
```

### 3. Staging Environment

The staging environment is designed for testing before production deployment. It provides a production-like environment with additional monitoring and security features.

**Key Features:**
- Production-like environment
- SSL/TLS support
- Performance optimizations
- Monitoring and logging

**Implementation:**
- `deployment/Dockerfile.backend` - Multi-stage Dockerfile for the backend (production stage used)
- `deployment/Dockerfile.frontend` - Dockerfile for the frontend
- `deployment/docker-compose.yml` - Base Docker Compose configuration
- `deployment/docker-compose.stag.yml` - Docker Compose overrides for staging
- `deployment/nginx/staging.conf` - Nginx configuration for SSL/TLS

**Usage:**
```bash
python deployment/deploy.py staging up
```

### 4. Production Environment

The production environment is optimized for performance, security, and reliability. It includes advanced features like load balancing, monitoring, and high availability.

**Key Features:**
- High availability with multiple replicas
- Load balancing
- Monitoring and alerting
- Security hardening
- Performance optimizations

**Implementation:**
- `deployment/Dockerfile.backend` - Multi-stage Dockerfile for the backend (production stage used)
- `deployment/Dockerfile.frontend` - Dockerfile for the frontend
- `deployment/docker-compose.yml` - Base Docker Compose configuration
- `deployment/docker-compose.prod.yml` - Docker Compose overrides for production
- `deployment/nginx/production.conf` - Nginx configuration for SSL/TLS
- `deployment/monitoring/` - Prometheus and Grafana configurations

**Usage:**
```bash
python deployment/deploy.py prod up
```

## Additional Tools

We've also created several tools to help with deployment and development:

1. **Deployment Script** - `deployment/deploy.py`
   - Manages deployment across different environments
   - Supports commands like up, down, build, logs, status, etc.

2. **Environment Setup Script** - `deployment/setup_env.py`
   - Sets up the development environment
   - Installs dependencies and configures the database

3. **Migration Script** - `deployment/migrate.py`
   - Manages database migrations
   - Supports commands like generate, apply, status, rollback

4. **Test Runner Script** - `deployment/run_tests.py`
   - Runs tests across different environments
   - Supports unit tests, integration tests, and end-to-end tests

5. **Metrics Module** - `server/python_backend/metrics.py`
   - Provides Prometheus metrics for monitoring
   - Tracks request latency, database queries, and application-specific metrics

## Continuous Integration/Continuous Deployment (CI/CD)

The deployment frameworks are designed to work with CI/CD pipelines. You can use the deployment script in your pipeline to automate the deployment process.

Example GitHub Actions workflow:
```yaml
name: Deploy to Staging

on:
  push:
    branches: [ staging ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Deploy to staging
        run: |
          python deployment/deploy.py staging build
          python deployment/deploy.py staging up
```

## Conclusion

These deployment frameworks provide a solid foundation for agile development of the EmailIntelligence project. They support the entire development lifecycle, from local development to production deployment, with consistent environments and tools.

For more detailed information, see the README file in the `deployment` directory.