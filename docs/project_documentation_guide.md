# Project Documentation Guide

This document outlines the various documentation files in the project and how to maintain them properly.

## Documentation Files

- `README.md`: Main project overview and setup instructions for new users
- `QWEN.md`: Detailed development context and architecture information
- `tools_used.md`: Comprehensive list of tools and technologies used in the project
- `docs/python_style_guide.md`: Python coding standards and best practices
- `docs/architecture/advanced_workflow_system.md`: Documentation for the node-based workflow system
- `docs/development/client_development.md`: Guidelines for client-side development
- `docs/deployment/deployment_guide.md`: Deployment instructions and configurations
- `docs/development/env_management.md`: Environment management guidelines
- `docs/development/extensions_guide.md`: Guide for creating and managing extensions
- `docs/deployment/launcher_guide.md`: Documentation for the unified launcher
- `docs/architecture/node_architecture.md`: Architecture details of the node-based system
- `docs/development/server_development.md`: Guidelines for server-side development

## Maintaining tools_used.md

The `tools_used.md` file is a critical document that provides an overview of all tools and technologies used in the Email Intelligence Platform. It serves as a reference for:

- New developers joining the project to understand the technology stack
- DevOps and deployment processes
- Technology decisions and planning
- Dependency management and security audits

### When to Update

Update `tools_used.md` whenever:

1. New dependencies are added to `pyproject.toml`, `package.json`, or `requirements.txt`
2. Existing dependencies are removed from the project
3. Major version changes occur that affect how tools are used
4. Development tools or infrastructure components change

### How to Update

1. Add or remove tools as they are incorporated or removed from the project
2. Group related tools under the appropriate categories:
   - Development Tools
   - Infrastructure & Deployment
   - Testing & Quality
   - Security & Performance
   - Development Environment
   - AI/NLP Specific Tools
   - Workflow & Node Engine
   - Code Quality & Linting Setup
   - Launcher & Management

3. Maintain alphabetical order within each category where appropriate
4. Use the format `- **Tool Name**: Brief description of what the tool does`

### Verification Process

To ensure the `tools_used.md` file remains accurate:

1. Periodically compare the listed tools with actual dependencies in:
   - `pyproject.toml`
   - `package.json` (in root and client directories)
   - `requirements.txt`
2. Check for imports in Python files to identify any tools not listed in dependency files
3. Remove tools that are no longer used in the project
4. Add tools that are in use but not documented

### Best Practices

- Keep descriptions concise but informative
- Ensure all team members understand the importance of maintaining this document
- Include the documentation maintenance in the code review process when dependencies change
- Regularly audit the file to ensure accuracy