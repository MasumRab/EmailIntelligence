#!/usr/bin/env python3
"""
Find tasks in git history that are not in current task JSON files
Usage: python scripts/find_lost_tasks.py [--commits N] [--output FILE]
"""

import json
import sys
import subprocess
import argparse
import re
from pathlib import Path
from collections import defaultdict

def get_git_commits(file_path, max_commits=50):
    """Get list of commits that modified the task files"""
    try:
        result = subprocess.run(
            ['git', 'log', '--format=%H', '--all', '--', str(file_path)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        commits = result.stdout.strip().split('\n')
        return [c for c in commits if c][:max_commits]
    except Exception as e:
        print(f"Error getting git commits: {e}", file=sys.stderr)
        return []

def get_file_at_commit(commit_hash, file_path):
    """Get file contents at a specific commit"""
    try:
        result = subprocess.run(
            ['git', 'show', f'{commit_hash}:{file_path}'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception as e:
        return None

def extract_tasks_from_json(content, tag="master"):
    """Extract tasks from JSON content"""
    tasks = []
    try:
        data = json.loads(content)
        
        if tag in data:
            tasks = data[tag].get('tasks', [])
        elif 'tasks' in data:
            tasks = data['tasks']
        elif isinstance(data, list):
            tasks = data
        
        return tasks
    except json.JSONDecodeError:
        # Try regex parsing for malformed JSON
        return extract_tasks_regex(content)

def extract_tasks_regex(content):
    """Extract tasks using regex (for malformed JSON)"""
    tasks = []
    lines = content.split('\n')
    depth = 0
    in_subtasks = False
    
    for i, line in enumerate(lines):
        depth += line.count('{') - line.count('}')
        if '"subtasks"' in line and '[' in line:
            in_subtasks = True
        if in_subtasks and depth <= 1:
            in_subtasks = False
        
        if not in_subtasks and depth == 1:
            id_match = re.search(r'"id":\s*(\d+)', line)
            if id_match:
                task_id = int(id_match.group(1))
                if 1 <= task_id <= 20:  # Reasonable task ID range
                    title = None
                    status = None
                    for j in range(i, min(i+30, len(lines))):
                        if title is None:
                            title_match = re.search(r'"title":\s*"([^"]+)"', lines[j])
                            if title_match:
                                title = title_match.group(1)
                        if status is None:
                            status_match = re.search(r'"status":\s*"([^"]+)"', lines[j])
                            if status_match:
                                status = status_match.group(1)
                        if title and status:
                            break
                    
                    if title and status:
                        tasks.append({
                            'id': task_id,
                            'title': title,
                            'status': status
                        })
    
    seen = set()
    return [t for t in tasks if t['id'] not in seen and not seen.add(t['id'])]

def get_task_signature(task):
    """Get unique signature for a task"""
    return (task.get('id'), task.get('title', ''))

def load_current_tasks(script_dir):
    """Load all current tasks from JSON files"""
    current_tasks = set()
    
    # Load from tasks.json
    tasks_file = script_dir / 'tasks/tasks.json'
    if tasks_file.exists():
        with open(tasks_file, 'r') as f:
            data = json.load(f)
            tasks = data.get('master', {}).get('tasks', [])
            for task in tasks:
                current_tasks.add(get_task_signature(task))
    
    # Load from tasks_invalid.json
    invalid_file = script_dir / 'tasks/tasks_invalid.json'
    if invalid_file.exists():
        try:
            with open(invalid_file, 'r') as f:
                content = f.read()
                tasks = extract_tasks_from_json(content)
                for task in tasks:
                    current_tasks.add(get_task_signature(task))
        except:
            tasks = extract_tasks_regex(open(invalid_file, 'r').read())
            for task in tasks:
                current_tasks.add(get_task_signature(task))
    
    # Load from tasks_expanded.json
    expanded_file = script_dir / 'tasks/tasks_expanded.json'
    if expanded_file.exists():
        with open(expanded_file, 'r') as f:
            data = json.load(f)
            tasks = data.get('master', {}).get('tasks', [])
            for task in tasks:
                current_tasks.add(get_task_signature(task))
    
    return current_tasks

def main():
    parser = argparse.ArgumentParser(description='Find tasks in git history not in current files')
    parser.add_argument('--commits', type=int, default=50, help='Max commits to check (default: 50)')
    parser.add_argument('--output', help='Output file for results (JSON)')
    parser.add_argument('--verbose', action='store_true', help='Show detailed progress')
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent.parent
    
    print("=" * 70)
    print("FINDING LOST TASKS IN GIT HISTORY")
    print("=" * 70)
    print()
    
    # Get current tasks
    print("Loading current tasks...")
    current_tasks = load_current_tasks(script_dir)
    print(f"Found {len(current_tasks)} unique tasks in current files")
    print()
    
    # Check git history for task files
    task_files = [
        'tasks/tasks.json',
        'tasks/tasks_invalid.json',
        'tasks/tasks_expanded.json',
        'tasks/tasks_new.json'
    ]
    
    all_historical_tasks = defaultdict(list)  # task_sig -> [(commit, file, task_data)]
    
    for task_file in task_files:
        print(f"Checking git history for {task_file}...")
        commits = get_git_commits(task_file, args.commits)
        
        if not commits:
            print(f"  No git history found for {task_file}")
            continue
        
        print(f"  Found {len(commits)} commits, checking...")
        
        for i, commit in enumerate(commits):
            if args.verbose:
                print(f"    Checking commit {commit[:8]} ({i+1}/{len(commits)})...")
            
            content = get_file_at_commit(commit, task_file)
            if not content:
                continue
            
            tasks = extract_tasks_from_json(content)
            if not tasks:
                tasks = extract_tasks_regex(content)
            
            for task in tasks:
                sig = get_task_signature(task)
                if sig not in current_tasks:
                    all_historical_tasks[sig].append({
                        'commit': commit,
                        'file': task_file,
                        'task': task
                    })
    
    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()
    
    if not all_historical_tasks:
        print("No lost tasks found in git history!")
        return
    
    print(f"Found {len(all_historical_tasks)} unique tasks in history that are not in current files:\n")
    
    # Group by task ID
    by_id = defaultdict(list)
    for sig, occurrences in all_historical_tasks.items():
        task_id, title = sig
        by_id[task_id].append((title, occurrences))
    
    results = []
    for task_id in sorted(by_id.keys()):
        for title, occurrences in by_id[task_id]:
            # Get most recent occurrence
            most_recent = max(occurrences, key=lambda x: x['commit'])
            task_data = most_recent['task']
            
            print(f"Task {task_id}: {title}")
            print(f"  Status: {task_data.get('status', 'N/A')}")
            print(f"  Priority: {task_data.get('priority', 'N/A')}")
            print(f"  Found in {len(occurrences)} commit(s):")
            for occ in occurrences[:3]:  # Show first 3
                commit_msg = subprocess.run(
                    ['git', 'log', '-1', '--format=%s', occ['commit']],
                    capture_output=True,
                    text=True,
                    cwd=script_dir
                ).stdout.strip()
                print(f"    - {occ['commit'][:8]} in {occ['file']}: {commit_msg}")
            if len(occurrences) > 3:
                print(f"    ... and {len(occurrences) - 3} more")
            print()
            
            results.append({
                'id': task_id,
                'title': title,
                'status': task_data.get('status'),
                'priority': task_data.get('priority'),
                'occurrences': [
                    {
                        'commit': occ['commit'],
                        'file': occ['file'],
                        'commit_message': subprocess.run(
                            ['git', 'log', '-1', '--format=%s', occ['commit']],
                            capture_output=True,
                            text=True,
                            cwd=script_dir
                        ).stdout.strip()
                    }
                    for occ in occurrences
                ],
                'task_data': task_data
            })
    
    # Save to file if requested
    if args.output:
        output_file = script_dir / args.output
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_file}")

if __name__ == '__main__':
    main()
