# LLxPRT Assistant-Specific Instructions

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains only LLxPRT-specific features and integrations.

## MCP Configuration for LLxPRT

Configure Task Master MCP server in your LLxPRT workspace:

```json
{
  "tools": {
    "task-master": {
      "enabled": true,
      "mcp": {
        "command": "npx",
        "args": ["-y", "task-master-ai"]
      }
    }
  }
}
```

**Note:** API keys are configured via `task-master models --setup`, not in MCP configuration.

## LLxPRT-Specific Features

### Advanced Reasoning & Planning

- Multi-step reasoning with explicit verification
- Complex problem decomposition
- Detailed execution planning before action
- Cross-referencing between multiple knowledge domains

Both `AGENTS.md` and `LLXPRT.md` are auto-loaded in LLxPRT context.

### Specialized Workflows

LLxPRT excels at:
- Architecture design and system planning
- Complex debugging with root cause analysis
- Performance optimization strategies
- Security vulnerability assessment

### Token Management

```bash
# Monitor reasoning token usage (LLxPRT-specific)
# Use structured prompts to optimize token efficiency
task-master analyze-complexity --research  # Uses LLxPRT's reasoning strengths
```

## Important Differences from Other Agents

### Extended Thinking Capabilities
LLxPRT supports extended reasoning chains for complex problems - leverage this for architecture and planning tasks.

### Explicit Verification
Always get LLxPRT to verify conclusions before proceeding - use this for critical decisions.

### Cross-Domain Analysis
Can correlate patterns across multiple system components simultaneously.

### Higher Precision
Slower but more accurate - ideal for planning and architecture, less ideal for rapid iteration.

## Recommended Model Configuration

For LLxPRT users:

```bash
# Use LLxPRT for complex analysis, fallback to faster model for iterations
task-master models --set-main <llxprt-model>
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback <fast-model>  # For rapid iterations
```

## Your Role with LLxPRT Assistant

As an LLxPRT assistant with Task Master:

1. **Leverage extended reasoning** - Use LLxPRT's strength for complex analysis
2. **Verify conclusions** - Ask LLxPRT to verify before proceeding
3. **Plan before executing** - Create detailed implementation plans
4. **Cross-reference patterns** - Find connections across system components
5. **Use for critical decisions** - Architecture, security, performance optimization

**Key Principle:** LLxPRT is best for planning, analysis, and architectural decisions. Use faster models for iterative implementation tasks.

---

## When to Use LLxPRT vs Faster Models

| Task Type | Best Choice | Reason |
|-----------|-------------|--------|
| Architecture design | LLxPRT | Needs extended reasoning |
| Bug investigation | LLxPRT | Root cause requires deep analysis |
| Performance optimization | LLxPRT | Must consider multiple factors |
| Security assessment | LLxPRT | Critical decisions need verification |
| Code implementation | Fast model | Faster iteration cycles |
| Unit testing | Fast model | Straightforward tasks |
| Documentation | Either | Task-dependent |

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
