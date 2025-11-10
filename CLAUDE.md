# Project Overview

## Agent Context Control System

This project implements an AI agent context control system to prevent context contamination across development branches. The system automatically detects the current Git branch and applies appropriate access controls and environment settings.

### Branch-Specific Access Control

- **orchestration-tools**: Full access to orchestration scripts, infrastructure tools, and system management
- **main**: Core application development with restricted access to orchestration tooling
- **scientific**: AI/research focused with access to analysis tools and experimental features

### Context Validation

Always run context validation before making changes:

```bash
./scripts/context-control --validate
```

This ensures you're working within the appropriate boundaries for the current branch.

## General Guidelines

- Use TypeScript for all new code
- Follow consistent naming conventions
- Write self-documenting code with clear variable and function names
- Prefer composition over inheritance
- Use meaningful comments for complex business logic

## Code Style

- Use 2 spaces for indentation
- Use semicolons
- Use double quotes for strings
- Use trailing commas in multi-line objects and arrays

## Architecture Principles

- Organize code by feature, not by file type
- Keep related files close together
- Use dependency injection for better testability
- Implement proper error handling
- Follow single responsibility principle
