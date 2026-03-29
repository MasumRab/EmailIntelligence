import os
import json
import time
import re
from datetime import datetime

PROJECT_ROOT = os.getcwd()
EXCLUDE_DIRS = {
    'node_modules', '.git', '.iflow', 'dist', 'build', '__pycache__', 
    'venv', '.venv', '.pytest_cache', '.mypy_cache', 'coverage', 'tests', 'test_data', 'archive'
}
EXCLUDE_EXTS = {
    '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.tar', '.gz', 
    '.exe', '.dll', '.so', '.pyc', '.class', '.md', '.txt', '.jsonl'
}

def parse_imports(file_path):
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Python imports
            imports.extend(re.findall(r'^import\s+(\w+)', content, re.MULTILINE))
            imports.extend(re.findall(r'^from\s+(\w+)', content, re.MULTILINE))
            # JS/TS imports
            imports.extend(re.findall(r'import\s+.*\s+from\s+[\'"](.+)[\'"]', content))
    except Exception:
        pass
    return list(set(imports))

def analyze_standard():
    stats = {
        "components": {},
        "relationships": [],
        "file_map": {}
    }
    
    start_time = time.time()
    
    # 1. Map Files & Components
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue
                
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, PROJECT_ROOT)
            
            # Identify Component/Module
            parts = rel_path.split(os.sep)
            component = parts[0]
            if component == "src" and len(parts) > 1:
                component = f"src/{parts[1]}"
            elif component == "client" and len(parts) > 2: # client/src/...
                component = f"client/{parts[1]}/{parts[2]}" if parts[1] == 'src' else f"client/{parts[1]}"
            
            if component not in stats["components"]:
                stats["components"][component] = {"files": 0, "type": "module"}
            
            stats["components"][component]["files"] += 1
            stats["file_map"][rel_path] = component
            
            # 2. Map Relationships (Imports)
            if ext in ['.py', '.ts', '.tsx', '.js']:
                imports = parse_imports(full_path)
                for imp in imports:
                    # Simple heuristic mapping
                    target = None
                    if imp.startswith('.'): continue # Skip relative for high-level graph
                    
                    # Check known internal modules
                    if imp in ['src', 'modules', 'client']: target = imp
                    elif f"src/{imp}" in stats["components"]: target = f"src/{imp}"
                    
                    if target and target != component:
                        stats["relationships"].append({
                            "source": component,
                            "target": target,
                            "type": "dependency"
                        })

    # Deduplicate relationships
    unique_rels = [dict(t) for t in {tuple(d.items()) for d in stats["relationships"]}]

    result = {
        "timestamp": datetime.now().isoformat(),
        "mode": "standard",
        "root": PROJECT_ROOT,
        "metrics": {
            "component_count": len(stats["components"]),
            "relationship_count": len(unique_rels),
            "duration_seconds": round(time.time() - start_time, 2)
        },
        "architecture": {
            "components": stats["components"],
            "relationships": unique_rels
        }
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    analyze_standard()
