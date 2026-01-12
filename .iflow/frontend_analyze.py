import os
import json
import re
import time

PROJECT_ROOT = os.getcwd()
CLIENT_ROOT = os.path.join(PROJECT_ROOT, "client")

def parse_package_json():
    try:
        with open(os.path.join(CLIENT_ROOT, "package.json"), 'r') as f:
            data = json.load(f)
            return {
                "dependencies": list(data.get("dependencies", {}).keys()),
                "devDependencies": list(data.get("devDependencies", {}).keys())
            }
    except:
        return {"error": "No package.json found"}

def find_components():
    components = {}
    
    for root, _, files in os.walk(os.path.join(CLIENT_ROOT, "src")):
        for f in files:
            if f.endswith(('.tsx', '.jsx')):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, CLIENT_ROOT)
                name = os.path.splitext(f)[0]
                
                with open(full_path, 'r') as content_file:
                    content = content_file.read()
                    
                    # Detect Hooks
                    hooks = re.findall(r'use[A-Z]\w+', content)
                    
                    # Detect Imports (Child Components)
                    imports = re.findall(r'import\s+(\w+)\s+from', content)
                    
                    components[rel_path] = {
                        "name": name,
                        "hooks": list(set(hooks)),
                        "imports": list(set(imports)),
                        "is_page": "pages" in rel_path,
                        "is_context": "context" in rel_path or "provider" in name.lower()
                    }
    return components

def analyze_frontend():
    if not os.path.exists(CLIENT_ROOT):
        print(json.dumps({"error": "Client directory not found"}))
        return

    start_time = time.time()
    
    pkg_data = parse_package_json()
    components = find_components()
    
    # Analyze State Management
    state_mgmt = {
        "contexts": [c for c, data in components.items() if data["is_context"]],
        "custom_hooks": [c for c in components.keys() if "hooks/" in c]
    }
    
    # Analyze Routing (Basic heuristic)
    routes = []
    for c, data in components.items():
        if "router" in str(data["imports"]).lower() or "route" in str(data["imports"]).lower():
            routes.append(c)

    result = {
        "timestamp": time.time(),
        "mode": "deep-frontend",
        "root": CLIENT_ROOT,
        "metrics": {
            "component_count": len(components),
            "duration_seconds": round(time.time() - start_time, 2)
        },
        "dependencies": pkg_data,
        "architecture": {
            "components": components,
            "state_management": state_mgmt,
            "routing_components": routes
        }
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    analyze_frontend()
