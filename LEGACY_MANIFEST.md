# Legacy Component Manifest

This document tracks all components marked as "Legacy Component" in the EmailIntelligence project. This standard was established to replace inconsistent usage of "deprecated" terminology across the codebase.

## Purpose

- **Standardization**: Provides a consistent marker for code that should be migrated or replaced
- **Tracking**: Helps maintain awareness of technical debt and migration requirements
- **Guidance**: Offers clear instructions for AI agents and developers working with legacy code

## Marker Standard

Components marked as "Legacy Component" should:

1. **Include a clear header comment** at the top of the file
2. **State the replacement/alternative** if known
3. **Include a migration timeline** if applicable
4. **Document the reason for deprecation**

## Currently Tracked Legacy Components

### Backend Components

| File Path | Status | Notes |
|-----------|--------|-------|
| `src/backend/node_engine/workflow_manager.py` | Legacy Component | Part of the deprecated `backend` package. Will be removed in a future release. |
| `src/backend/python_backend/workflow_editor_ui.py` | Legacy Component | Identified for future migration |

### Configuration Files

| File Path | Status | Notes |
|-----------|--------|-------|
| `.eslintrc.json` | Legacy Component | Migrated to ESLint 9+ flat config (`eslint.config.js`) |
| `client/.eslintrc.json` | Legacy Component | Migrated to flat config |
| `setup/launch.py` | Legacy Component (Conflict Resolution Needed) | Contains orphaned code blocks and merge conflicts that need resolution |

## Migration Guidelines

### For AI Agents

When working with legacy components:

1. **Read the marker header** - All legacy components include a header comment explaining their status
2. **Avoid modifying the legacy code directly** - Instead, plan for replacement/rewrite
3. **Check for alternatives** - Look for newer implementations that may replace the legacy component
4. **Document changes** - If you must modify a legacy component, document why in the commit message

### For Developers

1. **Do not add new features to legacy components**
2. **Plan migration in upcoming sprints**
3. **Test thoroughly** if changes to legacy code are unavoidable
4. **Update this manifest** when marking/unmarking components as legacy

## Marker Template

```python
# Legacy Component
# 
# Reason: [Why is this component marked as legacy?]
# Alternative: [What should be used instead?]
# Migration: [What steps need to be taken to migrate away from this?]
# Review Date: [When should this be revisited?]
```

## Change Log

- **2024**: Established "Legacy Component" standard to replace inconsistent "deprecated" terminology
- **2024**: Migrated ESLint configuration to flat config format
- **2024**: Identified workflow_manager.py and related backend components for future migration