# Multi-Tool Documentation Discovery & Processing

**For**: All AI agents and code editors (Claude, Gemini, Qwen, Cursor, Windsurf, Zed, Roo, etc.)  
**Purpose**: Tool-specific discovery patterns and context loading strategies  
**Date**: November 9, 2025

---

## 🛠️ Supported Tools & Discovery Methods

```
TOOL ECOSYSTEM IN EmailIntelligence
═══════════════════════════════════════════════════════════════

┌─ PRIMARY TOOLS (Full MCP Integration)
│  ├─ Amp (ampcode.com)
│  │  └─ Loads: .amp-settings.json, AGENTS.md, thread context
│  │
│  ├─ Claude Code (cursor/VSCode integration)
│  │  └─ Loads: CLAUDE.md, .claude/settings.json, .vscode/settings.json
│  │
│  ├─ Cursor (IDE)
│  │  └─ Loads: .cursor/mcp.json, .cursor/rules/, Cursor-specific context
│  │
│  └─ Gemini (Google's code integration)
│     └─ Loads: .gemini/settings.json, GEMINI.md

├─ SECONDARY TOOLS (Rule-based or Config files)
│  ├─ Qwen (Alibaba's model)
│  │  └─ Loads: .qwen/PROJECT_SUMMARY.md
│  │
│  ├─ Windsurf (IDE with AI)
│  │  └─ Loads: .windsurf/ config
│  │
│  ├─ Zed (Modern editor)
│  │  └─ Loads: .zed/settings, Zed extensions
│  │
│  ├─ Kilo (Code agent)
│  │  └─ Loads: .kilo/mcp.json, .kilo/rules/
│  │
│  ├─ Kiro (Variant agent)
│  │  └─ Loads: .kiro/ config
│  │
│  ├─ Roo (Code exploration)
│  │  └─ Loads: .roo/mcp.json, .roo/rules/
│  │
│  └─ Trae (Specialized tool)
│     └─ Loads: .trae/rules/

└─ INTEGRATION PATTERNS
   ├─ MCP Servers (.mcp.json files)
   ├─ Configuration (.claude/, .gemini/, .cursor/, etc.)
   ├─ Rules directories (./rules/ in each tool dir)
   └─ Tool-specific docs (CLAUDE.md, GEMINI.md, etc.)
```

---

## 🔍 Tool-Specific Discovery Patterns

### Amp (ampcode.com)

```
DISCOVERY SEQUENCE:
  1️⃣ Loads: .amp-settings.json
     ├─ Reads: amp.permissions, amp.guardedFiles
     ├─ Sets: Tool allowlist, confirmation rules
     └─ Decision: What operations require approval

  2️⃣ Loads: AGENTS.md (auto-load from project root)
     ├─ Reads: Task Master commands
     ├─ Reads: Workflow patterns
     └─ Decision: Essential development workflow

  3️⃣ Loads: Thread context (from ampcode.com/threads/T-xxx)
     ├─ Reads: Previous conversation history
     ├─ Reads: Decisions and reasoning
     └─ Decision: Continue from known state

  4️⃣ Searches: For docs via finder/grep
     ├─ Command: finder("orchestration")
     ├─ Results: All matching docs
     └─ Priority: AGENT_ORCHESTRATION_CHECKLIST.md first

CONTEXT WINDOW: ~150k tokens (largest)
  ├─ Thread context: ~50k
  ├─ Codebase: ~40k
  ├─ Discovery docs: ~15k
  └─ Working memory: ~45k

SAFETY MODEL: Explicit permission checks
  ├─ git push → "ask" in .amp-settings.json
  ├─ git commit → "ask" for confirmation
  ├─ Guarded files → Cannot edit without warning
  └─ Tool allowlist → Only whitelisted tools available

DISCOVERY STRENGTH: ✅ EXCELLENT
  ├─ Largest context window
  ├─ Thread persistence
  ├─ Explicit permission model
  └─ Full MCP integration
```

### Claude Code (VSCode/Cursor plugin)

```
DISCOVERY SEQUENCE:
  1️⃣ Loads: CLAUDE.md (auto-loaded)
     ├─ Section: Claude Code Integration
     ├─ Section: Essential MCP Tools
     └─ Section: Workflow recommendations

  2️⃣ Loads: .claude/settings.json
     ├─ Reads: allowedTools (tool allowlist)
     ├─ Reads: permissions
     └─ Decision: Which tools can be used

  3️⃣ Loads: .vscode/settings.json (if in VSCode)
     ├─ Reads: amp.permissions
     ├─ Reads: amp.mcpServers
     └─ Decision: Available MCP servers

  4️⃣ Loads: .mcp.json
     ├─ Reads: mcpServers definition
     ├─ Reads: Environment variables
     └─ Decision: Available agent tools

  5️⃣ Scans: .claude/commands/
     ├─ Finds: Custom slash commands
     ├─ Example: /taskmaster-next.md
     └─ Decision: Available shortcuts

CONTEXT WINDOW: ~100k tokens
  ├─ Files being edited: ~40k
  ├─ CLAUDE.md context: ~20k
  ├─ Relevant docs: ~10k
  └─ Working memory: ~30k

SAFETY MODEL: Tool allowlist
  └─ .claude/settings.json → "allowedTools": [...]

CUSTOM COMMANDS: Yes
  ├─ /taskmaster-next → Show next task
  ├─ /taskmaster-complete <id> → Complete task
  └─ User can add more in .claude/commands/

DISCOVERY STRENGTH: ✅ VERY GOOD
  ├─ Auto-loads CLAUDE.md
  ├─ Custom command shortcuts
  ├─ Tool allowlist safety
  └─ Full MCP integration available
```

### Cursor (IDE)

```
DISCOVERY SEQUENCE:
  1️⃣ Loads: .cursor/mcp.json
     ├─ Reads: mcpServers configuration
     ├─ Reads: Available servers
     └─ Decision: What tools are available

  2️⃣ Loads: .cursor/rules/
     ├─ Finds: Project-specific rules
     ├─ Example: rules_for_orchestration.md
     └─ Decision: How to behave in context

  3️⃣ Scans: README.md (if Cursor reads on startup)
     ├─ Reads: Project overview
     └─ Context: What is this project about?

  4️⃣ Discovers: via search in context
     ├─ Command: "Find docs about orchestration"
     ├─ Results: Searches repo for matches
     └─ Priority: By relevance

CONTEXT WINDOW: ~50k tokens (limited by IDE context)
  ├─ Current file: ~10k
  ├─ Recent edits: ~5k
  ├─ Prompt context: ~20k
  └─ Working memory: ~15k

RULES SYSTEM: Yes
  ├─ .cursor/rules/ directory
  ├─ Can define project-specific behavior
  ├─ Example: "Never commit to main directly"
  └─ Syntax: Cursor's rules.md format

IDE INTEGRATION: Native
  ├─ Full IDE file access
  ├─ Editor commands
  ├─ Terminal access
  └─ Git operations through IDE

DISCOVERY STRENGTH: ✅ GOOD
  ├─ MCP support
  ├─ Rules system
  ├─ IDE-native operations
  └─ Limited context (smaller window)
```

### Gemini (Google's integration)

```
DISCOVERY SEQUENCE:
  1️⃣ Loads: .gemini/settings.json
     ├─ Reads: mcpServers configuration
     ├─ Reads: API key setup
     └─ Decision: Available tools

  2️⃣ Loads: GEMINI.md (if exists)
     ├─ Reads: Gemini-specific configuration
     ├─ Reads: Custom workflows
     └─ Decision: Gemini-optimized approach

  3️⃣ Scans: Project files via API
     ├─ Discovers: Through file system access
     ├─ Searches: Using search API
     └─ Context: Limited to what API allows

CONTEXT WINDOW: ~30k tokens (API-limited)
  ├─ Request context: ~15k
  ├─ System prompt: ~5k
  ├─ Response buffer: ~10k
  └─ Limited token budget

API MODEL: Request-response
  ├─ Each interaction: New context
  ├─ No persistent thread history
  ├─ Must include context in each request
  └─ Smaller docs preferred

DISCOVERY STRENGTH: ⚠️ MEDIUM
  ├─ Requires explicit doc loading
  ├─ Limited context window
  ├─ No thread persistence
  └─ MCP available but limited
```

### Qwen (Alibaba's model)

```
DISCOVERY SEQUENCE:
  1️⃣ Loads: .qwen/PROJECT_SUMMARY.md
     ├─ Reads: High-level project overview
     ├─ Reads: Key concepts
     └─ Context: What should Qwen know?

  2️⃣ Scans: Project structure
     ├─ Discovers: docs/ directory
     ├─ Searches: README.md
     └─ Context: Self-discovery

  3️⃣ Uses: System prompt
     ├─ May include: Documentation paths
     ├─ May include: Dos and don'ts
     └─ Context: Rules embedded in prompt

CONTEXT WINDOW: ~20k tokens (API-limited)
  ├─ System prompt: ~5k
  ├─ Request: ~10k
  ├─ Response: ~5k
  └─ Very constrained

DISCOVERY STRENGTH: ⚠️ LIMITED
  ├─ Depends on .qwen/PROJECT_SUMMARY.md
  ├─ Small context budget
  ├─ Requires pre-loading docs in system prompt
  └─ No persistent memory
```

### Windsurf, Zed, Kilo, Kiro, Roo, Trae

```
DISCOVERY PATTERNS (Uniform across these tools):

SEQUENCE:
  1️⃣ Load: .<tool>/mcp.json (if exists)
     └─ MCP server configuration

  2️⃣ Load: .<tool>/rules/ (if exists)
     └─ Project-specific behavior rules

  3️⃣ Load: .<tool>/settings.json (if exists)
     └─ Tool-specific configuration

  4️⃣ Search: README.md, docs/
     └─ Self-discovery of docs

CONTEXT WINDOW: Varies
  ├─ Windsurf: ~80k tokens (IDE)
  ├─ Zed: ~60k tokens (IDE)
  ├─ Kilo/Kiro/Roo/Trae: ~40-50k tokens (agents)
  └─ All: Limited compared to Amp/Claude

COMMON FEATURES:
  ├─ MCP support (if configured)
  ├─ Rules-based behavior
  ├─ Project discovery
  └─ Limited persistence

DISCOVERY STRENGTH: ⚠️ VARIABLE
  ├─ Depends on configuration
  ├─ Smaller context windows
  ├─ Require explicit doc loading
  └─ Limited thread persistence
```

---

## 📊 Discovery Efficiency Comparison

| Tool | Context | Persistence | Thread | MCP | Rules | Safety | Strength |
|------|---------|-------------|--------|-----|-------|--------|----------|
| **Amp** | 150k | ✅ YES | ✅ YES | ✅ Full | ✅ YES | ✅ Best | ⭐⭐⭐⭐⭐ |
| **Claude** | 100k | ✅ YES | ✅ YES | ✅ Full | ✅ YES | ✅ Good | ⭐⭐⭐⭐⭐ |
| **Cursor** | 50k | ⚠️ Limited | ⚠️ Limited | ✅ Yes | ✅ YES | ✅ Good | ⭐⭐⭐⭐ |
| **Gemini** | 30k | ❌ NO | ❌ NO | ⚠️ Limited | ❌ NO | ⚠️ Basic | ⭐⭐⭐ |
| **Windsurf** | 80k | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ✅ YES | ⚠️ Basic | ⭐⭐⭐⭐ |
| **Zed** | 60k | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ⚠️ Basic | ⭐⭐⭐ |
| **Qwen** | 20k | ❌ NO | ❌ NO | ❌ NO | ❌ NO | ⚠️ Minimal | ⭐⭐ |
| **Kilo/Roo** | 40k | ⚠️ Limited | ❌ NO | ⚠️ Limited | ✅ YES | ⚠️ Basic | ⭐⭐⭐ |

---

## 📁 Configuration File Locations

### What each tool reads on startup

```
┌─ UNIVERSAL (All tools)
│  ├─ README.md (project overview)
│  ├─ AGENTS.md (if configured to load)
│  └─ docs/ directory (discoverable)
│
├─ Amp-specific
│  ├─ .amp-settings.json (permissions, guarded files)
│  └─ AGENTS.md (auto-loads from project)
│
├─ Claude Code
│  ├─ CLAUDE.md (auto-loads from project)
│  ├─ .claude/settings.json
│  ├─ .claude/commands/ (custom slash commands)
│  └─ .vscode/settings.json (if in VSCode)
│
├─ Cursor
│  ├─ .cursor/mcp.json
│  ├─ .cursor/rules/ (behavior rules)
│  └─ .cursor/settings.json (if exists)
│
├─ Gemini
│  ├─ .gemini/settings.json
│  └─ GEMINI.md (if created)
│
├─ Qwen
│  ├─ .qwen/PROJECT_SUMMARY.md
│  └─ .qwen/config.json (if exists)
│
├─ Windsurf/Zed/Others
│  ├─ .<tool>/mcp.json (if exists)
│  ├─ .<tool>/rules/ (if exists)
│  └─ .<tool>/settings.json (if exists)
│
└─ SHARED MCP
   └─ .mcp.json (root level, shared by all)
```

---

## 🎯 Optimized Discovery per Tool

### For HIGH-CONTEXT tools (Amp, Claude, OpenAI)

```
Optimize: Load EVERYTHING
  ├─ All discovery docs
  ├─ All safety checklists
  ├─ All decision trees
  ├─ All reference materials
  └─ Let agent filter by relevance

Pattern: Comprehensive context first, agent decides usage
```

### For MEDIUM-CONTEXT tools (Cursor, Windsurf, Zed)

```
Optimize: Load by task type
  ├─ Orchestration task → Load AGENT_ORCHESTRATION_CHECKLIST.md + ORCHESTRATION_SYSTEM.md
  ├─ CI/CD task → Load GITHUB_WORKFLOWS_ROADMAP.md
  ├─ Task management → Load AGENTS.md + .taskmaster/config.json
  └─ File ops → Load .amp-settings.json (guarded files)

Pattern: Two-tier loading
  1. Checklist (validation)
  2. Spec (detailed reference)
```

### For LIMITED-CONTEXT tools (Gemini, Qwen, Kilo)

```
Optimize: Load ONLY what's needed
  ├─ Create tool-specific docs (.gemini/SETUP.md, .qwen/RULES.md)
  ├─ Embed safety rules in system prompt
  ├─ Use .qwen/PROJECT_SUMMARY.md as executive summary
  ├─ Link to full docs but don't embed them
  └─ Rely on explicit user requests for context

Pattern: Summaries + system prompt, not full docs
  ├─ .qwen/PROJECT_SUMMARY.md (~200 lines)
  ├─ Embedded rules (in system prompt)
  ├─ Links to full docs for reference
  └─ User provides context when needed
```

---

## 🚀 Tool-Specific Recommended Docs

### Amp

```
ALWAYS LOAD:
  ├─ AGENTS.md (essential task commands)
  ├─ .amp-settings.json (permissions)
  └─ Thread context (from ampcode.com)

LOAD BY TASK:
  ├─ Orchestration → AGENT_ORCHESTRATION_CHECKLIST.md
  ├─ Workflows → GITHUB_WORKFLOWS_ROADMAP.md
  ├─ Git ops → ORCHESTRATION_SYSTEM.md decision trees
  └─ Tasks → .taskmaster/tasks/tasks.json

SIZE BUDGET: Unlimited (can load everything)
PRIORITY: Safety first, then comprehensiveness
```

### Claude Code

```
ALWAYS LOAD:
  ├─ CLAUDE.md (custom workflows)
  ├─ .claude/settings.json (tools available)
  └─ Custom commands from .claude/commands/

LOAD BY TASK:
  ├─ Orchestration → AGENT_ORCHESTRATION_CHECKLIST.md
  ├─ File mods → ORCHESTRATION_SYSTEM.md
  ├─ Task mgmt → AGENTS.md
  └─ CI/CD → GITHUB_WORKFLOWS_ROADMAP.md

SIZE BUDGET: 100k tokens
PRIORITY: Checklists > Specs > Examples
```

### Cursor

```
ALWAYS LOAD:
  ├─ .cursor/mcp.json (available tools)
  ├─ .cursor/rules/ (project rules)
  └─ README.md (project overview)

LOAD BY TASK:
  ├─ Orchestration → .cursor/rules/orchestration.md (create this)
  ├─ Safety → .cursor/rules/safety.md (create this)
  ├─ Tasks → AGENTS.md (simplified version)
  └─ CI/CD → Link to full docs

SIZE BUDGET: 50k tokens (limited)
PRIORITY: Rules > Checklists > Brief specs
RECOMMENDATION: Create Cursor-specific rule files
```

### Gemini

```
LOAD IN REQUEST:
  ├─ GEMINI.md (Gemini-specific setup)
  ├─ .gemini/settings.json (available tools)
  ├─ AGENT_ORCHESTRATION_CHECKLIST.md (first 100 lines)
  └─ Task-specific spec (if needed)

USER PROVIDES:
  ├─ High-level task description
  ├─ Links to relevant docs
  ├─ Explicit constraints
  └─ Safety reminders

SIZE BUDGET: 30k tokens (very limited)
PRIORITY: System prompt embedded rules
RECOMMENDATION: Create GEMINI.md with essential guidelines
```

### Qwen

```
CREATE: .qwen/PROJECT_SUMMARY.md (~200 lines)
  ├─ Project overview
  ├─ Key constraints (orchestration rules)
  ├─ Typical workflows
  └─ Links to full docs

SYSTEM PROMPT:
  ├─ Embed: Safety rules
  ├─ Embed: Common patterns
  ├─ Embed: Tool restrictions
  └─ Reference: Full docs if needed

USER PROVIDES:
  ├─ Task description
  ├─ Explicit doc references
  ├─ Safety context
  └─ Confirmation of constraints

SIZE BUDGET: 20k tokens (minimal)
PRIORITY: Efficiency over comprehensiveness
```

---

## 📋 Creating Tool-Specific Documentation

### Template for tool-specific setup guides

```
For each tool, create: docs/SETUP_<TOOL>.md

STRUCTURE:
  1. Quick Start
     ├─ Configuration file location
     ├─ First-time setup
     └─ Verification steps

  2. Discovery Process
     ├─ What files the tool loads
     ├─ What context it has
     └─ What it can access

  3. Safety Rules
     ├─ Constraints specific to tool
     ├─ Permission limitations
     └─ Guarded operations

  4. Common Tasks
     ├─ Example workflows for this tool
     ├─ Typical use cases
     └─ Expected behavior

  5. Troubleshooting
     ├─ Common issues
     ├─ Recovery procedures
     └─ Context limitations

Example files to create:
  ├─ docs/SETUP_CURSOR.md
  ├─ docs/SETUP_GEMINI.md
  ├─ docs/SETUP_QWEN.md
  └─ docs/SETUP_WINDSURF.md
```

---

## 🔗 Unified Documentation Entry Points

### How tools discover docs (all methods)

```
METHOD 1: README.md links
  ├─ Tool reads: README.md
  ├─ Finds: "See docs/ORCHESTRATION_SYSTEM.md"
  ├─ Action: Load that doc
  └─ Tools using: All (if they read README)

METHOD 2: AGENTS.md links
  ├─ Tool reads: AGENTS.md
  ├─ Finds: "Task Master commands"
  ├─ Action: Load .taskmaster/config.json
  └─ Tools using: Amp, Claude, others with explicit load

METHOD 3: Tool-specific docs
  ├─ Tool reads: CLAUDE.md, GEMINI.md, etc.
  ├─ Finds: Tool-specific recommendations
  ├─ Action: Load recommended docs
  └─ Tools using: Claude, Gemini (if docs exist)

METHOD 4: Direct search
  ├─ User: "Find docs about orchestration"
  ├─ Tool: Uses search/finder to locate
  ├─ Action: Load matching docs
  └─ Tools using: All (if they have search)

METHOD 5: MCP Tools
  ├─ Tool: Uses MCP Task Master server
  ├─ Finds: Tasks, docs, guidance through API
  ├─ Action: Follows MCP recommendations
  └─ Tools using: Those with MCP configured

METHOD 6: System prompt injection
  ├─ User provides: Docs in system prompt
  ├─ Tool receives: Pre-loaded context
  ├─ Action: Uses injected docs
  └─ Tools using: Limited-context (Gemini, Qwen)
```

---

## ✅ Checklist: Tool-Aware Documentation

```
For Amp/Claude (High context):
  [ ] All docs available in docs/
  [ ] Cross-references between docs
  [ ] No size restrictions (can load everything)
  [ ] Thread persistence expected
  [ ] Explicit safety rules loaded

For Cursor/Windsurf/Zed (Medium context):
  [ ] Tool-specific rule files created (if possible)
  [ ] Checklists available (high priority)
  [ ] Decision trees available (high priority)
  [ ] Size estimates for each doc
  [ ] README.md links to essential docs

For Gemini/Qwen/Kilo (Low context):
  [ ] Tool-specific docs created (.gemini/SETUP.md, etc.)
  [ ] PROJECT_SUMMARY.md exists (.qwen/PROJECT_SUMMARY.md)
  [ ] System prompt guidelines documented
  [ ] Links to full docs for reference
  [ ] Essential rules embedded (not in external docs)

For All tools:
  [ ] docs/ directory organized hierarchically
  [ ] INDEX.md created (master reference)
  [ ] Docs discoverable by search
  [ ] Cross-tool safety rules consistent
  [ ] Setup instructions for each tool
  [ ] Troubleshooting per-tool issues
```

---

## 🎯 Summary: Multi-Tool Strategy

```
HIGH-CONTEXT TOOLS (Amp, Claude, OpenAI):
  ├─ Load everything
  ├─ Leverage thread persistence
  ├─ Use full context window
  └─ Provide comprehensive guidance

MEDIUM-CONTEXT TOOLS (Cursor, Windsurf, Zed):
  ├─ Two-tier loading (checklist + spec)
  ├─ Create tool-specific rules
  ├─ Respect token limitations
  └─ Use IDE-native integrations

LOW-CONTEXT TOOLS (Gemini, Qwen, Kilo):
  ├─ Embed rules in system prompt
  ├─ Create tool-specific summaries
  ├─ Link to full docs for reference
  └─ Rely on explicit user guidance

ALL TOOLS:
  ├─ Consistent safety model across tools
  ├─ Discoverable documentation
  ├─ Clear per-tool setup instructions
  ├─ Tool-aware error handling
  └─ Centralized configuration (.mcp.json)
```

---

**Last Updated**: November 9, 2025  
**Audience**: Tool maintainers, developers, LLM agents  
**Status**: Framework documented, implementation pending per tool

