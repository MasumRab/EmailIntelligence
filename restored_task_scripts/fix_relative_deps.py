#!/usr/bin/env python3
"""
Fix Relative Dependencies in Task Files

This script fixes relative dependency references in task files,
converting them to proper absolute references and ensuring
dependency consistency.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Union
from collections import defaultdict

def resolve_relative_dependency(task_id: Union[str, int], relative_ref: str, all_tasks: List[Dict[str, Any]]) -> Union[str, int, None]:
    """
    Resolve a relative dependency reference to an absolute task ID.
    
    Relative references can be:
    - '+1', '+2', etc. (next task(s))
    - '-1', '-2', etc. (previous task(s))
    - '^1', '^2', etc. (parent task levels)
    """
    if isinstance(relative_ref, str):
        if relative_ref.startswith(('+', '-')):
            try:
                offset = int(relative_ref)
                target_index = None
                
                # Find current task index
                current_index = None
                for i, task in enumerate(all_tasks):
                    if str(task.get('id')) == str(task_id):
                        current_index = i
                        break
                
                if current_index is not None:
                    target_index = current_index + offset
                    if 0 <= target_index < len(all_tasks):
                        target_task = all_tasks[target_index]
                        return target_task.get('id')
            except ValueError:
                pass  # Not a numeric offset
        elif relative_ref.startswith('^'):
            # Handle parent/ancestor references (implementation depends on your hierarchy structure)
            # This is a placeholder - implement based on your specific hierarchy needs
            pass
    
    return None

def normalize_dependency(dep: Any) -> Union[str, int]:
    """Normalize a dependency to a consistent format"""
    if isinstance(dep, (str, int)):
        # Try to convert string numbers to integers
        if isinstance(dep, str) and dep.isdigit():
            return int(dep)
        return dep
    return str(dep)

def fix_dependencies_in_task(task: Dict[str, Any], all_tasks: List[Dict[str, Any]], task_id_map: Dict[Union[str, int], Dict[str, Any]]) -> Dict[str, Any]:
    """Fix dependencies in a single task"""
    if 'dependencies' not in task or not isinstance(task['dependencies'], list):
        return task
    
    original_deps = task['dependencies']
    fixed_deps = []
    resolved_deps = []
    
    for dep in original_deps:
        normalized_dep = normalize_dependency(dep)
        
        # Check if this is a relative reference
        if isinstance(normalized_dep, str) and (normalized_dep.startswith(('+', '-')) or normalized_dep.startswith('^')):
            resolved = resolve_relative_dependency(task.get('id'), normalized_dep, all_tasks)
            if resolved is not None:
                resolved_deps.append(f"{normalized_dep} -> {resolved}")
                fixed_deps.append(resolved)
            else:
                print(f"  - Could not resolve relative dependency '{normalized_dep}' for task {task.get('id')}")
                fixed_deps.append(normalized_dep)  # Keep original if can't resolve
        else:
            # Check if dependency exists
            if normalized_dep not in task_id_map:
                print(f"  - Warning: Dependency '{normalized_dep}' not found for task {task.get('id')}")
            fixed_deps.append(normalized_dep)
    
    task['dependencies'] = fixed_deps
    
    if resolved_deps:
        print(f"  - Resolved relative dependencies for task {task.get('id')}: {', '.join(resolved_deps)}")
    
    return task

def validate_dependency_consistency(tasks: List[Dict[str, Any]]) -> List[str]:
    """Validate dependency consistency and return warnings"""
    warnings = []
    task_id_map = {task.get('id'): task for task in tasks if isinstance(task, dict) and 'id' in task}
    
    for task in tasks:
        if not isinstance(task, dict) or 'id' not in task or 'dependencies' not in task:
            continue
        
        task_id = task['id']
        deps = task['dependencies']
        
        if not isinstance(deps, list):
            continue
        
        for dep in deps:
            if dep not in task_id_map:
                warnings.append(f"Task {task_id} depends on non-existent task {dep}")
            elif dep == task_id:
                warnings.append(f"Task {task_id} has circular dependency on itself")
    
    # Check for circular dependencies
    try:
        from collections import deque
        
        for task in tasks:
            if not isinstance(task, dict) or 'id' not in task or 'dependencies' not in task:
                continue
            
            task_id = task['id']
            deps = task.get('dependencies', [])
            
            if task_id in deps:
                warnings.append(f"Circular dependency: Task {task_id} depends on itself")
                continue
            
            # Simple cycle detection using BFS
            visited = set()
            queue = deque([task_id])
            
            while queue:
                current = queue.popleft()
                if current in visited:
                    warnings.append(f"Circular dependency detected involving task {task_id}")
                    break
                visited.add(current)
                
                current_task = task_id_map.get(current)
                if current_task and 'dependencies' in current_task:
                    for dep in current_task['dependencies']:
                        if dep in task_id_map and dep not in visited:
                            queue.append(dep)
    except:
        # If cycle detection fails, continue with other validations
        pass
    
    return warnings

def fix_task_file(filepath: str) -> bool:
    """Fix relative dependencies in a task file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict) or 'tasks' not in data:
            print(f"Warning: {filepath} does not have a valid tasks structure")
            return False
        
        tasks = data['tasks']
        if not isinstance(tasks, list):
            print(f"Warning: {filepath} tasks is not an array")
            return False
        
        # Create task ID map for quick lookup
        task_id_map = {}
        for task in tasks:
            if isinstance(task, dict) and 'id' in task:
                task_id_map[task['id']] = task
        
        modified = False
        
        # Fix dependencies in each task
        for i, task in enumerate(tasks):
            if not isinstance(task, dict):
                print(f"Warning: Task at index {i} is not an object, skipping")
                continue
            
            original_task = task.copy()
            updated_task = fix_dependencies_in_task(task, tasks, task_id_map)
            
            if updated_task != original_task:
                tasks[i] = updated_task
                modified = True
        
        # Validate dependency consistency
        warnings = validate_dependency_consistency(tasks)
        for warning in warnings:
            print(f"  - Dependency warning: {warning}")
        
        if modified or warnings:
            # Create backup
            backup_path = f"{filepath}.backup_{int(os.path.getmtime(filepath))}"
            os.rename(filepath, backup_path)
            print(f"  - Created backup: {backup_path}")
            
            # Write updated file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  - Updated: {filepath}")
        else:
            print(f"  - No changes needed: {filepath}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def process_directory(directory: str, pattern: str = "**/tasks.json"):
    """Process all task files in a directory"""
    dir_path = Path(directory)
    task_files = list(dir_path.glob(pattern))
    
    print(f"Found {len(task_files)} task files to process")
    
    success_count = 0
    for task_file in task_files:
        print(f"Processing: {task_file}")
        if fix_task_file(str(task_file)):
            success_count += 1
    
    print(f"\nProcessed {success_count}/{len(task_files)} files successfully")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix relative dependencies in task files')
    parser.add_argument('path', nargs='?', default='.', help='Path to process (file or directory)')
    parser.add_argument('--pattern', default='**/tasks.json', help='File pattern to match (for directories)')
    parser.add_argument('--file', help='Specific file to process (alternative to path)')
    
    args = parser.parse_args()
    
    path_to_process = args.file or args.path
    
    if os.path.isfile(path_to_process):
        print(f"Processing single file: {path_to_process}")
        success = fix_task_file(path_to_process)
        if success:
            print("File processed successfully")
        else:
            print("Failed to process file")
            sys.exit(1)
    elif os.path.isdir(path_to_process):
        print(f"Processing directory: {path_to_process}")
        process_directory(path_to_process, args.pattern)
    else:
        print(f"Error: Path does not exist: {path_to_process}")
        sys.exit(1)

if __name__ == "__main__":
    main()