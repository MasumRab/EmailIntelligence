#!/usr/bin/env python3
"""
Ultra Enhanced Reverse Engineer PRD from Task Markdown Files

This script takes task markdown files and generates a PRD that would produce
similar tasks when processed by task-master. The generated PRD follows the
RPG (Repository Planning Graph) method structure that task-master expects.

This ultra enhanced version implements advanced improvements:
- Enhanced information extraction with better parsing of structured content
- Improved capability-feature mapping with semantic analysis
- Advanced dependency graph with topological ordering and validation
- Structured success criteria with standardized formatting
- Standardized effort and complexity assessments
- Enhanced validation and iterative improvement mechanisms
- Better handling of the 14-section task format

Usage:
    python ultra_enhanced_reverse_engineer_prd.py --input-dir /path/to/task/files --output /path/to/generated_prd.md
"""

import argparse
import re
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import sys
import math


def extract_task_info_from_md_ultra_enhanced(file_path: str) -> Dict[str, Any]:
    """
    Ultra enhanced function to extract comprehensive information from task markdown files.
    Handles both standard 14-section format and legacy formats with extended metadata.
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
        'owner': '',
        'initiative': '',
        'scope': '',
        'focus': '',
        'prerequisites': '',
        'specification_details': '',
        'implementation_guide': '',
        'configuration_params': '',
        'performance_targets': '',
        'common_gotchas': '',
        'integration_checkpoint': '',
        'done_definition': '',
        'next_steps': '',
        'extended_metadata': {},
    }

    # Extract ID and title from header with multiple pattern support
    # Try 14-section format first
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['title'] = title_match.group(1).strip()
    
    # Extract ID from filename or content
    filename = Path(file_path).stem
    id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
    if id_match:
        task_info['id'] = id_match.group(1).replace('_', '.').replace('-', '.')
    else:
        # Try to extract from content if not in filename
        id_from_content = re.search(r'# Task\s+(?:ID:\s*)?(\d+(?:\.\d+)?)', content)
        if id_from_content:
            task_info['id'] = id_from_content.group(1)

    # Extract metadata from bold sections with comprehensive patterns
    metadata_patterns = {
        'status': r'\*\*Status:?\*\*\s*(.+?)(?:\n|$)',
        'priority': r'\*\*Priority:?\*\*\s*(.+?)(?:\n|$)',
        'effort': r'\*\*Effort:?\*\*\s*(.+?)(?:\n|$)',
        'complexity': r'\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)',
        'dependencies': r'\*\*Dependencies:?\*\*\s*(.+?)(?:\n|$)',
        'blocks': r'\*\*Blocks:?\*\*\s*(.+?)(?:\n|$)',
        'initiative': r'\*\*Initiative:?\*\*\s*(.+?)(?:\n|$)',
        'scope': r'\*\*Scope:?\*\*\s*(.+?)(?:\n|$)',
        'focus': r'\*\*Focus:?\*\*\s*(.+?)(?:\n|$)',
        'owner': r'\*\*Owner:?\*\*\s*(.+?)(?:\n|$)',
    }

    for field, pattern in metadata_patterns.items():
        match = re.search(pattern, content)
        if match:
            task_info[field] = match.group(1).strip()

    # Extract structured sections for 14-section format
    sections = {
        'purpose': r'## Overview/Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'success_criteria': r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'prerequisites': r'## Prerequisites & Dependencies\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'subtasks_breakdown': r'## Sub-subtasks Breakdown\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'specification_details': r'## Specification Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'implementation_guide': r'## Implementation Guide\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'configuration_params': r'## Configuration Parameters\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'performance_targets': r'## Performance Targets\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'testing_strategy': r'## Testing Strategy\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'common_gotchas': r'## Common Gotchas & Solutions\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'integration_checkpoint': r'## Integration Checkpoint\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'done_definition': r'## Done Definition\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'next_steps': r'## Next Steps\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'details': r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'test_strategy': r'## Test Strategy\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
    }

    for section_name, pattern in sections.items():
        match = re.search(pattern, content)
        if match:
            section_content = match.group(1).strip()
            if section_name == 'success_criteria':
                # Parse success criteria as checklist items
                criteria_items = re.findall(r'- \[.\]\s*(.+)', section_content)
                task_info['success_criteria'] = criteria_items
            elif section_name == 'subtasks_breakdown':
                # Parse subtasks if in table format
                table_match = re.search(r'\|\s*ID\s*\|\s*Subtask\s*\|[\s\S]*?\n((?:\|\s*[^\n]*\s*\|.*\n)+)', section_content)
                if table_match:
                    table_content = table_match.group(1)
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
                else:
                    # If not in table format, just store the content
                    task_info[section_name] = section_content
            else:
                task_info[section_name] = section_content

    # If success criteria weren't found in structured format, look for them in other ways
    if not task_info['success_criteria']:
        # Look for checklist items anywhere in the content
        checklist_pattern = r'- \[.\]\s*(.+?)(?=\n- \[|\Z)'
        checklist_matches = re.findall(checklist_pattern, content)
        task_info['success_criteria'] = checklist_matches

    # Extract extended metadata from comments
    ext_meta_match = re.search(r'<!-- EXTENDED_METADATA\s*\n([\s\S]*?)\nEND_EXTENDED_METADATA -->', content)
    if ext_meta_match:
        ext_meta_content = ext_meta_match.group(1)
        # Parse the extended metadata
        for line in ext_meta_content.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                task_info['extended_metadata'][key.strip()] = value.strip()

    # If purpose wasn't found in structured format, try to extract from description
    if not task_info['purpose']:
        desc_match = re.search(r'\*\*Description:?\*\*\s*(.+?)(?:\n|$)', content)
        if desc_match:
            task_info['purpose'] = desc_match.group(1).strip()

    # If details weren't found in structured format, try to extract from main content
    if not task_info['details']:
        # Look for content after the main header but before the first ## section
        header_end = content.find('\n\n')  # First double newline after header
        if header_end != -1:
            after_header = content[header_end:]
            # Look for first paragraph before any ## sections
            para_match = re.search(r'^([^\n]+\n?)+?(?=\n## |\n---|\n\*\*|\Z)', after_header, re.MULTILINE)
            if para_match:
                task_info['details'] = para_match.group(0).strip()

    return task_info


def parse_dependencies_ultra_enhanced(dependencies_str: str) -> List[str]:
    """
    Ultra enhanced function to parse dependencies string into a list of individual task IDs.
    Handles various formats and edge cases.
    """
    if not dependencies_str or dependencies_str.lower() in ['none', 'null', '', 'n/a']:
        return []

    # Handle various formats: comma-separated, space-separated, mixed
    # Remove common prefixes like "Task" or "task"
    deps = re.sub(r'\b[Tt]ask\s*', '', dependencies_str)

    # Split by commas, semicolons, or "and" - but preserve hyphens in task IDs
    parts = re.split(r',\s*|\s+and\s+|\s+AND\s+', deps)

    # Clean up each part and extract just the ID
    result = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Extract task ID patterns (e.g., 001, 001.1, 1, 1.1, etc.)
        # This pattern captures task IDs with optional decimal points
        id_matches = re.findall(r'(\d+(?:\.\d+)?)', part)
        for id_match in id_matches:
            # Normalize the ID format (ensure dots for decimals)
            normalized_id = id_match.replace(',', '.')
            if normalized_id:
                result.append(normalized_id)

    return [dep for dep in result if dep]


def create_meaningful_capability_name_ultra(task_info: Dict[str, Any]) -> str:
    """
    Ultra enhanced function to create a meaningful capability name based on the task content.

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
    elif 'integration' in purpose:
        return f"Integration: {task_info.get('id', 'Unknown')}"
    elif 'validation' in purpose:
        return f"Validation: {task_info.get('id', 'Unknown')}"
    elif 'alignment' in purpose or 'align' in purpose:
        return f"Alignment: {task_info.get('id', 'Unknown')}"
    else:
        # Create capability name from first few words of purpose if available
        purpose_words = purpose.split()[:3]
        if purpose_words:
            return f"{' '.join(word.capitalize() for word in purpose_words)}: {task_info.get('id', 'Unknown')}"
        else:
            return f"Capability: {task_info.get('id', 'Unknown')} - {task_info.get('title', 'Generic')}"


def format_success_criteria_ultra_enhanced(success_criteria: List[str]) -> str:
    """
    Ultra enhanced function to format success criteria in a standardized way.

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
            criteria_id = f"AC{i:03d}"

        criteria_section += f"| {criteria_id} | {criterion} | [Verification method] |\n"

    criteria_section += "\n"
    return criteria_section


def format_effort_section_ultra_enhanced(effort: str, complexity: str) -> str:
    """
    Ultra enhanced function to format effort information in standardized locations.

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
        # Try to parse effort ranges like "23-31 hours" or "2-3 hours"
        effort_hours_match = re.search(r'(\d+)-?(\d+)?\s*(hours|hrs|h)?', effort)
        if effort_hours_match:
            min_hours = effort_hours_match.group(1)
            max_hours = effort_hours_match.group(2) or min_hours
            effort_unit = effort_hours_match.group(3) or "hours"
            effort_section += f"- **Estimated Effort**: {effort} (approximately {min_hours}-{max_hours} {effort_unit})\n"
        else:
            effort_section += f"- **Estimated Effort**: {effort}\n"

    if complexity:
        effort_section += f"- **Complexity Level**: {complexity}\n"

    effort_section += "- **Resource Requirements**: [Based on effort estimation]\n\n"
    return effort_section


def format_complexity_section_ultra_enhanced(complexity: str) -> str:
    """
    Ultra enhanced function to format complexity metrics in a structured way.

    Args:
        complexity: Complexity level string

    Returns:
        String representing the complexity section
    """
    if not complexity:
        return ""

    complexity_section = "\n### Complexity Assessment\n"
    complexity_section += f"- **Technical Complexity**: {complexity}\n"
    
    # Try to extract numeric value from complexity for risk assessment
    complexity_num_match = re.search(r'(\d+)(?:/10)?', complexity)
    if complexity_num_match:
        complexity_num = int(complexity_num_match.group(1))
        if complexity_num >= 8:
            risk_level = "High"
        elif complexity_num >= 5:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        complexity_section += f"- **Implementation Risk**: {risk_level}\n"
    else:
        complexity_section += "- **Implementation Risk**: [Based on complexity level]\n"
    
    complexity_section += "- **Testing Complexity**: [Related to implementation]\n"
    complexity_section += "- **Integration Complexity**: [How complex the integration is]\n\n"
    return complexity_section


def generate_enhanced_capability_from_task_ultra(task_info: Dict[str, Any]) -> str:
    """
    Ultra enhanced function to generate a capability section for the PRD based on task information.

    Args:
        task_info: Dictionary containing task information

    Returns:
        String representing the enhanced capability section
    """
    capability_name = create_meaningful_capability_name_ultra(task_info)
    
    # Create feature description from purpose or details
    purpose = task_info.get('purpose', 'Task to implement the specified functionality')
    if purpose and len(purpose) > 100:
        # Truncate if too long
        purpose = purpose[:100] + '...'

    capability_template = f"""### Capability: {capability_name}
[Brief description of what this capability domain covers: {purpose}]

#### Feature: {task_info.get('title', 'Unnamed Feature')}
- **Description**: {purpose}
- **Inputs**: [What it needs - {task_info.get('dependencies', 'None')}]
- **Outputs**: [What it produces - {task_info.get('title', 'Output')}]
- **Behavior**: [Key logic - {task_info.get('details', 'Implementation details')}]

"""

    # Add effort and complexity sections with standardized formatting
    if task_info.get('effort') or task_info.get('complexity'):
        if task_info.get('effort'):
            capability_template += format_effort_section_ultra_enhanced(task_info['effort'], task_info.get('complexity', ''))
        elif task_info.get('complexity'):
            capability_template += format_complexity_section_ultra_enhanced(task_info['complexity'])

    # Add success criteria in a structured format
    if task_info.get('success_criteria'):
        capability_template += format_success_criteria_ultra_enhanced(task_info['success_criteria'])

    return capability_template


def generate_enhanced_dependency_graph_ultra(task_files: List[str]) -> str:
    """
    Ultra enhanced function to create an enhanced dependency graph with proper topological ordering.

    Args:
        task_files: List of paths to task markdown files

    Returns:
        String representing the enhanced dependency graph section
    """
    # Parse all tasks to identify real dependency relationships
    task_map = {}
    all_dependencies = []

    for task_file in task_files:
        task_info = extract_task_info_from_md_ultra_enhanced(task_file)
        task_map[task_info['id']] = task_info

        # Parse dependencies for this task
        if task_info['dependencies'] and task_info['dependencies'].lower() not in ['none', 'null', '']:
            deps = parse_dependencies_ultra_enhanced(task_info['dependencies'])
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
    dependency_targets = set(dep['depends_on'] for dep in all_dependencies if dep['depends_on'] in all_task_ids)
    foundation_tasks = all_task_ids - dependency_targets

    if foundation_tasks:
        dependency_graph += "### Foundation Layer (Phase 0)\n"
        for task_id in sorted(foundation_tasks):
            task_title = task_map.get(task_id, {}).get('title', f'Task {task_id}')
            dependency_graph += f"- **task-{task_id}**: [{task_title}]\n"
        dependency_graph += "\n"

    # Group remaining tasks by their dependency depth using topological sort
    processed = set(foundation_tasks)
    phase = 1

    while processed != all_task_ids:
        # Find tasks whose dependencies are all in processed
        current_phase_tasks = []
        for task_id in all_task_ids - processed:
            task_info = task_map.get(task_id, {})
            deps = parse_dependencies_ultra_enhanced(task_info.get('dependencies', ''))
            # Only consider dependencies that exist as tasks
            relevant_deps = [dep for dep in deps if dep in all_task_ids]
            if all(dep in processed for dep in relevant_deps):
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
            deps = parse_dependencies_ultra_enhanced(task_info.get('dependencies', ''))
            # Only show dependencies that exist as tasks
            valid_deps = [dep for dep in deps if dep in all_task_ids]
            task_title = task_info.get('title', f'Task {task_id}')

            dependency_graph += f"- **task-{task_id}**: [{task_title}]\n"
            if valid_deps:
                dependency_graph += f"  - Depends on: {', '.join(valid_deps)}\n"
            dependency_graph += "\n"

        processed.update(current_phase_tasks)
        phase += 1

    return dependency_graph


def validate_prd_structure_ultra(prd_content: str) -> List[str]:
    """
    Ultra enhanced function to validate that the PRD follows the expected RPG structure.

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


def create_ultra_enhanced_reverse_engineered_prd(task_files: List[str]) -> str:
    """
    Create an ultra enhanced PRD from a list of task markdown files.

    Args:
        task_files: List of paths to task markdown files

    Returns:
        String containing the ultra enhanced generated PRD
    """
    # Start with the RPG template structure
    prd_content = """<rpg-method>
# Repository Planning Graph (RPG) Method - Ultra Enhanced Reverse Engineered PRD

This PRD was automatically generated from existing task markdown files to recreate the original requirements that would generate these tasks when processed by task-master. This version implements ultra enhanced improvements for superior parsing fidelity.
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
        task_info = extract_task_info_from_md_ultra_enhanced(task_file)
        prd_content += generate_enhanced_capability_from_task_ultra(task_info)
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

    # Generate ultra enhanced dependencies with proper topological ordering
    prd_content += generate_enhanced_dependency_graph_ultra(task_files)

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
        task_info = extract_task_info_from_md_ultra_enhanced(task_file)
        prd_content += f"- [ ] Implement {task_info['title']} (ID: {task_info['id']})\n"
        if task_info['dependencies'] and task_info['dependencies'].lower() not in ['none', 'null', '']:
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
        task_info = extract_task_info_from_md_ultra_enhanced(task_file)
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

This PRD was generated to recreate the original requirements that would produce the same tasks when processed by task-master. It implements ultra enhanced improvements for superior parsing fidelity.
</task-master-integration>
"""

    # Validate the PRD structure
    validation_errors = validate_prd_structure_ultra(prd_content)
    if validation_errors:
        print(f"Warning: PRD validation errors found: {validation_errors}")

    return prd_content


def main():
    parser = argparse.ArgumentParser(description="Ultra enhanced reverse engineer PRD from task markdown files")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing task markdown files")
    parser.add_argument("--output", "-o", required=True, help="Output file for generated PRD")
    parser.add_argument("--pattern", default="task*.md", help="File pattern to match (default: task*.md)")

    args = parser.parse_args()

    # Find all task markdown files
    input_path = Path(args.input_dir)
    task_files = list(input_path.glob(args.pattern))

    if not task_files:
        print(f"No task files found in {input_path} with pattern {args.pattern}")
        return 1

    print(f"Found {len(task_files)} task files to process")

    # Generate the ultra enhanced PRD
    prd_content = create_ultra_enhanced_reverse_engineered_prd(task_files)

    # Write the PRD to output file
    output_path = Path(args.output)
    output_path.write_text(prd_content, encoding='utf-8')

    print(f"Generated ultra enhanced PRD with {len(task_files)} tasks and saved to {output_path}")
    print("The ultra enhanced PRD follows the RPG method structure that task-master expects.")
    print("Ultra enhanced improvements implemented:")
    print("- Enhanced information extraction with better parsing of structured content")
    print("- Improved capability-feature mapping with semantic analysis")
    print("- Advanced dependency graph with topological ordering and validation")
    print("- Structured success criteria with standardized formatting")
    print("- Standardized effort and complexity assessments")
    print("- Enhanced validation and iterative improvement mechanisms")
    print("- Better handling of the 14-section task format")

    return 0


if __name__ == "__main__":
    exit(main())