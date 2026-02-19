# Branch Isolation Guidelines (No Hooks)

**Date:** 2026-02-20  
**Policy:** Manual process, no automated hooks

---

## Why No Git Hooks

Git hooks can cause problems:
- ❌ CI/CD pipeline failures
- ❌ Team workflow conflicts
- ❌ Hard to debug merge issues
- ❌ Not portable across clones
- ❌ Can block legitimate operations

**Better approach:** Documentation + manual process + code review

---

## Branch Structure Awareness

### Know Your Branches

| Branch | Purpose | Structure | Update Method |
|--------|---------|-----------|---------------|
| **main** | Core application | backend/data, node_engine | Direct commits, PRs |
| **scientific** | Data analysis, ML | backend/data, node_engine | Merge FROM main (selective) |
| **orchestration-tools** | Git orchestration, hooks | context_control, cli/commands | Cherry-pick only |
| **taskmaster** | Task management | .taskmaster structure | Independent |

### Golden Rules

1. **NEVER** merge main ↔ orchestration-tools directly
2. **NEVER** merge main ↔ scientific directly  
3. **ALWAYS** use cherry-pick for cross-branch updates
4. **ALWAYS** review files before committing

---

## Safe Update Workflow (Manual Process)

### For orchestration-tools Updates

```bash
# Step 1: Create worktree
cd /home/masum/github/PR/.taskmaster
git worktree add -b update-orchestration-security \
  /home/masum/github/PR/orchestration-security-update \
  orchestration-tools

# Step 2: Cherry-pick specific commit
cd /home/masum/github/PR/orchestration-security-update
git cherry-pick <commit-hash> --no-commit

# Step 3: CRITICAL - Review what would be changed
git diff --cached --name-only

# Step 4: Exclude incompatible files
# Reset everything first
git reset HEAD

# Add ONLY compatible files
git add emailintelligence_cli.py
# Add src/core/*.py ONLY if you've verified structure matches

# Step 5: Verify before committing
git status
git diff --cached

# Step 6: Test
python emailintelligence_cli.py --help

# Step 7: Commit with clear message
git commit -m "security: Update emailintelligence_cli.py

Cherry-picked from consolidate/cli-unification:
- SecurityValidator integration
- PR number validation
- Git reference validation

Verified: Only emailintelligence_cli.py updated
Excluded: src/backend/*, Dockerfile.*, NVIDIA_*.md"

# Step 8: Push and create PR
git push origin update-orchestration-security
```

---

## Files to ALWAYS Exclude from orchestration-tools

```bash
# Never add these to orchestration-tools:
src/backend/data/              # Email data files
src/backend/node_engine/       # Different structure
src/backend/extensions/        # Plugin system
Dockerfile.prod                # Deployment
NVIDIA_DEPENDENCY_*.md         # GPU-specific
BRANCH_ANALYSIS_REPORT.md      # Analysis docs
SCIENTIFIC_BRANCH_ALIGNMENT_PLAN.md  # Scientific-specific
CLEANUP_SUMMARY.md             # Cleanup docs
CODEREVIEW_REPORT.md           # Review docs
```

## Files SAFE to Add to orchestration-tools

```bash
# These are generally safe:
emailintelligence_cli.py       # Main CLI (verify compatibility)
src/core/security.py           # IF structure matches
src/core/config.py             # IF structure matches
```

---

## Verification Checklist

Before pushing to orchestration-tools:

- [ ] I have reviewed `git diff --cached --name-only`
- [ ] I have excluded all `src/backend/data/*` files
- [ ] I have excluded all `src/backend/node_engine/*` files
- [ ] I have excluded all `Dockerfile.*` files
- [ ] I have excluded all `NVIDIA_*.md` files
- [ ] I have tested `python emailintelligence_cli.py --help`
- [ ] My commit message explains what was cherry-picked
- [ ] My commit message lists what was excluded

---

## Code Review Requirements

All orchestration-tools PRs must include:

### PR Description Template

```markdown
## Security Update: emailintelligence_cli.py

### Source
- Cherry-picked from: consolidate/cli-unification
- Original commit: <commit-hash>

### Files Changed
- emailintelligence_cli.py (security features only)

### Files Excluded
- src/backend/data/* (incompatible structure)
- src/backend/node_engine/* (incompatible structure)
- Dockerfile.prod (deployment-specific)
- NVIDIA_DEPENDENCY_*.md (GPU-specific)

### Testing
- [ ] CLI help works: `python emailintelligence_cli.py --help`
- [ ] SecurityValidator present: `grep -c SecurityValidator emailintelligence_cli.py`
- [ ] No incompatible files: `git diff --cached --name-only`

### Verification
Reviewer should verify:
1. Only emailintelligence_cli.py is changed
2. No backend/data or node_engine files included
3. CLI functionality works
```

---

## Alternative: Documentation-Only Approach

Instead of hooks, use documentation:

### 1. Add to CONTRIBUTING.md

```markdown
## Branch Update Guidelines

### orchestration-tools Updates

**IMPORTANT:** orchestration-tools has a different structure than main.

**DO:**
- Cherry-pick specific commits
- Review files before committing
- Exclude incompatible files (backend/data, node_engine, etc.)

**DO NOT:**
- Merge main directly into orchestration-tools
- Merge orchestration-tools directly into main
- Copy entire src/ directories

See: ORCHESTRATION_TOOLS_UPDATE_ANALYSIS.md for detailed guidance
```

### 2. Add Branch Structure Diagram

```markdown
## Branch Structures

```
main                    orchestration-tools
├── emailintelligence_cli.py    ├── emailintelligence_cli.py
├── src/                        ├── src/
│   ├── backend/                │   ├── context_control/
│   │   ├── data/               │   ├── cli/commands/
│   │   └── node_engine/        │   └── core/ (partial)
│   └── core/                   └── ...
└── ...
```

**Note:** src/ structures are incompatible - use cherry-pick, not merge.
```

---

## Team Communication

### When Creating PR

Tag reviewers with context:

```
@team-lead @security-lead 

This PR updates orchestration-tools with security features from main.

**Method:** Cherry-pick (not merge) to avoid structure pollution
**Files changed:** 1 (emailintelligence_cli.py only)
**Files excluded:** backend/data/*, node_engine/*, Dockerfile.*, etc.

Please verify no incompatible files are included.
```

### When Reviewing PR

Reviewer checklist:
- [ ] Only compatible files changed
- [ ] No backend/data/* included
- [ ] No node_engine/* included
- [ ] CLI functionality verified
- [ ] Commit message explains cherry-pick source

---

## Summary

| Approach | Hooks | Documentation | Manual Process |
|----------|-------|---------------|----------------|
| **Pros** | Automated blocking | Clear guidance | Flexible |
| **Cons** | CI/CD issues, team friction | Relies on discipline | Human error possible |
| **Recommended** | ❌ No | ✅ Yes | ✅ Yes |

**Best Practice:** Documentation + code review + team awareness

---

**References:**
- `ORCHESTRATION_TOOLS_UPDATE_ANALYSIS.md` - Full branch analysis
- `UPDATED_CONSOLIDATION_PLAN.md` - Cherry-pick workflow
- `CONTRIBUTING.md` - Add branch guidelines here
