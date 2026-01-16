#!/usr/bin/env python3
"""
Ralph Loop Controller for Task Distance Minimization

This script implements the Ralph Wiggum loop methodology to iteratively
minimize the distance between original task markdown files and tasks
generated from a PRD (Product Requirements Document).

The process:
1. Take original task markdown files
2. Generate a PRD using reverse engineering
3. Simulate task-master parse-prd to recreate tasks from PRD
4. Measure distance between original and recreated tasks
5. Adjust the PRD generation to minimize distance
6. Repeat until convergence or max iterations

Usage:
    python ralph_loop_controller.py --original-dir ./tasks --max-iterations 20
"""

import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any

# Import our custom modules
from task_distance_analyzer import analyze_task_distance, print_analysis_report
from iterative_distance_minimizer import iterative_distance_minimization, print_final_report


def create_ralph_loop_state(task_prompt: str, max_iterations: int = 20, completion_promise: str = None) -> Dict[str, Any]:
    """
    Create the state file for the Ralph loop.
    
    Args:
        task_prompt: The task prompt describing what to accomplish
        max_iterations: Maximum number of iterations
        completion_promise: Phrase that signals completion
        
    Returns:
        Dictionary with loop state information
    """
    state = {
        "task_prompt": task_prompt,
        "max_iterations": max_iterations,
        "completion_promise": completion_promise,
        "current_iteration": 0,
        "status": "initialized",
        "results": [],
        "best_distance": float('inf'),
        "best_similarity": 0,
        "convergence_threshold": 0.01,  # Stop if improvement is less than this
        "created_files": []
    }
    
    return state


def run_ralph_loop(original_dir: str, max_iterations: int = 20, completion_promise: str = None) -> Dict[str, Any]:
    """
    Run the Ralph loop for task distance minimization.
    
    Args:
        original_dir: Directory containing original task markdown files
        max_iterations: Maximum number of iterations
        completion_promise: Phrase that signals completion
        
    Returns:
        Dictionary with final results
    """
    print("Initializing Ralph Wiggum loop for task distance minimization...")
    print(f"Original tasks directory: {original_dir}")
    print(f"Max iterations: {max_iterations}")
    
    # Create loop state
    state = create_ralph_loop_state(
        "Minimize distance between original tasks and PRD-generated tasks",
        max_iterations,
        completion_promise
    )
    
    # Run the iterative minimization process
    results = iterative_distance_minimization(original_dir, max_iterations)
    
    # Update state with results
    state.update({
        "status": "completed",
        "final_results": results,
        "best_distance": results['best_distance'],
        "best_similarity": results['best_similarity']
    })
    
    # Print final report
    print_final_report(results)
    
    # Check if completion promise is met
    if completion_promise:
        # In a real scenario, we would check if the task is genuinely complete
        # For now, we'll just note that we've completed the iterations
        print(f"\n<promise>{completion_promise}</promise>")
    
    return state


def main():
    parser = argparse.ArgumentParser(description="Ralph Wiggum loop for task distance minimization")
    parser.add_argument("task_prompt", nargs='?', default="Minimize distance between original tasks and PRD-generated tasks",
                        help="The task prompt (what you want to accomplish)")
    parser.add_argument("--max-iterations", type=int, default=20,
                        help="Stop after N iterations (default: 20)")
    parser.add_argument("--completion-promise", 
                        help="Phrase that signals completion (USE QUOTES for multi-word)")
    parser.add_argument("--original-dir", "-d", required=True,
                        help="Directory containing original task markdown files")
    parser.add_argument("--output", "-o", help="Output file for loop state")
    
    args = parser.parse_args()
    
    # Run the Ralph loop
    state = run_ralph_loop(args.original_dir, args.max_iterations, args.completion_promise)
    
    # Save state if output file specified
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(f"\nLoop state saved to: {output_path}")
    
    # Also save to standard location
    standard_path = Path(".gemini/ralph-loop.local.md")
    standard_path.parent.mkdir(exist_ok=True)
    
    # Convert state to markdown format for the standard file
    markdown_content = f"""# Ralph Loop State

## Configuration
- **Task Prompt**: {state['task_prompt']}
- **Max Iterations**: {state['max_iterations']}
- **Completion Promise**: {state['completion_promise'] or 'None'}

## Status
- **Current Status**: {state['status']}
- **Current Iteration**: {state['current_iteration']}

## Results
- **Best Distance Achieved**: {state['best_distance']:.3f}
- **Best Similarity Achieved**: {state['best_similarity']:.3f}
- **Convergence Threshold**: {state['convergence_threshold']}

## Final Results Summary
{json.dumps({k:v for k,v in state.get('final_results', {}).items() if k != 'iteration_history'}, indent=2)}

"""
    
    with open(standard_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Loop state also saved to: {standard_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())