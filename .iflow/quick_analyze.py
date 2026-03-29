import os
import json
import time
from datetime import datetime

PROJECT_ROOT = os.getcwd()
EXCLUDE_DIRS = {
    'node_modules', '.git', '.iflow', 'dist', 'build', '__pycache__', 
    'venv', '.venv', '.pytest_cache', '.mypy_cache', 'coverage'
}
EXCLUDE_EXTS = {
    '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.tar', '.gz', 
    '.exe', '.dll', '.so', '.pyc', '.class'
}

def analyze_structure():
    stats = {
        "files_count": 0,
        "dirs_count": 0,
        "languages": {},
        "structure": {},
        "top_level_dirs": []
    }
    
    start_time = time.time()
    
    # Walk directory
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # In-place filtering of directories to prevent traversal
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        rel_path = os.path.relpath(root, PROJECT_ROOT)
        if rel_path == ".":
            stats["top_level_dirs"] = dirs
            current_struct = stats["structure"]
        else:
            # Quick mode: Only map top-level and 1 level deep
            depth = rel_path.count(os.sep)
            if depth > 1:
                continue
            
            parts = rel_path.split(os.sep)
            if parts[0] not in stats["structure"]:
                stats["structure"][parts[0]] = []
            
        stats["dirs_count"] += len(dirs)
        
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue
                
            stats["files_count"] += 1
            stats["languages"][ext] = stats["languages"].get(ext, 0) + 1

    # Tech Stack Detection
    tech_stack = []
    if os.path.exists("package.json"): tech_stack.append("Node.js/TypeScript")
    if os.path.exists("pyproject.toml") or os.path.exists("requirements.txt"): tech_stack.append("Python")
    if os.path.exists("docker-compose.yml"): tech_stack.append("Docker")
    if os.path.exists("vite.config.ts"): tech_stack.append("Vite")
    if os.path.exists("tailwind.config.ts"): tech_stack.append("Tailwind CSS")

    result = {
        "timestamp": datetime.now().isoformat(),
        "mode": "quick",
        "root": PROJECT_ROOT,
        "metrics": {
            "total_files": stats["files_count"],
            "total_directories": stats["dirs_count"],
            "language_breakdown": stats["languages"],
            "duration_seconds": round(time.time() - start_time, 2)
        },
        "tech_stack": tech_stack,
        "structure_summary": {
            "roots": stats["top_level_dirs"],
            "key_modules": list(stats["structure"].keys())
        }
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    analyze_structure()
