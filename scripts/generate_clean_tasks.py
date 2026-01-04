#!/usr/bin/env python3
"""
Generate clean sequential task files (001-020) from the enhanced plan.
This creates a task-master compatible numbering system with clear progression.
"""

from datetime import datetime
from pathlib import Path

# Clean numbering system: 001-020
TASK_PLAN = [
    {
        "id": "001",
        "title": "Framework Strategy Definition",
        "status": "pending",
        "priority": "high",
        "initiative": "Foundational CI/CD & Validation Framework",
        "subtasks": [
            ("001.1", "Define Target Selection Criteria", None),
            ("001.2", "Define Alignment Strategy Framework", "001.1"),
            ("001.3", "Create Documentation Foundation", "001.1, 001.2"),
            (
                "001.4",
                "Define Safety and Verification Procedures",
                "001.1, 001.2, 001.3",
            ),
        ],
        "original": "7 → I1.T0",
    },
    {
        "id": "002",
        "title": "Create Comprehensive Merge Validation Framework",
        "status": "pending",
        "priority": "high",
        "initiative": "Foundational CI/CD & Validation Framework",
        "subtasks": [
            ("002.1", "Define Validation Scope and Tooling", None),
            ("002.2", "Configure GitHub Actions Workflow", "002.1"),
            ("002.3", "Implement Architectural Enforcement Checks", "002.1"),
            ("002.4", "Integrate Unit and Integration Tests", "002.1"),
            ("002.5", "Develop E2E Smoke Tests", "002.1"),
            ("002.6", "Implement Performance Benchmarking", "002.1"),
            ("002.7", "Integrate Security Scans", "002.1"),
            ("002.8", "Consolidate Validation Results", "002.3, 002.4, 002.6, 002.7"),
            ("002.9", "Configure Branch Protection Rules", "002.2"),
        ],
        "original": "9 → I1.T1",
    },
    {
        "id": "003",
        "title": "Develop Pre-merge Validation Scripts",
        "status": "blocked",
        "priority": "high",
        "initiative": "Foundational CI/CD & Validation Framework",
        "subtasks": [
            ("003.1", "Define Critical Files and Validation Criteria", None),
            ("003.2", "Develop Core Validation Script", "003.1"),
            ("003.3", "Develop Unit and Integration Tests", "003.2"),
            ("003.4", "Integrate into CI/CD Pipeline", "003.3"),
            ("003.5", "Document and Communicate Process", "003.4"),
        ],
        "original": "19 → I1.T2",
    },
    {
        "id": "004",
        "title": "Establish Core Branch Alignment Framework",
        "status": "pending",
        "priority": "high",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("004.1", "Review Existing Branch Protections", None),
            ("004.2", "Configure Required Reviewers", None),
            ("004.3", "Enforce Passing Status Checks", None),
            ("004.4", "Enforce Merge Strategies and Linear History", None),
            ("004.5", "Design Local Git Hook Integration", None),
            ("004.6", "Integrate Pre-Merge Scripts into Hooks", "004.5"),
            ("004.7", "Develop Centralized Orchestration Script", "004.6"),
        ],
        "original": "54 → I2.T1",
    },
    {
        "id": "005",
        "title": "Develop Automated Error Detection Scripts",
        "status": "pending",
        "priority": "high",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("005.1", "Develop Merge Conflict Marker Detector", None),
            ("005.2", "Implement Garbled Text and Encoding Error Detector", None),
            ("005.3", "Implement Python Missing Imports Validator", None),
            ("005.4", "Develop Deleted Module Detection Logic", None),
        ],
        "original": "55 → I2.T2",
    },
    {
        "id": "006",
        "title": "Implement Branch Backup and Restore Mechanism",
        "status": "pending",
        "priority": "high",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("006.1", "Develop Feature Branch Backup and Restore", None),
            ("006.2", "Enhance Backup for Primary Branches", "006.1"),
            ("006.3", "Integrate into Automated Workflow", "006.1, 006.2"),
        ],
        "original": "56 → I2.T3",
    },
    {
        "id": "007",
        "title": "Develop Feature Branch Identification Tool",
        "status": "pending",
        "priority": "medium",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("007.1", "Implement Active Branch Identification", None),
            ("007.2", "Implement Git History Analysis", None),
            ("007.3", "Implement Similarity Analysis", None),
            ("007.4", "Implement Branch Age Analysis", None),
            ("007.5", "Integrate Backend-to-Src Migration Analysis", None),
            ("007.6", "Create Structured JSON Output", None),
        ],
        "original": "57 → I2.T4",
    },
    {
        "id": "008",
        "title": "Automate Changes Summary and Checklist Generation",
        "status": "pending",
        "priority": "medium",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("008.1", "Define CHANGES_SUMMARY.md Template", None),
            ("008.2", "Define ALIGNMENT_CHECKLIST.md Template", None),
            ("008.3", "Develop Git Diff Analysis Script", None),
            ("008.4", "Develop Test Results Integration", None),
            ("008.5", "Develop Coverage Report Integration", None),
            (
                "008.6",
                "Develop Template Population Script",
                "008.1, 008.3, 008.4, 008.5",
            ),
            ("008.7", "Develop Alignment Checklist Generator", "008.2"),
            ("008.8", "Implement GitHub PR Description Integration", "008.6"),
            ("008.9", "Implement GitHub PR Comment Integration", "008.6, 008.7"),
            ("009.0", "Develop Documentation Archival System", "008.6, 008.7"),
            ("009.1", "Implement Template Version Control", "008.1, 008.2"),
            ("009.2", "Develop Template Configuration System", "008.1, 008.2"),
            ("009.3", "Develop Template Testing Framework", "008.6, 008.7"),
            ("009.4", "Develop Documentation Website Integration", "008.6, 008.7"),
            ("009.5", "Finalize and Publish Documentation", "008.1-009.4"),
        ],
        "original": "58 → I2.TX (RESTORED)",
    },
    {
        "id": "010",
        "title": "Develop Core Primary-to-Feature Alignment Logic",
        "status": "pending",
        "priority": "high",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("010.1", "Integrate Optimal Primary Target Determination", None),
            ("010.2", "Implement Pre-Alignment Safety Checks", None),
            ("010.3", "Develop Automated Pre-Alignment Backup", None),
            ("010.4", "Implement Core Rebase Operation", None),
            ("010.5", "Develop Conflict Detection and Resolution", None),
            ("010.6", "Implement Intelligent Rollback Mechanisms", None),
            ("010.7", "Design Graceful Error Handling", None),
        ],
        "original": "59 → I2.T5",
    },
    {
        "id": "011",
        "title": "Implement Strategies for Complex Branches",
        "status": "pending",
        "priority": "medium",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("011.1", "Define Complexity Criteria for Branches", None),
            ("011.2", "Develop Iterative Rebase Procedure", None),
            ("011.3", "Implement Integration Branch Strategy", None),
            ("011.4", "Develop Enhanced Conflict Resolution", None),
            ("011.5", "Implement Targeted Testing", None),
        ],
        "original": "60 → I2.T6",
    },
    {
        "id": "012",
        "title": "Integrate Validation into Alignment Workflow",
        "status": "pending",
        "priority": "high",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("012.1", "Define Validation Integration Points", None),
            ("012.2", "Integrate Error Detection Scripts", None),
            ("012.3", "Implement Post-Alignment Validation Trigger", None),
            ("012.4", "Implement Alignment Rollback on Critical Failure", None),
            ("012.5", "Develop Unified Validation Reporting", None),
        ],
        "original": "61 → I2.T7",
    },
    {
        "id": "013",
        "title": "Orchestrate Branch Alignment Workflow",
        "status": "pending",
        "priority": "high",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("013.1", "Integrate Branch Identification Tool", None),
            ("013.2", "Develop Interactive Branch Selection UI", None),
            ("013.3", "Integrate Branch Alignment Logic", None),
            ("013.4", "Integrate Validation Framework", None),
            ("013.5", "Integrate Documentation Generation", None),
            ("013.6", "Develop State Persistence and Recovery", None),
            ("013.7", "Create Progress Reporting Module", None),
        ],
        "original": "62 → I2.T8",
    },
    {
        "id": "014",
        "title": "Establish End-to-End Testing for Framework",
        "status": "pending",
        "priority": "medium",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("014.1", "Design E2E Test Scenarios", None),
            ("014.2", "Implement Test Environment Provisioning", None),
            ("014.3", "Integrate Full Workflow in Test Runner", None),
            ("014.4", "Develop Post-Alignment Verification", None),
            ("014.5", "Implement Automated Reporting", None),
        ],
        "original": "83 → I2.T9",
    },
    {
        "id": "015",
        "title": "Finalize and Publish Documentation",
        "status": "pending",
        "priority": "low",
        "initiative": "Build Core Alignment Framework",
        "subtasks": [
            ("015.1", "Document Branching Strategy", None),
            ("015.2", "Detail Conflict Resolution Procedures", "015.1"),
            ("015.3", "Draft Orchestration Script Usage Guide", None),
            ("015.4", "Verify Documentation Consistency", "015.1, 015.2, 015.3"),
            ("015.5", "Publish Final Documentation", "015.4"),
        ],
        "original": "63 → I2.T10",
    },
    {
        "id": "016",
        "title": "Execute Scientific Branch Recovery",
        "status": "pending",
        "priority": "medium",
        "initiative": "Alignment Execution",
        "subtasks": [
            ("016.1", "Re-verify Branch Differences", None),
            ("016.2", "Identify Core Features to Preserve", None),
            ("016.3", "Perform Incremental Integration", None),
            ("016.4", "Resolve Conflicts", None),
            ("016.5", "Validate Functionality", None),
        ],
        "original": "23 → I3.T1",
    },
    {
        "id": "017",
        "title": "Align All Orchestration-Tools Branches",
        "status": "deferred",
        "priority": "high",
        "initiative": "Alignment Execution",
        "subtasks": [
            ("017.1", "Identify and Catalog Orchestration-Tools Branches", None),
            ("017.2", "Apply Alignment Framework to Each Branch", None),
            ("017.3", "Document Results", None),
        ],
        "original": "101 → I3.T2",
    },
    {
        "id": "018",
        "title": "Implement Regression Prevention Safeguards",
        "status": "blocked",
        "priority": "medium",
        "initiative": "Codebase Stability & Maintenance",
        "subtasks": [
            ("018.1", "Design Pre-merge Deletion Validation", None),
            ("018.2", "Establish Selective Revert Policies", None),
            ("018.3", "Implement Asset Preservation", None),
            ("018.4", "Create Documentation", None),
        ],
        "original": "27 → I4.T1",
    },
    {
        "id": "019",
        "title": "Scan and Resolve Merge Conflicts",
        "status": "deferred",
        "priority": "medium",
        "initiative": "Codebase Stability & Maintenance",
        "subtasks": [
            ("019.1", "Initialize Repository and List Remote Branches", None),
            ("019.2", "Scan Each Branch for Conflict Markers", None),
            ("019.3", "Resolve Identified Conflicts", None),
            ("019.4", "Verify Resolution", None),
        ],
        "original": "31 → I4.T2",
    },
    {
        "id": "020",
        "title": "Refine launch.py Dependencies",
        "status": "blocked",
        "priority": "medium",
        "initiative": "Codebase Stability & Maintenance",
        "subtasks": [
            ("020.1", "Review Task 38 Dependency Analysis", None),
            ("020.2", "Synchronize with requirements.txt", None),
            ("020.3", "Refactor Unused Imports", None),
            ("020.4", "Enhance CI/CD Checks", None),
        ],
        "original": "40 → I4.T3",
    },
]


def generate_task_file(task: dict, output_dir: Path) -> Path:
    """Generate a markdown file for a single task."""

    subtasks_md = ""
    for subtask_id, subtask_title, deps in task["subtasks"]:
        subtasks_md += f"""### {subtask_id}: {subtask_title}

**Purpose:** {subtask_title}

"""
        if deps:
            subtasks_md += f"**Depends on:** {deps}\n\n"
        subtasks_md += "---\n\n"

    success_criteria = "\n".join(f"- [ ] {st[1]}" for st in task["subtasks"])

    md = f"""# Task {task["id"]}: {task["title"]}

**Task ID:** {task["id"]}
**Status:** {task["status"]}
**Priority:** {task["priority"]}
**Initiative:** {task["initiative"]}
**Sequence:** {int(task["id"])} of 20

---

## Purpose

{task["title"]}

---

## Success Criteria

{success_criteria}

---

## Subtasks

{subtasks_md}---

## Implementation Notes

**Generated:** {datetime.now().isoformat()}
**Source:** complete_new_task_outline_ENHANCED.md
**Original Task:** {task["original"]}

"""

    filepath = output_dir / f"task-{task['id']}.md"
    filepath.write_text(md)
    return filepath


def main():
    output_dir = Path("new_task_plan/task_files")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Remove old task files
    for f in output_dir.glob("task-*.md"):
        f.unlink()

    print("Generating clean sequential task files (001-020)...\n")

    for task in TASK_PLAN:
        filepath = generate_task_file(task, output_dir)
        print(f"Created: {filepath.name} ({len(task['subtasks'])} subtasks)")

    print(f"\nGenerated {len(TASK_PLAN)} task files in: {output_dir}")

    # Count total subtasks
    total_subtasks = sum(len(t["subtasks"]) for t in TASK_PLAN)
    print(f"Total subtasks: {total_subtasks}")


if __name__ == "__main__":
    main()
