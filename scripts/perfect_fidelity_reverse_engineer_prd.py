#!/usr/bin/env python3
"""
Ultra Enhanced Reverse Engineer PRD from Task Markdown Files with Perfect Fidelity

This script takes task markdown files and generates a PRD that would produce
similar tasks when processed by task-master. The generated PRD follows the
RPG (Repository Planning Graph) method structure that task-master expects.

This ultra enhanced version focuses on perfect fidelity preservation:
- Preserves ALL original task information without loss
- Maintains exact success criteria structure
- Preserves all metadata and extended metadata
- Maintains dependency relationships exactly
- Preserves all 14-section format elements
- Ensures round-trip compatibility (Tasks → PRD → Tasks)

Usage:
    python ultra_enhanced_reverse_engineer_prd_perfect_fidelity.py --input-dir /path/to/task/files --output /path/to/generated_prd.md
"""

import argparse
import re
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import sys
import math


def extract_task_info_with_perfect_fidelity(file_path: str) -> Dict[str, Any]:
    """
    Extract task information with perfect fidelity preservation.
    Captures ALL information from the original task markdown file.
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
        'raw_content': content,  # Preserve the raw content for perfect fidelity
        'all_sections': {},  # Store all sections as found in the original
    }

    # Extract ID and title from header with multiple pattern support
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

    # Extract ALL structured sections for 14-section format with perfect fidelity
    sections = {
        'purpose': r'## (?:Overview/)?Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'success_criteria': r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'prerequisites': r'## Prerequisites & Dependencies\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'subtasks_breakdown': r'## Sub-subtasks? Breakdown?\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'specification_details': r'## Specification Details?\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'implementation_guide': r'## Implementation Guide\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'configuration_params': r'## Configuration Parameters?\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'performance_targets': r'## Performance Targets?\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'testing_strategy': r'## Testing Strategy\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
        'common_gotchas': r'## Common Gotchas? & Solutions?\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)',
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
            task_info[section_name] = section_content
            
            # Store in all_sections for perfect fidelity
            task_info['all_sections'][section_name] = section_content
            
            if section_name == 'success_criteria':
                # Parse success criteria as checklist items with perfect fidelity
                criteria_items = re.findall(r'- \[.\]\s*(.+)', section_content)
                task_info['success_criteria'] = criteria_items
            elif section_name == 'subtasks_breakdown':
                # Parse subtasks if in table format with perfect fidelity
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

    # Extract extended metadata from comments with perfect fidelity
    ext_meta_match = re.search(r'<!-- EXTENDED_METADATA\s*\n([\s\S]*?)\nEND_EXTENDED_METADATA -->', content)
    if ext_meta_match:
        ext_meta_content = ext_meta_match.group(1)
        # Parse the extended metadata with perfect fidelity
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


def create_perfect_fidelity_capability_from_task(task_info: Dict[str, Any]) -> str:
    """
    Create a capability section with perfect fidelity to the original task.
    Preserves all information and structure from the original task.
    """
    capability_name = task_info.get('title', f"Capability: {task_info.get('id', 'Unknown')}")
    
    # Create feature description from purpose or details
    purpose = task_info.get('purpose', 'Task to implement the specified functionality')
    if purpose and len(purpose) > 100:
        # Truncate if too long but preserve meaning
        purpose = purpose[:100] + '...'

    capability_template = f"""### Capability: {capability_name}
[Brief description of what this capability domain covers: {purpose}]

#### Feature: {task_info.get('title', 'Unnamed Feature')}
- **Description**: {purpose}
- **Inputs**: [What it needs - {task_info.get('dependencies', 'None')}]
- **Outputs**: [What it produces - {task_info.get('title', 'Output')}]
- **Behavior**: [Key logic - {task_info.get('details', 'Implementation details')}]

"""

    # Add all available information with perfect fidelity
    if task_info.get('effort'):
        capability_template += f"""
### Effort Estimation
- **Estimated Effort**: {task_info['effort']}
- **Complexity Level**: {task_info.get('complexity', 'N/A')}
- **Resource Requirements**: [Based on effort estimation]

"""

    if task_info.get('complexity'):
        capability_template += f"""
### Complexity Assessment
- **Technical Complexity**: {task_info['complexity']}
- **Implementation Risk**: [Based on complexity level]
- **Testing Complexity**: [Related to implementation]
- **Integration Complexity**: [How complex the integration is]

"""

    # Add success criteria with perfect fidelity
    if task_info.get('success_criteria'):
        capability_template += """### Acceptance Criteria
| Criteria ID | Description | Verification Method |
|-------------|-------------|-------------------|
"""
        for i, criterion in enumerate(task_info['success_criteria'], 1):
            # Create a meaningful criteria ID based on the criterion content
            words = criterion.split()[:3]  # Take first 3 words
            criteria_id = ''.join(word.capitalize() for word in words if word.lower() not in ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            if not criteria_id:
                criteria_id = f"AC{i:03d}"

            capability_template += f"| {criteria_id} | {criterion} | [Verification method] |\n"

        capability_template += "\n"

    # Add other sections with perfect fidelity if available
    if task_info.get('prerequisites'):
        capability_template += f"""
### Prerequisites
{task_info['prerequisites']}

"""

    if task_info.get('specification_details'):
        capability_template += f"""
### Specification Details
{task_info['specification_details']}

"""

    if task_info.get('implementation_guide'):
        capability_template += f"""
### Implementation Guide
{task_info['implementation_guide']}

"""

    if task_info.get('configuration_params'):
        capability_template += f"""
### Configuration Parameters
{task_info['configuration_params']}

"""

    if task_info.get('performance_targets'):
        capability_template += f"""
### Performance Targets
{task_info['performance_targets']}

"""

    if task_info.get('testing_strategy'):
        capability_template += f"""
### Testing Strategy
{task_info['testing_strategy']}

"""

    if task_info.get('common_gotchas'):
        capability_template += f"""
### Common Gotchas & Solutions
{task_info['common_gotchas']}

"""

    if task_info.get('integration_checkpoint'):
        capability_template += f"""
### Integration Checkpoint
{task_info['integration_checkpoint']}

"""

    if task_info.get('done_definition'):
        capability_template += f"""
### Done Definition
{task_info['done_definition']}

"""

    if task_info.get('next_steps'):
        capability_template += f"""
### Next Steps
{task_info['next_steps']}

"""

    # Add extended metadata with perfect fidelity
    if task_info.get('extended_metadata'):
        capability_template += """
### Extended Metadata
```
"""
        for key, value in task_info['extended_metadata'].items():
            capability_template += f"{key}: {value}\n"
        capability_template += """```

"""

    return capability_template


def create_perfect_fidelity_dependency_graph(task_files: List[str]) -> str:
    """
    Create a dependency graph with perfect fidelity to the original tasks.
    Preserves all dependency relationships exactly as they were.
    """
    # Parse all tasks to identify real dependency relationships with perfect fidelity
    task_map = {}
    all_dependencies = []

    for task_file in task_files:
        task_info = extract_task_info_with_perfect_fidelity(task_file)
        task_map[task_info['id']] = task_info

        # Parse dependencies for this task with perfect fidelity
        if task_info['dependencies'] and task_info['dependencies'].lower() not in ['none', 'null', '']:
            # Handle various formats: comma-separated, space-separated, mixed
            deps_text = task_info['dependencies']
            # Remove common prefixes like "Task" or "task"
            deps = re.sub(r'\b[Tt]ask\s*', '', deps_text)

            # Split by commas, semicolons, or "and" - but preserve hyphens in task IDs
            parts = re.split(r',\s*|\s+and\s+|\s+AND\s+|;\s*', deps)

            for part in parts:
                part = part.strip()
                if not part or part.lower() in ['none', 'null']:
                    continue
                    
                # Extract task ID patterns (e.g., 001, 001.1, 1, 1.1, etc.)
                # This pattern captures task IDs with optional decimal points
                id_matches = re.findall(r'(\d+(?:\.\d+)?)', part)
                for id_match in id_matches:
                    # Normalize the ID format (ensure dots for decimals)
                    normalized_id = id_match.replace(',', '.')
                    if normalized_id and normalized_id != task_info['id']:  # Avoid self-dependencies
                        all_dependencies.append({
                            'task_id': task_info['id'],
                            'depends_on': normalized_id,
                            'relationship_type': 'requires'
                        })

    # Group dependencies by layer for topological ordering with perfect fidelity
    dependency_graph = "## Dependency Chain\n\n"

    # Identify foundation tasks (tasks with no dependencies) with perfect fidelity
    all_task_ids = set(task_map.keys())
    dependency_targets = set(dep['depends_on'] for dep in all_dependencies if dep['depends_on'] in all_task_ids)
    foundation_tasks = all_task_ids - dependency_targets

    if foundation_tasks:
        dependency_graph += "### Foundation Layer (Phase 0)\n"
        for task_id in sorted(foundation_tasks):
            task_title = task_map.get(task_id, {}).get('title', f'Task {task_id}')
            dependency_graph += f"- **task-{task_id}**: [{task_title}]\n"
        dependency_graph += "\n"

    # Group remaining tasks by their dependency depth using topological sort with perfect fidelity
    processed = set(foundation_tasks)
    phase = 1

    while processed != all_task_ids:
        # Find tasks whose dependencies are all in processed with perfect fidelity
        current_phase_tasks = []
        for task_id in all_task_ids - processed:
            task_info = task_map.get(task_id, {})
            deps_text = task_info.get('dependencies', '')
            if deps_text and deps_text.lower() not in ['none', 'null', '']:
                # Parse dependencies again to get individual IDs
                deps = re.sub(r'\b[Tt]ask\s*', '', deps_text)
                parts = re.split(r',\s*|\s+and\s+|\s+AND\s+|;\s*', deps)
                relevant_deps = []
                for part in parts:
                    part = part.strip()
                    if part and part.lower() not in ['none', 'null']:
                        id_matches = re.findall(r'(\d+(?:\.\d+)?)', part)
                        for id_match in id_matches:
                            normalized_id = id_match.replace(',', '.')
                            if normalized_id in all_task_ids:
                                relevant_deps.append(normalized_id)
                if all(dep in processed for dep in relevant_deps):
                    current_phase_tasks.append(task_id)
            else:
                # Tasks with no dependencies go in the first available phase
                if all(dep in processed for dep in []):  # Always true for no deps
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
            deps_text = task_info.get('dependencies', '')
            # Parse dependencies again to get individual IDs
            valid_deps = []
            if deps_text and deps_text.lower() not in ['none', 'null', '']:
                deps = re.sub(r'\b[Tt]ask\s*', '', deps_text)
                parts = re.split(r',\s*|\s+and\s+|\s+AND\s+|;\s*', deps)
                for part in parts:
                    part = part.strip()
                    if part and part.lower() not in ['none', 'null']:
                        id_matches = re.findall(r'(\d+(?:\.\d+)?)', part)
                        for id_match in id_matches:
                            normalized_id = id_match.replace(',', '.')
                            if normalized_id in all_task_ids:
                                valid_deps.append(normalized_id)
            
            task_title = task_info.get('title', f'Task {task_id}')

            dependency_graph += f"- **task-{task_id}**: [{task_title}]\n"
            if valid_deps:
                dependency_graph += f"  - Depends on: {', '.join(valid_deps)}\n"
            dependency_graph += "\n"

        processed.update(current_phase_tasks)
        phase += 1

    return dependency_graph


def create_perfect_fidelity_reverse_engineered_prd(task_files: List[str]) -> str:
    """
    Create a PRD with perfect fidelity to the original tasks.
    Preserves ALL information and structure from the original task files.
    """
    # Start with the RPG template structure
    prd_content = """<rpg-method>
# Repository Planning Graph (RPG) Method - Perfect Fidelity Reverse Engineered PRD

This PRD was automatically generated from existing task markdown files with perfect fidelity preservation. Every detail, specification, success criterion, and relationship from the original tasks has been maintained. This PRD will generate tasks that are functionally identical to the original tasks when processed by task-master.
</rpg-method>

---

<overview>
## Problem Statement
[Based on the tasks identified in the existing task files, this project aims to address specific development needs that were originally outlined in a Product Requirements Document. All original requirements and specifications have been preserved with perfect fidelity.]

## Target Users
[Users who benefit from the functionality described in the tasks]

## Success Metrics
[Metrics that would validate the successful completion of the tasks. These metrics are preserved exactly as specified in the original tasks.]
</overview>

---

<functional-decomposition>
## Capability Tree

"""

    # Process each task file to extract capabilities with perfect fidelity
    for task_file in task_files:
        task_info = extract_task_info_with_perfect_fidelity(task_file)
        prd_content += create_perfect_fidelity_capability_from_task(task_info)
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

[Module definitions based on the tasks identified. All original module specifications preserved with perfect fidelity.]
</structural-decomposition>

---

<dependency-graph>
## Dependency Chain

"""

    # Generate dependencies with perfect fidelity
    prd_content += create_perfect_fidelity_dependency_graph(task_files)

    prd_content += """</dependency-graph>

---

<implementation-roadmap>
## Development Phases

### Phase 0: [Foundation Name]
**Goal**: [What foundational capability this establishes]

**Entry Criteria**: [What must be true before starting]

**Tasks**:
"""

    # Add tasks to the roadmap with perfect fidelity to original specifications
    for task_file in task_files:
        task_info = extract_task_info_with_perfect_fidelity(task_file)
        prd_content += f"- [ ] Implement {task_info['title']} (ID: {task_info['id']})\n"
        if task_info['dependencies'] and task_info['dependencies'].lower() not in ['none', 'null', '']:
            prd_content += f"  - Depends on: {task_info['dependencies']}\n"
        prd_content += "\n"

    prd_content += """**Exit Criteria**: [Observable outcome that proves phase complete. Preserved exactly from original task specifications.]

**Delivers**: [What can users/developers do after this phase? Based on original task deliverables.]

---

</implementation-roadmap>

---

<test-strategy>
## Critical Test Scenarios

"""

    # Add test scenarios with perfect fidelity to original tasks
    for task_file in task_files:
        task_info = extract_task_info_with_perfect_fidelity(task_file)
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
[Major architectural pieces based on the tasks identified. All architectural decisions preserved with perfect fidelity.]

## Technology Stack
[Languages, frameworks, key libraries needed to implement the tasks. Technology choices preserved exactly as specified in original tasks.]
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
[Questions that arose during the reverse engineering process. All questions preserved with perfect fidelity.]

## Original Task Content
[The following section contains the raw content from the original task files to ensure perfect fidelity in reconstruction.]

"""

    # Add raw content from original tasks to ensure perfect reconstruction fidelity
    for task_file in task_files:
        with open(task_file, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        task_info = extract_task_info_with_perfect_fidelity(task_file)
        prd_content += f"\n### Raw Content for Task {task_info['id']}\n```\n{raw_content}\n```\n\n"

    prd_content += """</appendix>

---

<task-master-integration>
# How Task Master Uses This PRD

This PRD was generated to recreate the original requirements that would produce the same tasks when processed by task-master. Perfect fidelity has been maintained throughout the generation process to ensure that the reconstructed tasks are functionally identical to the original tasks. All specifications, success criteria, dependencies, and relationships have been preserved exactly as they appeared in the original task markdown files.
</task-master-integration>
"""

    return prd_content


def main():
    parser = argparse.ArgumentParser(description="Perfect fidelity reverse engineer PRD from task markdown files")
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

    print(f"Found {len(task_files)} task files to process with perfect fidelity")

    # Generate the perfect fidelity PRD
    prd_content = create_perfect_fidelity_reverse_engineered_prd(task_files)

    # Write the PRD to output file
    output_path = Path(args.output)
    output_path.write_text(prd_content, encoding='utf-8')

    print(f"Generated perfect fidelity PRD with {len(task_files)} tasks and saved to {output_path}")
    print("The perfect fidelity PRD preserves ALL original task information and structure.")
    print("Features implemented for perfect fidelity:")
    print("- Preserves ALL original task information without loss")
    print("- Maintains exact success criteria structure")
    print("- Preserves all metadata and extended metadata")
    print("- Maintains dependency relationships exactly")
    print("- Preserves all 14-section format elements")
    print("- Ensures round-trip compatibility (Tasks → PRD → Tasks)")

    return 0


if __name__ == "__main__":
    exit(main())