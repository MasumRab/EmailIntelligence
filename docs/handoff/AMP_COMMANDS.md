# AMP Commands Guide - Agent Rules Implementation

**Purpose:** Complete reference for AMP CLI commands with native tools, skills integration, and subagent workflows.

**Last Updated:** 2026-04-12
**Branch:** orchestration-tools (isolated - NO merges)

---

## Table of Contents

1. [Tool Configuration Matrix](#tool-configuration-matrix)
2. [Available Skills](#available-skills)
3. [Native AMP Integrations](#native-amp-integrations)
4. [AMP Modes](#amp-modes)
5. [CLI Commands](#cli-commands)
6. [Subagent Workflows](#subagent-workflows)
7. [Review Process](#review-process)

---

## Tool Configuration Matrix

### Tier 1: CLI Tools (AgentsMdAgent Pattern)

CLI tools read root `AGENTS.md` via `settings.json contextFileName`. NO custom `output_path` in ruler.toml.

| Tool | Context Loading | Status |
|------|-----------------|--------|
| **AMP** | `AGENTS.md` via settings.json | ✅ ALIGNED |
| **Gemini CLI** | `AGENTS.md` + `GEMINI.md` | ✅ ALIGNED |
| **Qwen Code** | `AGENTS.md` + `QWEN.md` | ✅ ALIGNED |
| **OpenCode** | `AGENTS.md` | ✅ ALIGNED |
| **Kilo Code** | `AGENTS.md` | ✅ ALIGNED |

### Tier 2: IDE Tools (Ruler with output_path)

| Tool | Context Directory | Status |
|------|-------------------|--------|
| **Claude Code** | `CLAUDE.md` | ✅ ALIGNED |
| **Cursor** | `.cursor/rules/` | ✅ Working |
| **Windsurf** | `.windsurf/rules/` | ✅ Working |
| **Roo/Cline** | `.roo/rules/` | ✅ Working |
| **Trae** | `.trae/rules/` | ✅ Working |
| **Kiro** | `.kiro/steering/` | ✅ Working |

---

## Available Skills

### Letta Skills (`~/.letta/skills/`)

| Skill | Purpose | Phase Usage |
|-------|---------|-------------|
| `agent-resource-manager` | Analyze, dedupe, backup agent configs | Phase 6-7 cleanup |
| `agent-rules-handoff` | Multi-phase agent rules implementation | All phases |
| `branch-isolation-guard` | Enforce branch isolation policy | Pre/post execution |
| `tool-ecosystem-manager` | Detect installed AI tools, verify versions | Phase 0, Phase 9 |

### Agents Skills (`~/.agents/skills/`)

| Skill | Purpose | Phase Usage |
|-------|---------|-------------|
| `serena-mcp-agent` | Semantic code navigation (30x token reduction) | Complex refactoring |
| `coding-agent` | Run Codex, Claude Code, OpenCode via background | Second opinion |
| `ast-grep` | AST-based code search and replacement | Phase 6 deduplication |
| `gemini` | Gemini CLI integration | Parallel verification |
| `graphite-cli` | Git stack management | Branch operations |

### Project Skills (`.agents/skills/`)

Project-specific skills should be placed here.

---

## Native AMP Integrations

### Oracle (Second Opinion)

AMP's **oracle** tool provides a powerful second-opinion model (GPT-5.4 with high reasoning) for complex analysis and code review.

**When to use:**
- Complex debugging or code analysis
- Reviewing architectural decisions
- Getting a second opinion on approaches
- Deep reasoning on difficult problems

**Example prompts:**
```
"Use the oracle to review the last commit's changes. Verify the logic for notification sound triggers hasn't changed."
"Ask the oracle whether there isn't a better solution."
"Analyze how functions X and Y are used. Work with the oracle to figure out how to refactor duplication while keeping backwards compatibility."
```

**CLI invocation:**
```bash
amp -x "Use the oracle to review the agent rules architecture and suggest improvements"
```

### Librarian (Remote Codebase Search)

AMP's **Librarian** subagent searches remote codebases on GitHub (public and private) and Bitbucket Enterprise.

**When to use:**
- Cross-repository research
- Understanding how frameworks/libraries work
- Finding usage examples in other projects
- Investigating recent changes in dependencies

**Example prompts:**
```
"Search our docs and infra repositories to see how new versions get deployed."
"Ask the Librarian to investigate the validation code using Zod - why is this error happening?"
"Use the Librarian to investigate the foo service - were there recent API changes?"
```

**Requirements:**
- GitHub: Configure connection in settings (select private repos if needed)
- Bitbucket: Add `amp.bitbucketToken` to settings

### Subagents (Task Tool)

AMP can spawn **subagents** via the Task tool for parallel work. Each has its own context window and tool access.

**When to use:**
- Multi-step tasks that can be broken into independent parts
- Parallel work across different code areas
- Operations producing extensive output not needed after completion
- Keeping main thread context clean

**Limitations:**
- Can't communicate with each other mid-task
- Start fresh without conversation context
- Main agent only receives final summary

**Example prompts:**
```
"Use 3 subagents to convert these CSS files to Tailwind"
"Spawn subagents to: 1) identify merge conflict patterns, 2) suggest branch naming conventions, 3) recommend workflow improvements"
```

### Painter (Image Generation)

AMP's **Painter** tool generates and edits images using Gemini 3 Pro Image.

**When to use:**
- UI mockups for design review
- App icons and branding
- Redacting sensitive info from screenshots
- Style-guided edits with reference images

**Example prompts:**
```
"Use the painter to create a UI mockup for the settings page"
"Use the painter to generate an app icon - dark background, glowing terminal cursor"
"Use the painter to redact API keys in this screenshot"
```

### Code Review with Checks

AMP's built-in **`amp review`** performs code review for bugs, security, performance, and style violations.

**Custom Checks** are defined in `.agents/checks/`:

```markdown
---
name: performance
description: Flags common performance anti-patterns
severity-default: medium
tools: [Grep, Read]
---

Look for these patterns:
- Nested loops over same collection (O(n²) → O(n) with Set/Map)
- Repeated array.includes() in a loop
- Sorting inside a loop
```

**Check locations:**
- `.agents/checks/` — project-wide
- `api/.agents/checks/` — subtree-specific
- `~/.config/amp/checks/` — global

### Task Master AI (MCP)
```json
{
  "task-master-ai": {
    "command": "npm",
    "args": ["exec", "task-master-ai"],
    "env": {
      "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
      "GEMINI_API_KEY": "${GEMINI_API_KEY}",
      "GITHUB_API_KEY": "${GITHUB_API_KEY}"
    }
  }
}
```
**Usage:** `task-master list`, `task-master next`, `task-master show <id>`

### CodeKnowledge (ck) (MCP)
```json
{
  "ck": {
    "command": "ck",
    "args": ["--serve"]
  }
}
```
**Usage:** Semantic code search via MCP

---

## AMP Modes

| Mode | Description | Use For |
|------|-------------|---------|
| `rush` | Fast execution, minimal verification | Phase 0-4, simple fixes |
| `deep` | Thorough analysis, comprehensive verification | Gate checks, error recovery |
| `smart` | Balanced approach | Phase 5-8, mixed complexity |
| `large` | Extended context | Multi-phase, large file analysis |

---

## CLI Commands

### Phase 0: Content Bootstrap

```bash
amp threads new --mode rush --execute "You are bootstrapping Agent Rules content.

**Use Skill:** Load ~/.letta/skills/agent-rules-handoff for guidance.

**URLs:**
- https://agentrulegen.com
- https://agentrulegen.com/templates/python-fastapi

**Select:** Python, TypeScript, FastAPI, React, Pydantic

**Export to:** .ruler/AGENTS.md (80-150 lines)

**VERIFY:** test -f .ruler/AGENTS.md && echo 'PASS' || echo 'FAIL'"
```

### Phase 1: Emergency Fixes

```bash
amp threads new --mode rush --execute "You are executing Phase 1 Emergency Fixes.

**Phase Document:** docs/handoff/phase-01-emergency-fixes.md
**State File:** docs/handoff/STATE.md
**Branch Policy:** orchestration-tools is ISOLATED - NO merges to/from other branches

**Available Skills:**
- ~/.letta/skills/branch-isolation-guard — Verify isolation before/after
- ~/.letta/skills/tool-ecosystem-manager — Verify tool configs

**Tasks (13 steps):**
1.1-1.2: Resolve CLAUDE.md merge conflict
1.3-1.4: Fix .roo/mcp.json
1.5-1.6: Fix .cursor/mcp.json
1.7-1.8: Fix .claude/mcp.json
1.9-1.10: Fix .windsurf/mcp.json
1.11-1.12: Create .trae/mcp.json
1.13: Delete .rules file

**Critical Rules:**
1. Run VERIFY after EVERY step
2. Copy strings EXACTLY from phase document
3. NEVER use git add -A or git add .
4. DO NOT merge branches

**Start:** Read docs/handoff/phase-01-emergency-fixes.md"
```

### Phase 2: Content Fixes

```bash
amp threads new --mode rush --execute "You are executing Phase 2 Content Fixes.

**Phase Document:** docs/handoff/phase-02-content-fixes.md

**Available Skills:**
- ~/.letta/skills/agent-resource-manager — Analyze configs after fixes
- ~/.agents/skills/ast-grep — Search/replace for dedup patterns

**Tasks (8 steps):**
2.1-2.3: Fix Windsurf dev_workflow.md bugs
2.4-2.6: Fix Prisma references (project uses SQLAlchemy, NOT Prisma)
2.7a: Create rulesync.jsonc if missing
2.7: Update rulesync.jsonc targets
2.8: Verify all content fixes

**Start:** Read docs/handoff/phase-02-content-fixes.md"
```

### Phase 3: Ruler Setup

```bash
amp threads new --mode rush --execute "You are executing Phase 3 Ruler Setup.

**Phase Document:** docs/handoff/phase-03-ruler-setup.md

**Key Discovery:** CLI tools (amp, qwen, opencode, kilocode) read root AGENTS.md via settings.json.
DO NOT add output_path for these tools in ruler.toml.

**Available Skills:**
- ~/.letta/skills/agent-rules-handoff — Full handoff guidance
- ~/.letta/skills/tool-ecosystem-manager — Verify Ruler installation

**Tasks (6 steps):**
3.1: Create .ruler/ directory
3.2: Create .ruler/AGENTS.md (33 lines, NOT 861 lines per agent)
3.3: Create .ruler/ruler.toml (CLI-first, no output_path for CLI tools)
3.4: Verify Ruler config (dry-run)
3.5: Apply Ruler
3.6: Verify output

**Commands:**
ruler apply --project-root . --dry-run
ruler apply --project-root . --backup

**Start:** Read docs/handoff/phase-03-ruler-setup.md"
```

### Phase 4: Agent RuleZ Setup

```bash
amp threads new --mode rush --execute "You are executing Phase 4 Agent RuleZ Runtime Hooks Setup.

**Phase Document:** docs/handoff/phase-04-agent-rulez.md
**Binary:** rulez (installed at ~/.local/bin/rulez, or via mise)

**DO NOT use /tmp/rulez/** — use system-installed binary.

**Tasks (6 steps):**
4.1: Verify rulez binary (rulez --version)
4.2: Create .claude/hooks.yaml
4.3: Validate hooks.yaml
4.4: Lint hooks.yaml
4.5: Debug test: force push blocked (rulez debug --event 'Bash:git push --force origin main')
4.6: Debug test: normal commit allowed

**Expected:**
- Step 4.5: BLOCKED by rule: block-force-push
- Step 4.6: ALLOWED

**Start:** Read docs/handoff/phase-04-agent-rulez.md"
```

### Gate Check

```bash
amp threads new --mode deep --execute "You are running a Phase Gate Check.

**Phase:** [PHASE_NUMBER]

**Native AMP Tools:**
- Use **oracle** for deep reasoning on complex verification
- Use **Librarian** to cross-reference with framework documentation

**Available Skills:**
- ~/.letta/skills/branch-isolation-guard — Verify no forbidden merges
- ~/.letta/skills/tool-ecosystem-manager — Verify tool versions

**Gate Check Commands:**
echo '=== PHASE [N] GATE CHECK ==='

# File existence
for f in [FILES_TO_CHECK]; do
  test -f \"$f\" && echo '✓ $f: EXISTS' || echo '✗ $f: MISSING'
done

# Content verification
grep -q '[EXPECTED]' [FILE] && echo '✓ Content correct' || echo '✗ Content incorrect'

**After Gate Check:**
1. ALL PASS: Update STATE.md with Phase [N]: COMPLETE
2. ANY FAIL: Update STATE.md with Phase [N]: FAILED, document blockers
3. DO NOT proceed if ANY check fails

**If FAILED:** Use oracle for deep analysis, then spawn review process"
```

### Error Recovery

```bash
amp threads new --mode deep --execute "You are recovering from a FAILED verification.

**Step Failed:** [STEP_NUMBER]
**Expected:** [EXPECTED]
**Actual:** [ACTUAL]

**Native AMP Tools:**
- Use **oracle** for deep debugging and root cause analysis
- Use **Librarian** to search framework docs for correct patterns
- Use **subagents** for parallel investigation of multiple hypotheses

**Available Skills:**
- ~/.agents/skills/serena-mcp-agent — Semantic code search for complex issues
- ~/.agents/skills/coding-agent — Spawn for second opinion

**Recovery Protocol:**
1. Re-read the step and phase document
2. Re-read the file, identify differences
3. Use oracle to analyze the root cause
4. Re-execute with EXACT strings from phase document
5. Re-verify
6. If still failing after 3 attempts: Update STATE.md Current Blocker, stop

**If blocked:** Spawn review process with error details"
```

### Full Sequence

```bash
amp threads new --mode rush --execute "You are a Rush-level AMP agent executing the Agent Rules Implementation.

**Project:** /home/masum/github/EmailIntelligence
**Branch:** orchestration-tools (ISOLATED - NO merges)
**Task:** Fix 13 identified issues in AI coding agent configurations

**Handoff Documents:**
- Master: docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md
- Phases: docs/handoff/phase-01 through phase-04
- State: docs/handoff/STATE.md

**Native AMP Tools Available:**
- **oracle** — Second opinion on complex decisions (use for architecture questions)
- **Librarian** — Search GitHub/Bitbucket for framework patterns
- **subagents** — Parallel work when beneficial
- **Painter** — Generate diagrams if needed for documentation

**Skills Available:**
- ~/.letta/skills/branch-isolation-guard — Enforce isolation policy
- ~/.letta/skills/agent-rules-handoff — Phase guidance
- ~/.letta/skills/tool-ecosystem-manager — Tool verification
- ~/.agents/skills/serena-mcp-agent — Semantic code search
- ~/.agents/skills/coding-agent — Spawn for parallel work or second opinion

**Critical Rules:**
1. Run VERIFY after EVERY step
2. Copy strings EXACTLY — do not paraphrase
3. One edit per tool call — do not batch
4. NEVER use git add -A or git add .
5. DO NOT merge branches (isolation policy)

**Execution Order:** Phase 1 → 2 → 3 → 4 (REQUIRED)

**Start:** Read docs/handoff/phase-01-emergency-fixes.md"
```

---

## Subagent Workflows

### Oracle (Second Opinion for Complex Analysis)

AMP's native oracle tool provides GPT-5.4 reasoning for deep analysis.

**When to use:**
- Architectural decisions
- Complex debugging
- Code review requiring deep understanding
- Uncertain about best approach

**Example prompts in AMP:**
```
"Use the oracle to review the agent rules architecture"
"Ask the oracle whether there's a simpler solution"
"Work with the oracle to figure out how to refactor this while keeping backwards compatibility"
```

**Direct CLI invocation:**
```bash
amp -x "Use the oracle to analyze the Ruler configuration and suggest improvements"
```

### Librarian (Remote Codebase Research)

AMP's native Librarian searches GitHub and Bitbucket for framework patterns.

**When to use:**
- Understanding how a library/framework works
- Finding usage examples in other projects
- Cross-referencing with official documentation
- Investigating dependency changes

**Example prompts in AMP:**
```
"Use the Librarian to search the Ruler repo for how output_path affects CLI tools"
"Ask the Librarian how Agent RuleZ hooks work"
"Search our docs repo for orchestration-tool branch patterns"
```

**Direct CLI invocation:**
```bash
amp -x "Use the Librarian to investigate how Serena MCP handles symbol navigation"
```

### Subagents (Parallel Work)

AMP's Task tool spawns independent agents for parallel work.

**When to use:**
- Multiple independent tasks
- Parallel verification
- Clean context isolation

**Example prompts:**
```
"Spawn 3 subagents to: 1) verify MCP configs, 2) check ruler.toml syntax, 3) test hooks"
"Use subagents to analyze the codebase from different perspectives"
```

### Serena MCP Agent (Semantic Code Search)

For local semantic code navigation:

```
Invoke Skill: ~/.agents/skills/serena-mcp-agent

**When to use:**
- Large codebase navigation
- Symbol-based search (find functions, classes)
- Surgical edits (modify function body, preserve structure)
- 30x token reduction vs file-based search

**Example:**
1. Activate project: "Activate /home/masum/github/EmailIntelligence"
2. Find symbol: find_symbol name:"validate_config"
3. Edit: replace_symbol_body name:"validate_config" new_body:"..."
```

### Coding Agent (External Second Opinion)

For verification via other AI tools:

```
Invoke Skill: ~/.agents/skills/coding-agent

**When to use:**
- Second opinion on complex changes
- Parallel verification of fixes
- Cross-checking gate check results

**Example (Codex):**
bash pty:true command:"codex exec 'Verify the Agent Rules phase 1 fixes are correct'"

**Example (Claude Code):**
bash pty:true command:"claude 'Review the changes to MCP configs' workdir:/home/masum/github/EmailIntelligence"
```

### Gemini CLI (Parallel Verification)

```
Invoke Skill: ~/.agents/skills/gemini

**When to use:**
- Cross-verify tool configurations
- Parallel analysis of large files

**Example:**
gemini -p "Check if all MCP configs have correct structure"
```

---

## Review Process

### When to Spawn Review

- Gate check FAILED
- Verification failed 3+ times
- Uncertain about correct approach
- Need architectural decision

### Native AMP Tools for Review

| Tool | Use Case |
|------|----------|
| **oracle** | Deep analysis of root cause, architectural evaluation |
| **Librarian** | Search framework docs for correct patterns |
| **subagents** | Parallel investigation of multiple hypotheses |
| **amp review** | Built-in code review with custom checks |

### Review Spawn Command

```bash
amp threads new --mode deep --execute "You are running a REVIEW of the Agent Rules Implementation.

**Type:** [GATE_CHECK_FAILURE|VERIFICATION_FAILURE|ARCHITECTURAL_DECISION]
**Phase:** [PHASE_NUMBER]
**Issue:** [DESCRIPTION_OF_ISSUE]
**Context:** [RELEVANT_CONTEXT]

**Use Native AMP Tools:**
- Use **oracle** to deeply analyze the root cause and propose solutions
- Use **Librarian** to search framework documentation for correct patterns
- Use **subagents** to investigate multiple hypotheses in parallel

**Available Skills:**
- ~/.letta/skills/branch-isolation-guard — Branch policy verification
- ~/.letta/skills/tool-ecosystem-manager — Tool compatibility check
- ~/.agents/skills/serena-mcp-agent — Deep code analysis
- ~/.agents/skills/coding-agent — Second opinion (spawn Codex or Claude Code)

**Review Tasks:**
1. Use oracle to analyze the failing step or decision point
2. Use Librarian to search for correct patterns in framework docs
3. Check against handoff docs and project conventions
4. Propose concrete fix OR escalate to human

**Output Format:**
## Review Summary
- Issue: [description]
- Oracle Analysis: [summary from oracle tool]
- Root Cause: [analysis]
- Recommendation: [fix or decision]
- Confidence: [high/medium/low]
- Escalate: [yes/no]

If escalate=yes, provide clear question for human decision."
```

---

## Token Optimization Notes

- **Serena MCP:** 30x token reduction for code navigation vs file-based search
- **Ruler AGENTS.md:** 33 lines vs 861 lines per agent (26x reduction)
- **CLI tools:** Read AGENTS.md directly, no output_path needed
- **Gate checks:** Batch verification commands to reduce turns

---

## Branch Isolation Reminder

**CRITICAL:** orchestration-tools branch is ISOLATED.

| From | To | Allowed? |
|------|-----|----------|
| orchestration-tools | main | ❌ NEVER |
| orchestration-tools | scientific | ❌ NEVER |
| main | orchestration-tools | ❌ NEVER |
| scientific | orchestration-tools | ❌ NEVER |

Use `scripts/distribute_files.sh` for safe file distribution.

---

## References

- Master Handoff: `docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md`
- State File: `docs/handoff/STATE.md`
- Phase Docs: `docs/handoff/phase-*.md`
- Branch Policy: `~/.letta/skills/branch-isolation-guard/SKILL.md`
- Tool Ecosystem: `~/.letta/skills/tool-ecosystem-manager/SKILL.md`
