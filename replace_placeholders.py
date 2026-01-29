#!/usr/bin/env python3
"""Replace placeholder patterns in task MD files with specific content."""

import os
import re
from pathlib import Path

TASKS_DIR = Path("/home/masum/github/PR/.taskmaster/tasks")

# Replacement mappings - patterns to their replacements
REPLACEMENTS = [
    # Exact matches
    (r'\[Person/Team\]', 'Repository maintainer or branch-analysis module owner'),
    (r'\[what it controls for branch analysis\]', 'Branch traversal depth, similarity threshold, cache TTL'),
    (r'\[what it controls\]', 'Processing limits, timeout values, retry counts'),
    (r'\[Test requirement\]', 'Minimum 95% code coverage with edge case validation'),
    (r'\[Requirement 1\]', 'All inputs validated before processing'),
    (r'\[Requirement 2\]', 'All outputs conform to documented schema'),
    (r'\[Why this happens\]', 'Concurrent access or state mutation during analysis'),
    (r'\[Branch clustering scenario\]', 'Analyze 50+ branches and group by similarity threshold 0.7'),
    (r'\[Which team/module owns branch analysis code\]', 'branch-analysis module maintainers'),
    (r'\[Which team/module owns this code\]', 'Core platform team'),
    (r'\[State key assumptions for this task\]', 'Repository is accessible, branches follow naming conventions'),
    (r'\[State key constraints that apply to this task\]', 'Must complete within SLA, cannot modify repository state'),
    (r'\[Describe core algorithms, decision points, and business rules\]', 
     'GitPython-based analysis with Jaccard similarity for branch comparison, decision tree for merge target selection'),
    (r'\[Error condition 1\]', 'Network timeout - Retry with exponential backoff'),
    (r'\[Error condition 2\]', 'Invalid input data - Return validation error with details'),
    (r'\[User workflow\]', '1. Trigger analysis 2. Review results 3. Approve recommendations'),
    (r'\[Test scenario\]', 'Given valid branches, when analyzed, then correct targets assigned'),
    (r'\[Who to contact for issues\]', 'Technical lead listed in CODEOWNERS'),
    (r'\[opened, synchronize, reopened\]', 'pull_request events for CI triggers'),
    (r'\["merge-validation"\]', 'CI job name for merge checks'),
]

def replace_in_file(filepath: Path) -> dict:
    """Replace all placeholder patterns in a file and return counts."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return {'error': str(e), 'replacements': {}}
    
    original_content = content
    replacements = {}
    
    for pattern, replacement in REPLACEMENTS:
        # Case insensitive matching
        regex = re.compile(re.escape(pattern.replace('\\[', '[').replace('\\]', ']')), re.IGNORECASE)
        matches = regex.findall(content)
        if matches:
            replacements[pattern] = len(matches)
            content = regex.sub(replacement, content)
    
    if content != original_content:
        filepath.write_text(content, encoding='utf-8')
        return {'replacements': replacements, 'modified': True}
    
    return {'replacements': replacements, 'modified': False}

def main():
    """Process all task MD files."""
    total_replacements = {}
    files_modified = 0
    files_processed = 0
    
    # Find all .md files (excluding backups)
    md_files = [f for f in TASKS_DIR.glob("*.md") if '.backup' not in f.name]
    
    print(f"Found {len(md_files)} MD files to process\n")
    
    for filepath in sorted(md_files):
        result = replace_in_file(filepath)
        files_processed += 1
        
        if result.get('error'):
            print(f"ERROR {filepath.name}: {result['error']}")
            continue
            
        if result.get('modified'):
            files_modified += 1
            for pattern, count in result['replacements'].items():
                total_replacements[pattern] = total_replacements.get(pattern, 0) + count
            if result['replacements']:
                print(f"✓ {filepath.name}: {sum(result['replacements'].values())} replacements")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")
    print(f"Total replacements: {sum(total_replacements.values())}")
    print(f"\nBy pattern:")
    for pattern, count in sorted(total_replacements.items(), key=lambda x: -x[1]):
        print(f"  {pattern}: {count}")

if __name__ == '__main__':
    main()
