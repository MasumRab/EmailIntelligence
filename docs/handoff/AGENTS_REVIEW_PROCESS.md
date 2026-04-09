# Agents Review Process Plan

**Purpose:** Comprehensive review protocol for AI coding agent configurations across EmailIntelligence  
**Created:** 2026-04-09  
**Branch:** orchestration-tools

---

## Overview

This document defines a systematic review process for evaluating AI coding agent rules, tools, and context across EmailIntelligence worktrees and branches.

---

## Phase 0: Context Discovery

### Step 0.1 — Identify Current Tool Context

**Questions to answer:**

| Question | How to Check |
|----------|--------------|
| What AI tool am I using? | Check `$TERM`, `claude --version`, `cursor --version`, etc. |
| What project am I in? | `pwd`, `git remote -v`, `git branch --show-current` |
| What memory system is active? | Check `$MEMORY_DIR`, `~/.letta/agents/` |
| What skills are loaded? | Check `$SKILLS_DIR` or `~/.letta/skills/` |
| What MCP servers are configured? | Check `.mcp.json`, `.claude/mcp.json`, `.cursor/mcp.json` |

**Commands:**

```bash
# Current context discovery
echo "=== CURRENT CONTEXT ==="
echo "Tool: Letta Code"
echo "Agent ID: $AGENT_ID"
echo "Conversation: $CONVERSATION_ID"
echo "Memory Dir: $MEMORY_DIR"

# Project context
echo "=== PROJECT CONTEXT ==="
echo "Directory: $(pwd)"
echo "Branch: $(git branch --show-current)"
echo "Remote: $(git remote -v | head -1)"
echo "Last commit: $(git log -1 --oneline)"

# Tool context
echo "=== TOOL CONTEXT ==="
echo "Ruler installed: $(which ruler 2>/dev/null || echo 'NO')"
echo "RuleZ installed: $(which rulez 2>/dev/null || echo 'NO')"
echo "Node version: $(node --version 2>/dev/null || echo 'NO')"
echo "Python version: $(python3 --version 2>/dev/null || echo 'NO')"
```

---

### Step 0.2 — Identify All Agent Config Files

**Files to check:**

```bash
# Root-level agent files
ls -la AGENTS.md CLAUDE.md GEMINI.md QWEN.md IFLOW.md CRUSH.md LLXPRT.md 2>/dev/null

# Tool-specific directories
ls -la .cursor/rules/ .claude/rules/ .roo/rules*/ .windsurf/rules/ .trae/rules/ .kiro/steering/ .clinerules/ .cursor/mcp.json .claude/mcp.json .roo/mcp.json .windsurf/mcp.json .trae/mcp.json 2>/dev/null

# Sync tool configs
ls -la .ruler/ruler.toml .ruler/AGENTS.md rulesync.jsonc .claude/hooks.yaml 2>/dev/null
```

---

## Phase 1: Tool Inventory Review

### Step 1.1 — Ruler Configuration Review

**Checklist:**

```bash
echo "=== RULER CONFIG REVIEW ==="

# Does .ruler/ exist?
test -d .ruler && echo "✅ .ruler/ directory exists" || echo "❌ .ruler/ missing"

# Is ruler.toml valid?
python3 -c "import tomllib; tomllib.load(open('.ruler/ruler.toml', 'rb'))" 2>/dev/null && echo "✅ ruler.toml valid TOML" || echo "❌ ruler.toml invalid"

# Count enabled agents
echo -n "Enabled agents: "
grep -c "enabled = true" .ruler/ruler.toml 2>/dev/null || echo "0"

# Check AGENTS.md exists
test -f .ruler/AGENTS.md && echo "✅ .ruler/AGENTS.md exists ($(wc -l < .ruler/AGENTS.md) lines)" || echo "❌ .ruler/AGENTS.md missing"

# Check MCP server config
grep -q "\[mcp_servers\." .ruler/ruler.toml && echo "✅ MCP servers configured" || echo "⚠️ No MCP servers"
```

---

### Step 1.2 — RuleSync Configuration Review

**Checklist:**

```bash
echo "=== RULESYNC CONFIG REVIEW ==="

# Does rulesync.jsonc exist?
test -f rulesync.jsonc && echo "✅ rulesync.jsonc exists" || echo "❌ rulesync.jsonc missing"

# Is it valid JSONC?
python3 -c "import json; json.load(open('rulesync.jsonc'))" 2>/dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

# Count targets
echo -n "Targets: "
python3 -c "import json; d=json.load(open('rulesync.jsonc')); print(len(d.get('targets', [])))" 2>/dev/null || echo "0"
```

---

### Step 1.3 — Agent RuleZ Configuration Review

**Checklist:**

```bash
echo "=== AGENT RULEZ CONFIG REVIEW ==="

# Does hooks.yaml exist?
test -f .claude/hooks.yaml && echo "✅ .claude/hooks.yaml exists" || echo "❌ hooks.yaml missing"

# Is it valid YAML?
python3 -c "import yaml; yaml.safe_load(open('.claude/hooks.yaml'))" 2>/dev/null && echo "✅ Valid YAML" || echo "❌ Invalid YAML"

# Count rules
echo -n "Rules configured: "
grep -c "^  - name:" .claude/hooks.yaml 2>/dev/null || echo "0"

# Check if rulez binary is installed
which rulez 2>/dev/null && echo "✅ rulez binary installed" || echo "❌ rulez not installed"
```

---

## Phase 2: MCP Configuration Review

### Step 2.1 — Check All MCP Files

```bash
echo "=== MCP CONFIGURATION REVIEW ==="

for tool in .roo .cursor .claude .windsurf .trae; do
  mcp_file="$tool/mcp.json"
  if [ -f "$mcp_file" ]; then
    # Check if valid JSON
    python3 -c "import json; json.load(open('$mcp_file'))" 2>/dev/null
    if [ $? -eq 0 ]; then
      # Check if populated (not empty)
      size=$(wc -c < "$mcp_file")
      if [ "$size" -gt 50 ]; then
        echo "✅ $mcp_file: VALID ($size bytes)"
      else
        echo "⚠️ $mcp_file: VALID but small ($size bytes)"
      fi
    else
      echo "❌ $mcp_file: INVALID JSON"
    fi
  else
    echo "❌ $mcp_file: MISSING"
  fi
done
```

### Step 2.2 — Check MCP Server Consistency

```bash
echo "=== MCP SERVER CONSISTENCY ==="

# Check task-master-ai server config
echo "Task Master AI MCP server:"
for tool in .roo .cursor .claude .windsurf .trae; do
  mcp_file="$tool/mcp.json"
  if [ -f "$mcp_file" ]; then
    has_tm=$(python3 -c "import json; d=json.load(open('$mcp_file')); print('task-master-ai' in d.get('mcpServers', {}))" 2>/dev/null)
    if [ "$has_tm" = "True" ]; then
      echo "✅ $tool: task-master-ai configured"
    else
      echo "❌ $tool: task-master-ai missing"
    fi
  fi
done
```

---

## Phase 3: Content Quality Review

### Step 3.1 — Check AGENTS.md Quality

```bash
echo "=== AGENTS.md CONTENT REVIEW ==="

# Check key sections
for section in "Project Overview" "Code Conventions" "Build Commands" "Key Directories" "Task Management" "Critical Rules"; do
  if grep -qi "$section" .ruler/AGENTS.md 2>/dev/null; then
    echo "✅ Has section: $section"
  else
    echo "❌ Missing section: $section"
  fi
done

# Check line count
lines=$(wc -l < .ruler/AGENTS.md 2>/dev/null || echo "0")
if [ "$lines" -lt 20 ]; then
  echo "⚠️ AGENTS.md is brief ($lines lines) — consider expanding"
elif [ "$lines" -gt 200 ]; then
  echo "⚠️ AGENTS.md is long ($lines lines) — consider splitting"
else
  echo "✅ AGENTS.md length is reasonable ($lines lines)"
fi
```

### Step 3.2 — Check for Duplicated Content

```bash
echo "=== DUPLICATION CHECK ==="

# Compare CLAUDE.md to AGENTS.md
if [ -f CLAUDE.md ] && [ -f AGENTS.md ]; then
  common=$(comm -12 <(sort CLAUDE.md) <(sort AGENTS.md) | wc -l)
  echo "Common lines between CLAUDE.md and AGENTS.md: $common"
fi

# Check for Prisma references (if not using Prisma)
prisma_refs=$(grep -rl "prisma" .cursor/rules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l)
if [ "$prisma_refs" -gt 0 ]; then
  echo "⚠️ Found Prisma references in $prisma_refs files (project doesn't use Prisma)"
else
  echo "✅ No Prisma references found"
fi
```

---

## Phase 4: Token Usage Analysis

### Step 4.1 — Calculate Token Impact

```bash
echo "=== TOKEN USAGE ANALYSIS ==="

# Count lines in each agent config file
for file in AGENTS.md CLAUDE.md GEMINI.md QWEN.md; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file")
    tokens=$((lines * 5))  # rough estimate: 5 tokens per line
    echo "$file: $lines lines (~$tokens tokens)"
  fi
done

# Count lines in rule directories
for dir in .cursor/rules .claude/rules .roo/rules .windsurf/rules .trae/rules .kiro/steering; do
  if [ -d "$dir" ]; then
    lines=$(find "$dir" -name "*.md" -exec cat {} \; 2>/dev/null | wc -l)
    tokens=$((lines * 5))
    echo "$dir: $lines lines (~$tokens tokens)"
  fi
done
```

### Step 4.2 — Identify Token Hotspots

```bash
echo "=== TOKEN HOTSPOTS ==="

# Find files over 100 lines
find . -name "*.md" -path "./.cursor/*" -o -path "./.claude/*" -o -path "./.roo/*" -o -path "./.windsurf/*" -o -path "./.trae/*" -o -path "./.kiro/*" | while read f; do
  lines=$(wc -l < "$f" 2>/dev/null || echo "0")
  if [ "$lines" -gt 100 ]; then
    echo "⚠️ Large file: $f ($lines lines)"
  fi
done
```

---

## Phase 5: Skills & Extensions Review

### Step 5.1 — Check Letta Code Skills

```bash
echo "=== LETTA CODE SKILLS REVIEW ==="

# List available skills
ls -la ~/.letta/skills/ 2>/dev/null || echo "Skills directory not found"

# Count skills
skill_count=$(find ~/.letta/skills -name "SKILL.md" 2>/dev/null | wc -l)
echo "Skills available: $skill_count"

# Check memory files
ls -la ~/.letta/agents/$AGENT_ID/memory/system/ 2>/dev/null | head -10
```

### Step 5.2 — Check MCP Extensions

```bash
echo "=== MCP EXTENSIONS REVIEW ==="

# List MCP servers in root .mcp.json
if [ -f ".mcp.json" ]; then
  python3 -c "import json; d=json.load(open('.mcp.json')); print('\\n'.join(d.get('mcpServers', {}).keys()))" 2>/dev/null
fi
```

---

## Phase 6: Branch & Worktree Context

### Step 6.1 — Check Sibling Worktrees

```bash
echo "=== SIBLING WORKTREES REVIEW ==="

# List worktrees
git worktree list

# Check sibling directories
for dir in ~/github/EmailIntelligence*; do
  if [ -d "$dir" ] && [ "$dir" != "$(pwd)" ]; then
    branch=$(cd "$dir" && git branch --show-current 2>/dev/null)
    echo "📁 $dir → $branch"
  fi
done
```

### Step 6.2 — Compare Agent Files Across Worktrees

```bash
echo "=== CROSS-WORKTREE COMPARISON ==="

# Compare CLAUDE.md
for dir in ~/github/EmailIntelligence*; do
  if [ -f "$dir/CLAUDE.md" ]; then
    lines=$(wc -l < "$dir/CLAUDE.md")
    echo "CLAUDE.md in $dir: $lines lines"
  fi
done
```

---

## Review Summary Template

```markdown
## Agents Review Summary

**Date:** YYYY-MM-DD
**Project:** EmailIntelligence
**Branch:** orchestration-tools
**Reviewer:** [Agent Name]

### Tool Context
- Primary Tool: Letta Code
- Memory System: Letta Memory ($MEMORY_DIR)
- Skills Loaded: X
- MCP Servers: X

### Configuration Status
| Component | Status | Notes |
|-----------|--------|-------|
| Ruler | ✅/❌ | |
| RuleSync | ✅/❌ | |
| Agent RuleZ | ✅/❌ | |
| MCP configs | ✅/❌ | |

### Content Quality
- AGENTS.md: X lines, [quality assessment]
- Duplications found: X
- Token hotspots: [list]

### Issues Found
1. [Issue description]
2. [Issue description]

### Recommendations
1. [Recommendation]
2. [Recommendation]
```

---

## Execution Commands

### Quick Review (One Command)

```bash
echo "=== AGENTS REVIEW QUICK CHECK ==="
echo "Branch: $(git branch --show-current)"
echo "Ruler: $(test -f .ruler/ruler.toml && echo 'CONFIGURED' || echo 'MISSING')"
echo "RuleZ: $(test -f .claude/hooks.yaml && echo 'CONFIGURED' || echo 'MISSING')"
echo "RuleSync: $(test -f rulesync.jsonc && echo 'CONFIGURED' || echo 'MISSING')"
echo "MCP files: $(find . -name 'mcp.json' -not -path './node_modules/*' | wc -l) found"
echo "Skills: $(find ~/.letta/skills -name 'SKILL.md' 2>/dev/null | wc -l) available"
```

### Full Review Script

Save as `scripts/agents-review.sh`:

```bash
#!/bin/bash
# Agents Review Process — Full Execution
# Usage: ./scripts/agents-review.sh

set -e

echo "# Agents Review Report"
echo "Date: $(date)"
echo "Project: $(pwd)"
echo "Branch: $(git branch --show-current)"

# Run all phases
bash -c "$(cat <<'SCRIPT'
# Phase 0
echo "## Phase 0: Context Discovery"
echo "..."
# Phase 1
echo "## Phase 1: Tool Inventory Review"
echo "..."
# Phase 2-6...
SCRIPT
)"
```

---

## Related Documents

- `docs/handoff/phase-10-references.md` — agentrulegen.com guides
- `docs/handoff/README.md` — Tool coverage matrix
- `docs/SIBLING_WORKTREES_AGENT_FILES_ANALYSIS.md` — IFLOW/CRUSH/LLXPRT analysis
