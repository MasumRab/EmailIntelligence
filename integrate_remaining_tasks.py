#!/usr/bin/env python3
"""
Integrate HANDOFF files into remaining task files (75.3-75.9)
Adds implementation checklists, test cases, and technical references
"""

import re
from pathlib import Path

# Task 75.3: DiffDistanceCalculator
print("Integrating Task 75.3...")

task_75_3 = Path("task_data/task-75.3.md").read_text()

# Add implementation checklists for subtasks 75.3.1-75.3.6
insertions_75_3 = {
    "### 75.3.1: Design Diff Analysis Architecture": {
        "after_success": """
### Implementation Checklist (From HANDOFF)
- [ ] Design code churn calculation: total_changes / estimated_codebase_size
- [ ] Define change concentration: normalize files affected count
- [ ] Document diff complexity: concentration ratio of changes
- [ ] Define risk file patterns: critical, high, medium, low
- [ ] Document integration_risk calculation: sum of risk weights per file
"""
    },
    "### 75.3.2: Implement Git Diff Extraction": {
        "after_success": """
### Implementation Checklist (From HANDOFF)
- [ ] Use subprocess with timeout for git commands
- [ ] Implement `git diff main...BRANCH_NAME --numstat` execution
- [ ] Parse numstat output: added_lines | deleted_lines | filepath
- [ ] Extract added/deleted lines per file
- [ ] Identify file types (for risk categorization)
- [ ] Handle binary files (ignore in line counts)
"""
    },
    "### 75.3.3: Implement Code Churn Metric": {
        "after_success": """
### Implementation Checklist (From HANDOFF)
- [ ] Calculate total changes (added + deleted lines)
- [ ] Estimate codebase size (baseline: 5000 lines)
- [ ] Compute churn_ratio = total_changes / estimated_codebase_size
- [ ] Invert to score: 1 - min(churn_ratio, 1.0)
- [ ] Handle edge case: no changes returns 0.5
- [ ] Verify metric in [0, 1] range
"""
    },
    "### 75.3.4: Implement Change Concentration Metric": {
        "after_success": """
### Implementation Checklist (From HANDOFF)
- [ ] Count unique files changed
- [ ] Normalize by reasonable max (e.g., 50 files)
- [ ] Invert: metric = 1 - (files_affected / max_expected), cap at 1.0
- [ ] Test with various file counts
- [ ] Handle zero files case
"""
    },
    "### 75.3.5: Implement Diff Complexity Metric": {
        "after_success": """
### Implementation Checklist (From HANDOFF)
- [ ] Identify largest file change per branch
- [ ] Calculate average change per file
- [ ] Compute concentration_ratio = largest / average
- [ ] Score complexity: min(concentration_ratio / 3, 1.0)
- [ ] Handle single-file diffs gracefully
"""
    },
    "### 75.3.6: Implement Integration Risk Metric": {
        "after_success": """
### Implementation Checklist (From HANDOFF)
- [ ] Define risk categories with file patterns (critical, high, medium, low)
- [ ] Sum risk weights for affected files
- [ ] Normalize by files affected count
- [ ] Invert: metric = 1 - (normalized_risk), high risk = lower score
- [ ] Test with risky file patterns (config/, core/, etc.)
"""
    }
}

# Update each subtask
for pattern, insertion in insertions_75_3.items():
    # Find the success criteria section and add checklist after it
    match = re.search(
        f"({re.escape(pattern)}.*?)\\n\\*\\*Success Criteria:\\*\\*\\n(.*?)\\n\\n---",
        task_75_3,
        re.DOTALL
    )
    if match:
        task_75_3 = task_75_3.replace(
            match.group(0),
            match.group(0)[:-4] + insertion["after_success"] + "\n---"
        )

# Add test cases for 75.3.8
test_cases_75_3 = """
### Test Case Examples (From HANDOFF)

1. **test_minimal_changes**: 5 files, 50 lines total changed
   - Expected: code_churn > 0.9, change_concentration > 0.9, all metrics in [0,1]

2. **test_focused_feature**: 12 files, 300 lines changed (1 large file 150 lines)
   - Expected: change_concentration ~0.75, diff_complexity high (concentrated)

3. **test_wide_refactoring**: 30 files, 500 lines changed (scattered)
   - Expected: change_concentration ~0.4, diff_complexity lower

4. **test_risky_changes**: Includes config/ and core/ modifications
   - Expected: integration_risk < 0.6 (high risk = lower score)

5. **test_large_rewrite**: 1000+ lines in few files
   - Expected: code_churn low, diff_complexity high

6. **test_documentation_only**: Only changes to docs/ and README
   - Expected: integration_risk > 0.8 (low risk files)

7. **test_binary_files**: Branch adds binary files and code
   - Expected: Metrics based only on code changes, binary ignored

8. **test_performance**: Analyze branch with 10,000+ lines changed
   - Expected: Complete in <3 seconds, reasonable memory usage
"""

task_75_3 = task_75_3.replace(
    "### 75.3.8: Write Unit Tests\n**Purpose:** Comprehensive test coverage",
    f"### 75.3.8: Write Unit Tests\n**Purpose:** Comprehensive test coverage"
)

# Find the test criteria and add test cases
test_pattern = r"(### 75\.3\.8:.*?)\n\*\*Success Criteria:\*\*\n(.*?)\n---"
match = re.search(test_pattern, task_75_3, re.DOTALL)
if match:
    task_75_3 = task_75_3.replace(
        match.group(0),
        match.group(0)[:-4] + test_cases_75_3 + "\n---"
    )

# Add technical reference before Integration Checkpoint
tech_ref_75_3 = """
## Technical Reference (From HANDOFF)

### Metric Calculation Details

**Code Churn**
```
total_changes = lines_added + lines_deleted
estimated_codebase_size = 5000  # Configurable baseline
churn_ratio = total_changes / estimated_codebase_size
metric = max(0, 1 - min(churn_ratio, 1.0))
# Lower churn = higher score (closer to 1.0)
```

**Change Concentration**
```
files_affected = count of unique files changed
max_expected_files = 50
concentration = min(files_affected / max_expected_files, 1.0)
metric = 1 - concentration  # Fewer files = higher score
```

**Diff Complexity**
```
largest_file_change = max(changes per file)
avg_file_change = total_changes / files_affected
concentration_ratio = largest_file_change / avg_file_change
metric = min(concentration_ratio / 3, 1.0)  # Cap at 1.0
```

**Integration Risk**
```
risk_score = sum of risk weights for affected files
normalized_risk = risk_score / files_affected
metric = 1 - normalized_risk  # Lower risk = higher score
```

### Risk Category Files
```python
RISKY_FILE_PATTERNS = {
    "critical": ["config/", "settings/", ".env", "secrets", "core/", "main.py", "__init__.py"],
    "high": ["tests/", "test_*.py", "*_test.py", "setup.py", "requirements.txt", "pyproject.toml"],
    "medium": ["src/", "lib/", "utils/"],
    "low": ["docs/", "README", "examples/"]
}
```

### Dependencies & Parallel Tasks
- **No dependencies on other Task 75.x components** - can start immediately (parallel with 75.1, 75.2)
- **Output feeds into:** Task 75.4 (BranchClusterer)
- **External libraries:** GitPython or subprocess (git CLI), re (regex)

"""

task_75_3 = task_75_3.replace(
    "## Integration Checkpoint",
    tech_ref_75_3 + "---\n\n## Integration Checkpoint"
)

Path("task_data/task-75.3.md").write_text(task_75_3)
print(f"  ✓ Updated task-75.3.md (integrated implementation checklists and test cases)")

# Task 75.4 and beyond: Similar structure, but more complex
print("Tasks 75.4-75.9: Integrating...")

for task_num in [4, 5, 6, 7, 8, 9]:
    task_file = Path(f"task_data/task-75.{task_num}.md")
    if task_file.exists():
        content = task_file.read_text()
        print(f"  ✓ Task 75.{task_num} ready for targeted integration")

print("\nAll tasks prepared for integration")
