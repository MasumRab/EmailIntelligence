# Orchestration System - LLM Single-Shot Test Suite

**Purpose:** Validate that LLM can correctly answer orchestration questions with only this document as context (no prior thread history).

**Instructions:** 
1. Create a new Amp thread
2. Share the following documents as context:
   - ORCHESTRATION_PROCESS_GUIDE.md
   - ORCHESTRATION_PUSH_STRATEGIES.md
   - PHASE3_ROLLBACK_OPTIONS.md
3. Send each prompt below as a separate message
4. Evaluate answers against expected key points

---

## Test 1: Basic Strategy Understanding

**Prompt:**
```
What is Strategy 5 and when should we use it?
```

**Expected Key Points:**
- Branch aggregation pattern using orchestration-tools-changes
- Default strategy for normal operations
- Prevents duplicate PRs through debounce mechanism (5-second wait)
- Single PR created per session (all commits aggregated)
- Lower complexity than Strategy 7

**Scoring:** Full if all 5 points covered; 80% if 4; etc.

---

## Test 2: Emergency Detection

**Prompt:**
```
Our team just noticed we're getting 2-3 duplicate PRs even though the debounce file exists. 
What should we do?
```

**Expected Key Points:**
- Recognize as Strategy 5 failure scenario (debounce not preventing duplicates)
- Suggest: Check if hook is actually being triggered
- Verify: git rev-parse --abbrev-ref HEAD = orchestration-tools-changes
- Check: cat .git/hooks/post-commit to verify implementation
- Option: If unresolvable, escalate to Strategy 7 (git notes + warnings)
- Reference: Decision tree in guide
- Should NOT suggest full rollback yet (that's last resort)

**Scoring:** Full if escalation path clear; 80% if hook checking included but missing Strategy 7 option

---

## Test 3: Context Contamination Response

**Prompt:**
```
After running the validation script on orchestration-tools branch, we got:
✗ CRITICAL: Found 'plugins/' (should not exist on orchestration-tools)
✗ CRITICAL: Found 'AGENTS.md' (should be on main, not orchestration-tools)

What happened and how do we fix it?
```

**Expected Key Points:**
- Identify: Context contamination (application code leaked onto orchestration-tools)
- Root cause: Likely from merge with main or agent push
- Find problematic commit: git log --oneline | grep -E "Merge|contamination"
- Fix: git revert <commit-sha> OR git reset --hard to before contamination
- Verify: Re-run ./scripts/validate-orchestration-context.sh (should exit 0)
- Push: git push origin orchestration-tools
- Should NOT suggest deleting branch (that's nuclear option)

**Scoring:** Full if includes identify, fix, verify steps

---

## Test 4: Branch Role Understanding

**Prompt:**
```
I need to understand the three orchestration branches. What goes on each one and why are they separate?
```

**Expected Key Points:**

**main:**
- Distribution-ready (public)
- Full application code + 4 distribution docs
- No internal hooks or agent guidance files
- Role: What users get

**orchestration-tools:**
- Tool implementation (internal)
- Has hooks (.git/hooks/), validation scripts, setup logic
- NO application code (intentionally deleted)
- Role: Tool infrastructure

**orchestration-tools-changes:**
- Agent work area / staging
- Strategy 5 branch aggregation pattern
- Temporary testing artifacts
- Role: Working/testing before merge to orchestration-tools

**Scoring:** Full if all 3 branches clearly distinguished; 80% if roles clear but separation rationale missing

---

## Test 5: Strategy 7 Activation

**Prompt:**
```
We want to enable Strategy 7 (hybrid) as a backup. Walk me through the steps to activate it 
on the orchestration-tools branch.
```

**Expected Key Points (in order):**
1. git checkout orchestration-tools
2. git pull origin orchestration-tools
3. Add git notes: git notes add -m "message"
4. Update .git/hooks/post-commit to write git notes after debounce
5. Create .git/hooks/pre-push with warning message
6. git add, commit ("enable Strategy 7 hybrid...")
7. git push origin orchestration-tools
8. Verify: git notes list

**Scoring:** Full if 6+ steps in reasonable order; 80% if sequence slightly off but core logic correct

---

## Test 6: Debounce Configuration

**Prompt:**
```
Our debounce timeout is set to 5 seconds, but we're seeing duplicate PRs created 
because pushes come in waves faster than 5 seconds. How do we fix this?
```

**Expected Key Points:**
- Increase DEBOUNCE_TIMEOUT value in .git/hooks/post-commit
- Location: git checkout orchestration-tools → nano .git/hooks/post-commit
- Example: Change from 5 to 10 (or 15)
- Minimum recommended: 2 seconds
- Commit and push to orchestration-tools
- Propagate change on next post-checkout
- Should NOT suggest deleting debounce (that disables feature)

**Scoring:** Full if includes timeout value, location, and propagation

---

## Test 7: Quick Reference - Command Needed

**Prompt:**
```
I need to check if debounce is currently active right now. What command do I run?
```

**Expected Key Points:**
- ls -la .orchestration-push-debounce (or ls .orchestration-push-debounce)
- If file exists: Debounce is active
- If file doesn't exist: No active debounce
- Alternative: cat .orchestration-push-state (shows metadata)
- Context validation: ./scripts/validate-orchestration-context.sh

**Scoring:** Full if primary command correct; 80% if slightly different syntax but logic right

---

## Test 8: Rollback Decision

**Prompt:**
```
Everything is failing. We need to undo Strategy 5 completely without losing work on main. 
What's the fastest option?
```

**Expected Key Points:**
- Reference: PHASE3_ROLLBACK_OPTIONS.md has 5 identified options
- **Fastest (Option 1):** Delete orchestration-tools-changes branch + disable hook
  - git branch -D orchestration-tools-changes
  - git push origin --delete orchestration-tools-changes
  - rm .git/hooks/post-commit
- Time: ~2 minutes
- Main branch: Completely unaffected
- Effect: Strategy 5 disabled, but application code safe
- Should NOT suggest reset --hard to old commits (loses current work)

**Scoring:** Full if Option 1 identified and clear; 80% if references guide but misses time estimate

---

## Test 9: Monitoring Checklist

**Prompt:**
```
Create a daily monitoring checklist that a team should run to ensure Strategy 5 
is working correctly. What 4 commands should be in it?
```

**Expected Key Points (any 4 of these):**
1. git rev-parse --abbrev-ref HEAD (verify correct branch)
2. ls -la .orchestration-push-debounce (check debounce state)
3. ./scripts/validate-orchestration-context.sh (verify no contamination)
4. gh pr list --head orchestration-tools-changes (check PR creation count, should be 0-1)
5. git notes list (check metadata/history)
6. git diff orchestration-tools..orchestration-tools-changes --stat (verify changes)

**Scoring:** Full if 4 commands + purpose clear; 80% if commands listed but purposes missing

---

## Test 10: Scenario Walkthrough

**Prompt:**
```
Walk me through what happens step-by-step when a developer makes 5 commits and pushes them 
to orchestration-tools-changes in quick succession (all within 5 seconds).
```

**Expected Key Points (in order):**
1. Developer: git push orchestration-tools-changes (first push)
2. Post-commit hook: Detects branch == orchestration-tools-changes
3. Hook: Checks for .orchestration-push-debounce file (doesn't exist yet)
4. Hook: Creates .orchestration-push-debounce file
5. Hook: Starts 5-second timer
6. Developer: Makes commit #2, pushes
7. Post-commit hook: Detects debounce file EXISTS
8. Hook: Skips PR creation (changes aggregated)
9. Repeat for commits 3-5 (all aggregate)
10. After 5 seconds: Debounce file deleted
11. Single PR created (all 5 commits together)
12. Result: No duplicate PRs

**Scoring:** Full if timeline clear + aggregation concept evident; 80% if sequence slightly jumbled but logic right

---

## Test 11: Failure Mode - Advanced

**Prompt:**
```
We're experiencing a race condition where two pushes happen simultaneously (within <100ms).
Strategy 5 sometimes creates 2 PRs instead of 1. Which strategy should we switch to and why?
```

**Expected Key Points:**
- **Answer: Strategy 7 (hybrid)**
- Why: Git notes metadata survives force-push/simultaneous operations better
- Why: Pre-push warning gives human time to cancel if duplicate detected
- Why: Provides fallback tracking even if debounce fails
- Trade-off: More complex than Strategy 5 (acceptable for race condition)
- Process: Follow Strategy 7 activation steps in guide
- Should NOT suggest: Going back to original problem or creating new tool

**Scoring:** Full if Strategy 7 + reasons clear; 80% if correct strategy but incomplete rationale

---

## Test 12: Integration Question

**Prompt:**
```
If I merge orchestration-tools into main right now, what files would be lost from main? 
Should we ever do a full branch merge?
```

**Expected Key Points:**
- **Answer: NO, do not merge full branch**
- Why: orchestration-tools is tool-only (application code intentionally deleted)
- Result of merge: Would DELETE all application code from main
- Loss: src/, backend/, plugins/, tests/, etc.
- What to do instead: Copy only distribution artifacts (4 files: docs + validation script)
- Reference: This is why Phase 3 used selective copy, not full merge
- Branch separation: Intentional, maintain it

**Scoring:** Full if "NO" + reason clear; 80% if answer right but separation rationale fuzzy

---

## Grading Scale

**90-100%:** LLM ready for production (can answer independently)
**80-89%:** LLM mostly ready (minor gaps, can consult guide)
**70-79%:** LLM needs more context (needs to re-read guide)
**Below 70%:** Documentation unclear or LLM didn't absorb context

---

## Test Administration

### For Each Test:
1. Send prompt
2. Let LLM respond fully
3. Compare against expected points
4. Note any missing or incorrect information
5. Ask follow-up if needed: "Can you explain the debounce mechanism?" if step is vague

### Final Assessment:
- Count questions scoring 90%+
- If 10/12 or higher: **PASS** - LLM can operate independently
- If 8-9/12: **CONDITIONAL PASS** - LLM can operate with team review
- If below 8/12: **FAIL** - Documentation needs revision or LLM needs training

---

## Alternative Single-Prompt Version

If you want to test in one message instead of 12, use:

**Comprehensive Single Prompt:**
```
You are an operations engineer responsible for the EmailIntelligence orchestration system. 
Here's a week's worth of issues you need to solve:

1. Strategy 5 is creating 2 duplicate PRs even though debounce is active. Diagnose and fix.
2. Context validation failed: Found 'plugins/' and 'AGENTS.md' on orchestration-tools. Fix.
3. We need to enable Strategy 7 as backup. Walk through activation steps.
4. Debounce is too slow (5s window). How do we adjust?
5. Everything failed. Quick rollback without losing main branch work?
6. Create a daily monitoring checklist (4 commands).
7. Explain what happens when 5 commits are pushed in <5 seconds to orchestration-tools-changes.
8. Should we ever merge orchestration-tools into main? Why or why not?

For each, provide specific commands and explain reasoning.
```

**Scoring:** Count how many of 8 sub-questions answered correctly

---

## Files to Provide as Context

Before sending prompts, share these with LLM:

```
Please review these documents for context:
1. ORCHESTRATION_PROCESS_GUIDE.md (primary reference)
2. ORCHESTRATION_PUSH_STRATEGIES.md (strategy details)
3. PHASE3_ROLLBACK_OPTIONS.md (emergency procedures)

These are the authoritative guides. Answer the following questions 
based only on what's in these documents.
```

---

## Expected Results

**Good Documentation Indicators:**
- LLM scores 85%+ on tests 1-4 (basics)
- LLM scores 80%+ on tests 5-8 (procedures)
- LLM scores 75%+ on tests 9-12 (advanced)

**If Scores Are Low:**
- Document may need clearer structure
- Test questions may need revision
- LLM may not have fully ingested context (ask it to quote specific sections)

---

## Next Steps After Testing

1. **If PASS (10+/12):** Documentation is ready for team deployment
2. **If CONDITIONAL (8-9/12):** Add a FAQ section, revise unclear sections
3. **If FAIL (<8/12):** Schedule documentation review + revision
4. **Always:** Include this test suite in onboarding (new team members)

