#!/usr/bin/env python3
"""
MD File Validator and Enhancer for Taskmaster

This script validates and enhances MD files to ensure they meet the standards
for successful Jules task completion.
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple


class MDFileValidator:
    """Validates MD files against Taskmaster standards."""
    
    REQUIRED_SECTIONS = [
        "Task Header",
        "Overview/Purpose", 
        "Success Criteria",
        "Prerequisites & Dependencies",
        "Sub-subtasks Breakdown",
        "Specification Details",
        "Implementation Guide",
        "Configuration Parameters",
        "Performance Targets",
        "Testing Strategy",
        "Common Gotchas & Solutions",
        "Integration Checkpoint",
        "Done Definition",
        "Next Steps"
    ]
    
    PLACEHOLDER_PATTERNS = [
        r'\[Method to verify completion\]',
        r'\[Define.*?\]',
        r'\[Specify.*?\]',
        r'\[What.*?\]',
        r'\[How.*?\]',
        r'\[Step.*?\]',
        r'\[Code example.*?\]',
        r'\[param_name\]',
        r'\[type\]',
        r'\[default\]',
        r'\[validation_rule\]',
        r'\[var_name\]',
        r'\[yes/no\]',
        r'\[Time requirement\]',
        r'\[Throughput requirement\]',
        r'\[Limit for.*?\]',
        r'\[Number\]',
        r'\[Size/quantity.*?\]',
        r'\[Expected increase.*?\]',
        r'\[Current.*?\]',
        r'\[Test requirements.*?\]',
        r'\[Coverage target\]',
        r'\[Specific.*?\]',
        r'\[Quantity\]',
        r'\[Symptom:.*?\]',
        r'\[Cause:.*?\]',
        r'\[Solution:.*?\]',
        r'\[Branch analysis.*?\]',  # Specific to the task files we saw
    ]
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.tasks_dir = self.project_root / "tasks"
        
    def find_task_files(self) -> List[Path]:
        """Find all task MD files in the project."""
        if not self.tasks_dir.exists():
            return []
        
        task_files = []
        for file_path in self.tasks_dir.glob("*.md"):
            if "task-" in file_path.name.lower() or "task_" in file_path.name.lower():
                task_files.append(file_path)
                
        # Also check in subdirectories like task_data
        for file_path in (self.project_root / "task_data").rglob("*.md"):
            if "task-" in file_path.name.lower() or "task_" in file_path.name.lower():
                task_files.append(file_path)
                
        return task_files
    
    def validate_file_structure(self, file_path: Path) -> Dict[str, any]:
        """Validate the structure of a task file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'file': str(file_path),
            'valid': True,
            'missing_sections': [],
            'placeholder_issues': [],
            'success_criteria_issues': [],
            'implementation_guide_issues': []
        }
        
        # Check for required sections
        content_lower = content.lower()
        for section in self.REQUIRED_SECTIONS:
            if section.lower() not in content_lower:
                result['missing_sections'].append(section)
                result['valid'] = False
        
        # Check for placeholder patterns
        for pattern in self.PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                result['placeholder_issues'].extend(matches)
                result['valid'] = False
        
        # Check success criteria for placeholders
        success_section_match = re.search(r'## Success Criteria(.*?)## ', content, re.DOTALL)
        if success_section_match:
            success_content = success_section_match.group(1)
            for pattern in [r'\[Method to verify completion\]', r'\[Verification:.*?\]']:
                matches = re.findall(pattern, success_content)
                if matches:
                    result['success_criteria_issues'].extend(matches)
                    result['valid'] = False
        
        # Check implementation guide for placeholders
        impl_section_match = re.search(r'## Implementation Guide(.*?)## ', content, re.DOTALL)
        if impl_section_match:
            impl_content = impl_section_match.group(1)
            for pattern in [r'\[Step.*?\]', r'\[Code example.*?\]', r'\[Detailed instructions.*?\]']:
                matches = re.findall(pattern, impl_content)
                if matches:
                    result['implementation_guide_issues'].extend(matches)
                    result['valid'] = False
        
        return result
    
    def validate_all_files(self) -> List[Dict[str, any]]:
        """Validate all task files in the project."""
        task_files = self.find_task_files()
        results = []
        
        for file_path in task_files:
            result = self.validate_file_structure(file_path)
            results.append(result)
        
        return results
    
    def generate_enhancement_report(self, validation_results: List[Dict[str, any]]) -> str:
        """Generate a report of validation results."""
        report_lines = [
            "# MD File Validation Report",
            "",
            f"Total files analyzed: {len(validation_results)}",
            f"Valid files: {len([r for r in validation_results if r['valid']])}",
            f"Invalid files: {len([r for r in validation_results if not r['valid']])}",
            ""
        ]
        
        for result in validation_results:
            if not result['valid']:
                report_lines.append(f"## Issues in {result['file']}")
                
                if result['missing_sections']:
                    report_lines.append("### Missing Sections:")
                    for section in result['missing_sections']:
                        report_lines.append(f"- {section}")
                    report_lines.append("")
                
                if result['placeholder_issues']:
                    report_lines.append("### Placeholder Issues:")
                    unique_placeholders = list(set(result['placeholder_issues']))
                    for placeholder in unique_placeholders[:10]:  # Limit to first 10
                        report_lines.append(f"- {placeholder}")
                    if len(unique_placeholders) > 10:
                        report_lines.append(f"... and {len(unique_placeholders) - 10} more")
                    report_lines.append("")
                
                if result['success_criteria_issues']:
                    report_lines.append("### Success Criteria Issues:")
                    unique_issues = list(set(result['success_criteria_issues']))
                    for issue in unique_issues[:5]:
                        report_lines.append(f"- {issue}")
                    if len(unique_issues) > 5:
                        report_lines.append(f"... and {len(unique_issues) - 5} more")
                    report_lines.append("")
                
                if result['implementation_guide_issues']:
                    report_lines.append("### Implementation Guide Issues:")
                    unique_issues = list(set(result['implementation_guide_issues']))
                    for issue in unique_issues[:5]:
                        report_lines.append(f"- {issue}")
                    if len(unique_issues) > 5:
                        report_lines.append(f"... and {len(unique_issues) - 5} more")
                    report_lines.append("")
                
                report_lines.append("---")
                report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """Main function to run the validator."""
    print("🔍 Validating Taskmaster MD files...")
    
    validator = MDFileValidator()
    results = validator.validate_all_files()
    
    # Generate and save report
    report = validator.generate_enhancement_report(results)
    
    report_path = Path("MD_VALIDATION_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Validation complete! Report saved to {report_path}")
    print(f"📊 Found {len(results)} task files")
    print(f"📈 {len([r for r in results if r['valid']])} valid, {len([r for r in results if not r['valid']])} need enhancement")
    
    # Print summary statistics
    total_missing_sections = sum(len(r['missing_sections']) for r in results)
    total_placeholders = sum(len(r['placeholder_issues']) for r in results)
    
    print(f"🔍 Issues found: {total_missing_sections} missing sections, {total_placeholders} placeholder issues")


if __name__ == "__main__":
    main()