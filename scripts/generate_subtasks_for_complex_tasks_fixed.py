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
                f"### 1.1: Requirements Analysis and Design",
                f"- Analyze requirements for {title}",
                f"- Design implementation approach",
                f"- Define interfaces and data structures",
                f"- Plan error handling strategy",
                f"",
                f"### 1.2: Core Implementation",
                f"- Implement core functionality",
                f"- Write unit tests for core features",
                f"- Handle edge cases and error conditions",
                f"",
                f"### 1.3: Integration and Testing",
                f"- Integrate with existing components",
                f"- Perform integration testing",
                f"- Validate against requirements",
                f"",
                f"### 1.4: Documentation and Review",
                f"- Document implementation details",
                f"- Conduct code review",
                f"- Update relevant documentation",
                f""
            ]
        elif complexity >= 4:
            subtasks = [
                f"### 1.1: Implementation",
                f"- Implement core functionality for {title}",
                f"- Write unit tests",
                f"- Handle error cases",
                f"",
                f"### 1.2: Testing and Validation",
                f"- Test implementation against requirements",
                f"- Validate edge cases",
                f"",
                f"### 1.3: Documentation",
                f"- Document implementation",
                f"- Update relevant docs",
                f""
            ]
        else:
            subtasks = [
                f"### 1.1: Implementation",
                f"- Implement {title}",
                f"- Test functionality",
                f"- Document changes",
                f""
            ]

    elif 'analyze' in title.lower() or 'analysis' in title.lower():
        if complexity >= 7:
            subtasks = [
                f"### 1.1: Data Collection and Preparation",
                f"- Gather required data for analysis",
                f"- Clean and preprocess data",
                f"- Set up analysis environment",
                f"",
                f"### 1.2: Analysis Execution",
                f"- Perform core analysis",
                f"- Generate intermediate results",
                f"- Document findings",
                f"",
                f"### 1.3: Result Validation",
                f"- Validate analysis results",
                f"- Cross-check with known data",
                f"- Identify anomalies",
                f"",
                f"### 1.4: Reporting and Documentation",
                f"- Create analysis report",
                f"- Document methodology",
                f"- Summarize key findings",
                f""
            ]
        elif complexity >= 4:
            subtasks = [
                f"### 1.1: Analysis Setup",
                f"- Prepare analysis environment",
                f"- Gather required data",
                f"",
                f"### 1.2: Execute Analysis",
                f"- Perform the analysis",
                f"- Record results",
                f"",
                f"### 1.3: Document Findings",
                f"- Create summary report",
                f"- Document key insights",
                f""
            ]
        else:
            subtasks = [
                f"### 1.1: Perform Analysis",
                f"- Analyze {title}",
                f"- Document findings",
                f""
            ]

    elif 'design' in title.lower() or 'architecture' in title.lower():
        if complexity >= 7:
            subtasks = [
                f"### 1.1: Requirements Review",
                f"- Review functional requirements",
                f"- Identify non-functional requirements",
                f"- Define constraints and assumptions",
                f"",
                f"### 1.2: Architecture Design",
                f"- Create high-level architecture",
                f"- Define component interactions",
                f"- Specify interfaces",
                f"",
                f"### 1.3: Detailed Design",
                f"- Design detailed component structure",
                f"- Define data models",
                f"- Specify algorithms",
                f"",
                f"### 1.4: Validation and Review",
                f"- Validate design against requirements",
                f"- Conduct architecture review",
                f"- Document design decisions",
                f""
            ]
        elif complexity >= 4:
            subtasks = [
                f"### 1.1: Design Creation",
                f"- Create architecture design",
                f"- Define components and interfaces",
                f"",
                f"### 1.2: Design Validation",
                f"- Validate design against requirements",
                f"- Review design for consistency",
                f"",
                f"### 1.3: Documentation",
                f"- Document design decisions",
                f"- Create design diagrams",
                f""
            ]
        else:
            subtasks = [
                f"### 1.1: Create Design",
                f"- Design {title}",
                f"- Document key decisions",
                f""
            ]

    elif 'test' in title.lower() or 'validation' in title.lower():
        if complexity >= 7:
            subtasks = [
                f"### 1.1: Test Strategy Definition",
                f"- Define test approach and scope",
                f"- Identify test scenarios",
                f"- Plan test environment setup",
                f"",
                f"### 1.2: Test Case Development",
                f"- Create detailed test cases",
                f"- Define test data requirements",
                f"- Prepare test scripts",
                f"",
                f"### 1.3: Test Execution",
                f"- Execute test cases",
                f"- Record test results",
                f"- Document defects",
                f"",
                f"### 1.4: Test Reporting",
                f"- Analyze test results",
                f"- Create test summary report",
                f"- Document lessons learned",
                f""
            ]
        elif complexity >= 4:
            subtasks = [
                f"### 1.1: Test Preparation",
                f"- Set up test environment",
                f"- Prepare test cases",
                f"",
                f"### 1.2: Test Execution",
                f"- Execute tests",
                f"- Record results",
                f"",
                f"### 1.3: Reporting",
                f"- Create test report",
                f"- Document findings",
                f""
            ]
        else:
            subtasks = [
                f"### 1.1: Execute Tests",
                f"- Test {title}",
                f"- Document results",
                f""
            ]

    else:
        # Generic subtask pattern for other task types
        if complexity >= 7:
            subtasks = [
                f"### 1.1: Research and Planning",
                f"- Research requirements for {title}",
                f"- Plan implementation approach",
                f"- Identify potential challenges",
                f"",
                f"### 1.2: Implementation",
                f"- Execute core implementation",
                f"- Handle error cases",
                f"- Write unit tests",
                f"",
                f"### 1.3: Integration and Testing",
                f"- Integrate with existing components",
                f"- Perform integration tests",
                f"- Validate functionality",
                f"",
                f"### 1.4: Documentation and Review",
                f"- Document implementation",
                f"- Conduct review",
                f"- Update relevant documentation",
                f""
            ]
        elif complexity >= 4:
            subtasks = [
                f"### 1.1: Implementation",
                f"- Implement {title}",
                f"- Write tests",
                f"",
                f"### 1.2: Testing and Validation",
                f"- Test functionality",
                f"- Validate requirements",
                f"",
                f"### 1.3: Documentation",
                f"- Document changes",
                f"- Update docs",
                f""
            ]
        else:
            subtasks = [
                f"### 1.1: Execute Task",
                f"- Complete {title}",
                f"- Verify completion",
                f""
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