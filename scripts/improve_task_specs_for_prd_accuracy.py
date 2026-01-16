#!/usr/bin/env python3
"""
Task Specification Improver
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
    
    # 1. Ensure proper header structure
    improved_content = ensure_proper_header(improved_content)
    
    # 2. Improve success criteria formatting
    improved_content = improve_success_criteria_formatting(improved_content)
    
    # 3. Standardize metadata formatting
    improved_content = standardize_metadata(improved_content)
    
    # 4. Enhance description clarity
    improved_content = enhance_description_clarity(improved_content)
    
    # 5. Improve subtask structure
    improved_content = improve_subtask_structure(improved_content)
    
    # 6. Add missing sections if needed
    improved_content = add_missing_sections(improved_content)
    
    return improved_content


def ensure_proper_header(content: str) -> str:
    """
    Ensure the task has a proper header with all required metadata.
    """
    # Check if header exists in the expected format
    header_pattern = r'^# Task ID: \d+.*?$'
    header_match = re.search(header_pattern, content, re.MULTILINE)
    
    if not header_match:
        # If no proper header, try to create one from existing content
        title_match = re.search(r'\*\*Title:\*\*\s*(.+)', content)
        if title_match:
            title = title_match.group(1).strip()
            new_header = f"# Task ID: UNKNOWN\n\n**Title:** {title}\n\n**Status:** pending\n\n**Priority:** medium\n\n"
            # Find where the main content starts and insert header
            first_section = re.search(r'\*\*Description:\*\*|\*\*Details:\*\*', content)
            if first_section:
                content = new_header + content
            else:
                content = new_header + "**Description:** [Description needed]\n\n" + content
    
    return content


def improve_success_criteria_formatting(content: str) -> str:
    """
    Improve success criteria formatting to ensure they are clear and parseable.
    """
    # Find success criteria in extended metadata
    ext_meta_match = re.search(r'(<!-- EXTENDED_METADATA[\s\S]*?successCriteria:\n)([\s\S]*?)(\nEND_EXTENDED_METADATA -->)', content)
    if ext_meta_match:
        before_criteria = ext_meta_match.group(1)
        criteria_content = ext_meta_match.group(2)
        after_criteria = ext_meta_match.group(3)
        
        # Parse the current criteria
        criteria_lines = criteria_content.strip().split('\n')
        improved_criteria = []
        
        for line in criteria_lines:
            # Look for criteria that start with dashes or are indented
            if line.strip().startswith('- ') or line.strip().startswith('  - '):
                # Ensure proper formatting
                cleaned_line = line.strip()
                if not cleaned_line.startswith('- '):
                    cleaned_line = '- ' + cleaned_line[2:].strip() if len(cleaned_line) > 2 else cleaned_line
                improved_criteria.append(cleaned_line)
            elif line.strip():  # Non-empty line that doesn't start with dash
                improved_criteria.append('  ' + line.strip())  # Indent as part of previous item
        
        # Join the improved criteria
        improved_criteria_str = '\n'.join(improved_criteria)
        
        # Replace in the content
        content = content.replace(ext_meta_match.group(0), before_criteria + improved_criteria_str + after_criteria)
    
    # Also look for success criteria in main content (checklist format)
    success_criteria_section = re.search(r'(## Success Criteria\s*\n+)([\s\S]*?)(?=\n## |\n---|\Z)', content)
    if success_criteria_section:
        section_content = success_criteria_section.group(2)
        # Ensure checklist format
        checklist_items = re.findall(r'^([^-\n].*?)- \[.\] (.+)$', section_content, re.MULTILINE)
        if checklist_items:
            improved_section = ""
            for prefix, item in checklist_items:
                improved_section += f"{prefix.strip()}\n- [ ] {item}\n\n"
            content = content.replace(success_criteria_section.group(0), 
                                     success_criteria_section.group(1) + improved_section)
    
    return content


def standardize_metadata(content: str) -> str:
    """
    Standardize metadata fields to ensure consistent parsing.
    """
    # Ensure all required metadata fields exist
    required_fields = ['Status', 'Priority', 'Dependencies', 'Description']
    
    for field in required_fields:
        pattern = rf'\*\*{field}:?\*\*'
        if not re.search(pattern, content):
            if field == 'Status':
                content = f"**Status:** pending\n\n" + content
            elif field == 'Priority':
                content = re.sub(r'(\*\*Status:\*\*.*?\n)', r'\1**Priority:** medium\n\n', content)
            elif field == 'Dependencies':
                content = re.sub(r'(\*\*Priority:\*\*.*?\n)', r'\1**Dependencies:** None\n\n', content)
            elif field == 'Description':
                content = re.sub(r'(\*\*Dependencies:\*\*.*?\n)', r'\1**Description:** [Description needed]\n\n', content)
    
    return content


def enhance_description_clarity(content: str) -> str:
    """
    Enhance description clarity by ensuring it's specific and actionable.
    """
    # Look for the description field
    desc_match = re.search(r'(\*\*Description:\*\*\s*)(.*?)(?=\n\*\*|\n##|\n<!--|\Z)', content, re.DOTALL)
    if desc_match:
        description = desc_match.group(2).strip()
        
        # If description is generic, try to improve it
        if '[Description needed]' in description or 'task' in description.lower() or len(description) < 10:
            # Try to extract a better description from the details section
            details_match = re.search(r'## Details\s*\n+([\s\S]*?)(?=\n## |\n---|\Z)', content)
            if details_match:
                details = details_match.group(1).strip()
                # Use first sentence or first few words as description
                first_sentence = details.split('.')[0] if '.' in details else details[:100]
                if len(first_sentence) > 10:
                    new_desc = first_sentence.strip()
                    content = content.replace(desc_match.group(0), f"**Description:** {new_desc}\n\n")
    
    return content


def improve_subtask_structure(content: str) -> str:
    """
    Improve subtask structure to ensure consistency and clarity.
    """
    # Find subtask sections
    subtask_pattern = r'(### \d+\.\d+\. .+?\n)([\s\S]*?)(?=\n### \d+\.\d+\. |\n---|\Z)'
    subtask_matches = list(re.finditer(subtask_pattern, content))
    
    for match in reversed(subtask_matches):  # Process in reverse to maintain positions
        full_match = match.group(0)
        header = match.group(1)
        body = match.group(2)
        
        # Ensure each subtask has proper structure
        improved_body = body
        
        # Ensure status is present
        if '**Status:**' not in improved_body:
            improved_body = f"**Status:** pending\n\n" + improved_body
        
        # Ensure dependencies are present
        if '**Dependencies:**' not in improved_body:
            improved_body = re.sub(r'(\*\*Status:\*\*.*?\n)', r'\1**Dependencies:** None\n\n', improved_body)
        
        # Replace in content
        new_subtask = header + improved_body
        content = content.replace(full_match, new_subtask)
    
    return content


def add_missing_sections(content: str) -> str:
    """
    Add missing sections that are important for PRD accuracy.
    """
    # Add missing sections if they don't exist
    
    # Add Overview/Purpose section if missing
    if '## Overview/Purpose' not in content and '## Purpose' not in content:
        # Extract from description if available
        desc_match = re.search(r'\*\*Description:\*\*\s*(.+?)(?=\n\*\*|\n##|\Z)', content)
        description = desc_match.group(1).strip() if desc_match else "[Purpose to be defined]"
        
        purpose_section = f"\n## Overview/Purpose\n\n{description}\n\n"
        # Insert after the main header
        header_end = content.find('\n\n')  # First double newline after header
        if header_end != -1:
            content = content[:header_end] + purpose_section + content[header_end:]
    
    # Add Prerequisites & Dependencies section if missing
    if '## Prerequisites & Dependencies' not in content:
        prereq_section = f"\n## Prerequisites & Dependencies\n\n### Required Before Starting\n- [ ] No external dependencies\n\n### Blocks (What This Task Unblocks)\n- [ ] None specified\n\n"
        # Find a good place to insert (after purpose or details)
        if '## Overview/Purpose' in content:
            pos = content.find('## Overview/Purpose') + len('## Overview/Purpose')
            content = content[:pos] + prereq_section + content[pos:]
        elif '## Purpose' in content:
            pos = content.find('## Purpose') + len('## Purpose')
            content = content[:pos] + prereq_section + content[pos:]
    
    # Add Testing Strategy section if missing
    if '## Testing Strategy' not in content and '## Test Strategy' not in content:
        test_section = f"\n## Testing Strategy\n\n### Unit Tests\n- [ ] Tests cover core functionality\n- [ ] Edge cases handled appropriately\n\n### Integration Tests\n- [ ] Integration with dependent components verified\n- [ ] End-to-end workflow tested\n\n"
        # Find a good place to insert (before extended metadata or at end)
        ext_meta_pos = content.find('<!-- EXTENDED_METADATA')
        if ext_meta_pos != -1:
            content = content[:ext_meta_pos] + test_section + content[ext_meta_pos:]
        else:
            content += test_section
    
    # Add Done Definition section if missing
    if '## Done Definition' not in content:
        done_section = f"\n## Done Definition\n\n### Completion Criteria\n- [ ] All success criteria met\n- [ ] Code reviewed and approved\n- [ ] Tests passing\n- [ ] Documentation updated\n- [ ] No critical or high severity issues\n\n"
        # Find a good place to insert (before extended metadata or at end)
        ext_meta_pos = content.find('<!-- EXTENDED_METADATA')
        if ext_meta_pos != -1:
            content = content[:ext_meta_pos] + done_section + content[ext_meta_pos:]
        else:
            content += done_section
    
    return content


def main():
    parser = argparse.ArgumentParser(description="Improve task specifications to maximize PRD accuracy")
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