#!/usr/bin/env python3
"""
Quick Script Feature Comparison Matrix Generator

Fast comparison of functions and features across script versions to prevent functionality loss during consolidation.
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Any

def extract_functions_from_file(file_path: str) -> Set[str]:
    """Extract function names from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        return functions
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return set()

def extract_classes_from_file(file_path: str) -> Set[str]:
    """Extract class names from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        classes = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
        return classes
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return set()

def extract_imports_from_file(file_path: str) -> Set[str]:
    """Extract import statements from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
        return imports
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return set()

def detect_critical_patterns(file_path: str) -> Dict[str, bool]:
    """Detect critical functionality patterns in a Python file."""
    patterns = {
        'dynamic_improvement': False,
        'adaptive_thresholding': False,
        'layer_organization': False,
        'robust_parsing': False,
        'table_extraction': False,
        'iteration_tracking': False,
        'dependency_validation': False,
        'self_healing': False
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Critical pattern detection
        patterns['dynamic_improvement'] = 'iteration > 1' in content and 'prev_results' in content
        patterns['adaptive_thresholding']'] = 'similarity < 0.7' in content or 'threshold.*0.7' in content
        patterns['layer_organization'] = 'foundation' in content and 'layer' in content
        patterns['robust_parsing'] = 're.split' in content and 're.sub' in content
        patterns['table_extraction'] = 'table' in content and 'row' in content and '|' in content
        patterns['iteration_tracking'] = 'iteration_history' in content or 'best_results' in content
        patterns['dependency_validation'] = 'dep_id' in content and 'validate' in content
        patterns['self_healing'] = 'improvement' in content and 'threshold' in content
        
    except Exception as e:
        print(f"Error detecting patterns in {file_path}: {e}")
    
    return patterns

def compare_script_chain(script_files: List[str]) -> Dict[str, Any]:
    """Compare a chain of scripts and identify missing functionality."""
    if not script_files:
        return {"error": "No script files provided"}
    
    comparison = {
        "scripts": script_files,
        "functions": {},
        "classes": {},
        "imports": {},
        "patterns": {},
        "missing_functionality": {},
        "regression_warnings": []
    }
    
    # Extract features from each script
    for script_file in script_files:
        comparison["functions"][script_file] = extract_functions_from_file(script_file)
        comparison["classes"][script_file] = extract_classes_from_file(script_file)
        comparison["imports"][script_file] = extract_imports_from_file(script_file)
        comparison["patterns"][script_file] = detect_critical_patterns(script_file)
    
    # Identify missing functionality (present in older, missing in newer)
    for i in range(1, len(script_files)):
        older_script = script_files[i-1]
        newer_script = script_files[i]
        
        missing_functions = comparison["functions"][older_script] - comparison["functions"][newer_script]
        missing_classes = comparison["classes"][older_script] - comparison["classes"][newer_script]
        missing_patterns = {}
        
        for pattern, has_pattern in comparison["patterns"][older_script].items():
            if has_pattern and not comparison["patterns"][newer_script][pattern]:
                missing_patterns[pattern] = True
        
        if missing_functions or missing_classes or missing_patterns:
            comparison["missing_functionality"][f"{older_script} → {newer_script}"] = {
                "missing_functions": list(missing_functions),
                "missing_classes": list(missing_classes),
                "missing_patterns": list(missing_patterns.keys())
            }
            
            # Generate regression warnings
            if missing_functions:
                comparison["regression_warnings"].append(
                    f"⚠️ {newer_script} is missing functions: {', '.join(missing_functions)}"
                )
            if missing_patterns:
                comparison["regression_warnings"].append(
                    f"🚨 {newer_script} is missing critical patterns: {', '.join(missing_patterns.keys())}"
                )
    
    return comparison

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_feature_matrix.py script1.py script2.py [script3.py ...]")
        print("Example: python script_feature_matrix.py enhanced_iterative.py advanced_iterative.py")
        sys.exit(1)
    
    script_files = sys.argv[1:]
    
    # Verify all files exist
    for script_file in script_files:
        if not Path(script_file).exists():
            print(f"❌ File not found: {script_file}")
            sys.exit(1)
    
    print(f"🔍 Comparing {len(script_files)} scripts...")
    print("=" * 60)
    
    # Perform comparison
    result = compare_script_chain(script_files)
    
    # Print results
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    # Print feature matrix
    print("\n📊 FEATURE MATRIX:")
    for script_file in script_files:
        print(f"\n🔹 {script_file}:")
        print(f"   Functions: {len(result['functions'][script_file])}")
        print(f"   Classes: {len(result['classes'][script_file])}")
        print(f"   Critical Patterns: {sum(result['patterns'][script_file].values())}")
    
    # Print missing functionality
    if result["missing_functionality"]:
        print("\n🚨 MISSING FUNCTIONALITY DETECTED:")
        for transition, missing in result["missing_functionality"].items():
            print(f"\n❌ {transition}:")
            if missing["missing_functions"]:
                print(f"   Functions: {', '.join(missing['missing_functions'])}")
            if missing["missing_classes"]:
                print(f"   Classes: {', '.join(missing['missing_classes'])}")
            if missing["missing_patterns"]:
                print(f"   Critical Patterns: {', '.join(missing['missing_patterns'])}")
    else:
        print("\n✅ No missing functionality detected!")
    
    # Print regression warnings
    if result["regression_warnings"]:
        print("\n🚨 REGRESSION WARNINGS:")
        for warning in result["regression_warnings"]:
            print(f"   {warning}")
    
    # Save detailed results
    output_file = "script_comparison_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed results saved to: {output_file}")
    
    # Return exit code based on whether regressions were found
    if result["regression_warnings"]:
        print("\n❌ REGRESSIONS DETECTED - Review before consolidation!")
        sys.exit(1)
    else:
        print("\n✅ No regressions detected - Safe to proceed!")
        sys.exit(0)

if __name__ == "__main__":
    main()