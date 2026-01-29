#!/usr/bin/env python3
"""
Analyze processed tasks and their placeholder counts
"""

import re
from pathlib import Path


def count_placeholders(content: str) -> int:
    """Count the number of placeholder patterns in the content."""
    placeholder_patterns = [
        r'\[.*?\]',  # Square brackets with any content
        r'\(.*?\)',  # Parentheses with any content (when containing placeholders)
        r'\{\{.*?\}\}',  # Double curly braces
        r'PLACEHOLDER',  # Literal placeholder
        r'NEEDS_IMPLEMENTATION',  # Literal needs implementation
        r'TODO',  # Literal todo
        r'FIXME',  # Literal fixme
        r'METHOD TO VERIFY',  # Method to verify
        r'VERIFICATION METHOD',  # Verification method
        r'HOW TO TEST',  # How to test
        r'HOW TO VALIDATE',  # How to validate
        r'DESCRIPTION NEEDED',  # Description needed
        r'PARAMETER NAME',  # Parameter name
        r'EXPECTED OUTCOME',  # Expected outcome
        r'IMPLEMENTATION DETAILS',  # Implementation details
        r'SPECIFY',  # Specify
        r'DEFINE',  # Define
        r'CONFIGURATION PARAMETER',  # Configuration parameter
        r'CONFIGURATION VALUE',  # Configuration value
        r'CONFIGURATION OPTION',  # Configuration option
        r'CONFIGURATION SETTING',  # Configuration setting
        r'TEST REQUIREMENT',  # Test requirement
        r'TEST STRATEGY',  # Test strategy
        r'PERFORMANCE TARGET',  # Performance target
        r'PERFORMANCE REQUIREMENT',  # Performance requirement
        r'PERFORMANCE METRIC',  # Performance metric
        r'PERFORMANCE BENCHMARK',  # Performance benchmark
        r'PERFORMANCE INDICATOR',  # Performance indicator
        r'PERFORMANCE MEASUREMENT',  # Performance measurement
        r'PERFORMANCE GOAL',  # Performance goal
        r'PERFORMANCE OBJECTIVE',  # Performance objective
        r'PERFORMANCE STANDARD',  # Performance standard
        r'PERFORMANCE CRITERION',  # Performance criterion
        r'PERFORMANCE SPECIFICATION',  # Performance specification
        r'PERFORMANCE REQUIREMENT',  # Performance requirement
        r'PERFORMANCE EXPECTATION',  # Performance expectation
    ]

    count = 0
    for pattern in placeholder_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        count += len(matches)

    return count


def analyze_tasks():
    """Analyze tasks and their placeholder counts."""
    tasks_dir = Path("tasks")
    task_files = list(tasks_dir.glob("task*.md"))
    
    print("Task Analysis: Content vs Placeholders")
    print("=" * 60)
    print(f"{'Task ID':<15} {'Placeholders':<12} {'Content Lines':<13} {'Sections':<8} {'Checklists':<10}")
    print("-" * 60)
    
    task_analysis = []
    
    for task_file in task_files:
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count placeholders
        placeholders = count_placeholders(content)
        
        # Count content lines (non-empty, non-header lines)
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        content_lines = len([line for line in lines if not line.startswith('#')])
        
        # Count sections (headers with ##)
        sections = len(re.findall(r'^##\s', content, re.MULTILINE))
        
        # Count checklist items
        checklists = len(re.findall(r'- \[.\]', content))
        
        task_analysis.append({
            'file': task_file.name,
            'placeholders': placeholders,
            'content_lines': content_lines,
            'sections': sections,
            'checklists': checklists,
            'ratio': placeholders / max(content_lines, 1) * 100  # Placeholder-to-content ratio
        })
    
    # Sort by placeholder-to-content ratio (lowest first - best implementations)
    task_analysis.sort(key=lambda x: x['ratio'])
    
    for task in task_analysis:
        print(f"{task['file']:<15} {task['placeholders']:<12} {task['content_lines']:<13} {task['sections']:<8} {task['checklists']:<10}")
    
    print("\nTop 10 Most Implemented Tasks (Lowest Placeholder Ratios):")
    print("=" * 60)
    print(f"{'Task ID':<15} {'Placeholders':<12} {'Content Lines':<13} {'Ratio':<8}")
    print("-" * 60)
    for task in task_analysis[:10]:
        print(f"{task['file']:<15} {task['placeholders']:<12} {task['content_lines']:<13} {task['ratio']:<8.2f}%")
    
    print("\nBottom 10 Least Implemented Tasks (Highest Placeholder Ratios):")
    print("=" * 60)
    print(f"{'Task ID':<15} {'Placeholders':<12} {'Content Lines':<13} {'Ratio':<8}")
    print("-" * 60)
    for task in task_analysis[-10:]:
        print(f"{task['file']:<15} {task['placeholders']:<12} {task['content_lines']:<13} {task['ratio']:<8.2f}%")

    return task_analysis


if __name__ == "__main__":
    analysis = analyze_tasks()