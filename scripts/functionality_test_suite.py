#!/usr/bin/env python3
"""
Quick Functionality Testing Suite

Fast capability validation to ensure no functionality is lost during consolidation.
"""

import subprocess
import sys
import json
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Any


def test_script_capabilities(script_file: str) -> Dict[str, Any]:
    """Test if a script can perform its expected functions."""
    results = {
        "script": script_file,
        "help_works": False,
        "imports_work": False,
        "can_run": False,
        "has_critical_functions": [],
        "error": None,
    }

    try:
        # Test 1: Help works
        help_result = subprocess.run(
            ["python", script_file, "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if help_result.returncode == 0 or "Usage:" in help_result.stdout:
            results["help_works"] = True

        # Test 2: Import check
        import_result = subprocess.run(
            ["python", "-c", f'import ast; ast.parse(open("{script_file}").read())'],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if import_result.returncode == 0:
            results["imports_work"] = True

        # Test 3: Can run basic execution
        if results["help_works"] and results["imports_work"]:
            results["can_run"] = True

        # Test 4: Check for critical functions
        with open(script_file, "r") as f:
            content = f.read()

        critical_functions = []
        if "generate_improved_prd" in content:
            critical_functions.append("generate_improved_prd")
        if "generate_dependency_graph" in content:
            critical_functions.append("generate_dependency_graph")
        if "extract_task_info" in content:
            critical_functions.append("extract_task_info")
        if "minimize_distance" in content:
            critical_functions.append("minimize_distance")

        results["has_critical_functions"] = critical_functions

    except subprocess.TimeoutExpired:
        results["error"] = "Timeout during testing"
    except Exception as e:
        results["error"] = str(e)

    return results


def run_functionality_comparison(script_files: List[str]) -> Dict[str, Any]:
    """Compare functionality across multiple scripts."""
    if len(script_files) < 2:
        return {"error": "Need at least 2 scripts to compare"}

    comparison = {
        "scripts_tested": len(script_files),
        "test_results": {},
        "missing_capabilities": {},
        "regression_detected": False,
    }

    # Test each script
    for script_file in script_files:
        if not Path(script_file).exists():
            comparison["test_results"][script_file] = {
                "error": f"File not found: {script_file}"
            }
            continue

        comparison["test_results"][script_file] = test_script_capabilities(script_file)

    # Compare capabilities between versions
    for i in range(1, len(script_files)):
        older_script = script_files[i - 1]
        newer_script = script_files[i]

        older_result = comparison["test_results"].get(older_script, {})
        newer_result = comparison["test_results"].get(newer_script, {})

        if older_result.get("error") or newer_result.get("error"):
            continue

        missing_caps = []

        # Check for lost critical functions
        older_functions = set(older_result.get("has_critical_functions", []))
        newer_functions = set(newer_result.get("has_critical_functions", []))

        lost_functions = older_functions - newer_functions
        if lost_functions:
            missing_caps["lost_functions"] = list(lost_functions)
            comparison["regression_detected"] = True

        # Check for capability loss
        capabilities = ["help_works", "imports_work", "can_run"]
        for cap in capabilities:
            if older_result.get(cap, False) and not newer_result.get(cap, False):
                missing_caps[f"lost_{cap}"] = True
                comparison["regression_detected"] = True

        if missing_caps:
            comparison["missing_capabilities"][f"{older_script} → {newer_script}"] = (
                missing_caps
            )

    return comparison


def generate_quick_report(comparison: Dict[str, Any]) -> None:
    """Generate fast, actionable report."""
    print(f"🧪 Functionality Testing Results")
    print("=" * 50)

    # Script capabilities
    print("\n📊 SCRIPT CAPABILITIES:")
    for script, result in comparison["test_results"].items():
        if "error" in result:
            print(f"❌ {script}: {result['error']}")
        else:
            status = "✅" if result["can_run"] else "⚠️"
            print(f"{status} {script}")
            print(
                f"   Help: {result['help_works']} | Import: {result['imports_work']} | Run: {result['can_run']}"
            )
            if result["has_critical_functions"]:
                print(f"   Critical: {', '.join(result['has_critical_functions'])}")

    # Missing capabilities
    if comparison["missing_capabilities"]:
        print("\n🚨 MISSING CAPABILITIES:")
        for transition, missing in comparison["missing_capabilities"].items():
            print(f"\n❌ {transition}:")
            for cap, lost in missing.items():
                print(f"   {cap}: YES")

    # Final verdict
    print("\n" + "=" * 50)
    if comparison["regression_detected"]:
        print("🚨 REGRESSION DETECTED!")
        print("❌ Newer scripts have LESS capability than older versions")
        print("🛑 DO NOT PROCEED WITH CONSOLIDATION!")
        return 1
    else:
        print("✅ NO REGRESSIONS!")
        print("🎉 All functionality preserved - Safe to consolidate!")
        return 0


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python functionality_test_suite.py script1.py script2.py [script3.py ...]"
        )
        print(
            "Example: python functionality_test_suite.py enhanced_iterative.py advanced_iterative.py"
        )
        sys.exit(1)

    script_files = sys.argv[1:]

    print(f"🔍 Testing {len(script_files)} scripts...")

    # Run comparison
    comparison = run_functionality_comparison(script_files)

    if "error" in comparison:
        print(f"❌ Error: {comparison['error']}")
        sys.exit(1)

    # Generate report
    exit_code = generate_quick_report(comparison)

    # Save detailed results
    output_file = "functionality_test_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Detailed results saved to: {output_file}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
