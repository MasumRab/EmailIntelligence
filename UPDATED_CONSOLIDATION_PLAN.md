# Updated Consolidation Plan - Branch Isolation Strategy

**Date:** 2026-02-20  
**Status:** ✅ Analysis Complete, 🟡 orchestration-tools Selective Update Planned

---

## Critical Finding: Branch Structure Incompatibility

### Branch Comparison

| Branch | src/ Structure | emailintelligence_cli.py | Compatible With |
|--------|---------------|-------------------------|-----------------|
| **main** | backend/data, node_engine | Different version | ❌ None |
| **scientific** | backend/data, node_engine | Different version | ❌ None |
| **orchestration-tools** | context_control, cli/commands | 1,754 lines (taskmaster-style) | ❌ None |
| **taskmaster** | context_control, cli/commands | 1,745 lines (security features) | ❌ None |

**Conclusion:** These branches are **structurally incompatible** - full merges will cause pollution and conflicts.

---

## Why orchestration-tools Wasn't Updated First

### Normal Order (Should Have Been)
```
1. orchestration-tools (source of truth for orchestration)
2. main (merge FROM orchestration-tools)
3. scientific (merge FROM main)
```

### What Actually Happened
```
1. taskmaster (independent development)
2. consolidate/cli-unification (consolidation branch)
3. main (PR pending)
4. orchestration-tools (needs selective update)
5. scientific (needs separate plan)
```

### Root Causes

1. **Independent Development:** Security features developed on taskmaster, not orchestration-tools
2. **Urgency:** Security vulnerabilities took priority over proper branch order
3. **Structure Divergence:** Branches diverged structurally, making merges incompatible
4. **Discovery:** Incompatibility only discovered during consolidation

---

## Updated Strategy: Selective Cherry-Pick

### For orchestration-tools (Phase 5 Revised)

```bash
# After consolidate/cli-unification → main merge:

# 1. Create worktree
cd /home/masum/github/PR/.taskmaster
git worktree add -b update-orchestration-security \
  /home/masum/github/PR/orchestration-security-update \
  orchestration-tools

# 2. Cherry-pick security commit
cd /home/masum/github/PR/orchestration-security-update
git cherry-pick <commit-hash-from-consolidation> --no-commit

# 3. Review changes
git diff --cached --name-only

# 4. Exclude incompatible files
git reset HEAD src/backend/data/
git reset HEAD src/backend/node_engine/
git reset HEAD Dockerfile.prod
git reset HEAD NVIDIA_DEPENDENCIES_*.md
git reset HEAD backend/email_cache.db

# 5. Keep only compatible files
git add emailintelligence_cli.py
# Add src/core/*.py ONLY if compatible structure

# 6. Test
python emailintelligence_cli.py --help

# 7. Commit and push
git commit -m "security: Selective update of emailintelligence_cli.py

Cherry-picked from consolidate/cli-unification:
- SecurityValidator integration
- PR number validation
- Git reference validation

Excluded: main-specific files (backend/data, node_engine, etc.)"
git push origin update-orchestration-security

# 8. Create PR: update-orchestration-security → orchestration-tools
```

---

## Prevention: Documentation + Manual Process

### Branch Isolation Guidelines

**Location:** `BRANCH_ISOLATION_GUIDELINES.md`

**Purpose:** Documents which branches are incompatible and proper cherry-pick workflow

**Approach:** Manual process with code review (no automated hooks)

**Why No Hooks:**
- Hooks can cause CI/CD failures
- Team workflow conflicts
- Hard to debug merge issues
- Not portable across clones

**Better Approach:**
- Clear documentation
- Code review checklist
- Team awareness

---

## bd Issues Updated

### Original Epic (CLI Consolidation)
- **PR-f10:** CLI Consolidation: Unify emailintelligence_cli.py
  - ~~PR-9ds~~ Phase 1: Create worktree ✅ Closed
  - ~~PR-x44~~ Phase 2: Merge taskmaster ✅ Closed
  - ~~PR-duq~~ Phase 3: Test ✅ Closed
  - ~~PR-exk~~ Phase 4: Merge to main ✅ Closed
  - PR-vqo Phase 5: Propagate to all 🟡 **REVISED** (see below)

### New Epic (orchestration-tools Selective Update)
- **PR-o02:** orchestration-tools Security Update (Selective Cherry-Pick)
  - PR-4wi Phase 1: Create worktree ⚪ Pending
  - PR-43u Phase 2: Cherry-pick security commit ⚪ Pending
  - PR-0n8 Phase 3: Exclude incompatible files ⚪ Pending
  - PR-57w Phase 4: Test CLI ⚪ Pending
  - PR-7ei Phase 5: Merge via PR ⚪ Pending

---

## Files That Should NOT Go to orchestration-tools

```
# main-specific (DO NOT MERGE):
src/backend/data/              # Email data files
src/backend/node_engine/       # Different node engine structure
src/backend/extensions/        # Plugin system
Dockerfile.prod                # Deployment config
NVIDIA_DEPENDENCY_*.md         # GPU-specific (orchestration-tools is CPU-only)
BRANCH_ANALYSIS_REPORT.md      # Analysis docs
SCIENTIFIC_BRANCH_ALIGNMENT_PLAN.md  # Scientific-specific
```

## Files That SHOULD Go to orchestration-tools

```
# Security features only:
emailintelligence_cli.py       # Main CLI with security features
src/core/security.py           # IF structure is compatible
src/core/config.py             # IF structure is compatible
```

---

## Documentation Updates Required

### After orchestration-tools Update

Update these files in orchestration-tools branch:

1. **README.md**
   - Add "Security Features" section
   - Document SecurityValidator integration

2. **CHANGELOG.md**
   ```markdown
   ## [Unreleased] - Security Enhancement
   
   ### Added
   - SecurityValidator integration
   - PR number validation
   - Git reference validation (command injection prevention)
   
   ### Security
   - Prevents directory traversal attacks
   - Prevents command injection via git references
   
   ### Source
   - Cherry-picked from consolidate/cli-unification
   ```

3. **.emailintelligence/config.yaml** (if config structure changed)

4. **docs/SECURITY.md** (create if doesn't exist)

---

## scientific Branch - Separate Plan Needed

**Note:** scientific branch also has incompatible structure and needs a separate selective update plan.

**Action:** Create separate bd epic for scientific branch update after orchestration-tools is complete.

---

## Next Steps

### Immediate (After main PR Merge)

1. **Execute orchestration-tools selective update** (PR-o02 epic)
   ```bash
   # Follow steps in "For orchestration-tools (Phase 5 Revised)" section above
   ```

2. **Close original consolidation epic**
   ```bash
   bd close PR-vqo
   bd close PR-f10
   ```

3. **Create scientific branch epic** (separate plan)

### Long-Term Prevention

1. **Follow BRANCH_ISOLATION_GUIDELINES.md** - Manual process with code review
2. **Use cherry-pick workflow** for cross-branch updates
3. **Document branch structures** to prevent future confusion
4. **Code review checklist** - Verify no incompatible files included

---

## Summary

| Question | Answer |
|----------|--------|
| **Can worktree + bd update orchestration-tools?** | ✅ Yes, with cherry-pick (NOT full merge) |
| **Will full merge pollute orchestration-tools?** | ❌ YES - incompatible src/ structures |
| **Why wasn't orchestration-tools first?** | Independent development on taskmaster, urgency overrode order |
| **Recommended approach?** | Cherry-pick specific commits, exclude incompatible files |
| **How to prevent future issues?** | ✅ Git hook installed, use cherry-pick workflow |

---

**Documentation:**
- Full analysis: `ORCHESTRATION_TOOLS_UPDATE_ANALYSIS.md`
- This plan: `UPDATED_CONSOLIDATION_PLAN.md`
- Git hook: `.git/hooks/pre-merge-commit`

**Next Action:** After main PR merge, execute orchestration-tools selective update (PR-o02 epic).
