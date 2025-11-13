---
description: Guidelines for using the Backlog.md MCP system for task and project management
applyTo: "**/*"
---

# Backlog.md MCP Task Management System

This guide outlines the Backlog.md MCP system for task and project management, which serves as a fallback/alternative to the Taskmaster system.

## Overview

The Backlog.md MCP system provides a comprehensive task management solution with the following key features:

- **MCP Integration**: Full Model Context Protocol support for seamless AI agent integration
- **Resource-Based Access**: Access workflow information via `backlog://workflow/overview`
- **Tool-Based Operations**: Use `backlog.get_workflow_overview()` when MCP resources aren't available
- **Git Integration**: Automatic branch tracking and task association
- **Status Management**: Configurable task statuses and workflows

## Core Workflow

### 1. Initial Setup and Access

**First Time Working Here:**
- Read `backlog://workflow/overview` (MCP resource) OR
- Call `backlog.get_workflow_overview()` (MCP tool)
- This provides the complete workflow understanding

### 2. Decision Framework for Task Creation

**When to Create Tasks:**
- Complex multi-step features requiring tracking
- Cross-team coordination needs
- Features with dependencies spanning multiple components
- Work that benefits from structured progress tracking

**When NOT to Create Tasks:**
- Simple, single-step changes
- Routine maintenance work
- Work that can be completed in a single session
- Tasks that don't require coordination

### 3. Search-First Workflow

**Before Creating New Tasks:**
- Search existing backlog for similar or duplicate tasks
- Check task status and dependencies
- Review related work to avoid duplication
- Consider if existing tasks can be expanded instead

### 4. Task Creation and Management

**Creating New Tasks:**
- Use appropriate MCP tools for task creation
- Include clear acceptance criteria
- Define dependencies and blockers
- Set appropriate priority levels

**Task Lifecycle:**
- **To Do**: Initial state for planned work
- **In Progress**: Active work in progress
- **Done**: Completed and verified work

## MCP Tools Reference

### Core Tools

- `backlog.get_workflow_overview()`: Get complete workflow understanding
- `backlog.create_task()`: Create new tasks with proper structure
- `backlog.update_task()`: Modify existing task details
- `backlog.list_tasks()`: View tasks by status and filters
- `backlog.search_tasks()`: Find tasks by keywords or criteria
- `backlog.add_dependency()`: Create task relationships
- `backlog.update_status()`: Change task status through lifecycle

### Advanced Tools

- `backlog.create_milestone()`: Group related tasks under milestones
- `backlog.add_label()`: Categorize tasks with labels
- `backlog.generate_report()`: Create progress reports
- `backlog.export_tasks()`: Export tasks in various formats

## Integration with Taskmaster

The Backlog.md MCP system works alongside Taskmaster as follows:

- **Primary System**: Use Taskmaster for detailed, AI-assisted task breakdown and management
- **Fallback System**: Use Backlog.md MCP when Taskmaster is unavailable or for simpler task tracking
- **Complementary**: Both systems can be used together for different types of work

## Configuration

The backlog system is configured via `backlog/config.yml`:

```yaml
project_name: "EmailIntelligenceAuto"
default_status: "To Do"
statuses: ["To Do", "In Progress", "Done"]
labels: []
milestones: []
date_format: yyyy-mm-dd
max_column_width: 20
auto_open_browser: true
default_port: 6420
remote_operations: true
auto_commit: false
bypass_git_hooks: false
check_active_branches: true
active_branch_days: 30
```

## Best Practices

### Task Creation
- Use descriptive titles that clearly indicate the work
- Include acceptance criteria in task descriptions
- Set realistic estimates and dependencies
- Use labels for categorization and filtering

### Workflow Management
- Regularly review and update task status
- Use dependencies to prevent blocked work
- Create milestones for major feature releases
- Maintain clean backlog by archiving completed work

### Team Collaboration
- Use shared labels for cross-team visibility
- Create dependencies for inter-team work
- Use milestones to coordinate releases
- Regular backlog grooming sessions

## Troubleshooting

### Common Issues

**MCP Resource Not Available:**
- Fall back to `backlog.get_workflow_overview()` tool
- Check MCP server configuration
- Verify backlog system is properly installed

**Task Dependencies Issues:**
- Use `backlog.validate_dependencies()` to check for cycles
- Review dependency chains regularly
- Consider breaking complex dependency trees

**Status Synchronization:**
- Ensure all team members use consistent status updates
- Regular backlog reviews to catch stale tasks
- Use automation for status transitions where possible

## Integration Points

The backlog system integrates with:
- **Git**: Branch tracking and commit association
- **GitHub**: Issue and PR linking
- **CI/CD**: Automated status updates
- **Project Management**: Milestone and release planning
- **Reporting**: Progress tracking and analytics

This system provides a robust fallback and complementary approach to task management alongside the primary Taskmaster system.