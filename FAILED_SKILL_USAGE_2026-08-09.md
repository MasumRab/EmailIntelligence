# Failed Skill Usage Log

**Date:** 2026-08-09  
**Session:** PR Integration Merge (orchestration-tools → main)  
**Severity:** CRITICAL — 5 features dropped, 2 security regressions introduced

---

## Incident Summary

During merge of 8 PRs to main, conflict resolution used `git checkout --theirs` (brute-force take incoming) instead of surgical hunk-level resolution. This dropped critical security fixes and features from main that had landed after the PR branches were created.

**Dropped features:**
1. `shell=False` → `shell=True` in `scripts/branch_rename_migration.py` (command injection)
2. `verify_model_safety()` removed from `src/core/security.py` (insecure deserialization)
3. `client/src/pages/dashboard.tsx` completely emptied (0 bytes)
4. `src/core/performance_monitor.py` lost 19 lines (OptimizedPerformanceMonitor)
5. `src/core/rate_limiter.py` lost 4 lines

**Remediation:** All features restored from main after detection.

---

## Root Cause Analysis

### What skills were loaded
| Skill | Loaded? | Applied Correctly? |
|-------|---------|-------------------|
| git-surgeon | ✅ Yes | ❌ No — used `git checkout --theirs` instead of `git-surgeon hunks` |
| conflict-toolkit | ✅ Yes | ❌ No — skipped validation, skip keep-both-sides, skip shadow-scanner |

### Failure pattern
```
Trigger: Multiple merge conflicts detected
Expected: git-surgeon hunks → inspect → stage/discard surgically → validate
Actual:   git checkout --theirs → accept all incoming → merge → validate later
```

### Why it happened
1. **Volume bias:** 10+ conflicted files triggered "take all incoming" shortcut
2. **Assumption error:** Assumed PR branches were always ahead of main (not true — main had 1,489 commits ahead)
3. **Missing guardrail:** No pre-merge diff check against main
4. **Skill knowledge gap:** Loaded skills but didn't follow their prescribed workflows

### Conflict-toolkit violations
The conflict-toolkit skill explicitly prescribes:
- ✅ `git config rerere.enabled true` — DONE
- ❌ `git-surgeon hunks` for surgical resolution — SKIPPED
- ❌ `python -m py_compile` validation — SKIPPED
- ❌ Line count / function signature audit — SKIPPED
- ❌ Shadow-scanner for duplicate definitions — SKIPPED
- ❌ Keep-both-sides methodology — SKIPPED

---

## Correct Workflow (What Should Have Happened)

### Phase 1: Pre-Conflict Assessment
```bash
# Before resolving ANY conflicts:
1. git diff --stat origin/main..HEAD  # What's different?
2. git diff --stat origin/main -- <conflicted-files>  # What's being dropped?
3. Identify files where main has NEWER content than PR
```

### Phase 2: Surgical Resolution
```bash
# For EACH conflicted file:
1. git-surgeon hunks --file=<path>  # List all hunks
2. git-surgeon show <hunk-id>  # Inspect each hunk
3. Classify:
   - PR-only changes → stage
   - Main-only changes → discard PR's version
   - Both changed → keep-both-sides or take newer
4. git-surgeon stage <ids> / git-surgeon discard <ids>
```

### Phase 3: Validation Gate (MANDATORY)
```bash
# After resolving ALL conflicts, before commit:
1. python -m py_compile <all-python-files>
2. wc -l <key-files>  # Compare line counts with main
3. grep -c "def <function>" <files>  # Verify critical functions exist
4. git diff origin/main --stat  # Overall diff check
5. Check for: empty files, missing functions, security patterns
```

### Phase 4: Regression Check
```bash
# Before pushing/merging:
1. git show origin/main:<file> | wc -l  # Main's version
2. wc -l <file>  # Our version
3. If ours < main's by >10%: INVESTIGATE
4. grep -l "security\|sanitize\|validate\|verify" <files>  # Security patterns
5. Verify: shell=False, path validation, auth checks, type hints
```

---

## Pattern Matching for Automated Skill Loading

### Trigger patterns that should activate full conflict resolution
| Pattern | Action |
|---------|--------|
| `git rebase` produces conflicts | Load conflict-toolkit + git-surgeon |
| >5 conflicted files | Enforce validation gate |
| PR branch has <100 commits vs main's 1000+ | Flag divergence risk |
| Conflicts in security-critical files (auth.py, security.py, *.py with subprocess) | Enforce keep-both-sides |
| `--theirs` or `--ours` would be used | BLOCK — require git-surgeon inspection |
| Line count drop >10% in any file | BLOCK — require investigation |
| Empty file (0 bytes) after merge | BLOCK — require restoration |

### Skill loading rules
```
IF conflicts detected THEN
  LOAD conflict-toolkit
  LOAD git-surgeon
  LOAD pr-pipeline (for validation)
  
  FOR EACH conflicted file DO
    IF file contains security patterns THEN
      ENFORCE keep-both-sides methodology
    ENDIF
    IF file is >500 lines THEN
      REQUIRE git-surgeon hunk-level review
    ENDIF
  ENDFOR
  
  RUN validation gate BEFORE commit
  RUN regression check BEFORE push
ENDIF
```

### Red flags that should halt merges
1. Any file becomes 0 bytes
2. Any function that exists on main disappears
3. `shell=True` appears (should be `shell=False`)
4. `import subprocess` without `shell=False` audit
5. Path validation code removed
6. Auth/security decorators removed
7. Type hints stripped
8. Test files deleted
9. Line count drops >20%
10. New files from PR replace old files from main

---

## Lessons Learned

1. **Skills loaded ≠ skills applied.** Loading is not execution.
2. **Volume ≠ priority.** More conflicts doesn't mean take the shortcut.
3. **Always diff against target.** Before resolving, compare what main has.
4. **Validation is mandatory, not optional.** No commit without py_compile + line audit.
5. **Security patterns need extra scrutiny.** Any file with subprocess, auth, paths, or validation gets keep-both-sides treatment.
6. **Divergence matters.** When main has 1000+ commits ahead of PR, main likely has newer fixes.

---

## Prevention Checklist (Future Use)

- [ ] Load conflict-toolkit + git-surgeon on any conflict
- [ ] Run `git-surgeon hunks` before `git checkout --theirs`
- [ ] Check `git diff --stat origin/main` for dropped content
- [ ] Audit line counts for all conflicted files
- [ ] Verify critical functions exist post-resolution
- [ ] Run `python -m py_compile` on all changed Python files
- [ ] Check for security patterns (shell=False, path validation, auth)
- [ ] Block merge if any file is 0 bytes
- [ ] Block merge if any function from main is missing
- [ ] Document any intentional deletions with rationale

---

*Logged: 2026-08-09*  
*Severity: CRITICAL*  
*Status: Remediated (all features restored)*
