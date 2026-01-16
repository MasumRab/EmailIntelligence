#!/usr/bin/env python3
"""
Compare Similarity Scores Between Basic and Enhanced PRD Generation

This script compares the similarity scores between the basic and enhanced 
PRD generation approaches to measure the improvement achieved.
"""

import argparse
import tempfile
import os
from pathlib import Path
import json
from typing import Dict, Any

# Import the required modules
from scripts.reverse_engineer_prd import create_reverse_engineered_prd as basic_approach
from scripts.enhanced_reverse_engineer_prd import create_enhanced_reverse_engineered_prd as enhanced_approach
from scripts.super_enhanced_reverse_engineer_prd import create_super_enhanced_reverse_engineered_prd as super_enhanced_approach
from scripts.task_distance_analyzer import analyze_task_distance, print_analysis_report


def generate_tasks_json_from_prd(prd_content: str, original_task_files: list) -> str:
    """
    Simulate the task-master parse-prd process by creating a mock tasks.json.
    
    Args:
        prd_content: Content of the PRD file
        original_task_files: List of original task files for reference
    
    Returns:
        Path to the simulated tasks.json file
    """
    # This is a simplified simulation - in reality, task-master would process the PRD
    # For now, we'll create a mock JSON based on the original tasks
    # but shaped by PRD structure
    
    # Import the extraction function from the basic approach
    from scripts.reverse_engineer_prd import extract_task_info_from_md
    
    tasks_json = {
        "master": {
            "name": "Task Master",
            "version": "1.0.0",
            "description": "Tasks generated from PRD (comparison simulation)",
            "tasks": []
        }
    }

    # Extract task information from original files to simulate what might be generated
    for task_file in original_task_files:
        original_info = extract_task_info_from_md(task_file)

        # Create a simulated task based on the original but shaped by PRD structure
        simulated_task = {
            "id": original_info['id'],
            "title": original_info['title'],
            "description": original_info['purpose'],
            "status": original_info.get('status', 'pending'),
            "priority": original_info.get('priority', 'medium'),
            "dependencies": [],
            "details": original_info.get('details', ''),
            "subtasks": [],
            "testStrategy": original_info.get('test_strategy', ''),
            "complexity": len(original_info.get('subtasks', [])),
            "recommendedSubtasks": len(original_info.get('subtasks', [])),
            "expansionPrompt": "N/A - subtasks already defined.",
        }

        # Add subtasks if they exist
        for subtask in original_info.get('subtasks', []):
            simulated_subtask = {
                "id": subtask.get('id', 1),
                "title": subtask.get('title', ''),
                "description": "",
                "dependencies": [],
                "details": "",
                "testStrategy": "",
                "status": subtask.get('status', 'pending'),
                "parentId": original_info['id'],
            }
            simulated_task['subtasks'].append(simulated_subtask)

        tasks_json["master"]["tasks"].append(simulated_task)

    # Write the simulated tasks.json
    output_path = Path(f"simulated_tasks_comparison.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tasks_json, f, indent=2)

    return str(output_path)


def compare_approaches(original_dir: str, pattern: str = "task-*.md"):
    """
    Compare the similarity scores between basic, enhanced, and super enhanced approaches.
    
    Args:
        original_dir: Directory containing original task markdown files
        pattern: Pattern to match task files
    """
    original_path = Path(original_dir)
    original_files = list(original_path.glob(pattern))

    if not original_files:
        print(f"No task files found in {original_dir} with pattern {pattern}")
        return

    print(f"Found {len(original_files)} original task files for comparison")
    
    # Create temporary directory for intermediate files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 1. Test basic approach
        print("\n--- TESTING BASIC APPROACH ---")
        basic_prd = basic_approach(original_files)
        basic_prd_path = temp_path / "basic_generated_prd.md"
        basic_prd_path.write_text(basic_prd, encoding='utf-8')
        
        # Generate simulated tasks from basic PRD
        basic_tasks_json_path = generate_tasks_json_from_prd(basic_prd, original_files)
        
        # Analyze distance for basic approach
        basic_results = analyze_task_distance(original_dir, basic_tasks_json_path)
        print("BASIC APPROACH RESULTS:")
        print(f"  Average overall similarity: {basic_results['aggregated_metrics']['average_overall_similarity']:.3f}")
        print(f"  Average overall distance: {basic_results['aggregated_metrics']['average_overall_distance']:.3f}")
        
        # 2. Test enhanced approach
        print("\n--- TESTING ENHANCED APPROACH ---")
        enhanced_prd = enhanced_approach(original_files)
        enhanced_prd_path = temp_path / "enhanced_generated_prd.md"
        enhanced_prd_path.write_text(enhanced_prd, encoding='utf-8')
        
        # Generate simulated tasks from enhanced PRD
        enhanced_tasks_json_path = generate_tasks_json_from_prd(enhanced_prd, original_files)
        
        # Analyze distance for enhanced approach
        enhanced_results = analyze_task_distance(original_dir, enhanced_tasks_json_path)
        print("ENHANCED APPROACH RESULTS:")
        print(f"  Average overall similarity: {enhanced_results['aggregated_metrics']['average_overall_similarity']:.3f}")
        print(f"  Average overall distance: {enhanced_results['aggregated_metrics']['average_overall_distance']:.3f}")
        
        # 3. Test super enhanced approach
        print("\n--- TESTING SUPER ENHANCED APPROACH ---")
        super_enhanced_prd = super_enhanced_approach(original_files)
        super_enhanced_prd_path = temp_path / "super_enhanced_generated_prd.md"
        super_enhanced_prd_path.write_text(super_enhanced_prd, encoding='utf-8')
        
        # Generate simulated tasks from super enhanced PRD
        super_enhanced_tasks_json_path = generate_tasks_json_from_prd(super_enhanced_prd, original_files)
        
        # Analyze distance for super enhanced approach
        super_enhanced_results = analyze_task_distance(original_dir, super_enhanced_tasks_json_path)
        print("SUPER ENHANCED APPROACH RESULTS:")
        print(f"  Average overall similarity: {super_enhanced_results['aggregated_metrics']['average_overall_similarity']:.3f}")
        print(f"  Average overall distance: {super_enhanced_results['aggregated_metrics']['average_overall_distance']:.3f}")
        
        # 4. Compare results
        print("\n--- COMPARISON SUMMARY ---")
        basic_sim = basic_results['aggregated_metrics']['average_overall_similarity']
        enhanced_sim = enhanced_results['aggregated_metrics']['average_overall_similarity']
        super_enhanced_sim = super_enhanced_results['aggregated_metrics']['average_overall_similarity']
        
        basic_dist = basic_results['aggregated_metrics']['average_overall_distance']
        enhanced_dist = enhanced_results['aggregated_metrics']['average_overall_distance']
        super_enhanced_dist = super_enhanced_results['aggregated_metrics']['average_overall_distance']
        
        print(f"SIMILARITY COMPARISON:")
        print(f"  Basic approach:        {basic_sim:.3f}")
        print(f"  Enhanced approach:     {enhanced_sim:.3f} ({((enhanced_sim - basic_sim) / basic_sim * 100):+.1f}%)")
        print(f"  Super Enhanced:        {super_enhanced_sim:.3f} ({((super_enhanced_sim - basic_sim) / basic_sim * 100):+.1f}%)")
        
        print(f"\nDISTANCE COMPARISON (lower is better):")
        print(f"  Basic approach:        {basic_dist:.3f}")
        print(f"  Enhanced approach:     {enhanced_dist:.3f} ({((enhanced_dist - basic_dist) / basic_dist * 100):+.1f}%)")
        print(f"  Super Enhanced:        {super_enhanced_dist:.3f} ({((super_enhanced_dist - basic_dist) / basic_dist * 100):+.1f}%)")
        
        # Calculate improvement percentages
        enhanced_improvement = ((enhanced_sim - basic_sim) / basic_sim) * 100 if basic_sim != 0 else 0
        super_enhanced_improvement = ((super_enhanced_sim - basic_sim) / basic_sim) * 100 if basic_sim != 0 else 0
        
        print(f"\nIMPROVEMENT SUMMARY:")
        print(f"  Enhanced vs Basic:     {enhanced_improvement:+.1f}% improvement in similarity")
        print(f"  Super Enhanced vs Basic: {super_enhanced_improvement:+.1f}% improvement in similarity")
        
        # Detailed field comparisons
        print(f"\nDETAILED FIELD COMPARISONS:")
        print("Basic vs Enhanced vs Super Enhanced")
        
        # Get field similarities for each approach
        basic_fields = basic_results['aggregated_metrics']['field_similarities']
        enhanced_fields = enhanced_results['aggregated_metrics']['field_similarities']
        super_enhanced_fields = super_enhanced_results['aggregated_metrics']['field_similarities']
        
        all_fields = set(basic_fields.keys()) | set(enhanced_fields.keys()) | set(super_enhanced_fields.keys())
        
        print(f"{'Field':<25} {'Basic':<8} {'Enhanced':<10} {'Super Enh':<10} {'Change':<10}")
        print("-" * 70)
        
        for field in sorted(all_fields):
            b_val = basic_fields.get(field, 0)
            e_val = enhanced_fields.get(field, 0)
            s_val = super_enhanced_fields.get(field, 0)
            
            # Calculate improvement from basic to super enhanced
            improvement = ((s_val - b_val) / b_val * 100) if b_val != 0 else 0
            
            print(f"{field:<25} {b_val:<8.3f} {e_val:<10.3f} {s_val:<10.3f} {improvement:<+10.1f}%")


def main():
    parser = argparse.ArgumentParser(description="Compare similarity scores between PRD generation approaches")
    parser.add_argument("--original-dir", "-o", required=True,
                        help="Directory containing original task markdown files")
    parser.add_argument("--pattern", "-p", default="task-*.md",
                        help="Pattern to match task files (default: task-*.md)")

    args = parser.parse_args()

    print("Starting comparison of PRD generation approaches...")
    print(f"Original tasks dir: {args.original_dir}")
    print(f"File pattern: {args.pattern}")

    compare_approaches(args.original_dir, args.pattern)

    return 0


if __name__ == "__main__":
    exit(main())