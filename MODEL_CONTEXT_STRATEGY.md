# Model Context Strategy - Unified Guidelines

## Overview

This document describes the standardized context distribution strategy ensuring all AI models receive consistent guidelines and prevent confusion about tool capabilities.

---

## Architecture

### Three-Tier Context System

```
Tier 1: AGENTS.md (Universal Foundation)
├─ Task Master CLI commands (for all agents)
├─ MCP server configuration principles
├─ Core workflows (init, parse-prd, list, show, etc.)
├─ Best practices and patterns
└─ Valid for ALL models/environments

Tier 2: Model-Specific Files (Agent Customization)
├─ CLAUDE.md     → Claude Code, Claude AI
├─ GEMINI.md     → Gemini CLI
├─ QWEN.md       → Qwen CLI
├─ CRUSH.md      → Crush IDE
├─ LLXPRT.md     → LLxPRT extended reasoning
└─ IFLOW.md      → Iflow Cursor integration

Tier 3: Domain Documentation (Context Enhancement)
├─ ORCHESTRATION_PROCESS_GUIDE.md  → Strategy 5/7 operations
├─ PHASE3_ROLLBACK_OPTIONS.md       → Emergency procedures
├─ IMPROVED_PROMPT_ANSWERS.md       → Quality answer templates
├─ scientific_branch_features.md    → Scientific branch specifics
└─ Other technical deep-dives
```

---

## Context Distribution Rules

### Rule 1: AGENTS.md is Source of Truth
- Contains universal Task Master commands
- All models reference this file first
- Model-specific files extend, never contradict

### Rule 2: Each Model File Explicitly References AGENTS.md
```markdown
> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). 
> AGENTS.md contains the core Task Master commands and workflows for all AI agents. 
> This file contains only [MODEL]-specific features and integrations.
```

### Rule 3: Model Files Focus on Three Areas

**Area 1: MCP Configuration**
- Tool-specific setup (`.mcp.json`, `~/.qwen/settings.json`, etc.)
- Platform-specific requirements
- API key location guidance

**Area 2: Tool-Specific Features**
- Unique capabilities (e.g., Claude's Edit tool, Qwen's multi-turn context)
- Session management approach
- Built-in commands or keyboard shortcuts

**Area 3: Important Differences**
- What this agent CAN'T do that others can
- When to use this agent vs others
- Configuration peculiarities

### Rule 4: Consistent Structure
All model files follow this outline:
1. Header + AGENTS.md reference
2. MCP Configuration
3. [Model]-Specific Features
4. Important Differences from Other Agents
5. Recommended Model Configuration
6. Your Role with [Model]
7. Link back to AGENTS.md

---

## Implemented Models

### Claude (CLAUDE.md)
**Best For:** General-purpose development, file editing
- Native Edit tool (superior to sed/manual)
- Git integration
- Parallel worktrees
- Tool allowlist configuration

### Gemini (GEMINI.md)
**Best For:** Research, documentation, explanations
- Google Search grounding (alternative to Perplexity)
- Session checkpointing
- Token usage monitoring
- Headless mode for automation

### Qwen (QWEN.md)
**Best For:** Multi-language, reasoning tasks
- Multi-turn conversation context
- Model switching capability
- Math and reasoning strength
- Chinese language support

### Crush (CRUSH.md)
**Best For:** IDE-integrated development
- Visual file explorer
- Split editor windows
- Integrated debugging
- Collaborative workspaces

### LLxPRT (LLXPRT.md)
**Best For:** Planning, architecture, security analysis
- Extended reasoning chains
- Cross-domain analysis
- Verification-first approach
- Complex problem decomposition

### Iflow (IFLOW.md)
**Best For:** Cursor-integrated inline assistance
- Non-intrusive suggestions
- Keyboard-centric workflow
- Automatic file context loading
- Real-time completion

---

## Quality Assurance

### When Creating New Model Documentation

1. **Reference AGENTS.md**
   ```markdown
   > **Note:** This file works alongside `AGENTS.md`...
   ```

2. **Include All Six Sections**
   - Header + reference
   - MCP Configuration
   - [Model]-Specific Features
   - Important Differences
   - Recommended Configuration
   - Your Role

3. **Avoid Contradictions**
   - Run Task Master commands against AGENTS.md
   - Don't redefine Task Master behavior
   - Only extend with tool-specific features

4. **Test Context Loading**
   - Verify model receives both files
   - Check for command clarity
   - Ensure no configuration conflicts

### When Updating AGENTS.md

1. **Notify all model files** - Changes apply to all
2. **Check for conflicts** - May affect model-specific workflows
3. **Update version number** in AGENTS.md
4. **Document why** in commit message

### When Updating Model Files

1. **Never change Task Master commands**
2. **Update only tool-specific sections**
3. **Maintain header reference** to AGENTS.md
4. **Explain changes** in commit message

---

## Distribution

### Auto-Loaded Files
Most modern development environments auto-load context:

- **Claude Code:** AGENTS.md + CLAUDE.md (from `.claude/` and project root)
- **Gemini CLI:** AGENTS.md + GEMINI.md (both auto-loaded)
- **Qwen CLI:** AGENTS.md + QWEN.md (both auto-loaded)
- **Crush IDE:** AGENTS.md + CRUSH.md (via workspace)
- **LLxPRT:** AGENTS.md + LLXPRT.md (via context loading)
- **Iflow Cursor:** AGENTS.md + IFLOW.md (via extension)

### Manual Distribution
If auto-loading unavailable:

```bash
# Paste these files into model context window
cat AGENTS.md CLAUDE.md  # For Claude
cat AGENTS.md GEMINI.md  # For Gemini
# etc.
```

### Git Distribution
Files are version-controlled on `orchestration-tools-changes` branch:

```bash
git checkout orchestration-tools-changes
# All model files automatically available
```

---

## Conflict Resolution

### Scenario: Model File Contradicts AGENTS.md

**Resolution:** AGENTS.md is source of truth
- Remove contradiction from model file
- Add note explaining why model differs (if valid)
- Test to ensure no workflow breakage

### Scenario: Two Models Have Different Commands

**Resolution:** Create model-specific workaround
- Keep core Task Master command identical
- Add model-specific wrapper or instructions
- Document in model file why difference exists

Example:
```markdown
# Both models use task-master list, but:
- Claude Code: Add `mcp__task_master_ai__` prefix for MCP tools
- Gemini CLI: Use natural language "show me tasks"
```

---

## Common Pitfalls to Avoid

### ❌ Don't
- Redefine Task Master commands
- Contradict AGENTS.md
- Assume all models support same tools
- Use tool-specific syntax in universal docs
- Create new model files without this structure

### ✅ Do
- Reference AGENTS.md explicitly
- Extend with model-specific features only
- Document important limitations
- Follow consistent file structure
- Test context loading before release

---

## Adding a New Model

### Checklist

- [ ] Create `[MODEL_NAME].md` file
- [ ] Include AGENTS.md reference header
- [ ] Document MCP configuration
- [ ] List 3-5 model-specific features
- [ ] Explain important differences
- [ ] Provide recommended model configuration
- [ ] Describe your role with this model
- [ ] Test context loading
- [ ] Commit with message: `docs: add [MODEL_NAME] context guidelines`

### Template

```markdown
# [Model Name] - Context & Guidelines

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). 
> AGENTS.md contains the core Task Master commands and workflows for all AI agents. 
> This file contains only [Model Name]-specific features and integrations.

## MCP Configuration for [Model Name]

[Configuration template...]

## [Model Name]-Specific Features

[3-5 features...]

## Important Differences from Other Agents

[Key distinctions...]

## Recommended Model Configuration

[Model setup...]

## Your Role with [Model Name]

[Role description...]

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
```

---

## Current Status

✓ AGENTS.md - Universal foundation (2025-11-10)
✓ CLAUDE.md - Claude Code/AI (2025-11-10)
✓ GEMINI.md - Gemini CLI (pre-existing, aligned)
✓ QWEN.md - Qwen CLI (2025-11-10)
✓ CRUSH.md - Crush IDE (2025-11-10)
✓ LLXPRT.md - LLxPRT reasoning (2025-11-10)
✓ IFLOW.md - Iflow Cursor (2025-11-10)

**All model files follow consistent structure and reference AGENTS.md.**

---

## Next Steps

1. Test context loading in each environment
2. Verify no contradictions between files
3. Update this document if new patterns emerge
4. Monitor for model-specific issues requiring new guidelines

---

*Last Updated: 2025-11-10*
*Version: 1.0*
