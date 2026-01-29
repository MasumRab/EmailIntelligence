#!/usr/bin/env python3
"""
Reorganization Implementation: Bring Branch Analysis Forward in Task Flow

This script implements the reorganization plan to make branch analysis available earlier
in the workflow, maximizing PRD accuracy by having branch analysis data available upfront.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any
import sys


def analyze_task_dependencies(task_id: str) -> Dict[str, Any]:
    """
    Analyze the actual dependencies of a task to determine if they're essential.
    """
    task_file = Path(f"tasks/task-{task_id}.md")
    if not task_file.exists():
        print(f"Task file not found: {task_file}")
        return {}
    
    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract dependencies from the task file
    dependencies_match = re.search(r'Dependencies:\s*(.+?)(?:\n|$)', content)
    if dependencies_match:
        dependencies = dependencies_match.group(1).strip()
        # Parse the dependencies string
        deps_list = [dep.strip() for dep in dependencies.split(',')]
        deps_list = [dep for dep in deps_list if dep and dep.lower() not in ['none', 'null', '']]
        return {
            'task_id': task_id,
            'original_dependencies': dependencies,
            'parsed_dependencies': deps_list,
            'content': content
        }
    
    return {
        'task_id': task_id,
        'original_dependencies': 'None',
        'parsed_dependencies': [],
        'content': content
    }


def update_task_dependencies(task_id: str, new_dependencies: List[str]) -> bool:
    """
    Update the dependencies of a task.
    """
    task_file = Path(f"tasks/task-{task_id}.md")
    if not task_file.exists():
        print(f"Task file not found: {task_file}")
        return False

    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update the dependencies field
    if new_dependencies:
        new_deps_str = ', '.join(new_dependencies)
        updated_content = re.sub(
            r'(\*\*Dependencies:\*\*\s*).+?(\n)',
            f'**Dependencies:** {new_deps_str}\\2',
            content
        )
        # If no match, add the dependencies field
        if updated_content == content:
            # Find the position to insert dependencies (after status, priority, etc.)
            insert_pos = content.find('\n\n**Description:')
            if insert_pos == -1:
                insert_pos = content.find('\n\n**Details:')
            if insert_pos == -1:
                insert_pos = content.find('\n\n---')
            if insert_pos == -1:
                insert_pos = content.find('\n\n## ')
            if insert_pos != -1:
                updated_content = content[:insert_pos] + f"\n**Dependencies:** {new_deps_str}" + content[insert_pos:]
            else:
                # If no good position found, add at the beginning after the header
                header_end = content.find('\n\n')
                if header_end != -1:
                    updated_content = content[:header_end] + f"\n**Dependencies:** {new_deps_str}" + content[header_end:]
    else:
        # Remove dependencies or set to None
        updated_content = re.sub(
            r'(\*\*Dependencies:\*\*\s*).+?(\n)',
            '**Dependencies:** None\n',
            content
        )

    # Create backup
    backup_path = task_file.with_suffix(f'.md.backup_before_reorg_{task_id}')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Write updated content
    with open(task_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"Updated dependencies for Task {task_id}: {new_dependencies}")
    return True


def update_task_relationships():
    """
    Update the relationships between tasks to bring branch analysis forward.
    """
    print("Analyzing current task relationships...")
    
    # Analyze Task 007 dependencies
    task_007_info = analyze_task_dependencies("007")
    print(f"Task 007 current dependencies: {task_007_info.get('parsed_dependencies', [])}")
    
    # Analyze Task 002 dependencies
    task_002_info = analyze_task_dependencies("002")
    print(f"Task 002 current dependencies: {task_002_info.get('parsed_dependencies', [])}")
    
    # Analyze Task 004 dependencies
    task_004_info = analyze_task_dependencies("004")
    print(f"Task 004 current dependencies: {task_004_info.get('parsed_dependencies', [])}")
    
    # Based on our analysis, Task 007 should not depend on Task 004 if we want to bring it forward
    # The original documentation says Task 007 was merged into Task 002.6 as execution mode
    # So we should update Task 007 to have no dependencies or minimal dependencies
    
    print("\nReorganizing task dependencies to bring branch analysis forward...")
    
    # Update Task 007 to have no dependencies (since its functionality is integrated into Task 002.6)
    # Actually, let's update this more carefully - we need to understand the real relationship
    # According to the original documentation, Task 007 was merged into Task 002.6
    # So we should update Task 007 to reflect that it's part of Task 002
    
    # Update Task 007 dependencies to be consistent with its role as execution mode of Task 002.6
    # Task 002.6 depends on Task 002.5, and Task 002.5 depends on Task 002.4, etc.
    # So Task 007 (as execution mode) should be available after Task 002.1-002.3 are complete
    
    # Update Task 007 to have minimal dependencies
    update_task_dependencies("007", ["001"])  # Make it depend on Task 001 instead of 004
    
    # Update Task 004 to reflect that it uses branch analysis results
    # Task 004 should be updated to show it can use results from Task 002/007
    task_004_file = Path("tasks/task-004.md")
    if task_004_file.exists():
        with open(task_004_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add a note about using branch analysis results
        if "branch analysis" not in content.lower():
            # Find a good place to add this information
            # Look for the details section
            details_match = re.search(r'(\*\*Details:\*\*\s*)([\s\S]*?)(?=\n\*\*|\n---|\Z)', content)
            if details_match:
                details_section = details_match.group(2)
                # Add information about using branch analysis
                updated_details = details_section + "\n\nThis task utilizes branch analysis results from Task 002/007 to inform framework configuration decisions."
                
                updated_content = content.replace(details_section, updated_details)
                
                # Create backup
                backup_path = task_004_file.with_suffix('.md.backup_before_reorg_004')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Write updated content
                with open(task_004_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

                print("Updated Task 004 to reference branch analysis results")
    
    # Update Task 002.6 to clarify its role as the integration point for Task 007
    task_002_6_file = Path("tasks/task-002-6.md")
    if task_002_6_file.exists():
        with open(task_002_6_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add clarification about Task 007 execution mode
        if "Task 007 execution mode" not in content:
            # Find a good place to add this information
            purpose_match = re.search(r'(\*\*Purpose:\*\*\s*)([\s\S]*?)(?=\n\*\*|\n---|\Z)', content)
            if purpose_match:
                purpose_section = purpose_match.group(2)
                # Add information about Task 007 execution mode
                updated_purpose = purpose_section + "\n\nThis subtask also implements Task 007 (Feature Branch Identification) as an execution mode, making branch analysis capabilities available through the pipeline integration."
                
                updated_content = content.replace(purpose_section, updated_purpose)
                
                # Create backup
                backup_path = task_002_6_file.with_suffix('.md.backup_before_reorg_002_6')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Write updated content
                with open(task_002_6_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print("Updated Task 002.6 to clarify Task 007 execution mode")
    
    print("\nTask dependency reorganization completed successfully!")
    print("Branch analysis capabilities are now positioned earlier in the workflow.")
    print("Task 007 no longer blocked by Task 004, allowing earlier availability of branch analysis.")
    print("Task 004 updated to utilize branch analysis results when available.")


def update_workflow_documentation():
    """
    Update workflow documentation to reflect the reorganization.
    """
    print("Updating workflow documentation...")
    
    # Update the main workflow documentation
    workflow_docs = [
        Path("TASK_FLOW_OVERVIEW.md"),
        Path("WORKFLOW_DOCUMENTATION.md"),
        Path("IMPLEMENTATION_INDEX.md"),
        Path("README.md")
    ]
    
    for doc_path in workflow_docs:
        if doc_path.exists():
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update any references to the old workflow
            updated_content = content
            
            # Add information about the reorganization
            if "reorganization" not in content.lower() and "branch analysis" in content.lower():
                # Add a note about the reorganization at the beginning
                reorg_note = """<!-- REORGANIZATION NOTE: 
Branch analysis tasks (Task 002 and Task 007) have been reorganized to run earlier in the workflow 
for improved PRD accuracy. Task 007 functionality is now available as an execution mode of Task 002.6.
This allows branch identification and categorization to be available earlier in the process.
-->
"""
                updated_content = reorg_note + content
            
            # Create backup and update
            backup_path = doc_path.with_suffix(f'.md.backup_before_reorg')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Updated workflow documentation: {doc_path.name}")
    
    # If no workflow docs exist, create a new one
    reorg_doc_path = Path("BRANCH_ANALYSIS_REORGANIZATION.md")
    if not reorg_doc_path.exists():
        reorg_doc_content = """# Branch Analysis Reorganization

## Overview
This document describes the reorganization of branch analysis tasks to improve PRD accuracy by making branch analysis available earlier in the workflow.

## Changes Made
- Task 007 (Feature Branch Identification) dependencies reduced from Task 004 to allow earlier execution
- Task 002.6 (Pipeline Integration) updated to clarify its role as the execution point for Task 007
- Task 004 (Core Framework) updated to reference branch analysis results when available

## New Workflow
```
Task 001 ──┐
            ├── (both run in parallel)
Task 002 ──┤    └─ Task 007 functionality available early
            │
Task 004 ──┤    ┌─ Uses Task 007 results when available
            └────┘
Task 005 ── Task 006
```

## Benefits
- Branch analysis available earlier in the process
- Improved PRD accuracy with actual branch data
- Better planning decisions based on real analysis
- Reduced bottlenecks in the workflow
"""
        
        with open(reorg_doc_path, 'w', encoding='utf-8') as f:
            f.write(reorg_doc_content)
        
        print(f"Created new reorganization documentation: {reorg_doc_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Reorganize task dependencies to bring branch analysis forward")
    parser.add_argument("--apply", action="store_true", help="Apply the reorganization changes")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without applying")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN: Showing what would be changed without applying")
        print("Analyzing current task relationships...")
        
        task_007_info = analyze_task_dependencies("007")
        print(f"Task 007 current dependencies: {task_007_info.get('parsed_dependencies', [])}")
        
        task_004_info = analyze_task_dependencies("004")
        print(f"Task 004 current dependencies: {task_004_info.get('parsed_dependencies', [])}")
        
        print("\nWould update Task 007 to have minimal dependencies")
        print("Would update Task 004 to reference branch analysis results")
        print("Would update Task 002.6 to clarify Task 007 execution mode")
        print("Would update workflow documentation")
        
        return 0
    
    if not args.apply:
        print("Use --apply to execute the reorganization or --dry-run to see changes")
        return 1
    
    print("Starting task reorganization to bring branch analysis forward...")
    
    # Update task relationships
    update_task_relationships()

    # Update documentation
    update_workflow_documentation()
    
    print("\nReorganization completed successfully!")
    print("Branch analysis capabilities are now available earlier in the workflow.")
    print("This will improve PRD accuracy by providing actual branch analysis data upfront.")
    
    return 0


if __name__ == "__main__":
    exit(main())