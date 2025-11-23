"""
Update Statistics Script

Recounts tasks and updates statistics files after renumbering.
"""

import json
from pathlib import Path
from collections import defaultdict


def count_tasks_by_category(consolidated_dir: Path) -> dict:
    """Count tasks in each category directory."""
    category_counts = defaultdict(int)

    for category_dir in consolidated_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue

        # Count .md files that are tasks (not README)
        task_files = [
            f for f in category_dir.glob("*.md")
            if f.name != "README.md" and not f.name.startswith('categories/')
        ]
        category_counts[category_dir.name] = len(task_files)

    return dict(category_counts)


def update_consolidation_summary(consolidated_dir: Path, task_counts: dict):
    """Update the CONSOLIDATION_SUMMARY.md with new statistics."""
    total_tasks = sum(task_counts.values())

    # Calculate percentages
    category_stats = []
    for category, count in task_counts.items():
        percentage = (count / total_tasks * 100) if total_tasks > 0 else 0
        category_stats.append((category, count, percentage))

    # Sort by count descending
    category_stats.sort(key=lambda x: x[1], reverse=True)

    summary_content = f"""# Comprehensive Task Consolidation Summary

**Generated:** Auto-generated from remote branch analysis

## Overall Statistics

- **Branches analyzed:** 23
- **Total tasks extracted:** {total_tasks}
- **Categories created:** {len(task_counts)}

## Category Breakdown

| Category | Tasks | Percentage |
|----------|-------|------------|
"""

    for category, count, percentage in category_stats:
        # Format category name
        display_name = category.replace('_', ' ').title()
        summary_content += f"| {display_name} | {count} | {percentage:.1f}% |\n"

    summary_content += "\n## Categories\n\n"

    # Add category details
    category_details = {
        "consolidation_migration": {
            "name": "Consolidation & Migration",
            "keywords": "consolidat, migrat, centraliz, distribut, worktree, orchestrat, merge, integrat"
        },
        "branch_management": {
            "name": "Branch Management & Alignment",
            "keywords": "branch, align, pr , merge, extract, split, rebase, pull, push"
        },
        "validation_testing": {
            "name": "Validation & Testing",
            "keywords": "validat, test, verif, check, assert, performance, monitor"
        },
        "documentation_research": {
            "name": "Documentation & Research",
            "keywords": "document, research, summary, analysis, review, spec, plan"
        },
        "development_implementation": {
            "name": "Development & Implementation",
            "keywords": "implement, develop, code, feature, function, api, database"
        },
        "security_hardening": {
            "name": "Security & Hardening",
            "keywords": "secur, auth, encrypt, audit, compliance, vulnerab"
        },
        "uncategorized": {
            "name": "Uncategorized",
            "keywords": ""
        }
    }

    for category_key, count in task_counts.items():
        if category_key in category_details:
            details = category_details[category_key]
            summary_content += f"### {details['name']}\n"
            summary_content += f"- **Tasks:** {count}\n"
            summary_content += f"- **Location:** `consolidated/{category_key}/`\n"
            summary_content += f"- **Keywords:** {details['keywords']}\n\n"

    # Write the updated summary
    summary_file = consolidated_dir / "CONSOLIDATION_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)

    print(f"✅ Updated CONSOLIDATION_SUMMARY.md with {total_tasks} total tasks")


def update_master_backlog_header(consolidated_dir: Path, total_tasks: int):
    """Update the master backlog header with new task count."""
    master_file = consolidated_dir / "master_backlog.md"

    try:
        with open(master_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the total tasks line
        import re
        content = re.sub(
            r'\*\*Total Tasks:\*\* \d+',
            f'**Total Tasks:** {total_tasks}',
            content
        )

        with open(master_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated master_backlog.md header with {total_tasks} tasks")

    except Exception as e:
        print(f"❌ Error updating master_backlog.md: {e}")


def main():
    """Main update process."""
    consolidated_dir = Path("/home/masum/github/backlog/consolidated")

    print("🔄 Updating consolidation statistics...")

    # Count tasks by category
    task_counts = count_tasks_by_category(consolidated_dir)
    total_tasks = sum(task_counts.values())

    print(f"📊 Found {total_tasks} total tasks across {len(task_counts)} categories:")
    for category, count in sorted(task_counts.items()):
        print(f"   {category}: {count} tasks")

    # Update files
    update_consolidation_summary(consolidated_dir, task_counts)
    update_master_backlog_header(consolidated_dir, total_tasks)

    print("✅ Statistics update complete!")


if __name__ == "__main__":
    main()