# EmailIntelligence Testing Guide

This document provides an overview of the testing strategies and processes for the EmailIntelligence project. It serves as a central point for accessing detailed test case documentation.

## Overview

Our testing approach encompasses various levels to ensure the quality, reliability, and security of the EmailIntelligence application across different deployment environments. This includes unit tests, integration tests, API tests, end-to-end (E2E) tests, performance tests, and security scans.

The `deployment/deploy.py` script now integrates test execution capabilities, allowing tests to be run conveniently against specific environments.

## Test Execution

Tests are primarily run using the `deployment/deploy.py` script or directly via `deployment/run_tests.py`.

### Using `deploy.py`

The `deploy.py` script provides a `test` command that executes the `run_tests.py` script within the context of the specified Docker environment (dev, staging).

**General command:**
```bash
python deployment/deploy.py <environment> test [test_options]
```

**Examples:**
- Run all default tests (usually unit tests) in the `dev` environment:
  ```bash
  python deployment/deploy.py dev test
  ```
- Run only unit tests with coverage in the `dev` environment:
  ```bash
  python deployment/deploy.py dev test -- --unit --coverage
  ```
- Run E2E tests against the `staging` environment:
  ```bash
  python deployment/deploy.py staging test -- --e2e
  ```

(Note the `--` used to separate arguments for `deploy.py` from arguments intended for `run_tests.py`.)

Refer to the `run_tests.py` script's help for all available test options:
```bash
python deployment/run_tests.py --help
```

### Direct Execution with `run_tests.py`

For more direct control or specific scenarios, you can execute the `run_tests.py` script:
```bash
python deployment/run_tests.py [options]
```
This script handles the execution of different test suites like unit, integration, API, E2E, performance, and security tests.

## Detailed Test Cases

For specific test cases related to different aspects of the system, please refer to the following documents:

*   **[Test Cases for `deploy.py`](./TEST_CASES.md):** Verifies the functionality of the main deployment script (`deploy.py`) across various commands and environments.
*   **[Test Cases for Environment Parity and Configuration](./TEST_CASES_ENV_PARITY_CONFIG.md):** Focuses on ensuring consistency and correct configuration between staging and production environments.
*   **[Test Cases for Nginx Configuration](./TEST_CASES_NGINX.md):** Details tests for Nginx setup, including proxying, SSL/TLS, security headers, and static content.
*   **[Test Cases for Supporting Services](./TEST_CASES_SUPPORTING_SERVICES.md):** Covers tests for backend services like databases (connectivity, migrations) and other core processes.
*   **[Test Cases for `test_stages.py`](./TEST_CASES_TEST_STAGES.md):** Outlines tests for the `test_stages.py` script, which is orchestrated by `run_tests.py` for different test types.

## Test Types Overview

*   **Unit Tests:** Verify individual components or functions in isolation. Located in `tests/`.
*   **Integration Tests:** Test the interaction between different components or services. Located in `tests/integration/`.
*   **API Tests:** Validate the application's API endpoints. Located in `tests/api/`.
*   **End-to-End (E2E) Tests:** Simulate user scenarios and test the application flow from the user interface to the backend. Located in `tests/e2e/`.
*   **Performance Tests:** Measure the responsiveness, stability, and scalability of the application under load. Located in `tests/performance/`.
*   **Security Tests:** Identify potential vulnerabilities in the application. Located in `tests/security/`.

Regularly running these tests helps maintain code quality and ensure reliable deployments.
