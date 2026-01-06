# Task 7 Implementation Guide: Quick Start

**Status:** ✅ Ready for Implementation  
**Created:** January 4, 2025  
**Duration:** 1-1.5 weeks (36-54 hours)  

---

## What You Need to Know in 5 Minutes

**Task 7** is a framework-definition task that creates the strategy other branches will follow for alignment.

**You will produce:**
1. Target selection criteria (5+ factors, scoring formula)
2. Merge vs. rebase decision tree
3. Architecture alignment rules (10+ rules)
4. Conflict resolution procedures
5. Branch assessment checklist
6. Master framework guide (3-5 pages)
7. Real-world examples tested

**Timeline:** 1-1.5 weeks with 1-3 people  
**Parallelization:** Yes - subtasks 7.3, 7.4, 7.5 can run in parallel  

---

## Your 7 Subtasks

| # | Task | Hours | After | Notes |
|----|------|-------|-------|-------|
| 7.1 | Analyze branch state | 4-6 | — | Inventory all branches |
| 7.2 | Define target criteria | 6-8 | 7.1 | Create scoring formula |
| 7.3 | Merge vs. rebase | 4-6 | 7.2 | Decision tree |
| 7.4 | Architecture rules | 6-8 | 7.2 | 10+ rules + validation |
| 7.5 | Conflict resolution | 4-6 | 7.2 | 6+ scenarios + escalation |
| 7.6 | Branch checklist | 6-8 | 7.1,7.2,7.4 | 15-20 items, real examples |
| 7.7 | Master guide | 6-8 | 7.2,7.3,7.4,7.5,7.6 | Final consolidation |

**Critical Path:** 7.1 → 7.2 → [7.3,7.4,7.5] → [7.6] → 7.7

---

## Critical Success Factors

✅ **DO:**
- Create explicit, measurable criteria (not vague guidelines)
- Document all procedures clearly (repeatable by anyone)
- Test on 5+ real branches (prove it works)
- Handle edge cases (orphaned, stale, large divergence)
- Keep it accessible (stakeholders should understand)

❌ **DON'T:**
- Write ambiguous guidance
- Skip examples
- Ignore edge cases
- Over-engineer the framework
- Leave gotchas undocumented

---

## Getting Started (Today)

### 1. Read Documentation (30 minutes)
```bash
# Read the enhanced framework definition
cat task_data/task-7.md | less

# Key sections to review:
#   - Quick Navigation
#   - Success Criteria
#   - Subtasks Overview
#   - Configuration Template
#   - Common Gotchas
```

### 2. Review Framework Structure (15 minutes)
```bash
# Check the YAML configuration template
cat branch_alignment_framework.yaml

# This is your parameter tuning guide
```

### 3. Understand the Framework Approach (15 minutes)

**Your framework will answer these questions:**
1. How do we decide which target branch each feature branch should go to?
2. When should we merge vs. rebase?
3. What architectural rules must be respected?
4. How do we handle merge conflicts?
5. How do we verify alignment is successful?

---

## Day-by-Day Implementation Schedule

### Days 1-2: Analysis & Criteria (7.1-7.2)

**Day 1 (4-6 hours): Subtask 7.1 - Analyze Current Branch State**
```bash
# List all active branches
git branch -a

# For each feature branch, assess:
# - How many commits behind main?
# - What files changed?
# - Who is the author?
# - How old is it? (last commit date)

# Categorize by complexity:
# - Simple: <20 commits, <50 files, <7 days old
# - Moderate: 20-100 commits, 50-200 files, 7-30 days old
# - Complex: >100 commits, >200 files, >30 days old
```

**Output:** 15-20 branches inventoried with metadata

**Day 2 (6-8 hours): Subtask 7.2 - Define Target Selection Criteria**
```bash
# Create scoring formula with these factors:
# - Codebase similarity (0.30)      : file overlap %
# - Git history depth (0.25)        : common commits
# - Architectural alignment (0.20)  : import compatibility
# - Team priority (0.15)            : project importance
# - Branch age (0.10)               : staleness

# Test on 3-5 branches from 7.1:
# For each branch, calculate score for (main, scientific, develop)
# Target = highest_score >= 0.65
```

**Output:** Scoring formula documented, tested on real branches

---

### Days 2-4: Framework Components (7.3-7.5 in parallel)

**Option A: Sequential (1 person)**
- Day 2-3: Subtask 7.3 (merge vs. rebase)
- Day 3-4: Subtask 7.4 (architecture rules)
- Day 3-4: Subtask 7.5 (conflict resolution)

**Option B: Parallel (3 people, RECOMMENDED)**
- Day 2-3: Person 1 does 7.3 (merge vs. rebase)
- Day 2-3: Person 2 does 7.4 (architecture rules)
- Day 3-4: Person 3 does 7.5 (conflict resolution)
- **Savings: 10-12 hours**

**Day 2-3: Subtask 7.3 - Merge vs. Rebase Strategy**
```
Create decision tree:
  
  Is linear history required?
  ├─ YES → Use REBASE
  │   └─ Exception: If shared history > 100 commits, use MERGE
  └─ NO → Use MERGE (default)
      └─ Exception: If experimental, consider REBASE
```

**Output:** Decision tree with clear conditions

**Day 2-4: Subtask 7.4 - Architecture Alignment Rules**
```
Document 10+ rules like:
1. No forbidden imports (backend → frontend)
2. All required directories present (src/, tests/, docs/)
3. Module boundaries respected
4. Critical files unmodified (setup.py, AGENTS.md, config/)
5. Test coverage ≥80%
... (5+ more)

For each rule:
- Measurement method (static analysis? manual review?)
- Validation tool (ruff? flake8? mypy?)
```

**Output:** 10+ rules documented with validation procedures

**Day 3-4: Subtask 7.5 - Conflict Resolution**
```
Document these scenarios:
1. Both modified same file
2. Conflicting requirements
3. Binary files conflicted
4. Module boundaries conflict
5. Test conflicts
6. Critical file conflicts

For each:
- Approach to resolve
- Priority rule (feature code vs. target code)
- When to escalate
```

**Output:** 6+ scenarios with resolution approaches

---

### Days 4-5: Validation & Guide (7.6-7.7)

**Day 4 (6-8 hours): Subtask 7.6 - Branch Assessment Checklist**
```bash
# Create 15-20 item checklist with sections:

PRE-ALIGNMENT CHECKS:
□ Branch exists and is accessible
□ Current changes committed
□ No uncommitted changes
□ CI passing on both branches
□ No pending reviews blocking

POST-ALIGNMENT CHECKS:
□ Merge/rebase completed without failures
□ All conflicts resolved
□ Tests pass on aligned branch
□ Architecture rules still respected
□ CI passes on aligned branch

# Fill in with 3-5 real branch examples
```

**Output:** Checklist with real examples filled in

**Day 5 (6-8 hours): Subtask 7.7 - Master Framework Guide**
```bash
# Consolidate all outputs into 3-5 page master guide:

1. Executive Summary (1 page)
   - What is this framework?
   - Why does it matter?
   - Who uses it?

2. Framework Components (1 page)
   - Target selection criteria
   - Merge vs. rebase decision
   - Architecture rules

3. How to Use (1.5 pages)
   - Step-by-step procedure
   - Examples walkthrough
   - Edge case handling

4. Reference (0.5 pages)
   - YAML configuration
   - Troubleshooting
```

**Output:** Final 3-5 page guide with flowcharts and examples

---

## Quality Gates (Daily)

**Each day, verify:**
- [ ] All sections have examples
- [ ] All criteria are measurable
- [ ] All procedures are repeatable
- [ ] No ambiguous guidance
- [ ] Tests/validation methods specified
- [ ] Edge cases addressed

---

## Validation Checklist (Before Sign-Off)

**Content Quality:**
- [ ] All 7 subtasks complete
- [ ] task-7.md has 2000+ lines
- [ ] 15+ navigation links working
- [ ] 6+ framework components documented
- [ ] 9 gotchas have solutions
- [ ] 5+ real branches tested
- [ ] YAML configuration valid

**Framework Quality:**
- [ ] Target scoring formula tested
- [ ] Merge/rebase rules clear
- [ ] Architecture rules specific (10+)
- [ ] Conflict procedures documented
- [ ] Checklist is repeatable
- [ ] Examples are realistic

**Integration Ready:**
- [ ] Output matches Task 77 requirements
- [ ] Output matches Task 79 requirements
- [ ] Output matches Task 81 requirements
- [ ] No ambiguity in handoff
- [ ] Clear escalation paths

---

## Key Resources

| Document | Purpose | Read Time |
|----------|---------|-----------|
| `task-7.md` | Full framework | 30 min |
| `branch_alignment_framework.yaml` | Configuration | 10 min |
| `TASK_7_QUICK_REFERENCE.md` | Quick lookup | 5 min |
| `TASK_7_ENHANCEMENT_STATUS.md` | Status report | 15 min |

---

## Success Definition

Task 7 is **DONE** when:

✅ All 7 subtasks (7.1-7.7) marked complete  
✅ Framework documentation complete (3-5 pages)  
✅ Framework tested on 5+ real branches  
✅ No gotchas remain undocumented  
✅ Tasks 77, 79, 81 can use outputs without asking questions  
✅ Ready for downstream implementation  

---

## Questions?

**"What if a branch doesn't fit any category?"**
→ That's a gotcha - document the edge case, create new rule

**"What if the scoring formula is subjective?"**
→ Make it objective - define how to measure each factor numerically

**"What if the team disagrees with a rule?"**
→ Document the rule AND the override process (who can override, why)

**"How often does the framework need updating?"**
→ Quarterly review minimum, or when repository practices change

---

**START DATE:** Ready immediately  
**DURATION:** 1-1.5 weeks  
**OWNER:** Architecture Team  
**BLOCKS:** Tasks 77, 79, 81  

Good luck! Ask questions if anything is unclear.
