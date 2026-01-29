#!/usr/bin/env python3
"""
Enhanced Task Specification Improver for Branch Analysis Tasks
Maximizes PRD accuracy by improving branch analysis task specifications
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any
import sys


def improve_branch_analysis_task_spec(task_file_path: str) -> str:
    """
    Improve a branch analysis task specification to maximize PRD accuracy.
    """
    with open(task_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract current information
    task_info = extract_task_info(task_file_path)

    # Create enhanced specification with focus on branch analysis
    enhanced_spec = f"""# Task {task_info.get('id', 'X')}: {task_info.get('title', 'Branch Analysis Task')}

**Status:** {task_info.get('status', 'pending')}
**Priority:** {task_info.get('priority', 'medium')}
**Effort:** {task_info.get('effort', 'TBD')}
**Complexity:** {task_info.get('complexity', 'TBD')}
**Dependencies:** {task_info.get('dependencies', 'None')}
**Blocks:** {task_info.get('blocks', 'None')}
**Owner:** {task_info.get('owner', 'TBD')}
**Created:** {task_info.get('created', '2026-01-16')}
**Updated:** 2026-01-16
**Tags:** branch-analysis, enhanced-specification

---

## Overview/Purpose

{task_info.get('purpose', 'Perform comprehensive branch analysis to inform alignment decisions')}

**Scope:** {task_info.get('scope', 'Branch analysis and target assignment')}
**Focus:** {task_info.get('focus', 'Data-driven branch analysis')}
**Value Proposition:** Enables accurate branch alignment decisions based on quantitative analysis
**Success Indicator:** Provides clear, actionable recommendations for branch alignment

---

## Success Criteria

Task {task_info.get('id', 'X')} is complete when:

### Functional Requirements
"""
    
    # Add specific success criteria for branch analysis tasks
    if 'analyze' in task_info.get('title', '').lower() or 'analysis' in task_info.get('title', '').lower():
        enhanced_spec += f"""- [ ] Branch analysis methodology implemented and validated - Verification: [Method to verify completion]
- [ ] Analysis metrics calculated for all target branches - Verification: [Method to verify completion]
- [ ] Confidence scores assigned to all recommendations - Verification: [Method to verify completion]
- [ ] Analysis results documented in standardized format - Verification: [Method to verify completion]
"""
    elif 'cluster' in task_info.get('title', '').lower():
        enhanced_spec += f"""- [ ] Branch clustering algorithm implemented and tested - Verification: [Method to verify completion]
- [ ] Clusters validated against known branch characteristics - Verification: [Method to verify completion]
- [ ] Cluster assignments documented with confidence scores - Verification: [Method to verify completion]
- [ ] Clustering results integrated with target assignment process - Verification: [Method to verify completion]
"""
    elif 'identify' in task_info.get('title', '').lower():
        enhanced_spec += f"""- [ ] All active feature branches identified and cataloged - Verification: [Method to verify completion]
- [ ] Branch metadata extracted and validated - Verification: [Method to verify completion]
- [ ] Branch status assessment completed - Verification: [Method to verify completion]
- [ ] Comprehensive branch inventory documented - Verification: [Method to verify completion]
"""
    else:
        enhanced_spec += f"""- [ ] Core functionality implemented as specified - Verification: [Method to verify completion]
- [ ] All requirements satisfied - Verification: [Method to verify completion]
- [ ] Output matches expected format - Verification: [Method to verify completion]
- [ ] Integration with downstream processes validated - Verification: [Method to verify completion]
"""

    enhanced_spec += f"""
### Non-Functional Requirements
- [ ] Performance requirements met - Verification: [Method to verify completion]
- [ ] Security requirements satisfied - Verification: [Method to verify completion]
- [ ] Compatibility requirements fulfilled - Verification: [Method to verify completion]

### Quality Gates
- [ ] Code review passed - Verification: [Method to verify completion]
- [ ] Tests passing - Verification: [Method to verify completion]
- [ ] Documentation complete - Verification: [Method to verify completion]

---

## Prerequisites & Dependencies

### Required Before Starting
"""
    deps = task_info.get('dependencies', 'None')
    if deps and deps.lower() not in ['none', 'null']:
        enhanced_spec += f"- [ ] Dependencies satisfied: {deps}\n"
    else:
        enhanced_spec += f"- [ ] No external dependencies required\n"

    enhanced_spec += f"""
### Blocks (What This Task Unblocks)
- [ ] {task_info.get('blocks', 'No downstream tasks specified')}

### External Dependencies
- [ ] Python 3.8+
- [ ] Git with worktree support
- [ ] Access to repository with all feature branches

### Assumptions & Constraints
- [ ] Assumption: All feature branches are accessible via GitPython or CLI
- [ ] Constraint: Analysis must complete before alignment operations begin

---

## Sub-subtasks Breakdown
"""

    # Add enhanced subtasks based on the task type
    if 'analyze' in task_info.get('title', '').lower():
        enhanced_spec += f"""
### {task_info.get('id', 'X')}.1: Research and Planning
**Effort:** 1-2 hours
**Depends on:** None
**Priority:** high
**Status:** pending

**Objective:** Research branch analysis requirements and plan implementation approach

**Steps:**
1. Review branch analysis requirements
2. Plan implementation approach
3. Identify potential challenges in branch analysis

**Deliverables:**
- [ ] Branch analysis implementation plan

**Acceptance Criteria:**
- [ ] Plan completed with analysis methodology

**Resources Needed:**
- Branch analysis requirements document

### {task_info.get('id', 'X')}.2: Implementation
**Effort:** 2-4 hours
**Depends on:** {task_info.get('id', 'X')}.1
**Priority:** high
**Status:** pending

**Objective:** Implement core branch analysis functionality

**Steps:**
1. Implement core branch analysis functionality
2. Write unit tests for analysis functions
3. Handle error cases in branch analysis

**Deliverables:**
- [ ] Implemented branch analysis functionality
- [ ] Unit tests for analysis components

**Acceptance Criteria:**
- [ ] Branch analysis functionality works as expected
- [ ] Tests pass for all analysis functions

**Resources Needed:**
- Development environment with Git access

"""
    elif 'cluster' in task_info.get('title', '').lower():
        enhanced_spec += f"""
### {task_info.get('id', 'X')}.1: Research and Planning
**Effort:** 1-2 hours
**Depends on:** None
**Priority:** high
**Status:** pending

**Objective:** Research clustering requirements and plan implementation approach

**Steps:**
1. Review clustering algorithm requirements
2. Plan clustering implementation approach
3. Identify potential challenges in branch clustering

**Deliverables:**
- [ ] Clustering implementation plan

**Acceptance Criteria:**
- [ ] Plan completed with clustering methodology

**Resources Needed:**
- Clustering requirements document

### {task_info.get('id', 'X')}.2: Implementation
**Effort:** 2-4 hours
**Depends on:** {task_info.get('id', 'X')}.1
**Priority:** high
**Status:** pending

**Objective:** Implement core branch clustering functionality

**Steps:**
1. Implement core clustering algorithm
2. Write unit tests for clustering functions
3. Handle edge cases in clustering

**Deliverables:**
- [ ] Implemented branch clustering functionality
- [ ] Unit tests for clustering components

**Acceptance Criteria:**
- [ ] Branch clustering functionality works as expected
- [ ] Tests pass for all clustering functions

**Resources Needed:**
- Development environment with branch analysis data

"""
    else:
        enhanced_spec += f"""
### {task_info.get('id', 'X')}.1: Research and Planning
**Effort:** 1-2 hours
**Depends on:** None
**Priority:** high
**Status:** pending

**Objective:** Research requirements and plan implementation approach

**Steps:**
1. Review requirements
2. Plan implementation approach
3. Identify potential challenges

**Deliverables:**
- [ ] Implementation plan

**Acceptance Criteria:**
- [ ] Plan completed

**Resources Needed:**
- Requirements document

### {task_info.get('id', 'X')}.2: Implementation
**Effort:** 2-4 hours
**Depends on:** {task_info.get('id', 'X')}.1
**Priority:** high
**Status:** pending

**Objective:** Implement the core functionality

**Steps:**
1. Implement core functionality
2. Write unit tests
3. Handle error cases

**Deliverables:**
- [ ] Implemented functionality
- [ ] Unit tests

**Acceptance Criteria:**
- [ ] Functionality works as expected
- [ ] Tests pass

**Resources Needed:**
- Development environment

"""

    enhanced_spec += f"""
---

## Specification Details

### Technical Interface
```
[Define technical interfaces, function signatures, API endpoints, etc. specific to branch analysis]
```

### Data Models
[Define data models for branch analysis results, clustering outputs, or identification data]

### Business Logic
[Describe core algorithms, decision points, and business rules for branch analysis]

### Error Handling
- [Error condition specific to branch analysis]: [How it should be handled]
- [Error condition specific to git operations]: [How it should be handled]

### Performance Requirements
- [Branch analysis performance metric]: [Specific target]
- [Clustering algorithm efficiency]: [Specific target]

### Security Requirements
- [Git operation security]: [Specific security measure]
- [Path validation for branch names]: [Specific security measure]

---

## Implementation Guide

### Approach
[Recommended approach for branch analysis implementation with rationale]

### Code Structure
[Recommended file structure and organization for branch analysis components]

### Key Implementation Steps
1. [Step 1 with detailed instructions for branch analysis]
   ```
   [Code example for branch analysis]
   ```

2. [Step 2 with detailed instructions for branch analysis]
   ```
   [Code example for branch analysis]
   ```

### Integration Points
[How branch analysis integrates with alignment pipeline]

### Configuration Requirements
[What configuration changes are needed for branch analysis]

### Migration Steps (if applicable)
[Steps to migrate from previous branch analysis approaches]

---

## Configuration Parameters

### Required Parameters
| Parameter | Type | Default | Validation | Description |
|-----------|------|---------|------------|-------------|
| [param_name] | [type] | [default] | [validation_rule] | [what it controls for branch analysis] |

### Optional Parameters
| Parameter | Type | Default | Validation | Description |
|-----------|------|---------|------------|-------------|
| [param_name] | [type] | [default] | [validation_rule] | [what it controls for branch analysis] |

### Environmental Variables
| Variable | Required | Description |
|----------|----------|-------------|
| [var_name] | [yes/no] | [what it controls for branch analysis] |

---

## Performance Targets

### Response Time Requirements
- [Branch analysis scenario]: [Time requirement]

### Throughput Requirements
- [Branch clustering scenario]: [Throughput requirement]

### Resource Utilization
- Memory: [Limit for analysis operations]
- CPU: [Limit for analysis operations]
- Disk: [Limit for temporary analysis files]

### Scalability Targets
- Concurrent branches analyzed: [Number]
- Repository size: [Size/quantity that can be analyzed]
- Growth rate: [Expected increase over time period]

### Baseline Measurements
[Current branch analysis performance metrics for comparison]

---

## Testing Strategy

### Unit Tests
- [Branch analysis component]: [Test requirements and coverage target]

### Integration Tests
- [Branch analysis integration point]: [Test requirements]

### End-to-End Tests
- [Branch analysis workflow]: [Test requirements]

### Performance Tests
- [Branch analysis scenario]: [Performance target]

### Security Tests
- [Branch analysis security aspect]: [Test requirement]

### Edge Case Tests
- [Branch analysis edge case #1]: [How to test]
- [Branch analysis edge case #2]: [How to test]

### Test Data Requirements
[Specific branch analysis test data sets needed for comprehensive testing]

---

## Common Gotchas & Solutions

### Known Pitfalls
1. **[Branch analysis pitfall #1]**
   - **Symptom:** [What indicates this problem in branch analysis]
   - **Cause:** [Why this happens in branch analysis]
   - **Solution:** [How to avoid or fix branch analysis issue]

2. **[Branch analysis pitfall #2]**
   - **Symptom:** [What indicates this problem in branch analysis]
   - **Cause:** [Why this happens in branch analysis]
   - **Solution:** [How to avoid or fix branch analysis issue]

### Performance Gotchas
- [Branch analysis performance pitfall]: [How to avoid]

### Security Gotchas
- [Branch analysis security pitfall]: [How to avoid]

### Integration Gotchas
- [Branch analysis integration pitfall]: [How to avoid]

---

## Integration Checkpoint

### Pre-Integration Validation
- [ ] [Branch analysis validation check #1]
- [ ] [Branch analysis validation check #2]

### Integration Steps
1. [Branch analysis step 1 with specific instructions]
2. [Branch analysis step 2 with specific instructions]

### Post-Integration Validation
- [ ] [Branch analysis validation check #1]
- [ ] [Branch analysis validation check #2]

### Rollback Procedure
[Steps to revert branch analysis integration if issues arise]

---

## Done Definition

### Observable Proof of Completion
- [ ] [Branch analysis specific, observable outcome #1]
- [ ] [Branch analysis specific, observable outcome #2]
- [ ] [Branch analysis specific, observable outcome #3]

### Quality Gates Passed
- [ ] [Branch analysis quality gate #1]
- [ ] [Branch analysis quality gate #2]

### Stakeholder Acceptance
- [ ] [Branch analysis stakeholder approval #1]
- [ ] [Branch analysis stakeholder approval #2]

### Documentation Complete
- [ ] [Branch analysis document #1] updated
- [ ] [Branch analysis document #2] updated

---

## Next Steps

### Immediate Follow-ups
- [ ] [Branch analysis next task #1] - Owner: [Person/Team], Due: [Date]
- [ ] [Branch analysis next task #2] - Owner: [Person/Team], Due: [Date]

### Handoff Information
- **Code Ownership:** [Which team/module owns branch analysis code]
- **Maintenance Contact:** [Who to contact for branch analysis issues]
- **Monitoring:** [What branch analysis metrics to watch]

### Future Considerations
- [Branch analysis future enhancement #1]
- [Branch analysis future enhancement #2]

"""

    return enhanced_spec


def extract_task_info(task_file_path: str) -> Dict[str, Any]:
    """
    Extract task information from the task file.
    """
    with open(task_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    task_info = {
        'id': '',
        'title': '',
        'status': '',
        'priority': '',
        'effort': '',
        'complexity': '',
        'dependencies': '',
        'blocks': '',
        'owner': '',
        'created': '',
        'purpose': '',
        'scope': '',
        'focus': ''
    }

    # Extract ID from filename
    filename = Path(task_file_path).stem
    id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
    if id_match:
        task_info['id'] = id_match.group(1).replace('_', '.').replace('-', '.')

    # Extract title
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['title'] = title_match.group(1).strip()

    # Extract other metadata
    metadata_patterns = {
        'status': r'\*\*Status:?\*\*\s*(.+?)(?:\n|$)',
        'priority': r'\*\*Priority:?\*\*\s*(.+?)(?:\n|$)',
        'effort': r'\*\*Effort:?\*\*\s*(.+?)(?:\n|$)',
        'complexity': r'\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)',
        'dependencies': r'\*\*Dependencies:?\*\*\s*(.+?)(?:\n|$)',
        'blocks': r'\*\*Blocks:?\*\*\s*(.+?)(?:\n|$)',
        'owner': r'\*\*Owner:?\*\*\s*(.+?)(?:\n|$)',
        'created': r'\*\*Created:?\*\*\s*(.+?)(?:\n|$)',
    }

    for field, pattern in metadata_patterns.items():
        match = re.search(pattern, content)
        if match:
            task_info[field] = match.group(1).strip()

    # Extract purpose/description
    purpose_match = re.search(r'## Overview/Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if purpose_match:
        task_info['purpose'] = purpose_match.group(1).strip()
    else:
        desc_match = re.search(r'\*\*Description:?\*\*\s*(.+?)(?:\n|$)', content)
        if desc_match:
            task_info['purpose'] = desc_match.group(1).strip()

    # Extract scope and focus if available
    scope_match = re.search(r'\*\*Scope:?\*\*\s*(.+?)(?:\n|$)', content)
    if scope_match:
        task_info['scope'] = scope_match.group(1).strip()

    focus_match = re.search(r'\*\*Focus:?\*\*\s*(.+?)(?:\n|$)', content)
    if focus_match:
        task_info['focus'] = focus_match.group(1).strip()

    return task_info


def main():
    parser = argparse.ArgumentParser(description="Improve branch analysis task specifications to maximize PRD accuracy")
    parser.add_argument("--tasks-dir", "-d", default="./tasks", help="Directory containing task markdown files")
    parser.add_argument("--pattern", default="task*.md", help="File pattern to match (default: task*.md)")
    parser.add_argument("--apply", action="store_true", help="Apply changes to task files")
    parser.add_argument("--backup", action="store_true", help="Create backups before modifying")

    args = parser.parse_args()

    tasks_path = Path(args.tasks_dir)
    task_files = list(tasks_path.glob(args.pattern))

    if not task_files:
        print(f"No task files found in {tasks_path} with pattern {args.pattern}")
        return 1

    print(f"Found {len(task_files)} task files to process")
    print(f"Files to be processed: {[f.name for f in task_files[:5]]}{'...' if len(task_files) > 5 else ''}")

    if not args.apply:
        print("Use --apply to execute the improvements")
        return 0

    # Process each task file
    processed_count = 0
    for task_file in task_files:
        print(f"Improving task specification: {task_file.name}")
        
        # Create backup if requested
        if args.backup:
            backup_path = task_file.with_suffix(f'.md.backup_pre_branch_analysis_enhancement')
            with open(task_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"  - Created backup: {backup_path.name}")

        # Improve the task specification
        enhanced_content = improve_branch_analysis_task_spec(str(task_file))

        # Write the enhanced content
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)

        print(f"  ✓ Enhanced: {task_file.name}")
        processed_count += 1

    print(f"\nSuccessfully enhanced {processed_count} task specifications")
    print("Enhanced specifications now have improved branch analysis focus for maximum PRD accuracy")
    print("All specifications follow the enhanced 14-section format with detailed implementation guidance")

    return 0


if __name__ == "__main__":
    exit(main())