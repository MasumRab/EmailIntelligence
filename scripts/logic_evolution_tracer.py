#!/usr/bin/env python3
"""
Quick Logic Evolution Tracer

Fast tracing of how logic evolved across script versions to detect lost functionality.
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Any

def trace_function_evolution(script_files: List[str]) -> Dict[str, Any]:
    evolution = {
        "timeline": {},
        "added_functions": {},
        "removed_functions": {},
        "persistent_functions": set(),
        "function_count": {}
    }
    
    all_functions = set()
    
    for i, script_file in enumerate(script_files):
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        
        evolution["timeline"][f"v{i+1}_{Path(script_file).name}"] = sorted(functions)
        evolution["function_count"][f"v{i+1}"] = len(functions)
        
        if i == 0:
            evolution["persistent_functions"] = functions
        else:
            evolution["persistent_functions"] &= functions
        
        if i > 0:
            prev_file = script_files[i-1]
            prev_name = f"v{i}_{Path(prev_file).name}"
            curr_name = f"v{i+1}_{Path(script_file).name}"
            
            added = functions - evolution["timeline"][prev_name]
            removed = evolution["timeline"][prev_name] - functions
            
            evolution["added_functions"][curr_name] = sorted(added)
            evolution["removed_functions"][curr_name] = sorted(removed)
        
        all_functions |= functions
    
    return evolution

def trace_pattern_evolution(script_files: List[str]) -> Dict[str, Any]:
    """Trace how critical patterns evolved across script versions."""
    evolution = {
        "timeline": {},
        "added_patterns": {},
        "removed_patterns": {},
        "pattern_strength": {}
    }
    
    critical_patterns = {
        'dynamic_improvement': r'iteration\s*>\s*1.*prev_results',
        'adaptive_thresholding': r'similarity\s*<\s*0\.7|threshold.*0\.7',
        'layer_organization': r'foundation.*layer|dependent.*layer',
        'robust_parsing': r're\.split.*\[\,\s+\]|re\.sub.*\[\^0-9\.\]',
        'table_extraction': r'table.*row.*\||\|.*table',
        'iteration_tracking': r'iteration_history|best_results',
        'dependency_validation': r'dep_id.*validate|validate.*dependency',
        'self_healing': r'improvement.*threshold'
    }
    
    for i, script_file in enumerate(script_files):
        with open(script_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        version_name = f"v{i+1}_{Path(script_file).name}"
        evolution["timeline"][version_name] = {}
        
        pattern_matches = 0
        for pattern_name, pattern in critical_patterns.items():
            has_pattern = bool(re.search(pattern, content, re.IGNORECASE))
            evolution["timeline"][version_name][pattern_name] = has_pattern
            if has_pattern:
                pattern_matches += 1
        
        evolution["pattern_strength"][version_name] = pattern_matches
        
        if i > 0:
            prev_name = f"v{i}_{Path(script_files[i-1]).name}"
            
            added_patterns = []
            removed_patterns = []
            
            for pattern_name in critical_patterns:
                had_pattern = evolution["timeline"][prev_name].get(pattern_name, False)
                has_pattern = evolution["timeline"][version_name].get(pattern_name, False)
                
                if has_pattern and not has_pattern:
                    removed_patterns.append(pattern_name)
                elif not had_pattern and has_pattern:
                    added_patterns.append(pattern_name)
            
            if added_patterns:
                evolution["added_patterns"][version_name] = added_patterns
            if removed_patterns:
                evolution["removed_patterns"][version_name] = removed_patterns
    
    return evolution

def analyze_function_complexity(script_file: str) -> Dict[str, Any]:
    """Analyze complexity of functions in a script."""
    with open(script_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tree = ast.parse(content)
    complexity = {
        'total_functions': 0,
        'avg_lines_per_function': 0,
        'max_lines_per_function': 0,
        'complex_functions': []
    }
    
    function_lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            complexity['total_functions'] += 1
            lines = node.end_lineno - node.start_lineno + 1
            function_lines.append(lines)
            
            if lines > 50:  # Complex function threshold
                complexity['complex_functions'].append({
                    'name': node.name,
                    'lines': lines
                })
    
    if function_lines:
        complexity['avg_lines_per_function'] = sum(function_lines) / len(function_lines)
        complexity['max_lines_per_function'] = max(function_lines)
    
    return complexity

def main():
    if len(sys.argv) < 2:
        print("Usage: python logic_evolution_tracer.py script1.py script2.py [script3.py ...]")
        print("Example: python logic_evolution_tracer.py enhanced_iterative.py advanced_iterative.py ultra_iterative.py")
        sys.exit(1)
    
    script_files = sys.argv[1:]
    
    print(f"🔍 Tracing evolution across {len(script_files)} scripts...")
    print("=" * 60)
    
    # Trace function evolution
    function_evolution = trace_function_evolution(script_files)
    pattern_evolution = trace_pattern_evolution(script_files)
    
    # Print function evolution
    print("\n📊 FUNCTION EVOLUTION:")
    for version, functions in function_evolution["timeline"].items():
        print(f"   {version}: {len(functions)} functions")
    
    print(f"\n📈 Function Changes:")
    for transition, changes in function_evolution["added_functions"].items():
        if function_evolution["removed_functions"].get(transition):
            print(f"   {transition}:")
            print(f"      + Added: {', '.join(changes)}")
            print(f"      - Removed: {', '.join(function_evolution['removed_functions'][transition])}")
        elif changes:
            print(f"   {transition}: + Added: {', '.join(changes)}")
    
    # Print pattern evolution
    print(f"\n🎯 PATTERN EVOLUTION:")
    for version, patterns in pattern_evolution["timeline"].items():
        active_patterns = [name for name, active in patterns.items() if active]
        print(f"   {version}: {len(active_patterns)} critical patterns")
        if active_patterns:
            print(f"      Active: {', '.join(active_patterns)}")
    
    print(f"\n🚨 PATTERN LOSSES:")
    for transition, lost_patterns in pattern_evolution["removed_patterns"].items():
        print(f"   {transition}: LOST {', '.join(lost_patterns)}")
    
    # Analyze complexity
    print(f"\n📏 COMPLEXITY ANALYSIS:")
    for script_file in script_files:
        complexity = analyze_function_complexity(script_file)
        script_name = Path(script_file).name
        print(f"   {script_name}:")
        print(f"      Functions: {complexity['total_functions']}")
        print(f"      Avg Lines: {complexity['avg_lines_per_function']:.1f}")
        print(f"      Max Lines: {complexity['max_lines_per_function']}")
        if complexity['complex_functions']:
            print(f"      Complex: {[f['name']}({f['lines']}L)" for f in complexity['complex_functions']]}")
    
    # Identify critical losses
    critical_losses = []
    for transition, lost_patterns in pattern_evolution["removed_patterns"].items():
        critical_patterns = [p for p in lost_patterns if p in [
            'dynamic_improvement', 'adaptive_thresholding', 'layer_organization', 
            'robust_parsing', 'table_extraction'
        ]]
        if critical_patterns:
            critical_losses.append(f"{transition}: {', '.join(critical_patterns)}")
    
    if critical_losses:
        print(f"\n🚨 CRITICAL LOSSES DETECTED:")
        for loss in critical_losses:
            print(f"   {loss}")
        print(f"\n❌ REGRESSION ALERT - Review before consolidation!")
        return 1
    else:
        print(f"\n✅ No critical losses detected!")
        return 0

if __name__ == "__main__":
    main()