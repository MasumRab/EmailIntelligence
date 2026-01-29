#!/usr/bin/env python3
"""
Deprecation Script for Task 007
Since Task 007's functionality was merged into Task 002.6 as an execution mode,
Task 007 is now redundant and should be deprecated to avoid confusion.
"""

import argparse
import json
from pathlib import Path
import shutil
from datetime import datetime


def deprecate_task_007():
    """
    Deprecate Task 007 since its functionality is now part of Task 002.6
    """
    print("Deprecating Task 007 - functionality merged into Task 002.6")
    
    task_007_path = Path("tasks/task-007.md")
    
    if not task_007_path.exists():
        print(f"Task 007 file not found at {task_007_path}")
        return False
    
    # Read the current Task 007 content
    with open(task_007_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Create a deprecated version that redirects to Task 002.6
    deprecated_content = f"""# DEPRECATED: Task 007 - Feature Branch Identification and Categorization Tool

**STATUS: DEPRECATED** - This task's functionality has been merged into Task 002.6 as an execution mode
**New Location:** Task 002.6 (PipelineIntegration) - Feature Branch Identification execution mode
**Deprecation Date:** {datetime.now().strftime('%Y-%m-%d')}
**Reason:** Functionality consolidated into Task 002.6 for better integration and reduced redundancy

---

## Deprecation Notice

This task (Task 007) is **deprecated** as its functionality has been fully integrated into Task 002.6 (PipelineIntegration) as an execution mode. 

### Original Purpose (Now in Task 002.6):
Create a Python tool to automatically identify active feature branches, analyze their Git history, and suggest the optimal primary branch target (main, scientific, or orchestration-tools) based on codebase similarity and shared history.

### New Implementation Location:
All functionality from Task 007 is now available as part of Task 002.6 under the \"Task 007 feature branch ID mode\".

### Migration Instructions:
- Refer to Task 002.6 for feature branch identification and categorization
- Any workflows that previously referenced Task 007 should now reference Task 002.6
- The feature branch identification functionality is executed as an integrated mode within the pipeline integration task

### Original Task Details:
{original_content}

---

## Redirect Information

**Use Instead:** Task 002.6 - Pipeline Integration (with Task 007 execution mode)
**Equivalent Functionality:** Available in Task 002.6 under the feature branch identification execution mode
**Integration Point:** The branch identification functionality is now tightly integrated with the pipeline, providing better coordination and reduced overhead
"""
    
    # Create backup of original file
    backup_path = task_007_path.with_suffix('.md.backup_deprecated_007')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)

    # Write the deprecated content
    with open(task_007_path, 'w', encoding='utf-8') as f:
        f.write(deprecated_content)

    print(f"Task 007 has been deprecated and redirected to Task 002.6")
    print(f"Original content backed up to: {backup_path}")
    print(f"Updated Task 007 with deprecation notice and redirect information")

    # Also update any references to Task 007 in other tasks to point to Task 002.6
    update_references_to_task_007()

    return True


def update_references_to_task_007():
    """
    Update references to Task 007 in other task files to indicate the deprecation
    and redirect to Task 002.6 where appropriate
    """
    print("Updating references to deprecated Task 007...")
    
    # Find all task files
    task_files = Path("tasks").glob("task-*.md")
    
    for task_file in task_files:
        if task_file.name == "task-007.md":  # Skip the deprecated file itself
            continue
            
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this file references Task 007
        if "Task 007" in content or "task-007" in content or "007" in content:
            # Create backup
            backup_path = task_file.with_suffix(f'.md.backup_ref_update_{task_file.stem}')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Add a note about Task 007 deprecation if not already present
            if "DEPRECATED" not in content and "deprecated" not in content.lower():
                # Add a note at the top of any dependencies section that mentions Task 007
                updated_content = content
                
                # Look for places where Task 007 is referenced as a dependency
                import re
                updated_content = re.sub(
                    r'(Dependencies:.*?)(007)(.*?)(?=\n|\Z)',
                    r'\1~~007~~ (DEPRECATED: Use 002.6 instead)\3',
                    updated_content
                )
                
                # Write updated content
                with open(task_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"  Updated references in {task_file.name}")
    
    print("Reference updates completed.")


def update_project_documentation():
    """
    Update project documentation to reflect Task 007 deprecation
    """
    print("Updating project documentation to reflect Task 007 deprecation...")
    
    # Update any documentation that mentions Task 007 as a separate entity
    docs_to_check = [
        Path("README.md"),
        Path("TASK_STRUCTURE_STANDARD.md"),
        Path("IMPLEMENTATION_INDEX.md"),
        Path("BRANCH_ANALYSIS_REORGANIZATION.md"),
        Path("PERFECT_FIDELITY_PROCESS_DOCUMENTATION.md"),
        Path("PLANNING_TASK_UPDATES.md")
    ]
    
    for doc_path in docs_to_check:
        if doc_path.exists():
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if the document mentions Task 007 as a separate task
            if "Task 007" in content and "002.6" not in content.split(doc_path.name)[0] + content.split(doc_path.name)[-1]:
                # Create backup
                backup_path = doc_path.with_suffix(f'.md.backup_update_{doc_path.stem}')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Add information about Task 007 deprecation
                if "deprecation" not in content.lower() and "deprecated" not in content.lower():
                    # Add a note about the deprecation
                    deprecation_note = f"\n\n> **NOTE**: Task 007 functionality has been merged into Task 002.6 as an execution mode. Refer to Task 002.6 for feature branch identification and categorization capabilities.\n\n"
                    
                    # Insert after the first header or at the beginning
                    if content.startswith('#'):
                        first_header_end = content.find('\n\n')  # End of first section
                        if first_header_end != -1:
                            updated_content = content[:first_header_end] + deprecation_note + content[first_header_end:]
                        else:
                            updated_content = content + deprecation_note
                    else:
                        updated_content = deprecation_note + content
                    
                    with open(doc_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    print(f"  Updated documentation: {doc_path.name}")
    
    print("Project documentation updates completed.")


def main():
    parser = argparse.ArgumentParser(description="Deprecate Task 007 since its functionality is merged into Task 002.6")
    parser.add_argument("--apply", action="store_true", help="Apply the deprecation changes")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without applying")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN: Would deprecate Task 007 and update references")
        print("- Mark Task 007 as deprecated with redirect to Task 002.6")
        print("- Update references in other task files")
        print("- Update project documentation")
        print("- Create backups of all modified files")
        return 0
    
    if not args.apply:
        print("Use --apply to execute the deprecation or --dry-run to see changes")
        return 1
    
    print("Starting Task 007 deprecation process...")
    print("Task 007 functionality was merged into Task 002.6 as execution mode.")
    print("Deprecating Task 007 to eliminate redundancy and confusion.")
    
    # Deprecate Task 007
    success = deprecate_task_007()
    
    if success:
        # Update references to Task 007
        update_references_to_task_007()
        
        # Update project documentation
        update_project_documentation()
        
        print("\nTask 007 deprecation completed successfully!")
        print("The system now properly reflects that Task 007 functionality is available in Task 002.6.")
        print("This eliminates redundancy and clarifies the task workflow.")
        
        return 0
    else:
        print("\nTask 007 deprecation failed!")
        return 1


if __name__ == "__main__":
    exit(main())