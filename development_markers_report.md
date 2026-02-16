# Development Markers Report

This report catalogs all TODOs, FIXMEs, and other development markers found in the EmailIntelligence codebase, organized by priority, component, and type.

## 1. TODO Comments

### High Priority
- None identified

### Medium Priority
- None identified

### Low Priority
- None identified

## 2. FIXME Markers

### High Priority
- **setup_linting.py:66** - `W0511, # fixme`

### Medium Priority
- None identified

### Low Priority
- None identified

## 3. Development Notes

### Security Notes
- **launch.py:260** - `# SECURITY NOTE: Use shell=False whenever possible to prevent shell injection.`
- **launch.py:365** - `# SECURITY NOTE: Using hardcoded PyTorch URL - ensure this source is trusted`
- **backend/node_engine/workflow_manager.py:50** - Security path traversal check
- **backend/node_engine/workflow_manager.py:75** - Security path traversal check
- **backend/node_engine/workflow_manager.py:141** - Security path traversal check

### General Notes
- **src/core/database.py:17** - `# NOTE: These dependencies will be moved to the core framework as well.`
- **launch.py:784** - `# Note: The client and server-ts might require additional parameters or configuration`
- **backend/node_engine/test_nodes.py:176** - `# Import here to avoid circular dependency issues`
- **plugins/example_workflow_plugin/__init__.py:12** - `# Note: Plugins need to import from the main application's modules.`
- **backend/python_nlp/smart_filters.py:1417-1418** - Column name notes in DB
- **backend/python_backend/main.py:40** - Circular dependency warning
- **backend/python_backend/workflow_routes.py:186** - Node-based workflow note
- **backend/python_backend/workflow_routes.py:334** - Legacy system note

### Debug/Development Notes
- **launch.py:277** - `# Always log stdout for visibility, especially for debugging setup steps.`
- **launch.py:625** - `cmd.append("--reload")  # Enable auto-reload in debug mode`
- **backend/python_nlp/gmail_service.py:759** - `# Include full script output for debugging or richer info`
- **backend/python_backend/workflow_editor_ui.py:119** - `# JSON representation of workflow (for debugging/serialization)`
- **backend/python_backend/tests/conftest.py:125** - `# This is a bit of a hack, but necessary for this kind of integration test.`
- **backend/python_backend/tests/conftest.py:129** - `# We need to run the async startup event in a sync context for the test fixture`

## 4. Code Quality Issues

### High Priority Security Concerns
1. **Hardcoded Security Notes**:
   - Shell injection warning in launch.py
   - Hardcoded PyTorch URL security note

2. **Path Traversal Protections**:
   - Multiple security checks in workflow_manager.py

3. **Session Management**:
   - Secret key generation in security.py uses `secrets.token_urlsafe(32)` but comment notes it should come from secure storage in production

### Medium Priority Issues
1. **Missing Method Implementations**:
   - None identified (update_category and delete_category methods have been implemented)

2. **Circular Dependencies**:
   - Warning about circular dependency in main.py

### Low Priority Issues
1. **Debug Code**:
   - Debug mode flags and reload options
   - Test fixture workarounds

## 5. Feature Gaps

### Workflow System
- Missing proper workflow selection implementation (TODO in email_routes.py)
- Legacy system compatibility notes

### Plugin System
- Notes about plugin import requirements

### Authentication
- TODO in JULES_WIP_ANALYSIS.md about Gmail API authentication for non-interactive environments

## 6. Summary

The codebase contains a relatively small number of explicit TODO and FIXME markers, with only one TODO and one FIXME identified. However, there are several notes and comments indicating areas for improvement:

1. **Security**: Several security notes indicating areas that need attention, particularly around shell injection prevention and hardcoded URLs
2. **Missing Features**: One critical TODO for workflow selection implementation
3. **Technical Debt**: Notes about missing methods and circular dependencies
4. **Debug Code**: Several debug-related comments that may need cleanup in production

The most critical items to address are:
1. Implementing proper workflow selection (high priority)
2. Addressing the FIXME in setup_linting.py (high priority)
3. Resolving the security notes in launch.py (high priority)
4. Implementing missing methods in category_service.py (medium priority)