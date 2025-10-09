# Tools Used

This document lists the tools used during the audit of the `sqlite` branch.

## Standard System Tools
- `git`: Used for version control, specifically for checking out the `sqlite` branch.
- `ls` (via `list_files`): Used to list files and directories to explore the codebase.
- `cat` (via `read_file`): Used to read the contents of files.

## Python Tools
- `poetry`: Used in an attempt to manage Python dependencies and run the test suite. The audit revealed significant issues with the project's Poetry setup.
- `pip`: Used as an alternative to Poetry to install Python dependencies from `requirements-dev.txt` and to install missing packages individually.
- `pytest`: Used to attempt to run the project's test suite. The audit revealed that the test suite was un-runnable due to missing dependencies and an improper `PYTHONPATH` configuration.

## Static Analysis
- Manual code review was performed on key files such as `server/db.ts`, `drizzle.config.ts`, `tests/test_database.py`, `pyproject.toml`, `requirements.txt`, and `requirements-dev.txt` to understand the state of the `sqlite` migration and the project's dependency management.