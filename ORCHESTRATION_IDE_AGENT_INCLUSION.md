# Orchestration IDE Agent File Inclusion Strategy

**Status:** Complete  
**Branch:** orchestration-tools  
**Last Updated:** 2025-11-17

## Overview

This document ensures all IDE-specific agent instruction files and configurations are properly included in the orchestration-tools branch for consistent AI agent support across all IDEs and tools.

---

## Included IDE Agent Files

### Primary Agent Instruction Files (Root Level)

These files provide agent-specific guidance that extends `AGENTS.md`:

| File | IDE/Tool | Purpose | Status |
|------|----------|---------|--------|
| `AGENTS.md` | Core/Main | Task Master orchestration baseline | ✅ Included |
| `CRUSH.md` | Crush IDE | Crush IDE-specific Task Master integration | ✅ Included |
| `LLXPRT.md` | LLxPRT | Extended reasoning and planning workflows | ✅ Included |
| `IFLOW.md` | Iflow/Cursor | Inline AI assistance and cursor workflows | ✅ Included |
| `QWEN.md` | Qwen | Qwen-specific AI instructions | ✅ Included |
| `CLAUDE.md` | Claude Code | Claude Code integration and workflows | ✅ Included |
| `terminal-jarvis_AGENTS.md` | Terminal Jarvis | Terminal-based task management | ✅ Included |
| `cognee-AGENTS.md` | Cognee | Cognee framework integration | ✅ Included |

### Complementary IDE Configuration Directories

| Path | IDE/Tool | Purpose | Status |
|------|----------|---------|--------|
| `.claude/**` | Claude Code | Claude Code settings, commands, agents | ✅ Tracked |
| `.cursor/**` | Cursor IDE | Cursor IDE rules and commands | ✅ Tracked |
| `.windsurf/**` | Windsurf IDE | Windsurf IDE rules and configuration | ✅ Tracked |
| `.roo/**` | Roo IDE | Roo IDE rules and configuration | ✅ Tracked |
| `.kilo/**` | Kilo Code | Kilo Code rules and configuration | ✅ Tracked |
| `.clinerules/**` | Cline IDE | Cline IDE rules and workflows | ✅ Tracked |
| `.opencode/**` | OpenCode | SpecKit commands and integration | ✅ Tracked |
| `.specify/**` | Specify | Planning templates and scripts | ✅ Tracked |
| `.github/instructions/**` | All IDEs | Shared instruction files | ✅ Tracked |

### Supporting Documentation

| File | Purpose | Status |
|------|---------|--------|
| `TASKMASTER_INTEGRATION_README.md` | Task Master integration guide | ✅ Included |
| `MODEL_CONTEXT_STRATEGY.md` | Model configuration and context | ✅ Included |
| `ORCHESTRATION_CONTROL_MODULE.md` | Orchestration module details | ✅ Included |
| `.mcp.json` | MCP server configuration | ✅ Included |
| `.env.example` | Environment variable templates | ✅ Included |

---

## File Inclusion Manifest

### PowerShell Variable Mappings

The following PowerShell-style variable mapping ensures consistent file references:

```powershell
# IDE Agent Instruction Files
$AGENTS_FILE        = Join-Path $REPO_ROOT 'AGENTS.md'
$CRUSH_FILE         = Join-Path $REPO_ROOT 'CRUSH.md'
$LLXPRT_FILE        = Join-Path $REPO_ROOT 'LLXPRT.md'
$IFLOW_FILE         = Join-Path $REPO_ROOT 'IFLOW.md'
$QWEN_FILE          = Join-Path $REPO_ROOT 'QWEN.md'
$CLAUDE_FILE        = Join-Path $REPO_ROOT 'CLAUDE.md'

# IDE Configuration Directories - Core
$COPILOT_FILE       = Join-Path $REPO_ROOT '.github/**'
$CLAUDE_DIR         = Join-Path $REPO_ROOT '.claude/**'
$CURSOR_FILE        = Join-Path $REPO_ROOT '.cursor/**'
$WINDSURF_FILE      = Join-Path $REPO_ROOT '.windsurf/**'
$ROO_FILE           = Join-Path $REPO_ROOT '.roo/**'
$KILOCODE_FILE      = Join-Path $REPO_ROOT '.kilo/**'

# IDE Configuration Directories - Additional
$CLINEFILES         = Join-Path $REPO_ROOT '.clinerules/**'
$OPENCODE_FILE      = Join-Path $REPO_ROOT '.opencode/**'
$SPECIFY_FILE       = Join-Path $REPO_ROOT '.specify/**'

# MCP and Environment Configuration
$MCP_CONFIG         = Join-Path $REPO_ROOT '.mcp.json'
$ENV_EXAMPLE        = Join-Path $REPO_ROOT '.env.example'

# Task Master Integration
$TASKMASTER_README  = Join-Path $REPO_ROOT 'TASKMASTER_INTEGRATION_README.md'
$MODEL_CONTEXT      = Join-Path $REPO_ROOT 'MODEL_CONTEXT_STRATEGY.md'
$ORCH_CONTROL       = Join-Path $REPO_ROOT 'ORCHESTRATION_CONTROL_MODULE.md'
```

---

## Relationship to Reference Documents

### CRUSH.md Integration
- Extends `AGENTS.md` with Crush IDE-specific features
- Covers MCP configuration, workspace integration, and inline AI
- Points users to `AGENTS.md` for complete Task Master commands

### LLXPRT.md Integration
- Extends `AGENTS.md` for extended reasoning workflows
- Details complex task handling and verification
- References core Task Master functionality in `AGENTS.md`

### IFLOW.md Integration
- Extends `AGENTS.md` with Cursor-based inline workflows
- Covers non-intrusive assistance and keyboard efficiency
- Links to `AGENTS.md` for full command reference

### QWEN.md Integration
- Qwen-specific AI model instructions
- Configured via Task Master models command (see `AGENTS.md`)

### CLAUDE.md Integration
- Claude Code specific integration
- Auto-loaded by Claude Code workspace
- Extends `AGENTS.md` functionality for Claude users

---

## Git Tracking Configuration

All files are tracked in orchestration-tools branch:

```bash
# Verify all files are tracked
git ls-files | grep -E '(AGENTS|CRUSH|LLXPRT|IFLOW|QWEN|CLAUDE|terminal-jarvis|cognee|\.claude|\.cursor|\.windsurf|\.roo|\.kilo)'

# Check .gitignore doesn't exclude IDE configs
git check-ignore -v .claude/ .cursor/ .windsurf/ .roo/ .kilo/
```

---

## Distribution to Secondary Branches

These files are distributed from orchestration-tools to:
- `main` - Stable release branch
- `scientific` - Scientific computing branch

Distribution uses the standardized branch propagation system documented in:
- `.github/BRANCH_PROPAGATION_POLICY.md`
- `BRANCH_UPDATE_PROCEDURE.md`

---

## Maintenance Checklist

When adding new IDE agent files:

- [ ] Create new `{IDE}-AGENTS.md` file in repo root
- [ ] Ensure it extends `AGENTS.md` (not replaces)
- [ ] Add to git tracking: `git add {IDE}-AGENTS.md`
- [ ] Update this document's inclusion manifest
- [ ] Verify MCP configuration in `.mcp.json` if applicable
- [ ] Test in target IDE environment
- [ ] Commit to orchestration-tools with clear message
- [ ] Document in branch propagation checklist

---

## Validation Command

```bash
# Verify all IDE agent files are present and tracked
for file in AGENTS.md CRUSH.md LLXPRT.md IFLOW.md QWEN.md CLAUDE.md; do
  if git ls-files | grep -q "^$file$"; then
    echo "✅ $file - tracked"
  else
    echo "❌ $file - NOT tracked"
  fi
done

# Verify IDE config directories are tracked (core)
for dir in .claude .cursor .windsurf .roo .kilo; do
  if git ls-files | grep -q "^$dir/"; then
    echo "✅ $dir/ - tracked"
  else
    echo "⚠️ $dir/ - check if intentional"
  fi
done

# Verify additional IDE directories are tracked
for dir in .clinerules .opencode .specify; do
  if git ls-files | grep -q "^$dir/"; then
    echo "✅ $dir/ - tracked"
  else
    echo "⚠️ $dir/ - check if intentional"
  fi
done
```

---

## References

- `AGENTS.md` - Core agent guidance (Task Master)
- `CRUSH.md`, `LLXPRT.md`, `IFLOW.md` - IDE-specific extensions
- `.mcp.json` - MCP server configuration
- `.github/BRANCH_PROPAGATION_POLICY.md` - Branch management policy
- `BRANCH_UPDATE_PROCEDURE.md` - Distribution procedure

---

*This document ensures consistent IDE agent support across orchestration-tools and downstream branches.*
