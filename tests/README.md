# EmailIntelligence Tests

This directory contains tests for the EmailIntelligence application. The testing framework supports various types of tests, including unit tests, integration tests, and end-to-end tests.

## Test Files

- **test_nlp_engine.py**: Tests for the NLP engine functionality
- **test_smart_filters.py**: Tests for the smart filtering functionality

## Running Tests

You can run tests using the unified launcher:

```bash
# Run all tests
python launch.py --unit

# Run tests with coverage report
python launch.py --unit --coverage

# Run specific test types
python launch.py --integration
python launch.py --e2e
python launch.py --performance
python launch.py --security
```

Or you can run tests directly using pytest:

```bash
# Run all tests
pytest tests/

# Run a specific test file
pytest tests/test_nlp_engine.py

# Run tests with coverage
pytest tests/ --cov=server
```

## Writing Tests

When writing tests, follow these guidelines:

1. **Naming**: Test files should be named `test_*.py` and test functions should be named `test_*`
2. **Organization**: Group related tests in the same file
3. **Fixtures**: Use pytest fixtures for setup and teardown
4. **Mocking**: Use mocks for external dependencies
5. **Assertions**: Use descriptive assertions with clear error messages

Example test:

```python
import pytest
from server.python_nlp.nlp_engine import NLPEngine

def test_sentiment_analysis():
    # Arrange
    engine = NLPEngine()
    text = "I love this application!"
    
    # Act
    result = engine.analyze_sentiment(text)
    
    # Assert
    assert result["sentiment"] == "positive"
    assert result["confidence"] > 0.8
```

## API Test Coverage

Comprehensive API tests have been implemented for the Python FastAPI backend (`server/python_backend/main.py`).
These tests cover the following endpoint categories:
- Dashboard and Health Checks (`tests/test_dashboard_api.py`, `tests/test_health_check_api.py`)
- Email Management (CRUD operations) (`tests/test_email_api.py`)
- Category Management (`tests/test_category_api.py`)
- Gmail Integration (sync, smart retrieval, strategies, performance) (`tests/test_gmail_api.py`)
- Smart Filters (CRUD, generation, pruning) (`tests/test_filter_api.py`)
- Action Item Extraction (`tests/test_api_actions.py`)

These tests utilize `fastapi.testclient.TestClient` and `unittest.mock` to ensure robust testing of API behavior, including success cases, error handling, and validation.

## Test Coverage

The project aims for high test coverage, especially for critical components like the NLP engine and smart filters. Use the coverage report to identify areas that need more testing:

```bash
python launch.py --unit --coverage
```

## Continuous Integration

Tests are automatically run in the CI/CD pipeline for every pull request and merge to the main branch. The pipeline will fail if any tests fail or if the coverage drops below the threshold.

## Test Data

Test data is stored in the `tests/data` directory. This includes sample emails, expected outputs, and other test fixtures.

## End-to-End Testing

End-to-end tests simulate real user interactions with the application. These tests use a headless browser to interact with the frontend and verify that the entire application works correctly.

To run end-to-end tests:

```bash
python launch.py --e2e
```