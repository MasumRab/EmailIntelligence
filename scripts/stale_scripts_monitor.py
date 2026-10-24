#!/usr/bin/env python3
"""
Maintenance monitor for stale scripts.
Lists scripts/ files with their last-modified time and flags ones not touched in 90 days.
"""

import os
import subprocess
import time
from datetime import datetime

def get_file_last_modified_time(filepath: str) -> float:
    """Get the last modified time of a file using git."""
    try:
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", filepath],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        if output:
            return float(output)
    except subprocess.CalledProcessError:
        pass
        
    # Fallback to file system mtime if not tracked by git or git fails
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return time.time()

def check_stale_scripts(directory: str = "scripts", days_threshold: int = 90) -> dict:
    """
    Check scripts in a directory for staleness.
    Returns a dict with 'stale_files' and 'all_files'.
    """
    now = time.time()
    threshold_seconds = days_threshold * 24 * 60 * 60
    
    results = {
        "stale_files": [],
        "all_files": []
    }
    
    if not os.path.exists(directory):
        return results
        
    for root, _, files in os.walk(directory):
        for file in files:
            # Skip hidden files or __pycache__ if any
            if file.startswith('.') or '__pycache__' in root:
                continue
                
            filepath = os.path.join(root, file)
            mtime = get_file_last_modified_time(filepath)
            
            is_stale = (now - mtime) > threshold_seconds
            
            file_info = {
                "filepath": filepath,
                "last_modified": mtime,
                "is_stale": is_stale,
                "days_since_modified": (now - mtime) / (24 * 60 * 60)
            }
            
            results["all_files"].append(file_info)
            if is_stale:
                results["stale_files"].append(file_info)
                
    return results

def main():
    print("Checking for stale scripts...")
    results = check_stale_scripts()
    
    print(f"\nFound {len(results['all_files'])} total scripts.")
    print(f"Found {len(results['stale_files'])} stale scripts (not modified in >90 days):")
    
    # Sort stale files by staleness
    stale_sorted = sorted(results['stale_files'], key=lambda x: x['days_since_modified'], reverse=True)
    for f in stale_sorted:
        dt = datetime.fromtimestamp(f['last_modified']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  - {f['filepath']} (Last modified: {dt}, {f['days_since_modified']:.1f} days ago)")
        
if __name__ == "__main__":
    main()
