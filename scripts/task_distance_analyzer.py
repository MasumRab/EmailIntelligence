#!/usr/bin/env python3
"""
Task Distance Analyzer

This script measures the "distance" or difference between:
1. Original task markdown files
2. Tasks recreated from a PRD (using the reverse engineering approach)

The goal is to quantify how much information is preserved or lost in the round-trip:
Original Tasks → PRD → Tasks (via task-master parse-prd)

Usage:
    python task_distance_analyzer.py --original-dir /path/to/original/tasks --generated-prd /path/to/generated.prd
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from difflib import SequenceMatcher
import yaml


def extract_task_info_from_md(file_path: str) -> Dict[str, Any]:
    """
    Extract key information from a task markdown file.
    
    Args:
        file_path: Path to the task markdown file
        
    Returns:
        Dictionary containing extracted task information
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    task_info = {
        'id': '',
        'title': '',
        'status': '',
        'priority': '',
        'effort': '',
        'complexity': '',
        'dependencies': '',
        'purpose': '',
        'success_criteria': [],
        'subtasks': [],
        'details': '',
        'test_strategy': '',
        'blocks': ''
    }
    
    # Extract title from header
    title_match = re.search(r'^# Task.*?[:\-\s]+(.+)$', content, re.MULTILINE)
    if title_match:
        task_info['title'] = title_match.group(1).strip()
    
    # Extract ID from filename or content
    filename = Path(file_path).stem
    id_match = re.search(r'task[-_]?(\d+(?:[-_.]\d+)*)', filename, re.IGNORECASE)
    if id_match:
        task_info['id'] = id_match.group(1).replace('_', '.').replace('-', '.')
    
    # Extract metadata from bold sections
    status_match = re.search(r'\*\*Status:?\*\*\s*(.+?)(?:\n|$)', content)
    if status_match:
        task_info['status'] = status_match.group(1).strip()
        
    priority_match = re.search(r'\*\*Priority:?\*\*\s*(.+?)(?:\n|$)', content)
    if priority_match:
        task_info['priority'] = priority_match.group(1).strip()
        
    effort_match = re.search(r'\*\*Effort:?\*\*\s*(.+?)(?:\n|$)', content)
    if effort_match:
        task_info['effort'] = effort_match.group(1).strip()
        
    complexity_match = re.search(r'\*\*Complexity:?\*\*\s*(.+?)(?:\n|$)', content)
    if complexity_match:
        task_info['complexity'] = complexity_match.group(1).strip()
        
    deps_match = re.search(r'\*\*Dependencies:?\*\*\s*(.+?)(?:\n|$)', content)
    if deps_match:
        task_info['dependencies'] = deps_match.group(1).strip()
    
    blocks_match = re.search(r'\*\*Blocks:?\*\*\s*(.+?)(?:\n|$)', content)
    if blocks_match:
        task_info['blocks'] = blocks_match.group(1).strip()
    
    # Extract purpose
    purpose_match = re.search(r'## Purpose\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if purpose_match:
        task_info['purpose'] = purpose_match.group(1).strip()
    
    # Extract details
    details_match = re.search(r'## Details\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if details_match:
        task_info['details'] = details_match.group(1).strip()
    
    # Extract test strategy
    test_match = re.search(r'## Test Strategy\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if test_match:
        task_info['test_strategy'] = test_match.group(1).strip()
    
    # Extract success criteria
    criteria_match = re.search(r'## Success Criteria\s*\n+([\s\S]+?)(?=\n## |\n---|\Z)', content)
    if criteria_match:
        criteria_text = criteria_match.group(1)
        # Find all checklist items
        criteria_items = re.findall(r'- \[.\] (.+)', criteria_text)
        task_info['success_criteria'] = criteria_items
    
    # Extract subtasks if they exist in table format
    subtask_table_match = re.search(r'\|\s*ID\s*\|\s*Subtask\s*\|[\s\S]*?\n((?:\|\s*[^\n]*\s*\|.*\n)+)', content)
    if subtask_table_match:
        table_content = subtask_table_match.group(1)
        # Extract subtask rows
        rows = table_content.strip().split('\n')
        for row in rows:
            if '|' in row:
                parts = [part.strip() for part in row.split('|')]
                if len(parts) >= 4:  # ID | Subtask | Status | Effort
                    subtask = {
                        'id': parts[1] if len(parts) > 1 else '',
                        'title': parts[2] if len(parts) > 2 else '',
                        'status': parts[3] if len(parts) > 3 else ''
                    }
                    if subtask['id']:  # Only add if we have an ID
                        task_info['subtasks'].append(subtask)
    
    return task_info


def extract_task_info_from_json(task_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract key information from a task JSON object.
    
    Args:
        task_json: Dictionary representing a task from tasks.json
        
    Returns:
        Dictionary containing extracted task information
    """
    task_info = {
        'id': str(task_json.get('id', '')),
        'title': task_json.get('title', ''),
        'status': task_json.get('status', ''),
        'priority': task_json.get('priority', ''),
        'effort': '',  # Effort is not typically in JSON, but might be in details
        'complexity': str(task_json.get('complexity', '')),
        'dependencies': ', '.join(task_json.get('dependencies', [])),
        'purpose': task_json.get('description', '') or task_json.get('details', ''),
        'success_criteria': [],  # Success criteria are not typically in JSON
        'subtasks': [],
        'details': task_json.get('details', ''),
        'test_strategy': task_json.get('testStrategy', ''),
        'blocks': ''  # Blocks is not typically in JSON
    }
    
    # Extract effort from details if it exists
    details = task_json.get('details', '')
    effort_match = re.search(r'Effort:?\s*(.+?)(?:\n|$)', details)
    if effort_match:
        task_info['effort'] = effort_match.group(1).strip()
    
    # Process subtasks
    for subtask in task_json.get('subtasks', []):
        subtask_info = {
            'id': str(subtask.get('id', '')),
            'title': subtask.get('title', ''),
            'status': subtask.get('status', '')
        }
        task_info['subtasks'].append(subtask_info)
    
    return task_info


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
    
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def calculate_task_distance(original_task: Dict[str, Any], generated_task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the "distance" between an original task and a generated task.
    
    Args:
        original_task: Dictionary with original task information
        generated_task: Dictionary with generated task information
        
    Returns:
        Dictionary with distance metrics
    """
    distances = {}
    
    # Calculate similarity for each field
    fields_to_compare = [
        'title', 'status', 'priority', 'effort', 'complexity', 
        'dependencies', 'purpose', 'details', 'test_strategy', 'blocks'
    ]
    
    total_similarity = 0
    comparison_count = 0
    
    for field in fields_to_compare:
        orig_val = original_task.get(field, '')
        gen_val = generated_task.get(field, '')
        
        similarity = calculate_similarity(str(orig_val), str(gen_val))
        distances[f'{field}_similarity'] = similarity
        total_similarity += similarity
        comparison_count += 1
    
    # Compare success criteria
    orig_criteria = original_task.get('success_criteria', [])
    gen_criteria = generated_task.get('success_criteria', [])
    
    # Calculate criteria similarity
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
    
    distances['success_criteria_similarity'] = criteria_similarity
    total_similarity += criteria_similarity
    comparison_count += 1
    
    # Compare subtasks
    orig_subtasks = original_task.get('subtasks', [])
    gen_subtasks = generated_task.get('subtasks', [])
    
    if orig_subtasks or gen_subtasks:
        # Calculate subtask similarity
        matched_subtasks = 0
        total_subtasks = max(len(orig_subtasks), len(gen_subtasks))
        
        for orig_sub in orig_subtasks:
            for gen_sub in gen_subtasks:
                if calculate_similarity(orig_sub.get('id', ''), gen_sub.get('id', '')) > 0.8:
                    if calculate_similarity(orig_sub.get('title', ''), gen_sub.get('title', '')) > 0.7:
                        matched_subtasks += 1
                        break
        
        subtask_similarity = matched_subtasks / total_subtasks if total_subtasks > 0 else 1.0
    else:
        subtask_similarity = 1.0
    
    distances['subtasks_similarity'] = subtask_similarity
    total_similarity += subtask_similarity
    comparison_count += 1
    
    # Calculate overall similarity
    overall_similarity = total_similarity / comparison_count if comparison_count > 0 else 1.0
    distances['overall_similarity'] = overall_similarity
    distances['overall_distance'] = 1 - overall_similarity
    
    return distances


def load_tasks_from_json_file(json_file_path: str) -> List[Dict[str, Any]]:
    """
    Load tasks from a JSON file (like tasks.json).
    
    Args:
        json_file_path: Path to the JSON file
        
    Returns:
        List of task dictionaries
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle different JSON structures
    if 'master' in data and 'tasks' in data['master']:
        tasks = data['master']['tasks']
    elif 'tasks' in data:
        tasks = data['tasks']
    else:
        tasks = data if isinstance(data, list) else []
    
    return tasks


def analyze_task_distance(original_dir: str, generated_json: str) -> Dict[str, Any]:
    """
    Analyze the distance between original tasks and generated tasks.
    
    Args:
        original_dir: Directory containing original task markdown files
        generated_json: Path to generated tasks JSON file
        
    Returns:
        Dictionary with analysis results
    """
    original_path = Path(original_dir)
    json_path = Path(generated_json)
    
    # Load original tasks from markdown files
    original_files = list(original_path.glob("task-*.md"))
    original_tasks = {}
    
    for file_path in original_files:
        task_info = extract_task_info_from_md(file_path)
        if task_info['id']:
            original_tasks[task_info['id']] = task_info
    
    # Load generated tasks from JSON file
    generated_tasks_list = load_tasks_from_json_file(json_path)
    generated_tasks = {}
    
    for task in generated_tasks_list:
        task_id = str(task.get('id', ''))
        if task_id:
            generated_tasks[task_id] = extract_task_info_from_json(task)
    
    # Compare tasks
    results = {
        'comparison_summary': {
            'original_task_count': len(original_tasks),
            'generated_task_count': len(generated_tasks),
            'matched_task_count': 0,
            'unmatched_original': [],
            'unmatched_generated': []
        },
        'detailed_comparisons': {},
        'aggregated_metrics': {
            'average_overall_similarity': 0,
            'average_overall_distance': 0,
            'field_similarities': {}
        }
    }
    
    matched_count = 0
    total_similarity = 0
    
    # Track field similarities across all tasks
    field_similarities = {}
    
    # Compare each original task with its generated counterpart
    for task_id, original_task in original_tasks.items():
        if task_id in generated_tasks:
            generated_task = generated_tasks[task_id]
            
            # Calculate distance
            distance_metrics = calculate_task_distance(original_task, generated_task)
            
            results['detailed_comparisons'][task_id] = {
                'original': original_task,
                'generated': generated_task,
                'distances': distance_metrics
            }
            
            # Add to totals
            total_similarity += distance_metrics['overall_similarity']
            matched_count += 1
            
            # Accumulate field similarities
            for field, sim_value in distance_metrics.items():
                if '_similarity' in field:
                    if field not in field_similarities:
                        field_similarities[field] = []
                    field_similarities[field].append(sim_value)
        else:
            results['comparison_summary']['unmatched_original'].append(task_id)
    
    # Find generated tasks that don't have originals
    for task_id in generated_tasks.keys():
        if task_id not in original_tasks:
            results['comparison_summary']['unmatched_generated'].append(task_id)
    
    results['comparison_summary']['matched_task_count'] = matched_count
    
    # Calculate averages
    if matched_count > 0:
        results['aggregated_metrics']['average_overall_similarity'] = total_similarity / matched_count
        results['aggregated_metrics']['average_overall_distance'] = 1 - (total_similarity / matched_count)
    
    # Calculate average field similarities
    for field, values in field_similarities.items():
        if values:
            results['aggregated_metrics']['field_similarities'][field] = sum(values) / len(values)
    
    return results


def print_analysis_report(results: Dict[str, Any]):
    """
    Print a formatted analysis report.
    
    Args:
        results: Results dictionary from analyze_task_distance
    """
    print("=" * 80)
    print("TASK DISTANCE ANALYSIS REPORT")
    print("=" * 80)
    
    summary = results['comparison_summary']
    print(f"\nCOMPARISON SUMMARY:")
    print(f"  Original tasks: {summary['original_task_count']}")
    print(f"  Generated tasks: {summary['generated_task_count']}")
    print(f"  Matched tasks: {summary['matched_task_count']}")
    
    if summary['unmatched_original']:
        print(f"  Unmatched in original: {len(summary['unmatched_original'])}")
        for task_id in summary['unmatched_original'][:5]:  # Show first 5
            print(f"    - {task_id}")
        if len(summary['unmatched_original']) > 5:
            print(f"    ... and {len(summary['unmatched_original']) - 5} more")
    
    if summary['unmatched_generated']:
        print(f"  Unmatched in generated: {len(summary['unmatched_generated'])}")
        for task_id in summary['unmatched_generated'][:5]:  # Show first 5
            print(f"    - {task_id}")
        if len(summary['unmatched_generated']) > 5:
            print(f"    ... and {len(summary['unmatched_generated']) - 5} more")
    
    metrics = results['aggregated_metrics']
    print(f"\nAGGREGATED METRICS:")
    print(f"  Average overall similarity: {metrics['average_overall_similarity']:.3f}")
    print(f"  Average overall distance: {metrics['average_overall_distance']:.3f}")
    
    print(f"\nFIELD SIMILARITIES:")
    for field, avg_sim in sorted(metrics['field_similarities'].items()):
        print(f"  {field}: {avg_sim:.3f}")
    
    print(f"\nDETAILED COMPARISONS:")
    for task_id, comparison in list(results['detailed_comparisons'].items())[:3]:  # Show first 3
        distances = comparison['distances']
        print(f"  Task {task_id}:")
        print(f"    Overall similarity: {distances['overall_similarity']:.3f}")
        print(f"    Title similarity: {distances.get('title_similarity', 0):.3f}")
        print(f"    Purpose similarity: {distances.get('purpose_similarity', 0):.3f}")
        print(f"    Status similarity: {distances.get('status_similarity', 0):.3f}")
    
    if len(results['detailed_comparisons']) > 3:
        print(f"  ... and {len(results['detailed_comparisons']) - 3} more tasks")


def main():
    parser = argparse.ArgumentParser(description="Analyze distance between original and generated tasks")
    parser.add_argument("--original-dir", "-o", required=True, 
                       help="Directory containing original task markdown files")
    parser.add_argument("--generated-json", "-g", required=True,
                       help="Path to generated tasks JSON file")
    parser.add_argument("--output", "-out", help="Output file for results (JSON format)")
    
    args = parser.parse_args()
    
    print("Starting task distance analysis...")
    print(f"Original tasks dir: {args.original_dir}")
    print(f"Generated tasks JSON: {args.generated_json}")
    
    results = analyze_task_distance(args.original_dir, args.generated_json)
    
    # Print report
    print_analysis_report(results)
    
    # Save results if output file specified
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())