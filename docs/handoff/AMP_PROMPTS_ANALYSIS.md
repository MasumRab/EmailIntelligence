# AMP Prompts Analysis — Tool Improvements

**Purpose:** Analyze each AMP prompt for tool optimizations  
**Created:** 2026-04-09

---

## Prompt 1: `full_task_execution`

**Current State:** Generic text prompts agent to read docs and execute.

**Issues:**
- No progress tracking — agent may skip steps
- No forced verification — relies on "trust me" approach
- No parallel execution — sequential by default

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Auto-create todo list** | TodoWrite | Add at prompt start: `TodoWrite with phases 1-4 steps` |
| **Force verification loops** | Bash | Add explicit VERIFY commands with expected output |
| **Track state automatically** | Write/Edit | After each phase, auto-update STATE.md |
| **Enable parallel research** | Task | For phases 6-8, spawn parallel explore agents |
| **Gate check enforcement** | Bash | If gate fails, STOP with clear error message |

**Improved Prompt Section:**

```markdown
**START PROTOCOL:**

1. IMMEDIATELY run TodoWrite to track all phase steps
2. Read docs/handoff/STATE.md for current progress
3. For each step:
   a. Execute the step (Edit/Write/Bash)
   b. Run VERIFY command from phase document
   c. If PASS: Update TodoWrite, proceed
   d. If FAIL: Update STATE.md blocker, STOP

**CRITICAL:** Do NOT proceed to next step if VERIFY fails.
```

**Token Savings:** ~200 tokens (auto-tracked progress vs manual)

---

## Prompt 2: `phase_specific_execution`

**Current State:** Phase-by-phase execution with verification.

**Issues:**
- Repetitive verification commands
- No automatic handoff on completion
- State file may drift from actual

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Read phase file automatically** | Read | Add: `Read docs/handoff/phase-0X-*.md as first action` |
| **Parse step count** | Bash | `grep -c "^## Step" phase-*.md` |
| **Auto-update STATE.md** | Write | After each step, write status |
| **Handoff prompt generation** | memory | Store handoff template, auto-fill on PASS |
| **Error escalation** | AskUserQuestion | If blocked, ask user for resolution strategy |

**Improved Prompt Section:**

```markdown
**EXECUTION PROTOCOL:**

1. Read `docs/handoff/phase-0[N]-[name].md`
2. Parse step count: `grep -c "^## Step" docs/handoff/phase-*.md`
3. Initialize STATE.md if missing with current phase
4. For each step:
   a. Execute step action
   b. Run VERIFY command
   c. Write result to STATE.md step tracker
5. After all steps: Run GATE CHECK
6. If PASS: Write handoff prompt to STATE.md
7. If FAIL: AskUserQuestion for resolution path
```

---

## Prompt 3: `ruler_sync_execution`

**Current State:** Manual Ruler commands with expected targets.

**Issues:**
- No pre-check for required files
- No comparison of before/after
- Backup files may be left scattered

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Pre-validate dependencies** | Bash | Check `.ruler/AGENTS.md` exists and valid |
| **Dry-run first** | Bash | Always run `ruler apply --dry-run` before apply |
| **Diff analysis** | Bash | Use `ruler apply --dry-run 2>&1 \| grep -E "^Writing|^Skipping"` |
| **Backup management** | Glob | Find and list `.bak` files after apply |
| **Parallel verification** | Task | Spawn verify agents for each target file |

**Improved Prompt Section:**

```markdown
**PRE-CHECK:**
```bash
test -f .ruler/ruler.toml || { echo "FAIL: ruler.toml missing"; exit 1 }
test -f .ruler/AGENTS.md || { echo "FAIL: AGENTS.md missing"; exit 1 }
grep -q "EmailIntelligence" .ruler/AGENTS.md || { echo "FAIL: No project content"; exit 1 }
```

**DRY-RUN FIRST:**
```bash
ruler apply --project-root . --dry-run 2>&1 | tee /tmp/ruler-dryrun.log
```

**APPLY:**
```bash
ruler apply --project-root . --backup
find . -name "*.bak" -type f  # List backups created
```
```

---

## Prompt 4: `agent_rulez_runtime`

**Current State:** RuleZ debug commands with expected behaviors.

**Issues:**
- No automatic rule installation check
- Debug scenarios are manual
- No coverage report for all rules

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Binary check** | Bash | `which rulez || echo "INSTALL FIRST"` |
| **Config validation** | Bash | `python3 -c "import yaml; yaml.safe_load(open('.claude/hooks.yaml'))"` |
| **Batch debug scenarios** | Write | Create `rulez_test_scenarios.yaml` with all test cases |
| **Coverage report** | Task | Run all debug tests, collect BLOCKED/ALLOWED results |
| **Interactive rule testing** | Skill | Create `/rulez-test` skill for repeated testing |

**Improved Prompt Section:**

```markdown
**VALIDATION SUITE:**

1. Check binary: `which rulez && rulez --version`
2. Validate config: `rulez validate --config .claude/hooks.yaml`
3. Lint for overlaps: `rulez lint --config .claude/hooks.yaml`

**DEBUG SCENARIOS (batch):**
```bash
for scenario in "Bash:git push --force origin main" \
                "Bash:git reset --hard" \
                "Bash:git add -A" \
                "Bash:cat .env" \
                "Edit:src/main.py"; do
  result=$(/tmp/rulez/rulez debug --config .claude/hooks.yaml --event "$scenario" 2>&1)
  echo "$scenario: $result"
done
```

**EXPECTED:**
- git push --force: BLOCKED
- git reset --hard: BLOCKED  
- git add -A: BLOCKED
- cat .env: BLOCKED
- Edit:src/main.py: ALLOWED with inject
```

---

## Prompt 5: `content_bootstrap`

**Current State:** Manual browser workflow + customization.

**Issues:**
- No API integration with agentrulegen.com
- Manual copy-paste introduces errors
- No validation of generated content

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Web content fetch** | fetch_webpage | Fetch templates directly from agentrulegen.com |
| **Content extraction** | Bash | Parse and extract rules from fetched HTML |
| **Validation** | Read | Compare generated vs AGENTS.md best practices |
| **Template library** | memory | Store common templates in Letta memory for reuse |
| **Auto-customize** | Write | Inject project-specific sections automatically |

**Improved Prompt Section:**

```markdown
**FETCH TEMPLATES:**

1. Fetch Python/FastAPI template:
   ```
   fetch_webpage("https://agentrulegen.com/templates/python-fastapi")
   ```
   Extract rules from returned content

2. Fetch TypeScript/React template:
   ```
   fetch_webpage("https://agentrulegen.com/templates/typescript-react")
   ```

3. Combine and customize:
   - Add Key Directories section
   - Add Task Master integration
   - Add Critical Rules

4. Write to `.ruler/AGENTS.md`

5. Validate:
   - Line count between 80-200
   - Has sections: Code Style, Architecture, Testing
   - No duplications with existing CLAUDE.md
```

---

## Prompt 6: `error_recovery`

**Current State:** Manual recovery steps.

**Issues:**
- No automatic diagnosis
- Relies on agent to self-correct
- No escalation path

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Auto-diagnosis** | Read + Grep | Read failed file, grep for expected pattern |
| **Diff generation** | Bash | `diff <(echo "$expected") <(cat "$file")` |
| **Suggested fix** | Edit | Auto-generate edit_file call with correct params |
| **Escalation** | AskUserQuestion | If auto-fix fails 3 times, ask for human help |
| **Error logging** | memory | Store error patterns for future reference |

**Improved Prompt Section:**

```markdown
**AUTO-DIAGNOSIS:**

1. Read the failed file: `Read [FILE_PATH]`
2. Grep for expected content: `grep -n "[EXPECTED_STRING]" [FILE]`
3. If not found, show context: `grep -C 5 "[PARTIAL_MATCH]" [FILE]`
4. Generate diff:
   ```bash
   diff <(echo "[EXPECTED]") <(cat [FILE]) || echo "DIFF GENERATED"
   ```
5. Suggest fix: Generate Edit call with exact old_string/new_string
6. Re-verify
7. If 3 failures: AskUserQuestion with options:
   - Skip step
   - Manual intervention
   - Abort phase
```

---

## Prompt 7: `token_optimization`

**Current State:** Manual token calculation and analysis.

**Issues:**
- No automated scanning
- Deduplication is manual
- No before/after comparison

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Automated scanning** | Glob + Bash | Scan all `.md` files, calculate token loads |
| **Duplication detection** | Task | Spawn explore agent to find duplicate sections |
| **Before/after diff** | Bash | Store original token count, compare after |
| **Auto-consolidation** | Edit | Move duplicates to AGENTS.md, remove from tools |
| **Visualization** | Write | Generate token usage report as markdown table |

**Improved Prompt Section:**

```markdown
**AUTOMATED SCAN:**

```bash
echo "# Token Usage Report" > /tmp/token-report.md
echo "" >> /tmp/token-report.md

for file in $(find . -name "*.md" -path "./.cursor/*" -o -path "./.claude/*" -o -path "./.roo/*" -o -path "./.windsurf/*"); do
  lines=$(wc -l < "$file")
  tokens=$((lines * 5))
  echo "- $file: $lines lines (~$tokens tokens)" >> /tmp/token-report.md
done

total=$(find . -name "*.md" \( -path "./.cursor/*" -o -path "./.claude/*" -o -path "./.roo/*" \) -exec cat {} \; | wc -l)
echo "" >> /tmp/token-report.md
echo "**Total:** $total lines (~$((total * 5)) tokens)" >> /tmp/token-report.md
```

**DUPLICATION CHECK:**
Use Task agent to find duplicate section headers across all rule files.

**CONSOLIDATION:**
For each duplicate:
1. Check if content in AGENTS.md
2. If not, add to AGENTS.md
3. Remove from tool-specific file
4. Add import reference (tool-specific)
```

---

## Prompt 8: `verification_loop`

**Current State:** 8 manual verification loops.

**Issues:**
- No parallel execution
- No aggregation of results
- No final pass/fail determination

**Recommended Tool Improvements:**

| Improvement | Tool | Implementation |
|------------|------|----------------|
| **Parallel loops** | Task | Spawn 4 agents for loops 1-4, 4 agents for loops 5-8 |
| **Result aggregation** | Write | Collect all results into verification-report.md |
| **Auto-fix** | Edit | For failures, attempt auto-fix with error_recovery |
| **Pass/fail matrix** | Write | Generate final status table |
| **CI integration** | Bash | Generate exit code 0 (pass) or 1 (fail) |

**Improved Prompt Section:**

```markdown
**PARALLEL VERIFICATION:**

Spawn 4 Task agents in parallel:
- Agent 1: Loops 1-2 (file checks)
- Agent 2: Loops 3-4 (MCP + context tests)
- Agent 3: Loops 5-6 (cross-tool parity)
- Agent 4: Loops 7-8 (RuleSync + RuleZ)

**COLLECT RESULTS:**
```bash
cat > docs/handoff/VERIFICATION_REPORT.md << 'EOF'
# Verification Report

**Date:** $(date)
**Branch:** $(git branch --show-current)

## Results

| Loop | Status | Details |
|------|--------|---------|
| 1 | PASS/FAIL | |
| 2 | PASS/FAIL | |
| ... | ... | |

## Final Status

**PASS:** All verification loops passed
**FAIL:** [X] loops failed — see details above
EOF
```

**EXIT CODE:**
```bash
# If any loop failed, exit 1
grep -q "FAIL" docs/handoff/VERIFICATION_REPORT.md && exit 1 || exit 0
```
```

---

## Summary: Tool Improvement Matrix

| Prompt | Highest Impact Tool | Savings |
|--------|---------------------|---------|
| full_task_execution | **TodoWrite** | ~200 tokens (auto-tracked) |
| phase_specific_execution | **Read + Write** | ~150 tokens (auto-state) |
| ruler_sync_execution | **Bash (dry-run)** | ~100 tokens (catch issues early) |
| agent_rulez_runtime | **Task (batch tests)** | ~300 tokens (parallel testing) |
| content_bootstrap | **fetch_webpage** | ~500 tokens (no manual copy) |
| error_recovery | **AskUserQuestion** | ~400 tokens (escalation path) |
| token_optimization | **Task + Glob** | ~350 tokens (parallel scan) |
| verification_loop | **Task (parallel)** | ~800 tokens (4x speedup) |

**Total Potential Savings:** ~2,800 tokens per full execution

---

## Recommended Default AMP Skills

Based on analysis, create these AMP-specific skills:

| Skill | Purpose | Reusability |
|-------|---------|-------------|
| `/verify-step` | Auto-verify with expected output check | High |
| `/gate-check` | Run phase gate check and report | High |
| `/update-state` | Write/update STATE.md with progress | High |
| `/collect-results` | Aggregate parallel agent results | Medium |
| `/escalate-error` | Auto-diagnose and escalate failures | Medium |
