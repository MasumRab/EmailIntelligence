# Task 7: Align and Architecturally Integrate Feature Branches with Justified Targets

## Overview

Define the strategic framework and decision criteria for aligning multiple feature branches with their optimal integration targets based on codebase similarity, Git history, architectural alignment, and project priorities. 

**This is a FRAMEWORK-DEFINITION task**, not a branch-alignment task. Task 7 produces strategic documentation, criteria, and procedures that other alignment tasks (77, 79, 81) will use for actual implementation.

**Total Effort:** 36-54 hours | **Timeline:** 1-1.5 weeks | **Parallelizable:** Yes (some subtasks)

---

## Quick Navigation

Navigate this document using these links:

- [Overview](#overview)
- [Developer Quick Reference](#developer-quick-reference)
- [Success Criteria](#success-criteria)
- [Performance Baselines](#performance-baselines)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration & Defaults](#configuration--defaults)
- [Framework Components](#framework-components)
- [Decision Criteria](#decision-criteria-for-target-selection)
- [Typical Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---

## Developer Quick Reference

### What to Build

A complete framework that defines HOW branches should be aligned, including:

1. **Target Selection Criteria** - Decision matrix for determining optimal target branches
2. **Merge vs. Rebase Strategy** - When and how to use each approach
3. **Architecture Alignment Rules** - Requirements for architectural consistency
4. **Conflict Resolution Framework** - Procedures for handling merge conflicts
5. **Verification Procedures** - Steps to validate alignment success
6. **Branch Assessment Checklist** - Template for evaluating branches
7. **Alignment Documentation** - Guidelines for documenting decisions

### Framework Outputs (Required Deliverables)

```json
{
  "framework": {
    "target_selection_criteria": {
      "similarity_weight": 0.30,
      "history_weight": 0.25,
      "architecture_weight": 0.20,
      "priority_weight": 0.15,
      "age_weight": 0.10
    },
    "merge_strategy_rules": {
      "linear_history_required": true,
      "max_divergence_commits": 500,
      "default_approach": "merge"
    },
    "architecture_rules": [
      "no forbidden imports",
      "module boundaries respected",
      "required directories present"
    ]
  }
}
```

---

## Success Criteria

Task 7 is complete when:

**Core Framework Deliverables:**
- [ ] **Target selection criteria** defined with 5+ factors and scoring weights (must sum to 1.0)
- [ ] **Merge vs. rebase decision tree** created with clear conditional rules
- [ ] **Architecture alignment rules** documented (minimum 10 rules with examples)
- [ ] **Conflict resolution procedures** specified with step-by-step process
- [ ] **Branch verification checklist** created (minimum 5-item checklist with examples)
- [ ] **Framework documentation** complete (3-5 page guide with real examples)

**Framework Quality:**
- [ ] All criteria have explicit scoring/evaluation method
- [ ] All procedures are repeatable and unambiguous
- [ ] All examples are realistic and tested
- [ ] Framework handles edge cases (orphaned branches, stale branches, large divergence)
- [ ] Framework is technology-agnostic (works with any git workflow)

**Integration Readiness:**
- [ ] Compatible with Task 77 (Feature/X branches)
- [ ] Compatible with Task 79 (Execution with validation)
- [ ] Compatible with Task 81 (Scientific branch alignment)
- [ ] Clear input/output specifications for downstream tasks
- [ ] Framework outputs match expected format for Tasks 77/79/81

**Validation:**
- [ ] All 7 subtasks complete
- [ ] Documentation complete and reviewed
- [ ] Examples tested against real branches
- [ ] Ready for hand-off to Tasks 77, 79, 81

---

## Performance Baselines

Framework completeness targets (documentation focus, not runtime):

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Framework documentation** | 3-5 pages | Comprehensive but accessible |
| **Decision criteria count** | 5+ factors | Covers all relevant aspects |
| **Architecture rules** | 10+ rules | Thorough coverage of patterns |
| **Example branches** | 5-8 real cases | Proves framework works in practice |
| **Conflict scenarios** | 6+ documented | Covers common conflicts |
| **Edge cases handled** | 8+ cases | Orphaned, stale, large drift, etc. |
| **Time to implement criteria** | <2 hours per branch | Framework should enable quick decisions |
| **Ambiguity level** | <5% uncovered cases | Framework should be comprehensive |
| **Stakeholder review rounds** | <2 rounds needed | Framework should be clear upfront |

---

## Subtasks Overview

### Dependency Flow Diagram

```
7.1 (4-6h) ──→ 7.2 (6-8h) ──→ 7.3 (4-6h)
[Analyze]      [Criteria]     [Strategy]
    │              │              │
    └──────────────┴──────────────┼──→ 7.4 (6-8h) ──→ 7.7 (6-8h)
                                  │    [Rules]         [Guide]
                              7.5 (4-6h)
                              [Resolve]
                                  │
                                  └──→ 7.6 (6-8h)
                                      [Checklist]

Critical Path: 7.1 → 7.2 → 7.4 → 7.7
Maximum Duration: 22-30 hours (sequential)
With Parallelization: 7.3, 7.5 can run parallel with 7.4, saving 10-12 hours
```

### Parallel Opportunities

**Can run in parallel (after 7.2):**
- 7.3: Merge vs. rebase strategy (independent of rules)
- 7.4: Architecture alignment rules (independent of strategy)
- 7.5: Conflict resolution (can use criteria from 7.2)

All three are independent of each other. **Estimated parallel execution saves 10-12 hours.**

**Must be sequential:**
- 7.1 → 7.2 (criteria depend on branch analysis)
- 7.2 → 7.4 (rules depend on criteria)
- All → 7.7 (master guide needs all components)

### Timeline with Parallelization

**Days 1-2: Analysis & Criteria (7.1-7.2)**
- Day 1: Analyze current branch state (7.1)
- Day 1-2: Define target selection criteria (7.2)

**Days 2-4: Rules & Strategy (7.3, 7.4, 7.5 in parallel)**
- Day 2-3: Merge vs. rebase strategy (7.3, 1 person)
- Day 2-3: Architecture alignment rules (7.4, 1 person)
- Day 3-4: Conflict resolution (7.5, 1 person, can overlap)

**Days 4-5: Verification & Guide (7.6-7.7)**
- Day 4: Branch assessment checklist (7.6)
- Day 5: Master framework guide (7.7)

**Total: 5-7 days with parallelization**

---

## Subtasks

### 7.1: Analyze Current Branch State & Alignment Needs
**Purpose:** Understand what branches exist, their divergence, and what alignment looks like  
**Effort:** 4-6 hours

**Steps:**
1. List all active feature branches in repository
2. Assess divergence from main/scientific for each
3. Identify shared history and common ancestors
4. Document which branches conflict with each other
5. Categorize branches by complexity (simple, moderate, complex)

**Success Criteria:**
- [ ] Complete inventory of 15+ branches (or all active branches)
- [ ] Divergence metrics documented (commits behind, days since last commit)
- [ ] Shared history patterns identified
- [ ] Complexity categories assigned
- [ ] Ready as input for 7.2 (target selection criteria)

**Blocks:** 7.2, 7.4

---

### 7.2: Define Target Branch Selection Criteria
**Purpose:** Create decision matrix for assigning optimal targets  
**Effort:** 6-8 hours  
**Depends on:** 7.1

**Steps:**
1. Identify 5-8 factors for target selection (similarity, history, architecture, priority, age)
2. Define measurement for each factor (0-1 scale)
3. Assign weights that sum to 1.0 (typically: 0.25, 0.20, 0.20, 0.15, 0.10, 0.05, 0.05)
4. Create scoring formula (weighted sum or decision tree)
5. Test formula on 3-5 real branches from 7.1

**Success Criteria:**
- [ ] 5-8 clear criteria with measurement method
- [ ] Weights documented and justified
- [ ] Scoring formula defined
- [ ] Formula tested on real branches
- [ ] Score consistently produces valid targets

**Blocks:** 7.3, 7.4, 7.7

---

### 7.3: Document Merge vs. Rebase Strategy
**Purpose:** Create decision tree for merge vs. rebase selection  
**Effort:** 4-6 hours  
**Depends on:** 7.2 (can start after, needs criteria context)

**Steps:**
1. Define conditions for merge (e.g., shared history, long-lived branches)
2. Define conditions for rebase (e.g., linear history, short-lived branches)
3. Create decision tree with clear branching logic
4. Document trade-offs of each approach
5. Provide examples for each scenario

**Success Criteria:**
- [ ] Clear conditions for each strategy
- [ ] Decision tree with yes/no branches
- [ ] Trade-offs documented
- [ ] Minimum 3 examples for each approach
- [ ] Unambiguous guidance for choosing

**Blocks:** 7.7

---

### 7.4: Define Architecture Alignment Rules & Validation
**Purpose:** Establish rules for architectural consistency during alignment  
**Effort:** 6-8 hours  
**Depends on:** 7.2

**Steps:**
1. Define 10+ architectural rules (module boundaries, imports, structure)
2. Specify validation method for each rule (static analysis, manual review, tests)
3. Create checklist for pre-alignment validation
4. Create checklist for post-alignment validation
5. Document what to do if alignment violates rules

**Success Criteria:**
- [ ] 10+ specific rules defined
- [ ] Validation method for each rule
- [ ] Pre-alignment checklist created
- [ ] Post-alignment checklist created
- [ ] Clear escalation path if rules violated

**Blocks:** 7.7

---

### 7.5: Create Conflict Resolution Framework
**Purpose:** Document how to identify and resolve merge conflicts  
**Effort:** 4-6 hours  
**Depends on:** 7.2

**Steps:**
1. Identify 6+ common conflict scenarios
2. Document resolution approach for each
3. Create priority rules (e.g., "choose feature code over target code")
4. Define when to escalate conflicts
5. Provide testing steps after resolution

**Success Criteria:**
- [ ] 6+ conflict scenarios documented
- [ ] Resolution approach for each
- [ ] Priority rules defined and justified
- [ ] Escalation criteria defined
- [ ] Post-resolution testing specified

**Blocks:** 7.7

---

### 7.6: Create Branch Assessment Checklist & Examples
**Purpose:** Provide template and real examples for evaluating branches  
**Effort:** 6-8 hours  
**Depends on:** 7.1, 7.2, 7.4

**Steps:**
1. Create checklist template with 15-20 items
2. Include pre-alignment checks
3. Include post-alignment checks
4. Fill in checklist for 3-5 real branches from 7.1
5. Document what "passing" looks like for each item

**Success Criteria:**
- [ ] 15-20 item checklist created
- [ ] Pre and post-alignment sections
- [ ] Real examples filled in
- [ ] Clear pass/fail criteria for each item
- [ ] Checklist is repeatable for future branches

**Blocks:** 7.7

---

### 7.7: Compile Framework Documentation & Create Master Guide
**Purpose:** Create final framework guide for downstream tasks  
**Effort:** 6-8 hours  
**Depends on:** 7.2, 7.3, 7.4, 7.5, 7.6 (or at least 7.2)

**Steps:**
1. Consolidate all outputs (criteria, rules, strategies, checklists)
2. Create 3-5 page master guide
3. Add navigation and quick reference
4. Include flowcharts for decision points
5. Add real-world examples for each component

**Success Criteria:**
- [ ] Master guide 3-5 pages
- [ ] All components integrated
- [ ] Flowcharts for key decisions
- [ ] 5+ real-world examples
- [ ] Ready for hand-off to Tasks 77, 79, 81

---

## Configuration & Defaults

### Branch Alignment Framework Configuration

```yaml
# branch_alignment_framework.yaml
# Task 7: Framework definition configuration

framework_metadata:
  name: "Feature Branch Alignment Framework"
  version: "1.0"
  created_date: "2025-01-04"
  owner: "Architecture Team"
  downstream_tasks: [77, 79, 81]

target_selection_criteria:
  # Factors for determining optimal target branch
  codebase_similarity:
    weight: 0.30
    scale: [0, 1]
    measurement: "file overlap percentage"
    
  git_history_depth:
    weight: 0.25
    scale: [0, 1]
    measurement: "commits shared with target"
    
  architectural_alignment:
    weight: 0.20
    scale: [0, 1]
    measurement: "module/import compatibility"
    
  team_priority:
    weight: 0.15
    scale: [0, 1]
    measurement: "project priority score"
    
  branch_age_factor:
    weight: 0.10
    scale: [0, 1]
    measurement: "days since last commit"

merge_strategy_rules:
  # When to use merge vs. rebase
  use_merge_if:
    - "shared_history_commits > 100"
    - "branch_age_days > 30"
    - "multiple_developers: true"
    - "public_branch: true"
    
  use_rebase_if:
    - "linear_history_required: true"
    - "branch_age_days < 7"
    - "single_developer: true"
    - "experimental_branch: true"
  
  default_strategy: "merge"

architecture_rules:
  # Architectural constraints for alignment
  required_directories:
    - "src/"
    - "tests/"
    - "docs/"
  
  forbidden_imports:
    - "backend → frontend"
    - "core → temporary"
    - "utils → domain"
  
  critical_files:
    - "setup/__init__.py"
    - "AGENTS.md"
    - "config/defaults.yaml"
  
  min_test_coverage: 80
  
  architecture_checks:
    - "no circular dependencies"
    - "module boundaries respected"
    - "import hierarchy maintained"

conflict_resolution_priority:
  # How to resolve conflicts
  prefer: "feature_code"  # "feature_code" or "target_code"
  
  conflict_scenarios:
    - name: "both modified same file"
      approach: "manual review + merge"
      escalate_if: ">20 conflicts in single file"
    
    - name: "conflicting requirements"
      approach: "align with architecture team"
      escalate_if: "impacts module boundary"
    
    - name: "binary files conflicted"
      approach: "pick one version, merge manually"
      escalate_if: "affects critical files"

verification:
  # Validation requirements
  require_tests_pass: true
  min_test_coverage: 80
  require_ci_pass: true
  require_lint_pass: true
  require_code_review: true
  min_approvals: 1
  
  pre_alignment_checks:
    - "branches exist and accessible"
    - "current changes committed"
    - "ci passing on both branches"
    - "no uncommitted changes"
  
  post_alignment_checks:
    - "merge/rebase completed without failures"
    - "conflicts resolved"
    - "tests pass on aligned branch"
    - "architecture rules respected"
    - "ci passes on aligned branch"

safety:
  # Risk mitigation
  create_backup_branch: true
  backup_naming: "{branch}-backup-{date}"
  enable_rollback: true
  rollback_retention_days: 7
  require_dry_run: true
  
  dry_run_checks:
    - "merge_simulation"
    - "conflict_detection"
    - "architecture_validation"
    - "test_impact_analysis"

reporting:
  # Documentation and tracking
  output_format: "json"
  include_metrics: true
  include_decision_rationale: true
  log_level: "INFO"
  log_format: "structured"
```

---

## Framework Components

### 1. Target Selection Criteria (from 7.2)

**Formula:** `target_score = Σ(factor_i × weight_i)`

**Scoring Method:**
- Each factor normalized to [0, 1]
- Weights sum to 1.0
- Final score ≥ 0.65 required for assignment
- Top score wins (usually main or scientific)

**Factors:**
1. **Codebase Similarity** (0.30) - File overlap with target
2. **Git History Depth** (0.25) - Common commits with target
3. **Architectural Alignment** (0.20) - Module compatibility
4. **Team Priority** (0.15) - Project importance
5. **Branch Age** (0.10) - Staleness factor

### 2. Merge vs. Rebase Decision Tree (from 7.3)

```
Is linear history required?
├─ YES → Use REBASE
│   └─ Exception: If shared history > 100 commits, use MERGE instead
└─ NO → Use MERGE (default)
    └─ Exception: If experimental/temporary, consider REBASE
```

### 3. Architecture Alignment Rules (from 7.4)

**Required Rules (must not violate):**
1. No forbidden imports (e.g., backend → frontend)
2. All required directories present
3. Module boundaries respected
4. Critical files unmodified (setup, config, docs)

**Validation Points:**
- Pre-alignment: Static analysis on current state
- Post-alignment: Re-run after merge, verify still clean

### 4. Conflict Resolution (from 7.5)

**Priority:** Feature code > Target code > Manual review

**Escalation Triggers:**
- >20 conflicts in single file → Architecture review
- Conflicts in critical files → Team lead approval
- Conflicts in module boundaries → Architecture team

---

## Decision Criteria for Target Selection

### How to Assign an Optimal Target

**Process:**

1. **Calculate Codebase Similarity** (0-1 scale)
   ```
   similarity = (files_in_common / max(files_branch, files_target)) × 100%
   normalized = similarity / 100
   ```

2. **Calculate Git History Depth** (0-1 scale)
   ```
   common_commits = commits_in_both_branches
   normalized = min(common_commits / 100, 1.0)
   ```

3. **Calculate Architectural Alignment** (0-1 scale)
   ```
   alignment = (imports_valid / total_imports) × (no_violations ? 1.0 : 0.8)
   ```

4. **Assign Priority Score** (0-1 scale)
   ```
   Based on project plan: 1.0 for critical, 0.5 for medium, 0.2 for low
   ```

5. **Apply Age Factor** (0-1 scale)
   ```
   days_since_commit = today - last_commit_date
   age_score = exp(-days_since_commit / 30)  # 30-day decay window
   ```

6. **Calculate Final Score**
   ```
   final_score = (0.30 × similarity) + (0.25 × history) + 
                 (0.20 × architecture) + (0.15 × priority) + 
                 (0.10 × age)
   
   target = branch with highest_score (≥ 0.65)
   ```

**Example:**
- Feature branch: feature/auth-system
- Candidates: main, scientific, develop

| Factor | main | scientific | develop |
|--------|------|-----------|---------|
| Similarity (0.30) | 0.85 × 0.30 = 0.255 | 0.45 × 0.30 = 0.135 | 0.72 × 0.30 = 0.216 |
| History (0.25) | 0.92 × 0.25 = 0.230 | 0.55 × 0.25 = 0.138 | 0.68 × 0.25 = 0.170 |
| Architecture (0.20) | 0.88 × 0.20 = 0.176 | 0.42 × 0.20 = 0.084 | 0.70 × 0.20 = 0.140 |
| Priority (0.15) | 0.95 × 0.15 = 0.143 | 0.70 × 0.15 = 0.105 | 0.60 × 0.15 = 0.090 |
| Age (0.10) | 0.78 × 0.10 = 0.078 | 0.65 × 0.10 = 0.065 | 0.82 × 0.10 = 0.082 |
| **TOTAL** | **0.882** ✅ | **0.527** ❌ | **0.698** ✅ |

**Result:** Main wins (0.882), feature/auth-system → main

---

## Typical Development Workflow

### Step-by-Step Framework Creation

```bash
# Task 7: Create Branch Alignment Framework
# Follow these steps in order

# Step 1: Analyze current branch state (7.1, 4-6h)
git branch -a | grep -E "feature/|docs-|fix/" > branch_inventory.txt
# For each branch: git log --oneline branch..main | wc -l

# Step 2: Define target selection criteria (7.2, 6-8h)
# Edit branch_alignment_framework.yaml
# Define 5-8 factors with weights (sum = 1.0)
# Create scoring formula
# Test on 3-5 real branches

# Step 3: Document merge vs. rebase strategy (7.3, 4-6h)
# Create MERGE_VS_REBASE_DECISION.md
# Define conditions for each approach
# Create decision tree with clear logic

# Step 4: Define architecture rules (7.4, 6-8h)
# Identify 10+ architectural rules
# Document validation method for each
# Create pre/post alignment checklists

# Step 5: Create conflict resolution framework (7.5, 4-6h)
# Document 6+ common conflict scenarios
# Provide resolution approach for each
# Define escalation criteria

# Step 6: Create branch assessment checklist (7.6, 6-8h)
# Create 15-20 item checklist
# Fill in with real branch examples (3-5)
# Document pass/fail criteria

# Step 7: Compile master guide (7.7, 6-8h)
# Consolidate all outputs
# Create 3-5 page master guide
# Add flowcharts and examples

# Validation
git add task-7.md branch_alignment_framework.yaml MERGE_VS_REBASE_DECISION.md
git commit -m "feat: complete Task 7 framework definition"
```

### Development Commands

```bash
# Verify framework completeness
grep -c "^###\|^##" task-7.md  # Should have 20+ sections

# Validate YAML configuration
python3 -c "import yaml; yaml.safe_load(open('branch_alignment_framework.yaml'))"

# Test decision criteria on real branches
for branch in $(git branch -r | grep feature/); do
    echo "Scoring $branch..."
    # Run scoring formula on $branch
done

# Create framework documentation
echo "# Branch Alignment Framework" > FRAMEWORK_GUIDE.md
cat task-7.md branch_alignment_framework.yaml >> FRAMEWORK_GUIDE.md
```

---

## Integration Handoff

### Output Specification for Downstream Tasks

Task 7 produces three key deliverables for Tasks 77, 79, 81:

#### 1. Target Selection Criteria (→ Task 77)

**Input to Task 77:** Scoring criteria and formula

```json
{
  "target_selection_criteria": {
    "factors": [
      {
        "name": "codebase_similarity",
        "weight": 0.30,
        "measurement": "file_overlap_percentage"
      },
      {
        "name": "git_history_depth",
        "weight": 0.25,
        "measurement": "common_commits"
      }
    ],
    "formula": "weighted_sum",
    "min_threshold": 0.65,
    "primary_targets": ["main", "scientific"]
  }
}
```

**Used by Task 77 to:** Score each feature/X branch and assign optimal target

#### 2. Merge/Rebase Decision Framework (→ Task 79)

**Input to Task 79:** Decision tree for choosing merge vs. rebase

```json
{
  "merge_rebase_strategy": {
    "decision_tree": {
      "linear_history_required": {
        "yes": "use_rebase",
        "no": {
          "shared_history_gt_100": {
            "yes": "use_merge",
            "no": "use_rebase"
          }
        }
      }
    },
    "default": "merge"
  }
}
```

**Used by Task 79 to:** Choose correct strategy for each branch's alignment

#### 3. Verification Checklist (→ Task 81)

**Input to Task 81:** Pre/post alignment validation steps

```json
{
  "verification_checklist": {
    "pre_alignment": [
      "branch_exists",
      "ci_passing_on_branch",
      "no_uncommitted_changes",
      "no_pending_reviews"
    ],
    "post_alignment": [
      "merge_completed_without_failures",
      "conflicts_resolved",
      "tests_pass",
      "architecture_rules_respected",
      "ci_passes"
    ]
  }
}
```

**Used by Task 81 to:** Validate scientific branch alignment before final merge to main

### Format Specifications

**JSON Schema for Framework Output:**

```json
{
  "framework": {
    "metadata": {
      "version": "string",
      "created_date": "ISO8601",
      "owner": "string"
    },
    "target_selection_criteria": {
      "factors": [{"name": "string", "weight": "number (0-1)", "measurement": "string"}],
      "formula": "string",
      "min_threshold": "number (0-1)"
    },
    "merge_rebase_strategy": {
      "decision_tree": "object",
      "default_strategy": "enum(merge|rebase)"
    },
    "architecture_rules": [
      {
        "rule": "string",
        "validation_method": "string",
        "critical": "boolean"
      }
    ],
    "conflict_resolution": [
      {
        "scenario": "string",
        "approach": "string",
        "priority": "string"
      }
    ],
    "verification_checklist": {
      "pre_alignment": ["string"],
      "post_alignment": ["string"]
    }
  }
}
```

### Integration Points

| Task | Receives | Provides |
|------|----------|----------|
| **Task 77** | Target criteria | Branch→target assignments |
| **Task 79** | Merge/rebase decision tree | Execution strategy |
| **Task 81** | Verification checklist | Validation results |

---

## Common Gotchas & Solutions

### Gotcha 1: Target Selection Scoring Produces Ties ⚠️

**Problem:** Two targets have identical score (e.g., both 0.75)  
**Symptom:** Unclear which target to choose when scores equal  
**Root Cause:** Weights not fine-grained enough, or insufficient tiebreaker criteria

**Solution:** Add tiebreaker rules
```yaml
target_selection_tiebreaker:
  rule_1: "prefer_main_over_scientific"
  rule_2: "prefer_older_branch_if_ages_similar"
  rule_3: "prefer_more_recent_activity"
```

**Test:** Create two fake branches with identical scores, verify tiebreaker applied

---

### Gotcha 2: Merge Conflicts Arise from Different Architectures 🔴

**Problem:** Merging branches with conflicting module structures causes conflicts  
**Symptom:** Hundreds of merge conflicts, impossible to resolve manually  
**Root Cause:** Architecture rules not checked before alignment

**Solution:** Pre-alignment architecture validation
```bash
# Before merge, check architecture compatibility
git diff --name-only main feature/branch | \
  grep -E "src/backend|module_boundaries.yaml" && \
  echo "⚠️ Architecture risk - review before merge"
```

**Test:** Attempt to merge branch that violates architecture rules, catch before merge

---

### Gotcha 3: Branch Age Metric Produces Counterintuitive Results ⚠️

**Problem:** Very old stale branch (6 months) scores higher than recent (2 weeks)  
**Symptom:** Framework assigns targets irrationally  
**Root Cause:** Age weight too high, or aging function incorrect

**Solution:** Use exponential decay correctly
```python
import math
days_since = (today - last_commit).days
age_score = math.exp(-days_since / 30)  # 30-day half-life
# Result: 30 days ago = 0.37, 1 day ago = 0.97
```

**Test:** Score branches of various ages, verify younger branches score higher

---

### Gotcha 4: Git History Depth Fails on Orphaned Branches 🔴

**Problem:** Orphaned branches have no common ancestor, can't calculate history depth  
**Symptom:** `git merge-base` fails, scoring breaks  
**Root Cause:** No error handling for orphaned branches

**Solution:** Handle orphaned branches gracefully
```bash
git merge-base branch1 branch2 2>/dev/null || {
  echo "⚠️ Orphaned branch detected"
  common_commits=0
  history_score=0.0
}
```

**Test:** Attempt to score branch with no common history to main, verify graceful fallback

---

### Gotcha 5: Codebase Similarity Metric Over-Weights File Count ⚠️

**Problem:** Branch modifying only 2 files in large codebase scores low (5% overlap)  
**Symptom:** Small legitimate branches get wrong target assignment  
**Root Cause:** Similarity formula doesn't account for relative change size

**Solution:** Use normalized similarity metric
```python
files_changed = len(changed_files)
total_files = len(all_files)
change_significance = min(files_changed / total_files, 1.0)
# Now small changes in large repo get fair score
```

**Test:** Create branch modifying 5 files in 10k-file repo, verify fair scoring

---

### Gotcha 6: Priority Score Becomes Subjective and Gamed ⚠️

**Problem:** Different team members assign different priorities to same branch  
**Symptom:** Framework produces inconsistent results, loses credibility  
**Root Cause:** Priority scoring criteria unclear

**Solution:** Explicitly define priority levels
```yaml
priority_levels:
  critical: 1.0      # Blocks release, security fix, critical bug
  high: 0.8          # Needed for current sprint
  medium: 0.5        # Nice to have, planned work
  low: 0.2           # Backlog, experimental
  
priority_source: "GitHub milestone or Jira priority"
```

**Test:** Have 3 people score same branch, verify ±0.1 variance

---

### Gotcha 7: Merge Strategy Decision Ignores Team Preferences 🔴

**Problem:** Decision tree chooses rebase, but team standardized on merge  
**Symptom:** Framework conflicts with team conventions  
**Root Cause:** No consideration of organizational preferences

**Solution:** Allow override with documentation
```yaml
merge_strategy_rules:
  default: "merge"  # Organizational standard
  
  rebase_exceptions:
    - "if linear history required by security review"
    - "if commit count < 10 AND branch age < 7 days"
    
  decision_override:
    allowed: true
    required_approval: "tech lead"
    must_document: true
```

**Test:** Override decision for test branch, verify documentation requirement

---

### Gotcha 8: Conflict Resolution Priority Oversimplifies Complex Cases 🔴

**Problem:** "Prefer feature code" breaks when feature code is buggy  
**Symptom:** Choosing wrong code, causes regressions post-alignment  
**Root Cause:** Priority rule doesn't account for code quality

**Solution:** Add escalation for significant conflicts
```yaml
conflict_escalation:
  triggers:
    - ">20 conflicts in single file"
    - "conflicts in critical files"
    - "conflicting logic/algorithms"
    - "conflicts in tests"
    
  escalation_path: "architecture team review"
  required_approval: true
```

**Test:** Create scenario with 50 conflicts, verify escalation triggered

---

### Gotcha 9: Framework Documentation Becomes Outdated Quickly 🔴

**Problem:** Branch naming conventions change, framework still references old patterns  
**Symptom:** Framework guidance contradicts current repository state  
**Root Cause:** No mechanism to keep framework in sync with reality

**Solution:** Add maintenance schedule and feedback loop
```yaml
framework_maintenance:
  review_schedule: "quarterly"
  feedback_mechanism: "GitHub issues tagged 'framework-feedback'"
  update_triggers:
    - "branch naming convention changes"
    - "architecture changes"
    - "new team preferences"
  
  version_history: "FRAMEWORK_CHANGELOG.md"
```

**Test:** Run framework against repository quarterly, document needed updates

---

## Integration Checkpoint

**When to move to Tasks 77, 79, 81:**
- [ ] All 7 subtasks complete
- [ ] Framework documentation complete (3-5 pages)
- [ ] All deliverables match specification
- [ ] Examples tested against real branches
- [ ] No validation errors
- [ ] Commit message: "feat: complete Task 7 branch alignment framework"

**Handoff validation:**
```bash
# Verify all outputs exist and are valid
test -f task-7.md && echo "✓ Framework guide"
test -f branch_alignment_framework.yaml && echo "✓ Configuration"
python3 -c "import yaml; yaml.safe_load(open('branch_alignment_framework.yaml'))" && echo "✓ Valid YAML"
grep -c "^###" task-7.md | awk '{if($1>=20) print "✓ Comprehensive documentation"}'
```

---

## Notes for Implementer

**Framework Design Principles:**
1. Be explicit - no ambiguous guidance
2. Be testable - all criteria should be measurable
3. Be repeatable - any team member should get same result
4. Be maintainable - include version and update mechanism
5. Be flexible - allow documented overrides

**Edge Cases (Must Handle):**
- Orphaned branches (no common ancestor)
- Stale branches (6+ months no commits)
- Very large divergence (1000+ commits behind)
- Architecture violations
- Critical files modified
- Binary files in conflicts

**Quality Checklist:**
- All scoring criteria normalized to [0,1]
- All weights sum to 1.0
- All formulas tested on ≥3 real branches
- All rules have examples
- All procedures are clear enough for automation

---

## Done Definition

Task 7 is done when:
1. All 7 subtasks marked complete
2. Framework documentation complete (3-5 pages)
3. All 7 deliverables present and validated
4. Framework tested on 5+ real branches
5. Examples all use realistic scenarios
6. Ready for hand-off to Tasks 77, 79, 81
7. All gotchas documented with solutions
8. Stakeholder approval obtained
