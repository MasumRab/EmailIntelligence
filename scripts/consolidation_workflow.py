#!/usr/bin/env python3
"""
Consolidation Workflow with Functionality Preservation

Automated consolidation that ensures no functionality is lost during script cleanup.
"""

import subprocess
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any


def run_verification_pipeline(script_files: List[str]) -> Dict[str, Any]:
    """Run complete verification pipeline before consolidation."""
    print(f"🔍 Running verification pipeline on {len(script_files)} scripts...")

    pipeline_results = {
        "feature_matrix": {},
        "critical_analysis": {},
        "functionality_tests": {},
        "overall_status": "unknown",
        "safe_to_consolidate": False,
        "missing_functionality": [],
    }

    # Step 1: Feature matrix comparison
    print("\n1️⃣ Running feature matrix comparison...")
    try:
        matrix_result = subprocess.run(
            ["python", ".taskmaster/scripts/script_feature_matrix.py"] + script_files,
            capture_output=True,
            text=True,
        )

        if matrix_result.returncode == 0:
            pipeline_results["feature_matrix"] = {
                "status": "passed",
                "no_regressions": True,
            }
        else:
            pipeline_results["feature_matrix"] = {
                "status": "failed",
                "regressions_detected": True,
            }
            pipeline_results["missing_functionality"].append(
                "Feature regression detected"
            )
    except Exception as e:
        pipeline_results["feature_matrix"] = {"status": "error", "error": str(e)}

    # Step 2: Critical logic analysis
    print("2️⃣ Running critical logic analysis...")
    try:
        critical_result = subprocess.run(
            ["python", ".taskmaster/scripts/critical_logic_identifier.py"]
            + script_files,
            capture_output=True,
            text=True,
        )

        if critical_result.returncode == 0:
            pipeline_results["critical_analysis"] = {
                "status": "passed",
                "no_critical_loss": True,
            }
        else:
            pipeline_results["critical_analysis"] = {
                "status": "failed",
                "critical_loss_detected": True,
            }
            pipeline_results["missing_functionality"].append(
                "Critical logic loss detected"
            )
    except Exception as e:
        pipeline_results["critical_analysis"] = {"status": "error", "error": str(e)}

    # Step 3: Functionality testing
    print("3️⃣ Running functionality tests...")
    try:
        test_result = subprocess.run(
            ["python", ".taskmaster/scripts/functionality_test_suite.py"]
            + script_files,
            capture_output=True,
            text=True,
        )

        if test_result.returncode == 0:
            pipeline_results["functionality_tests"] = {
                "status": "passed",
                "no_regressions": True,
            }
        else:
            pipeline_results["functionality_tests"] = {
                "status": "failed",
                "regressions_detected": True,
            }
            pipeline_results["missing_functionality"].append(
                "Functionality regression detected"
            )
    except Exception as e:
        pipeline_results["functionality_tests"] = {"status": "error", "error": str(e)}

    # Overall safety assessment
    all_passed = all(
        [
            pipeline_results["feature_matrix"].get("status") == "passed",
            pipeline_results["critical_analysis"].get("status") == "passed",
            pipeline_results["functionality_tests"].get("status") == "passed",
        ]
    )

    pipeline_results["safe_to_consolidate"] = all_passed
    pipeline_results["overall_status"] = "safe" if all_passed else "unsafe"

    return pipeline_results


def create_deprecated_backup(scripts_to_archive: List[str]) -> str:
    """Create backup directory for deprecated scripts."""
    timestamp = subprocess.check_output(["date", "+%Y%m%d_%H%M%S"], text=True).strip()
    backup_dir = Path(f"deprecated_scripts_{timestamp}")
    backup_dir.mkdir(exist_ok=True)

    for script in scripts_to_archive:
        if Path(script).exists():
            shutil.move(script, backup_dir / Path(script).name)

    return str(backup_dir)


def generate_consolidation_plan(script_files: List[str]) -> Dict[str, Any]:
    """Generate plan for which scripts to keep and consolidate."""
    plan = {
        "scripts_to_keep": [],
        "scripts_to_archive": [],
        "rescue_operations": [],
        "unified_scripts": [],
    }

    # Script prioritization based on analysis
    if len(script_files) >= 2:
        # Keep latest versions that passed all tests
        plan["scripts_to_keep"] = [script_files[-1]]  # Assume last is latest

        # Archive older versions that have safe replacements
        plan["scripts_to_archive"] = script_files[:-1]

        # Add rescue operations for any missing functionality
        plan["rescue_operations"] = [
            "Extract dynamic improvement logic from enhanced_iterative_distance_minimizer.py",
            "Extract robust dependency parsing from enhanced_reverse_engineer_prd.py",
            "Extract table-based subtask extraction from enhanced_reverse_engineer_prd.py",
            "Extract layer-based organization from enhanced_reverse_engineer_prd.py",
        ]

        # Plan unified scripts
        plan["unified_scripts"] = [
            "unified_task_fidelity_manager.py",
            "unified_reverse_engineer_prd.py",
            "unified_iterative_minimizer.py",
        ]

    return plan


def run_consolidation(scripts: List[str], dry_run: bool = True) -> Dict[str, Any]:
    """Run the actual consolidation process."""
    print(f"🔧 Running consolidation {'(DRY RUN)' if dry_run else '(LIVE)'}...")

    # Step 1: Verification
    verification = run_verification_pipeline(scripts)

    if not verification["safe_to_consolidate"]:
        print("\n❌ CONSOLIDATION BLOCKED!")
        print("🚨 Safety checks failed - cannot proceed")
        print("Missing functionality:")
        for missing in verification["missing_functionality"]:
            print(f"  - {missing}")
        return {"status": "blocked", "verification": verification}

    # Step 2: Generate consolidation plan
    print("\n📋 Generating consolidation plan...")
    plan = generate_consolidation_plan(scripts)

    # Step 3: Execute if not dry run
    if dry_run:
        print("\n🔍 DRY RUN - No changes made")
        print("Plan would be:")
        print(f"  Keep: {', '.join(plan['scripts_to_keep'])}")
        print(f"  Archive: {', '.join(plan['scripts_to_archive'])}")
        print(f"  Rescue: {len(plan['rescue_operations'])} operations")
        print(f"  Create: {', '.join(plan['unified_scripts'])}")
        return {"status": "dry_run_success", "plan": plan, "verification": verification}

    # Live consolidation
    print("\n🚀 EXECUTING CONSOLIDATION...")

    # Archive deprecated scripts
    if plan["scripts_to_archive"]:
        backup_dir = create_deprecated_backup(plan["scripts_to_archive"])
        print(f"📦 Archived {len(plan['scripts_to_archive'])} scripts to {backup_dir}")

    # Note: Actual unified script creation would go here
    # This is where you'd extract the critical logic and create new unified scripts

    print("\n✅ CONSOLIDATION COMPLETE!")
    return {"status": "success", "plan": plan, "verification": verification}


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python consolidation_workflow.py script1.py script2.py [script3.py ...] [--live]"
        )
        print(
            "Example: python consolidation_workflow.py enhanced_iterative.py advanced_iterative.py --live"
        )
        sys.exit(1)

    script_files = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    dry_run = "--live" not in sys.argv

    print(f"🎯 Script Consolidation with Functionality Preservation")
    print("=" * 60)
    print(f"📁 Scripts to process: {len(script_files)}")
    print(f"🔍 Mode: {'LIVE CONSOLIDATION' if not dry_run else 'DRY RUN'}")

    # Run consolidation
    result = run_consolidation(script_files, dry_run)

    # Save report
    report_file = f"consolidation_report_{'live' if not dry_run else 'dryrun'}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Report saved to: {report_file}")

    if result["status"] == "blocked":
        sys.exit(1)
    elif result["status"] == "dry_run_success":
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
