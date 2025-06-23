Note: This branch of the application has been configured to use SQLite. PostgreSQL-specific sections in the main [Deployment Guide](../../docs/deployment_guide.md) may not apply directly or will require adaptation for an SQLite environment.

# Deployment

This directory contains configurations and scripts related to deploying the EmailIntelligence application.

## Overview

The deployment strategy for EmailIntelligence supports various environments:
-   **Local Development:** Using local Node.js, Python, and optionally Docker for services like PostgreSQL.
-   **Dockerized Local Environment:** Running the entire application stack (frontend, Node.js backend, Python backend, PostgreSQL) in Docker containers locally.
-   **Staging Environment:** A Dockerized environment configured for staging/testing.
-   **Production Environment:** A Dockerized environment configured for production deployment.

## Key Files and Directories

-   **`Dockerfile.frontend`**: Dockerfile for building the frontend application.
-   **`Dockerfile.backend`**: Dockerfile for building the Python FastAPI backend application.
-   **`docker-compose.yml`**: Base Docker Compose file for services.
-   **`docker-compose.dev.yml`**: Docker Compose overrides for local development.
-   **`docker-compose.stag.yml`**: Docker Compose overrides for staging.
-   **`docker-compose.prod.yml`**: Docker Compose overrides for production.
-   **`nginx/`**: Nginx configurations for reverse proxy, SSL termination, etc.
    -   `nginx/default.conf`: Base Nginx configuration (often for development).
    -   `nginx/production.conf`: Nginx configuration for production.
    -   `nginx/staging.conf`: Nginx configuration for staging.
    -   Other common Nginx config snippets (`common_*.conf`).
-   **`monitoring/`**: Configurations for monitoring tools (e.g., Prometheus, Grafana).
    -   `monitoring/prometheus.yml`: Prometheus configuration.
    -   `monitoring/grafana/provisioning/`: Grafana provisioning for dashboards and datasources.
-   **`deploy.py`**: Python script for managing deployments across different environments (local, Docker, staging, production). This script often wraps Docker Compose commands and other deployment tasks. (This file is not present in the current file listing but is a common pattern).
-   **`migrate.py`**: Python script for handling database migrations, typically using Drizzle ORM. (This file is not present but often part of such a setup).
-   **`setup_env.py`**: Python script to help set up `.env` files with default configurations.
-   **`run_tests.py`**: Python script for running automated tests, potentially across different parts of the application or in specific environments.
-   **`TESTING_GUIDE.md`**: Detailed guide on testing procedures and strategies.
-   **`TEST_CASES*.md`**: Documents detailing various test cases for different parts of the application.

## Deployment Environments

### 1. Local Development (Non-Dockerized)

-   Run frontend and backend servers directly on the host machine.
-   Requires local installation of Node.js, Python, and PostgreSQL (or connection to a remote instance).
-   Typically managed via `launch.py --stage dev` as described in the main [README.md](../../README.md) and [Launcher Guide](../../docs/launcher_guide.md).

### 2. Dockerized Local Environment

-   Uses Docker Compose to run all services in containers.
-   Simplifies dependency management and environment consistency.
-   Often managed by `python deployment/deploy.py local up` (if `deploy.py` exists and is configured for this).
-   Alternatively, direct `docker-compose -f deployment/docker-compose.yml -f deployment/docker-compose.dev.yml up` can be used.

### 3. Staging Environment

-   A pre-production environment that mirrors production as closely as possible.
-   Deployed using Docker Compose with staging-specific configurations (`docker-compose.stag.yml`).
-   Typically involves building production-like Docker images.
-   Managed by `python deployment/deploy.py stag up` (or similar `deploy.py` command).

### 4. Production Environment

-   Live environment for end-users.
-   Deployed using Docker Compose with production-hardened configurations (`docker-compose.prod.yml`).
-   Involves building optimized Docker images, secure configurations, and robust monitoring.
-   Managed by `python deployment/deploy.py prod up` (or similar `deploy.py` command).

## General Deployment Workflow (using `deploy.py` if available)

While a `deploy.py` script is not explicitly listed in the current file structure, a typical workflow using such a script (or manual Docker Compose commands) would be:

1.  **Build Images:**
    ```bash
    python deployment/deploy.py <environment> build
    # Example: python deployment/deploy.py prod build
    # Or manually: docker-compose -f ... build
    ```
2.  **Apply Database Migrations (if applicable):**
    ```bash
    python deployment/deploy.py <environment> migrate
    # Example: python deployment/deploy.py prod migrate
    # This would typically run `npm run db:push` or similar inside the appropriate container.
    ```
3.  **Start Services:**
    ```bash
    python deployment/deploy.py <environment> up
    # Example: python deployment/deploy.py prod up -d (for detached mode)
    # Or manually: docker-compose -f ... up -d
    ```
4.  **View Logs:**
    ```bash
    python deployment/deploy.py <environment> logs
    # Or manually: docker-compose -f ... logs -f
    ```
5.  **Stop Services:**
    ```bash
    python deployment/deploy.py <environment> down
    # Or manually: docker-compose -f ... down
    ```

## Configuration Management

-   Environment variables are crucial for configuring the application in different environments.
-   Base configurations might be in `.env` (gitignored) or directly in Docker Compose files.
-   Production and staging environments should use secure methods for managing secrets (e.g., Docker secrets, environment variables injected by CI/CD or orchestration platform).

## Nginx Reverse Proxy

-   Nginx is used as a reverse proxy in staging and production environments.
-   Handles SSL termination, serves static frontend assets, and routes API requests to the appropriate backend services.
-   Configuration files are located in `nginx/`.

## Monitoring

-   Prometheus and Grafana are set up for monitoring application metrics and performance.
-   Prometheus scrapes metrics from backend services.
-   Grafana provides dashboards for visualizing these metrics.
-   Configurations are in `monitoring/`.

For more detailed instructions, refer to the main [Deployment Guide](../../docs/deployment_guide.md). The `deploy.py` script (if implemented) would also contain its own usage instructions (`python deployment/deploy.py --help`).
