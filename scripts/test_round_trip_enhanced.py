#!/usr/bin/env python3
"""
Enhanced Round-trip Test for PRD Generation
Tests the full round-trip process with proper empty tasks.json handling:
1. Backup current tasks.json
2. Start with empty tasks.json
3. Parse PRD to generate tasks
4. Compare generated tasks with original tasks
5. Restore original tasks.json
"""

import argparse
import tempfile
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
import json
import subprocess
import sys

# Add the current directory to the path to import the module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the ultra enhanced PRD generation
from ultra_enhanced_reverse_engineer_prd import create_ultra_enhanced_reverse_engineered_prd, extract_task_info_from_md_ultra_enhanced
from taskmaster_runner import run_task_master_parse_prd, check_task_master_available


def backup_tasks_json(tasks_json_path: str) -> str:
    """
    Backup the current tasks.json file.
    
    Args:
        tasks_json_path: Path to the tasks.json file
        
    Returns:
        Path to the backup file
    """
    backup_path = f"{tasks_json_path}.roundtrip_backup"
    if os.path.exists(tasks_json_path):
        shutil.copy2(tasks_json_path, backup_path)
        print(f"✅ Backed up tasks.json to {backup_path}")
    else:
        print(f"ℹ️ No existing tasks.json found at {tasks_json_path}")
    return backup_path


def restore_tasks_json(backup_path: str, tasks_json_path: str):
    """
    Restore tasks.json from backup.
    
    Args:
        backup_path: Path to the backup file
        tasks_json_path: Path to restore tasks.json to
    """
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, tasks_json_path)
        print(f"✅ Restored tasks.json from {backup_path}")
        os.remove(backup_path)
        print(f"🗑️  Removed backup file {backup_path}")
    else:
        print(f"⚠️  Backup file not found: {backup_path}")


def create_empty_tasks_json(tasks_json_path: str):
    """
    Create an empty tasks.json file for round trip testing.
    
    Args:
        tasks_json_path: Path to create empty tasks.json
        
    Returns:
        Path to the created empty tasks.json
    """
    empty_tasks = {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "Empty tasks for round-trip test",
            "lastUpdated": "2026-01-27T00:00:00Z",
            "tasks": []
        }
    }
    
    with open(tasks_json_path, 'w') as f:
        json.dump(empty_tasks, f, indent=2)
    
    print(f"✅ Created empty tasks.json at {tasks_json_path}")
    return tasks_json_path


def run_parse_prd_for_round_trip(prd_file: str, tasks_json_path: str) -> str:
    """
    Run task-master parse-prd to generate tasks from PRD with proper empty tasks.json handling.
    
    Args:
        prd_file: Path to the PRD file
        tasks_json_path: Path to tasks.json (should be empty for round trip)
        
    Returns:
        Path to the generated tasks.json file
    """
    # Use the taskmaster_runner which handles both real task-master and simulation
    return run_task_master_parse_prd(
        prd_file=prd_file,
        output_dir=os.path.dirname(tasks_json_path),
        fallback_simulation=True,
        extract_task_info_func=extract_task_info_from_md_ultra_enhanced,
        original_task_files=None,  # We'll use the PRD to generate tasks
        simulation_description="round-trip test with empty tasks.json",
    )


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two text strings.
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        Float between 0 and 1 representing similarity
    """
    if not text1 and not text2:
        return 1.0
    if not text1 or not text2:
        return 0.0

    # Simple character-based similarity
    from difflib import SequenceMatcher
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def calculate_task_similarity(original_task: Dict[str, Any], generated_task: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate similarity between original and generated tasks.
    
    Args:
        original_task: Dictionary with original task information
        generated_task: Dictionary with generated task information
        
    Returns:
        Dictionary with similarity scores for each field
    """
    similarities = {}

    # Fields to compare
    fields_to_compare = [
        'title', 'status', 'priority', 'effort', 'complexity',
        'dependencies', 'purpose', 'details', 'test_strategy', 'blocks'
    ]

    for field in fields_to_compare:
        orig_val = original_task.get(field, '')
        gen_val = generated_task.get(field, '')

        similarity = calculate_similarity(str(orig_val), str(gen_val))
        similarities[f'{field}_similarity'] = similarity

    # Compare success criteria
    orig_criteria = original_task.get('success_criteria', [])
    gen_criteria = generated_task.get('success_criteria', [])

    if orig_criteria or gen_criteria:
        # Simple overlap ratio
        orig_set = set(str(c).lower() for c in orig_criteria)
        gen_set = set(str(c).lower() for c in gen_criteria)

        if orig_set or gen_set:
            intersection = len(orig_set.intersection(gen_set))
            union = len(orig_set.union(gen_set))
            criteria_similarity = intersection / union if union > 0 else 0
        else:
            criteria_similarity = 1.0
    else:
        criteria_similarity = 1.0

    similarities['success_criteria_similarity'] = criteria_similarity

    # Calculate overall similarity
    total_similarity = sum(similarities.values())
    num_fields = len(similarities)
    overall_similarity = total_similarity / num_fields if num_fields > 0 else 1.0
    similarities['overall_similarity'] = overall_similarity
    similarities['overall_distance'] = 1 - overall_similarity

    return similarities


def run_round_trip_test(task_files: List[str], tasks_json_path: str) -> Dict[str, Any]:
    """
    Run the enhanced round-trip test with proper empty tasks.json handling:
    1. Backup current tasks.json
    2. Create empty tasks.json
    3. Generate PRD from original tasks
    4. Parse PRD to generate tasks
    5. Compare generated tasks with original tasks
    6. Restore original tasks.json
    
    Args:
        task_files: List of paths to task markdown files
        tasks_json_path: Path to tasks.json file
        
    Returns:
        Dictionary with test results and similarity metrics
    """
    print("Running enhanced round-trip test with empty tasks.json")
    print(f"Processing {len(task_files)} task files")

    # Step 0: Backup current tasks.json
    print("\nStep 0: Backing up current tasks.json...")
    backup_path = backup_tasks_json(tasks_json_path)

    try:
        # Step 1: Create empty tasks.json
        print("\nStep 1: Creating empty tasks.json...")
        empty_tasks_path = create_empty_tasks_json(tasks_json_path)

        # Step 2: Generate PRD from original tasks
        print("\nStep 2: Generating PRD from original tasks...")
        prd_content = create_ultra_enhanced_reverse_engineered_prd(task_files)

        # Save the PRD for inspection
        prd_path = Path("roundtrip_test_prd_enhanced.md")
        with open(prd_path, 'w', encoding='utf-8') as f:
            f.write(prd_content)

        print(f"Generated PRD saved to {prd_path}")

        # Step 3: Run task-master parse-prd to generate tasks from PRD
        print("\nStep 3: Running task-master parse-prd to generate tasks from PRD...")
        generated_tasks_path = run_parse_prd_for_round_trip(str(prd_path), tasks_json_path)

        # Step 4: Load and compare original tasks with generated tasks
        print("\nStep 4: Comparing original tasks with generated tasks...")

        # Load original tasks from markdown files
        original_tasks = {}
        for task_file in task_files:
            task_info = extract_task_info_from_md_ultra_enhanced(task_file)
            original_tasks[task_info['id']] = task_info

        # Load generated tasks from tasks.json
        with open(generated_tasks_path, 'r') as f:
            generated_data = json.load(f)
        generated_tasks = {task['id']: task for task in generated_data.get('master', {}).get('tasks', [])}

        # Compare tasks
        comparison_results = {
            'original_task_count': len(original_tasks),
            'generated_task_count': len(generated_tasks),
            'compared_tasks': 0,
            'field_similarities': {},
            'task_similarities': {},
            'average_overall_similarity': 0,
            'average_overall_distance': 0,
            'missing_tasks': [],
            'extra_tasks': []
        }

        # Find missing and extra tasks
        original_ids = set(original_tasks.keys())
        generated_ids = set(generated_tasks.keys())
        
        comparison_results['missing_tasks'] = list(original_ids - generated_ids)
        comparison_results['extra_tasks'] = list(generated_ids - original_ids)

        total_similarity = 0
        compared_count = 0

        # Compare common tasks
        common_ids = original_ids.intersection(generated_ids)
        
        for task_id in common_ids:
            original_task = original_tasks[task_id]
            generated_task = generated_tasks[task_id]
            
            # Calculate similarity
            task_similarities = calculate_task_similarity(original_task, generated_task)

            comparison_results['task_similarities'][task_id] = task_similarities
            total_similarity += task_similarities['overall_similarity']
            compared_count += 1

            # Accumulate field similarities
            for field, sim_value in task_similarities.items():
                if '_similarity' in field:
                    if field not in comparison_results['field_similarities']:
                        comparison_results['field_similarities'][field] = []
                    comparison_results['field_similarities'][field].append(sim_value)

        comparison_results['compared_tasks'] = compared_count

        if compared_count > 0:
            comparison_results['average_overall_similarity'] = total_similarity / compared_count
            comparison_results['average_overall_distance'] = 1 - (total_similarity / compared_count)

        # Calculate average field similarities
        for field, values in comparison_results['field_similarities'].items():
            if values:
                comparison_results['field_similarities'][field] = sum(values) / len(values)

        return comparison_results

    finally:
        # Step 5: Restore original tasks.json
        print("\nStep 5: Restoring original tasks.json...")
        restore_tasks_json(backup_path, tasks_json_path)


def print_round_trip_results(results: Dict[str, Any]):
    """
    Print the enhanced round-trip test results.
    
    Args:
        results: Results dictionary from run_round_trip_test
    """
    print("\n" + "="*80)
    print("ENHANCED ROUND-TRIP TEST RESULTS")
    print("="*80)

    print(f"\nTEST SUMMARY:")
    print(f"  Original tasks: {results['original_task_count']}")
    print(f"  Generated tasks: {results['generated_task_count']}")
    print(f"  Tasks compared: {results['compared_tasks']}")
    print(f"  Missing tasks: {len(results['missing_tasks'])} - {results['missing_tasks']}")
    print(f"  Extra tasks: {len(results['extra_tasks'])} - {results['extra_tasks']}")
    print(f"  Average overall similarity: {results['average_overall_similarity']:.3f}")
    print(f"  Average overall distance: {results['average_overall_distance']:.3f}")

    print(f"\nFIELD SIMILARITIES:")
    for field, avg_sim in sorted(results['field_similarities'].items()):
        print(f"  {field}: {avg_sim:.3f}")

    print(f"\nTASK-LEVEL RESULTS:")
    for task_id, similarities in results['task_similarities'].items():
        print(f"  Task {task_id}: {similarities['overall_similarity']:.3f} similarity")

    print(f"\n🎯 The test validates the full round-trip process with empty tasks.json")
    print(f"   Higher similarity scores indicate better PRD generation fidelity.")
    print(f"   Missing/extra tasks indicate areas for improvement in PRD parsing.")


def main():
    parser = argparse.ArgumentParser(description="Run enhanced round-trip test for PRD generation")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing task markdown files")
    parser.add_argument("--tasks-json", "-t", default=".taskmaster/tasks/tasks.json", 
                       help="Path to tasks.json file (default: .taskmaster/tasks/tasks.json)")
    parser.add_argument("--pattern", default="task*.md", help="File pattern to match (default: task*.md)")

    args = parser.parse_args()

    print("Starting enhanced round-trip test for PRD generation...")
    print(f"Input directory: {args.input_dir}")
    print(f"Tasks JSON: {args.tasks_json}")
    print(f"File pattern: {args.pattern}")

    # Find all task markdown files
    input_path = Path(args.input_dir)
    task_files = list(input_path.glob(args.pattern))

    if not task_files:
        print(f"No task files found in {input_path} with pattern {args.pattern}")
        return 1

    print(f"Found {len(task_files)} task files for testing")

    # Run the enhanced round-trip test
    results = run_round_trip_test(task_files, args.tasks_json)

    # Print the results
    print_round_trip_results(results)

    return 0


if __name__ == "__main__":
    exit(main())