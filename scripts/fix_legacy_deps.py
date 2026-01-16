#!/usr/bin/env python3
"""
Fix legacy task dependencies in markdown files.
"""

import re
from pathlib import Path

# Mapping of legacy ID -> New ID (formatted)
ID_MAP = {
    # Core Validation/Setup
    r'\b19\b': '003',
    r'\b19\.': '003.',
    
    # Core Framework
    r'\b54\b': '004',
    r'\b54\.': '004.',
    
    # Error Detection
    r'\b55\b': '005',
    r'\b55\.': '005.',
    
    # Backup
    r'\b56\b': '006',
    r'\b56\.': '006.',
    
    # Branch ID
    r'\b57\b': '007',
    r'\b57\.': '007.',
    
    # Documentation/Summary
    r'\b58\b': '008',
    r'\b58\.': '008.',
    
    # Core Alignment
    r'\b59\b': '009',
    r'\b59\.': '009.',
    
    # Complex Strategies
    r'\b60\b': '010',
    r'\b60\.': '010.',
    
    # Complex Handling (Advanced)
    r'\b61\b': '011',
    r'\b61\.': '011.',
    
    # Validation Integration
    r'\b62\b': '012',
    r'\b62\.': '012.',
    
    # Orchestration
    r'\b14\b': '013',
    r'\b14\.': '013.',
    
    # Final Docs
    r'\b63\b': '015',
    r'\b63\.': '015.',
    
    # Scientific Recovery
    r'\b17\b': '016',
    r'\b17\.': '016.',
    
    # Orchestration Tools Alignment
    r'\b18\b': '017',
    r'\b18\.': '017.',
    
    # Conflict Scan
    r'\b23\b': '019',
    r'\b23\.': '019.',
    
    # Launch.py
    r'\b24\b': '020',
    r'\b24\.': '020.',
}

def fix_dependencies():
    tasks_dir = Path("tasks")
    for task_file in tasks_dir.glob("task-*.md"):
        content = task_file.read_text()
        original_content = content
        
        # Replace in "Dependencies:" lines
        def replace_deps(match):
            line = match.group(0)
            for old, new in ID_MAP.items():
                line = re.sub(old, new, line)
            return line

        content = re.sub(r'^\*\*Dependencies:\*\*.*$', replace_deps, content, flags=re.MULTILINE)
        
        # Replace in "### Subtasks" headers (e.g., ### 59.1. -> ### 009.1.)
        def replace_headers(match):
            line = match.group(0)
            for old, new in ID_MAP.items():
                line = re.sub(old, new, line)
            return line
            
        content = re.sub(r'^### \d+\..*$', replace_headers, content, flags=re.MULTILINE)

        if content != original_content:
            task_file.write_text(content)
            print(f"Updated {task_file.name}")

if __name__ == "__main__":
    fix_dependencies()
