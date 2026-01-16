#!/usr/bin/env python3
"""
Reverse Engineer PRD from Task Markdown Files

This script takes task markdown files and generates a PRD that would produce 
similar tasks when processed by task-master. The generated PRD follows the 
RPG (Repository Planning Graph) method structure that task-master expects.

Usage:
    python reverse_engineer_prd.py --input-dir /path/to/task/files --output /path/to/generated_prd.md
"""

import argparse
import re
import os
from pathlib import Path
from typing import List, Dict, Any
import json


def extract_task_info_from_md(file_path: str) -> Dict[str, Any]:
    """
    Extract key information from a task markdown file.
    
    Args:
        file_path: Path to the task markdown file
        
    Returns:
        Dictionary containing extracted task information
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    task_info = {
        'id': '',
        'title': '',
        'status': '',
        'priority': '',
        'effort': '',
        'complexity': '',
        'dependencies': '',
        'purpose': '',
        'success_criteria': [],
        'subtasks': [],
        'details': ''
    }
    
    # Extract title from header
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['title'] = title_match.group(1).strip()
    
    # Extract ID from filename or content
    filename = Path(file_path).stem
    id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
    if id_match:
        task_info['id'] = id_match.group(1).replace('_', '.').replace('-', '.')
    
    # Extract metadata from bold sections
    status_match = re.search(r'\*\*Status:?\*\*\s*(.+?)(?:\n|$)', content)
    if status_match:
        task_info['status'] = status_match.group(1).strip()
        
    priority_match = re.search(r'\*\*Priority:?\*\*\s*(.+?)(?:\n|$)', content)
    if priority_match:
        task_info['priority'] = priority_match.group(1).strip()
        
    effort_match = re.search(r'\*\*Effort:?\*\*\s*(.+?)(?:\n|$)', content)
    if effort_match:
        task_info['effort'] = effort_match.group(1).strip()
        
    complexity_match = re.search(r'\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)', content)
    if complexity_match:
        task_info['complexity'] = complexity_match.group(1).strip()
        
    deps_match = re.search(r'\*\*Dependencies:?\*\*\s*(.+?)(?:\n|$)', content)
    if deps_match:
        task_info['dependencies'] = deps_match.group(1).strip()
    
    # Extract purpose
    purpose_match = re.search(r'## Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if purpose_match:
        task_info['purpose'] = purpose_match.group(1).strip()
    
    # Extract success criteria
    criteria_match = re.search(r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if criteria_match:
        criteria_text = criteria_match.group(1)
        # Find all checklist items
        criteria_items = re.findall(r'- \[.\] (.+)', criteria_text)
        task_info['success_criteria'] = criteria_items
    
    # Extract details
    details_match = re.search(r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if details_match:
        task_info['details'] = details_match.group(1).strip()
    
    # Extract subtasks if they exist in table format
    subtask_table_match = re.search(r'\|\s*ID\s*\|\s*Subtask\s*\|[\s\S]*?\n((?:\|\s*[^\n]*\s*\|.*\n)+)', content)
    if subtask_table_match:
        table_content = subtask_table_match.group(1)
        # Extract subtask rows
        rows = table_content.strip().split('\n')
        for row in rows:
            if '|' in row:
                parts = [part.strip() for part in row.split('|')]
                if len(parts) >= 4:  # ID | Subtask | Status | Effort
                    subtask = {
                        'id': parts[1] if len(parts) > 1 else '',
                        'title': parts[2] if len(parts) > 2 else '',
                        'status': parts[3] if len(parts) > 3 else ''
                    }
                    if subtask['id']:  # Only add if we have an ID
                        task_info['subtasks'].append(subtask)
    
    return task_info


def generate_capability_from_task(task_info: Dict[str, Any]) -> str:
    """
    Generate a capability section for the PRD based on task information.
    
    Args:
        task_info: Dictionary containing task information
        
    Returns:
        String representing the capability section
    """
    capability_template = f"""### Capability: {task_info['title']}
[Brief description of what this capability domain covers]

#### Feature: {task_info['title']}
- **Description**: {task_info['purpose'][:100] + '...' if len(task_info['purpose']) > 100 else task_info['purpose'] or 'Task to implement the specified functionality'}
- **Inputs**: [What it needs]
- **Outputs**: [What it produces]
- **Behavior**: [Key logic]

"""
    return capability_template


def generate_dependency_from_task(task_info: Dict[str, Any]) -> str:
    """
    Generate a dependency entry for the PRD based on task information.
    
    Args:
        task_info: Dictionary containing task information
        
    Returns:
        String representing the dependency entry
    """
    # Extract just the main task number (e.g., from "1.2" get "1")
    main_task_id = task_info['id'].split('.')[0] if '.' in task_info['id'] else task_info['id']
    
    dependency_entry = f"  - **task-{main_task_id}**: [Provides {task_info['title']} capability]\n"
    return dependency_entry


def generate_task_as_prd_section(task_info: Dict[str, Any]) -> str:
    """
    Generate a PRD section that represents the task.
    
    Args:
        task_info: Dictionary containing task information
        
    Returns:
        String representing the PRD section
    """
    prd_section = f"""
## Task {task_info['id']}: {task_info['title']}

### Purpose
{task_info['purpose']}

### Success Criteria
"""
    for criterion in task_info['success_criteria']:
        prd_section += f"- [ ] {criterion}\n"
    
    prd_section += f"""

### Implementation Details
{task_info['details']}

"""
    return prd_section


def create_reverse_engineered_prd(task_files: List[str]) -> str:
    """
    Create a PRD from a list of task markdown files.
    
    Args:
        task_files: List of paths to task markdown files
        
    Returns:
        String containing the generated PRD
    """
    # Start with the RPG template structure
    prd_content = """<rpg-method>
# Repository Planning Graph (RPG) Method - Reverse Engineered PRD

This PRD was automatically generated from existing task markdown files to recreate the original requirements that would generate these tasks when processed by task-master.
</rpg-method>

---

<overview>
## Problem Statement
[Based on the tasks identified in the existing task files, this project aims to address specific development needs that were originally outlined in a Product Requirements Document.]

## Target Users
[Users who benefit from the functionality described in the tasks]

## Success Metrics
[Metrics that would validate the successful completion of the tasks]
</overview>

---

<functional-decomposition>
## Capability Tree

"""
    
    # Process each task file to extract capabilities
    for task_file in task_files:
        task_info = extract_task_info_from_md(task_file)
        prd_content += generate_capability_from_task(task_info)
    
    prd_content += """</functional-decomposition>

---

<structural-decomposition>
## Repository Structure

```
project-root/
├── src/
│   ├── [module-name]/       # Maps to: [Capability Name]
│   │   ├── [file].js        # Maps to: [Feature Name]
│   │   └── index.js         # Public exports
│   └── [module-name]/
├── tests/
└── docs/
```

## Module Definitions

[Module definitions based on the tasks identified]
</structural-decomposition>

---

<dependency-graph>
## Dependency Chain

### Foundation Layer (Phase 0)
No dependencies - these are built first.

"""
    
    # Generate dependencies based on task relationships
    for task_file in task_files:
        task_info = extract_task_info_from_md(task_file)
        if task_info['dependencies'] and task_info['dependencies'].lower() != 'none':
            prd_content += generate_dependency_from_task(task_info)
    
    prd_content += """</dependency-graph>

---

<implementation-roadmap>
## Development Phases

### Phase 0: [Foundation Name]
**Goal**: [What foundational capability this establishes]

**Entry Criteria**: [What must be true before starting]

**Tasks**:
"""
    
    # Add tasks to the roadmap
    for task_file in task_files:
        task_info = extract_task_info_from_md(task_file)
        prd_content += f"- [ ] Implement {task_info['title']} (ID: {task_info['id']})\n"
        if task_info['dependencies'] and task_info['dependencies'].lower() != 'none':
            prd_content += f"  - Depends on: {task_info['dependencies']}\n"
        prd_content += "\n"
    
    prd_content += """**Exit Criteria**: [Observable outcome that proves phase complete]

**Delivers**: [What can users/developers do after this phase?]

---

</implementation-roadmap>

---

<test-strategy>
## Critical Test Scenarios

"""
    
    # Add test scenarios based on tasks
    for task_file in task_files:
        task_info = extract_task_info_from_md(task_file)
        prd_content += f"### {task_info['title']}\n"
        prd_content += "**Happy path**:\n"
        prd_content += f"- [Successfully implement {task_info['title']}]\n"
        prd_content += "- Expected: [Task completed successfully]\n\n"
        
        prd_content += "**Error cases**:\n"
        prd_content += f"- [Failure to implement {task_info['title']}]\n"
        prd_content += "- Expected: [Proper error handling]\n\n"
    
    prd_content += """</test-strategy>

---

<architecture>
## System Components
[Major architectural pieces based on the tasks identified]

## Technology Stack
[Languages, frameworks, key libraries needed to implement the tasks]
</architecture>

---

<risks>
## Technical Risks
**Risk**: Complexity of implementing all identified tasks
- **Impact**: High - Could delay project timeline
- **Likelihood**: Medium
- **Mitigation**: Break tasks into smaller subtasks
- **Fallback**: Prioritize critical tasks first
</risks>

---

<appendix>
## Open Questions
[Questions that arose during the reverse engineering process]
</appendix>

---

<task-master-integration>
# How Task Master Uses This PRD

This PRD was generated to recreate the original requirements that would produce the same tasks when processed by task-master.
</task-master-integration>
"""
    
    return prd_content


def main():
    parser = argparse.ArgumentParser(description="Reverse engineer PRD from task markdown files")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing task markdown files")
    parser.add_argument("--output", "-o", required=True, help="Output file for generated PRD")
    parser.add_argument("--pattern", default="task-*.md", help="File pattern to match (default: task-*.md)")
    
    args = parser.parse_args()
    
    # Find all task markdown files
    input_path = Path(args.input_dir)
    task_files = list(input_path.glob(args.pattern))
    
    if not task_files:
        print(f"No task files found in {input_path} with pattern {args.pattern}")
        return 1
    
    print(f"Found {len(task_files)} task files to process")
    
    # Generate the PRD
    prd_content = create_reverse_engineered_prd(task_files)
    
    # Write the PRD to output file
    output_path = Path(args.output)
    output_path.write_text(prd_content, encoding='utf-8')
    
    print(f"Generated PRD with {len(task_files)} tasks and saved to {output_path}")
    print("The generated PRD follows the RPG method structure that task-master expects.")
    
    return 0


if __name__ == "__main__":
    exit(main())