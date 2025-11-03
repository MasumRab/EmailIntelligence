---
epic: "[[Testing and Quality Assurance]]"
priority: High
status: To Do
---
# Task: Fix Failing App Startup Test `test_app_startup`

## Description

The test `test_app_startup` in `tests/core/test_app.py` is currently failing with a `404 Not Found` error. This test is critical for ensuring that the main application starts up correctly and the Gradio UI is mounted.

The core of the issue is that the `/ui` endpoint is not available in the test environment. This is likely because the Gradio UI is not being mounted correctly when the application is created for testing.

## Acceptance Criteria

-   The `test_app_startup` test is un-skipped.
-   The test is able to access the `/ui` endpoint and verify that the Gradio UI is mounted.
-   All tests in `tests/core/test_app.py` pass.
