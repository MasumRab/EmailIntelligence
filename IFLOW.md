# Iflow Cursor Integration Guide

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains Iflow cursor-specific features and integrations.

## About Iflow Cursor

Iflow is a cursor-extension-based development environment providing inline AI suggestions and code completion while maintaining full control over the codebase.

## MCP Configuration for Iflow

Configure Task Master MCP server in your Iflow/Cursor configuration:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"]
    }
  }
}
```

**Note:** API keys are configured via `task-master models --setup`, not in MCP configuration.

## Iflow-Specific Features

### Inline AI Assistance

- Real-time code completion suggestions
- Inline refactoring recommendations
- Quick explanations via hover
- Context-aware code generation

Both `AGENTS.md` and `IFLOW.md` are auto-loaded in Iflow Cursor context.

### Cursor-Based Workflows

```bash
# Leverage Iflow's inline suggestions
# Select code → Right-click → "Ask Iflow" for explanations
# Type comment → Iflow auto-completes implementation

# Terminal integration
task-master next    # Get next task from inline terminal
```

### Smart Context

- Iflow tracks open files automatically
- Maintains context across edits
- Understands your coding patterns
- Provides continuity between sessions

## Important Differences from Other Agents

### Non-Intrusive Assistance
Iflow provides suggestions without forcing actions - you maintain full control.

### Keyboard-Centric
Optimized for keyboard shortcuts and efficient typing workflows.

### File-Aware Context
Automatically loads context from open files without explicit commands.

### Seamless Integration
Works naturally within Cursor environment - no context switching needed.

## Recommended Model Configuration

For Iflow Cursor users:

```bash
# Set Iflow/Cursor-compatible model as primary
task-master models --set-main <cursor-compatible-model>
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback <backup-model>
```

## Your Role with Iflow Cursor

As an Iflow Cursor assistant with Task Master:

1. **Provide inline suggestions** - Use Iflow's inline context for recommendations
2. **Respect user control** - Suggest without forcing changes
3. **Keyboard efficiency** - Optimize for keyboard-centric workflows
4. **File context awareness** - Leverage automatically loaded file context
5. **Quick explanations** - Provide concise, on-demand explanations

**Key Principle:** Iflow Cursor is about intelligent, non-intrusive assistance. Task Master integrates for structured task management within this flow-based workflow.

---

## Iflow Best Practices

- Keep files open for context continuity
- Use quick-fix suggestions for refactoring
- Maintain cursor position for task continuity
- Leverage auto-completion for implementation speed
- Reference loaded files implicitly (Iflow tracks them)

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
