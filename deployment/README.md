# EmailIntelligence Deployment Framework

This directory contains deployment configurations and scripts for the EmailIntelligence project. The framework supports multiple deployment environments for agile development.

## Deployment Environments

### 1. Local Development Environment

The local development environment is designed for quick testing and development on your local machine.

**Features:**
- Hot-reloading for quick development
- Direct access to the file system
- Simple setup with minimal dependencies

**Usage:**
```bash
python deployment/deploy.py local up
```

### 2. Docker-based Development Environment

The Docker-based development environment provides a consistent development experience across different machines.

**Features:**
- Containerized services (backend, frontend, database)
- Volume mounts for live code changes
- Isolated environment that matches production

**Usage:**
```bash
python deployment/deploy.py dev up
```

### 3. Staging Environment

The staging environment is designed for testing before production deployment.

**Features:**
- Production-like environment
- SSL/TLS support
- Performance optimizations

**Usage:**
```bash
python deployment/deploy.py staging up
```

### 4. Production Environment

The production environment is optimized for performance, security, and reliability.

**Features:**
- High availability with multiple replicas
- Load balancing
- Monitoring and alerting
- Security hardening

**Usage:**
```bash
python deployment/deploy.py prod up
```

## Deployment Commands

The deployment script supports the following commands:

- `up`: Start the environment
- `down`: Stop the environment
- `build`: Build the environment
- `logs`: View logs
- `status`: Check status
- `test`: Run tests
- `migrate`: Run database migrations
- `backup`: Backup the database
- `restore`: Restore the database

## Directory Structure

- `Dockerfile.dev`: Docker configuration for development
- `Dockerfile.staging`: Docker configuration for staging
- `Dockerfile.production`: Docker configuration for production
- `Dockerfile.frontend`: Docker configuration for the frontend
- `docker-compose.dev.yml`: Docker Compose configuration for development
- `docker-compose.staging.yml`: Docker Compose configuration for staging
- `docker-compose.production.yml`: Docker Compose configuration for production
- `nginx/`: Nginx configurations for different environments
- `monitoring/`: Prometheus and Grafana configurations
- `deploy.py`: Deployment script
- `local_dev.py`: Local development server script

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized environments)
- PostgreSQL (for local development)
- Node.js and npm (for frontend development)

## Environment Variables

The following environment variables are used by the deployment framework:

- `DATABASE_URL`: PostgreSQL connection string
- `NODE_ENV`: Environment name (development, staging, production)
- `PORT`: Port for the backend server
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name
- `GRAFANA_PASSWORD`: Grafana admin password

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EmailIntelligence.git
   cd EmailIntelligence
   ```

2. Set up the local development environment:
   ```bash
   python deployment/deploy.py local build
   python deployment/deploy.py local up
   ```

3. Access the application:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:5173

## Continuous Integration/Continuous Deployment (CI/CD)

For CI/CD, you can use the deployment script in your pipeline:

```yaml
# Example GitHub Actions workflow
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

## Troubleshooting

If you encounter issues with the deployment, check the logs:

```bash
python deployment/deploy.py <environment> logs
```

For database issues, you can try resetting the database:

```bash
python deployment/deploy.py <environment> down
# Delete the volume if needed (Docker environments only)
docker volume rm emailintelligence_postgres_data
python deployment/deploy.py <environment> up
```