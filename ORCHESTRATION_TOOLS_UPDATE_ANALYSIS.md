# orchestration-tools Update Analysis

**Date:** 2026-02-20  
**Issue:** Branch structure incompatibility between main and orchestration-tools

---

## Critical Finding: Structurally Different Branches

### Branch Comparison

| Aspect | orchestration-tools | main | Compatible? |
|--------|---------------------|------|-------------|
| **emailintelligence_cli.py** | ✅ 1,754 lines (taskmaster version) | ✅ Different version | ❌ Different |
| **src/ structure** | taskmaster-style (context_control, cli/commands) | Different (backend/data, node_engine) | ❌ **INCOMPATIBLE** |
| **AI agent configs** | .agents/, .claude/, .cline/, .codex/, .roo/ | Minimal (.cursor/, .continue/) | ❌ Different |
| **Documentation** | Extensive (.RULES_*, .cli_framework/) | Standard (README, CONTRIBUTING) | ❌ Different |
| **Purpose** | Orchestration tools, git hooks | Main application | ❌ Different scope |

---

## Why Full Merge Would Pollute orchestration-tools

### Files That Should NOT Go to orchestration-tools

```
# main-specific files (DO NOT MERGE):
src/backend/data/              # Email data files
src/backend/node_engine/       # Node engine (different from orchestration-tools)
src/backend/extensions/        # Plugin system
BRANCH_ANALYSIS_REPORT.md      # Analysis docs
CLEANUP_SUMMARY.md             # Cleanup docs
CODEREVIEW_REPORT.md           # Review docs
SCIENTIFIC_BRANCH_ALIGNMENT_PLAN.md  # Scientific-specific
SCIENTIFIC_SUBTREE_GUIDE.md    # Scientific-specific
Dockerfile.prod                # Deployment
NVIDIA_DEPENDENCIES_*.md       # GPU-specific (orchestration-tools is CPU-only)
```

### Files That SHOULD Go to orchestration-tools

```
# Security enhancements only:
emailintelligence_cli.py (security features only)
src/core/security.py (if compatible)
src/core/config.py (if compatible)
```

---

## Why orchestration-tools Wasn't Updated First

### Normal Branch Alignment Order

```
Standard Flow:
1. orchestration-tools (source of truth for orchestration)
2. main (merge FROM orchestration-tools)
3. scientific (merge FROM main)
```

### What Happened Instead

```
Actual Flow:
1. taskmaster (development branch) ← emailintelligence_cli.py security features developed here
2. consolidate/cli-unification (consolidation branch) ← security features merged here
3. main (target for consolidation) ← PR to be created
4. orchestration-tools (should receive security features) ← NEEDS SELECTIVE UPDATE
5. scientific (separate structure) ← NEEDS SEPARATE PLAN
```

### Root Cause

**The consolidation was done from taskmaster → main, bypassing orchestration-tools because:**

1. **taskmaster had the security features** (developed independently)
2. **orchestration-tools already had similar code** but wasn't the source
3. **Urgency to fix security vulnerabilities** took priority over proper branch order
4. **Branch structure divergence** wasn't fully appreciated until now

---

## Recommended Approach: Cherry-Pick / Selective Update

### Option 1: Cherry-Pick Specific Commits (RECOMMENDED)

```bash
# After consolidate/cli-unification is merged to main:

# Create worktree for orchestration-tools update
cd /home/masum/github/PR/.taskmaster
git worktree add -b update-orchestration-security /home/masum/github/PR/orchestration-security-update orchestration-tools

cd /home/masum/github/PR/orchestration-security-update

# Cherry-pick ONLY the security commit from consolidation
git cherry-pick <commit-hash-from-consolidate/cli-unification> --no-commit

# Review what would be changed
git diff --cached --name-only

# Unstage files that shouldn't go to orchestration-tools
git reset HEAD src/backend/data/
git reset HEAD src/backend/node_engine/
git reset HEAD Dockerfile.prod
# ... etc

# Only keep emailintelligence_cli.py and compatible src/ files
git add emailintelligence_cli.py
git add src/core/security.py  # If compatible
git add src/core/config.py  # If compatible

# Commit
git commit -m "security: Add SecurityValidator to emailintelligence_cli

Cherry-picked security features from consolidate/cli-unification:
- SecurityValidator integration
- PR number validation
- Git reference validation

Excluded: main-specific files (backend/data, node_engine, etc.)"

# Test
python emailintelligence_cli.py --help

# Push and create PR
git push origin update-orchestration-security
```

---

### Option 2: Manual File Copy (More Control)

```bash
# Create worktree
git worktree add -b update-orchestration-security /home/masum/github/PR/orchestration-security-update orchestration-tools

cd /home/masum/github/PR/orchestration-security-update

# Get the security-enhanced CLI from consolidation branch
git show consolidate/cli-unification:emailintelligence_cli.py > emailintelligence_cli.py

# Review changes
git diff emailintelligence_cli.py

# If compatible src/ files exist, copy selectively
git show consolidate/cli-unification:src/core/security.py > src/core/security.py

# Commit only what's needed
git add emailintelligence_cli.py src/core/security.py
git commit -m "security: Add SecurityValidator integration"

# Test and push
python emailintelligence_cli.py --help
git push origin update-orchestration-security
```

---

### Option 3: Three-Way Merge with Sparse-Checkout (Advanced)

```bash
# Create worktree
git worktree add -b update-orchestration-security /home/masum/github/PR/orchestration-security-update orchestration-tools

cd /home/masum/github/PR/orchestration-security-update

# Enable sparse checkout
git sparse-checkout init --cone
git sparse-checkout set emailintelligence_cli.py src/core/

# Merge only specific paths from main (after consolidation)
git merge --no-commit --no-ff main

# Unstage everything not needed
git reset HEAD .
git sparse-checkout disable

# Add only what we want
git add emailintelligence_cli.py

# Commit
git commit -m "security: Selective merge of emailintelligence_cli.py security features"
```

---

## Updated bd Issues for orchestration-tools

```bash
# Create new bd epic for orchestration-tools update
bd create --type epic "orchestration-tools Security Update (Selective)"

# Create phases
bd create --type task --parent <epic-id> "Phase 1: Create orchestration-tools worktree"
bd create --type task --parent <epic-id> "Phase 2: Cherry-pick security commit"
bd create --type task --parent <epic-id> "Phase 3: Review and exclude incompatible files"
bd create --type task --parent <epic-id> "Phase 4: Test CLI functionality"
bd create --type task --parent <epic-id> "Phase 5: Merge to orchestration-tools"

# Link to main epic if needed
bd dep add <orchestration-epic> --related-to PR-f10
```

---

## Documentation Updates Required

### orchestration-tools Documentation to Update

After security update, update these files in orchestration-tools:

1. **README.md** - Add security features section
2. **.emailintelligence/config.yaml** - Update if config structure changed
3. **docs/SECURITY.md** - Document new validation features
4. **CHANGELOG.md** - Add security enhancement entry

### Example CHANGELOG Entry

```markdown
## [Unreleased] - Security Enhancement

### Added
- SecurityValidator integration for path validation
- PR number validation to prevent invalid inputs
- Git reference validation (command injection prevention)
- ConfigurationManager for centralized config
- GitOperations for modular git operations

### Security
- Prevents directory traversal attacks
- Prevents command injection via git references
- Validates all user inputs before use

### Source
- Cherry-picked from consolidate/cli-unification branch
- Original source: taskmaster branch security enhancements
```

---

## Prevention: Avoiding Main ↔ scientific ↔ orchestration-tools Merges

### Branch Isolation Rules

```bash
# Add to .git/config or global git config:

# Prevent accidental merges between structurally different branches
git config --local merge.orchestration-tools-driver.name "orchestration-tools isolation"
git config --local merge.orchestration-tools-driver.driver "echo '⚠️  WARNING: Merging orchestration-tools requires selective cherry-pick, not full merge' && false"

# Or use git hooks (.git/hooks/pre-merge-commit)
cat > .git/hooks/pre-merge-commit << 'EOF'
#!/bin/bash
# Prevent merges between structurally different branches

CURRENT_BRANCH=$(git branch --show-current)
MERGING_BRANCH=$MERGE_HEAD

# List of branches that should not be directly merged
INCOMPATIBLE_BRANCHES="main scientific orchestration-tools"

if echo "$INCOMPATIBLE_BRANCHES" | grep -qw "$CURRENT_BRANCH"; then
    if echo "$INCOMPATIBLE_BRANCHES" | grep -qw "$MERGING_BRANCH"; then
        if [ "$CURRENT_BRANCH" != "$MERGING_BRANCH" ]; then
            echo "⚠️  ERROR: Direct merge between $CURRENT_BRANCH and $MERGING_BRANCH is not allowed!"
            echo ""
            echo "These branches have incompatible structures."
            echo "Use cherry-pick or selective file update instead:"
            echo ""
            echo "  git cherry-pick <commit-hash> --no-commit"
            echo "  # Review changes"
            echo "  git reset HEAD <files-to-exclude>"
            echo "  git commit -m 'message'"
            echo ""
            exit 1
        fi
    fi
fi
exit 0
EOF
chmod +x .git/hooks/pre-merge-commit
```

---

## Updated Consolidation Plan

### Phase 5 Revised: Selective Updates

```bash
# After main merge is complete:

# 5a. orchestration-tools (cherry-pick approach)
git worktree add -b update-orchestration-security /home/masum/github/PR/orchestration-security-update orchestration-tools
cd /home/masum/github/PR/orchestration-security-update
git cherry-pick <consolidation-commit> --no-commit
git reset HEAD src/backend/data/ src/backend/node_engine/ Dockerfile.prod
git add emailintelligence_cli.py
git commit -m "security: Selective update of emailintelligence_cli.py"
git push origin update-orchestration-security
# Create PR: update-orchestration-security → orchestration-tools

# 5b. scientific (separate plan needed - different structure)
# See: SCIENTIFIC_BRANCH_ALIGNMENT_PLAN.md

# 5c. taskmaster (already has the features - just sync)
git checkout taskmaster
git merge main -m "Sync with main after consolidation"
git push origin taskmaster
```

---

## Summary

| Question | Answer |
|----------|--------|
| **Can worktree + bd workflow update orchestration-tools?** | ✅ Yes, but with cherry-pick, NOT full merge |
| **Will full merge pollute orchestration-tools?** | ❌ YES - main has incompatible src/ structure |
| **Why wasn't orchestration-tools updated first?** | taskmaster developed features independently, urgency overrode proper order |
| **Recommended approach?** | Cherry-pick specific commits, exclude incompatible files |
| **How to prevent future issues?** | Git hooks to block incompatible merges, use cherry-pick workflow |

---

**Next Action:** Create bd issues for selective orchestration-tools update using cherry-pick approach.
