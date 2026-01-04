# Task 75 Improvement Template

**Use this template to apply Week 1 improvements to each remaining task file (75.2-75.9)**

---

## Section 1: Quick Navigation

Copy this after Purpose section, before Developer Quick Reference:

```markdown
---

## Quick Navigation

Navigate this document using these links:

- [Purpose](#purpose)
- [Developer Quick Reference](#developer-quick-reference)
- [Success Criteria](#success-criteria)
- [Subtasks Overview](#subtasks-overview)
- [Subtask Details](#subtasks)
- [Configuration](#configuration-parameters) [or appropriate section name]
- [Technical Reference](#technical-reference)
- [Common Gotchas & Solutions](#common-gotchas--solutions)
- [Development Workflow](#typical-development-workflow)
- [Integration Handoff](#integration-handoff)
- [Integration Checkpoint](#integration-checkpoint)
- [Done Definition](#done-definition)

**Pro tip:** Use Ctrl+F to search within sections, or click links above to jump directly

---
```

---

## Section 2: Performance Baselines

Replace the existing Success Criteria section with:

```markdown
## Success Criteria

Task 75.X is complete when:

**Core Functionality:**
[Keep existing core functionality items]

**Performance Targets:**
- [ ] [Operation name]: **< X seconds** (on typical scenario)
- [ ] Memory usage: **< Y MB** per operation
- [ ] Handles **[large dataset description]** without failure
- [ ] [Metric name]: **O(complexity)** where X = [variable]
- [ ] [Timeout/critical metric]: **Z seconds max**

**Quality Assurance:**
[Keep existing quality items, remove duplicate performance items]

**Integration Readiness:**
[Keep existing integration items]
```

---

## Section 3: Subtasks Overview

Insert this as a new section before the "## Subtasks" section:

```markdown
---

## Subtasks Overview

### Dependency Flow Diagram

```
[TASK A] (X-Yh) ────────┐
[Task A Name]           │
                        ├─→ [TASK B] (A-Bh) ────────┐
                        │  [Task B Name]             │
                        │                            ├─→ [TASKS C-E] (parallel) ────┐
                        │                            │   [Parallel task names]      │
                        │                            │                              ├─→ [TASK F] (X-Yh)
                        └────────────────────────────┘                              │  [Final task]
                                                                                    │
                                                                                    └─→ [TASK G] (A-Bh)
                                                                                       [Testing task]

Critical Path: [TASK A] → [TASK B] → [TASKS C-E] (parallel) → [TASK F] → [TASK G]
Minimum Duration: X-Y hours (with parallelization)
```

### Parallel Opportunities

**Can run in parallel (after [dependency]):**
- [Task 1]: [Description]
- [Task 2]: [Description]
- [Task 3]: [Description]

All tasks depend only on [parent task] and are independent of each other. **Estimated parallel execution saves X-Y hours.**

**Must be sequential:**
- [Task A] → [Task B] (reason)
- [Task B] → [Task C] (reason)
- [Task C] → [Task D] (reason)

### Timeline with Parallelization

**Days 1-2: [First Phase] ([TASK A])**
- [Subtask 1]
- [Subtask 2]

**Days 2-3: [Second Phase] ([TASK B])**
- [Subtask 1]
- [Subtask 2]

**Days 3-5: [Parallel Phase] ([TASKS C-E] in parallel)**
- Days 3-4: [Task 1] + [Task 2] (2 people)
- Days 3-4: [Task 3] + [Task 4] (2 people)
- Days 4-5: [Task 5] (can overlap)

**Days 5-6: [Integration Phase] ([TASKS F-G])**
- Day 5: [Task F description]
- Day 6: [Task G description]

---
```

---

## Section 4: Configuration & Defaults

Replace the existing "## Configuration Parameters" section with:

```markdown
## Configuration & Defaults

All parameters should be externalized to configuration files (not hardcoded). Use YAML format:

```yaml
# config/[component_name].yaml
[component_name]:
  # [Category Name]
  param_name_1: value1  # [Description/unit]
  param_name_2: value2  # [Description/unit]
  
  # [Another Category]
  param_name_3: value3  # [Description/unit]
  param_name_4: value4  # [Description/unit]
```

**How to use in code:**
```python
import yaml

def load_config(config_path='config/[component].yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)['[component_name]']

config = load_config()
PARAM_1 = config['param_name_1']
PARAM_2 = config['param_name_2']
# ... etc
```

**Why externalize?**
- Easy to tune without redeploying code
- Different configurations for different environments (dev/test/prod)
- Can adjust thresholds based on organizational needs
- No code recompilation needed to adjust parameters
```

---

## Section 5: Development Workflow

Insert before Integration Checkpoint section:

```markdown
---

## Typical Development Workflow

Complete step-by-step git workflow for implementing this task. Copy-paste ready sequences:

### Setup Your Feature Branch

```bash
# 1. Create and push feature branch
git checkout -b feat/[component-name]
git push -u origin feat/[component-name]

# 2. Create directory structure
mkdir -p src/[component] tests/[component]
touch src/[component]/__init__.py
git add src/[component]/
git commit -m "chore: create [component] module structure"
```

### Subtask [X]: [Task Name]

```bash
# [Specific implementation for this subtask]
cat > src/[component]/[file].py << 'EOF'
# [Code example]
EOF

git add src/[component]/[file].py
git commit -m "feat: implement [feature] ([TASK_ID])"
```

[Repeat for each major subtask]

### Final Steps

```bash
# Create configuration file
mkdir -p config
cat > config/[component].yaml << 'EOF'
[component]:
  param: value
  # [rest of config]
EOF

git add config/
git commit -m "config: [component] configuration parameters"

# Push to origin
git push origin feat/[component-name]

# Create pull request
gh pr create --title "Complete Task 75.X: [Component Name]" \
             --body "Implements [component] with [key features]"
```

---
```

---

## Section 6: Integration Handoff

Insert before Common Gotchas & Solutions:

```markdown
---

## Integration Handoff

### What Gets Passed to Task 75.X (Downstream Task)

**Task 75.X expects input in this format:**

```python
from src.[component] import [ClassName]

[instance] = [ClassName](...)
result = [instance].analyze(...)

# result is a dict like:
# {
#   "key1": value1,
#   "key2": value2,
#   ...
# }
```

**Task 75.X uses these outputs by:**
1. [Step 1: How downstream task consumes this]
2. [Step 2: Second processing step]
3. [Step 3: Final step]

**Validation before handoff:**
```bash
# Verify output matches specification
python -c "
from src.[component] import [ClassName]
[instance] = [ClassName](...)
result = [instance].analyze(...)

# Check required fields
assert '[key1]' in result
assert '[key2]' in result

# Check value ranges/types
assert isinstance(result['[key1]'], [type])
assert 0 <= result['[key2]'] <= 1

print('✓ Output valid and ready for Task 75.X')
"
```

---
```

---

## Section 7: Common Gotchas & Solutions

Insert before Integration Checkpoint:

```markdown
---

## Common Gotchas & Solutions

### Gotcha 1: [Problem Title] ⚠️

**Problem:** [Clear description of what goes wrong]
**Symptom:** [How the problem manifests to the developer]
**Root Cause:** [Why the problem occurs]

**Solution:** [Fix with code example]
```python
[Code showing correct approach]
```

**Test:** [How to verify the fix works]

---

### Gotcha 2: [Problem Title] ⚠️

[Repeat pattern for 6-9 gotchas]

---
```

---

## How to Use This Template

1. **Copy each section above** to the corresponding task file (75.2-75.9)
2. **Customize placeholders:**
   - `[TASK A]`, `[TASK B]` → actual subtask numbers (75.2.1, 75.2.2, etc.)
   - `[Component Name]` → actual component name (CodebaseStructureAnalyzer, etc.)
   - `[Performance metrics]` → task-specific metrics and targets
   - `[Gotchas]` → extract from technical documentation and HANDOFF files
3. **Validate all sections work** (test Quick Navigation links)
4. **Cross-reference** with the technical documentation for each task

---

## Task-Specific Customization Notes

### Task 75.2: CodebaseStructureAnalyzer
- Performance: Focus on directory traversal time, file counts
- Gotchas: Permission errors, symlinks, binary files
- Integration: Next step is Task 75.4 BranchClusterer

### Task 75.3: DiffDistanceCalculator
- Performance: Focus on diff parsing, distance computation
- Gotchas: Large diffs, encoding issues, binary files
- Integration: Next step is Task 75.4 BranchClusterer

### Task 75.4: BranchClusterer
- Performance: Focus on clustering time, quality metrics
- Gotchas: Single branch, identical branches, NaN values
- Integration: Takes input from 75.1-75.3, passes to 75.5-75.6

### Task 75.5: IntegrationTargetAssigner
- Performance: Focus on assignment speed, tag generation
- Gotchas: Ambiguous cases, low confidence, missing data
- Integration: Takes input from 75.4, passes to 75.6

### Task 75.6: PipelineIntegration
- Performance: Focus on end-to-end pipeline time, parallelization
- Gotchas: Cache invalidation, timeout handling, output validation
- Integration: Orchestrates 75.1-75.5, outputs to 75.7-75.8

### Task 75.7: VisualizationReporting
- Performance: Focus on dashboard load time, chart rendering
- Gotchas: Chart rendering performance, PDF generation, responsive design
- Integration: Takes input from 75.6

### Task 75.8: TestingSuite
- Performance: Focus on test execution time, coverage
- Gotchas: Test isolation, fixture management, performance targets
- Integration: Tests all modules 75.1-75.6

### Task 75.9: FrameworkIntegration
- Performance: Focus on framework init, API latency
- Gotchas: Import ordering, dependency conflicts, API versioning
- Integration: Consolidates 75.1-75.8, enables downstream tasks

---

**Use IMPROVEMENT_EXAMPLES.md and TASK_75_IMPROVEMENTS.md for detailed gotchas and examples specific to each task.**
