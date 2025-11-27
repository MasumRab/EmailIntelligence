#!/usr/bin/env python3
"""
Validate Task Master tasks.json file for structural issues, dependencies, and consistency.
"""
import json
import sys
from collections import defaultdict

def validate_tasks_structure(tasks_file):
    """Validate the tasks.json file for structural issues."""
    print(f"Validating tasks file: {tasks_file}")
    
    try:
        with open(tasks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    # Extract tasks from the nested structure
    if 'master' in data and 'tasks' in data['master']:
        tasks = data['master']['tasks']
    else:
        tasks = data.get('tasks', [])
    
    print(f"Found {len(tasks)} tasks to validate")
    
    # Validation results
    errors = []
    warnings = []
    
    # Track all task IDs for dependency validation
    all_task_ids = set()
    task_lookup = {}
    
    # Check for duplicate IDs and collect all IDs
    for task in tasks:
        task_id = task.get('id')
        if task_id is not None:
            all_task_ids.add(task_id)
            task_lookup[task_id] = task
            
            # Check for duplicate IDs
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    subtask_id = subtask.get('id')
                    if subtask_id is not None:
                        full_id = f"{task_id}.{subtask_id}" if isinstance(subtask_id, int) else f"{task_id}.{subtask_id}"
                        all_task_ids.add(full_id)
                        task_lookup[full_id] = subtask
    
    # Validate each task
    for task in tasks:
        task_id = task.get('id')
        
        # Check required fields
        if 'id' not in task:
            errors.append(f"Task missing 'id' field: {task.get('title', 'Unknown')}")
        
        if 'title' not in task:
            errors.append(f"Task {task_id} missing 'title' field")
        
        if 'status' not in task:
            errors.append(f"Task {task_id} missing 'status' field")
        elif task['status'] not in ['pending', 'in-progress', 'done', 'deferred', 'cancelled', 'review']:
            warnings.append(f"Task {task_id} has invalid status: {task['status']}")
        
        # Validate dependencies
        dependencies = task.get('dependencies', [])
        if dependencies:
            for dep in dependencies:
                if dep not in all_task_ids:
                    errors.append(f"Task {task_id} has invalid dependency: {dep}")
        
        # Validate subtasks
        if 'subtasks' in task:
            subtasks = task['subtasks']
            for subtask in subtasks:
                subtask_id = subtask.get('id')
                subtask_full_id = f"{task_id}.{subtask_id}" if isinstance(subtask_id, int) else f"{task_id}.{subtask_id}"
                
                if 'id' not in subtask:
                    errors.append(f"Subtask in task {task_id} missing 'id' field")
                
                if 'title' not in subtask:
                    errors.append(f"Subtask {subtask_full_id} missing 'title' field")
                
                if 'status' not in subtask:
                    errors.append(f"Subtask {subtask_full_id} missing 'status' field")
                elif subtask['status'] not in ['pending', 'in-progress', 'done', 'deferred', 'cancelled', 'review']:
                    warnings.append(f"Subtask {subtask_full_id} has invalid status: {subtask['status']}")
                
                # Validate subtask dependencies
                subtask_deps = subtask.get('dependencies', [])
                if subtask_deps:
                    for dep in subtask_deps:
                        if isinstance(dep, str) and dep not in all_task_ids:
                            # Check if it's a relative dependency like "1.1" or "1.2"
                            if '.' in dep:
                                parts = dep.split('.')
                                if len(parts) == 2:
                                    parent_id = parts[0]
                                    subtask_num = parts[1]
                                    if parent_id == str(task_id):
                                        # This is a valid relative dependency within the same parent
                                        continue
                                    else:
                                        errors.append(f"Subtask {subtask_full_id} has invalid dependency: {dep}")
                                else:
                                    errors.append(f"Subtask {subtask_full_id} has invalid dependency format: {dep}")
                            else:
                                errors.append(f"Subtask {subtask_full_id} has invalid dependency: {dep}")
    
    # Check for circular dependencies
    dependency_graph = defaultdict(list)
    for task in tasks:
        task_id = task.get('id')
        deps = task.get('dependencies', [])
        for dep in deps:
            dependency_graph[dep].append(task_id)
    
    # Check for circular dependencies using DFS
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in dependency_graph[node]:
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    visited = set()
    rec_stack = set()
    for task_id in all_task_ids:
        if task_id not in visited:
            if has_cycle(task_id, visited, rec_stack):
                errors.append(f"Circular dependency detected involving task {task_id}")
    
    # Print results
    print(f"\nValidation Results:")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    if errors:
        print("\n❌ Errors found:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\n⚠️  Warnings found:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors:
        print(f"\n✅ All validations passed! The tasks.json file is structurally sound.")
        return True
    else:
        print(f"\n❌ Validation failed with {len(errors)} errors.")
        return False

def main():
    tasks_file = "tasks/tasks.json"
    success = validate_tasks_structure(tasks_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()