#!/usr/bin/env python3
"""
Ultra Enhanced Task Markdown to JSON Converter
Improves fidelity in the PRD to task.json process by preserving more information
"""
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime


def extract_task_info_from_md_ultra_enhanced(file_path: str) -> dict:
    """
    Ultra enhanced function to extract comprehensive information from task markdown files.
    Handles both standard 14-section format and legacy formats with extended metadata.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    task = {
        "subtasks": [],
        "extended_metadata": {}
    }

    # Extract ID and title from header with multiple pattern support
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task['title'] = title_match.group(1).strip()

    # Extract ID from filename or content
    filename = Path(file_path).stem
    id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
    if id_match:
        task['id'] = id_match.group(1).replace('_', '.').replace('-', '.')
    else:
        # Try to extract from content if not in filename
        id_from_content = re.search(r'# Task\s+(?:ID:\s*)?(\d+(?:\.\d+)?)', content)
        if id_from_content:
            task['id'] = id_from_content.group(1)

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
            task[field] = match.group(1).strip()

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
                task['success_criteria'] = criteria_items
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
                                    task['subtasks'].append(subtask)
                else:
                    # If not in table format, just store the content
                    task[section_name] = section_content
            else:
                task[section_name] = section_content

    # If success criteria weren't found in structured format, look for them in other ways
    if 'success_criteria' not in task:
        # Look for checklist items anywhere in the content
        checklist_pattern = r'- \[.\]\s*(.+?)(?=\n- \[|\Z)'
        checklist_matches = re.findall(checklist_pattern, content)
        task['success_criteria'] = checklist_matches

    # Extract extended metadata from comments
    ext_meta_match = re.search(r'<!-- EXTENDED_METADATA\s*\n([\s\S]*?)\nEND_EXTENDED_METADATA -->', content)
    if ext_meta_match:
        ext_meta_content = ext_meta_match.group(1)
        # Parse the extended metadata
        for line in ext_meta_content.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                task['extended_metadata'][key.strip()] = value.strip()

    # If purpose wasn't found in structured format, try to extract from description
    if 'purpose' not in task:
        desc_match = re.search(r'\*\*Description:?\*\*\s*(.+?)(?:\n|$)', content)
        if desc_match:
            task['purpose'] = desc_match.group(1).strip()

    # If details weren't found in structured format, try to extract from main content
    if 'details' not in task:
        # Look for content after the main header but before the first ## section
        header_end = content.find('\n\n')  # First double newline after header
        if header_end != -1:
            after_header = content[header_end:]
            # Look for first paragraph before any ## sections
            para_match = re.search(r'^([^\n]+\n?)+?(?=\n## |\n---|\n\*\*|\Z)', after_header, re.MULTILINE)
            if para_match:
                task['details'] = para_match.group(0).strip()

    return task


def map_to_tasks_json_format_ultra(task: dict) -> dict:
    """
    Maps the parsed task to the final tasks.json structure with enhanced fidelity.
    """
    # Map main task with all available information
    json_task = {
        "id": task.get("id"),
        "title": task.get("title", ""),
        "description": task.get("purpose", "") or task.get("description", ""),
        "status": task.get("status", "pending"),
        "priority": task.get("priority", "medium"),
        "dependencies": [],
        "details": task.get("details", ""),
        "subtasks": [],
        "testStrategy": task.get("test_strategy", "") or task.get("testing_strategy", ""),
        "complexity": task.get("complexity", "0/10"),
        "effort": task.get("effort", "0 hours"),
        "updatedAt": datetime.now().isoformat(),
        "createdAt": datetime.now().isoformat(),
        "blocks": task.get("blocks", ""),
        "initiative": task.get("initiative", ""),
        "scope": task.get("scope", ""),
        "focus": task.get("focus", ""),
        "owner": task.get("owner", ""),
        "prerequisites": task.get("prerequisites", ""),
        "specification_details": task.get("specification_details", ""),
        "implementation_guide": task.get("implementation_guide", ""),
        "configuration_params": task.get("configuration_params", ""),
        "performance_targets": task.get("performance_targets", ""),
        "common_gotchas": task.get("common_gotchas", ""),
        "integration_checkpoint": task.get("integration_checkpoint", ""),
        "done_definition": task.get("done_definition", ""),
        "next_steps": task.get("next_steps", ""),
        "extended_metadata": task.get("extended_metadata", {}),
    }

    # Parse dependencies string into array
    if task.get("dependencies"):
        deps_str = task["dependencies"]
        if deps_str.lower() not in ['none', 'null', '']:
            # Handle various formats: comma-separated, space-separated, "and" separated
            deps = re.split(r'[,\s]+| and ', deps_str)
            deps = [dep.strip() for dep in deps if dep.strip()]
            json_task["dependencies"] = deps

    # Map subtasks with enhanced information
    for sub in task.get("subtasks", []):
        json_subtask = {
            "id": sub.get("id"),
            "title": sub.get("title", ""),
            "description": sub.get("description", ""),
            "dependencies": sub.get("dependencies", []),
            "details": sub.get("details", ""),
            "status": sub.get("status", "pending"),
            "parentId": sub.get("parentId", task.get("id")),
            "effort": sub.get("effort", ""),
        }
        json_task["subtasks"].append(json_subtask)

    # Add success criteria as specific requirements
    if task.get("success_criteria"):
        json_task["success_criteria"] = task["success_criteria"]

    return {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "Generated from task markdown with ultra-enhanced fidelity.",
            "lastUpdated": datetime.now().isoformat(),
            "tasks": [json_task]
        }
    }


def main():
    """Main function with ultra-enhanced fidelity."""
    parser = argparse.ArgumentParser(description="Ultra enhanced converter: Converts task markdown to JSON with maximum fidelity preservation.")
    parser.add_argument("markdown_file", help="Path to the task markdown file.")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    filepath = Path(args.markdown_file)
    if not filepath.is_file():
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)

    try:
        # Use ultra-enhanced parsing
        parsed_task = extract_task_info_from_md_ultra_enhanced(str(filepath))
        tasks_json_structure = map_to_tasks_json_format_ultra(parsed_task)
        
        json_output = json.dumps(tasks_json_structure, indent=2)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"Ultra-enhanced task JSON saved to {args.output}")
        else:
            print(json_output)
            
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()