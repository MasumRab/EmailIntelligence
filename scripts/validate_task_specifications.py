#!/usr/bin/env python3
"""
Task Specification Quality Validator
Validates task files against the enhanced template to ensure maximum PRD generation accuracy
"""

import argparse
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
import sys


def validate_task_file(task_path: str) -> Dict[str, any]:
    """
    Validate a task file against the enhanced template requirements.
    """
    with open(task_path, 'r', encoding='utf-8') as f:
        content = f.read()

    validation_results = {
        'file_path': str(task_path),
        'valid': True,
        'issues': [],
        'completeness_score': 0,
        'sections_present': [],
        'missing_sections': [],
        'quality_indicators': {}
    }

    # Required sections for maximum PRD accuracy
    required_sections = [
        r'## Overview/Purpose',
        r'## Success Criteria',
        r'## Prerequisites & Dependencies',
        r'## Sub-subtasks Breakdown',
        r'## Specification Details',
        r'## Implementation Guide',
        r'## Configuration Parameters',
        r'## Performance Targets',
        r'## Testing Strategy',
        r'## Common Gotchas & Solutions',
        r'## Integration Checkpoint',
        r'## Done Definition',
        r'## Next Steps'
    ]

    # Check for required sections
    missing_sections = []
    present_sections = []

    for section in required_sections:
        pattern = section.replace('[', r'\[').replace(']', r'\]')
        if re.search(pattern, content):
            present_sections.append(section)
        else:
            missing_sections.append(section)

    validation_results['sections_present'] = present_sections
    validation_results['missing_sections'] = missing_sections

    # Check for header metadata
    header_fields = [
        r'\*\*Status:', r'\*\*Priority:', r'\*\*Effort:',
        r'\*\*Complexity:', r'\*\*Dependencies:'
    ]

    missing_header_fields = []
    for field in header_fields:
        if not re.search(field, content):
            missing_header_fields.append(field.replace(r'\*\*', '**').replace(r'\[', '[').replace(r'\]', ']'))

    if missing_header_fields:
        validation_results['issues'].append(f"Missing header fields: {missing_header_fields}")

    # Check for success criteria quality
    success_criteria_match = re.search(r'## Success Criteria\s*\n+([\s\S]*?)(?=\n## |\Z)', content)
    if success_criteria_match:
        criteria_content = success_criteria_match.group(1)
        # Count checklist items
        checklist_items = re.findall(r'- \[.\]\s+.+', criteria_content)
        validation_results['quality_indicators']['success_criteria_count'] = len(checklist_items)

        if len(checklist_items) < 3:
            validation_results['issues'].append(f"Success criteria has only {len(checklist_items)} items, recommend at least 3")
    else:
        validation_results['issues'].append("No success criteria section found")

    # Check for subtasks quality
    subtasks_match = re.search(r'## Sub-subtasks Breakdown\s*\n+([\s\S]*?)(?=\n## |\Z)', content)
    if subtasks_match:
        subtasks_content = subtasks_match.group(1)
        # Count subtasks (look for ### headers)
        subtask_headers = re.findall(r'### \d+\.\d+:', subtasks_content)
        validation_results['quality_indicators']['subtask_count'] = len(subtask_headers)

        if len(subtask_headers) < 2:
            validation_results['issues'].append(f"Only {len(subtask_headers)} subtasks found, recommend at least 2 for complex tasks")
    else:
        validation_results['issues'].append("No sub-subtasks breakdown found")

    # Calculate completeness score
    total_required = len(required_sections) + len(header_fields)
    present_count = len(present_sections) + (len(header_fields) - len(missing_header_fields))
    completeness_score = present_count / total_required if total_required > 0 else 0
    validation_results['completeness_score'] = completeness_score

    # Overall validation
    if missing_sections or missing_header_fields or completeness_score < 0.8:
        validation_results['valid'] = False

    return validation_results


def validate_all_tasks(tasks_dir: str) -> Dict[str, any]:
    """
    Validate all task files in a directory.
    """
    tasks_path = Path(tasks_dir)
    task_files = list(tasks_path.glob("task*.md"))

    results = {
        'total_tasks': len(task_files),
        'valid_tasks': 0,
        'invalid_tasks': 0,
        'total_issues': 0,
        'average_completeness': 0,
        'task_validations': [],
        'summary_issues': {}
    }

    total_completeness = 0

    for task_file in task_files:
        validation = validate_task_file(str(task_file))
        results['task_validations'].append(validation)
        
        if validation['valid']:
            results['valid_tasks'] += 1
        else:
            results['invalid_tasks'] += 1
            
        results['total_issues'] += len(validation['issues'])
        total_completeness += validation['completeness_score']

        # Aggregate issues by type
        for issue in validation['issues']:
            issue_type = issue.split(':')[0]  # Get the first part as issue type
            if issue_type not in results['summary_issues']:
                results['summary_issues'][issue_type] = 0
            results['summary_issues'][issue_type] += 1

    if results['total_tasks'] > 0:
        results['average_completeness'] = total_completeness / results['total_tasks']

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate task specifications for maximum PRD generation accuracy")
    parser.add_argument("--tasks-dir", "-d", default="./tasks", help="Directory containing task markdown files")
    parser.add_argument("--output", "-o", help="Output file for validation results (JSON format)")
    parser.add_argument("--report", "-r", action="store_true", help="Generate detailed report")

    args = parser.parse_args()

    print(f"Validating task specifications in: {args.tasks_dir}")
    
    results = validate_all_tasks(args.tasks_dir)

    print(f"\nVALIDATION SUMMARY:")
    print(f"  Total tasks analyzed: {results['total_tasks']}")
    print(f"  Valid tasks: {results['valid_tasks']}")
    print(f"  Invalid tasks: {results['invalid_tasks']}")
    print(f"  Total issues found: {results['total_issues']}")
    print(f"  Average completeness: {results['average_completeness']:.2%}")

    if args.report:
        print(f"\nDETAILED ISSUE BREAKDOWN:")
        for issue_type, count in sorted(results['summary_issues'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {issue_type}: {count} occurrences")

        print(f"\nTASK-BY-TASK RESULTS:")
        for validation in results['task_validations']:
            status = "✓" if validation['valid'] else "✗"
            print(f"  {status} {Path(validation['file_path']).name}: {validation['completeness_score']:.2%} complete")
            if validation['issues'] and len(validation['issues']) < 5:  # Only show issues if not too many
                for issue in validation['issues'][:3]:  # Show first 3 issues
                    print(f"      - {issue}")
                if len(validation['issues']) > 3:
                    print(f"      ... and {len(validation['issues']) - 3} more issues")

    # Save results if output file specified
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"\nValidation results saved to: {args.output}")

    # Exit with error code if there are invalid tasks
    if results['invalid_tasks'] > 0:
        print(f"\nWARNING: {results['invalid_tasks']} tasks have specification issues that may impact PRD generation accuracy.")
        print("Recommendation: Address the issues before proceeding with PRD generation.")
        return 1

    print(f"\nAll tasks meet the enhanced specification requirements for maximum PRD generation accuracy.")
    return 0


if __name__ == "__main__":
    exit(main())