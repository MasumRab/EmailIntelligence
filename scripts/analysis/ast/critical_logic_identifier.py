#!/usr/bin/env python3
"""
Quick Critical Logic Identification System

Fast detection of critical functionality that must be preserved during consolidation.
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Any


def analyze_function_importance(
    func_name: str, func_node: ast.FunctionDef, content: str
) -> Dict[str, Any]:
    """Analyze how critical a function is based on patterns and usage."""
    importance = {
        "name": func_name,
        "critical": False,
        "reasons": [],
        "complexity": 0,
        "line_count": func_node.end_lineno - func_node.lineno
        if hasattr(func_node, "end_lineno")
        else 0,
    }

    # Critical function detection patterns
    critical_patterns = {
        "dynamic_improvement": [
            "improv",
            "adaptive",
            "threshold",
            "iteration.*prev",
            "similarity.*<",
        ],
        "dependency_handling": [
            "dependency",
            "dep_.*id",
            "validate.*dep",
            "layer.*found",
        ],
        "robust_parsing": ["re\.split", "re\.sub", "clean.*id", "parse.*table"],
        "self_healing": ["best.*result", "history.*track", "error.*recover"],
        "testing_validation": ["test.*scenario", "validate.*result", "check.*function"],
    }

    # Check for critical patterns
    content_lower = content.lower()
    for category, patterns in critical_patterns.items():
        for pattern in patterns:
            if re.search(pattern, content_lower):
                importance["critical"] = True
                importance["reasons"].append(f"{category}: {pattern}")

    # Calculate complexity (simplified)
    importance["complexity"] = importance["line_count"]

    return importance


def identify_critical_functions(script_file: str) -> List[Dict[str, Any]]:
    """Identify all critical functions in a script."""
    try:
        with open(script_file, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)

        critical_functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                importance = analyze_function_importance(node.name, node, content)
                if importance["critical"]:
                    critical_functions.append(importance)

        # Sort by importance (line count as proxy)
        critical_functions.sort(key=lambda x: x["line_count"], reverse=True)

        return critical_functions
    except Exception as e:
        print(f"Error analyzing {script_file}: {e}")
        return []


def check_missing_critical_patterns(old_file: str, new_file: str) -> Dict[str, Any]:
    """Check if new script is missing critical patterns from old script."""
    try:
        with open(old_file, "r") as f:
            old_content = f.read()
        with open(new_file, "r") as f:
            new_content = f.read()
    except Exception as e:
        return {"error": f"Could not read files: {e}"}

    # Critical patterns that should not be lost
    critical_patterns = {
        "dynamic_improvement": r"(iteration.*>.*1.*and.*prev_results|similarity\s*<\s*0\.7|improvement.*threshold)",
        "robust_parsing": r"(re\.split.*\[,\s\+\]|re\.sub.*\[\^0-9\.\]|table.*row.*\|)",
        "layer_organization": r"(foundation.*layer|dependent.*layer|layer.*foundation)",
        "self_healing": r"(best.*result|iteration.*history|error.*recover)",
        "dependency_validation": r"(dep.*id.*validate|relationship.*type|depends.*on)",
    }

    missing_patterns = {}
    for pattern_name, pattern in critical_patterns.items():
        if re.search(pattern, old_content, re.IGNORECASE):
            if not re.search(pattern, new_content, re.IGNORECASE):
                missing_patterns[pattern_name] = {
                    "pattern": pattern,
                    "severity": "HIGH"
                    if pattern_name in ["dynamic_improvement", "robust_parsing"]
                    else "MEDIUM",
                }

    return missing_patterns


def generate_critical_report(script_files: List[str]) -> Dict[str, Any]:
    """Generate comprehensive report of critical logic across scripts."""
    report = {
        "scripts_analyzed": len(script_files),
        "critical_functions": {},
        "missing_patterns": {},
        "recommendations": [],
    }

    # Analyze each script
    for script_file in script_files:
        if not Path(script_file).exists():
            print(f"❌ File not found: {script_file}")
            continue

        report["critical_functions"][script_file] = identify_critical_functions(
            script_file
        )

    # Check missing patterns between versions
    if len(script_files) >= 2:
        for i in range(1, len(script_files)):
            old_file = script_files[i - 1]
            new_file = script_files[i]

            missing = check_missing_critical_patterns(old_file, new_file)
            if missing and "error" not in missing:
                report["missing_patterns"][f"{old_file} → {new_file}"] = missing

                # Add recommendations
                for pattern_name, info in missing.items():
                    if info["severity"] == "HIGH":
                        report["recommendations"].append(
                            f"🚨 CRITICAL: {new_file} is missing {pattern_name} from {old_file}"
                        )
                    else:
                        report["recommendations"].append(
                            f"⚠️ MEDIUM: {new_file} is missing {pattern_name} from {old_file}"
                        )

    return report


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python critical_logic_identifier.py script1.py script2.py [script3.py ...]"
        )
        print(
            "Example: python critical_logic_identifier.py enhanced_iterative.py advanced_iterative.py"
        )
        sys.exit(1)

    script_files = sys.argv[1:]

    print(f"🔍 Analyzing {len(script_files)} scripts for critical logic...")
    print("=" * 60)

    # Generate report
    report = generate_critical_report(script_files)

    # Print critical functions
    print("\n🚨 CRITICAL FUNCTIONS IDENTIFIED:")
    for script_file, functions in report["critical_functions"].items():
        if functions:
            print(f"\n🔹 {script_file}:")
            for func in functions[:3]:  # Top 3 most critical
                print(f"   🚨 {func['name']} (lines: {func['line_count']})")
                for reason in func["reasons"]:
                    print(f"      - {reason}")
        else:
            print(f"\n🔹 {script_file}: No critical functions identified")

    # Print missing patterns
    if report["missing_patterns"]:
        print("\n❌ MISSING CRITICAL PATTERNS:")
        for transition, missing in report["missing_patterns"].items():
            print(f"\n{transition}:")
            for pattern_name, info in missing.items():
                print(f"   {info['severity']}: {pattern_name}")
                print(f"   Pattern: {info['pattern']}")

    # Print recommendations
    if report["recommendations"]:
        print("\n📋 RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"   {rec}")

    # Exit code based on critical findings
    if any(
        missing.get("severity") == "HIGH"
        for missing in report["missing_patterns"].values()
    ):
        print("\n❌ CRITICAL FUNCTIONALITY LOSS DETECTED!")
        print("🚨 DO NOT PROCEED WITH CONSOLIDATION WITHOUT FIXING!")
        sys.exit(1)
    elif report["missing_patterns"]:
        print("\n⚠️ Some functionality loss detected - Review carefully")
        sys.exit(2)
    else:
        print("\n✅ No critical functionality loss detected")
        print("🎉 Safe to proceed with consolidation!")
        sys.exit(0)


if __name__ == "__main__":
    main()
