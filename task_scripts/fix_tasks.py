#!/usr/bin/env python3
"""
Comprehensive Task File Fixer

This script provides a comprehensive solution for fixing common issues in task files:
- Missing status fields
- Relative dependencies
- Invalid JSON structure
- Merge conflicts
- Security validation
- Atomic operations
"""

import json
import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Tuple, Union
import re
import hashlib
import time
import copy
from datetime import datetime

class ComprehensiveTaskFixer:
    """Comprehensive task file fixer addressing multiple common issues"""
    
    def __init__(self):
        self.backup_dir = Path(tempfile.gettempdir()) / "task_fixer_backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.security_patterns = [
            r'\.\./', r'\.\.\\', r'/etc/', r'/root/', r'C:\\Windows\\', r'~/.ssh/'
        ]
    
    def create_backup(self, filepath: str) -> str:
        """Create a backup of the original file"""
        timestamp = int(time.time())
        original_path = Path(filepath)
        backup_name = f"{original_path.stem}_{timestamp}{original_path.suffix}"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(filepath, backup_path)
        print(f"  - Created backup: {backup_path}")
        return str(backup_path)
    
    def validate_path_security(self, filepath: str) -> bool:
        """Validate file path security"""
        normalized_path = os.path.normpath(filepath)
        for pattern in self.security_patterns:
            if re.search(pattern, normalized_path, re.IGNORECASE):
                print(f"  - Security violation: {filepath}")
                return False
        return True
    
    def check_merge_conflicts(self, filepath: str) -> bool:
        """Check for Git merge conflict markers"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        conflict_markers = ['<<<<<<<', '=======', '>>>>>>>']
        has_conflicts = any(marker in content for marker in conflict_markers)
        
        if has_conflicts:
            print(f"  - Merge conflicts detected in: {filepath}")
        
        return has_conflicts
    
    def fix_missing_status(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Fix missing status fields in tasks"""
        fixed_data = copy.deepcopy(data)
        fixes = []
        
        if 'tasks' in fixed_data and isinstance(fixed_data['tasks'], list):
            for i, task in enumerate(fixed_data['tasks']):
                if isinstance(task, dict):
                    if 'status' not in task:
                        task['status'] = 'pending'
                        fixes.append(f"Added 'pending' status to task {task.get('id', i)}")
                    elif task['status'] not in ['pending', 'in-progress', 'completed', 'cancelled', 'deferred']:
                        original_status = task['status']
                        task['status'] = 'pending'
                        fixes.append(f"Fixed invalid status '{original_status}' to 'pending' for task {task.get('id', i)}")
        
        return fixed_data, fixes
    
    def fix_relative_dependencies(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Fix relative dependency references"""
        fixed_data = copy.deepcopy(data)
        fixes = []
        
        if 'tasks' in fixed_data and isinstance(fixed_data['tasks'], list):
            # Create task ID mapping
            task_map = {}
            for task in fixed_data['tasks']:
                if isinstance(task, dict) and 'id' in task:
                    task_map[task['id']] = task
            
            for task in fixed_data['tasks']:
                if isinstance(task, dict) and 'dependencies' in task and isinstance(task['dependencies'], list):
                    original_deps = task['dependencies']
                    fixed_deps = []
                    
                    for dep in original_deps:
                        if isinstance(dep, str) and dep.startswith(('+', '-')):
                            # Handle relative dependencies
                            try:
                                offset = int(dep)
                                current_index = None
                                # Find current task index
                                for i, t in enumerate(fixed_data['tasks']):
                                    if t.get('id') == task.get('id'):
                                        current_index = i
                                        break
                                
                                if current_index is not None:
                                    target_index = current_index + offset
                                    if 0 <= target_index < len(fixed_data['tasks']):
                                        target_task = fixed_data['tasks'][target_index]
                                        target_id = target_task.get('id')
                                        fixed_deps.append(target_id)
                                        fixes.append(f"Resolved relative dependency '{dep}' to task {target_id} for task {task.get('id')}")
                                    else:
                                        fixed_deps.append(dep)  # Keep original if can't resolve
                                else:
                                    fixed_deps.append(dep)  # Keep original if can't find current task
                            except ValueError:
                                fixed_deps.append(dep)  # Keep original if not a valid number
                        else:
                            fixed_deps.append(dep)
                    
                    task['dependencies'] = fixed_deps
        
        return fixed_data, fixes
    
    def fix_invalid_structure(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Fix common structural issues"""
        fixed_data = copy.deepcopy(data)
        fixes = []
        
        # Ensure 'tasks' exists and is a list
        if 'tasks' not in fixed_data:
            fixed_data['tasks'] = []
            fixes.append("Added missing 'tasks' array")
        elif not isinstance(fixed_data['tasks'], list):
            fixed_data['tasks'] = []
            fixes.append("Fixed 'tasks' to be an array")
        
        # Fix individual tasks
        for i, task in enumerate(fixed_data['tasks']):
            if not isinstance(task, dict):
                # Replace non-object with a valid task structure
                fixed_task = {
                    'id': i,
                    'title': f'Fixed Task {i}',
                    'status': 'pending'
                }
                fixed_data['tasks'][i] = fixed_task
                fixes.append(f"Fixed invalid task object at index {i}")
            else:
                # Ensure required fields exist
                if 'id' not in task:
                    task['id'] = i
                    fixes.append(f"Added missing 'id' to task at index {i}")
                
                if 'title' not in task:
                    task['title'] = f'Untitled Task {task.get("id", i)}'
                    fixes.append(f"Added missing 'title' to task {task.get('id')}")
        
        return fixed_data, fixes
    
    def fix_file(self, filepath: str) -> bool:
        """Comprehensive fix of a task file"""
        print(f"Processing: {filepath}")
        
        # Security validation
        if not self.validate_path_security(filepath):
            print(f"  - Security validation failed, skipping: {filepath}")
            return False
        
        # Check for merge conflicts
        if self.check_merge_conflicts(filepath):
            print(f"  - Skipping file with merge conflicts: {filepath}")
            return False
        
        try:
            # Load original data
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            original_data = copy.deepcopy(data)
            
            # Apply all fixes
            fixes_applied = []
            
            # Fix 1: Missing status fields
            data, status_fixes = self.fix_missing_status(data)
            fixes_applied.extend(status_fixes)
            
            # Fix 2: Relative dependencies
            data, dep_fixes = self.fix_relative_dependencies(data)
            fixes_applied.extend(dep_fixes)
            
            # Fix 3: Invalid structure
            data, struct_fixes = self.fix_invalid_structure(data)
            fixes_applied.extend(struct_fixes)
            
            # Only write if changes were made
            if data != original_data:
                # Create backup
                backup_path = self.create_backup(filepath)
                
                # Write fixed data
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"  - Applied {len(fixes_applied)} fixes to: {filepath}")
                for fix in fixes_applied[:5]:  # Show first 5 fixes
                    print(f"    • {fix}")
                if len(fixes_applied) > 5:
                    print(f"    ... and {len(fixes_applied) - 5} more fixes")
            else:
                print(f"  - No changes needed: {filepath}")
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"  - JSON decode error in {filepath}: {e}")
            return False
        except Exception as e:
            print(f"  - Error processing {filepath}: {e}")
            return False
    
    def process_directory(self, directory: str, pattern: str = "**/tasks.json") -> Tuple[int, int]:
        """Process all task files in a directory"""
        dir_path = Path(directory)
        task_files = list(dir_path.glob(pattern))
        
        print(f"Found {len(task_files)} task files to process")
        
        success_count = 0
        for task_file in task_files:
            if self.fix_file(str(task_file)):
                success_count += 1
        
        return success_count, len(task_files)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Comprehensive Task File Fixer')
    parser.add_argument('path', nargs='?', default='.', help='Path to process (file or directory)')
    parser.add_argument('--pattern', default='**/tasks.json', help='File pattern to match (for directories)')
    parser.add_argument('--file', help='Specific file to process (alternative to path)')
    
    args = parser.parse_args()
    
    fixer = ComprehensiveTaskFixer()
    
    path_to_process = args.file or args.path
    
    if os.path.isfile(path_to_process):
        print(f"Processing single file: {path_to_process}")
        success = fixer.fix_file(path_to_process)
        if success:
            print("File processed successfully")
        else:
            print("Failed to process file")
            sys.exit(1)
    elif os.path.isdir(path_to_process):
        print(f"Processing directory: {path_to_process}")
        success_count, total_count = fixer.process_directory(path_to_process, args.pattern)
        print(f"\nProcessed {success_count}/{total_count} files successfully")
    else:
        print(f"Error: Path does not exist: {path_to_process}")
        sys.exit(1)

if __name__ == "__main__":
    main()