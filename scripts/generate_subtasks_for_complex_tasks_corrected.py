#!/usr/bin/env python3
"""
Subtask Generator for Tasks
Generates appropriate subtasks for tasks that lack them, especially high-complexity ones
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List


def generate_subtasks_for_task(task_file_path: str) -> str:
    """
    Generate appropriate subtasks for a task that lacks them.
    """
    with open(task_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract task information
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled Task"

    # Determine complexity level based on content or filename
    complexity_match = re.search(r'Complexity:?\s*(\d+)', content)
    if complexity_match:
        complexity = int(complexity_match.group(1))
    else:
        # Estimate complexity based on title and content length
        complexity = min(10, max(1, len(content) // 1000))

    # Generate appropriate subtasks based on task title and complexity
    subtasks = []

    # Common subtask patterns based on task types
    if 'implement' in title.lower() or 'develop' in title.lower() or 'create' in title.lower():
        if complexity >= 7:
            subtasks = [
                "### 1.1: Requirements Analysis and Design",
                f"- Analyze requirements for {title}",
                "- Design implementation approach",
                "- Define interfaces and data structures",
                "- Plan error handling strategy",
                "",
                "### 1.2: Core Implementation",
                "- Implement core functionality",
                "- Write unit tests for core features",
                "- Handle edge cases and error conditions",
                "",
                "### 1.3: Integration and Testing",
                "- Integrate with existing components",
                "- Perform integration testing",
                "- Validate against requirements",
                "",
                "### 1.4: Documentation and Review",
                "- Document implementation details",
                "- Conduct code review",
                "- Update relevant documentation",
                ""
            ]
        elif complexity >= 4:
            subtasks = [
                "### 1.1: Implementation",
                f"- Implement core functionality for {title}",
                "- Write unit tests",
                "- Handle error cases",
                "",
                "### 1.2: Testing and Validation",
                "- Test implementation against requirements",
                "- Validate edge cases",
                "",
                "### 1.3: Documentation",
                "- Document implementation",
                "- Update relevant docs",
                ""
            ]
        else:
            subtasks = [
                "### 1.1: Implementation",
                f"- Implement {title}",
                "- Test functionality",
                "- Document changes",
                ""
            ]

    elif 'analyze' in title.lower() or 'analysis' in title.lower():
        if complexity >= 7:
            subtasks = [
                "### 1.1: Data Collection and Preparation",
                "- Gather required data for analysis",
                "- Clean and preprocess data",
                "- Set up analysis environment",
                "",
                "### 1.2: Analysis Execution",
                "- Perform core analysis",
                "- Generate intermediate results",
                "- Document findings",
                "",
                "### 1.3: Result Validation",
                "- Validate analysis results",
                "- Cross-check with known data",
                "- Identify anomalies",
                "",
                "### 1.4: Reporting and Documentation",
                "- Create analysis report",
                "- Document methodology",
                "- Summarize key findings",
                ""
            ]
        elif complexity >= 4:
            subtasks = [
                "### 1.1: Analysis Setup",
                "- Prepare analysis environment",
                "- Gather required data",
                "",
                "### 1.2: Execute Analysis",
                "- Perform the analysis",
                "- Record results",
                "",
                "### 1.3: Document Findings",
                "- Create summary report",
                "- Document key insights",
                ""
            ]
        else:
            subtasks = [
                "### 1.1: Perform Analysis",
                f"- Analyze {title}",
                "- Document findings",
                ""
            ]

    elif 'design' in title.lower() or 'architecture' in title.lower():
        if complexity >= 7:
            subtasks = [
                "### 1.1: Requirements Review",
                "- Review functional requirements",
                "- Identify non-functional requirements",
                "- Define constraints and assumptions",
                "",
                "### 1.2: Architecture Design",
                "- Create high-level architecture",
                "- Define component interactions",
                "- Specify interfaces",
                "",
                "### 1.3: Detailed Design",
                "- Design detailed component structure",
                "- Define data models",
                "- Specify algorithms",
                "",
                "### 1.4: Validation and Review",
                "- Validate design against requirements",
                "- Conduct architecture review",
                "- Document design decisions",
                ""
            ]
        elif complexity >= 4:
            subtasks = [
                "### 1.1: Design Creation",
                "- Create architecture design",
                "- Define components and interfaces",
                "",
                "### 1.2: Design Validation",
                "- Validate design against requirements",
                "- Review design for consistency",
                "",
                "### 1.3: Documentation",
                "- Document design decisions",
                "- Create design diagrams",
                ""
            ]
        else:
            subtasks = [
                "### 1.1: Create Design",
                f"- Design {title}",
                "- Document key decisions",
                ""
            ]

    elif 'test' in title.lower() or 'validation' in title.lower():
        if complexity >= 7:
            subtasks = [
                "### 1.1: Test Strategy Definition",
                "- Define test approach and scope",
                "- Identify test scenarios",
                "- Plan test environment setup",
                "",
                "### 1.2: Test Case Development",
                "- Create detailed test cases",
                "- Define test data requirements",
                "- Prepare test scripts",
                "",
                "### 1.3: Test Execution",
                "- Execute test cases",
                "- Record test results",
                "- Document defects",
                "",
                "### 1.4: Test Reporting",
                "- Analyze test results",
                "- Create test summary report",
                "- Document lessons learned",
                ""
            ]
        elif complexity >= 4:
            subtasks = [
                "### 1.1: Test Preparation",
                "- Set up test environment",
                "- Prepare test cases",
                "",
                "### 1.2: Test Execution",
                "- Execute tests",
                "- Record results",
                "",
                "### 1.3: Reporting",
                "- Create test report",
                "- Document findings",
                ""
            ]
        else:
            subtasks = [
                "### 1.1: Execute Tests",
                f"- Test {title}",
                "- Document results",
                ""
            ]

    else:
        # Generic subtask pattern for other task types
        if complexity >= 7:
            subtasks = [
                "### 1.1: Research and Planning",
                f"- Research requirements for {title}",
                "- Plan implementation approach",
                "- Identify potential challenges",
                "",
                "### 1.2: Implementation",
                "- Execute core implementation",
                "- Handle error cases",
                "- Write unit tests",
                "",
                "### 1.3: Integration and Testing",
                "- Integrate with existing components",
                "- Perform integration tests",
                "- Validate functionality",
                "",
                "### 1.4: Documentation and Review",
                "- Document implementation",
                "- Conduct review",
                "- Update relevant documentation",
                ""
            ]
        elif complexity >= 4:
            subtasks = [
                "### 1.1: Implementation",
                f"- Implement {title}",
                "- Write tests",
                "",
                "### 1.2: Testing and Validation",
                "- Test functionality",
                "- Validate requirements",
                "",
                "### 1.3: Documentation",
                "- Document changes",
                "- Update docs",
                ""
            ]
        else:
            subtasks = [
                "### 1.1: Execute Task",
                f"- Complete {title}",
                "- Verify completion",
                ""
            ]

    # Create the subtasks section
    subtasks_section = "## Sub-subtasks Breakdown\n\n"
    subtasks_section += "\n".join(subtasks)

    # Find where to insert the subtasks section
    # Look for a good place to insert - after the main description but before other sections
    sections_to_find = [
        r'\n## Prerequisites & Dependencies',
        r'\n## Specification Details',
        r'\n## Implementation Guide',
        r'\n## Success Criteria',
        r'\n---\n',
        r'\n## Configuration Parameters',
        r'\n## Performance Targets',
        r'\n## Testing Strategy',
        r'\n## Common Gotchas',
        r'\n## Integration Checkpoint',
        r'\n## Done Definition',
        r'\n## Next Steps'
    ]

    insertion_point = len(content)  # Default to end of file

    for section_pattern in sections_to_find:
        match = re.search(section_pattern, content)
        if match:
            insertion_point = min(insertion_point, match.start())

    # Insert the subtasks section
    new_content = content[:insertion_point] + "\n" + subtasks_section + "\n" + content[insertion_point:]

    return new_content


def main():
    # Find all task files that lack subtasks (based on our analysis)
    tasks_dir = Path("/home/masum/github/PR/.taskmaster/tasks")
    all_task_files = list(tasks_dir.glob("task*.md"))

    # We identified tasks without subtasks in our analysis
    # Let's process the high-complexity ones first (complexity >= 6)
    high_complexity_tasks = []

    for task_file in all_task_files:
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract complexity
        complexity_match = re.search(r'Complexity:?\s*(\d+)', content)
        if complexity_match:
            complexity = int(complexity_match.group(1))
            if complexity >= 6:  # High complexity tasks
                # Check if task already has subtasks
                if not re.search(r'## Sub-subtasks?|### \d+\.\d+', content):
                    high_complexity_tasks.append(task_file)

    print(f"Found {len(high_complexity_tasks)} high-complexity tasks without subtasks")

    # Process each high-complexity task without subtasks
    updated_count = 0
    for task_file in high_complexity_tasks:
        print(f"Generating subtasks for: {task_file.name}")

        try:
            # Generate new content with subtasks
            new_content = generate_subtasks_for_task(str(task_file))

            # Create backup
            backup_path = task_file.with_suffix(f'.md.backup_before_subtasks')
            task_file.rename(backup_path)

            # Write new content
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"  ✓ Generated subtasks for {task_file.name}")
            updated_count += 1

        except Exception as e:
            print(f"  ✗ Error processing {task_file.name}: {e}")

    print(f"\nSuccessfully updated {updated_count} high-complexity tasks with subtasks")

    # Also process some medium complexity tasks
    medium_complexity_tasks = []
    for task_file in all_task_files:
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract complexity
        complexity_match = re.search(r'Complexity:?\s*(\d+)', content)
        if complexity_match:
            complexity = int(complexity_match.group(1))
            if 4 <= complexity < 6:  # Medium complexity tasks
                # Check if task already has subtasks
                if not re.search(r'## Sub-subtasks?|### \d+\.\d+', content):
                    medium_complexity_tasks.append(task_file)

    print(f"\nFound {len(medium_complexity_tasks)} medium-complexity tasks without subtasks")

    # Process medium complexity tasks
    for task_file in medium_complexity_tasks[:10]:  # Limit to first 10 to avoid too many changes at once
        print(f"Generating subtasks for: {task_file.name}")

        try:
            # Generate new content with subtasks
            new_content = generate_subtasks_for_task(str(task_file))

            # Create backup
            backup_path = task_file.with_suffix(f'.md.backup_before_subtasks')
            task_file.rename(backup_path)

            # Write new content
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"  ✓ Generated subtasks for {task_file.name}")
            updated_count += 1

        except Exception as e:
            print(f"  ✗ Error processing {task_file.name}: {e}")

    print(f"\nTotal tasks updated with subtasks: {updated_count}")
    print("Subtasks have been added to high and medium complexity tasks to improve task manageability.")
    print("This will help break down complex tasks into manageable pieces for better tracking and implementation.")

    return 0


if __name__ == "__main__":
    exit(main())