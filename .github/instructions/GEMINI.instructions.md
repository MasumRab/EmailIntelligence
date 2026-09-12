---
description: ''
applyTo: '**/*'
---
# Additional Conventions Beyond the Built-in Functions

As this project's AI coding tool, you must follow the additional conventions below, in addition to the built-in functions.

# Project Overview

## General Guidelines

- Use Python 3.11+ for backend, orchestration, and script changes; use TypeScript for the React client
- Follow consistent naming conventions
- Write self-documenting code with clear variable and function names
- Prefer composition over inheritance
- Use meaningful comments for complex business logic

## Code Style

- Python: follow Black formatting, 100 char line length, and type-hinted function signatures
- TypeScript: use 2 spaces, semicolons, and double quotes

## Architecture Principles

- Keep backend work aligned with the FastAPI/Python modules and frontend work aligned with `client/`
- Keep related files close together
- Use dependency injection for better testability
- Implement proper error handling
- Follow single responsibility principle
