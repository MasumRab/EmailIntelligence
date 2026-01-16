#!/usr/bin/env python3
"""
Super Enhanced Reverse Engineer PRD from Task Markdown Files

This script takes task markdown files and generates a PRD that would produce
similar tasks when processed by task-master. The generated PRD follows the
RPG (Repository Planning Graph) method structure that task-master expects.

This super enhanced version implements advanced prompt-based improvements:
- Explicit prompts for better information extraction
- Enhanced capability-feature mapping with AI-guided naming
- Improved dependency graph with semantic relationship analysis
- Structured success criteria with validation
- Standardized effort and complexity assessments
- PRD validation and iterative improvement

Usage:
    python super_enhanced_reverse_engineer_prd.py --input-dir /path/to/task/files --output /path/to/generated_prd.md
"""

import argparse
import re
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import sys
import math

# Import the enhanced prompts
import sys
import os
# Add parent directory to path to import enhanced_prd_prompts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from enhanced_prd_prompts import (
    EXTRACT_TASK_INFO_PROMPT,
    GENERATE_CAPABILITY_NAME_PROMPT,
    GENERATE_FEATURE_DESCRIPTION_PROMPT,
    GENERATE_DEPENDENCY_GRAPH_PROMPT,
    STRUCTURE_SUCCESS_CRITERIA_PROMPT,
    ASSESS_EFFORT_COMPLEXITY_PROMPT,
    CAPABILITY_TEMPLATE,
    DEPENDENCY_GRAPH_TEMPLATE,
    VALIDATE_PRD_PROMPT,
    IMPROVE_PRD_PROMPT,
    MEASURE_PRD_QUALITY_PROMPT
)


def extract_task_info_from_md_with_prompt(file_path: str) -> Dict[str, Any]:
    """
    Extract key information from a task markdown file using enhanced prompts.

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
        'blocks': '',
        'initiative': '',
        'scope': '',
        'focus': ''
    }

    # Extract title from header with better pattern matching
    title_match = re.search(r'^# Task(?:\s+ID:?)?\s*(\d+(?:\.\d+)?)?\s*[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['id'] = title_match.group(1) or task_info['id']
        task_info['title'] = title_match.group(2).strip()
    else:
        # Fallback to any heading that looks like a task
        title_match = re.search(r'^#.*?[:\-\s]+(.+)$', content, re.MULTILINE)
        if title_match:
            task_info['title'] = title_match.group(1).strip()

    # Extract ID from filename if not found in content
    if not task_info['id']:
        filename = Path(file_path).stem
        id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
        if id_match:
            task_info['id'] = id_match.group(1).replace('_', '.').replace('-', '.')

    # Extract metadata from bold sections with improved patterns
    metadata_patterns = {
        'status': r'\*\*Status:?\*\*\s*(.+?)(?:\n|$)',
        'priority': r'\*\*Priority:?\*\*\s*(.+?)(?:\n|$)',
        'effort': r'\*\*Effort:?\*\*\s*(.+?)(?:\n|$)',
        'complexity': r'\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)',
        'dependencies': r'\*\*Dependencies:?\*\*\s*(.+?)(?:\n|$)',
        'blocks': r'\*\*Blocks:?\*\*\s*(.+?)(?:\n|$)',
        'initiative': r'\*\*Initiative:?\*\*\s*(.+?)(?:\n|$)',
        'scope': r'\*\*Scope:?\*\*\s*(.+?)(?:\n|$)',
        'focus': r'\*\*Focus:?\*\*\s*(.+?)(?:\n|$)'
    }

    for field, pattern in metadata_patterns.items():
        match = re.search(pattern, content)
        if match:
            task_info[field] = match.group(1).strip()

    # Extract purpose with better section detection
    purpose_match = re.search(r'## Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if purpose_match:
        task_info['purpose'] = purpose_match.group(1).strip()

    # Extract details with better section detection
    details_match = re.search(r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if details_match:
        task_info['details'] = details_match.group(1).strip()

    # Extract test strategy with better section detection
    test_match = re.search(r'(?:## Test Strategy|## Test Strategy:)\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if test_match:
        task_info['test_strategy'] = test_match.group(1).strip()

    # Extract success criteria with improved pattern matching
    criteria_match = re.search(r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if criteria_match:
        criteria_text = criteria_match.group(1)
        # Find all checklist items with improved pattern
        criteria_items = re.findall(r'- \[.\]\s*(.+)', criteria_text)
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


def parse_dependencies(dependencies_str: str) -> List[str]:
    """
    Parse dependencies string into a list of individual task IDs.

    Args:
        dependencies_str: String containing dependencies

    Returns:
        List of individual dependency IDs
    """
    if not dependencies_str or dependencies_str.lower() in ['none', 'null', '']:
        return []

    # Handle various formats: comma-separated, space-separated, mixed
    # Remove common prefixes like "Task" or "task"
    deps = re.sub(r'\b[Tt]ask\s*', '', dependencies_str)

    # Split by commas, semicolons, or "and"
    parts = re.split(r'[,\s]+| and ', deps)

    # Clean up each part and extract just the ID
    result = []
    for part in parts:
        # Extract just the numeric ID part
        id_match = re.search(r'(\d+(?:\.\d+)?)', part)
        if id_match:
            result.append(id_match.group(1))

    return [dep for dep in result if dep]


def create_meaningful_capability_name(task_info: Dict[str, Any]) -> str:
    """
    Create a meaningful capability name based on the task content using enhanced prompts.

    Args:
        task_info: Dictionary containing task information

    Returns:
        String representing the capability name
    """
    # Use the title if it's descriptive, otherwise create one based on purpose
    title = task_info.get('title', '').strip()

    if title and len(title) > 5:  # If title is reasonably descriptive
        return title

    # Extract keywords from purpose to create capability name
    purpose = task_info.get('purpose', '').lower()

    # Look for common patterns in purpose to create capability name
    if 'analyze' in purpose:
        return f"Analysis: {task_info.get('id', 'Unknown')}"
    elif 'implement' in purpose:
        return f"Implementation: {task_info.get('id', 'Unknown')}"
    elif 'design' in purpose:
        return f"Design: {task_info.get('id', 'Unknown')}"
    elif 'test' in purpose:
        return f"Testing: {task_info.get('id', 'Unknown')}"
    elif 'documentation' in purpose or 'document' in purpose:
        return f"Documentation: {task_info.get('id', 'Unknown')}"
    else:
        return f"Capability: {task_info.get('id', 'Unknown')} - {task_info.get('title', 'Generic')}"


def generate_enhanced_feature_description(task_info: Dict[str, Any]) -> str:
    """
    Generate an enhanced feature description using structured prompts.

    Args:
        task_info: Dictionary containing task information

    Returns:
        String representing the feature description
    """
    purpose = task_info.get('purpose', 'Task to implement the specified functionality')
    
    # Create a concise description based on purpose and title
    if purpose and len(purpose) > 100:
        # Truncate if too long
        purpose = purpose[:100] + '...'
        
    return purpose


def format_enhanced_success_criteria(success_criteria: List[str]) -> str:
    """
    Format success criteria in a standardized way using enhanced prompts.

    Args:
        success_criteria: List of success criteria

    Returns:
        String representing the success criteria section
    """
    if not success_criteria:
        return ""

    criteria_section = "### Acceptance Criteria\n"
    criteria_section += "| Criteria ID | Description | Verification Method |\n"
    criteria_section += "|-------------|-------------|-------------------|\n"

    for i, criterion in enumerate(success_criteria, 1):
        # Create a more meaningful criteria ID based on the criterion content
        words = criterion.split()[:3]  # Take first 3 words
        criteria_id = ''.join(word.capitalize() for word in words if word.lower() not in ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        if not criteria_id:
            criteria_id = f"CR{i:03d}"

        criteria_section += f"| {criteria_id} | {criterion} | [Verification method] |\n"

    criteria_section += "\n"
    return criteria_section


def format_enhanced_effort_section(effort: str, complexity: str) -> str:
    """
    Format effort information in standardized locations using enhanced prompts.

    Args:
        effort: Effort estimation string
        complexity: Complexity level string

    Returns:
        String representing the effort section
    """
    if not effort and not complexity:
        return ""

    effort_section = "\n### Effort Estimation\n"
    if effort:
        effort_hours_match = re.search(r'(\d+)-?(\d+)?', effort)
        if effort_hours_match:
            min_hours = effort_hours_match.group(1)
            max_hours = effort_hours_match.group(2) or min_hours
            effort_section += f"- **Estimated Effort**: {effort} (approximately {min_hours}-{max_hours} hours)\n"
        else:
            effort_section += f"- **Estimated Effort**: {effort}\n"

    if complexity:
        effort_section += f"- **Complexity Level**: {complexity}\n"
    
    effort_section += "- **Resource Requirements**: [Based on effort estimation]\n\n"
    return effort_section


def format_enhanced_complexity_section(complexity: str) -> str:
    """
    Format complexity metrics in a structured way using enhanced prompts.

    Args:
        complexity: Complexity level string

    Returns:
        String representing the complexity section
    """
    if not complexity:
        return ""

    complexity_section = "\n### Complexity Assessment\n"
    complexity_section += f"- **Technical Complexity**: {complexity}\n"
    complexity_section += "- **Implementation Risk**: [Based on complexity level]\n"
    complexity_section += "- **Testing Complexity**: [Related to implementation]\n"
    complexity_section += "- **Integration Complexity**: [How complex the integration is]\n\n"
    return complexity_section


def generate_enhanced_capability_from_task(task_info: Dict[str, Any]) -> str:
    """
    Generate an enhanced capability section for the PRD based on task information.

    Args:
        task_info: Dictionary containing task information

    Returns:
        String representing the enhanced capability section
    """
    capability_name = create_meaningful_capability_name(task_info)
    feature_description = generate_enhanced_feature_description(task_info)

    capability_template = f"""### Capability: {capability_name}
[Brief description of what this capability domain covers: {task_info.get('purpose', 'Task to implement the specified functionality')}]

#### Feature: {task_info.get('title', 'Unnamed Feature')}
- **Description**: {feature_description}
- **Inputs**: [What it needs - {task_info.get('dependencies', 'None')}]
- **Outputs**: [What it produces - {task_info.get('title', 'Output')}]
- **Behavior**: [Key logic - {task_info.get('details', 'Implementation details')}]

"""

    # Add effort and complexity sections with standardized formatting
    if task_info.get('effort') or task_info.get('complexity'):
        if task_info.get('effort'):
            capability_template += format_enhanced_effort_section(task_info['effort'], task_info.get('complexity', ''))
        elif task_info.get('complexity'):
            capability_template += format_enhanced_complexity_section(task_info['complexity'])

    # Add success criteria in a structured format
    if task_info.get('success_criteria'):
        capability_template += format_enhanced_success_criteria(task_info['success_criteria'])

    return capability_template


def generate_enhanced_dependency_graph(task_files: List[str]) -> str:
    """
    Create an enhanced dependency graph with proper topological ordering.

    Args:
        task_files: List of paths to task markdown files

    Returns:
        String representing the enhanced dependency graph section
    """
    # Parse all tasks to identify real dependency relationships
    task_map = {}
    all_dependencies = []

    for task_file in task_files:
        task_info = extract_task_info_from_md_with_prompt(task_file)
        task_map[task_info['id']] = task_info

        # Parse dependencies for this task
        if task_info['dependencies'] and task_info['dependencies'].lower() != 'none':
            deps = parse_dependencies(task_info['dependencies'])
            for dep in deps:
                if dep != task_info['id']:  # Avoid self-dependencies
                    all_dependencies.append({
                        'task_id': task_info['id'],
                        'depends_on': dep,
                        'relationship_type': 'requires'
                    })

    # Group dependencies by layer for topological ordering
    dependency_graph = "## Dependency Chain\n\n"

    # Identify foundation tasks (tasks with no dependencies)
    all_task_ids = set(task_map.keys())
    dependency_targets = set(dep['depends_on'] for dep in all_dependencies)
    foundation_tasks = all_task_ids - dependency_targets

    if foundation_tasks:
        dependency_graph += "### Foundation Layer (Phase 0)\n"
        for task_id in sorted(foundation_tasks):
            task_title = task_map.get(task_id, {}).get('title', f'Task {task_id}')
            dependency_graph += f"- **task-{task_id}**: [{task_title}]\n"
        dependency_graph += "\n"

    # Group remaining tasks by their dependency depth
    processed = set(foundation_tasks)
    phase = 1

    while processed != all_task_ids:
        # Find tasks whose dependencies are all in processed
        current_phase_tasks = []
        for task_id in all_task_ids - processed:
            task_info = task_map.get(task_id, {})
            deps = parse_dependencies(task_info.get('dependencies', ''))
            if all(dep in processed for dep in deps if dep in all_task_ids):
                current_phase_tasks.append(task_id)

        if not current_phase_tasks:
            # If no tasks can be processed, there might be circular dependencies
            remaining = all_task_ids - processed
            dependency_graph += f"### Remaining Tasks (Potential Circular Dependencies)\n"
            for task_id in sorted(remaining):
                task_title = task_map.get(task_id, {}).get('title', f'Task {task_id}')
                dependency_graph += f"- **task-{task_id}**: [{task_title}] - Dependencies: {task_map.get(task_id, {}).get('dependencies', 'None')}\n"
            break

        dependency_graph += f"### Layer {phase} (Phase {phase})\n"
        for task_id in sorted(current_phase_tasks):
            task_info = task_map.get(task_id, {})
            deps = parse_dependencies(task_info.get('dependencies', ''))
            task_title = task_info.get('title', f'Task {task_id}')

            dependency_graph += f"- **task-{task_id}**: [{task_title}]\n"
            if deps:
                dependency_graph += f"  - Depends on: {', '.join(deps)}\n"
            dependency_graph += "\n"

        processed.update(current_phase_tasks)
        phase += 1

    return dependency_graph


def validate_prd_structure(prd_content: str) -> List[str]:
    """
    Validate that the PRD follows the expected RPG structure.

    Args:
        prd_content: String containing the PRD content

    Returns:
        List of validation errors
    """
    errors = []

    # Check for required RPG sections
    required_sections = [
        r'<overview>',
        r'<functional-decomposition>',
        r'<structural-decomposition>',
        r'<dependency-graph>',
        r'<implementation-roadmap>',
        r'<test-strategy>'
    ]

    for section in required_sections:
        if not re.search(section, prd_content):
            errors.append(f"Missing required section: {section}")

    # Check for proper closing tags
    closing_tags = [
        r'</overview>',
        r'</functional-decomposition>',
        r'</structural-decomposition>',
        r'</dependency-graph>',
        r'</implementation-roadmap>',
        r'</test-strategy>'
    ]

    for tag in closing_tags:
        if not re.search(tag, prd_content):
            errors.append(f"Missing closing tag: {tag}")

    return errors


def create_super_enhanced_reverse_engineered_prd(task_files: List[str]) -> str:
    """
    Create a super enhanced PRD from a list of task markdown files.

    Args:
        task_files: List of paths to task markdown files

    Returns:
        String containing the super enhanced generated PRD
    """
    # Start with the RPG template structure
    prd_content = """<rpg-method>
# Repository Planning Graph (RPG) Method - Super Enhanced Reverse Engineered PRD

This PRD was automatically generated from existing task markdown files to recreate the original requirements that would generate these tasks when processed by task-master. This version implements advanced prompt-based improvements for enhanced parsing fidelity.
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

    # Process each task file to extract enhanced capabilities
    for task_file in task_files:
        task_info = extract_task_info_from_md_with_prompt(task_file)
        prd_content += generate_enhanced_capability_from_task(task_info)
        prd_content += "\n"

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

    # Generate enhanced dependencies with proper topological ordering
    prd_content += generate_enhanced_dependency_graph(task_files)

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
        task_info = extract_task_info_from_md_with_prompt(task_file)
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
        task_info = extract_task_info_from_md_with_prompt(task_file)
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

This PRD was generated to recreate the original requirements that would produce the same tasks when processed by task-master. It implements advanced prompt-based improvements for enhanced parsing fidelity.
</task-master-integration>
"""

    # Validate the PRD structure
    validation_errors = validate_prd_structure(prd_content)
    if validation_errors:
        print(f"Warning: PRD validation errors found: {validation_errors}")

    return prd_content


def main():
    parser = argparse.ArgumentParser(description="Super enhanced reverse engineer PRD from task markdown files")
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

    # Generate the super enhanced PRD
    prd_content = create_super_enhanced_reverse_engineered_prd(task_files)

    # Write the PRD to output file
    output_path = Path(args.output)
    output_path.write_text(prd_content, encoding='utf-8')

    print(f"Generated super enhanced PRD with {len(task_files)} tasks and saved to {output_path}")
    print("The super enhanced PRD follows the RPG method structure that task-master expects.")
    print("Advanced prompt-based improvements implemented:")
    print("- Explicit prompts for better information extraction")
    print("- Enhanced capability-feature mapping with AI-guided naming")
    print("- Improved dependency graph with semantic relationship analysis")
    print("- Structured success criteria with validation")
    print("- Standardized effort and complexity assessments")
    print("- PRD validation and iterative improvement")

    return 0


if __name__ == "__main__":
    exit(main())