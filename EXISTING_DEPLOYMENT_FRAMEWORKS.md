# Existing Deployment Frameworks

This document outlines the deployment frameworks currently utilized within the EmailIntelligence project.

## 1. Local Development Environment

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

## 2. Docker-based Development Environment

*   **Purpose:** Provides a consistent and reproducible development environment across different machines using Docker.
*   **Key Features:**
    *   Containerizes backend, frontend, and database services.
    *   Utilizes volume mounts to reflect live code changes within containers.
    *   Offers an isolated environment that closely mirrors the staging and production setups.
    *   Ensures all team members work with an identical development stack.
*   **Key Files:**
    *   `deployment/Dockerfile.dev`: Docker configuration specific to the backend development environment.
    *   `deployment/docker-compose.dev.yml`: Docker Compose file defining and managing the multi-container setup.
*   **Usage:**
    ```bash
    python deployment/deploy.py dev up
    ```

## 3. Staging Environment

*   **Purpose:** Serves as a pre-production environment for testing changes in a setup that closely mirrors production. It helps catch issues before they reach users.
*   **Key Features:**
    *   Provides a production-like environment.
    *   Includes SSL/TLS support for secure connections, typically managed by Nginx.
    *   Incorporates performance optimizations similar to production.
    *   Features enhanced monitoring and logging to track application behavior and diagnose problems.
*   **Key Files:**
    *   `deployment/Dockerfile.staging`: Docker configuration for the backend in the staging environment.
    *   `deployment/docker-compose.staging.yml`: Docker Compose file for the staging environment.
    *   `deployment/nginx/staging.conf`: Nginx configuration specific to staging, handling SSL/TLS and request proxying.
*   **Usage:**
    ```bash
    python deployment/deploy.py staging up
    ```

## 4. Production Environment

*   **Purpose:** The live environment for the application, optimized for performance, security, and reliability to serve end-users.
*   **Key Features:**
    *   Designed for high availability, potentially using multiple replicas of services.
    *   Implements load balancing to distribute traffic efficiently.
    *   Integrates advanced monitoring and alerting systems.
    *   Employs security hardening measures to protect against threats.
    *   Utilizes performance optimizations for fast response times.
*   **Key Files:**
    *   `deployment/Dockerfile.production`: Docker configuration for the backend in the production environment.
    *   `deployment/docker-compose.production.yml`: Docker Compose file for the production environment.
    *   `deployment/nginx/production.conf`: Nginx configuration for production, handling SSL/TLS, load balancing, and serving static assets.
    *   `deployment/monitoring/prometheus.yml`: Configuration for Prometheus, used for monitoring system metrics and application-specific metrics.
*   **Usage:**
    ```bash
    python deployment/deploy.py prod up
    ```

## 5. Additional Deployment Tools

Beyond the environment-specific frameworks, several scripts and modules support the deployment and development lifecycle:

*   **`deployment/deploy.py`**:
    *   **Purpose:** A centralized script for managing deployments across all defined environments (local, dev, staging, prod).
    *   **Functionality:** Supports commands such as `up`, `down`, `build`, `logs`, `status`, `test`, `migrate`, `backup`, and `restore`.

*   **`deployment/setup_env.py`**:
    *   **Purpose:** Assists in setting up the necessary development environment.
    *   **Functionality:** Handles tasks like installing dependencies and configuring the database for local development.

*   **`deployment/migrate.py`**:
    *   **Purpose:** Manages database schema migrations.
    *   **Functionality:** Supports commands like `generate` (to create new migration scripts), `apply` (to apply pending migrations), `status` (to check migration status), and `rollback` (to revert migrations).

*   **`deployment/run_tests.py`**:
    *   **Purpose:** Executes tests across different environments.
    *   **Functionality:** Supports various types of tests, including unit tests, integration tests, and end-to-end tests.

*   **`server/python_backend/metrics.py`**:
    *   **Purpose:** Provides Prometheus metrics for application monitoring.
    *   **Functionality:** Tracks key performance indicators such as request latency, database query performance, and other custom application-specific metrics.
