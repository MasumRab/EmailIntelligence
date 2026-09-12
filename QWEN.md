# Qwen CLI-Specific Instructions

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the shared Task Master workflow and project baseline. This file keeps Qwen-specific runtime and workflow guidance at the project root as a reviewed Tier 2 context file.

## Runtime on This Branch

- Project config lives in `.qwen/settings.json`.
- The current Qwen runtime loads `AGENTS.md` as the shared baseline via `.qwen/settings.json`.
- `.taskmaster/.qwen/session_manager.py` also reads the root `QWEN.md` file into captured project context, so this file must remain at the project root.

## MCP Configuration

Current project configuration:

```json
{
  "context": {
    "fileName": "AGENTS.md"
  },
  "mcpServers": {
    "task-master-ai": {
      "command": "npm",
      "args": ["exec", "task-master-ai"],
      "type": "stdio"
    }
  }
}
```

API keys are configured via environment variables and `task-master models --setup`, not in repo-local plaintext.

## Qwen CLI-Specific Features

### Session Management

Built-in session commands:

- `/chat` — start a new conversation while keeping context
- `/context` — inspect current loaded context
- `/model` — switch between Qwen models
- `/history` — inspect recent conversation history
- `/usage` — view token and request usage

For this repo, the most reliable resume pattern is: `AGENTS.md` baseline + root `QWEN.md` + `docs/handoff/STATE.md`.

### Headless Mode for Automation

Qwen works well for scripted or one-shot analysis:

```bash
qwen "What's the next task?"
qwen --stream "Summarize the current handoff state"
qwen --model qwen-plus "Analyze this code"
```

### Strengths to Lean On

- multi-step reasoning
- code review and code explanation
- multilingual explanations
- fast iteration on structured prompts

## Important Differences from Other Agents

### Root File Still Matters

Even though `.qwen/settings.json` currently points shared context loading at `AGENTS.md`, the root `QWEN.md` file is still part of the branch policy because session-manager tooling reads it directly.

### Supplemental Summary Is Separate

`.qwen/PROJECT_SUMMARY.md` is retained as a lightweight supplemental note only. If it conflicts with this file or `.qwen/settings.json`, prefer the settings file first and this file second.

### MCP Permissions Live in Qwen Settings

Qwen-specific permissions and MCP wiring are managed in `.qwen/settings.json`, not in `.mcp.json`.

## Recommended Usage

As a Qwen assistant in this repo:

1. Use `AGENTS.md` for shared project rules and commands.
2. Use `QWEN.md` for Qwen-only runtime notes and workflow differences.
3. Use `/context` or session-manager tooling to confirm what is loaded.
4. Use `docs/handoff/STATE.md` as the authoritative execution log for this cleanup.

**Key Principle:** Preserve Qwen-specific root guidance without duplicating the shared AGENTS baseline.
