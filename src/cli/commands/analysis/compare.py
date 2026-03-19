"""
Compare Command Module

Implements a command for comparing functions and features across script versions.
Ported from script_feature_matrix.py.
"""

import ast
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Set

from ..interface import Command


class CompareCommand(Command):
    """
    Command for comparing features across different script versions.
    
    Helps prevent functionality loss during consolidation by identifying 
    missing functions, classes, and patterns in newer script versions.
    """

    @property
    def name(self) -> str:
        return "compare"

    @property
    def description(self) -> str:
        return "Compare features across script versions to prevent functionality loss"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "scripts", 
            nargs="+", 
            help="List of script files to compare (in chronological order)"
        )
        parser.add_argument(
            "--json", 
            action="store_true", 
            help="Output comparison results as JSON"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {}

    async def execute(self, args: Namespace) -> int:
        """Execute the comparison command."""
        script_files = args.scripts
        
        # Verify all files exist
        for script_file in script_files:
            if not Path(script_file).exists():
                print(f"Error: File not found: {script_file}")
                return 1

        print(f"Comparing {len(script_files)} scripts...")
        
        comparison = self._compare_script_chain(script_files)
        
        if args.json:
            import json
            print(json.dumps(comparison, indent=2))
        else:
            self._print_comparison_report(comparison, script_files)
            
        return 0

    def _extract_features(self, file_path: str) -> Dict[str, Set[str]]:
        """Extract functions, classes, and imports from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
            
            features = {
                "functions": {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)},
                "classes": {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)},
                "imports": set()
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        features["imports"].add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        features["imports"].add(node.module)
            
            return features
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return {"functions": set(), "classes": set(), "imports": set()}

    def _detect_patterns(self, file_path: str) -> Dict[str, bool]:
        """Detect critical functionality patterns."""
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
            
            # Pattern detection logic
            patterns['dynamic_improvement'] = 'iteration > 1' in content and 'prev_results' in content
            patterns['adaptive_thresholding'] = 'similarity < 0.7' in content or 'threshold.*0.7' in content
            patterns['layer_organization'] = 'foundation' in content and 'layer' in content
            patterns['robust_parsing'] = 're.split' in content and 're.sub' in content
            patterns['table_extraction'] = 'table' in content and 'row' in content and '|' in content
            patterns['iteration_tracking'] = 'iteration_history' in content or 'best_results' in content
            patterns['dependency_validation'] = 'dep_id' in content and 'validate' in content
            patterns['self_healing'] = 'improvement' in content and 'threshold' in content
            
        except Exception:
            pass
        
        return patterns

    def _compare_script_chain(self, script_files: List[str]) -> Dict[str, Any]:
        """Compare a chain of scripts."""
        comparison = {
            "functions": {},
            "classes": {},
            "imports": {},
            "patterns": {},
            "missing": {}
        }
        
        for script_file in script_files:
            features = self._extract_features(script_file)
            comparison["functions"][script_file] = list(features["functions"])
            comparison["classes"][script_file] = list(features["classes"])
            comparison["imports"][script_file] = list(features["imports"])
            comparison["patterns"][script_file] = self._detect_patterns(script_file)
        
        # Identify missing functionality between transitions
        for i in range(1, len(script_files)):
            older = script_files[i-1]
            newer = script_files[i]
            
            missing_functions = set(comparison["functions"][older]) - set(comparison["functions"][newer])
            missing_classes = set(comparison["classes"][older]) - set(comparison["classes"][newer])
            
            missing_patterns = []
            for pattern, has_pattern in comparison["patterns"][older].items():
                if has_pattern and not comparison["patterns"][newer][pattern]:
                    missing_patterns.append(pattern)
            
            if missing_functions or missing_classes or missing_patterns:
                comparison["missing"][f"{older} -> {newer}"] = {
                    "functions": list(missing_functions),
                    "classes": list(missing_classes),
                    "patterns": missing_patterns
                }
        
        return comparison

    def _print_comparison_report(self, comparison: Dict[str, Any], script_files: List[str]) -> None:
        """Print human-readable comparison report."""
        print("\n" + "=" * 40)
        print("FEATURE MATRIX")
        print("=" * 40)
        
        for script in script_files:
            print(f"\n- {script}:")
            print(f"  Functions: {len(comparison['functions'][script])}")
            print(f"  Classes:   {len(comparison['classes'][script])}")
            print(f"  Patterns:  {sum(comparison['patterns'][script].values())}")

        if comparison["missing"]:
            print("\n" + "!" * 40)
            print("MISSING FUNCTIONALITY DETECTED")
            print("!" * 40)
            
            for transition, missing in comparison["missing"].items():
                print(f"\n[ {transition} ]")
                if missing["functions"]:
                    print(f"  Missing Functions: {', '.join(missing['functions'])}")
                if missing["classes"]:
                    print(f"  Missing Classes:   {', '.join(missing['classes'])}")
                if missing["patterns"]:
                    print(f"  Missing Patterns:  {', '.join(missing['patterns'])}")
        else:
            print("\n" + "v" * 40)
            print("NO REGRESSIONS DETECTED")
            print("v" * 40)
