#!/usr/bin/env python3
"""
Task Specification Enhancer
Enhances existing task files to maximize PRD generation accuracy based on the enhanced template
"""

import argparse
import re
import json
from pathlib import Path
from typing import Dict, Any, List
import sys


def enhance_task_specification(task_path: str) -> str:
    """
    Enhance a task specification to maximize PRD generation accuracy.
    """
    with open(task_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract existing information
    task_info = extract_basic_task_info(content, task_path)

    # Build enhanced task specification using the enhanced template
    enhanced_content = f"""# Task {task_info['id']}: {task_info['title']}

**Status:** {task_info.get('status', 'pending')}
**Priority:** {task_info.get('priority', 'medium')}
**Effort:** {task_info.get('effort', 'TBD')}
**Complexity:** {task_info.get('complexity', 'TBD')}/10
**Dependencies:** {task_info.get('dependencies', 'None')}
**Blocks:** {task_info.get('blocks', 'None')}
**Owner:** {task_info.get('owner', 'TBD')}
**Created:** {task_info.get('created', '2026-01-16')}
**Updated:** 2026-01-16
**Tags:** {task_info.get('tags', 'enhanced')}

---

## Overview/Purpose

{task_info.get('purpose', 'Task to implement the specified functionality')}

**Scope:** {task_info.get('scope', 'Implementation of specified functionality')}
**Focus:** {task_info.get('focus', 'Core functionality implementation')}
**Value Proposition:** {task_info.get('value_prop', 'Delivers the required functionality')}
**Success Indicator:** {task_info.get('success_indicator', 'Task completed successfully')}

---

## Success Criteria

Task {task_info['id']} is complete when:

### Functional Requirements
{generate_functional_success_criteria(task_info)}

### Non-Functional Requirements
{generate_non_functional_success_criteria(task_info)}

### Quality Gates
{generate_quality_gates(task_info)}

---

## Prerequisites & Dependencies

### Required Before Starting
{generate_prerequisites(task_info)}

### Blocks (What This Task Unblocks)
{generate_blocks_section(task_info)}

### External Dependencies
{generate_external_dependencies(task_info)}

### Assumptions & Constraints
{generate_assumptions_constraints(task_info)}

---

## Sub-subtasks Breakdown

{generate_subtasks_breakdown(task_info)}

---

## Specification Details

{generate_specification_details(task_info)}

---

## Implementation Guide

{generate_implementation_guide(task_info)}

---

## Configuration Parameters

{generate_configuration_parameters(task_info)}

---

## Performance Targets

{generate_performance_targets(task_info)}

---

## Testing Strategy

{generate_testing_strategy(task_info)}

---

## Common Gotchas & Solutions

{generate_common_gotchas(task_info)}

---

## Integration Checkpoint

{generate_integration_checkpoint(task_info)}

---

## Done Definition

{generate_done_definition(task_info)}

---

## Next Steps

{generate_next_steps(task_info)}

"""

    return enhanced_content


def extract_basic_task_info(content: str, file_path: str) -> Dict[str, Any]:
    """
    Extract basic information from existing task content.
    """
    task_info = {
        'id': 'UNKNOWN',
        'title': 'Untitled Task',
        'status': 'pending',
        'priority': 'medium',
        'effort': 'TBD',
        'complexity': 'TBD',
        'dependencies': 'None',
        'blocks': 'None',
        'owner': 'TBD',
        'created': '2026-01-16',
        'tags': 'enhanced',
        'purpose': 'Task to implement the specified functionality',
        'scope': 'Implementation of specified functionality',
        'focus': 'Core functionality implementation',
        'value_prop': 'Delivers the required functionality',
        'success_indicator': 'Task completed successfully',
        'existing_content': content
    }

    # Extract ID from filename or content
    filename = Path(file_path).stem
    id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
    if id_match:
        task_info['id'] = id_match.group(1).replace('_', '.').replace('-', '.')

    # Extract title from header
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['title'] = title_match.group(1).strip()

    # Extract metadata from bold sections
    metadata_patterns = {
        'status': r'\*\*Status:?\*\*\s*(.+?)(?:\n|$)',
        'priority': r'\*\*Priority:?\*\*\s*(.+?)(?:\n|$)',
        'effort': r'\*\*Effort:?\*\*\s*(.+?)(?:\n|$)',
        'complexity': r'\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)',
        'dependencies': r'\*\*Dependencies:?\*\*\s*(.+?)(?:\n|$)',
        'blocks': r'\*\*Blocks:?\*\*\s*(.+?)(?:\n|$)',
        'owner': r'\*\*Owner:?\*\*\s*(.+?)(?:\n|$)',
    }

    for field, pattern in metadata_patterns.items():
        match = re.search(pattern, content)
        if match:
            task_info[field] = match.group(1).strip()

    # Extract purpose/description
    purpose_match = re.search(r'## Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if purpose_match:
        task_info['purpose'] = purpose_match.group(1).strip()
    else:
        # Try to find description in other formats
        desc_match = re.search(r'\*\*Description:?\*\*\s*(.+?)(?:\n|$)', content)
        if desc_match:
            task_info['purpose'] = desc_match.group(1).strip()

    # Extract existing details
    details_match = re.search(r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if details_match:
        task_info['existing_details'] = details_match.group(1).strip()

    # Extract existing success criteria
    criteria_match = re.search(r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if criteria_match:
        task_info['existing_criteria'] = criteria_match.group(1).strip()

    return task_info


def generate_functional_success_criteria(task_info: Dict[str, Any]) -> str:
    """
    Generate functional success criteria based on task information.
    """
    if task_info.get('existing_criteria'):
        # Convert existing criteria to checklist format
        criteria_items = re.findall(r'- \[.\]\s*(.+)', task_info['existing_criteria'])
        if criteria_items:
            result = ""
            for i, item in enumerate(criteria_items, 1):
                result += f"- [ ] {item.strip()} - Verification: [Method to verify completion]\n"
            return result

    # Generate default functional criteria based on title
    title = task_info.get('title', 'the task').lower()
    result = f"- [ ] {task_info.get('title', 'Implement the required functionality')} - Verification: [Method to verify completion]\n"
    
    if 'implement' in title or 'create' in title or 'develop' in title:
        result += f"- [ ] Core functionality implemented - Verification: [Method to verify completion]\n"
        result += f"- [ ] All requirements satisfied - Verification: [Method to verify completion]\n"
    elif 'analyze' in title:
        result += f"- [ ] Analysis completed - Verification: [Method to verify completion]\n"
        result += f"- [ ] Findings documented - Verification: [Method to verify completion]\n"
    elif 'test' in title or 'validate' in title:
        result += f"- [ ] Testing completed - Verification: [Method to verify completion]\n"
        result += f"- [ ] Results validated - Verification: [Method to verify completion]\n"
    
    return result


def generate_non_functional_success_criteria(task_info: Dict[str, Any]) -> str:
    """
    Generate non-functional success criteria.
    """
    result = f"- [ ] Performance requirements met - Verification: [Method to verify completion]\n"
    result += f"- [ ] Security requirements satisfied - Verification: [Method to verify completion]\n"
    result += f"- [ ] Compatibility requirements fulfilled - Verification: [Method to verify completion]\n"
    return result


def generate_quality_gates(task_info: Dict[str, Any]) -> str:
    """
    Generate quality gates.
    """
    result = f"- [ ] Code review passed - Verification: [Method to verify completion]\n"
    result += f"- [ ] Tests passing - Verification: [Method to verify completion]\n"
    result += f"- [ ] Documentation complete - Verification: [Method to verify completion]\n"
    return result


def generate_prerequisites(task_info: Dict[str, Any]) -> str:
    """
    Generate prerequisites section.
    """
    deps = task_info.get('dependencies', 'None')
    if deps.lower() in ['none', 'null', '']:
        return "- [ ] No external prerequisites required\n"
    else:
        return f"- [ ] Dependencies satisfied: {deps}\n"


def generate_blocks_section(task_info: Dict[str, Any]) -> str:
    """
    Generate blocks section.
    """
    blocks = task_info.get('blocks', 'None')
    if blocks.lower() in ['none', 'null', '']:
        return "- [ ] No downstream tasks blocked by this task\n"
    else:
        return f"- [ ] Unblocks: {blocks}\n"


def generate_external_dependencies(task_info: Dict[str, Any]) -> str:
    """
    Generate external dependencies section.
    """
    return f"- [ ] Python 3.8+\n- [ ] Git with worktree support\n- [ ] Access to repository\n"


def generate_assumptions_constraints(task_info: Dict[str, Any]) -> str:
    """
    Generate assumptions and constraints section.
    """
    result = f"- [ ] Assumption: [State key assumptions for this task]\n"
    result += f"- [ ] Constraint: [State key constraints that apply to this task]\n"
    return result


def generate_subtasks_breakdown(task_info: Dict[str, Any]) -> str:
    """
    Generate subtasks breakdown.
    """
    # If we have existing details, try to extract subtasks from them
    if task_info.get('existing_details'):
        # Look for numbered lists or step-by-step instructions
        steps = re.findall(r'\d+\.\s*(.+)', task_info['existing_details'])
        if steps and len(steps) >= 2:
            result = ""
            for i, step in enumerate(steps[:5], 1):  # Take first 5 steps as subtasks
                result += f"### {task_info['id']}.{i}: {step[:50]}...\n"
                result += f"**Effort:** TBD\n"
                result += f"**Depends on:** None\n"
                result += f"**Priority:** medium\n"
                result += f"**Status:** pending\n\n"
                result += f"**Objective:** [What this subtask accomplishes]\n\n"
                result += f"**Steps:**\n1. [Step 1]\n2. [Step 2]\n\n"
                result += f"**Deliverables:**\n- [ ] [Deliverable 1]\n\n"
                result += f"**Acceptance Criteria:**\n- [ ] [Criterion 1]\n\n"
                result += f"**Resources Needed:**\n- [Resource 1]\n\n"
            return result

    # Default subtasks if no existing details
    result = f"### {task_info['id']}.1: Research and Planning\n"
    result += f"**Effort:** 1-2 hours\n"
    result += f"**Depends on:** None\n"
    result += f"**Priority:** high\n"
    result += f"**Status:** pending\n\n"
    result += f"**Objective:** Research requirements and plan implementation approach\n\n"
    result += f"**Steps:**\n1. Review requirements\n2. Plan implementation approach\n3. Identify potential challenges\n\n"
    result += f"**Deliverables:**\n- [ ] Implementation plan\n\n"
    result += f"**Acceptance Criteria:**\n- [ ] Plan completed\n\n"
    result += f"**Resources Needed:**\n- Requirements document\n\n"

    result += f"### {task_info['id']}.2: Implementation\n"
    result += f"**Effort:** 2-4 hours\n"
    result += f"**Depends on:** {task_info['id']}.1\n"
    result += f"**Priority:** high\n"
    result += f"**Status:** pending\n\n"
    result += f"**Objective:** Implement the core functionality\n\n"
    result += f"**Steps:**\n1. Implement core functionality\n2. Write unit tests\n3. Handle error cases\n\n"
    result += f"**Deliverables:**\n- [ ] Implemented functionality\n- [ ] Unit tests\n\n"
    result += f"**Acceptance Criteria:**\n- [ ] Functionality works as expected\n- [ ] Tests pass\n\n"
    result += f"**Resources Needed:**\n- Development environment\n\n"

    return result


def generate_specification_details(task_info: Dict[str, Any]) -> str:
    """
    Generate specification details.
    """
    result = f"### Technical Interface\n"
    result += f"```\n[Define technical interfaces, function signatures, API endpoints, etc.]\n```\n\n"
    result += f"### Data Models\n"
    result += f"[Define data models, schemas, and structures]\n\n"
    result += f"### Business Logic\n"
    result += f"[Describe core algorithms, decision points, and business rules]\n\n"
    result += f"### Error Handling\n"
    result += f"- [Error condition 1]: [How it should be handled]\n- [Error condition 2]: [How it should be handled]\n\n"
    result += f"### Performance Requirements\n"
    result += f"- [Requirement 1]: [Specific metric]\n- [Requirement 2]: [Specific metric]\n\n"
    result += f"### Security Requirements\n"
    result += f"- [Requirement 1]: [Specific security measure]\n- [Requirement 2]: [Specific security measure]\n"
    return result


def generate_implementation_guide(task_info: Dict[str, Any]) -> str:
    """
    Generate implementation guide.
    """
    result = f"### Approach\n[Recommended approach for implementation with rationale]\n\n"
    result += f"### Code Structure\n[Recommended file structure and organization]\n\n"
    result += f"### Key Implementation Steps\n"
    result += f"1. [Step 1 with detailed instructions]\n   ```\n   [Code example]\n   ```\n\n"
    result += f"2. [Step 2 with detailed instructions]\n   ```\n   [Code example]\n   ```\n\n"
    result += f"### Integration Points\n[How this integrates with existing components]\n\n"
    result += f"### Configuration Requirements\n[What configuration changes are needed]\n\n"
    result += f"### Migration Steps (if applicable)\n[Steps to migrate from previous implementation]\n"
    return result


def generate_configuration_parameters(task_info: Dict[str, Any]) -> str:
    """
    Generate configuration parameters.
    """
    result = f"### Required Parameters\n| Parameter | Type | Default | Validation | Description |\n"
    result += f"|-----------|------|---------|------------|-------------|\n"
    result += f"| [param_name] | [type] | [default] | [validation_rule] | [what it controls] |\n\n"
    result += f"### Optional Parameters\n| Parameter | Type | Default | Validation | Description |\n"
    result += f"|-----------|------|---------|------------|-------------|\n"
    result += f"| [param_name] | [type] | [default] | [validation_rule] | [what it controls] |\n\n"
    result += f"### Environmental Variables\n| Variable | Required | Description |\n"
    result += f"|----------|----------|-------------|\n"
    result += f"| [var_name] | [yes/no] | [what it controls] |\n"
    return result


def generate_performance_targets(task_info: Dict[str, Any]) -> str:
    """
    Generate performance targets.
    """
    result = f"### Response Time Requirements\n- [Scenario]: [Time requirement]\n\n"
    result += f"### Throughput Requirements\n- [Scenario]: [Throughput requirement]\n\n"
    result += f"### Resource Utilization\n- Memory: [Limit]\n- CPU: [Limit]\n- Disk: [Limit]\n\n"
    result += f"### Scalability Targets\n- Concurrent users: [Number]\n- Data volume: [Size/quantity]\n- Growth rate: [Expected increase over time period]\n\n"
    result += f"### Baseline Measurements\n[Current performance metrics for comparison]\n"
    return result


def generate_testing_strategy(task_info: Dict[str, Any]) -> str:
    """
    Generate testing strategy.
    """
    result = f"### Unit Tests\n- [Component]: [Test requirements and coverage target]\n\n"
    result += f"### Integration Tests\n- [Integration point]: [Test requirements]\n\n"
    result += f"### End-to-End Tests\n- [User workflow]: [Test requirements]\n\n"
    result += f"### Performance Tests\n- [Test scenario]: [Performance target]\n\n"
    result += f"### Security Tests\n- [Security aspect]: [Test requirement]\n\n"
    result += f"### Edge Case Tests\n- [Edge case #1]: [How to test]\n- [Edge case #2]: [How to test]\n\n"
    result += f"### Test Data Requirements\n[Specific test data sets needed for comprehensive testing]\n"
    return result


def generate_common_gotchas(task_info: Dict[str, Any]) -> str:
    """
    Generate common gotchas and solutions.
    """
    result = f"### Known Pitfalls\n"
    result += f"1. **[Pitfall #1]**\n   - **Symptom:** [What indicates this problem]\n   - **Cause:** [Why this happens]\n   - **Solution:** [How to avoid or fix]\n\n"
    result += f"2. **[Pitfall #2]**\n   - **Symptom:** [What indicates this problem]\n   - **Cause:** [Why this happens]\n   - **Solution:** [How to avoid or fix]\n\n"
    result += f"### Performance Gotchas\n- [Performance pitfall]: [How to avoid]\n\n"
    result += f"### Security Gotchas\n- [Security pitfall]: [How to avoid]\n\n"
    result += f"### Integration Gotchas\n- [Integration pitfall]: [How to avoid]\n"
    return result


def generate_integration_checkpoint(task_info: Dict[str, Any]) -> str:
    """
    Generate integration checkpoint.
    """
    result = f"### Pre-Integration Validation\n- [ ] [Validation check #1]\n- [ ] [Validation check #2]\n\n"
    result += f"### Integration Steps\n1. [Step 1 with specific instructions]\n2. [Step 2 with specific instructions]\n\n"
    result += f"### Post-Integration Validation\n- [ ] [Validation check #1]\n- [ ] [Validation check #2]\n\n"
    result += f"### Rollback Procedure\n[Steps to revert the integration if issues arise]\n"
    return result


def generate_done_definition(task_info: Dict[str, Any]) -> str:
    """
    Generate done definition.
    """
    result = f"### Observable Proof of Completion\n- [ ] [Specific, observable outcome #1]\n- [ ] [Specific, observable outcome #2]\n- [ ] [Specific, observable outcome #3]\n\n"
    result += f"### Quality Gates Passed\n- [ ] [Quality gate #1]\n- [ ] [Quality gate #2]\n\n"
    result += f"### Stakeholder Acceptance\n- [ ] [Stakeholder approval #1]\n- [ ] [Stakeholder approval #2]\n\n"
    result += f"### Documentation Complete\n- [ ] [Document #1] updated\n- [ ] [Document #2] updated\n"
    return result


def generate_next_steps(task_info: Dict[str, Any]) -> str:
    """
    Generate next steps.
    """
    result = f"### Immediate Follow-ups\n- [ ] [Next task #1] - Owner: [Person/Team], Due: [Date]\n- [ ] [Next task #2] - Owner: [Person/Team], Due: [Date]\n\n"
    result += f"### Handoff Information\n- **Code Ownership:** [Which team/module owns this code]\n- **Maintenance Contact:** [Who to contact for issues]\n- **Monitoring:** [What metrics to watch]\n\n"
    result += f"### Future Considerations\n- [Future enhancement #1]\n- [Future enhancement #2]\n"
    return result


def main():
    parser = argparse.ArgumentParser(description="Enhance task specifications to maximize PRD generation accuracy")
    parser.add_argument("--tasks-dir", "-d", default="./tasks", help="Directory containing task markdown files")
    parser.add_argument("--pattern", default="task*.md", help="File pattern to match (default: task*.md)")
    parser.add_argument("--backup", action="store_true", help="Create backups of original files")

    args = parser.parse_args()

    tasks_path = Path(args.tasks_dir)
    task_files = list(tasks_path.glob(args.pattern))

    if not task_files:
        print(f"No task files found in {tasks_path} with pattern {args.pattern}")
        return 1

    print(f"Enhancing {len(task_files)} task files to maximize PRD generation accuracy...")

    enhanced_count = 0
    for task_file in task_files:
        print(f"Enhancing: {task_file.name}")

        if args.backup:
            # Create backup
            backup_path = task_file.with_suffix(f'.md.backup_pre_enhancement')
            with open(task_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)

        # Enhance the task specification
        enhanced_content = enhance_task_specification(str(task_file))

        # Write the enhanced content
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)

        print(f"  ✓ Enhanced: {task_file.name}")
        enhanced_count += 1

    print(f"\nSuccessfully enhanced {enhanced_count} task files.")
    print("All task files now follow the enhanced template for maximum PRD generation accuracy.")
    print("The enhanced specifications include comprehensive sections for better information preservation.")

    return 0


if __name__ == "__main__":
    exit(main())