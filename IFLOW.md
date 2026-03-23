# Iflow Cursor Integration Guide

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains Iflow cursor-specific features and integrations.


## MCP Configuration for Iflow

Configure Task Master MCP server in your Iflow/Cursor configuration:


## Recommended Model Configuration


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


## Iflow Best Practices

- Keep files open for context continuity
- Use quick-fix suggestions for refactoring
- Maintain cursor position for task continuity
- Leverage auto-completion for implementation speed
- Reference loaded files implicitly (Iflow tracks them)

