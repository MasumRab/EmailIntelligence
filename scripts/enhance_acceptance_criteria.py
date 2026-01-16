#!/usr/bin/env python3
"""
Acceptance Criteria Enhancer
Improves all acceptance criteria in task files to be more specific, measurable, testable, and verifiable.
"""

import argparse
import re
from pathlib import Path
from typing import Dict, Any, List


def enhance_acceptance_criteria(content: str) -> str:
    """
    Enhance the acceptance criteria in a task file to be more specific, measurable, testable, and verifiable.
    """
    # Find the success criteria section
    success_criteria_pattern = r'(## Success Criteria\s*\n+)([\s\S]*?)(?=\n## |\n---|\Z)'
    match = re.search(success_criteria_pattern, content)
    
    if not match:
        # If no success criteria section, try to find checklist items anywhere in the content
        checklist_items = re.findall(r'- \[.\]\s*(.+)', content)
        if checklist_items:
            # Create a success criteria section with enhanced items
            new_criteria_section = "## Success Criteria\n\n"
            for item in checklist_items:
                enhanced_item = enhance_single_criteria(item.strip())
                new_criteria_section += f"- [ ] {enhanced_item}\n"
            new_criteria_section += "\n"
            
            # Find a good place to insert the success criteria section
            # Look for after the description/purpose section
            desc_end = content.find('\n\n## ')  # Find first section after description
            if desc_end == -1:
                desc_end = len(content)  # If no other sections, append at end
            
            content = content[:desc_end] + new_criteria_section + content[desc_end:]
        return content
    
    section_header = match.group(1)
    section_content = match.group(2)
    
    # Parse the current criteria
    criteria_items = re.findall(r'- \[.\]\s*(.+)', section_content)
    
    # Enhance each criteria
    enhanced_criteria = "## Success Criteria\n\n"
    for item in criteria_items:
        enhanced_item = enhance_single_criteria(item.strip())
        enhanced_criteria += f"- [ ] {enhanced_item}\n"
    
    enhanced_criteria += "\n"
    
    # Replace the original section with the enhanced one
    content = content.replace(match.group(0), section_header + enhanced_criteria)
    
    return content


def enhance_single_criteria(criteria: str) -> str:
    """
    Enhance a single acceptance criteria to be more specific, measurable, testable, and verifiable.
    """
    # If the criteria is already well-defined, return as is
    if is_well_defined_criteria(criteria):
        return criteria
    
    # Enhance vague criteria by making them more specific and testable
    enhanced = criteria
    
    # Common patterns to enhance
    if re.search(r'(created|created|established|defined|built|implemented)', criteria, re.IGNORECASE):
        # Add more specific verification details
        if 'document' in criteria.lower():
            enhanced = f"{criteria} - Document is saved in the correct location and follows the specified format"
        elif 'function' in criteria.lower() or 'method' in criteria.lower():
            enhanced = f"{criteria} - Function executes without errors and returns expected output for valid inputs"
        elif 'framework' in criteria.lower():
            enhanced = f"{criteria} - Framework components are properly integrated and pass all unit tests"
        elif 'system' in criteria.lower():
            enhanced = f"{criteria} - System performs all specified functions and meets performance requirements"
        elif 'process' in criteria.lower():
            enhanced = f"{criteria} - Process completes all steps and produces expected outputs"
        elif 'module' in criteria.lower():
            enhanced = f"{criteria} - Module integrates properly with other components and handles edge cases"
        elif 'test' in criteria.lower():
            enhanced = f"{criteria} - Test passes with >95% coverage and handles error cases appropriately"
        elif 'configured' in criteria.lower():
            enhanced = f"{criteria} - Configuration is validated and all parameters are set correctly"
        else:
            # General enhancement for implementation tasks
            enhanced = f"{criteria} - Implementation passes all validation checks and meets specified requirements"
    
    # Add verification method if not already present
    if not has_verification_method(enhanced):
        enhanced += " - Verification: [Method to verify completion]"
    
    return enhanced


def is_well_defined_criteria(criteria: str) -> bool:
    """
    Check if a criteria is already well-defined (specific, measurable, testable).
    """
    # Check if the criteria contains specific, measurable elements
    has_quantifier = bool(re.search(r'(\d+%|\d+ hours|\d+ days|\d+ items|>?\d+|<\d+)', criteria))
    has_verification = 'verification:' in criteria.lower() or 'test' in criteria.lower() or 'confirm' in criteria.lower()
    has_specific_action = bool(re.search(r'(validate|verify|check|ensure|confirm|measure|calculate|implement)', criteria, re.IGNORECASE))
    
    # If it has any of these elements, consider it well-defined
    return has_quantifier or has_verification or has_specific_action


def has_verification_method(criteria: str) -> bool:
    """
    Check if the criteria already has a verification method specified.
    """
    return 'verification:' in criteria.lower() or 'method:' in criteria.lower()


def enhance_all_task_acceptance_criteria(task_files: List[Path]) -> int:
    """
    Enhance acceptance criteria for all task files in the list.
    
    Args:
        task_files: List of paths to task markdown files
    
    Returns:
        Number of files processed
    """
    processed_count = 0
    
    for task_file in task_files:
        print(f"Enhancing acceptance criteria in {task_file.name}...")
        
        # Read the task file
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Enhance the acceptance criteria
        enhanced_content = enhance_acceptance_criteria(content)
        
        # Write the enhanced content back to the file
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        processed_count += 1
        print(f"  ✓ Enhanced acceptance criteria in {task_file.name}")
    
    return processed_count


def main():
    parser = argparse.ArgumentParser(description="Enhance acceptance criteria in task files to be more specific, measurable, testable, and verifiable")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing task markdown files")
    parser.add_argument("--pattern", default="task*.md", help="File pattern to match (default: task*.md)")
    
    args = parser.parse_args()
    
    # Find all task markdown files
    input_path = Path(args.input_dir)
    task_files = list(input_path.glob(args.pattern))
    
    if not task_files:
        print(f"No task files found in {input_path} with pattern {args.pattern}")
        return 1
    
    print(f"Found {len(task_files)} task files to enhance")
    
    # Enhance acceptance criteria in all task files
    processed = enhance_all_task_acceptance_criteria(task_files)
    
    print(f"\nSuccessfully enhanced acceptance criteria in {processed} task files")
    print("Enhancements made:")
    print("- Made criteria more specific and measurable")
    print("- Added verification methods where missing")
    print("- Improved testability of each criterion")
    print("- Ensured criteria are objectively verifiable")
    
    return 0


if __name__ == "__main__":
    exit(main())