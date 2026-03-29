# Dependency Management and Troubleshooting Guide

This document provides guidance on managing Python dependencies, troubleshooting common import errors, and best practices to maintain a stable development environment.

## 1. Common Import Errors and Their Causes

### 1.1 `ModuleNotFoundError: No module named 'some_module'`
*   **Cause:** The required package is not installed in the active Python environment, or the package name in the import statement is incorrect.
*   **Resolution:**
    *   Ensure your virtual environment is activated.
    *   Install the missing package using `pip install some_module` or `uv pip install some_module`.
    *   Verify the package name is correct.

### 1.2 `AttributeError: module 'some_module' has no attribute 'some_attribute'`
*   **Cause:** This often indicates a version incompatibility. A function, class, or variable that your code expects might have been removed, renamed, or changed in a newer (or older) version of the installed package.
*   **Example: NLTK `DownloadError` Issue**
    *   **Problem:** In some NLTK versions (e.g., >3.6.5), `nltk.downloader.DownloadError` was removed, leading to `AttributeError` when code tried to access it.
    *   **Resolution:** Pin the NLTK version to `3.6.5` in `requirements.txt` or `uv.lock` to ensure compatibility.
*   **Resolution:**
    *   Check the documentation of the package for changes in the API.
    *   Review `requirements.txt` or `uv.lock` for pinned versions. If the error occurs after an update, try reverting to a previous working version.
    *   Use `pip show some_module` to check the installed version and compare it with the expected version.

### 1.3 `ImportError: cannot import name 'some_name' from 'some_module'`
*   **Cause:** Similar to `AttributeError`, this usually means `some_name` is not available in `some_module` for the installed version, or there's a circular import dependency.
*   **Resolution:**
    *   Verify the spelling of `some_name` and `some_module`.
    *   Check package documentation for API changes.
    *   Inspect for circular imports if the issue is not version-related.

## 2. Dependency Management Best Practices

### 2.1 Use Virtual Environments
Always work within a virtual environment (`venv` or `conda`). This isolates your project's dependencies from your system's Python installation and other projects, preventing conflicts.

*   **Activation:**
    *   `source venv/bin/activate` (Linux/macOS)
    *   `.\venv\Scripts\activate` (Windows PowerShell)
    *   `venv\Scripts\activate.bat` (Windows Command Prompt)

### 2.2 Pin Dependencies
Use `requirements.txt` or `uv.lock` to explicitly pin the versions of all your project's dependencies. This ensures reproducibility across different environments.

*   **Generating `requirements.txt`:** `pip freeze > requirements.txt`
*   **Using `uv.lock`:** `uv pip compile -o uv.lock requirements.in` (assuming you have a `requirements.in` file)

### 2.3 Regular Updates (with caution)
Periodically update your dependencies to benefit from bug fixes and new features, but do so cautiously. Always test thoroughly after updating.

*   `uv pip install --upgrade -r requirements.txt`
*   `uv pip install --upgrade -e .[dev]` (for editable installs with dev dependencies)

### 2.4 NLTK Data Management
If your project uses NLTK, ensure that necessary NLTK data (e.g., 'punkt', 'stopwords') is downloaded. The `setup/environment.py` script handles this automatically.

## 3. Troubleshooting Workflow

1.  **Activate Virtual Environment:** Always start by ensuring your correct virtual environment is activated.
2.  **Check Error Message:** Read the full traceback carefully. The error message (e.g., `ModuleNotFoundError`, `AttributeError`) and the line number are crucial.
3.  **Verify Installation:** Use `pip list` or `uv pip list` to see installed packages and their versions. Compare with `requirements.txt` or `uv.lock`.
4.  **Reinstall Dependencies:** If in doubt, try reinstalling dependencies:
    *   `rm -rf venv` (to remove existing venv)
    *   `python launch.py setup` (to recreate venv and reinstall dependencies)
5.  **Consult Documentation:** If a specific `AttributeError` or `ImportError` persists, check the official documentation of the problematic library for breaking changes in recent versions.
6.  **Check `setup/validation.py`:** The `launch.py` script includes environment validation checks. If these checks fail, address the reported issues.

By following these guidelines, you can minimize dependency-related issues and streamline your development process.
