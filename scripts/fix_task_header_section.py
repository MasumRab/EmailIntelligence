#!/usr/bin/env python3
"""
Fix Task Header Section in MD Files

This script adds the missing 'Task Header' section to MD files that have the header information
but lack the proper section heading as required by the 14-section standard.
"""

import re
from pathlib import Path


def fix_task_header_section(file_path: Path):
    """Fix the missing Task Header section in a task file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if the file already has a Task Header section
    if '## Task Header' in content or '# Task Header' in content:
        print(f"ℹ️  {file_path.name}: Already has Task Header section")
        return False
    
    # Look for the current header pattern (title followed by metadata)
    header_pattern = r'^(# Task.*?\n(?:\*\*.*?\*\*.*?\n)*\n?)'
    match = re.match(header_pattern, content, re.MULTILINE)
    
    if match:
        header_content = match.group(1)
        
        # Create the proper Task Header section
        new_content = '## Task Header\n\n' + header_content + '\n' + content[len(header_content):]
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {file_path.name}: Added Task Header section")
        return True
    else:
        print(f"⚠️  {file_path.name}: Could not identify header pattern to convert")
        return False


def main():
    """Main function to process all task files."""
    print("🔧 Fixing Task Header sections in MD files...")
    
    tasks_dir = Path("tasks")
    task_files = list(tasks_dir.glob("task*.md"))
    
    if not task_files:
        print("No task files found in tasks/ directory")
        return 1
    
    fixed_count = 0
    for task_file in task_files:
        try:
            if fix_task_header_section(task_file):
                fixed_count += 1
        except Exception as e:
            print(f"❌ Error processing {task_file.name}: {e}")
    
    print(f"\n✅ Fixed Task Header sections in {fixed_count} files")
    print("Files now comply with the 14-section standard format.")
    
    return 0


if __name__ == "__main__":
    exit(main())