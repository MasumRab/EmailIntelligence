# EmailIntelligence Deployment Framework

This directory contains deployment configurations and scripts for the EmailIntelligence project. The framework supports multiple deployment environments for agile development.

## Deployment Environments

### 1. Local Development Environment

The local development environment is designed for quick testing and development on your local machine. It provides a simple way to run the Python backend with hot-reloading and debugging.

**Key Features:**
- Hot-reloading for quick development
- Direct access to the file system
- Simple setup with minimal dependencies
- Easy debugging

**Implementation:**
- `deployment/local_dev.py` - Script to run the local development server (Note: ensure this file exists or adjust description)
- Uses `uvicorn` with reload enabled
- Connects to a local PostgreSQL database

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

## Understanding the Configuration

This section explains the core components of the deployment setup.

### Dockerfiles

-   **`Dockerfile.backend`**: This is a multi-stage Dockerfile for the Python backend.
    -   A `base` stage installs common dependencies.
    -   A `development` stage builds upon `base`, includes development tools (like linters, hot-reloading servers), and is used for the `dev` environment.
    -   A `production` stage also builds upon `base` but installs production-grade servers (e.g., Gunicorn) and is optimized for performance. This is used for `staging` and `prod` environments.
    The `deploy.py` script, via Docker Compose, ensures the correct target stage is built and used for each environment.
-   **`Dockerfile.frontend`**: This Dockerfile builds the frontend application, typically for production deployments. For development, the frontend might be served using a Node.js development server directly (as configured in `docker-compose.dev.yml`).

### Docker Compose Setup

The Docker Compose configuration now uses a base file and environment-specific override files:

-   **`docker-compose.yml` (Base File):** Defines common services, networks, and volumes shared across all environments. For example, the `postgres` service definition is usually here. The `backend` service defined here might point to a default stage in `Dockerfile.backend`.
-   **`docker-compose.<env>.yml` (Override Files):**
    -   `docker-compose.dev.yml`: Tailors the setup for development. It overrides services defined in the base file (e.g., to use the `development` stage of `Dockerfile.backend`, mount local code for hot-reloading) and adds development-specific services (e.g., a Node.js dev server for the frontend).
    -   `docker-compose.stag.yml`: Configures the staging environment, typically overriding services to use production-like settings and the `production` stage of `Dockerfile.backend`.
    -   `docker-compose.prod.yml`: Configures the production environment, also using the `production` stage of `Dockerfile.backend` and including production-specific settings for services like Nginx, frontend, and monitoring tools.

When `deploy.py` runs a command for an environment (e.g., `dev`), it effectively uses a command like:
`docker-compose -f deployment/docker-compose.yml -f deployment/docker-compose.dev.yml <command>`
This layering allows for a clean separation of common configurations from environment-specific adjustments.

### NGINX Configurations
The NGINX configurations located in the `nginx/` directory have been refactored. Common settings (like SSL protocols, security headers, basic proxy parameters) are extracted into `common_*.conf` snippet files. Environment-specific files (`production.conf`, `staging.conf`) then include these common snippets and add their own specific directives (e.g., server names, SSL certificate paths, caching rules). This reduces redundancy and improves maintainability.

## Deployment Commands

The deployment script supports the following commands:

- `up`: Start the environment
- `down`: Stop the environment
- `build`: Build the environment
- `logs`: View logs
- `status`: Check status
- `test`: Run tests using the `run_tests.py` script. This command executes tests within the context of the specified environment's backend service. You can pass arguments directly to `run_tests.py`. For example, to run only unit tests:
  ```bash
  python deployment/deploy.py <environment> test -- --unit
  ```
  (Note the `--` before `--unit`, which is a common convention to separate arguments for the main script from arguments for the sub-script, though it might not be strictly necessary depending on your shell and argument parsing.)
  Refer to `python deployment/run_tests.py --help` for all available test options.
For a comprehensive overview of testing procedures and detailed test cases, please see the [Testing Guide](./TESTING_GUIDE.md).
- `migrate`: Run database migrations
- `backup`: Backup the database
- `restore`: Restore the database

## Testing

A comprehensive suite of tests is available to ensure the quality and stability of the EmailIntelligence application. Tests can be executed via the `deploy.py` script. For detailed information on the testing strategy, different types of tests, and specific test cases, please refer to our [Testing Guide](./TESTING_GUIDE.md).

## Directory Structure

- `Dockerfile.backend`: Multi-stage Dockerfile for the Python backend (base, development, production).
- `Dockerfile.frontend`: Dockerfile for the frontend application.
- `docker-compose.yml`: Base Docker Compose configuration, defining common services like databases.
- `docker-compose.dev.yml`: Docker Compose overrides for the development environment.
- `docker-compose.stag.yml`: Docker Compose overrides for the staging environment.
- `docker-compose.prod.yml`: Docker Compose overrides for the production environment.
- `nginx/`: Contains Nginx configurations. These have been refactored to use common snippets (e.g., `common_ssl_settings.conf`, `common_proxy_backend.conf`) included by environment-specific files like `production.conf` and `staging.conf`.
  - `nginx/production.conf`: Nginx configuration for the production environment.
  - `nginx/staging.conf`: Nginx configuration for the staging environment.
  - `nginx/default.conf`: Basic Nginx configuration, potentially for development or as a fallback.
  - `nginx/common_*.conf`: Common configuration snippets shared across environments.
- `monitoring/`: Prometheus and Grafana configurations.
- `deploy.py`: Main deployment script (acts as a wrapper around Docker Compose).
- `extensions.py`, `migrate.py`, `models.py`, `run_tests.py`, `setup_env.py`, `test_stages.py`: Auxiliary Python scripts for deployment, testing, or utility functions.

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

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/EmailIntelligence.git
    cd EmailIntelligence
    ```

2.  **Set up the Docker-based development environment:**
    This is the recommended way to get started for a consistent environment.
    ```bash
    python deployment/deploy.py dev build
    python deployment/deploy.py dev up
    ```

3.  **Access the application (Docker-based dev):**
    - Backend: http://localhost:8000 (or as configured)
    - Frontend: http://localhost:5173 (or as configured)

    *(Note: For pure local development without Docker, you would typically run the backend and frontend services manually. For example, for a Python backend: `python server/main.py` and for a Node.js frontend: `npm run dev` from within the client directory. Refer to specific service documentation for manual setup details.)*

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