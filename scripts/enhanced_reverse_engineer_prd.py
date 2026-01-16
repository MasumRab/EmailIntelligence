#!/usr/bin/env python3
"""
Enhanced Reverse Engineer PRD from Task Markdown Files

This script takes task markdown files and generates a PRD that would produce 
similar tasks when processed by task-master. The generated PRD follows the 
RPG (Repository Planning Graph) method structure that task-master expects.

This enhanced version addresses the low similarity scores identified in the 
Ralph loop analysis:
- Dependencies: 0% similarity → Now properly mapped
- Effort: 13.7% similarity → Now standardized
- Success Criteria: 13.7% similarity → Now structured
- Complexity: 33.6% similarity → Now standardized

Usage:
    python enhanced_reverse_engineer_prd.py --input-dir /path/to/task/files --output /path/to/generated_prd.md
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
        'details': '',
        'test_strategy': '',
        'blocks': ''
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
    
    blocks_match = re.search(r'\*\*Blocks:?\*\*\s*(.+?)(?:\n|$)', content)
    if blocks_match:
        task_info['blocks'] = blocks_match.group(1).strip()
    
    # Extract purpose
    purpose_match = re.search(r'## Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if purpose_match:
        task_info['purpose'] = purpose_match.group(1).strip()
    
    # Extract details
    details_match = re.search(r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if details_match:
        task_info['details'] = details_match.group(1).strip()
    
    # Extract test strategy
    test_match = re.search(r'## Test Strategy\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if test_match:
        task_info['test_strategy'] = test_match.group(1).strip()
    
    # Extract success criteria
    criteria_match = re.search(r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if criteria_match:
        criteria_text = criteria_match.group(1)
        # Find all checklist items
        criteria_items = re.findall(r'- \[.\] (.+)', criteria_text)
        task_info['success_criteria'] = criteria_items
    
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


def generate_dependency_graph_from_tasks(task_files: List[str]) -> str:
    """
    Create a comprehensive dependency graph that accurately reflects
    the relationships between tasks based on their actual dependencies.
    
    Args:
        task_files: List of paths to task markdown files
        
    Returns:
        String representing the dependency graph section
    """
    all_dependencies = []
    
    for task_file in task_files:
        task_info = extract_task_info_from_md(task_file)
        if task_info['dependencies'] and task_info['dependencies'].lower() != 'none':
            # Parse the dependencies string to extract individual task IDs
            # Handle both comma-separated and space-separated dependencies
            dep_text = task_info['dependencies']
            # Split by comma or semicolon, then strip spaces
            deps = [dep.strip() for dep in re.split(r'[,\s]+', dep_text) if dep.strip()]
            
            for dep in deps:
                # Clean up dependency ID (remove extra text)
                dep_id = re.sub(r'[^0-9.]', '', dep)  # Keep only digits and dots
                if dep_id and dep_id != 'None' and dep_id != task_info['id']:
                    all_dependencies.append({
                        'task_id': task_info['id'],
                        'depends_on': dep_id,
                        'relationship_type': 'requires'
                    })
    
    # Generate structured dependency graph
    if not all_dependencies:
        return "### Foundation Layer (Phase 0)\nNo dependencies - these are built first.\n\n"
    
    dependency_graph = "## Dependency Chain\n\n"
    
    # Group dependencies by layer
    foundation_tasks = []
    dependent_tasks = []
    
    for dep in all_dependencies:
        if dep['depends_on'] not in [d['task_id'] for d in all_dependencies]:
            foundation_tasks.append(dep['depends_on'])
        dependent_tasks.append(dep)
    
    # Add foundation layer
    if foundation_tasks:
        dependency_graph += "### Foundation Layer (Phase 0)\n"
        for task_id in set(foundation_tasks):
            dependency_graph += f"- **task-{task_id}**: [Foundation task]\n"
        dependency_graph += "\n"
    
    # Add dependent layers
    for dep in dependent_tasks:
        dependency_graph += f"### Task {dep['task_id']}\n"
        dependency_graph += f"- **Depends on**: Task {dep['depends_on']}\n"
        dependency_graph += f"- **Relationship**: {dep['relationship_type']}\n\n"
    
    return dependency_graph


def format_success_criteria_for_prd(task_info: Dict[str, Any]) -> str:
    """
    Format success criteria in a standardized way that task-master can easily parse
    
    Args:
        task_info: Dictionary containing task information
        
    Returns:
        String representing the success criteria section
    """
    if not task_info['success_criteria']:
        return ""
    
    criteria_section = "### Acceptance Criteria\n"
    criteria_section += "| Criteria ID | Description | Verification Method |\n"
    criteria_section += "|-------------|-------------|-------------------|\n"
    
    for i, criterion in enumerate(task_info['success_criteria'], 1):
        criteria_section += f"| AC{i:03d} | {criterion} | [Test method] |\n"
    
    criteria_section += "\n"
    return criteria_section


def add_effort_to_prd_sections(task_info: Dict[str, Any]) -> str:
    """
    Add effort information in standardized locations throughout the PRD
    
    Args:
        task_info: Dictionary containing task information
        
    Returns:
        String representing the effort section
    """
    if not task_info['effort']:
        return ""
    
    effort_section = f"""
### Effort Estimation
- **Estimated Effort**: {task_info['effort']}
- **Complexity Level**: {task_info['complexity']}
- **Resource Requirements**: [Based on effort estimation]
"""
    return effort_section


def add_complexity_metrics(task_info: Dict[str, Any]) -> str:
    """
    Add complexity metrics in a structured format
    
    Args:
        task_info: Dictionary containing task information
        
    Returns:
        String representing the complexity section
    """
    if not task_info['complexity']:
        return ""
    
    complexity_section = f"""
### Complexity Assessment
- **Technical Complexity**: {task_info['complexity']}
- **Implementation Risk**: [Based on complexity level]
- **Testing Complexity**: [Related to implementation]
- **Integration Complexity**: [How complex the integration is]
"""
    return complexity_section


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
    
    # Add effort and complexity sections
    if task_info['effort']:
        capability_template += add_effort_to_prd_sections(task_info)
    if task_info['complexity']:
        capability_template += add_complexity_metrics(task_info)
    
    # Add success criteria
    if task_info['success_criteria']:
        capability_template += format_success_criteria_for_prd(task_info)
    
    capability_template += "\n"
    return capability_template


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

"""
    
    # Add success criteria in a structured format
    if task_info['success_criteria']:
        prd_section += "### Success Criteria\n"
        for criterion in task_info['success_criteria']:
            prd_section += f"- [ ] {criterion}\n"
        prd_section += "\n"
    
    # Add effort and complexity
    if task_info['effort']:
        prd_section += f"### Effort\n{task_info['effort']}\n\n"
    if task_info['complexity']:
        prd_section += f"### Complexity\n{task_info['complexity']}\n\n"
    
    prd_section += f"""
### Implementation Details
{task_info['details']}

"""
    
    # Add test strategy if available
    if task_info['test_strategy']:
        prd_section += f"### Test Strategy\n{task_info['test_strategy']}\n\n"
    
    return prd_section


def create_enhanced_reverse_engineered_prd(task_files: List[str]) -> str:
    """
    Create an enhanced PRD from a list of task markdown files.
    
    Args:
        task_files: List of paths to task markdown files
        
    Returns:
        String containing the enhanced generated PRD
    """
    # Start with the RPG template structure
    prd_content = """<rpg-method>
# Repository Planning Graph (RPG) Method - Enhanced Reverse Engineered PRD

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

"""
    
    # Generate dependencies based on actual task relationships
    prd_content += generate_dependency_graph_from_tasks(task_files)
    
    prd_content += """</dependency-graph>

---

<implementation-roadmap>
## Development Phases

### Phase 0: [Foundation Name]
**Goal**: [What foundational capability this establishes]

**Entry Criteria**: [What must be true before starting]

**Tasks**:
"""
    
    # Add tasks to the roadmap with proper dependency information
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
    
    # Add test scenarios based on tasks with proper success criteria
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
    parser = argparse.ArgumentParser(description="Enhanced reverse engineer PRD from task markdown files")
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
    
    # Generate the enhanced PRD
    prd_content = create_enhanced_reverse_engineered_prd(task_files)
    
    # Write the PRD to output file
    output_path = Path(args.output)
    output_path.write_text(prd_content, encoding='utf-8')
    
    print(f"Generated enhanced PRD with {len(task_files)} tasks and saved to {output_path}")
    print("The enhanced PRD follows the RPG method structure that task-master expects.")
    print("Improvements made to address low similarity scores:")
    print("- Dependencies: Now properly mapped with structured relationships")
    print("- Effort: Now standardized in effort estimation sections")
    print("- Success Criteria: Now in structured acceptance criteria format")
    print("- Complexity: Now in standardized complexity assessment format")
    
    return 0


if __name__ == "__main__":
    exit(main())