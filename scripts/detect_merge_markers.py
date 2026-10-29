#!/usr/bin/env python3
"""
Detects merge conflict markers in given files.
"""

import sys
import os
from pathlib import Path

def detect_merge_markers(files):
    errors = []
    patterns = ('<<<<<<<', '=======', '>>>>>>>')
    
    for f in files:
        # Sanitize input path to prevent path traversal
        path = Path(f).resolve()
        
        # Ensure it's within the current working directory
        if not str(path).startswith(str(Path.cwd())):
            errors.append(f"PATH TRAVERSAL ERROR: Path must be within current directory: {f}")
            continue

        if not path.is_file():
            continue
            
        try:
            with open(path, 'r', encoding='utf-8') as fp:
                for i, line in enumerate(fp, 1):
                    if line.startswith(patterns):
                        errors.append(f"MERGE MARKER: {f}:{i}")
        except UnicodeDecodeError:
            # Skip binary files or files with encoding issues for now
            pass
        except Exception as e:
            errors.append(f"READ ERROR: {f} - {e}")
            
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect_merge_markers.py <file1> <file2> ...")
        sys.exit(0)
        
    files = sys.argv[1:]
    errors = detect_merge_markers(files)
    
    if errors:
        print("ERRORS DETECTED:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("No errors detected")
        sys.exit(0)
