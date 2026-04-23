# Crush IDE-Specific Instructions

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains only Crush IDE-specific features and integrations.

## MCP Configuration for Crush IDE

Configure Task Master MCP server in your Crush workspace configuration:

```json
{
  "extensions": {
    "task-master-ai": {
      "enabled": true,
      "mcpServer": {
        "command": "npx",
        "args": ["-y", "task-master-ai"]
      }
    }
  }
}
```

**Note:** API keys are configured via `task-master models --setup`, not in MCP configuration.

## Crush IDE-Specific Features

### Workspace Integration

- Built-in terminal with task management
- File explorer with MCP tool integration
- Split editor windows for parallel task work
- Integrated debugging and linting

Both `AGENTS.md` and `CRUSH.md` are auto-loaded in Crush workspace context.

### File Management in Crush

```bash
# Direct file operations from integrated terminal
task-master show 1.2    # View task details
task-master update-subtask --id=1.2 --prompt="progress notes"

# File context available via workspace explorer
# Edit files directly in Crush editor (superior UX to terminal)
```

### Inline AI Assistance

- Hover over code for explanations
- Right-click → "Analyze with Task Master"
- Inline suggestions for code improvements

## Important Differences from Other Agents

### Integrated Development Environment
Crush provides a unified IDE experience - no need for separate terminal windows.

### Visual File Tree
Navigate repository structure with visual file explorer (more efficient than `ls`/`find`).

### Real-time Collaboration
Crush supports shared workspaces - multiple developers on same project.

### No Separate Configuration Files
Settings managed within Crush IDE GUI, not via `.crush/` directories.

## Recommended Model Configuration

For Crush IDE users:

```bash
# Configure via Crush IDE settings panel
task-master models --set-main <your-preferred-model>
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback <backup-model>
```

## Your Role with Crush IDE

As a Crush IDE assistant with Task Master:

1. **Leverage IDE features** - Use visual file explorer, split editors, integrated terminal
2. **Use MCP tools naturally** - Available through IDE context menu and inline suggestions
3. **Manage tasks in editor** - View task details directly in Crush
4. **Workspace coordination** - Facilitate multi-developer workflows
5. **Real-time feedback** - Provide immediate code analysis and suggestions

**Key Principle:** Crush IDE provides a complete development environment. Task Master integrates seamlessly for task-driven development workflows.

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
