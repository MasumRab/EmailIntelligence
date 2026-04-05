# New Capabilities Introduced by External Tools

**Date:** 2026-04-05  
**Purpose:** Exhaustive inventory of every feature/capability the external tools provide that does NOT exist in the current EmailIntelligence agent rules setup

---

## Current Baseline (What Exists Today)

| Capability | Status | Implementation |
|-----------|--------|----------------|
| Rule files per tool | ✅ | Manual `.md` files in 6 tool dirs |
| MCP configs | ⚠️ Partial | 3 of 7 tools have working configs |
| Commands | ✅ | `.claude/commands/`, `.cursor/commands/`, `.gemini/commands/`, `.qwen/commands/` |
| Subagents/Modes | ⚠️ Partial | `.claude/agents/planner.md`, `.roo/rules/.roomodes` (5 modes) |
| Hooks | ⚠️ Kiro only | 7 Kiro hooks, no other tool |
| Ignore files | ✅ | `.cursorignore`, `.geminiignore`, `.rulesyncignore` |
| Permissions | ⚠️ Ad-hoc | `.claude/settings.json`, `.qwen/settings.json` — not synced |
| Skills | ❌ None | No agent skills in any tool directory |
| Templates | ❌ None | No rule templates system |
| Validation/CI checks | ❌ None | No drift detection, no CI pipeline |
| Security-specific rules | ❌ None | Only passing mentions in self_improve.md |
| Testing strategy rules | ❌ None | No dedicated testing guidance |
| Content from community | ❌ None | All rules manually authored or from Taskmaster boilerplate |
| Lockfile for dependencies | ❌ None | No version-pinned rule sources |
| Rule analytics/dashboard | ❌ None | No visibility into rule usage |
| MCP tool-level config | ❌ None | No `enabledTools`/`disabledTools` |
| Global (user-scope) rules | ❌ None | All rules project-scoped only |
| Automatic backups | ❌ None | No backup before rule changes |
| Version detection | ❌ None | No framework version-aware rules |
| Documentation mirroring | ❌ None | No human-readable mirror of agent rules |

---

## New Capabilities by Tool

### 1. RuleSync v7.27 — 19 New Capabilities

#### A. Sync & Generation Engine (Core — not present today)

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **RS-1** | **Single-source generation** | Write rules once in `.rulesync/*.md`, generate to all 28+ targets | ❌ Manual copy-paste with find-replace |
| **RS-2** | **`--check` drift detection** | `rulesync generate --check` exits code 1 if generated files don't match source — CI-ready | ❌ No drift detection at all |
| **RS-3** | **`--dry-run` preview** | Shows what would change without writing files | ❌ No preview capability |
| **RS-4** | **`--delete` clean generation** | Wipes existing tool directories before regenerating, preventing stale file accumulation | ❌ Stale `.rules` file persists |
| **RS-5** | **Import from any tool** | `rulesync import --targets cline` imports existing rules into unified format | ❌ No import mechanism |
| **RS-6** | **28+ target tools** | Supports Claude Code, Cursor, Cline, Roo, Kiro, Windsurf, Qwen, OpenCode, Gemini, Copilot, Codex, Junie, Goose, Warp, Replit, Zed, deepagents, Factory Droid, Rovodev, Antigravity, AugmentCode, Kilo Code, Copilot CLI, AGENTS.md, AgentsSkills | Only 6 tools configured manually |

#### B. Permissions Syncing (Not present today)

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **RS-7** | **Unified permissions schema** | JSON Schema with `allow`/`ask`/`deny` per tool/action, synced across tools from single `.rulesync/permissions.json` | ❌ Permissions defined ad-hoc in `.claude/settings.json` and `.qwen/settings.json` with different formats, not synced |
| **RS-8** | **Permissions as a feature flag** | `--features permissions` flag in generate/import commands | ❌ Not a managed feature |

#### C. Skills Management (Not present today)

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **RS-9** | **Declarative skill installation** | Declare skills in `rulesync.jsonc`, run `rulesync install` to fetch and place them | ❌ No skill management at all |
| **RS-10** | **Lockfile for skills** | `rulesync install --frozen` fails if lockfile is stale (CI safety) | ❌ No lockfile concept |
| **RS-11** | **Fetch skills from remote repos** | `rulesync fetch dyoshikawa/rulesync --features skills` pulls community/official skills | ❌ No remote skill sourcing |
| **RS-12** | **`AgentsSkills` target** | Generates to the universal `~/.agents/skills/` directory | ❌ Skills not generated |

#### D. Simulated Features (Not present today)

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **RS-13** | **Simulated commands** | `--simulate-commands` generates command-like instructions for tools that don't natively support commands (Copilot, Cursor, Codex) | ❌ Commands only exist for tools that natively support them |
| **RS-14** | **Simulated subagents** | `--simulate-subagents` creates subagent-like patterns for tools without native subagent support | ❌ Subagents only in Claude and Roo |
| **RS-15** | **Simulated skills** | `--simulate-skills` creates skill-like structures for tools without native skill directories | ❌ No skills at all |

#### E. Infrastructure Features (Not present today)

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **RS-16** | **MCP tool-level config** | `enabledTools`/`disabledTools` support for Codex CLI and OpenCode (`🔧` flag) | ❌ MCP configs only specify servers, not tool filtering |
| **RS-17** | **Global (user-scope) mode** | `--global` flag generates rules in `~/.claude/`, `~/.cursor/` etc. for user-wide defaults | ❌ Only project-scoped rules |
| **RS-18** | **gitignore management** | `rulesync gitignore` auto-adds generated files to `.gitignore` with correct patterns | ❌ `.gitignore` manually maintained |
| **RS-19** | **MCP server mode** | `rulesync mcp` starts RuleSync as an MCP server — agents can manage rules programmatically | ❌ No agent-accessible rule management |

---

### 2. Agent Rules Builder — 6 New Capabilities

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **ARB-1** | **Community rule library** | 10,000+ community-contributed rules curated from real GitHub projects | ❌ All rules are manually written or Taskmaster boilerplate |
| **ARB-2** | **Language/framework-specific templates** | Pre-built rule sets for 40+ languages including Python, FastAPI, Django, React, TypeScript | ❌ No framework-specific rule templates; current rules are generic Prisma/JS boilerplate |
| **ARB-3** | **Verbosity tiers** | Each rule available at 3 levels: concise, balanced, detailed — choose density | ❌ All rules are single-verbosity |
| **ARB-4** | **Rule sharing via public links** | Save rule sets and share via URL; others can fork as starting point | ❌ No sharing mechanism |
| **ARB-5** | **Multi-agent export format** | Single builder exports to Cursor, Claude, Copilot, Windsurf, Gemini, Codex formats | ❌ Manual per-tool formatting |
| **ARB-6** | **Rule browsing and discovery** | Browse rules by language, framework, category; popular rules leaderboard | ❌ No rule discovery or community access |

---

### 3. Agent Rules Kit v3.8 — 8 New Capabilities

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **ARK-1** | **Automatic framework version detection** | Scans project to auto-detect framework versions, generates version-specific rules | ❌ No version detection; rules are version-agnostic |
| **ARK-2** | **Architecture-aware rule generation** | Generates rules specific to architectural patterns (DDD, Hexagonal, MVC, Atomic Design) | ❌ No architecture-specific rules despite project using interface-based architecture |
| **ARK-3** | **MCP tool usage rules** | Generates best-practice rules for using MCP tools (PAMPA, GitHub, Memory, Filesystem, Git) with error handling patterns, rate limit guidance, security patterns | ❌ MCP configs exist but no usage guidance rules |
| **ARK-4** | **Automatic backup before changes** | Smart backup system preserves custom rules when updating/regenerating | ❌ No backup mechanism; `rulesync --delete` would destroy customizations |
| **ARK-5** | **Documentation mirroring** | `--mirror` flag generates `.md` files that mirror rules in human-readable format for code review | ❌ No human-readable mirror; rules are agent-only |
| **ARK-6** | **Enhanced debug mode** | Detailed logging of rule generation process for troubleshooting | ❌ No debug visibility into rule generation |
| **ARK-7** | **Multi-IDE install from existing rules** | `npx agent-rules-kit install --target=cursor` converts existing `.mdc` rules to any IDE format | ❌ No cross-format conversion |
| **ARK-8** | **MCP SDK coverage** | Rules for implementing MCP servers/clients in Python, TypeScript, Java, Kotlin, C#, Swift | ❌ No MCP development guidance |

---

### 4. agent-rules (Liran Tal) — 5 New Capabilities

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **AR-1** | **Security-focused coding rules** | Dedicated `secure-code` topic with rules from Node.js Secure Coding guide — input validation, injection prevention, dependency scanning | ❌ Only passing mention "Follow security best practices" in AGENTS.md |
| **AR-2** | **Security vulnerability scanning rules** | `security-vulnerabilities` topic with Snyk.io-based vulnerability detection and remediation patterns | ❌ No vulnerability scanning guidance |
| **AR-3** | **Testing strategy rules** | Dedicated `testing` topic with comprehensive test patterns from JavaScript Testing Best Practices — unit/integration/e2e patterns, mocking guidelines, coverage targets | ❌ Only "Tests pass" in Definition of Done; no testing strategy |
| **AR-4** | **MCP server scaffolding** | `--mcp` flag auto-configures MCP servers (`.vscode/mcp.json`, `.gemini/settings.json`) with non-destructive merge | ❌ MCP configs are manually created and inconsistent |
| **AR-5** | **Custom command scaffolding** | `--commands` flag deploys reusable prompts/commands (e.g., GitHub issue implementation workflow) | ❌ Commands exist but are all speckit-related; no issue/security workflows |

---

### 5. agentfiles (Obsidian Plugin) — 6 New Capabilities

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **AF-1** | **Unified skill browser** | Browse skills, commands, and agents from 13+ tools in a single UI (three-column view) | ❌ No visibility across tool configs |
| **AF-2** | **Skill marketplace** | Install community skills from [skills.sh](https://skills.sh) directly | ❌ No marketplace access |
| **AF-3** | **Conversation history browser** | Browse Claude Code session history, search, tag, and export to vault | ❌ No session history visibility |
| **AF-4** | **Dashboard analytics** | Usage analytics: burn rate, context tax, health metrics via `skillkit scan` | ❌ No analytics on rule/skill usage |
| **AF-5** | **Inline skill editor** | Edit skills with markdown preview and save (Cmd+S) from Obsidian | ❌ Rules edited via IDE or text editor only |
| **AF-6** | **Deep search** | Full-text search across all skills/commands/agents with toggleable deep search scope | ❌ No cross-tool search capability |

---

## Consolidated New Capabilities Summary

### By Category

| Category | Count | Sources | Current State |
|----------|-------|---------|---------------|
| **Sync & Distribution** | 6 | RS-1 through RS-6 | ❌ Manual copy-paste |
| **Validation & CI** | 3 | RS-2, RS-3, RS-10 | ❌ Zero validation |
| **Permissions Management** | 2 | RS-7, RS-8 | ❌ Ad-hoc, unsynced |
| **Skills Management** | 6 | RS-9 through RS-12, AF-1, AF-2 | ❌ No skills system |
| **Simulated Features** | 3 | RS-13, RS-14, RS-15 | ❌ Not available |
| **Security Rules** | 2 | AR-1, AR-2 | ❌ No security rules |
| **Testing Rules** | 1 | AR-3 | ❌ No testing strategy |
| **Community/Templates** | 4 | ARB-1 through ARB-4, ARB-6 | ❌ No community access |
| **Multi-format Export** | 3 | ARB-5, ARK-7, RS-5 | ❌ Manual formatting |
| **Framework Detection** | 2 | ARK-1, ARK-2 | ❌ Version-agnostic |
| **MCP Tooling** | 3 | ARK-3, ARK-8, RS-16 | ❌ No MCP guidance |
| **Backup & Safety** | 1 | ARK-4 | ❌ No backups |
| **Documentation Mirror** | 1 | ARK-5 | ❌ No mirroring |
| **Debug/Observability** | 3 | ARK-6, AF-4, AF-6 | ❌ No observability |
| **Infrastructure** | 3 | RS-17, RS-18, RS-19 | ❌ Not available |
| **Session Management** | 1 | AF-3 | ❌ No session view |
| **Verbosity Control** | 1 | ARB-3 | ❌ Single verbosity |
| **Rule Scaffolding** | 2 | AR-4, AR-5 | ❌ Manual creation |
| **Runtime Enforcement** | 15 | AZ-1 through AZ-15 | ❌ No enforcement |
| **TOML Config** | 12 | RL-1 through RL-12 | ❌ No declarative config |
| **Persistent Memory** | 4 | LC-1 through LC-4 | ❌ No memory |
| **TOTAL NEW** | **71** | | |

### By Priority for This Project

#### 🔴 High Priority (Directly fixes stress test issues)

| # | Capability | Tool | Fixes Issue |
|---|-----------|------|-------------|
| RS-1 | Single-source generation | RuleSync | Eliminates 5,570 duplicate lines |
| RS-2 | `--check` drift detection | RuleSync | Prevents future drift (CI) |
| RS-5 | Import from existing tools | RuleSync | Bootstraps from Cline canonical |
| RS-7 | Permissions syncing | RuleSync | Syncs Claude/Qwen permissions |
| ARB-2 | Python/FastAPI templates | Agent Rules Builder | Replaces Prisma boilerplate (M1) |

#### 🟡 Medium Priority (Enhances quality)

| # | Capability | Tool | Value |
|---|-----------|------|-------|
| AR-1 | Security coding rules | agent-rules | Fills missing security guidance |
| AR-3 | Testing strategy rules | agent-rules | Fills missing test strategy |
| RS-9 | Declarative skill install | RuleSync | Manages skills systematically |
| RS-13 | Simulated commands | RuleSync | Extends commands to more tools |
| RS-14 | Simulated subagents | RuleSync | Extends subagents beyond Claude/Roo |
| ARK-3 | MCP tool usage rules | Agent Rules Kit | Adds MCP best-practice guidance |
| RS-18 | gitignore management | RuleSync | Auto-manages generated file tracking |
| RS-3 | `--dry-run` preview | RuleSync | Safe rule changes |
| ARK-4 | Automatic backups | Agent Rules Kit | Safety net for regeneration |

#### 🟢 Low Priority (Nice-to-have)

| # | Capability | Tool | Value |
|---|-----------|------|-------|
| RS-17 | Global mode | RuleSync | User-wide defaults |
| RS-19 | MCP server mode | RuleSync | Agents manage their own rules |
| ARB-3 | Verbosity tiers | Agent Rules Builder | Rule density control |
| ARB-4 | Sharing via links | Agent Rules Builder | Team collaboration |
| ARK-1 | Version detection | Agent Rules Kit | Version-specific rules |
| ARK-2 | Architecture-aware rules | Agent Rules Kit | DDD/interface pattern rules |
| ARK-5 | Documentation mirroring | Agent Rules Kit | Human review of agent rules |
| AF-1 | Unified skill browser | agentfiles | Visual skill management |
| AF-4 | Dashboard analytics | agentfiles | Usage visibility |

---

## Feature Overlap Analysis

Some features appear in multiple tools. Where overlap exists, the recommended tool is noted.

| Feature | RuleSync | Ruler | Agent RuleZ | ARK | agent-rules | ARB | agentfiles | Recommended |
|---------|:--------:|:-----:|:-----------:|:---:|:-----------:|:---:|:----------:|:-----------:|
| Multi-tool rule generation | ✅ 28 tools | ✅ 13 tools | ❌ | ✅ 9 IDEs | ✅ 4 tools | ✅ 7+ formats | ❌ | **RuleSync** (broadest) |
| MCP config sync | ✅ | ✅ | ❌ | ❌ | ✅ (2 tools) | ❌ | ❌ | **RuleSync** |
| Runtime enforcement | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | **Agent RuleZ** (unique) |
| Policy validation | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | **Agent RuleZ** (unique) |
| Policy testing | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | **Agent RuleZ** (unique) |
| TOML config | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | **Ruler** (unique) |
| Trae support | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | **Ruler** (unique) |
| MCP usage best practices | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | **ARK** (unique) |
| Community rule library | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 10K+ | ✅ marketplace | **ARB** (largest) |
| Security rules | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | **agent-rules** (unique) |
| Testing rules | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | **agent-rules** (unique) |
| Skills management | ✅ lockfile | ❌ | ✅ cross-runtime | ❌ | ❌ | ❌ | ✅ browser | **RuleSync** (CI-ready) |
| CI drift detection | ✅ `--check` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **RuleSync** (unique) |
| Permissions sync | ✅ schema | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **RuleSync** (unique) |
| Backup before changes | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | **Ruler** or **ARK** |
| Version auto-detect | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | **ARK** (unique) |
| Analytics/dashboard | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | **agentfiles** (unique) |
| Simulated commands | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **RuleSync** (unique) |
| Persistent memory | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **Letta Code** (unique) |

---

### 6. Agent RuleZ v2.3.0 — 15 New Capabilities (RUNTIME ENFORCEMENT)

**Category:** Runtime Policy Engine — ONLY tool that enforces at execution time
**Source:** https://github.com/SpillwaveSolutions/agent_rulez

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **AZ-1** | **Runtime blocking** | Intercepts tool calls and blocks dangerous operations before execution | ❌ No enforcement, rules are advisory only |
| **AZ-2** | **Rule injection** | Injects context/instructions before tool execution | ❌ No dynamic context injection |
| **AZ-3** | **`rulez validate`** | Validates hooks.yaml syntax and structure | ❌ No config validation |
| **AZ-4** | **`rulez lint`** | Analyzes rule quality, detects overlapping matchers | ❌ No rule quality analysis |
| **AZ-5** | **`rulez debug`** | Simulates events without live execution — test-driven policy | ❌ No policy testing |
| **AZ-6** | **`rulez test`** | Batch test from YAML scenarios — CI-ready policy testing | ❌ No CI policy tests |
| **AZ-7** | **`rulez explain`** | Post-hoc analysis of what rules fired | ❌ No audit trail |
| **AZ-8** | **`rulez repl`** | Interactive debug mode for real-time testing | ❌ No interactive debugging |
| **AZ-9** | **Multi-runtime support** | Works with Claude Code, OpenCode, Gemini CLI, Codex CLI | ❌ No cross-tool enforcement |
| **AZ-10** | **Path-based matching** | Block/inject based on file paths | ❌ No path-based rules |
| **AZ-11** | **Command regex matching** | Match tool commands with regex patterns | ❌ No command filtering |
| **AZ-12** | **Priority-based rules** | Rules evaluated in priority order | ❌ No rule ordering |
| **AZ-13** | **Fail-open mode** | Allow operations if rule evaluation fails | ❌ No fail-safe mode |
| **AZ-14** | **Skills management** | `rulez skills sync/status/diff` across runtimes | ❌ No cross-runtime skill sync |
| **AZ-15** | **Self-update** | `rulez upgrade` from GitHub releases | ❌ Manual updates only |

**🔴 CRITICAL:** Agent RuleZ fills a gap NO other tool addresses — runtime enforcement. All other tools manage static files. Agent RuleZ actually prevents dangerous operations.

---

### 7. Ruler — 12 New Capabilities (ALTERNATIVE SYNC)

**Category:** Static File Sync (TOML-based)
**Source:** https://github.com/intellectronica/ruler

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **RL-1** | **TOML configuration** | Declarative config in `.ruler/ruler.toml` | ❌ No declarative config |
| **RL-2** | **MCP server config** | Unified `[mcp_servers]` section in TOML | ❌ MCP configs scattered |
| **RL-3** | **Gitignore management** | Auto-adds generated files to .gitignore | ❌ Manual .gitignore updates |
| **RL-4** | **Dry-run mode** | Preview changes before applying | ❌ No preview |
| **RL-5** | **Backup before apply** | Creates `.bak` files automatically | ❌ No automatic backups |
| **RL-6** | **13+ agent support** | claude, cursor, cline, copilot, roo, kiro, trae, windsurf, amp, gemini-cli, qwen, opencode, codex | ❌ Only 6 tools configured |
| **RL-7** | **Nested mode** | Option to nest rules in subdirectories | ❌ Flat structure only |
| **RL-8** | **AGENTS.md generation** | Generates AGENTS.md from `.ruler/AGENTS.md` | ❌ Manual AGENTS.md |
| **RL-9** | **Per-agent config** | Enable/disable agents individually | ❌ All-or-nothing |
| **RL-10** | **Environment variable expansion** | `${VAR}` syntax in MCP config | ❌ Hardcoded values |
| **RL-11** | **Trae support** | Supports Trae IDE (RuleSync does not) | ❌ No Trae config |
| **RL-12** | **Simple setup** | Single `ruler.toml` vs RuleSync's multiple files | ❌ Complex multi-file config |

---

### 8. Letta Code — 4 Capabilities (MEMORY-FIRST AGENT)

**Category:** Stateful Agent with Persistent Memory
**Source:** https://letta.com

| # | Capability | Description | Current State |
|---|-----------|-------------|---------------|
| **LC-1** | **Persistent memory** | Agent remembers across sessions in `~/.letta/agents/` | ❌ Other tools have no memory |
| **LC-2** | **Progressive disclosure** | Summary in system prompt, detail loaded on demand | ❌ All-or-nothing context |
| **LC-3** | **Memory filesystem** | Git-backed memory with version control | ❌ No memory versioning |
| **LC-4** | **Skills system** | Reusable workflows with tool access | ⚠️ Limited skills support |

---

## Capabilities NOT Available in ANY Tool

These gaps exist in the current setup and none of the evaluated tools address them:

| Gap | Description | Would Need |
|-----|-------------|-----------|
| **Trae IDE support** | No tool supports Trae as a target | Manual or custom script |
| **Kiro hooks cross-tool sync** | Kiro's hook system is unique; no tool replicates hooks for other tools | Kiro-specific |
| **Python security rules** | agent-rules focuses on Node.js; no tool generates Python/FastAPI security rules | Manual authoring or adaptation |
| **Backlog.md integration** | No tool generates Backlog.md workflow rules | Manual (already in AGENTS.md) |
| **Taskmaster MCP rules** | No tool generates Taskmaster-specific MCP usage guidance | Already custom-authored |
| **Merge conflict prevention** | No tool prevents merge conflicts in agent rule files | Git workflow discipline |
| **Rule content validation** | No tool validates that rule content is relevant to the actual project (e.g., Prisma refs in a non-Prisma project) | Manual review or custom linter |

---

## Implementation Recommendation

**Adopt 71 total capabilities via a 4-tool stack:**

```
RuleSync (primary)       → 19 capabilities (sync, validation, permissions, skills, CI)
Agent RuleZ (enforcement)→ 15 capabilities (runtime blocking, validate, lint, debug, test)
Ruler (alternative sync) → 12 capabilities (TOML config, Trae support, simple setup)
Agent Rules Builder      → 6 capabilities  (templates, community, multi-format)
agent-rules              → 5 capabilities  (security, testing, MCP scaffolding)
Agent Rules Kit          → 8 capabilities  (version detect, backup, mirror, MCP usage)
agentfiles               → 6 capabilities  (browser, marketplace, analytics, search, sessions)
Letta Code               → 4 capabilities  (persistent memory, progressive disclosure)
                           ─────────────────
                           75 total capabilities (4 overlap)
                           71 unique capabilities
```

**Recommended Minimum Stack:**
```
RuleSync (static sync) + Agent RuleZ (runtime enforcement) + Agent Rules Builder (bootstrap)
= 40 unique capabilities covering sync, enforcement, and content
```

**71 total new capabilities vs 0 in current setup.**
