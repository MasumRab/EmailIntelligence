#!/usr/bin/env python3
"""
Enhanced Task Specification Improver
Improves all task specifications to maximize PRD accuracy by ensuring consistent structure,
clear success criteria, and proper formatting for optimal parsing.
"""

import argparse
import re
from pathlib import Path
from typing import Dict, Any, List
import json


def improve_task_specification(content: str, file_path: str) -> str:
    """
    Improve a single task specification to maximize PRD accuracy.
    """
    # Extract current information
    improved_content = content
    
    # 1. Parse the existing task structure
    parsed_task = parse_task_structure(improved_content)
    
    # 2. Reconstruct the task with proper structure
    improved_content = reconstruct_task_with_proper_structure(parsed_task)
    
    return improved_content


def parse_task_structure(content: str) -> Dict[str, Any]:
    """
    Parse the task structure to extract all components.
    """
    task_data = {
        'header': '',
        'title': '',
        'id': '',
        'status': '',
        'priority': '',
        'dependencies': '',
        'description': '',
        'details': '',
        'test_strategy': '',
        'subtasks': [],
        'extended_metadata': {},
        'other_sections': {}
    }
    
    # Extract header information
    header_match = re.search(r'^(#.*)', content, re.MULTILINE)
    if header_match:
        task_data['header'] = header_match.group(1)
        
        # Extract ID from header
        id_match = re.search(r'Task ID: (\d+)', task_data['header'])
        if id_match:
            task_data['id'] = id_match.group(1)
    
    # Extract metadata fields
    metadata_patterns = {
        'title': r'\*\*Title:\*\*\s*(.+)',
        'status': r'\*\*Status:\*\*\s*(.+)',
        'priority': r'\*\*Priority:\*\*\s*(.+)',
        'dependencies': r'\*\*Dependencies:\*\*\s*(.+)',
        'description': r'\*\*Description:\*\*\s*(.+?)(?=\n\*\*|\n##|\Z)'
    }
    
    for field, pattern in metadata_patterns.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            task_data[field] = match.group(1).strip()
    
    # Extract details section
    details_match = re.search(r'## Details\s*\n+([\s\S]*?)(?=\n## |\n---|\Z)', content)
    if details_match:
        task_data['details'] = details_match.group(1).strip()
    
    # Extract test strategy
    test_match = re.search(r'## Test Strategy\s*\n+([\s\S]*?)(?=\n## |\n---|\Z)', content)
    if test_match:
        task_data['test_strategy'] = test_match.group(1).strip()
    
    # Extract subtasks
    subtask_pattern = r'(### \d+\.\d+\. .+?\n)([\s\S]*?)(?=\n### \d+\.\d+\. |\n---|\Z)'
    subtask_matches = list(re.finditer(subtask_pattern, content))
    
    for match in subtask_matches:
        header = match.group(1).strip()
        body = match.group(2).strip()
        
        subtask_data = {
            'header': header,
            'body': body,
            'status': '',
            'dependencies': ''
        }
        
        # Extract subtask metadata
        status_match = re.search(r'\*\*Status:\*\*\s*(.+)', body)
        if status_match:
            subtask_data['status'] = status_match.group(1).strip()
        
        deps_match = re.search(r'\*\*Dependencies:\*\*\s*(.+)', body)
        if deps_match:
            subtask_data['dependencies'] = deps_match.group(1).strip()
        
        task_data['subtasks'].append(subtask_data)
    
    # Extract extended metadata
    ext_meta_match = re.search(r'<!-- EXTENDED_METADATA\s*\n([\s\S]*?)\nEND_EXTENDED_METADATA -->', content)
    if ext_meta_match:
        ext_meta_content = ext_meta_match.group(1)
        # Parse the extended metadata
        for line in ext_meta_content.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                task_data['extended_metadata'][key.strip()] = value.strip()
    
    return task_data


def reconstruct_task_with_proper_structure(task_data: Dict[str, Any]) -> str:
    """
    Reconstruct the task with proper structure following the 14-section standard.
    """
    # Build the header
    header_section = f"{task_data['header']}\n\n"
    
    # Add metadata in proper format
    metadata_section = f"""**Status:** {task_data.get('status', 'pending')}
**Priority:** {task_data.get('priority', 'medium')}
**Dependencies:** {task_data.get('dependencies', 'None')}
**Effort:** {task_data['extended_metadata'].get('effort', 'TBD')}
**Complexity:** {task_data['extended_metadata'].get('complexity', 'TBD')}

"""
    
    # Add Overview/Purpose section
    purpose_content = task_data.get('description', task_data['extended_metadata'].get('focus', '[Purpose to be defined]'))
    if not purpose_content or purpose_content == '[Purpose to be defined]':
        purpose_content = task_data.get('details', '')[:200] + "..." if task_data.get('details') else '[Purpose to be defined]'
    
    overview_section = f"""## Overview/Purpose
{purpose_content}

"""
    
    # Add Success Criteria section
    success_criteria = task_data['extended_metadata'].get('successCriteria', '')
    success_criteria_section = "## Success Criteria\n\n"
    if success_criteria:
        # Parse the success criteria from extended metadata
        criteria_lines = success_criteria.split('\n')
        for line in criteria_lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Clean up the line and format as checklist
                clean_line = line.replace('- ', '').strip()
                if clean_line:
                    success_criteria_section += f"- [ ] {clean_line}\n"
    else:
        success_criteria_section += "- [ ] [Success criteria to be defined]\n"
    
    success_criteria_section += "\n"
    
    # Add Prerequisites & Dependencies section
    prerequisites_section = f"""## Prerequisites & Dependencies

### Required Before Starting
- [ ] {task_data.get('dependencies', 'No external dependencies')}

### Blocks (What This Task Unblocks)
- [ ] {task_data['extended_metadata'].get('blocks', 'None specified')}

### External Dependencies
- [ ] {task_data['extended_metadata'].get('dependencies', 'None')}

"""
    
    # Add Specification Details section
    spec_details_section = f"""## Specification Details

### Task Interface
- **ID**: {task_data.get('id', 'N/A')}
- **Title**: {task_data.get('title', 'N/A')}
- **Status**: {task_data.get('status', 'N/A')}
- **Priority**: {task_data.get('priority', 'N/A')}
- **Effort**: {task_data['extended_metadata'].get('effort', 'N/A')}
- **Complexity**: {task_data['extended_metadata'].get('complexity', 'N/A')}

"""
    
    # Add Implementation Guide section
    implementation_guide = f"""## Implementation Guide

{task_data.get('details', 'Implementation details to be filled in.')}

"""
    
    # Add Configuration Parameters section
    config_section = f"""## Configuration Parameters

- **Owner**: {task_data['extended_metadata'].get('owner', 'TBD')}
- **Initiative**: {task_data['extended_metadata'].get('initiative', 'TBD')}
- **Scope**: {task_data['extended_metadata'].get('scope', 'TBD')}
- **Focus**: {task_data['extended_metadata'].get('focus', 'TBD')}

"""
    
    # Add Performance Targets section
    perf_section = f"""## Performance Targets

- **Effort Range**: {task_data['extended_metadata'].get('effort', 'TBD')}
- **Complexity Level**: {task_data['extended_metadata'].get('complexity', 'TBD')}

"""
    
    # Add Testing Strategy section
    test_section = f"""## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
{task_data.get('test_strategy', 'No specific test strategy defined')}

"""
    
    # Add Common Gotchas & Solutions section
    gotchas_section = f"""## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

"""
    
    # Add Integration Checkpoint section
    integration_section = f"""## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

"""
    
    # Add Done Definition section
    done_section = f"""## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied

"""
    
    # Add Next Steps section
    next_section = f"""## Next Steps

- [ ] {task_data['extended_metadata'].get('blocks', 'No next steps specified')}
- [ ] Additional steps to be defined

"""
    
    # Add Sub-subtasks Breakdown section
    subtasks_section = "## Sub-subtasks Breakdown\n\n"
    for subtask in task_data.get('subtasks', []):
        subtasks_section += f"### {subtask.get('header', 'N/A')}\n"
        subtasks_section += f"- **Status**: {subtask.get('status', 'N/A')}\n"
        subtasks_section += f"- **Dependencies**: {subtask.get('dependencies', 'N/A')}\n\n"
    
    if not task_data.get('subtasks'):
        subtasks_section += "# No subtasks defined\n\n"
    
    # Add Extended Metadata section
    ext_meta_section = "\n<!-- EXTENDED_METADATA\n"
    for key, value in task_data.get('extended_metadata', {}).items():
        ext_meta_section += f"{key}: {value}\n"
    ext_meta_section += "END_EXTENDED_METADATA -->\n"
    
    # Combine all sections in the proper order
    complete_task = (
        header_section +
        metadata_section +
        overview_section +
        success_criteria_section +
        prerequisites_section +
        subtasks_section +
        spec_details_section +
        implementation_guide +
        config_section +
        perf_section +
        test_section +
        gotchas_section +
        integration_section +
        done_section +
        next_section +
        ext_meta_section
    )
    
    return complete_task


def main():
    parser = argparse.ArgumentParser(description="Enhanced task specification improver to maximize PRD accuracy")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing task markdown files")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory for improved task files")
    parser.add_argument("--pattern", default="task*.md", help="File pattern to match (default: task*.md)")
    parser.add_argument("--backup", action="store_true", help="Create backup of original files")

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

    print(f"Found {len(task_files)} task files to improve")

    # Process each task file
    for task_file in task_files:
        print(f"Improving {task_file.name}...")
        
        # Create backup if requested
        if args.backup:
            backup_path = output_path / f"{task_file.stem}_backup.md"
            with open(task_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
        
        # Read the task file
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Improve the task specification
        improved_content = improve_task_specification(content, str(task_file))
        
        # Write the improved content to the output file
        output_file = output_path / task_file.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(improved_content)
        
        print(f"  ✓ Improved {task_file.name} -> {output_file.name}")

    print(f"\nSuccessfully improved {len(task_files)} task files")
    print(f"Improved files saved to {output_path}")
    if args.backup:
        print(f"Backups saved in {output_path} with '_backup' suffix")

    return 0


if __name__ == "__main__":
    exit(main())