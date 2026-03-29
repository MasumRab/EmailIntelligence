# Orchestration Process & Strategy Switching Guide

## Overview

This guide outlines the complete orchestration cleanup and Strategy 5/7 switching process, including context contamination handling and tool-based deployment.

---

## Part 1: Context Contamination Cleanup Process

### Problem
Agent tools accumulate context (application code, config files) on orchestration-tools branch. This must be cleaned before main integration.

### Cleanup Process

#### Phase 1: Identify & Revert Contamination

```bash
# On orchestration-tools branch
./scripts/validate-orchestration-context.sh

# If contamination found, identify problematic commit
git log --oneline | grep -E "Merge|contamination"

# Revert the contamination commit
git revert <commit-sha>
git push origin orchestration-tools
```

**Expected Result:** Exit code 0 from validation script

#### Phase 2: Test Strategy Implementation

```bash
# Switch to orchestration-tools-changes
git checkout orchestration-tools-changes

# Simulate multi-agent pushes
for i in {1..3}; do
  echo "change $i" >> test_file.txt
  git add test_file.txt
  git commit -m "test: simulated push $i"
  git push origin orchestration-tools-changes
done

# Verify debounce file creation (Strategy 5)
ls -la .orchestration-push-debounce 2>/dev/null && echo "✓ Debounce active"
```

#### Phase 3: Deploy & Cleanup

```bash
# Remove test artifacts
rm -f test_file.txt multi_test.txt test_push_marker.txt
git add -A
git commit -m "chore: remove test artifacts"
git push origin orchestration-tools-changes

# Validate clean context
./scripts/validate-orchestration-context.sh
# Should report: 0 issues on orchestration-tools branch
```

---

## Part 2: Strategy Switching (Tool-Based)

### Strategy 5: Default (Branch Aggregation)

**When to use:** Normal operations, multiple incremental pushes

**Implementation:**
```bash
# 1. Push to orchestration-tools-changes (not orchestration-tools directly)
git checkout orchestration-tools-changes
git push origin orchestration-tools-changes

# 2. Post-commit hook detects branch
# Hook checks: .orchestration-push-debounce file
# If exists: aggregates changes (prevents PR creation)
# If not exists: sets debounce, waits 5 seconds

# 3. After debounce clears
# Single PR created: orchestration-tools-changes → orchestration-tools
```

**Configuration:**
```bash
# Debounce timeout (seconds)
DEBOUNCE_TIMEOUT=5  # in .git/hooks/post-commit

# To adjust: Edit hook on orchestration-tools branch
git checkout orchestration-tools
nano .git/hooks/post-commit
# Change: DEBOUNCE_TIMEOUT=10 (or desired value)
git commit -am "config: adjust debounce timeout"
git push origin orchestration-tools
```

**Status Check:**
```bash
# Check if debounce is active
cat .orchestration-push-debounce 2>/dev/null && echo "Debounce active" || echo "No debounce"

# Check push state
cat .orchestration-push-state

# Validate context (should pass)
./scripts/validate-orchestration-context.sh
```

---

### Strategy 7: Fallback (Hybrid - Strategy 5 + Metadata)

**When to use:** If Strategy 5 fails or race conditions detected

**Activation:**

```bash
# 1. Identify Strategy 5 failure
# Symptoms: duplicate PRs despite debounce, race conditions, merge conflicts

# 2. Enable Strategy 7 (keep Strategy 5, add git notes + warnings)
git checkout orchestration-tools
git pull origin orchestration-tools

# 3. Add git notes metadata tracking
git notes add -m "Push strategy: hybrid (5+7)
Timestamp: $(date)
Debounce: 5s
Metadata: git notes tracking enabled"

# 4. Update hook to write notes on push
# Edit .git/hooks/post-commit
nano .git/hooks/post-commit

# Add after debounce logic:
git notes add -m "Aggregated push at $(date +%s)" || true

# 5. Add pre-push warning hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" == "orchestration-tools-changes" ]]; then
  echo "⚠️  Strategy 7 active: Hybrid debounce + metadata tracking"
  echo "Push will be aggregated (5s wait). Control+C to cancel."
  sleep 2
fi
EOF
chmod +x .git/hooks/pre-push

# 6. Commit and push
git add .git/hooks/post-commit .git/hooks/pre-push
git commit -m "chore: enable Strategy 7 hybrid (debounce + git notes + warnings)"
git push origin orchestration-tools

# 7. Verify
git notes list | head -3  # See accumulated metadata
```

**Comparison: Strategy 5 vs Strategy 7**

| Feature | Strategy 5 | Strategy 7 |
|---------|-----------|-----------|
| Branch Aggregation | ✓ | ✓ |
| Debounce Logic | ✓ | ✓ |
| Git Notes Metadata | — | ✓ |
| Pre-push Warnings | — | ✓ |
| Resilience | Medium | High |
| Complexity | Low | Medium |
| Use Case | Normal ops | Edge cases |

---

## Part 3: Branch Structure & Roles

### Main Branch (Distribution)
**Purpose:** Public, application code + deployment artifacts

**Allowed Files:**
- Application source code (src/, backend/, plugins/)
- Configuration (tsconfig.json, package.json, etc.)
- Distribution orchestration docs (4 approved files)
- Tests, CI/CD workflows

**Blocked Files:**
- Internal hooks (.git/hooks/)
- Agent guidance (AGENTS.md, CRUSH.md, etc.)
- Internal debug/process files

**Deploy Command:**
```bash
git checkout main
git pull origin main
# Files auto-available for: CI/CD, users, distribution
```

---

### orchestration-tools Branch (Tool Infrastructure)
**Purpose:** Tool implementation, hooks, internal infrastructure

**Contains:**
- Post-commit/post-merge/post-push hooks (.git/hooks/)
- Strategy implementation (debounce logic)
- Validation scripts (context check)
- Internal setup/install scripts

**Does NOT Contain:**
- Application code (src/, backend/, plugins/ deleted)
- Distribution-only docs

**Deploy Command:**
```bash
git checkout orchestration-tools
git pull origin orchestration-tools
# Hooks auto-install via post-checkout
# Context validated (should pass)
```

---

### orchestration-tools-changes Branch (Working/Staging)
**Purpose:** Agent work area, testing, pull request staging

**Workflow:**
```bash
git checkout orchestration-tools-changes

# Make changes (multiple commits during session)
# ...changes...
git push origin orchestration-tools-changes

# Post-commit hook detects:
# - Branch = orchestration-tools-changes
# - Creates .orchestration-push-debounce file
# - Waits 5 seconds (aggregates future pushes)
# - Creates single PR → orchestration-tools

# After PR merges:
git fetch origin
git merge origin/orchestration-tools  # Sync latest
# Continue work or create new PR
```

---

## Part 4: Decision Tree - When to Switch Strategies

```
Detect Issue?
│
├─ Multiple PRs created for single session
│  └─ Check: Is debounce file created? (.orchestration-push-debounce)
│     ├─ NO → Strategy 5 not activating
│     │   └─ Check hook: cat .git/hooks/post-commit
│     │   └─ Verify branch: git rev-parse --abbrev-ref HEAD
│     │   └─ Fix: Reinstall hooks via scripts/install-hooks.sh
│     │
│     └─ YES → Debounce working, but PRs still duplicate
│        └─ Switch to Strategy 7 (see "Activation" above)

├─ Race condition detected (simultaneous pushes)
│  └─ Switch to Strategy 7 (git notes persistence)
│  └─ Increase debounce timeout: DEBOUNCE_TIMEOUT=10

├─ Merge conflicts on orchestration-tools-changes
│  └─ Verify: git diff orchestration-tools..orchestration-tools-changes
│  └─ If unresolvable: Reset & retry
│     git reset --hard orchestration-tools
│     git push origin orchestration-tools-changes --force-with-lease

├─ Context contamination appears
│  └─ Run: ./scripts/validate-orchestration-context.sh
│  └─ Identify commit: git log --oneline --all | grep -E "Merge|contamination"
│  └─ Revert: git revert <commit-sha>
│  └─ Push: git push origin orchestration-tools

└─ Complete failure / need to restart
   └─ See: PHASE3_ROLLBACK_OPTIONS.md
   └─ Option 1: Discard Strategy 5 (2 min)
   └─ Option 3: Reset to clean state (2 min)
   └─ Option 5: Emergency reset to main (5 min)
```

---

## Part 5: Monitoring & Tuning

### Daily Checks

```bash
# 1. Verify strategy is active
git rev-parse --abbrev-ref HEAD  # Should show active branch
ls -la .orchestration-push-debounce 2>/dev/null || echo "No active debounce"

# 2. Validate context
./scripts/validate-orchestration-context.sh  # Exit 0 = clean

# 3. Check for orphaned state files
ls -la .orchestration-push-state 2>/dev/null || echo "No orphaned state"

# 4. Monitor PR creation
gh pr list --head orchestration-tools-changes | wc -l  # Should be 0 or 1
```

### Tuning Debounce Timeout

**If seeing duplicate PRs:**
```bash
# Increase debounce window (default 5s)
git checkout orchestration-tools
nano .git/hooks/post-commit
# Change: DEBOUNCE_TIMEOUT=5 → DEBOUNCE_TIMEOUT=10
git commit -am "config: increase debounce to 10s"
git push origin orchestration-tools
```

**If debounce too long (blocking work):**
```bash
# Decrease debounce window
# Change: DEBOUNCE_TIMEOUT=10 → DEBOUNCE_TIMEOUT=3
# (Minimum recommended: 2s)
```

---

## Part 6: Runbook - Common Scenarios

### Scenario A: Normal Session (Strategy 5)

```bash
# 1. Start session
git checkout orchestration-tools-changes
git pull origin orchestration-tools-changes

# 2. Make multiple changes
for change in {1..5}; do
  echo "change $change" >> file.txt
  git add file.txt
  git commit -m "feat: change $change"
  git push origin orchestration-tools-changes
done
# Debounce auto-activates: changes aggregate into one PR

# 3. After PR merges to orchestration-tools
git fetch origin
git merge origin/orchestration-tools
echo "✓ Continue development or create new PR"
```

### Scenario B: Race Condition Detected (Escalate to Strategy 7)

```bash
# 1. Detect: Duplicate PRs despite debounce
gh pr list --head orchestration-tools-changes
# Output: 2+ open PRs → Problem

# 2. Switch to Strategy 7
git checkout orchestration-tools
git pull origin orchestration-tools

# 3. Enable git notes
git notes add -m "Escalated to Strategy 7 at $(date)"

# 4. Update hook (see Strategy 7 section)
# ... (insert hook updates)

# 5. Commit & push
git push origin orchestration-tools

# 6. Resume work on orchestration-tools-changes
git checkout orchestration-tools-changes
git merge origin/orchestration-tools
echo "✓ Strategy 7 now active"
```

### Scenario C: Context Contamination Detected

```bash
# 1. Identify contamination
./scripts/validate-orchestration-context.sh
# Output: ✗ CRITICAL: Found 'plugins/' ...

# 2. Find problematic commit
git log --oneline --all | grep -E "Merge|plugins" | head -5

# 3. Revert
git checkout orchestration-tools
git revert <commit-sha>  # Or reset --hard to before commit
git push origin orchestration-tools

# 4. Verify clean
./scripts/validate-orchestration-context.sh
# Output: ✓ Context validation PASSED (0 issues)

# 5. Notify team
echo "Contamination cleaned. Branch safe for merging to main."
```

### Scenario D: Emergency Rollback (All Strategies Failing)

```bash
# 1. Check rollback options
cat PHASE3_ROLLBACK_OPTIONS.md

# 2. Quick rollback (Option 1: Discard Strategy 5)
git branch -D orchestration-tools-changes
git push origin --delete orchestration-tools-changes
echo "✓ Strategy 5 discarded, branch deleted"

# 3. Verify main is unaffected
git checkout main
git log --oneline -1
# Should show: 1b1d3a4 feat(main): integrate Strategy 5...
echo "✓ Main branch intact"

# 4. Plan recovery
echo "Next: Choose Strategy 7 or restart with fresh orchestration-tools-changes"
```

---

## Part 7: Tool Commands Reference

### Essential Commands

```bash
# Check current strategy status
git branch -v
git rev-parse --abbrev-ref HEAD

# Validate context (run frequently)
./scripts/validate-orchestration-context.sh

# Check debounce state
ls -la .orchestration-push-debounce .orchestration-push-state 2>/dev/null || echo "No debounce"

# View hook implementation
cat .git/hooks/post-commit | head -30

# List git notes (Strategy 7)
git notes list
git notes show <commit-hash>

# Monitor PR creation
gh pr list --head orchestration-tools-changes

# Check branch difference
git diff orchestration-tools..orchestration-tools-changes --stat

# Safe reset to remote state
git reset --hard origin/orchestration-tools-changes
git reset --hard origin/orchestration-tools

# Force-safe push after reset
git push origin orchestration-tools-changes --force-with-lease
git push origin orchestration-tools --force-with-lease
```

---

## Summary: Process Flow

```
Session Start
    ↓
Checkout orchestration-tools-changes
    ↓
Make changes (multiple commits)
    ↓
Push to orchestration-tools-changes
    ↓
Post-commit hook:
  ├─ Detects branch
  ├─ Creates/checks .orchestration-push-debounce
  ├─ If debounce active: Aggregate (no PR)
  └─ If new: Start debounce, wait 5s
    ↓
After debounce clears:
  ├─ Single PR created (all commits aggregated)
  └─ No duplicate PRs
    ↓
Developer reviews/merges PR
    ↓
Merge: orchestration-tools-changes → orchestration-tools
    ↓
Context validated (should pass)
    ↓
Distribution: main already has docs/scripts
    ↓
Session ends / Continue development
```

---

## Key Files

- `.git/hooks/post-commit` - Strategy 5/7 implementation
- `scripts/validate-orchestration-context.sh` - Context validator
- `PHASE3_ROLLBACK_OPTIONS.md` - Emergency escape routes
- `ORCHESTRATION_PUSH_STRATEGIES.md` - Strategy details
- `.orchestration-push-debounce` - Debounce state (temporary)
- `.orchestration-push-state` - Push metadata (temporary)

---

## Status

✓ Strategy 5: Implemented & Tested
✓ Strategy 7: Documented (fallback)
✓ Context Separation: Verified
✓ Rollback Options: Identified
✓ Ready for: Production deployment

**Last Updated:** 2025-11-10
**Version:** 1.0
