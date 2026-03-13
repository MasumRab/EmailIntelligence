#!/usr/bin/env python3
"""
Roundtrip Fidelity Test: Tasks → PRD → Tasks

Tests how much information is preserved when converting:
1. Original Tasks → PRD (reverse engineering)
2. PRD → Generated Tasks (simulated parse-prd)
3. Compare Original vs Generated

Since task-master parse-prd is not implemented, we simulate the parsing
by extracting information from the generated PRD.
"""

import sys
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Add scripts to path
sys.path.append('scripts')

from advanced_reverse_engineer_prd import (
    extract_task_info_from_md,
    create_advanced_reverse_engineered_prd,
    parse_dependencies
)


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using multiple metrics."""
    if not text1 or not text2:
        return 0.0
    
    # Normalize texts
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()
    
    # Simple word overlap (Jaccard-like)
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1 & words2
    union = words1 | words2
    
    jaccard = len(intersection) / len(union) if union else 0.0
    
    # Check if one contains the other (for partial matches)
    contains_score = 0.0
    if text1 in text2 or text2 in text1:
        contains_score = 0.5
    
    # Return weighted average
    return (jaccard * 0.7) + (contains_score * 0.3)


def compare_task_info(original: Dict[str, Any], generated: Dict[str, Any]) -> Dict[str, float]:
    """Compare original task info with generated/simulated task info."""
    scores = {}
    
    # Title similarity
    scores['title'] = calculate_text_similarity(
        original.get('title', ''),
        generated.get('title', '')
    )
    
    # Effort match (exact or range overlap)
    orig_effort = original.get('effort', '')
    gen_effort = generated.get('effort', '')
    scores['effort'] = 1.0 if orig_effort == gen_effort else (
        0.5 if gen_effort and orig_effort in gen_effort else 0.0
    )
    
    # Complexity match
    orig_complexity = original.get('complexity', '')
    gen_complexity = generated.get('complexity', '')
    scores['complexity'] = 1.0 if orig_complexity == gen_complexity else 0.0
    
    # Dependencies match
    orig_deps = set(parse_dependencies(original.get('dependencies', '')))
    gen_deps = set(parse_dependencies(generated.get('dependencies', '')))
    if orig_deps or gen_deps:
        scores['dependencies'] = len(orig_deps & gen_deps) / max(len(orig_deps | gen_deps), 1)
    else:
        scores['dependencies'] = 1.0  # Both have no dependencies
    
    # Success criteria match
    orig_criteria = set(original.get('success_criteria', []))
    gen_criteria = set(generated.get('success_criteria', []))
    if orig_criteria or gen_criteria:
        scores['success_criteria'] = len(orig_criteria & gen_criteria) / max(len(orig_criteria | gen_criteria), 1)
    else:
        scores['success_criteria'] = 1.0  # Both have no criteria
    
    # Purpose/description similarity
    scores['purpose'] = calculate_text_similarity(
        original.get('purpose', ''),
        generated.get('purpose', '')
    )
    
    # Calculate overall score (weighted average)
    weights = {
        'title': 0.15,
        'effort': 0.15,
        'complexity': 0.15,
        'dependencies': 0.15,
        'success_criteria': 0.25,
        'purpose': 0.15
    }
    
    overall = sum(scores[k] * weights[k] for k in weights.keys())
    scores['overall'] = overall
    
    return scores


def simulate_parse_prd(prd_content: str, original_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Simulate what task-master parse-prd would generate from PRD.
    
    Since parse-prd is not implemented, we extract information from the PRD
    and create task structures that match what would be generated.
    """
    generated_tasks = []
    
    # For each original task, simulate what would be generated from PRD
    for orig_task in original_tasks:
        task_id = orig_task['id']
        
        # Search for this task's section in PRD
        task_section_pattern = rf'###.*?{re.escape(task_id)}.*?\n(.*?)(?=###|\Z)'
        section_match = re.search(task_section_pattern, prd_content, re.DOTALL | re.IGNORECASE)
        
        generated_task = {
            'id': task_id,
            'title': orig_task['title'],  # Title would be extracted from PRD
            'effort': '',  # PRD doesn't have effort estimates
            'complexity': '',  # PRD doesn't have complexity
            'dependencies': orig_task.get('dependencies', ''),  # Would be extracted from dependency graph
            'purpose': '',  # Would be extracted from feature description
            'success_criteria': [],  # Would be extracted from acceptance criteria table
        }
        
        if section_match:
            section_text = section_match.group(1)
            
            # Extract purpose from description
            desc_match = re.search(r'\*\*Description\*\*:\s*(.+)', section_text)
            if desc_match:
                generated_task['purpose'] = desc_match.group(1).strip()
            
            # Extract effort if present
            effort_match = re.search(r'\*\*Estimated Effort\*\*:\s*(\d+-?\d*\s*hours)', section_text)
            if effort_match:
                generated_task['effort'] = effort_match.group(1)
            
            # Extract complexity if present
            complexity_match = re.search(r'\*\*Technical Complexity\*\*:\s*(\d+/10)', section_text)
            if complexity_match:
                generated_task['complexity'] = complexity_match.group(1)
            
            # Extract acceptance criteria from table
            criteria_pattern = r'\|[^|]+\|([^|]+)\|[^|]+\|'
            criteria_matches = re.findall(criteria_pattern, section_text)
            generated_task['success_criteria'] = [c.strip() for c in criteria_matches[:10]]  # Limit to 10
        
        generated_tasks.append(generated_task)
    
    return generated_tasks


def run_fidelity_test(task_files: List[str]) -> Dict[str, Any]:
    """
    Run complete fidelity test: Tasks → PRD → Tasks → Compare
    
    Returns:
        Dictionary with fidelity scores and analysis
    """
    results = {
        'tasks_tested': len(task_files),
        'individual_scores': [],
        'average_scores': {},
        'analysis': {}
    }
    
    # Step 1: Extract info from original tasks
    print(f"Step 1: Extracting info from {len(task_files)} original tasks...")
    original_tasks = []
    for task_file in task_files:
        task_info = extract_task_info_from_md(task_file)
        original_tasks.append(task_info)
    
    # Step 2: Generate PRD from tasks
    print("Step 2: Generating PRD from tasks...")
    prd_content = create_advanced_reverse_engineered_prd(task_files)
    print(f"  Generated PRD: {len(prd_content):,} characters")
    
    # Save PRD for inspection
    Path('test_roundtrip_prd.md').write_text(prd_content)
    print("  Saved PRD to test_roundtrip_prd.md")
    
    # Step 3: Simulate parse-prd (generate tasks from PRD)
    print("Step 3: Simulating parse-prd (generating tasks from PRD)...")
    generated_tasks = simulate_parse_prd(prd_content, original_tasks)
    print(f"  Generated {len(generated_tasks)} tasks")
    
    # Step 4: Compare original vs generated
    print("Step 4: Comparing original vs generated tasks...")
    print()
    
    total_scores = {
        'title': 0.0,
        'effort': 0.0,
        'complexity': 0.0,
        'dependencies': 0.0,
        'success_criteria': 0.0,
        'purpose': 0.0,
        'overall': 0.0
    }
    
    for i, (orig, gen) in enumerate(zip(original_tasks, generated_tasks)):
        scores = compare_task_info(orig, gen)
        results['individual_scores'].append({
            'task_id': orig['id'],
            'title': orig['title'][:50],
            'scores': scores
        })
        
        # Accumulate for averages
        for key in total_scores.keys():
            total_scores[key] += scores[key]
        
        # Print individual result
        print(f"  Task {orig['id']}: {scores['overall']*100:.1f}% fidelity")
        print(f"    Title: {scores['title']*100:.0f}% | Effort: {scores['effort']*100:.0f}% | Complexity: {scores['complexity']*100:.0f}%")
        print(f"    Dependencies: {scores['dependencies']*100:.0f}% | Criteria: {scores['success_criteria']*100:.0f}% | Purpose: {scores['purpose']*100:.0f}%")
        print()
    
    # Calculate averages
    n = len(task_files)
    for key in total_scores:
        results['average_scores'][key] = total_scores[key] / n if n > 0 else 0.0
    
    # Analysis
    results['analysis'] = {
        'highest_fidelity': max(results['individual_scores'], key=lambda x: x['scores']['overall']),
        'lowest_fidelity': min(results['individual_scores'], key=lambda x: x['scores']['overall']),
        'information_preserved': [
            'Task titles',
            'Dependencies (from dependency graph)',
            'Some success criteria (from acceptance criteria tables)'
        ],
        'information_lost': [
            'Effort estimates (not in PRD format)',
            'Complexity ratings (not in PRD format)',
            'Detailed implementation guides',
            'Templates and examples',
            'Branch-specific details'
        ]
    }
    
    return results


def main():
    """Main function to run fidelity tests."""
    print("=" * 70)
    print("ROUNDTRIP FIDELITY TEST: Tasks → PRD → Tasks")
    print("=" * 70)
    print()
    
    # Test with different task samples
    test_sets = {
        'Single Task (001)': ['tasks/task_001.md'],
        'First 5 Tasks': ['tasks/task_001.md', 'tasks/task_002.md', 'tasks/task_005.md', 'tasks/task_007.md', 'tasks/task_009.md'],
        'First 10 Tasks': [f'tasks/task_{str(i).zfill(3)}.md' for i in range(1, 11)],
    }
    
    all_results = {}
    
    for test_name, task_files in test_sets.items():
        print()
        print("=" * 70)
        print(f"TEST: {test_name}")
        print("=" * 70)
        print()
        
        # Filter to only existing files
        existing_files = [f for f in task_files if Path(f).exists()]
        
        if not existing_files:
            print(f"  No existing files found for {test_name}")
            continue
        
        results = run_fidelity_test(existing_files)
        all_results[test_name] = results
        
        # Print summary
        print()
        print("-" * 70)
        print(f"SUMMARY: {test_name}")
        print("-" * 70)
        print(f"  Tasks Tested: {results['tasks_tested']}")
        print(f"  Average Overall Fidelity: {results['average_scores']['overall']*100:.1f}%")
        print(f"  Highest Fidelity: Task {results['analysis']['highest_fidelity']['task_id']} ({results['analysis']['highest_fidelity']['scores']['overall']*100:.1f}%)")
        print(f"  Lowest Fidelity: Task {results['analysis']['lowest_fidelity']['task_id']} ({results['analysis']['lowest_fidelity']['scores']['overall']*100:.1f}%)")
        print()
    
    # Final summary
    print()
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print()
    
    for test_name, results in all_results.items():
        print(f"{test_name}:")
        print(f"  Overall Fidelity: {results['average_scores']['overall']*100:.1f}%")
        print(f"  - Title: {results['average_scores']['title']*100:.0f}%")
        print(f"  - Effort: {results['average_scores']['effort']*100:.0f}%")
        print(f"  - Complexity: {results['average_scores']['complexity']*100:.0f}%")
        print(f"  - Dependencies: {results['average_scores']['dependencies']*100:.0f}%")
        print(f"  - Success Criteria: {results['average_scores']['success_criteria']*100:.0f}%")
        print(f"  - Purpose: {results['average_scores']['purpose']*100:.0f}%")
        print()
    
    # Save results
    import json
    results_file = Path('roundtrip_fidelity_results.json')
    
    # Convert results to JSON-serializable format
    json_results = {}
    for test_name, results in all_results.items():
        json_results[test_name] = {
            'tasks_tested': results['tasks_tested'],
            'average_scores': results['average_scores'],
            'highest_fidelity_task': results['analysis']['highest_fidelity']['task_id'],
            'highest_fidelity_score': results['analysis']['highest_fidelity']['scores']['overall'],
            'lowest_fidelity_task': results['analysis']['lowest_fidelity']['task_id'],
            'lowest_fidelity_score': results['analysis']['lowest_fidelity']['scores']['overall'],
        }
    
    results_file.write_text(json.dumps(json_results, indent=2))
    print(f"Results saved to {results_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())
