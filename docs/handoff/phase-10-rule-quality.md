# Phase 10: Agent Rules Quality Evaluation

**Purpose:** Evaluate, improve, and validate agent file content using `verify-agent-content.sh`, `detect-branch-stack.sh`, and `agentrulegen.com`.
**Steps:** 8
**Dependencies:** Phase 9 complete (structural verification passed)
**Companion files:**
- `scripts/detect-branch-stack.sh` — Auto-detects tech stack and recommends templates per branch
- `scripts/verify-agent-content.sh` — Audits .ruler/AGENTS.md against live branch state
- `phase-10-stack-evaluation.md` — Pre-built rule-by-rule gap analysis for `orchestration-tools`
- `phase-10-references.md` — Extended tool documentation and cross-tool equivalence tables

---

## Why This Phase Exists

Structural correctness (Phase 9) confirms files exist and configs parse. This phase checks whether the **content** of those files is actually useful to agents — not redundant, not stale, and not wasting context window tokens.

Based on research (ETH Zurich, Feb 2026): LLM-generated rules files reduce task success by 3% and increase cost by 20%. Only rules the agent **cannot infer** from config files should remain.

---

## Step 10.1 — Detect branch tech stack

```bash
bash scripts/detect-branch-stack.sh
```

This script auto-detects:
- Python dependencies from `requirements.txt` / `pyproject.toml`
- JavaScript/TypeScript dependencies from `client/package.json`
- Shell script count in `modules/` and `scripts/`
- Config files that make certain rules redundant (`.flake8`, `setup.cfg`, `pytest.ini`)
- Source code patterns (async routes, SQLAlchemy, CLI architecture)

**Output:** A list of recommended agentrulegen.com templates (✅ FULL MATCH, ⚠️ PARTIAL, ⚪ SKIP) and redundancy signals.

Save the output — it drives Steps 10.3–10.5.

---

## Step 10.2 — Run structural accuracy check

```bash
bash scripts/verify-agent-content.sh
```

**PASS:** `Claimed & Stale: 0` and `Undocumented: 0`
**If failing:** Update `.ruler/AGENTS.md` to match live branch, run `ruler apply`, re-run.

---

## Step 10.3 — Import project config into agentrulegen.com Builder

1. Open `agentrulegen.com/builder`
2. Use **Import Project Config** — drag and drop the config files detected in Step 10.1:
   - `requirements.txt` if Python deps were detected
   - `client/package.json` if JS/TS deps were detected
3. The builder auto-detects the language and framework stack
4. If import doesn't capture everything, manually add languages/frameworks from the Step 10.1 output
5. Review the generated rules — note any recommendations that our `.ruler/AGENTS.md` is missing

**What to look for** (varies by branch — use Step 10.1 output):
- Rules for detected frameworks (FastAPI, React, etc.) — only if code exists on this branch
- Rules for shell script safety — only if shell script count > 10
- Git workflow rules — only for multi-branch projects

---

## Step 10.4 — Evaluate templates for stack-specific recommendations

For each template marked ✅ or ⚠️ in Step 10.1's output:

1. Read the template at `agentrulegen.com/templates/<name>`
2. For **each rule** in the template, classify it:

| Classification | Criteria | Action |
|---------------|----------|--------|
| **ALREADY COVERED** | Rule exists in `.ruler/AGENTS.md` | Skip |
| **WORTH ADDING** | Agent cannot infer from config; code pattern exists on branch | Add to `.ruler/AGENTS.md` |
| **NOT APPLICABLE** | Code pattern doesn't exist on this branch | Skip |
| **NOT WORTH ADDING** | Agent infers from config files or universal conventions | Skip |
| **REDUNDANT** | Expressed in `.flake8`, `setup.cfg`, `pytest.ini`, `package.json`, etc. | Skip |

3. Record findings in the STATE file Phase 10 Decision Log

For ⚠️ PARTIAL templates: only evaluate rules where the code pattern exists on this branch.
For ⚪ SKIP templates: skip entirely.

**Pre-built evaluation:** For the `orchestration-tools` branch, a complete rule-by-rule evaluation exists in `phase-10-stack-evaluation.md`. Use it directly instead of re-evaluating.

Also browse **Popular Rules** at `agentrulegen.com` for:
- Python rules with high upvotes
- TypeScript/React rules (if client/ exists)
- Shell scripting rules (if shell count > 10)

Record any rules worth adopting in the decision log.

---

## Step 10.5 — Analyze current rules via agentrulegen.com/analyze

1. Open `agentrulegen.com/analyze`
2. Paste the full contents of `.ruler/AGENTS.md`
3. Review the classification of each rule:

| Tier | Action |
|------|--------|
| **Essential** | Keep — agent cannot infer this from config files |
| **Helpful** | Keep — saves agent significant exploration time |
| **Redundant** | Remove — agent reads this from `.flake8`, `package.json`, `tsconfig.json`, etc. |
| **Improve Codebase** | Move to linter/formatter config instead of agent instructions |

4. Record the quality score and tier breakdown

**Repeat for Tier 2 files** (if they exist):
- `GEMINI.md`
- `QWEN.md`
- `IFLOW.md`, `CRUSH.md` (if present)

---

## Step 10.6 — Apply findings

### From the Analyzer (Step 10.5):

For each rule classified as **Redundant**:
- Verify: does a config file (`.flake8`, `setup.cfg`, `package.json`, `pytest.ini`) already express this?
- If yes → remove from `.ruler/AGENTS.md`
- If no (false positive) → keep

For each rule classified as **Improve Codebase**:
- Check if a linter rule or CI check already enforces it
- If enforceable by tooling → remove from `.ruler/AGENTS.md`, add to the appropriate config
- If not enforceable → reclassify as Essential and keep

### From the Template Evaluation (Step 10.4):

For each rule classified as **WORTH ADDING**:
- Verify it isn't already covered by existing rules
- Verify it's Essential or Helpful (not Redundant via config files)
- Add to `.ruler/AGENTS.md` under the appropriate section

**Pre-built findings for `orchestration-tools`:** See `phase-10-stack-evaluation.md` → "Consolidated Gap Analysis" section for the exact rules to add.

### After all edits:

```bash
ruler apply          # Redistribute to all agent configs
bash scripts/verify-agent-content.sh   # Confirm no drift
bash scripts/detect-branch-stack.sh    # Verify template recommendations still hold
```

---

## Step 10.7 — Check Tier 2 files for duplication and waste

For each Tier 2 file (`GEMINI.md`, `QWEN.md`):

1. **Duplicate content check:** Does it repeat rules already in `AGENTS.md` (Tier 1)?
   - If yes → remove the duplicate, keep only Tier 2-specific content
2. **MCP config block check:** Does the inline MCP config match the actual settings file?
   - Compare against `.gemini/settings.json` / `.qwen/settings.json`
3. **Vague rules check:** Does it contain "write clean code", "follow best practices", etc.?
   - If yes → remove (wastes context tokens with zero behavior change)

---

## Step 10.8 — Gate check

```bash
echo "=== PHASE 10 GATE CHECK ==="

# 1. Branch stack detection
echo "--- Stack Detection ---"
bash scripts/detect-branch-stack.sh 2>/dev/null | grep -E "^  (✅|⚠️|⚪)" | head -10

# 2. Structural accuracy
echo ""
echo "--- Structural ---"
bash scripts/verify-agent-content.sh 2>/dev/null | tail -4

# 3. Rule count (lean rules outperform verbose ones)
echo ""
echo "--- Content size ---"
echo -n ".ruler/AGENTS.md lines: "; wc -l < .ruler/AGENTS.md
echo -n "GEMINI.md lines: "; wc -l < GEMINI.md 2>/dev/null || echo "N/A"
echo -n "QWEN.md lines: "; wc -l < QWEN.md 2>/dev/null || echo "N/A"

# 4. Check for known redundant patterns
echo ""
echo "--- Redundancy check ---"
for f in .ruler/AGENTS.md GEMINI.md QWEN.md; do
    [ -f "$f" ] || continue
    echo "$f:"
    echo -n "  Vague rules: "
    grep -ci "clean code\|best practices\|write.*maintainable\|follow.*conventions" "$f" 2>/dev/null || echo "0"
    echo -n "  Config-inferable rules: "
    grep -ci "Use TypeScript\|Use React\|use black\|2-space indent" "$f" 2>/dev/null || echo "0"
done

# 5. Ruler distribution matches source
echo ""
echo "--- Distribution sync ---"
echo -n "AGENTS.md matches .ruler/AGENTS.md: "
diff <(sed -n '/^# EmailIntelligence/,$p' AGENTS.md) .ruler/AGENTS.md > /dev/null 2>&1 && echo "YES" || echo "DRIFT"
echo -n "CLAUDE.md matches .ruler/AGENTS.md: "
diff <(sed -n '/^# EmailIntelligence/,$p' CLAUDE.md) .ruler/AGENTS.md > /dev/null 2>&1 && echo "YES" || echo "DRIFT"

# 6. Stack evaluation exists for this branch
echo ""
echo "--- Stack Evaluation ---"
BRANCH="$(git branch --show-current)"
echo -n "Pre-built evaluation for $BRANCH: "
[ -f "docs/handoff/phase-10-stack-evaluation.md" ] && echo "EXISTS" || echo "MISSING"
```

**PASS criteria:**
- Stack detection runs without errors
- Structural: `Claimed & Stale: 0`, `Undocumented: 0`
- Tier 1 under 80 lines
- Zero vague/redundant patterns
- Distribution in sync (no drift)
- Stack evaluation document exists for current branch
- agentrulegen.com quality score and tier breakdown recorded in STATE

---

## agentrulegen.com Quick Reference

| Feature | URL | Use Case |
|---------|-----|----------|
| **Builder** | `agentrulegen.com/builder` | Generate rules from scratch — select language, framework, import config file |
| **Analyzer** | `agentrulegen.com/analyze` | Paste existing rules file → get Essential/Helpful/Redundant/Improve classification |
| **Templates** | `agentrulegen.com/templates` | Pre-built rule sets by stack (python-fastapi, ai-agent-workflow, git-workflow, etc.) |
| **Browse Rules** | `agentrulegen.com` → Explore → Browse | Browse community rules by language/framework, sorted by votes |
| **Popular Rules** | `agentrulegen.com` → Explore → Popular | Top community-ranked rules leaderboard |
| **Guides** | `agentrulegen.com/guides` | Setup guides per tool (Cursor, Claude Code, Copilot, Windsurf, etc.) |

### Import Config Feature

The Builder accepts drag-and-drop of project config files to auto-detect your stack:
- `requirements.txt`, `pyproject.toml`, `Pipfile` → Python + framework detection
- `package.json` → JavaScript/TypeScript + framework detection
- `go.mod`, `Cargo.toml`, `composer.json`, `Gemfile`, etc.

### Export Formats

One set of rules exports to all agent formats:
- `.cursorrules` / `.cursor/rules/*.mdc`
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.windsurfrules`
- `.clinerules`
- `GEMINI.md`

### Verbosity Levels

The Builder supports three verbosity settings:
- **Concise** — minimal rules, lowest token cost
- **Balanced** — good coverage without waste
- **Detailed** — comprehensive but higher token cost

For this project, prefer **Concise** or **Balanced** to keep context window efficient.

---

## Reference Material

For extended tool documentation, config syntax, and cross-tool equivalence tables, see `docs/handoff/phase-10-references.md` (reference appendix).
