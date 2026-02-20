# Cass CLI Session Analysis Report

**Date**: 2026-01-18  
**Investigation Tool**: `cass` - Unified TUI search over coding agent histories

## Executive Summary

Cross-agent session analysis using `cass` CLI revealed the development history for Feature 004 (Guided CLI Workflows) and the gemini-cli-prompt-library project. Key finding: **typer + rich + InquirerPy** was selected as the CLI stack with documented agentic compatibility requirements.

---

## Cass CLI Capabilities

### Supported Agents
| Supported | Not Supported |
|-----------|---------------|
| amp, gemini, opencode, claude_code, codex, cline, aider, cursor, chatgpt, pi_agent | qwen, kimi |

### Key Commands Used
```bash
cass search "query"     # Fuzzy search across sessions
cass timeline           # Activity timeline
cass context <path>     # Related sessions for a file
cass export             # Export to markdown
cass expand             # Show messages around a line
cass stats              # Index statistics
```

---

## Session Findings

### Primary Workspace
**Path**: `~/.gemini/tmp/ecf9a8bc2dfe40868144eda095201fa9bea57f16fec6afc9397615d58ba49520/`  
**Sessions**: 115 total

### Key Sessions

| Date | Agent | Session ID | Focus |
|------|-------|------------|-------|
| 2026-01-13 10:46 | gemini | session-2026-01-13T10-46-* | Feature 004, CLI framework decision |
| 2026-01-13 16:36 | gemini | session-2026-01-13T16-36-* | Constitution finalization, Ralph Wiggum loop |
| 2025-10-25 04:48 | gemini | session-2025-10-25T04-48-82579874 | `/prompt:improve` command (improve.toml) |
| 2026-01-14 01:49 | opencode | ses_445ce61b2ffedvZhBppw5aQDhA | DSPy-HELM migration, benchmarking |

---

## CLI Framework Decision

### Selected Stack: Option D
```
typer + rich + InquirerPy
```

### Technical Constraint TC-001
- **typer**: CLI command structure
- **InquirerPy**: Advanced interactive prompts
- **rich**: Beautiful terminal output

### Requirements Captured
- Interactive + headless modes
- Workflow state persistence
- Agentic CLI compatibility (JSON output, stdin pipe support)

### Alternative Considered
- Charmbracelet (Go-based) - rejected to stay with Python stack

---

## CLI Library Compatibility Matrix

### Agentic Compatibility

| Library | JSON Output | Headless Mode | No TTY Safe | Recommended |
|---------|-------------|---------------|-------------|-------------|
| **typer** | ✅ `--json` | ✅ | ✅ | ✅ Yes |
| **cyclopts** | ✅ Built-in | ✅ | ✅ | ✅ Yes |
| **python-fire** | ✅ Default | ✅ Native | ✅ | ✅ Yes |
| **rich** | ✅ `force_terminal=False` | ✅ | ✅ | ✅ Yes |
| **Textual** | ✅ Headless mode | ✅ Native | ✅ | ✅ Yes |
| **InquirerPy** | ❌ | ⚠️ Hangs | ❌ Blocks | ⚠️ Needs wrapper |
| **questionary** | ❌ | ⚠️ Hangs | ❌ Blocks | ⚠️ Needs wrapper |

### Agentic Detection Pattern
```python
def is_agentic() -> bool:
    indicators = [
        not sys.stdin.isatty(),
        not sys.stdout.isatty(),
        os.environ.get("AGENT_MODE") == "1",
        os.environ.get("CI") == "true",
        os.environ.get("NONINTERACTIVE") == "1",
    ]
    return any(indicators)
```

---

## Feature 004 Context

**Spec Location**: `/home/masum/github/EmailIntelligenceGem/specs/004-guided-workflow/`

### Artifacts
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `tasks.md` - Task breakdown
- `data-model.md` - Data structures

### Core Component
**WorkflowContextManager**: `src/lib/workflow_context.py`

### Commands
- `guide-dev` - Developer workflow guidance
- `guide-pr` - PR resolution guidance
- Access via: `python launch.py guide-dev|guide-pr`

---

## Recommendations

1. **Wrapper Required**: InquirerPy needs `is_agentic()` fallback for headless operation
2. **JSON Output**: All CLI commands should support `--json` flag
3. **State Persistence**: WorkflowContextManager should save/resume across sessions
4. **Testing**: Use Textual's headless mode for automated testing

---

## References

- gemini-cli-prompt-library: `/home/masum/github/gemini-cli-prompt-library`
- DSPy-HELM work: opencode session `ses_445ce61b2ffedvZhBppw5aQDhA`
- Constitution: `.specify/memory/constitution.md`
