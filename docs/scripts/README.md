# Analysis Scripts Documentation

This directory contains automation scripts for analyzing agent configurations and Jules sessions.

---

## Scripts Overview

| Script | Language | Purpose |
|--------|----------|---------|
| `scripts/analyze_agent_rules.py` | Python + Playwright | Browser automation for agentrulegen.com/analyze |
| `scripts/analyze_agent_rules.mjs` | Node.js + Playwright | Same tool in JavaScript |
| `scripts/docs_content_analyzer.py` | Python | Analyze documentation structure |

---

## `analyze_agent_rules.py` / `.mjs`

### Purpose

Submit agent configuration files to [agentrulegen.com/analyze](https://agentrulegen.com/analyze) and scrape results.

### Why Browser Automation?

agentrulegen.com has no API. This script:
1. Launches headless Chromium
2. Navigates to /analyze
3. Pastes config file content
4. Clicks "Analyze" button
5. Scrapes and returns structured results

### Requirements

```bash
# Python
pip install playwright
playwright install chromium

# Node.js
npm install playwright
npx playwright install chromium
```

### Usage

```bash
# Python version
python scripts/analyze_agent_rules.py .ruler/AGENTS.md
python scripts/analyze_agent_rules.py .claude/hooks.yaml
python scripts/analyze_agent_rules.py rulesync.jsonc

# Node.js version
node scripts/analyze_agent_rules.mjs .ruler/AGENTS.md
node scripts/analyze_agent_rules.mjs .claude/hooks.yaml rulesync.jsonc
```

### Output

Returns JSON with categories:
```json
{
  "file": ".ruler/AGENTS.md",
  "charCount": 1250,
  "redundant": ["Duplicate TypeScript rules", "Redundant import patterns"],
  "essential": ["Security guidelines", "Testing requirements"],
  "improvable": ["Could add TypeScript conventions"],
  "missing": ["No React patterns specified"]
}
```

---

## Integration with AMP CLI

These scripts can be invoked from AMP commands to validate agent configurations during handoff phases.

### AMP Command Reference

Add to AMP prompts:

```
**Analysis Scripts:**
- scripts/analyze_agent_rules.py — Browser automation for agentrulegen.com
- scripts/analyze_agent_rules.mjs — Node.js version

**Usage in AMP Session:**
"Run scripts/analyze_agent_rules.py on .ruler/AGENTS.md and report redundant patterns"
"Analyze .claude/hooks.yaml for missing security rules"
```

### Example AMP Phase Integration

#### Phase 3: Ruler Setup (Post-Ruler Verification)

```bash
amp threads new --mode rush --execute "You are verifying Ruler output.

**Script Available:**
scripts/analyze_agent_rules.py — Submit AGENTS.md to agentrulegen.com/analyze

**Tasks:**
1. Run: python scripts/analyze_agent_rules.py .ruler/AGENTS.md
2. Review 'redundant' items — simplify if possible
3. Review 'missing' items — add if critical
4. Re-run Ruler if changes needed

**Expected:**
- No critical missing items
- Minimal redundant content"
```

#### Phase 6: Deduplication

```bash
amp threads new --mode smart --execute "You are deduplicating agent rules content.

**Script Available:**
scripts/analyze_agent_rules.py — Detect redundant patterns

**Tasks:**
1. Analyze each agent config file
2. Cross-reference with .ruler/AGENTS.md
3. Identify duplicated rules across files
4. Remove duplicates, keep single source of truth in AGENTS.md

**Usage:**
python scripts/analyze_agent_rules.py .cursor/rules/system.md
python scripts/analyze_agent_rules.py .windsurf/rules/windsurf_rules.md"
```

---

## Jules Session Analysis

### Integration with `jules_sessions/`

The analysis scripts can process Jules session files:

```bash
# Analyze all Jules patches for patterns
python scripts/analyze_agent_rules.py --jules-sessions jules_sessions/

# Extract optimization patterns from Jules output
python scripts/analyze_agent_rules.py --extract-patterns jules_sessions/pr571_session.json
```

### Use in AMP Commands

```
"Run analyze_agent_rules.py on the Jules sessions for pr571 and summarize optimization patterns"
```

---

## Adding New Analysis Capabilities

### Extending `analyze_agent_rules.py`

```python
# Add new analysis mode
async def analyze_with_llm(file_path: str) -> dict:
    """Use LLM to suggest improvements beyond rulegen output."""
    # ... implementation
```

### Creating New Scripts

Place in `scripts/` and document here:

| Script | Purpose |
|--------|---------|
| `scripts/YOUR_SCRIPT.py` | Description |

---

## AMP Commands Document

For full AMP CLI integration, see `docs/handoff/AMP_COMMANDS.md` on the `orchestration-tools` branch.

### Cross-Branch Access

```bash
# View AMP commands from orchestration-tools
git show origin/orchestration-tools:docs/handoff/AMP_COMMANDS.md

# Or checkout that file temporarily
git show origin/orchestration-tools:docs/handoff/AMP_COMMANDS.md > /tmp/amp_commands.md
```

---

## Maintenance

### Update Requirements

```bash
# Check for Playwright updates
pip install --upgrade playwright
npx playwright install chromium
```

### Validate Script Functionality

```bash
# Test script still works with agentrulegen.com
python scripts/analyze_agent_rules.py .ruler/AGENTS.md --test
```

---

## References

- [agentrulegen.com](https://agentrulegen.com) — Online agent rules analyzer
- [Playwright Documentation](https://playwright.dev/python/)
- `jules_sessions/README.md` — Jules session tracking documentation
- `docs/handoff/AMP_COMMANDS.md` (orchestration-tools branch) — Full AMP command reference
