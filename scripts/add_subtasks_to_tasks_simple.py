#!/usr/bin/env python3
"""
Simple Script to Add Subtasks to Complex Tasks
Finds tasks without subtasks and adds appropriate subtasks to improve manageability
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, List


def add_subtasks_to_task(task_file_path: str) -> str:
    """
    Add appropriate subtasks to a task that lacks them.
    """
    with open(task_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract task information
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Untitled Task"

    # Extract complexity
    complexity_match = re.search(r'Complexity:?\s*(\d+)', content)
    if complexity_match:
        complexity = int(complexity_match.group(1))
    else:
        # Estimate complexity based on content length
        complexity = min(10, max(1, len(content) // 1000))

    # Generate appropriate subtasks based on complexity
    if complexity >= 7:
        # High complexity tasks get detailed subtasks
        subtasks_section = f"""## Sub-subtasks Breakdown

### 1.1: Research and Planning
- Research requirements for {title}
- Plan implementation approach
- Identify potential challenges and risks

### 1.2: Implementation
- Implement core functionality
- Write unit tests
- Handle error cases

### 1.3: Integration and Testing
- Integrate with existing components
- Perform integration testing
- Validate against requirements

### 1.4: Documentation and Review
- Document implementation details
- Conduct code review
- Update relevant documentation

"""
    elif complexity >= 4:
        # Medium complexity tasks get moderate subtasks
        subtasks_section = f"""## Sub-subtasks Breakdown

### 1.1: Implementation
- Implement {title}
- Write tests for functionality
- Handle edge cases

### 1.2: Testing and Validation
- Test implementation against requirements
- Validate error handling
- Verify functionality works as expected

### 1.3: Documentation
- Document changes made
- Update relevant documentation
- Add comments to code if applicable

"""
    else:
        # Low complexity tasks get simple subtasks
        subtasks_section = f"""## Sub-subtasks Breakdown

### 1.1: Execute Task
- Complete {title}
- Verify completion
- Update status

"""

    # Find a good place to insert the subtasks section
    # Look for the end of the main content before the final sections
    insertion_points = [
        r'\n---\n',
        r'\n## Test Strategy',
        r'\n## Testing Strategy',
        r'\n## Implementation Notes',
        r'\n## Implementation Guide',
        r'\n## Progress Log',
        r'\n## Next Steps',
        r'\n## Done Definition',
        r'\n## Next Steps'
    ]

    insertion_point = len(content)  # Default to end of file

    for pattern in insertion_points:
        match = re.search(pattern, content)
        if match:
            insertion_point = min(insertion_point, match.start())

    # Insert the subtasks section
    new_content = content[:insertion_point] + "\n" + subtasks_section + "\n" + content[insertion_point:]

    return new_content


def main():
    # Find task files that don't have subtasks
    tasks_dir = Path("/home/masum/github/PR/.taskmaster/tasks")
    all_task_files = list(tasks_dir.glob("task*.md"))

    # Identify tasks without subtasks sections
    tasks_without_subtasks = []
    for task_file in all_task_files:
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if task has subtasks section by looking for common patterns
        has_subtasks = (
            'Sub-subtasks' in content or 
            'Subtasks Breakdown' in content or
            '## Subtasks' in content or
            re.search(r'### \d+\.\d+:?', content)  # Look for subtask-style headers
        )
        
        if not has_subtasks:
            # Extract complexity to determine if it needs subtasks
            complexity_match = re.search(r'Complexity:?\s*(\d+)', content)
            if complexity_match:
                complexity = int(complexity_match.group(1))
                if complexity >= 4:  # Only add subtasks to medium+ complexity tasks
                    tasks_without_subtasks.append(task_file)
            else:
                # If no complexity specified, add to list for manual review
                tasks_without_subtasks.append(task_file)

    print(f"Found {len(tasks_without_subtasks)} tasks without subtasks")

    # Process each task without subtasks
    updated_count = 0
    for task_file in tasks_without_subtasks:
        print(f"Adding subtasks to: {task_file.name}")

        try:
            # Generate new content with subtasks
            new_content = add_subtasks_to_task(str(task_file))

            # Create backup
            backup_path = task_file.with_suffix(f'.md.backup_before_subtasks_{updated_count+1}')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(open(task_file, 'r', encoding='utf-8').read())

            # Write new content
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"  ✓ Added subtasks to {task_file.name}")
            updated_count += 1

        except Exception as e:
            print(f"  ✗ Error processing {task_file.name}: {e}")

    print(f"\nSuccessfully updated {updated_count} tasks with subtasks")
    print("Subtasks have been added to tasks that lacked them to improve task manageability.")
    print("This will help break down complex tasks into manageable pieces for better tracking and implementation.")

    return 0


if __name__ == "__main__":
    exit(main())