#!/usr/bin/env python3
"""
Task Structure Standardizer
Updates existing task files to follow the 14-section standard format
"""

import argparse
import re
from pathlib import Path
from typing import Dict, Any, List
import json


def extract_task_info_from_md_enhanced(file_path: str) -> Dict[str, Any]:
    """
    Enhanced function to extract comprehensive information from task markdown files.
    Handles both standard format and extended metadata in comments.
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
        'extended_metadata': {},  # For capturing metadata from comments
    }

    # Extract title from header with better pattern matching
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['title'] = title_match.group(1).strip()

    # Extract ID from filename or content
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
        'focus': r'\*\*Focus:?\*\*\s*(.+?)(?:\n|$)',
        'owner': r'\*\*Owner:?\*\*\s*(.+?)(?:\n|$)',
    }

    for field, pattern in metadata_patterns.items():
        match = re.search(pattern, content)
        if match:
            task_info[field] = match.group(1).strip()

    # Extract purpose with better section detection
    purpose_match = re.search(r'## Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if purpose_match:
        task_info['purpose'] = purpose_match.group(1).strip()
    else:
        # Look for description field as alternative
        desc_match = re.search(r'\*\*Description:?\*\*\s*(.+?)(?:\n|$)', content)
        if desc_match:
            task_info['purpose'] = desc_match.group(1).strip()

    # Extract details with better section detection
    details_match = re.search(r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if details_match:
        task_info['details'] = details_match.group(1).strip()
    else:
        # Look for details in the main content after the header
        header_end = content.find('\n\n')  # First double newline after header
        if header_end != -1:
            # Look for content after the header but before the first section
            after_header = content[header_end:]
            # Extract first paragraph as details if no ## Details section
            para_match = re.search(r'^([^\n]+\n?)+?(?=\n## |\n---|\n\*\*|\Z)', after_header, re.MULTILINE)
            if para_match:
                task_info['details'] = para_match.group(0).strip()

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
    else:
        # Look for success criteria in extended metadata
        ext_meta_match = re.search(r'successCriteria:\s*\n((?:\s*- .+\n?)*)', content)
        if ext_meta_match:
            raw_criteria = ext_meta_match.group(1)
            # Extract criteria from the extended metadata format
            criteria_from_meta = re.findall(r'- (.+)', raw_criteria)
            task_info['success_criteria'] = criteria_from_meta

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

    return task_info


def convert_to_standard_format(task_info: Dict[str, Any]) -> str:
    """
    Convert task information to the 14-section standard format.
    """
    # Format success criteria as checklist
    success_criteria_str = ""
    if task_info['success_criteria']:
        success_criteria_str = "## Success Criteria\n\n"
        for criterion in task_info['success_criteria']:
            success_criteria_str += f"- [ ] {criterion}\n"
        success_criteria_str += "\n"
    
    # Format subtasks if they exist
    subtasks_str = ""
    if task_info['subtasks']:
        subtasks_str = "## Sub-subtasks Breakdown\n\n"
        for subtask in task_info['subtasks']:
            subtasks_str += f"### {subtask.get('id', 'N/A')}: {subtask.get('title', 'N/A')}\n"
            subtasks_str += f"- **Status**: {subtask.get('status', 'N/A')}\n\n"
    
    # Format prerequisites
    prereq_str = f"## Prerequisites & Dependencies\n\n### Required Before Starting\n"
    if task_info['dependencies'] and task_info['dependencies'].lower() != 'none':
        prereq_str += f"- [ ] Dependencies: {task_info['dependencies']}\n"
    else:
        prereq_str += "- [ ] No external dependencies\n"
    prereq_str += "\n"
    
    # Format specification details
    spec_str = f"## Specification Details\n\n### Task Interface\n- **ID**: {task_info['id']}\n"
    spec_str += f"- **Title**: {task_info['title']}\n"
    spec_str += f"- **Status**: {task_info['status']}\n"
    spec_str += f"- **Priority**: {task_info['priority']}\n"
    if task_info['effort']:
        spec_str += f"- **Effort**: {task_info['effort']}\n"
    if task_info['complexity']:
        spec_str += f"- **Complexity**: {task_info['complexity']}\n"
    spec_str += "\n"
    
    # Format implementation guide
    impl_str = f"## Implementation Guide\n\n"
    if task_info['details']:
        impl_str += f"{task_info['details']}\n\n"
    else:
        impl_str += "Implementation details to be filled in.\n\n"
    
    # Format configuration parameters
    config_str = f"## Configuration Parameters\n\n"
    config_str += "# No specific configuration parameters defined\n\n"
    
    # Format performance targets
    perf_str = f"## Performance Targets\n\n"
    perf_str += "# Performance targets to be defined based on requirements\n\n"
    
    # Format testing strategy
    test_str = f"## Testing Strategy\n\n"
    if task_info['test_strategy']:
        test_str += f"{task_info['test_strategy']}\n\n"
    else:
        test_str += "# Testing strategy to be defined\n\n"
    
    # Format gotchas
    gotchas_str = f"## Common Gotchas & Solutions\n\n"
    gotchas_str += "# Common issues and solutions to be documented\n\n"
    
    # Format integration checkpoint
    integration_str = f"## Integration Checkpoint\n\n"
    integration_str += "# Criteria for moving to next phase\n\n"
    
    # Format done definition
    done_str = f"## Done Definition\n\n"
    done_str += "# Complete when all success criteria are checked\n\n"
    
    # Format next steps
    next_str = f"## Next Steps\n\n"
    if task_info['blocks']:
        next_str += f"- Unblocks: {task_info['blocks']}\n"
    next_str += "# Additional next steps to be defined\n\n"
    
    # Construct the full task in standard format
    standard_task = f"""# Task {task_info['id']}: {task_info['title']}

**Status:** {task_info['status'] or 'Not Started'}
**Priority:** {task_info['priority'] or 'Medium'}
**Effort:** {task_info['effort'] or 'TBD'}
**Complexity:** {task_info['complexity'] or 'TBD'}
**Dependencies:** {task_info['dependencies'] or 'None'}

---

## Overview/Purpose
{task_info['purpose'] or 'Purpose to be defined'}

{success_criteria_str}{prereq_str}{subtasks_str}{spec_str}{impl_str}{config_str}{perf_str}{test_str}{gotchas_str}{integration_str}{done_str}{next_str}"""

    return standard_task


def standardize_task_file(input_file: str, output_file: str):
    """
    Standardize a single task file to the 14-section format.
    """
    print(f"Processing {input_file} -> {output_file}")
    
    # Extract information from the existing task file
    task_info = extract_task_info_from_md_enhanced(input_file)
    
    # Convert to standard format
    standardized_content = convert_to_standard_format(task_info)
    
    # Write the standardized content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(standardized_content)
    
    print(f"Successfully standardized {input_file}")


def main():
    parser = argparse.ArgumentParser(description="Standardize task files to 14-section format")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing task markdown files")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory for standardized task files")
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

    print(f"Found {len(task_files)} task files to standardize")

    # Process each task file
    for task_file in task_files:
        # Create output filename by adding '_standardized' suffix
        output_file = output_path / f"{task_file.stem}_standardized.md"
        standardize_task_file(str(task_file), str(output_file))

    print(f"Successfully standardized {len(task_files)} task files")
    print(f"Standardized files saved to {output_path}")

    return 0


if __name__ == "__main__":
    exit(main())