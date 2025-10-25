Note: This branch of the application has been configured to use SQLite. PostgreSQL-specific sections in the main [Deployment Guide](../../docs/deployment_guide.md) may not apply directly or will require adaptation for an SQLite environment.

# Deployment

This directory contains configurations and scripts related to deploying the EmailIntelligence application.

## Overview

The deployment strategy for EmailIntelligence supports various environments:
-   **Local Development:** Using local Python and Node.js (for the frontend) and optionally Docker for other services.
-   **Dockerized Local Environment:** Running the entire application stack (frontend, Python backend) in Docker containers locally.
-   **Staging Environment:** A Dockerized environment configured for staging/testing.
-   **Production Environment:** A Dockerized environment configured for production deployment.

## Key Files and Directories

-   **`Dockerfile.backend`**: Dockerfile for building the Python FastAPI backend application.
-   **`Dockerfile.frontend`**: Dockerfile for building the React frontend application.
-   **`docker-compose.yml`**: Base Docker Compose file for services.
-   **`docker-compose.dev.yml`**: Docker Compose overrides for local development.
-   **`docker-compose.prod.yml`**: Docker Compose overrides for production.
-   **`deploy.py`**: Python script for managing deployments across different environments.
-   **`nginx/`**: Nginx configurations for reverse proxy, SSL termination, etc.
-   **`monitoring/`**: Configurations for monitoring tools (e.g., Prometheus, Grafana).
-   **`setup_env.py`**: Python script to help set up `.env` files with default configurations.
-   **`run_tests.py`**: Python script for running automated tests.

## Deployment Environments

### 1. Local Development (Non-Dockerized)

-   Run frontend and backend servers directly on the host machine.
-   Requires local installation of Node.js and Python.
-   Typically managed via `launch.py --stage dev` as described in the main [README.md](../../README.md) and [Launcher Guide](../../docs/launcher_guide.md).

### 2. Dockerized Local Environment

-   Uses Docker Compose to run all services in containers.
-   Simplifies dependency management and environment consistency.
-   Managed by `python deployment/deploy.py dev <command>`.

### 3. Staging Environment

-   A pre-production environment that mirrors production as closely as possible.
-   Deployed using Docker Compose with staging-specific configurations (`docker-compose.stag.yml`).
-   Typically involves building production-like Docker images.
-   Managed by `python deployment/deploy.py stag <command>`.

### 4. Production Environment

-   Live environment for end-users.
-   Deployed using Docker Compose with production-hardened configurations (`docker-compose.prod.yml`).
-   Involves building optimized Docker images, secure configurations, and robust monitoring.
-   Managed by `python deployment/deploy.py prod <command>`.

## General Deployment Workflow (using `deploy.py`)

Use the `deployment/deploy.py` script to manage your Docker deployments. It supports `dev`, `stag`, and `prod` environments.

1.  **Build Images:**
    ```bash
    python deployment/deploy.py <environment> build
    # Example: python deployment/deploy.py prod build
    ```
2.  **Start Services:**
    ```bash
    python deployment/deploy.py <environment> up
    # Example: python deployment/deploy.py dev up -d
    ```
3.  **Stop Services:**
    ```bash
    python deployment/deploy.py <environment> down
    ```
4.  **View Logs:**
    ```bash
    python deployment/deploy.py <environment> logs
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
