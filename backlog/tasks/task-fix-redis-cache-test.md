---
epic: "[[Testing and Quality Assurance]]"
priority: High
status: To Do
---
# Task: Fix Failing Redis Cache Test `test_redis_basic_operations`

## Description

The test `test_redis_basic_operations` in `tests/core/test_caching.py` is currently failing with an `AssertionError`. This test is critical for ensuring that the Redis cache backend is working correctly.

The core of the issue is that the test is unable to connect to Redis. This is because a Redis server is not available in the test environment.

## Acceptance Criteria

-   The `test_redis_basic_operations` test is un-skipped.
-   The test is able to connect to a Redis server.
-   All tests in `tests/core/test_caching.py` pass.
