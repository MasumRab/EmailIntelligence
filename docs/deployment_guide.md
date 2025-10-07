# EmailIntelligence Deployment Framework

This directory contains deployment configurations and scripts for the EmailIntelligence project. The framework supports multiple deployment environments for agile development.

## Deployment Environments

### 1. Local Development Environment

*   **Purpose:** Enables quick testing and development directly on a developer's local machine.
*   **Key Features:**
    *   Hot-reloading for rapid feedback on code changes.
    *   Direct access to the project's file system.
    *   Simple setup with minimal external dependencies.
    *   Facilitates easy debugging of the Python backend.
*   **Key Files:**
    *   `deployment/local_dev.py`: The primary script for running the local development server. It utilizes `uvicorn` with reload capabilities.
*   **Usage:**
    ```bash
    python deployment/deploy.py local up
    ```

### 2. Docker-based Development Environment

*   **Purpose:** Provides a consistent and reproducible development environment across different machines using Docker.

The Docker-based development environment provides a consistent development experience across different machines.

**Features:**
*   Containerizes backend, frontend, and database services.
*   Utilizes volume mounts for live code changes within containers.
*   Offers an isolated environment that closely mirrors staging and production.
*   Ensures all team members work with an identical development stack.

**Usage:**
```bash
python deployment/deploy.py dev up
```

### 3. Staging Environment

*   **Purpose:** Serves as a pre-production environment for testing changes in a setup that closely mirrors production. It helps catch issues before they reach users.

The staging environment is designed for testing before production deployment.

**Features:**
*   Provides a production-like environment.
*   Includes SSL/TLS support (typically via Nginx).
*   Incorporates performance optimizations similar to production.
*   Features enhanced monitoring and logging.

**Usage:**
```bash
python deployment/deploy.py staging up
```

### 4. Production Environment

*   **Purpose:** The live environment for the application, optimized for performance, security, and reliability to serve end-users.

The production environment is optimized for performance, security, and reliability.

**Features:**
*   Designed for high availability (e.g., multiple service replicas).
*   Implements load balancing for efficient traffic distribution.
*   Integrates advanced monitoring and alerting systems.
*   Employs security hardening measures.
*   Utilizes performance optimizations for fast response times.

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
- `test`: Run tests using the `run_tests.py` script.
  *   **Purpose (from EXISTING_DEPLOYMENT_FRAMEWORKS.md):** Executes tests across different environments.
  *   **Functionality (from EXISTING_DEPLOYMENT_FRAMEWORKS.md):** Supports various types of tests, including unit tests, integration tests, and end-to-end tests.
  This command executes tests within the context of the specified environment's backend service. You can pass arguments directly to `run_tests.py`. For example, to run only unit tests:
  ```bash
  python deployment/deploy.py <environment> test -- --unit
  ```
  (Note the `--` before `--unit`, which is a common convention to separate arguments for the main script from arguments for the sub-script, though it might not be strictly necessary depending on your shell and argument parsing.)
  Refer to `python deployment/run_tests.py --help` for all available test options.
For a comprehensive overview of testing procedures and detailed test cases, please see the [Testing Guide](../deployment/TESTING_GUIDE.md).
- `migrate`: Run database migrations
- `backup`: Backup the database
- `restore`: Restore the database

## Testing

A comprehensive suite of tests is available to ensure the quality and stability of the EmailIntelligence application. Tests can be executed via the `deploy.py` script. For detailed information on the testing strategy, different types of tests, and specific test cases, please refer to our [Testing Guide](../deployment/TESTING_GUIDE.md).

## Auxiliary Scripts and Tools

This section describes additional scripts that support the deployment and development lifecycle.

*   **`deployment/setup_env.py`**:
    *   **Purpose:** Assists in setting up the necessary development environment.
    *   **Functionality:** Handles tasks like installing dependencies and configuring the database for local development.

*   **`deployment/migrate.py`**:
    *   **Purpose:** Manages database schema migrations.
    *   **Functionality:** Supports commands like `generate` (to create new migration scripts), `apply` (to apply pending migrations), `status` (to check migration status), and `rollback` (to revert migrations).
    *(Note: The `deploy.py` script provides a `migrate` command which utilizes this script.)*

*   **`backend/python_backend/metrics.py`**:
    *   **Purpose:** Provides Prometheus metrics for application monitoring.
    *   **Functionality:** Tracks key performance indicators such as request latency, database query performance, and other custom application-specific metrics.

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
- `local_dev.py`: Script for running the local development server (without Docker).
- `extensions.py`, `migrate.py`, `models.py`, `run_tests.py`, `setup_env.py`, `test_stages.py`: Auxiliary Python scripts for deployment, testing, or utility functions.

## Prerequisites

- Python 3.12 or higher
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

    *(Note: For pure local development without Docker, you would typically run the backend and frontend services manually. For example, for a Python backend: `python backend/python_backend/main.py` and for a Node.js frontend: `npm run dev` from within the client directory. Refer to specific service documentation for manual setup details.)*

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
          python-version: '3.12'
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