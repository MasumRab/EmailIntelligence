#!/usr/bin/env python3
"""
Task Specification Enhancer for Maximum PRD Accuracy
Restructures task files according to the 14-section standard to maximize PRD generation accuracy.
"""

import argparse
import re
from pathlib import Path
from typing import Dict, Any


def restructure_task_to_14_section_format(content: str) -> str:
    """
    Restructure a task file to follow the 14-section standard format for maximum PRD accuracy.
    """
    # Parse the existing task content to extract information
    parsed_task = parse_existing_task(content)
    
    # Rebuild the task following the 14-section format
    restructured_content = f"""# Task {parsed_task['id']}: {parsed_task['title']}

**Status:** {parsed_task['status']}
**Priority:** {parsed_task['priority']}
**Effort:** {parsed_task['effort']}
**Complexity:** {parsed_task['complexity']}
**Dependencies:** {parsed_task['dependencies']}

---

## Overview/Purpose
{parsed_task['purpose']}

"""

    # Add success criteria in checklist format
    if parsed_task['success_criteria']:
        restructured_content += "## Success Criteria\n\n"
        for criterion in parsed_task['success_criteria']:
            restructured_content += f"- [ ] {criterion}\n"
        restructured_content += "\n"
    else:
        restructured_content += "## Success Criteria\n\n- [ ] [Success criteria to be defined]\n\n"

    # Add prerequisites and dependencies
    restructured_content += f"""## Prerequisites & Dependencies

### Required Before Starting
{parsed_task['prerequisites']}

### Blocks (What This Task Unblocks)
{parsed_task['blocks']}

### External Dependencies
{parsed_task['external_dependencies']}

"""

    # Add subtasks breakdown
    restructured_content += "## Sub-subtasks Breakdown\n\n"
    for subtask in parsed_task['subtasks']:
        restructured_content += f"### {subtask['id']}: {subtask['title']}\n"
        restructured_content += f"- **Status**: {subtask['status']}\n"
        restructured_content += f"- **Dependencies**: {subtask['dependencies']}\n"
        restructured_content += f"- **Details**: {subtask['details']}\n\n"

    # Add specification details
    restructured_content += f"""## Specification Details

### Task Interface
- **ID**: {parsed_task['id']}
- **Title**: {parsed_task['title']}
- **Status**: {parsed_task['status']}
- **Priority**: {parsed_task['priority']}
- **Effort**: {parsed_task['effort']}
- **Complexity**: {parsed_task['complexity']}

### Requirements
{parsed_task['requirements']}

"""

    # Add implementation guide
    restructured_content += f"""## Implementation Guide

{parsed_task['implementation_guide']}

"""

    # Add configuration parameters
    restructured_content += f"""## Configuration Parameters

- **Owner**: {parsed_task['owner']}
- **Initiative**: {parsed_task['initiative']}
- **Scope**: {parsed_task['scope']}
- **Focus**: {parsed_task['focus']}

"""

    # Add performance targets
    restructured_content += f"""## Performance Targets

- **Effort Range**: {parsed_task['effort']}
- **Complexity Level**: {parsed_task['complexity']}

"""

    # Add testing strategy
    restructured_content += f"""## Testing Strategy

{parsed_task['test_strategy']}

"""

    # Add common gotchas
    restructured_content += f"""## Common Gotchas & Solutions

{parsed_task['gotchas']}

"""

    # Add integration checkpoint
    restructured_content += f"""## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

"""

    # Add done definition
    restructured_content += f"""## Done Definition

### Completion Criteria
{parsed_task['done_definition']}

"""

    # Add next steps
    restructured_content += f"""## Next Steps

{parsed_task['next_steps']}

"""

    # Add extended metadata if it exists
    if parsed_task['extended_metadata']:
        restructured_content += f"\n<!-- EXTENDED_METADATA\n"
        for key, value in parsed_task['extended_metadata'].items():
            restructured_content += f"{key}: {value}\n"
        restructured_content += f"END_EXTENDED_METADATA -->\n"

    return restructured_content


def parse_existing_task(content: str) -> Dict[str, Any]:
    """
    Parse an existing task file to extract all relevant information.
    """
    task_data = {
        'id': 'UNKNOWN',
        'title': 'Untitled Task',
        'status': 'pending',
        'priority': 'medium',
        'effort': 'TBD',
        'complexity': 'TBD',
        'dependencies': 'None',
        'purpose': 'Task purpose to be defined',
        'success_criteria': [],
        'prerequisites': '- [ ] No external prerequisites',
        'blocks': '- [ ] No specific blocks defined',
        'external_dependencies': '- [ ] No external dependencies',
        'subtasks': [],
        'requirements': 'Requirements to be specified',
        'implementation_guide': 'Implementation guide to be defined',
        'owner': 'TBD',
        'initiative': 'TBD',
        'scope': 'TBD',
        'focus': 'TBD',
        'test_strategy': 'Test strategy to be defined',
        'gotchas': '- [ ] No common gotchas identified',
        'done_definition': '- [ ] All success criteria met\n- [ ] Code reviewed and approved\n- [ ] Tests passing\n- [ ] Documentation updated',
        'next_steps': '- [ ] Next steps to be defined',
        'extended_metadata': {}
    }

    # Extract ID from header
    id_match = re.search(r'Task ID:?\s*(\d+(?:\.\d+)?)', content)
    if id_match:
        task_data['id'] = id_match.group(1)

    # Extract title
    title_match = re.search(r'\*\*Title:\*\*\s*(.+)', content)
    if title_match:
        task_data['title'] = title_match.group(1).strip()

    # Extract status
    status_match = re.search(r'\*\*Status:\*\*\s*(.+)', content)
    if status_match:
        task_data['status'] = status_match.group(1).strip()

    # Extract priority
    priority_match = re.search(r'\*\*Priority:\*\*\s*(.+)', content)
    if priority_match:
        task_data['priority'] = priority_match.group(1).strip()

    # Extract effort
    effort_match = re.search(r'\*\*Effort:\*\*\s*(.+)|effort:\s*([^\n]+)', content, re.IGNORECASE)
    if effort_match:
        task_data['effort'] = (effort_match.group(1) or effort_match.group(2)).strip()

    # Extract complexity
    complexity_match = re.search(r'\*\*Complexity:\*\*\s*(.+)|complexity:\s*([^\n]+)', content, re.IGNORECASE)
    if complexity_match:
        task_data['complexity'] = (complexity_match.group(1) or complexity_match.group(2)).strip()

    # Extract dependencies
    deps_match = re.search(r'\*\*Dependencies:\*\*\s*(.+)', content)
    if deps_match:
        task_data['dependencies'] = deps_match.group(1).strip()

    # Extract purpose/description
    purpose_patterns = [
        r'\*\*Description:\*\*\s*([\s\S]*?)(?=\n\*\*|\n##|\n---|\Z)',
        r'\*\*Purpose:\*\*\s*([\s\S]*?)(?=\n\*\*|\n##|\n---|\Z)',
        r'## Overview/Purpose\s*\n+([\s\S]*?)(?=\n## |\n---|\Z)',
        r'## Purpose\s*\n+([\s\S]*?)(?=\n## |\n---|\Z)'
    ]
    
    for pattern in purpose_patterns:
        match = re.search(pattern, content)
        if match:
            task_data['purpose'] = match.group(1).strip()
            break

    # Extract success criteria
    criteria_patterns = [
        r'## Success Criteria\s*\n+([\s\S]*?)(?=\n## |\n---|\Z)',
        r'- \[.\] (.+)'  # Direct checklist items
    ]
    
    for pattern in criteria_patterns:
        matches = re.findall(pattern, content)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]  # Get first capturing group if it's a tuple
                task_data['success_criteria'].append(match.strip())

    # Extract subtasks
    subtask_pattern = r'(?:### |\n## )(\d+\.\d+)\.\s*(.+?)\n(?:\*\*Status:\*\*\s*(\w+))?.*?(?:\*\*Dependencies:\*\*\s*([^\n]+))?.*?(?:\*\*Details:\*\*|(?=\n### |\n## |\Z))([\s\S]*?)(?=\n### |\n## |\Z)'
    subtask_matches = re.finditer(subtask_pattern, content)
    
    for match in subtask_matches:
        subtask = {
            'id': match.group(1),
            'title': match.group(2).strip(),
            'status': match.group(3) if match.group(3) else 'pending',
            'dependencies': match.group(4) if match.group(4) else 'None',
            'details': match.group(5).strip() if match.group(5) else 'Details to be defined'
        }
        task_data['subtasks'].append(subtask)

    # Extract extended metadata
    ext_meta_match = re.search(r'<!-- EXTENDED_METADATA\s*\n([\s\S]*?)\nEND_EXTENDED_METADATA -->', content)
    if ext_meta_match:
        ext_meta_content = ext_meta_match.group(1)
        for line in ext_meta_content.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                task_data['extended_metadata'][key.strip()] = value.strip()

    # Extract other fields if available
    if not task_data['extended_metadata']:
        # Look for common extended metadata patterns in comments
        blocks_match = re.search(r'blocks:\s*([^\n]+)', content, re.IGNORECASE)
        if blocks_match:
            task_data['blocks'] = f"- [ ] {blocks_match.group(1).strip()}"

        initiative_match = re.search(r'initiative:\s*([^\n]+)', content, re.IGNORECASE)
        if initiative_match:
            task_data['initiative'] = initiative_match.group(1).strip()

        scope_match = re.search(r'scope:\s*([^\n]+)', content, re.IGNORECASE)
        if scope_match:
            task_data['scope'] = scope_match.group(1).strip()

        focus_match = re.search(r'focus:\s*([^\n]+)', content, re.IGNORECASE)
        if focus_match:
            task_data['focus'] = focus_match.group(1).strip()

        owner_match = re.search(r'owner:\s*([^\n]+)', content, re.IGNORECASE)
        if owner_match:
            task_data['owner'] = owner_match.group(1).strip()

    return task_data


def main():
    parser = argparse.ArgumentParser(description="Restructure task files to 14-section format for maximum PRD accuracy")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing task markdown files")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory for restructured task files")
    parser.add_argument("--pattern", default="task*.md", help="File pattern to match (default: task*.md)")

    args = parser.parse_args()

    # Find all task markdown files
    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    task_files = list(input_path.glob(args.pattern))

    if not task_files:
        print(f"No task files found in {input_path} with pattern {args.pattern}")
        return 1

    print(f"Found {len(task_files)} task files to restructure")

    # Process each task file
    for task_file in task_files:
        print(f"Restructuring {task_file.name}...")

        # Read the task file
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Restructure the task to 14-section format
        restructured_content = restructure_task_to_14_section_format(content)

        # Write the restructured content to output file
        output_file = output_path / task_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(restructured_content)

        print(f"  ✓ Restructured {task_file.name} -> {output_file.name}")

    print(f"\nSuccessfully restructured {len(task_files)} task files to 14-section format")
    print(f"Restructured files saved to {output_path}")
    print("The 14-section format maximizes PRD generation accuracy by providing:")
    print("- Consistent structure for reliable parsing")
    print("- Complete information in standardized locations")
    print("- Clear success criteria in checklist format")
    print("- Proper dependency and prerequisite information")
    print("- Well-defined implementation guide and testing strategy")

    return 0


if __name__ == "__main__":
    exit(main())